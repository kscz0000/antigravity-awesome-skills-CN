---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-community-evals"
name: hugging-face-community-evals
description: 使用 inspect-ai 或 lighteval 对 Hugging Face Hub 模型运行本地评估。
risk: unknown
---

# 概述

## 适用场景
适用于本地模型评估、后端选择和 GPU 冒烟测试，在 Hugging Face Jobs 工作流之外进行。

本技能用于**在本地硬件上对 Hugging Face Hub 上的模型运行评估**。

涵盖内容：
- `inspect-ai` 本地推理
- `lighteval` 本地推理
- `vllm`、Hugging Face Transformers 和 `accelerate` 的选择
- 冒烟测试、任务选择和后端回退策略

不涵盖内容：
- Hugging Face Jobs 编排
- model-card 或 `model-index` 编辑
- README 表格提取
- Artificial Analysis 导入
- `.eval_results` 生成或发布
- PR 创建或 community-evals 自动化

如果用户想要**在 Hugging Face Jobs 上远程运行相同的评估**，转交 `hugging-face-jobs` 技能，并传递本技能中的某个本地脚本。

如果用户想要**将结果发布到社区评估工作流**，在生成评估运行后停止，并将该发布步骤转交 `~/code/community-evals`。

> 以下所有路径均相对于包含此 `SKILL.md` 的目录。

# 脚本选择指南

| 使用场景 | 脚本 |
|---|---|
| 通过推理提供商对 Hub 模型运行本地 `inspect-ai` 评估 | `scripts/inspect_eval_uv.py` |
| 使用 `vllm` 或 Transformers 在本地 GPU 上运行 `inspect-ai` 评估 | `scripts/inspect_vllm_uv.py` |
| 使用 `vllm` 或 `accelerate` 在本地 GPU 上运行 `lighteval` 评估 | `scripts/lighteval_vllm_uv.py` |
| 额外命令模式 | `examples/USAGE_EXAMPLES.md` |

# 前置条件

- 本地执行优先使用 `uv run`。
- 对于受限/私有模型，设置 `HF_TOKEN`。
- 本地 GPU 运行前，验证 GPU 访问权限：

```bash
uv --version
printenv HF_TOKEN >/dev/null
nvidia-smi
```

如果 `nvidia-smi` 不可用，可以：
- 使用 `scripts/inspect_eval_uv.py` 进行更轻量的提供商支持评估，或
- 如果用户需要远程计算，转交 `hugging-face-jobs` 技能。

# 核心工作流

1. 选择评估框架。
   - 需要显式任务控制和 inspect 原生流程时使用 `inspect-ai`。
   - 基准测试自然表达为 lighteval 任务字符串时使用 `lighteval`，特别是排行榜风格任务。
2. 选择推理后端。
   - 支持的架构优先使用 `vllm` 以获得吞吐量。
   - 使用 Hugging Face Transformers（`--backend hf`）或 `accelerate` 作为兼容性回退。
3. 从冒烟测试开始。
   - `inspect-ai`：添加 `--limit 10` 或类似参数。
   - `lighteval`：添加 `--max-samples 10`。
4. 冒烟测试通过后再扩展规模。
5. 如果用户需要远程执行，将相同脚本和参数转交 `hugging-face-jobs`。

# 快速开始

## 选项 A：inspect-ai 本地推理提供商路径

适用于模型已被 Hugging Face Inference Providers 支持，且需要最低本地设置开销的场景。

```bash
uv run scripts/inspect_eval_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu \
  --limit 20
```

适用场景：
- 需要快速本地冒烟测试
- 不需要直接 GPU 控制
- 任务已存在于 `inspect-evals`

## 选项 B：本地 GPU 上的 inspect-ai

适用于需要直接加载 Hub 模型、使用 `vllm`，或对不支持的架构回退到 Transformers 的场景。

本地 GPU：

```bash
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task gsm8k \
  --limit 20
```

Transformers 回退：

```bash
uv run scripts/inspect_vllm_uv.py \
  --model microsoft/phi-2 \
  --task mmlu \
  --backend hf \
  --trust-remote-code \
  --limit 20
```

## 选项 C：本地 GPU 上的 lighteval

适用于任务自然表达为 `lighteval` 任务字符串的场景，特别是 Open LLM Leaderboard 风格基准测试。

本地 GPU：

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5" \
  --max-samples 20 \
  --use-chat-template
```

`accelerate` 回退：

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model microsoft/phi-2 \
  --tasks "leaderboard|mmlu|5" \
  --backend accelerate \
  --trust-remote-code \
  --max-samples 20
```

# 远程执行边界

本技能明确止步于**本地执行和后端选择**。

如果用户想要：
- 在 Hugging Face Jobs 上运行这些脚本
- 选择远程硬件
- 向远程作业传递密钥
- 调度周期性运行
- 检查/取消/监控作业

则切换到 **`hugging-face-jobs`** 技能，并传递其中一个脚本及所选参数。

# 任务选择

`inspect-ai` 示例：
- `mmlu`
- `gsm8k`
- `hellaswag`
- `arc_challenge`
- `truthfulqa`
- `winogrande`
- `humaneval`

`lighteval` 任务字符串格式为 `suite|task|num_fewshot`：
- `leaderboard|mmlu|5`
- `leaderboard|gsm8k|5`
- `leaderboard|arc_challenge|25`
- `lighteval|hellaswag|0`

多个 `lighteval` 任务可在 `--tasks` 中用逗号分隔。

# 后端选择

- 支持的架构上优先使用 `inspect_vllm_uv.py --backend vllm` 获得快速 GPU 推理。
- `vllm` 不支持该模型时使用 `inspect_vllm_uv.py --backend hf`。
- 支持的模型上优先使用 `lighteval_vllm_uv.py --backend vllm` 获得吞吐量。
- 使用 `lighteval_vllm_uv.py --backend accelerate` 作为兼容性回退。
- Inference Providers 已覆盖该模型且不需要直接 GPU 控制时使用 `inspect_eval_uv.py`。

# 硬件建议

| 模型规模 | 建议本地硬件 |
|---|---|
| `< 3B` | 消费级 GPU / Apple Silicon / 小型开发 GPU |
| `3B - 13B` | 更强的本地 GPU |
| `13B+` | 高内存本地 GPU 或转交 `hugging-face-jobs` |

冒烟测试优先使用更便宜的本地运行加上 `--limit` 或 `--max-samples`。

# 故障排查

- CUDA 或 vLLM OOM：
  - 降低 `--batch-size`
  - 降低 `--gpu-memory-utilization`
  - 切换到更小的模型进行冒烟测试
  - 必要时转交 `hugging-face-jobs`
- 模型不被 `vllm` 支持：
  - `inspect-ai` 切换到 `--backend hf`
  - `lighteval` 切换到 `--backend accelerate`
- 受限/私有仓库访问失败：
  - 验证 `HF_TOKEN`
- 需要自定义模型代码：
  - 添加 `--trust-remote-code`

# 示例

参见：
- `examples/USAGE_EXAMPLES.md` 查看本地命令模式
- `scripts/inspect_eval_uv.py`
- `scripts/inspect_vllm_uv.py`
- `scripts/lighteval_vllm_uv.py`

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不应替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，应停止并请求澄清。
