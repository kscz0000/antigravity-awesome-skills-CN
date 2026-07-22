# macOS（Apple Silicon）本地训练

在 Mac 上本地运行小型 LoRA 微调任务用于冒烟测试和快速迭代，然后提交到 HF Jobs。

## 何时使用本地 Mac vs HF Jobs

| 本地 Mac | HF Jobs / 云 GPU |
|-----------|-------------------|
| 模型 ≤3B，仅文本 | 模型 7B+ |
| 仅 LoRA/PEFT | QLoRA 4-bit（CUDA/bitsandbytes）|
| 短上下文（≤1024）| 长上下文 / 全量微调 |
| 冒烟测试、数据集验证 | 生产运行、VLM |

**典型工作流：** 本地冒烟测试 → HF Jobs 使用相同配置 → 导出/量化（[gguf_conversion.md](gguf_conversion.md)）

## 推荐默认值

| 设置 | 值 | 备注 |
|---------|-------|-------|
| 模型大小 | 首次运行 0.5B–1.5B | 验证后再扩展 |
| 最大序列长度 | 512–1024 | 越小越省内存 |
| 批次大小 | 1 | 通过梯度累积扩展 |
| 梯度累积 | 8–16 | 有效批次 = 8–16 |
| LoRA 秩 (r) | 8–16 | alpha = 2×r |
| Dtype | float32 | fp16 在 MPS 上导致 NaN；bf16 仅在 M1 Pro+ 和 M2/M3/M4 上 |

### 硬件对应的内存

| 统一内存 | 最大模型大小 |
|-------------|---------------|
| 16 GB | ~0.5B–1.5B |
| 32 GB | ~1.5B–3B |
| 64 GB | ~3B（短上下文）|

## 设置

```bash
xcode-select --install
python3 -m venv .venv && source .venv/bin/activate
pip install -U "torch>=2.2" "transformers>=4.40" "trl>=0.12" "peft>=0.10" \
    datasets accelerate safetensors huggingface_hub
```

验证 MPS：
```bash
python -c "import torch; print(torch.__version__, '| MPS:', torch.backends.mps.is_available())"
```

可选 — 为本地 Mac 配置 Accelerate（无分布式、无混合精度、MPS 设备）：
```bash
accelerate config
```

## 训练脚本

<details>
<summary><strong>train_lora_sft.py</strong></summary>

```python
import os
from dataclasses import dataclass
from typing import Optional
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

set_seed(42)

@dataclass
class Cfg:
    model_id: str = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")
    dataset_id: str = os.environ.get("DATASET_ID", "HuggingFaceH4/ultrachat_200k")
    dataset_split: str = os.environ.get("DATASET_SPLIT", "train_sft[:500]")
    data_files: Optional[str] = os.environ.get("DATA_FILES", None)
    text_field: str = os.environ.get("TEXT_FIELD", "")
    messages_field: str = os.environ.get("MESSAGES_FIELD", "messages")
    out_dir: str = os.environ.get("OUT_DIR", "outputs/local-lora")
    max_seq_length: int = int(os.environ.get("MAX_SEQ_LENGTH", "512"))
    max_steps: int = int(os.environ.get("MAX_STEPS", "-1"))

cfg = Cfg()
device = "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(cfg.model_id, use_fast=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(cfg.model_id, torch_dtype=torch.float32)
model.to(device)
model.config.use_cache = False

if cfg.data_files:
    ds = load_dataset("json", data_files=cfg.data_files, split="train")
else:
    ds = load_dataset(cfg.dataset_id, split=cfg.dataset_split)

def format_example(ex):
    if cfg.text_field and isinstance(ex.get(cfg.text_field), str):
        ex["text"] = ex[cfg.text_field]
        return ex
    msgs = ex.get(cfg.messages_field)
    if isinstance(msgs, list):
        if hasattr(tokenizer, "apply_chat_template"):
            try:
                ex["text"] = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
                return ex
            except Exception:
                pass
        ex["text"] = "\n".join([str(m) for m in msgs])
        return ex
    ex["text"] = str(ex)
    return ex

ds = ds.map(format_example)
ds = ds.remove_columns([c for c in ds.column_names if c != "text"])

lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
                  task_type="CAUSAL_LM", target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])

sft_kwargs = dict(
    output_dir=cfg.out_dir, per_device_train_batch_size=1, gradient_accumulation_steps=8,
    learning_rate=2e-4, logging_steps=10, save_steps=200, save_total_limit=2,
    gradient_checkpointing=True, report_to="none", fp16=False, bf16=False,
    max_seq_length=cfg.max_seq_length, dataset_text_field="text",
)
if cfg.max_steps > 0:
    sft_kwargs["max_steps"] = cfg.max_steps
else:
    sft_kwargs["num_train_epochs"] = 1

trainer = SFTTrainer(model=model, train_dataset=ds, peft_config=lora,
                     args=SFTConfig(**sft_kwargs), processing_class=tokenizer)
trainer.train()
trainer.save_model(cfg.out_dir)
print(f"✅ 已保存至: {cfg.out_dir}")
```

