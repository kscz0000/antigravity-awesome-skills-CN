# Hugging Face Jobs 执行

在 Hugging Face 托管 GPU 上跑训练，无需自建任何基础设施。同一份训练脚本本地和 Jobs 都能跑 —— 本参考只涵盖 Jobs 特有的注意事项。

## 前置依赖

- Hugging Face 账户有 **Pro、Team 或 Enterprise** 套餐。Jobs 是付费的。
- `HF_TOKEN` 带 **write** 权限。在本地用 `hf auth login` 登录一次（`hf` CLI 的现代命令；旧的 `huggingface-cli login` 仍能用，但已弃用）。
- 接入 `hf_jobs()` MCP 工具，或 `hf` CLI。如果从托管脚本安装 CLI，下载到临时文件、审阅后再在本地跑。

## 三种提交路径

### 1. 通过 MCP 内联脚本（在 Claude Code 中推荐）

把完整训练脚本作为 `script` 传入。依赖来自 PEP 723 header。

```python
hf_jobs("uv", {
    "script": """
# /// script
# requires-python = ">=3.10"
# dependencies = ["sentence-transformers[train]>=5.0", "trackio"]
# ///

# <full training script content>
""",
    "flavor": "a10g-large",
    "timeout": "3h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

### 2. 通过 MCP 用 URL 提交脚本

把脚本上传到 Hub（作为 model 或 dataset 仓库文件）或 Gist，再通过 URL 引用：

```python
hf_jobs("uv", {
    "script": "https://huggingface.co/USERNAME/scripts/resolve/main/train_bi_encoder.py",
    "flavor": "a10g-large",
    "timeout": "3h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

本地文件路径（`./train.py`、`/path/to/train.py`）**不可用** —— Jobs 在与你的文件系统隔离的容器中运行。

### 3. CLI

```bash
hf jobs uv run \
    --flavor a10g-large \
    --timeout 3h \
    --secrets HF_TOKEN \
    "https://huggingface.co/USERNAME/scripts/resolve/main/train.py"
```

语法注意：
- 命令顺序是 `hf jobs uv run`，**不是** `hf jobs run uv`。
- 标志（`--flavor`、`--timeout`、`--secrets`）放在脚本 URL **之前**。
- `--secrets`（复数），不是 `--secret`。

## Jobs 必需的脚本修改

往你的 `TrainingArguments` 里加这些：

```python
args = SentenceTransformerTrainingArguments(
    ...,
    push_to_hub=True,
    hub_model_id="your-username/my-model",
    hub_strategy="every_save",        # push each checkpoint; timeout-safe
    save_strategy="steps",
    save_steps=0.1,                   # 10 saves/pushes per epoch; scales with dataset size
)
```

各项的作用：

| 参数 | 原因 |
|---|---|
| `push_to_hub=True` | Jobs 容器在任务结束后会被销毁。没有 Hub 推送，权重全部丢失。 |
| `hub_model_id` | 标识目标 repo 必需。 |
| `hub_strategy="every_save"` | 默认行为，但在 Jobs 上值得显式：每个 checkpoint 写入时即推送，超时也能留下已完成的 checkpoint。`"end"` 只在 `trainer.train()` 返回时推一次，超时则全丢。 |
| `save_strategy="steps"` + `save_steps=0.1` | 必须真存 checkpoint，`hub_strategy="every_save"` 才有东西可推。`0.1` 这种小数 = 每 10% 训练存一次，随数据量自动扩展。 |

## 密钥

密钥是注入到 Jobs 容器中的环境变量。它们不会出现在日志中，也不属于脚本的一部分。

| 密钥 | 何时需要 |
|---|---|
| `HF_TOKEN` | 始终需要，用于 Hub 推送。也覆盖 Trackio 鉴权。 |
| `WANDB_API_KEY` | 使用 `report_to="wandb"` 时。 |
| `MLFLOW_TRACKING_URI`、`MLFLOW_TRACKING_TOKEN` | 用 MLflow 配远程 server 时。 |

任务配置里的 `$HF_TOKEN` 语法会在提交时从你的本地环境取值 —— 字面量 `$HF_TOKEN` 会被替换成你的 token 值。永远不要在脚本里硬编码 token。

Trackio（本技能默认 tracker）用 `HF_TOKEN` 鉴权，所以无需额外密钥。除非你用 W&B / MLflow，否则不用管上面那两行。

## 超时

默认 **30 分钟**，对几乎所有真实训练都太短。显式设置：

```python
"timeout": "2h"       # 2 hours
"timeout": "90m"      # 90 minutes
"timeout": "1.5h"     # 90 minutes
"timeout": 7200       # seconds, as integer
```

规则：**估计训练时间 × 1.3**。额外缓冲覆盖模型加载、数据集缓存、检查点保存和 Hub 推送。

超时后容器会立即被杀掉。只有 Hub 上的数据（`hub_strategy="every_save"` 在这里救命）或持久卷里的内容能活下来。

## 数据集缓存

Hugging Face 数据集默认缓存在 `~/.cache/huggingface/datasets` —— **在容器内部**，任务结束就销毁。每次 Jobs 跑都要重新下载数据集。

对大数据集（>5 GB）这就有影响了。可选方案：
- **持久 `/data` 卷**（Jobs 功能，查阅最新文档）：设 `HF_DATASETS_CACHE=/data/datasets` 让缓存跨任务持久。
- **本地预缓存，推到 Hub**：数据集已经在 Hub 上则什么都不用做。如果只在本地，用 `dataset.push_to_hub(...)` 推一次，后续任务直接从 Hub 加载。

## 监控运行中的任务

```bash
hf jobs ps [--all]                        # running (or all) jobs
hf jobs inspect <job-id>                  # full config + status
hf jobs logs <job-id> [--follow|--tail N] # tail or stream
hf jobs cancel <job-id>
hf jobs hardware                          # list flavors + hourly rates
```

`hf jobs logs <id> --follow` 在 `Bash run_in_background` 下，配合一个 `Monitor` 监听训练脚本 verdict 块输出的 `VERDICT:` 行，效果很好。

MCP 等价（签名因 server 版本而异 —— 看实际工具列表）：`hf_jobs("ps")`、`hf_jobs("logs", {"job_id": ...})`、`hf_jobs("cancel", {"job_id": ...})`。

对于周期性运行，`hf jobs scheduled uv run "<cron>" <script> ...` 可调度；`hf jobs scheduled ps/suspend/delete` 管理。

## 常见失败

### 跑完后报"Model not found on Hub"

跑成功了但 `push_to_hub` 没开。容器没了，权重也没了。
修：始终设 `push_to_hub=True` + `hub_model_id=...` + `secrets={"HF_TOKEN": "$HF_TOKEN"}`。

### Tracker 连不上

- **Trackio：** 缺 `HF_TOKEN` 或没有 write 权限。加 `"secrets": {"HF_TOKEN": "$HF_TOKEN"}` 并确保 token 有写权限。
- **W&B：** 缺 `WANDB_API_KEY`。加 `"secrets": {"HF_TOKEN": "$HF_TOKEN", "WANDB_API_KEY": "$WANDB_API_KEY"}`。

### 第一步就 OOM

flavor 太小。升一档（见 `hardware_guide.md`）。

### 训练启动但 eval 永远卡住

`eval_strategy="steps"` 但没给 `eval_dataset`。始终提供 eval 数据集，或者设 `eval_strategy="no"`。

### 数据集下载超时

大数据集或冷启动缓存慢。增大 `timeout` 或预缓存到持久卷。

### `CachedMultipleNegativesRankingLoss` + `gradient_checkpointing=True` 崩溃

Cached 损失与 gradient checkpointing 不兼容。关掉 `gradient_checkpointing`。

提交后，MCP 返回 job id。想看进度时用 `hf_jobs("logs", {"job_id": ...})` —— 不要在紧凑循环里轮询。端到端提交模板在 `scripts/train_sentence_transformer_example.py` / `scripts/train_cross_encoder_example.py` / `scripts/train_sparse_encoder_example.py`；把脚本内容包在 §1 的内联模板里。
