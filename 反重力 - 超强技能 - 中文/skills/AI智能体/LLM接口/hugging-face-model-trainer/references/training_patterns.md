# 常见训练模式

本指南提供了 Hugging Face Jobs 上 TRL 的常见训练模式和用例。

## 多 GPU 训练

跨多个 GPU 的自动分布式训练。TRL/Accelerate 自动处理分布式：

```python
hf_jobs("uv", {
    "script": """
# 你的训练脚本（与单 GPU 相同）
# 无需修改 - Accelerate 自动检测多个 GPU
""",
    "flavor": "a10g-largex2",  # 2x A10G GPU
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**多 GPU 技巧：**
- 无需修改代码
- 使用 `per_device_train_batch_size`（每个 GPU，非总计）
- 有效批次大小 = `per_device_train_batch_size` × `num_gpus` × `gradient_accumulation_steps`
- 监控 GPU 利用率以确保两个 GPU 都在使用

## DPO 训练（偏好学习）

使用偏好数据进行对齐训练：

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["trl>=0.12.0", "trackio"]
# ///

from datasets import load_dataset
from trl import DPOTrainer, DPOConfig
import trackio

dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")

# 创建 train/eval 分割
dataset_split = dataset.train_test_split(test_size=0.1, seed=42)

config = DPOConfig(
    output_dir="dpo-model",
    push_to_hub=True,
    hub_model_id="username/dpo-model",
    num_train_epochs=1,
    beta=0.1,  # KL 惩罚系数
    eval_strategy="steps",
    eval_steps=50,
    report_to="trackio",
    run_name="baseline_run", # 使用有意义的运行名称
    # max_length=1024,  # 默认值 - 仅在需要不同序列长度时设置
)

trainer = DPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",  # 使用 instruct 模型作为基础
    train_dataset=dataset_split["train"],
    eval_dataset=dataset_split["test"],  # 重要：启用 eval_strategy 时提供 eval_dataset
    args=config,
)

trainer.train()
trainer.push_to_hub()
trackio.finish()
""",
    "flavor": "a10g-large",
    "timeout": "3h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**DPO 文档：** 使用 `hf_doc_fetch("https://huggingface.co/docs/trl/dpo_trainer")`

## GRPO 训练（在线 RL）

用于在线强化学习的组相对策略优化：

```python
hf_jobs("uv", {
    "script": "https://raw.githubusercontent.com/huggingface/trl/main/examples/scripts/grpo.py",
    "script_args": [
        "--model_name_or_path", "Qwen/Qwen2.5-0.5B-Instruct",
        "--dataset_name", "trl-lib/math_shepherd",
        "--output_dir", "grpo-model",
        "--push_to_hub",
        "--hub_model_id", "username/grpo-model"
    ],
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**GRPO 文档：** 使用 `hf_doc_fetch("https://huggingface.co/docs/trl/grpo_trainer")`

## Trackio 配置

**使用合理的 trackio 设置默认值。**完整文档见 `references/trackio_guide.md`，包括为实验分组运行。

### 基本模式

```python
import trackio

trackio.init(
    project="my-training",
    run_name="baseline-run",             # 用户可识别的描述性名称
    space_id="username/trackio",     # 默认 space: {username}/trackio
    config={
        # 保持 config 最小 - 仅包含超参数和模型/数据集信息
        "model": "Qwen/Qwen2.5-0.5B",
        "dataset": "trl-lib/Capybara",
        "learning_rate": 2e-5,
    }
)

# 你的训练代码...

trackio.finish()
```

### 为实验分组（可选）

当用户想要比较相关运行时，使用 `group` 参数：

```python
# 超参数扫描
trackio.init(project="hyperparam-sweep", run_name="lr-0.001", group="lr_0.001")
trackio.init(project="hyperparam-sweep", run_name="lr-0.01", group="lr_0.01")
```

## 模式选择指南

| 用例 | 模式 | 硬件 | 时间 |
|----------|---------|----------|------|
| SFT 训练 | `scripts/train_sft_example.py` | a10g-large | 2-6 小时 |
| 大数据集（>10K）| 多 GPU | a10g-largex2 | 4-12 小时 |
| 偏好学习 | DPO 训练 | a10g-large | 2-4 小时 |
| 在线 RL | GRPO 训练 | a10g-large | 3-6 小时 |

## 关键：评估数据集要求

**⚠️ 重要**：如果设置 `eval_strategy="steps"` 或 `eval_strategy="epoch"`，你**必须**向 trainer 提供 `eval_dataset`，否则训练将挂起。

### ✅ 正确 - 带 eval 数据集：
```python
dataset_split = dataset.train_test_split(test_size=0.1, seed=42)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset_split["train"],
    eval_dataset=dataset_split["test"],  # ← 启用 eval_strategy 时必须提供
    args=SFTConfig(eval_strategy="steps", ...),
)
```

### ❌ 错误 - 将挂起：
```python
trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    # 没有 eval_dataset 但 eval_strategy="steps" ← 将挂起
    args=SFTConfig(eval_strategy="steps", ...),
)
```

### 选项：没有 eval 数据集时禁用评估
```python
config = SFTConfig(
    eval_strategy="no",  # ← 显式禁用评估
    # ... 其他配置
)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    # 不需要 eval_dataset
    args=config,
)
```

## 最佳实践

1. **使用 train/eval 分割** - 创建评估分割以监控进度
2. **启用 Trackio** - 实时监控进度
3. **为超时增加 20-30% 缓冲** - 考虑加载/保存开销
4. **先用 TRL 官方脚本测试** - 自定义代码前使用维护的示例
5. **始终提供 eval_dataset** - 使用 eval_strategy 时，或设置为 "no"
6. **对大模型使用多 GPU** - 7B+ 模型显著受益

## 另见

- `scripts/train_sft_example.py` - 带 Trackio 和 eval 分割的完整 SFT 模板
- `scripts/train_dpo_example.py` - 完整 DPO 模板
- `scripts/train_grpo_example.py` - 完整 GRPO 模板
- `references/hardware_guide.md` - 详细硬件规格
- `references/training_methods.md` - 所有 TRL 训练方法概述
- `references/troubleshooting.md` - 常见问题和解决方案
