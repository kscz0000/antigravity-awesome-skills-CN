---
name: trl-training
description: 使用 TRL（Transformers Reinforcement Learning）训练和微调 Transformer 语言模型。支持通过 CLI 命令进行 SFT、DPO、GRPO、KTO、RLOO 和奖励模型训练（trl、SFT、DPO、PPO、RLHF、奖励模型、训练）。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/trl-training
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# TRL 训练技能
## 使用时机

当你需要使用 TRL（Transformers Reinforcement Learning）训练和微调 Transformer 语言模型时，请使用此技能。支持通过 CLI 命令进行 SFT、DPO、GRPO、KTO、RLOO 和奖励模型训练。


你是使用 TRL（Transformers Reinforcement Learning）库训练和微调大语言模型的专家。

## 概述

TRL 提供 CLI 命令，用于使用最先进技术对基础模型进行后训练：

- **SFT**（Supervised Fine-Tuning，监督微调）：在指令跟随或对话数据集上微调模型
- **DPO**（Direct Preference Optimization，直接偏好优化）：使用偏好数据对齐模型
- **GRPO**（Group Relative Policy Optimization，分组相对策略优化）：通过对多个采样输出进行相互排序并基于其比较奖励进行优化来训练模型
- **RLOO**（Reinforce Leave One Out，留一法强化）：基于生成奖励的在线 RL 训练
- **奖励模型训练**：训练用于 RLHF 的奖励模型

TRL 基于 Hugging Face Transformers 和 Accelerate 构建，可与 Hugging Face 生态系统无缝集成。

## 核心命令

### trl sft — 监督微调

在指令跟随或对话数据集上微调语言模型。

**全量训练：**

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2-0.5B \
  --dataset_name trl-lib/Capybara \
  --learning_rate 2.0e-5 \
  --num_train_epochs 1 \
  --packing \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --eos_token '<|im_end|>' \
  --eval_strategy steps \
  --eval_steps 100 \
  --output_dir Qwen2-0.5B-SFT \
  --push_to_hub
```

**使用 LoRA 适配器训练：**

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2-0.5B \
  --dataset_name trl-lib/Capybara \
  --learning_rate 2.0e-4 \
  --num_train_epochs 1 \
  --packing \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --eos_token '<|im_end|>' \
  --eval_strategy steps \
  --eval_steps 100 \
  --use_peft \
  --lora_r 32 \
  --lora_alpha 16 \
  --output_dir Qwen2-0.5B-SFT \
  --push_to_hub
```

### trl dpo — 直接偏好优化

使用偏好数据（chosen/rejected 对）对齐模型。

**全量训练：**

```bash
trl dpo \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --learning_rate 5.0e-7 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --max_steps 1000 \
  --gradient_accumulation_steps 8 \
  --eval_strategy steps \
  --eval_steps 50 \
  --output_dir Qwen2-0.5B-DPO \
  --no_remove_unused_columns
```

**使用 LoRA 适配器训练：**

```bash
trl dpo \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --learning_rate 5.0e-6 \
  --num_train_epochs 1 \
  --per_device_train_batch_size 2 \
  --max_steps 1000 \
  --gradient_accumulation_steps 8 \
  --eval_strategy steps \
  --eval_steps 50 \
  --output_dir Qwen2-0.5B-DPO \
  --no_remove_unused_columns \
  --use_peft \
  --lora_r 32 \
  --lora_alpha 16
```

### trl grpo — 分组相对策略优化

使用奖励函数或 LLM-as-a-judge 评估生成并提供奖励来训练模型。

**基础用法：**

```bash
trl grpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/gsm8k \
  --reward_funcs accuracy_reward \
  --output_dir Qwen2-0.5B-GRPO \
  --push_to_hub
```

### trl rloo — 留一法强化

模型生成文本并根据自定义条件获得奖励的在线 RL 训练。

**基础用法：**

```bash
trl rloo \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/tldr \
  --reward_model_name_or_path sentiment-analysis:nlptown/bert-base-multilingual-uncased-sentiment \
  --output_dir Qwen2-0.5B-RLOO \
  --push_to_hub
```

### trl reward — 奖励模型训练

训练奖励模型，为 RLHF 评估文本质量。

**全量训练：**

```bash
trl reward \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir Qwen2-0.5B-Reward \
  --per_device_train_batch_size 8 \
  --num_train_epochs 1 \
  --learning_rate 1.0e-5 \
  --eval_strategy steps \
  --eval_steps 50 \
  --max_length 2048
```

**使用 LoRA 适配器训练：**

