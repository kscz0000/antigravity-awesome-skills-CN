# 在 Hugging Face Trainer 中使用 timm 模型

Transformers 通过 `TimmWrapper` 类为 timm 模型提供一等支持。你可以加载任何 timm 模型并直接与 `Trainer` API 配合用于图像分类。以下是工作原理：

## 加载 timm 模型

`TimmWrapperForImageClassification` 类（位于 `transformers/src/transformers/models/timm_wrapper/modeling_timm_wrapper.py`）封装 timm 模型，使其完全兼容 Trainer API。可以通过 `Auto` 类加载：

```python
from transformers import AutoModelForImageClassification, AutoImageProcessor, Trainer, TrainingArguments

# 加载 timm 模型用于图像分类
checkpoint = "timm/resnet50.a1_in1k"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)
model = AutoModelForImageClassification.from_pretrained(
    checkpoint,
    num_labels=10,  # 设置为你的类别数
    ignore_mismatched_sizes=True,  # 更改 num_labels 时需要
)
```

## 关键细节

1. **图像处理器**：`TimmWrapperImageProcessor` 自动从 timm 配置中解析正确的变换。它同时暴露 `val_transforms` 和 `train_transforms`（含数据增强），如代码所示：

```64:65:transformers/src/transformers/models/timm_wrapper/image_processing_timm_wrapper.py
        # useful for training, see examples/pytorch/image-classification/run_image_classification.py
        self.train_transforms = timm.data.create_transform(**self.data_config, is_training=True)
```

2. **内置损失计算**：`TimmWrapperForImageClassification.forward()` 接受 `labels` 参数并自动计算交叉熵损失，正是 Trainer 所期望的：

```374:376:transformers/src/transformers/models/timm_wrapper/modeling_timm_wrapper.py
        loss = None
        if labels is not None:
            loss = self.loss_function(labels, logits, self.config)
```

3. **返回 `ImageClassifierOutput`**：输出格式是标准 transformers 输出，Trainer 无缝处理。

## 完整训练示例

```python
from transformers import AutoModelForImageClassification, AutoImageProcessor, Trainer, TrainingArguments
from datasets import load_dataset

# 加载数据集
dataset = load_dataset("food101", split="train[:5000]")
dataset = dataset.train_test_split(test_size=0.2)

# 加载 timm 模型 + 处理器
checkpoint = "timm/resnet50.a1_in1k"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)
model = AutoModelForImageClassification.from_pretrained(
    checkpoint,
    num_labels=101,
    ignore_mismatched_sizes=True,
)

# 预处理
def transform(batch):
    batch["pixel_values"] = [image_processor(img)["pixel_values"][0] for img in batch["image"]]
    batch["labels"] = batch["label"]
    return batch

dataset["train"].set_transform(transform)
dataset["test"].set_transform(transform)

# 训练
training_args = TrainingArguments(
    output_dir="./timm-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=50,
    remove_unused_columns=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

trainer.train()
```

Hub 上任何 timm 检查点（以 `timm/` 为前缀）都开箱即用（ResNet、EfficientNet、ViT、ConvNeXt 等）。封装器处理 timm 接口与 Trainer 期望格式之间的所有转换。