</details>

### 运行

```bash
python train_lora_sft.py
```

**环境变量覆盖：**

```bash
MODEL_ID="Qwen/Qwen2.5-1.5B-Instruct" python train_lora_sft.py   # 不同模型
MAX_STEPS=50 python train_lora_sft.py                              # 快速 50 步测试
DATA_FILES="my_data.jsonl" python train_lora_sft.py                # 本地 JSONL 文件
PYTORCH_ENABLE_MPS_FALLBACK=1 python train_lora_sft.py             # MPS 操作回退到 CPU
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 python train_lora_sft.py      # 禁用 MPS 内存限制（谨慎使用）
```

**本地 JSONL 格式** — 聊天消息或纯文本：
```jsonl
{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]}
```
```jsonl
{"text": "User: Hello\nAssistant: Hi!"}
```
纯文本格式：`DATA_FILES="file.jsonl" TEXT_FIELD="text" MESSAGES_FIELD="" python train_lora_sft.py`

### 验证成功

- 损失在步进中下降
- `outputs/local-lora/` 包含 `adapter_config.json` + `*.safetensors`

## 快速评估

<details>
<summary><strong>eval_generate.py</strong></summary>

```python
import os, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")
ADAPTER = os.environ.get("ADAPTER_DIR", "outputs/local-lora")
device = "mps" if torch.backends.mps.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(BASE, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32)
model.to(device)
model = PeftModel.from_pretrained(model, ADAPTER)

prompt = os.environ.get("PROMPT", "用 3 个要点解释梯度累积。")
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=120, do_sample=True, temperature=0.7, top_p=0.9)
print(tokenizer.decode(out[0], skip_special_tokens=True))
```

</details>

## 故障排除（macOS 特定）

有关一般训练问题，请参阅 [troubleshooting.md](troubleshooting.md)。

| 问题 | 修复 |
|---------|-----|
| MPS 不支持的操作 / 崩溃 | `PYTORCH_ENABLE_MPS_FALLBACK=1` |
| OOM / 系统不稳定 | 减少 `MAX_SEQ_LENGTH`，使用更小模型，设置 `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`（谨慎）|
| fp16 NaN / 损失爆炸 | 保持 `fp16=False`（默认），降低学习率 |
| LoRA "module not found" | 打印 `model.named_modules()` 查找正确的目标名称 |
| TRL args TypeError | 检查 TRL 版本；脚本使用 `SFTConfig` + `processing_class`（TRL ≥0.12）|
| Intel Mac | 无 MPS — 改用 HF Jobs |

**按架构划分的常见 LoRA 目标模块：**

| 架构 | target_modules |
|-------------|---------------|
| Llama/Qwen/Mistral | `q_proj`, `k_proj`, `v_proj`, `o_proj` |
| GPT-2/GPT-J | `c_attn`, `c_proj` |
| BLOOM | `query_key_value`, `dense` |

## MLX 替代方案

[MLX](https://github.com/ml-explore/mlx) 提供更紧密的 Apple Silicon 集成，但生态较小，训练 API 不太成熟。对于本技能的工作流（本地验证 → HF Jobs），推荐使用 PyTorch + MPS 以保证一致性。MLX 微调请参阅 [mlx-lm](https://github.com/ml-explore/mlx-lm)。

## 另见

- [troubleshooting.md](troubleshooting.md) — 通用 TRL 故障排除
- [hardware_guide.md](hardware_guide.md) — HF Jobs 的 GPU 选择
- [gguf_conversion.md](gguf_conversion.md) — 导出用于设备端推理
- [training_methods.md](training_methods.md) — SFT、DPO、GRPO 概述
