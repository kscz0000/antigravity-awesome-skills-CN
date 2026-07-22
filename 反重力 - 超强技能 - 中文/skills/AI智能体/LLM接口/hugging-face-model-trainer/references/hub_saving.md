# 将训练结果保存到 Hugging Face Hub

**⚠️ 关键：** 训练环境是临时的。除非推送到 Hub，否则任务完成时所有结果都会丢失。

## 为什么必须推送到 Hub

在 Hugging Face Jobs 上运行时：
- 环境是临时的
- 任务完成时所有文件被删除
- 没有本地磁盘持久化
- 任务结束后无法访问结果

**不推送到 Hub，训练将完全浪费。**

## 必需配置

### 1. 训练配置

在 SFTConfig 或 trainer 配置中：

```python
SFTConfig(
    push_to_hub=True,                    # 启用 Hub 推送
    hub_model_id="username/model-name",   # 目标仓库
)
```

### 2. 任务配置

提交任务时：

```python
hf_jobs("uv", {
    "script": "train.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 提供认证
})
```

**`$HF_TOKEN` 占位符会自动替换为你的 Hugging Face token。**

## 完整示例

```python
# train.py
# /// script
# dependencies = ["trl"]
# ///

from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

dataset = load_dataset("trl-lib/Capybara", split="train")

# 配置 Hub 推送
config = SFTConfig(
    output_dir="my-model",
    num_train_epochs=3,

    # ✅ 关键：Hub 推送配置
    push_to_hub=True,
    hub_model_id="myusername/my-trained-model",

    # 可选：推送策略
    push_to_hub_model_id="myusername/my-trained-model",
    push_to_hub_organization=None,
    push_to_hub_token=None,  # 使用环境 token
)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    args=config,
)

trainer.train()

# ✅ 推送最终模型
trainer.push_to_hub()

print("✅ 模型已保存至: https://huggingface.co/myusername/my-trained-model")
```

**提交时使用认证：**

```python
hf_jobs("uv", {
    "script": "train.py",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 必需！
})
```

## 保存哪些内容

当 `push_to_hub=True` 时：

1. **模型权重** - 最终训练参数
2. **分词器** - 关联的分词器
3. **配置** - 模型配置（config.json）
4. **训练参数** - 使用的超参数
5. **模型卡片** - 自动生成的文档
6. **检查点** - 如果启用了 `save_strategy="steps"`

## 检查点保存

在训练期间保存中间检查点：

```python
SFTConfig(
    output_dir="my-model",
    push_to_hub=True,
    hub_model_id="username/my-model",

    # 检查点配置
    save_strategy="steps",
    save_steps=100,              # 每 100 步保存一次
    save_total_limit=3,          # 仅保留最后 3 个检查点
)
```

**好处：**
- 任务失败时恢复训练
- 比较检查点性能
- 使用中间模型

**检查点推送至：** `username/my-model`（同一仓库）

## 认证方法

### 方法 1：自动 Token（推荐）

```python
"secrets": {"HF_TOKEN": "$HF_TOKEN"}
```

自动使用你登录的 Hugging Face token。

### 方法 2：显式 Token

```python
"secrets": {"HF_TOKEN": "hf_abc123..."}
```

显式提供 token（出于安全考虑不推荐）。

### 方法 3：环境变量

```python
"env": {"HF_TOKEN": "hf_abc123..."}
```

作为常规环境变量传递（比 secrets 不安全）。

**始终优先使用方法 1** 以确保安全性和便利性。

## 验证检查清单

提交任何训练任务前，验证：

- [ ] 训练配置中设置 `push_to_hub=True`
- [ ] 指定 `hub_model_id`（格式：`username/model-name`）
- [ ] 任务配置中设置 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- [ ] 仓库名称不与现有仓库冲突
- [ ] 你对目标命名空间有写入权限

## 仓库设置

### 自动创建

如果仓库不存在，将在首次推送时自动创建。

### 手动创建

