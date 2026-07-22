# Unsloth：快速微调与内存优化

**Unsloth** 是一个微调库，为 LLM 训练提供约 2 倍的训练速度和约 60% 的显存节省。它在 GPU 内存有限或速度至关重要时特别有用。

- **GitHub**：[unslothai/unsloth](https://github.com/unslothai/unsloth)
- **文档**：[unsloth.ai/docs](https://unsloth.ai/docs)

## 何时使用 Unsloth

如果被指示使用 Unsloth，或以下用例之一适用，请使用 Unsloth：

| 用例 | 推荐 |
|----------|----------------|
| 标准文本 LLM 微调 | TRL 足够，但 Unsloth 更快 |
| GPU 内存有限 | **使用 Unsloth** - 减少 60% 显存 |
| 需要最大速度 | **使用 Unsloth** - 快 2 倍 |
| 大模型（>13B）| **使用 Unsloth** - 内存效率至关重要 |

## 支持的模型

Unsloth 支持许多流行模型，包括：
- **文本 LLM**：Llama 3/3.1/3.2/3.3、Qwen 2.5/3、Mistral、Phi-4、Gemma 2/3、LFM2/2.5
- **视觉 LLM**：Qwen3-VL、Gemma 3、Llama 3.2 Vision、Pixtral

可用时使用 Unsloth 预优化模型变体：
```python
# Unsloth 优化模型加载更快且使用更少内存
model_id = "unsloth/LFM2.5-1.2B-Instruct"      # 4-bit 量化
model_id = "unsloth/gemma-3-4b-pt"            # 视觉模型
model_id = "unsloth/Qwen3-VL-8B-Instruct"     # 视觉模型
```

## 安装

```python
# /// script
# dependencies = [
#     "unsloth",
#     "trl",
#     "datasets",
#     "trackio",
# ]
# ///
```

## 基本用法：文本 LLM

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 使用 Unsloth 优化加载模型
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="LiquidAI/LFM2.5-1.2B-Instruct",
    max_seq_length=4096,
)

# 添加 LoRA 适配器
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "out_proj", "in_proj", "w1", "w2", "w3"],
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

# 加载数据集
dataset = load_dataset("trl-lib/Capybara", split="train")

# 使用 TRL 训练
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="./output",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        max_steps=500,
        learning_rate=2e-4,
        report_to="trackio",
    ),
)

trainer.train()
```

## LFM2.5 特定设置

对于 LFM2.5 推理，使用这些推荐的生成参数：

**Instruct 模型：**
```python
temperature = 0.1
top_k = 50
top_p = 0.1
repetition_penalty = 1.05
```

**Thinking 模型：**
```python
temperature = 0.05
top_k = 50
repetition_penalty = 1.05
```

## 视觉语言模型（VLM）

Unsloth 通过 `FastVisionModel` 为 VLM 提供专门支持：

```python
from unsloth import FastVisionModel, get_chat_template
from unsloth.trainer import UnslothVisionDataCollator
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 使用 Unsloth 加载 VLM
model, processor = FastVisionModel.from_pretrained(
    "unsloth/gemma-3-4b-pt",  # 或 "unsloth/Qwen3-VL-8B-Instruct"
    load_in_4bit=True,
    use_gradient_checkpointing="unsloth",
)

# 为所有模态添加 LoRA
model = FastVisionModel.get_peft_model(
    model,
    finetune_vision_layers=True,      # 训练视觉编码器
    finetune_language_layers=True,    # 训练语言模型
    finetune_attention_modules=True,  # 训练注意力
    finetune_mlp_modules=True,        # 训练 MLP
    r=16,
    lora_alpha=32,
    target_modules="all-linear",
)

# 应用聊天模板（基础模型必需）
processor = get_chat_template(processor, "gemma-3")

# 加载 VLM 数据集（带图像和消息）
dataset = load_dataset("your-vlm-dataset", split="train", streaming=True)

# 启用训练模式
FastVisionModel.for_training(model)

