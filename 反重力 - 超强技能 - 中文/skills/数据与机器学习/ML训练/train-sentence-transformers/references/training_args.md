# 训练参数

`SentenceTransformerTrainingArguments`、`CrossEncoderTrainingArguments` 和 `SparseEncoderTrainingArguments` 都继承自 Hugging Face 的 `TrainingArguments`，所以 95% 的参数相同。

本参考涵盖真正影响嵌入模型训练的那些参数。

## 推荐的默认集合

从这个开始，只在有理由时改：

```python
from sentence_transformers import SentenceTransformerTrainingArguments
from sentence_transformers.base.sampler import BatchSamplers

args = SentenceTransformerTrainingArguments(
    output_dir="models/my-model",

    # Duration
    num_train_epochs=1,
    # max_steps=10_000,                    # alternative to epochs

    # Batch size
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    gradient_accumulation_steps=1,

    # Optimizer
    learning_rate=2e-5,
    warmup_steps=0.1,                      # transformers v5.2 deprecated `warmup_ratio`; pass the ratio as a float directly to `warmup_steps`
    lr_scheduler_type="linear",
    weight_decay=0.0,

    # Precision
    bf16=True,                             # fp16=True on older GPUs (T4, V100)

    # Sampler (bi-encoder + sparse-encoder)
    batch_sampler=BatchSamplers.NO_DUPLICATES,

    # Eval + checkpointing
    eval_strategy="steps",
    eval_steps=0.1,                        # fraction: 10 evals/epoch, scales with dataset size
    save_strategy="steps",
    save_steps=0.1,                        # keep aligned with eval_steps for load_best_model_at_end
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_NanoBEIR_mean_cosine_ndcg@10",
    greater_is_better=True,

    # Logging
    logging_steps=0.01,                    # fraction: ~100 log lines/epoch
    logging_first_step=True,
    run_name="my-model",
    report_to="trackio",                   # or "wandb", "tensorboard", "mlflow", "none"
)
```

## 持续时间

- `num_train_epochs` —— 最常用。1（大数据集，>500k），3–10（小数据集）。
- `max_steps` —— 想用固定算力预算时替代 epochs。覆盖 `num_train_epochs`。
- 大数据集 1 epoch 都嫌多时，按算力计划选 `max_steps`。

## Batch 大小

有效 batch 大小 = `per_device_train_batch_size × num_gpus × gradient_accumulation_steps`。

经验法则：
- **对比损失（MNRL、GIST、SMNRL）**：把 `per_device_train_batch_size` 推到 VRAM 允许的越高越好。batch 内负例越多 = 梯度越丰富。64–256 典型。
- **回归损失（CoSENTLoss、CosineSimilarityLoss 等）**：batch 大小影响小。16–64 即可。
- **交叉编码器**：batch 大小对质量不那么关键。32–128 典型。
- 装不下目标 per-device batch，用 `gradient_accumulation_steps` 模拟 —— 但对 MNRL 系列损失，这 **不会** 带来与真 batch 同样的收益（batch 内负例仍然只是 per-device）。改用 `CachedMultipleNegativesRankingLoss`。

## 学习率与调度

- `2e-5` 是 BERT 系 encoder 全参数微调的安全默认。
- LoRA / PEFT adapter 用 `1e-4` 到 `5e-4`。
- `StaticEmbedding` 从零训练用 `2e-1`（远高于 transformer，因为每个 token 都是自由浮动的向量，没有上游梯度）。
- `lr_scheduler_type="linear"` 配合 `warmup_steps=0.1` 是标准（`< 1` 的 float 被解释为总步数的比例）。`"cosine"` 同样好用；非常短的运行用 `"constant_with_warmup"` 即可。legacy `warmup_ratio` 在 transformers v5.2 中弃用，改成 `warmup_steps` 接 float；传 `warmup_ratio=...` 仍能用但会发 DeprecationWarning。
- loss 出现 NaN 时，**先降 LR**。

## 精度