训练前创建仓库：

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(
    repo_id="username/model-name",
    repo_type="model",
    private=False,  # 或 True 表示私有仓库
)
```

### 仓库命名

**有效名称：**
- `username/my-model`
- `username/model-name`
- `organization/model-name`

**无效名称：**
- `model-name`（缺少用户名）
- `username/model name`（不允许空格）
- `username/MODEL`（不推荐大写）

## 故障排除

### 错误：401 Unauthorized

**原因：**未提供 HF_TOKEN 或 token 无效

**解决方案：**
1. 验证任务配置中设置 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 检查是否已登录：`hf auth whoami`
3. 重新登录：`hf auth login`

### 错误：403 Forbidden

**原因：**对仓库没有写入权限

**解决方案：**
1. 检查仓库命名空间是否与你的用户名匹配
2. 验证你是组织成员（如果使用组织命名空间）
3. 检查仓库是否私有（如果访问组织仓库）

### 错误：找不到仓库

**原因：**仓库不存在且自动创建失败

**解决方案：**
1. 先手动创建仓库
2. 检查仓库名称格式
3. 验证命名空间存在

### 错误：训练期间推送失败

**原因：**网络问题或 Hub 不可用

**解决方案：**
1. 训练继续但最终推送失败
2. 检查点可能已保存
3. 任务完成后手动重新推送

### 问题：模型已保存但不可见

**可能原因：**
1. 仓库是私有——查看 https://huggingface.co/username
2. 命名空间错误——验证 `hub_model_id` 与登录匹配
3. 推送仍在进行——等待几分钟

## 训练后手动推送

如果训练完成但推送失败，手动推送：

```python
from transformers import AutoModel, AutoTokenizer

# 从本地检查点加载
model = AutoModel.from_pretrained("./output_dir")
tokenizer = AutoTokenizer.from_pretrained("./output_dir")

# 推送到 Hub
model.push_to_hub("username/model-name", token="hf_abc123...")
tokenizer.push_to_hub("username/model-name", token="hf_abc123...")
```

**注意：**仅在任务尚未完成（文件仍存在）时可行。

## 最佳实践

1. **始终启用 `push_to_hub=True`**
2. **对长时间训练使用检查点保存**
3. **在任务完成前在日志中验证 Hub 推送**
4. **设置合适的 `save_total_limit`** 避免过多检查点
5. **使用描述性仓库名称**（如 `qwen-capybara-sft` 而非 `model1`）
6. **添加模型卡片** 包含训练详情
7. **为模型添加相关标签**（如 `text-generation`、`fine-tuned`）

## 监控推送进度

查看日志中的推送进度：

```python
hf_jobs("logs", {"job_id": "your-job-id"})
```

**寻找：**
```
Pushing model to username/model-name...
Upload file pytorch_model.bin: 100%
✅ Model pushed successfully
```

## 示例：完整生产设置

```python
# production_train.py
# /// script
# dependencies = ["trl>=0.12.0", "peft>=0.7.0"]
# ///

from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
import os

# 验证 token 可用
assert "HF_TOKEN" in os.environ, "环境中找不到 HF_TOKEN！"

# 加载数据集
dataset = load_dataset("trl-lib/Capybara", split="train")
print(f"✅ 数据集已加载: {len(dataset)} 条样本")

# 配置全面的 Hub 设置
config = SFTConfig(
    output_dir="qwen-capybara-sft",

    # Hub 配置
    push_to_hub=True,
    hub_model_id="myusername/qwen-capybara-sft",
    hub_strategy="checkpoint",  # 推送检查点

    # 检查点配置
    save_strategy="steps",
    save_steps=100,
    save_total_limit=3,

    # 训练设置
    num_train_epochs=3,
    per_device_train_batch_size=4,

    # 日志
    logging_steps=10,
    logging_first_step=True,
)

# 使用 LoRA 训练
trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,
    args=config,
    peft_config=LoraConfig(r=16, lora_alpha=32),
)

print("🚀 开始训练...")
trainer.train()

print("💾 推送最终模型到 Hub...")
trainer.push_to_hub()

print("✅ 训练完成！")
print(f"模型可用地址: https://huggingface.co/myusername/qwen-capybara-sft")
```

**提交：**

```python
hf_jobs("uv", {
    "script": "production_train.py",
    "flavor": "a10g-large",
    "timeout": "6h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

## 关键要点

**没有 `push_to_hub=True` 和 `secrets={"HF_TOKEN": "$HF_TOKEN"}`，所有训练结果将永久丢失。**

提交任何训练任务前，始终验证这两项已配置。