```bash
trl reward \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir Qwen2-0.5B-Reward-LoRA \
  --per_device_train_batch_size 8 \
  --num_train_epochs 1 \
  --learning_rate 1.0e-4 \
  --eval_strategy steps \
  --eval_steps 50 \
  --max_length 2048 \
  --use_peft \
  --lora_task_type SEQ_CLS \
  --lora_r 32 \
  --lora_alpha 16
```

## 配置文件

TRL 支持 YAML 配置文件以实现可复现的训练。所有 CLI 参数都可以在配置文件中指定。

**配置示例（sft_config.yaml）：**

```yaml
model_name_or_path: Qwen/Qwen2.5-0.5B
dataset_name: trl-lib/Capybara
learning_rate: 2.0e-5
num_train_epochs: 1
per_device_train_batch_size: 8
gradient_accumulation_steps: 2
output_dir: ./sft_output
use_peft: true
lora_r: 16
lora_alpha: 16
report_to: trackio
```

**使用配置启动：**

```bash
trl sft --config sft_config.yaml
```

**覆盖配置值：**

```bash
trl sft --config sft_config.yaml --learning_rate 1.0e-5
```

## 分布式训练

TRL 与 Accelerate 集成，支持多 GPU 和多节点训练。

**多 GPU 训练：**

```bash
trl sft \
  --config sft_config.yaml \
  --num_processes 4
```

**使用预定义 Accelerate 配置：**

TRL 提供预定义配置：`single_gpu`、`multi_gpu`、`fsdp1`、`fsdp2`、`zero1`、`zero2`、`zero3`

```bash
trl sft \
  --config sft_config.yaml \
  --accelerate_config zero2
```

**自定义 Accelerate 配置：**

```bash
# Generate custom config
accelerate config

# Use custom config
trl sft --config sft_config.yaml --config_file ~/.cache/huggingface/accelerate/default_config.yaml
```

**全分片数据并行（FSDP）：**

```bash
trl sft --config sft_config.yaml --accelerate_config fsdp2
```

**DeepSpeed ZeRO：**

```bash
trl sft --config sft_config.yaml --accelerate_config zero3
```

## 故障排查

### CUDA 显存不足

- 减小 `--per_device_train_batch_size` 并增加 `--gradient_accumulation_steps`
- 启用 `--use_peft` 进行 LoRA 训练
- 使用 `--gradient_checkpointing` 以节省显存
- 尝试更小的模型或更长的序列截断

### 数据集加载问题

- 验证数据集是否存在：检查 Hugging Face Hub 或本地路径
- 检查数据集格式是否与预期列匹配
- 多配置数据集使用 `--dataset_config`
- 检查数据集：`from datasets import load_dataset; ds = load_dataset(name)`

### 模型加载问题

- 验证模型是否存在于 Hugging Face Hub
- 检查受限模型是否需要身份验证：`hf auth login`
- 对于本地模型，请提供绝对路径
- 确保有足够的磁盘空间和内存

### 训练缓慢

- 对短序列启用数据集 `--packing`
- 如果显存允许，使用更大的 `--per_device_train_batch_size`
- 在 Ampere GPU 上启用 `--tf32` 以加快计算
- 在支持的硬件上使用 `--bf16`
- 考虑使用 `--num_processes` 进行多 GPU 训练

### 生成问题（GRPO/RLOO）

- 检查数据集中的 prompt 格式
- 调整 `--temperature` 和 `--top_p` 进行生成
- 验证奖励函数（针对 GRPO/RLOO）

## 其他资源

- **文档**：https://huggingface.co/docs/trl
- **GitHub**：https://github.com/huggingface/trl
- **示例**：https://github.com/huggingface/trl/tree/main/examples

## 最佳实践

1. **从 SFT 开始**：在进行偏好对齐之前，始终先使用 SFT 微调基础模型
2. **使用 LoRA 提高效率**：启用 `--use_peft` 以加快训练并降低显存占用
3. **监控训练**：使用 `--report_to trackio`（或 `--report_to wandb` 或 `--report_to tensorboard`）进行追踪
4. **保存检查点**：TRL 会自动将检查点保存到 `--output_dir`
5. **先在小数据集上测试**：在全量训练前验证流水线可行
6. **使用配置文件**：创建 YAML 配置以实现可复现性
7. **利用 Accelerate**：使用多 GPU 训练以加快迭代速度

在帮助用户使用 TRL 时：
- 始终检查哪种训练方法适合其用例
- 验证数据集格式是否与预期 schema 匹配
- 建议先使用较小的模型进行测试
- 在资源受限环境中推荐 LoRA
- 指向具体的文档章节以了解高级功能

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时，才使用此技能。
- 在进行更改之前，请根据当前官方文档验证命令、API 行为、配额、凭证和部署效果。
- 不要将生成的示例视为针对特定环境的测试、安全审查或用户对破坏性或高成本操作的批准的替代品。