**不可协商规则：** 以 **fp32** 加载模型（默认 —— 不要给 model 构造或 `model_kwargs` 传 `torch_dtype=torch.bfloat16`）。用下面的 `bf16=True` / `fp16=True` 标志启用 **autocast**，而不是权重转换。trainer 把模型和 optimizer state 保留在 fp32，在 forward/backward 时把激活 autocast 到 bf16/fp16。这保留了 Adam 的全精度动量，同时给你大部分 bf16 吞吐。

在创建 optimizer *之前* 把权重 cast 到 bf16 会让 Adam state（`exp_avg`、`exp_avg_sq`）也进入 bf16 —— bf16 的 7-bit 尾数对小梯度动量太粗，会跨运行出现静默质量回退。

| 标志 | 何时用 |
|---|---|
| `bf16=True` | Ampere（A10G、A100、3090）及更新（Hopper、Ada）。支持时优先选 —— 比 fp16 数值上更稳定。仅激活；权重保持 fp32。 |
| `fp16=True` | 旧 GPU（T4、V100、2080、Titan V）。准备好看到 NaN 时降 LR 或开 loss scaling。仅激活；权重保持 fp32。 |
| 都不设 | 全程 fp32。慢；只用于调试数值问题。 |

不要同时设 `bf16=True` 和 `fp16=True`。

**trainer 外的 evaluator 调用**（通常是预训练基线 + 一次训练后 pass）用不到 trainer 的 autocast。手动包一层加速 —— 注意这种 wrap **只在模型用 `attn_implementation="flash_attention_2"` 时才严格必需**，因为 FA2 kernel 需要 bf16/fp16 输入才能工作。不用 FA2 时这是吞吐优化，不是正确性要求：

```python
import torch
from contextlib import nullcontext

def autocast_ctx():
    if not torch.cuda.is_available():
        return nullcontext()
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return torch.autocast("cuda", dtype=dtype)

with autocast_ctx():
    evaluator(model)            # baseline
trainer.train()
with autocast_ctx():
    evaluator(model)            # post-training
```

**FlashAttention 2** 要 bf16/fp16 输入但不要求 bf16 权重。传 `model_kwargs={"attn_implementation": "flash_attention_2"}` *不要* 带 `torch_dtype`，让 `bf16=True` autocast 给 FA2 喂 bf16 激活。权重保持 fp32，optimizer state 保持 fp32。

## Batch 采样器（双编码器 + 稀疏编码器）

`batch_sampler=BatchSamplers.NO_DUPLICATES` 对对比损失至关重要。否则同一 (anchor, positive) 会在一个 batch 中出现多次，把真正的正例变成假负例。

MNRL / SMNRL / CachedMNRL / GIST 用 `BatchSamplers.NO_DUPLICATES`（默认推荐）；batch 三元组损失（`BatchAllTripletLoss`、`BatchHardTripletLoss`）用 `BatchSamplers.GROUP_BY_LABEL`；仅在每 batch 字符串比较太慢的很大数据集上用 `BatchSamplers.NO_DUPLICATES_HASHED`。

多数据集训练，类似的 `MultiDatasetBatchSamplers` 类控制如何从各数据集采样（`ROUND_ROBIN`、`PROPORTIONAL`）。DDP 下，每个数据集自动 per-process 分片 —— 无需额外配置；设一次 `multi_dataset_batch_sampler=...`，单卡和 N 卡跑行为一致。

## 评估与 checkpoint

```python
eval_strategy="steps",
eval_steps=0.1,                        # evaluate every 10% of training
save_strategy="steps",
save_steps=0.1,                        # save at the same cadence (required for load_best_model_at_end)
save_total_limit=2,
load_best_model_at_end=True,
metric_for_best_model="eval_<EvaluatorName>_<metric>",
greater_is_better=True,
```

