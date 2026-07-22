# 将视觉模型保存到 Hugging Face Hub

## 目录
- 为什么需要推送到 Hub
- 必需配置（TrainingArguments、任务配置）
- 完整示例
- 保存的内容
- 重要事项：保存图像处理器
- 检查点保存
- 模型卡片配置
- 保存标签映射
- 认证方法
- 验证清单
- 仓库设置（自动/手动创建、命名）
- 故障排除（401、403、推送失败、推理问题）
- 训练后手动推送
- 示例：完整生产配置
- 推理示例

---

**关键提示：** 训练环境是临时的。除非推送到 Hub，否则任务完成时所有结果都会丢失。

## 为什么需要推送到 Hub

在 Hugging Face Jobs 上运行时：
- 环境是临时的
- 任务完成时所有文件被删除
- 没有本地磁盘持久化
- 任务结束后无法访问结果

**不推送到 Hub，训练就完全白费。**

## 必需配置

### 1. 训练配置

在你的 TrainingArguments 中：

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="my-object-detector",
    push_to_hub=True,                    # Enable Hub push
    hub_model_id="username/model-name",   # Target repository
)
```

### 2. 任务配置

提交任务时：

```python
hf_jobs("uv", {
    "script": training_script_content,  # Pass the Python script content directly as a string
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # Provide authentication
})
```

**`$HF_TOKEN` 语法引用你实际的 Hugging Face token 值。**

## 完整示例

```python
# train_detector.py
# /// script
# dependencies = ["transformers", "torch", "torchvision", "datasets"]
# ///

