# TRL 训练方法概述

TRL（Transformer Reinforcement Learning，Transformer 强化学习）提供多种训练方法用于微调和对齐语言模型。本参考提供了每种方法的简要概述。

## 监督微调（SFT）

**它是什么：** 在演示数据上使用监督学习的标准指令调优。

**何时使用：**
- 在特定任务数据上对基础模型进行初始微调
- 教授新能力或领域
- 微调最常见的起点

**数据集格式：** 带 "messages" 字段的对话格式，或 text 字段，或 prompt/completion 对

**示例：**
```python
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="my-model",
        push_to_hub=True,
        hub_model_id="username/my-model",
        eval_strategy="no",  # 简单示例禁用 eval
        # max_length=1024 是默认值 - 仅在需要不同长度时设置
    )
)
trainer.train()
```

**注意：**有关带评估监控的生产训练，参阅 `scripts/train_sft_example.py`

**文档：** `hf_doc_fetch("https://huggingface.co/docs/trl/sft_trainer")`

## 直接偏好优化（DPO）

**它是什么：** 直接在偏好对上训练的对齐方法（chosen vs rejected 响应），无需奖励模型。

**何时使用：**
- 将模型与人类偏好对齐
- SFT 后提升响应质量
- 拥有配对的偏好数据（chosen/rejected 响应）

**数据集格式：** 带 "chosen" 和 "rejected" 字段的偏好对

**示例：**
```python
from trl import DPOTrainer, DPOConfig

trainer = DPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",  # 使用 instruct 模型
    train_dataset=dataset,
    args=DPOConfig(
        output_dir="dpo-model",
        beta=0.1,  # KL 惩罚系数
        eval_strategy="no",  # 简单示例禁用 eval
        # max_length=1024 是默认值 - 仅在需要不同长度时设置
    )
)
trainer.train()
```

**注意：**有关带评估监控的生产训练，参阅 `scripts/train_dpo_example.py`

**文档：** `hf_doc_fetch("https://huggingface.co/docs/trl/dpo_trainer")`

## 组相对策略优化（GRPO）

**它是什么：** 相对于组性能进行优化的在线 RL 方法，适用于具有可验证奖励的任务。

**何时使用：**
- 具有自动奖励信号的任务（代码执行、数学验证）
- 在线学习场景
- 当 DPO 离线数据不足时

**数据集格式：** 仅 prompt 格式（模型生成响应，奖励在线计算）

**示例：**
```python
# 使用 TRL 维护的脚本
hf_jobs("uv", {
    "script": "https://raw.githubusercontent.com/huggingface/trl/main/examples/scripts/grpo.py",
    "script_args": [
        "--model_name_or_path", "Qwen/Qwen2.5-0.5B-Instruct",
        "--dataset_name", "trl-lib/math_shepherd",
        "--output_dir", "grpo-model"
    ],
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**文档：** `hf_doc_fetch("https://huggingface.co/docs/trl/grpo_trainer")`

## 奖励建模

**它是什么：** 训练奖励模型对响应进行评分，用作 RLHF 流水线的组件。

**何时使用：**
- 构建 RLHF 流水线
- 需要自动质量评分
- 为 PPO 训练创建奖励信号

**数据集格式：** 带 "chosen" 和 "rejected" 响应的偏好对

**文档：** `hf_doc_fetch("https://huggingface.co/docs/trl/reward_trainer")`

## 方法选择指南

| 方法 | 复杂度 | 所需数据 | 用途 |
|--------|-----------|---------------|----------|
| **SFT** | 低 | 演示 | 初始微调 |
| **DPO** | 中 | 配对偏好 | SFT 后对齐 |
| **GRPO** | 中 | Prompt + 奖励函数 | 带自动奖励的在线 RL |
| **Reward** | 中 | 配对偏好 | 构建 RLHF 流水线 |

## 推荐流水线

**对于大多数用例：**
1. **从 SFT 开始** - 在任务数据上微调基础模型
2. **接着用 DPO** - 使用配对数据对齐到偏好
3. **可选：GGUF 转换** - 部署用于本地推理

**对于高级 RL 场景：**
1. **从 SFT 开始** - 微调基础模型
2. **训练奖励模型** - 在偏好数据上

## 数据集格式参考

完整的数据集格式规范，使用：
```python
hf_doc_fetch("https://huggingface.co/docs/trl/dataset_formats")
```

或验证你的数据集：
```bash
uv run https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py \
  --dataset your/dataset --split train
```

## 另见

- `references/training_patterns.md` - 常见训练模式和示例
- `scripts/train_sft_example.py` - 完整 SFT 模板
- `scripts/train_dpo_example.py` - 完整 DPO 模板
- [数据集检查器](https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py) - 数据集格式验证工具