**优先用比例值而非绝对步数。** `eval_steps=0.1` / `save_steps=0.1` / `logging_steps=0.01` 被解释为总训练步数的比例（每个 epoch 10 次 eval、100 行日志），并随数据集大小或 epoch 数自动扩展。HF Trainer 在初始化时把 `< 1` 的 float 转成 `int(total_steps * fraction)`，所以同一份配置在 10k 或 10M 行上都能用 —— 不用每次重算绝对步数。

仅在有具体原因时用绝对整数（如 `eval_steps=500`）：在已知步数上比较运行，或 `max_steps` 设成让比例不好用的特殊值。

不可协商规则：
1. `load_best_model_at_end=True` 时 `save_steps` 必须是 `eval_steps` 的倍数（或相等），这样 best-eval checkpoint 确实在盘上。让两者相等最简单（如都是 `0.1`）。
2. 如果 `eval_strategy="steps"` 且没传 `eval_dataset`，训练会卡住。要么给 eval 数据集，要么设 `eval_strategy="no"`。
3. `metric_for_best_model` 必须与 evaluator 写的 key 完全匹配。模式一般是 `f"eval_{evaluator.primary_metric}"`。常见取值：
   - `NanoBEIREvaluator`（双编码器，cosine）：`eval_NanoBEIR_mean_cosine_ndcg@10`
   - `SparseNanoBEIREvaluator`（稀疏，dot）：`eval_NanoBEIR_mean_dot_ndcg@10`
   - `CrossEncoderNanoBEIREvaluator`（从 BM25 top-100 重排）：`eval_NanoBEIR_R100_mean_ndcg@10`
   - `EmbeddingSimilarityEvaluator(name="sts-dev")`：`eval_sts-dev_spearman_cosine`

## 早停

通过 `callbacks=[...]` 加 `EarlyStoppingCallback`：

```python
from transformers import EarlyStoppingCallback

trainer = SentenceTransformerTrainer(
    ..., callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)
```

这要求 `load_best_model_at_end=True` 和 `metric_for_best_model=...` 都设好。

`early_stopping_patience=3` 意为"3 个连续 eval 轮次里 best 指标都没改善就停"。用 `early_stopping_threshold=0.001` 要求最小改善幅度。

**真正起作用时：**
- **交叉编码器**：强烈推荐。CE 重排器通常在训练中段达峰然后退化 —— best checkpoint 很少是最后一个。早停省算力 *并* 防止质量回退。
- **双编码器和稀疏编码器**：通常 plateau 而不是回退，所以早停触发频率低得多。`load_best_model_at_end=True` 单独就能给你正确的最终模型；加 callback 是 belt-and-suspenders 安全网。

## 恢复训练

`trainer.train(resume_from_checkpoint=True)` 从 `output_dir` 中最新 checkpoint 恢复。传具体路径可从具体 step 恢复：`resume_from_checkpoint="models/my-model/checkpoint-500"`。

跨恢复持久化的状态：optimizer、scheduler、random seed、trainer step counter。**不**持久的：`IterableDataset` 的数据集迭代顺序 —— 如果用 streaming 数据集，必须自己处理恢复。

## Hub 推送

`push_to_hub=True` + `hub_model_id="your-username/my-model"` + `hub_strategy="every_save"` 是标准模式。在 HF Jobs 上，提交任务时再传 `secrets={"HF_TOKEN": "$HF_TOKEN"}`。四个 `hub_strategy` 取值：`"every_save"`（每个 checkpoint，HF Jobs 强制）、`"end"`（只最终）、`"checkpoint"`（最新，覆盖）、`"all_checkpoints"`（每个作为独立 commit）。

## 日志

```python
logging_steps=0.01,             # fraction: ~100 log lines per epoch (use an int for a fixed cadence)
logging_first_step=True,        # log before any training; useful sanity check
logging_dir=None,               # defaults to output_dir/runs
report_to="trackio",            # or ["trackio", "tensorboard"] for multiple; "none" disables all
run_name="meaningful-name",     # shown in the tracker UI
```