from transformers import (
    AutoImageProcessor,
    AutoModelForObjectDetection,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset
import os
import torch

# Load dataset
dataset = load_dataset("cppe-5", split="train")

# Load model and processor
model_name = "facebook/detr-resnet-50"
image_processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForObjectDetection.from_pretrained(
    model_name,
    num_labels=5,  # Number of classes
    ignore_mismatched_sizes=True
)

# Configure with Hub push
training_args = TrainingArguments(
    output_dir="my-detector",
    num_train_epochs=10,
    per_device_train_batch_size=8,

    # ✅ CRITICAL: Hub push configuration
    push_to_hub=True,
    hub_model_id="myusername/cppe5-detector",

    # Optional: Push strategy
    hub_strategy="checkpoint",  # Push checkpoints during training
)

# ✅ CRITICAL: Authenticate with Hub BEFORE creating Trainer
from huggingface_hub import login
hf_token = os.environ.get("HF_TOKEN") or os.environ.get("hfjob")
if hf_token:
    login(token=hf_token)
    training_args.hub_token = hf_token
elif training_args.push_to_hub:
    raise ValueError("HF_TOKEN not found! Add secrets={'HF_TOKEN': '$HF_TOKEN'} to job config.")

# Define collate function
def collate_fn(batch):
    pixel_values = [item["pixel_values"] for item in batch]
    labels = [item["labels"] for item in batch]
    encoding = image_processor.pad(pixel_values, return_tensors="pt")
    return {
        "pixel_values": encoding["pixel_values"],
        "labels": labels
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=collate_fn,
)

trainer.train()

# ✅ Push final model and processor
trainer.push_to_hub()
image_processor.push_to_hub("myusername/cppe5-detector")

print("✅ Model saved to: https://huggingface.co/myusername/cppe5-detector")
```

**使用认证提交：**

```python
hf_jobs("uv", {
    "script": training_script_content,  # Pass script content as a string, NOT a filename
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ Required!
})
```

## 保存的内容

当 `push_to_hub=True` 时：

1. **模型权重** - 最终训练的参数
2. **图像处理器** - 关联的预处理配置
3. **配置** - 模型配置（config.json），包括：
   - 标签/类别数量
   - 架构细节（backbone、num_queries 等）
   - 标签映射（id2label、label2id）
4. **训练参数** - 使用的超参数
5. **模型卡片** - 自动生成的文档
6. **检查点** - 如果启用了 `save_strategy="steps"`

## 重要事项：保存图像处理器

**目标检测模型需要单独保存图像处理器：**

```python
# After training completes
trainer.push_to_hub()

# ✅ Also push the image processor
image_processor.push_to_hub(
    repo_id="username/model-name",
    commit_message="Upload image processor"
)
```

**为什么这很重要：**
- 模型需要特定的图像预处理（缩放、归一化）
- 图像处理器包含关键配置
- 没有它，模型无法用于推理

## 检查点保存

在训练期间保存中间检查点：

```python
TrainingArguments(
    output_dir="my-detector",
    push_to_hub=True,
    hub_model_id="username/my-detector",

    # Checkpoint configuration
    save_strategy="steps",
    save_steps=500,              # Save every 500 steps
    save_total_limit=3,          # Keep only last 3 checkpoints
    hub_strategy="checkpoint",   # Push checkpoints to Hub
)
```

**好处：**
- 任务失败时恢复训练
- 比较检查点性能
- 使用中间模型
- 跟踪训练进度

**检查点推送到：** `username/my-detector`（同一仓库）

## 模型卡片配置

添加元数据以提高可发现性：

```python
# At the end of training script
model.push_to_hub(
    "username/my-detector",
    commit_message="Upload trained object detection model",
    tags=["object-detection", "vision", "cppe-5"],
    model_card_kwargs={
        "license": "apache-2.0",
        "dataset": "cppe-5",
        "metrics": ["map", "recall", "precision"],
        "pipeline_tag": "object-detection",
    }
)
```

## 保存标签映射

**目标检测的关键：** 将类别标签与模型一起保存：

```python
# Define your label mappings
id2label = {0: "Coverall", 1: "Face_Shield", 2: "Gloves", 3: "Goggles", 4: "Mask"}
label2id = {v: k for k, v in id2label.items()}

# Update model config before training
model.config.id2label = id2label
model.config.label2id = label2id

# Now train and push
trainer.train()
trainer.push_to_hub()
```

**没有标签映射时：**
- 模型输出仅为数字 ID
- 没有可读的类别名称
- 难以解释结果

## 认证方法

有关 token 类型、`$HF_TOKEN` 自动替换、`secrets` 与 `env` 的区别以及安全最佳实践的完整指南，请参阅 `hugging-face-jobs` 技能 → *Token 使用指南*。

**推荐：** 始终通过 `secrets` 传递 token（服务端加密）：

```python
"secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ Automatic replacement with your logged-in token
```

## 验证清单

提交任何训练任务之前，请验证：

- [ ] TrainingArguments 中设置了 `push_to_hub=True`
- [ ] 已指定 `hub_model_id`（格式：`username/model-name`）
- [ ] 图像处理器将单独保存
- [ ] 已配置标签映射（id2label、label2id）
- [ ] 仓库名称不与现有仓库冲突
- [ ] 你对目标命名空间有写入权限

## 仓库设置

### 自动创建

如果仓库不存在，首次推送时会自动创建。

### 手动创建

在训练前创建仓库：

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(
    repo_id="username/detector-name",
    repo_type="model",
    private=False,  # or True for private repo
)
```

### 仓库命名

**有效名称：**
- `username/detr-cppe5`
- `username/yolos-object-detector`
- `organization/custom-detector`

**无效名称：**
- `detector-name`（缺少用户名）
- `username/detector name`（不允许空格）
- `username/DETECTOR`（不建议大写）

**推荐命名：**
- 包含模型架构：`detr-`、`yolos-`、`deta-`
- 包含数据集：`-cppe5`、`-coco`、`-voc`
- 描述性强：`detr-resnet50-cppe5` > `model1`

## 故障排除

### 错误：401 Unauthorized

**原因：** 未提供 HF_TOKEN、token 无效，或在 Trainer 初始化前未完成认证

**解决方案：**
1. 确认任务配置中包含 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 确认脚本在创建 `Trainer` 之前调用了 `login(token=hf_token)` 并设置了 `training_args.hub_token = hf_token`
3. 检查本地是否已登录：`hf auth whoami`
4. 重新登录：`hf auth login`

**根本原因：** `Trainer` 在 `push_to_hub=True` 时，会在 `__init__()` 期间调用 `create_repo(token=self.args.hub_token)`。在 Jobs 中依赖隐式的环境变量 token 解析不可靠。调用 `login()` 会全局保存 token，设置 `training_args.hub_token` 确保 Trainer 将其显式传递给所有 Hub API 调用。

### 错误：403 Forbidden

**原因：** 没有仓库的写入权限

**解决方案：**
1. 检查仓库命名空间是否与你的用户名匹配
2. 确认你是组织成员（如果使用组织命名空间）
3. 确认仓库不是私有的（如果访问组织仓库）

### 错误：Repository not found

**原因：** 仓库不存在且自动创建失败

**解决方案：**
1. 先手动创建仓库
2. 检查仓库名称格式
3. 确认命名空间存在

### 错误：训练期间推送失败

**原因：** 网络问题或 Hub 不可用

**解决方案：**
1. 训练继续但最终推送失败
2. 检查点可能已保存
3. 任务完成后重新手动推送

### 问题：模型加载成功但推理失败

**可能原因：**
1. 图像处理器未保存——确认已单独推送
2. 标签映射缺失——检查 config.json 是否包含 id2label
3. 图像尺寸错误——确认图像处理器与训练配置匹配

### 问题：模型已保存但不可见

**可能原因：**
1. 仓库是私有的——检查 https://huggingface.co/username
2. 命名空间错误——确认 `hub_model_id` 与登录身份匹配
3. 推送仍在进行——等待几分钟

## 训练后手动推送

如果训练完成但推送失败，手动推送：

```python
from transformers import AutoModelForObjectDetection, AutoImageProcessor

# Load from local checkpoint
model = AutoModelForObjectDetection.from_pretrained("./output_dir")
image_processor = AutoImageProcessor.from_pretrained("./output_dir")

# Push to Hub
model.push_to_hub("username/model-name", token="hf_abc123...")
image_processor.push_to_hub("username/model-name", token="hf_abc123...")
```

**注意：** 仅在任务未完成时可行（文件仍然存在）。

## 最佳实践

1. **始终启用 `push_to_hub=True`**
2. **单独保存图像处理器** - 推理的关键
3. **在训练前配置标签映射**
4. **对长时间训练使用检查点保存**
5. **在任务完成前验证 Hub 推送** 日志
6. **设置适当的 `save_total_limit`** 以避免过多检查点
7. **使用描述性仓库名称**（例如 `detr-cppe5` 而非 `detector1`）
8. **添加模型卡片**，包含：
   - 训练数据集
   - 评估指标（mAP、IoU）
   - 示例使用代码
   - 局限性
9. **为模型添加适当标签**：
   - `object-detection`
   - 架构：`detr`、`yolos`、`deta`
   - 数据集：`coco`、`voc`、`cppe-5`

## 监控推送进度

检查日志查看推送进度：

```python
hf_jobs("logs", {"job_id": "your-job-id"})
```

**查找：**
```
Pushing model to username/detector-name...
Upload file pytorch_model.bin: 100%
✅ Model pushed successfully
Pushing image processor...
✅ Image processor pushed successfully
```

## 示例：完整生产配置

```python
# production_detector.py
# /// script
# dependencies = [
#     "transformers>=4.30.0",
#     "torch>=2.0.0",
#     "torchvision>=0.15.0",
#     "datasets>=2.12.0",
#     "evaluate>=0.4.0"
# ]
# ///

from transformers import (
    AutoImageProcessor,
    AutoModelForObjectDetection,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset
import os
import torch

# Configuration
MODEL_NAME = "facebook/detr-resnet-50"
DATASET_NAME = "cppe-5"
HUB_MODEL_ID = "myusername/detr-cppe5-detector"
NUM_CLASSES = 5

# Class labels
id2label = {0: "Coverall", 1: "Face_Shield", 2: "Gloves", 3: "Goggles", 4: "Mask"}
label2id = {v: k for k, v in id2label.items()}

print(f"🔧 Loading dataset: {DATASET_NAME}")
dataset = load_dataset(DATASET_NAME, split="train")
print(f"✅ Dataset loaded: {len(dataset)} examples")

print(f"🔧 Loading model: {MODEL_NAME}")
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForObjectDetection.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_CLASSES,
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)
print("✅ Model loaded")

# Configure with comprehensive Hub settings
training_args = TrainingArguments(
    output_dir="detr-cppe5",

    # Hub configuration
    push_to_hub=True,
    hub_model_id=HUB_MODEL_ID,
    hub_strategy="checkpoint",  # Push checkpoints

    # Checkpoint configuration
    save_strategy="steps",
    save_steps=500,
    save_total_limit=3,

    # Training settings
    num_train_epochs=10,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    learning_rate=1e-4,
    warmup_steps=500,

    # Evaluation
    eval_strategy="steps",
    eval_steps=500,

    # Logging
    logging_steps=50,
    logging_first_step=True,

    # Performance
    fp16=True,  # Mixed precision training
    dataloader_num_workers=4,
)

# ✅ CRITICAL: Authenticate with Hub BEFORE creating Trainer
# login() saves the token globally so ALL hub operations can find it.
from huggingface_hub import login
hf_token = os.environ.get("HF_TOKEN") or os.environ.get("hfjob")
if hf_token:
    login(token=hf_token)
    training_args.hub_token = hf_token
elif training_args.push_to_hub:
    raise ValueError("HF_TOKEN not found! Add secrets={'HF_TOKEN': '$HF_TOKEN'} to job config.")

# Data collator
def collate_fn(batch):
    pixel_values = [item["pixel_values"] for item in batch]
    labels = [item["labels"] for item in batch]
    encoding = image_processor.pad(pixel_values, return_tensors="pt")
    return {
        "pixel_values": encoding["pixel_values"],
        "labels": labels
    }

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=collate_fn,
)

print("🚀 Starting training...")
trainer.train()

print("💾 Pushing final model to Hub...")
trainer.push_to_hub(
    commit_message="Upload trained DETR model on CPPE-5",
    tags=["object-detection", "detr", "cppe-5", "vision"],
)

print("💾 Pushing image processor to Hub...")
image_processor.push_to_hub(
    repo_id=HUB_MODEL_ID,
    commit_message="Upload image processor"
)

print("✅ Training complete!")
print(f"Model available at: https://huggingface.co/{HUB_MODEL_ID}")
print(f"\nTo use your model:")
print(f"```python")
print(f"from transformers import AutoImageProcessor, AutoModelForObjectDetection")
print(f"")
print(f"processor = AutoImageProcessor.from_pretrained('{HUB_MODEL_ID}')")
print(f"model = AutoModelForObjectDetection.from_pretrained('{HUB_MODEL_ID}')")
print(f"```")
```

**提交：**

```python
hf_jobs("uv", {
    "script": training_script_content,  # Pass script content as a string, NOT a filename
    "flavor": "a10g-large",
    "timeout": "8h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

## 推理示例

训练完成后，使用你的模型：

```python
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from PIL import Image
import torch

# Load model from Hub
processor = AutoImageProcessor.from_pretrained("username/detr-cppe5-detector")
model = AutoModelForObjectDetection.from_pretrained("username/detr-cppe5-detector")

# Load and process image
image = Image.open("test_image.jpg")
inputs = processor(images=image, return_tensors="pt")

# Run inference
with torch.no_grad():
    outputs = model(**inputs)

# Post-process results
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs,
    threshold=0.5,
    target_sizes=target_sizes
)[0]

# Print detections
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence "
        f"{round(score.item(), 3)} at location {box}"
    )
```

## 关键要点

**没有 `push_to_hub=True` 和 `secrets={"HF_TOKEN": "$HF_TOKEN"}`，所有训练结果将永久丢失。**

**对于目标检测，还需要记住：**
1. 单独保存图像处理器
2. 配置标签映射（id2label、label2id）
3. 包含适当的模型卡片元数据

提交任何训练任务之前，请始终验证以上三项都已配置。
