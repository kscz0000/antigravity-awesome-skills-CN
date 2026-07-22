# 使用示例

本文档提供针对 **在 Hugging Face Hub 模型上本地运行评估** 的实用示例。

## 本技能涵盖的内容

- `inspect-ai` 本地运行
- 使用 `vllm` 或 Transformers 后端的 `inspect-ai`
- 使用 `vllm` 或 `accelerate` 的 `lighteval` 本地运行
- 冒烟测试和后端回退模式

## 本技能未涵盖的内容

- `model-index`
- `.eval_results`
- 社区评估发布工作流
- model-card PR 创建
- Hugging Face Jobs 编排

如果想要远程运行这些相同的脚本，使用 `hugging-face-jobs` 技能并传递 `scripts/` 中的某个脚本。

## 环境准备

```bash
cd skills/hugging-face-evaluation
export HF_TOKEN=hf_xxx
uv --version
```

对于本地 GPU 运行：

```bash
nvidia-smi
```

## inspect-ai 示例

### 快速冒烟测试

```bash
uv run scripts/inspect_eval_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu \
  --limit 10
```

### 使用 vLLM 的本地 GPU

```bash
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-8B-Instruct \
  --task gsm8k \
  --limit 20
```

### Transformers 回退

```bash
uv run scripts/inspect_vllm_uv.py \
  --model microsoft/phi-2 \
  --task mmlu \
  --backend hf \
  --trust-remote-code \
  --limit 20
```

## lighteval 示例

### 单任务

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --tasks "leaderboard|mmlu|5" \
  --max-samples 20
```

### 多任务

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5" \
  --max-samples 20 \
  --use-chat-template
```

### accelerate 回退

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model microsoft/phi-2 \
  --tasks "leaderboard|mmlu|5" \
  --backend accelerate \
  --trust-remote-code \
  --max-samples 20
```

## 转交给 Hugging Face Jobs

当本地硬件不足时，切换到 `hugging-face-jobs` 技能并远程运行这些脚本之一。保留脚本路径和参数；将编排工作移至那里。