**Tracker 推荐：**
- **Trackio**（默认）适合个人 / 小团队：除了 `HF_TOKEN` 没别的开销。第一次跑时在 `https://huggingface.co/spaces/<your-username>/trackio` 自动建 Space；之后的 run 会追加并按 `run_name` 分组。
- **W&B** 适合大团队或 sweep / report 功能。`pip install wandb && wandb login`（或设 `WANDB_API_KEY`）。
- **TensorBoard** 适合隔离环境。无远程面板。
- **MLflow** 已是组织标准时。

对 trackio sweep / 消融，训练前用 `trackio.init(project="...", name="...", group="v1", config={...})` 把相关 run 并排分组。不用 `trackio.init()`，默认值由 `run_name` 和 HF 用户名派生。

**Tracker 坑：**
- `report_to="all"` 启用所有已装集成（通常比你要的多）；`"none"` 关闭所有（当前 `transformers` 默认）。始终显式设。
- HF Jobs 上的 Trackio 没有 `secrets={"HF_TOKEN": "$HF_TOKEN"}` 会静默失败。HF Jobs 上的 W&B 需要 `secrets` 中加 `WANDB_API_KEY`。
- DDP 下 HF Trainer 只在 rank 0 log；脚本中的自定义日志可能需要显式 rank 检查以避免重复写。

## 显存节省参数

```python
gradient_checkpointing=True,    # trades compute for memory. ~30% slowdown, ~40% less memory.
gradient_checkpointing_kwargs={"use_reentrant": False},
torch_empty_cache_steps=1000,   # periodically clear PyTorch allocator cache
dataloader_num_workers=2,       # parallel data loading; 2-4 is usually enough
dataloader_pin_memory=True,
```

**不要**把 `gradient_checkpointing=True` 与任何 `Cached*` 损失混用 —— 冲突。

## 超参搜索

`trainer.hyperparameter_search(...)` 通过 Hugging Face 的 `Trainer` API 在所有三个 trainer 上都支持（后端 Optuna、Ray Tune、Sigopt 或 W&B）。

最小示例：

```python
def model_init(trial):
    return SentenceTransformer("microsoft/mpnet-base")

def hp_space(trial):
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-6, 1e-4, log=True),
        "num_train_epochs": trial.suggest_int("num_train_epochs", 1, 3),
        "per_device_train_batch_size": trial.suggest_categorical(
            "per_device_train_batch_size", [32, 64, 128]
        ),
    }

trainer = SentenceTransformerTrainer(
    model=None, model_init=model_init,
    args=args, train_dataset=train_dataset, eval_dataset=eval_dataset,
    loss=lambda model: MultipleNegativesRankingLoss(model),   # function that takes model -> loss
    evaluator=evaluator,
)

best_run = trainer.hyperparameter_search(
    hp_space=hp_space,
    direction="maximize",
    n_trials=10,
    backend="optuna",
)
print(best_run)
```

装后端：`pip install optuna`（或 `ray[tune]`）。

HPO 很贵。在单次手调运行端到端工作之前别碰它。对多数生产模型，从上面范围挑合理 LR 再调 batch 大小就够了。

## 多任务训练参数（简述）

在 dict 数据集 + dict 损失上训练时，加：

```python
multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL,  # or ROUND_ROBIN
```

见 `../scripts/train_sentence_transformer_multi_dataset_example.py`（docstring 涵盖 per-dataset 损失、单损失 + DatasetDict 变体、采样器、坑）。

## 不要

- 不要设 `eval_strategy="epoch"` 但不设 `save_strategy="epoch"` —— checkpoint / eval 对齐对 `load_best_model_at_end` 重要。
- 除非有自定义 collator 要用损失看不到的元数据列，否则不要设 `remove_unused_columns=False`。默认（True）更安全 —— 自动丢未用列。
- 不要为了"验证可复现性"设 `seed` 然后期望不同 GPU 或 PyTorch 版本间逐 bit 一致 —— 跨硬件的逐 bit 可复现性不被保证。
- 除非有具体理由，不要调 `adam_beta1` / `adam_beta2` / `adam_epsilon`。99% 的情况默认就够。