# 使用 VLM 特定的 collator 训练
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    processing_class=processor.tokenizer,
    data_collator=UnslothVisionDataCollator(model, processor),
    args=SFTConfig(
        output_dir="./vlm-output",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        max_steps=500,
        learning_rate=2e-4,
        # VLM 特定设置
        remove_unused_columns=False,
        dataset_text_field="",
        dataset_kwargs={"skip_prepare_dataset": True},
        report_to="trackio",
    ),
)

trainer.train()
```

## 与标准 TRL 的关键差异

| 方面 | 标准 TRL | Unsloth |
|--------|--------------|---------|
| 模型加载 | `AutoModelForCausalLM.from_pretrained()` | `FastLanguageModel.from_pretrained()` |
| LoRA 设置 | `PeftModel` / `LoraConfig` | `FastLanguageModel.get_peft_model()` |
| VLM 加载 | 支持有限 | `FastVisionModel.from_pretrained()` |
| VLM collator | 手动 | `UnslothVisionDataCollator` |
| 内存使用 | 标准 | 减少约 60% |
| 训练速度 | 标准 | 约 2 倍 |

## VLM 数据集格式

VLM 数据集应包含：
- `images`：PIL 图像或图像路径列表
- `messages`：带图像引用的对话格式

```python
{
    "images": [<PIL.Image>, ...],
    "messages": [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": "描述这张图像"}
        ]},
        {"role": "assistant", "content": "这张图像显示..."}
    ]
}
```

## 流式数据集

对于大型 VLM 数据集，使用流式以避免磁盘空间问题：

```python
dataset = load_dataset(
    "your-vlm-dataset",
    split="train",
    streaming=True,  # 从 Hub 流式获取
)

# 流式时必须使用 max_steps（不能基于 epoch 训练）
SFTConfig(max_steps=500, ...)
```

## 保存模型

### 保存 LoRA 适配器

```python
model.save_pretrained("./adapter")
processor.save_pretrained("./adapter")

# 推送到 Hub
model.push_to_hub("username/my-vlm-adapter")
processor.push_to_hub("username/my-vlm-adapter")
```

### 合并并保存完整模型

```python
# 将 LoRA 权重合并到基础模型
model = model.merge_and_unload()

# 保存合并后的模型
model.save_pretrained("./merged")
tokenizer.save_pretrained("./merged")
```

### 转换为 GGUF

Unsloth 模型可以转换为 GGUF 用于 llama.cpp/Ollama：

```python
# 保存为 16-bit 用于 GGUF 转换
model.save_pretrained_gguf("./gguf", tokenizer, quantization_method="f16")

# 或直接量化
model.save_pretrained_gguf("./gguf", tokenizer, quantization_method="q4_k_m")
```

## Qwen3-VL 特定设置

对于 Qwen3-VL 模型，使用这些推荐的设置：

**Instruct 模型：**
```python
temperature = 0.7
top_p = 0.8
presence_penalty = 1.5
```

**Thinking 模型：**
```python
temperature = 1.0
top_p = 0.95
presence_penalty = 0.0
```

## 硬件要求

| 模型 | 最小显存（Unsloth 4-bit）| 推荐 GPU |
|-------|--------------------------|-----------------|
| 2B-4B | 8GB | T4, L4 |
| 7B-8B | 16GB | A10G, L4x4 |
| 13B | 24GB | A10G-large |
| 30B+ | 48GB+ | A100 |

## 示例：完整 VLM 训练脚本

完整的生产就绪示例见 `scripts/unsloth_sft_example.py`，包括：
- Unsloth VLM 设置
- 流式数据集支持
- Trackio 监控
- Hub 推送
- CLI 参数

本地运行：
```bash
uv run scripts/unsloth_sft_example.py \
    --dataset trl-lib/Capybara \
    --max-steps 500 \
    --output-repo username/my-model
```

在 HF Jobs 上运行：
```python
hf_jobs("uv", {
    "script": "<script content>",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

## 另见

- `scripts/unsloth_sft_example.py` - 完整文本 LLM 训练示例
- [Unsloth 文档](https://unsloth.ai/docs)
- [LFM2.5 指南](https://unsloth.ai/docs/models/tutorials/lfm2.5)
- [Qwen3-VL 指南](https://unsloth.ai/docs/models/qwen3-vl-how-to-run-and-fine-tune)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
