# 图像分类

## 目录
- 加载 Food-101 数据集
- 预处理（ViT 图像处理器、torchvision 变换）
- 评估（准确率指标、compute_metrics）
- 训练（TrainingArguments、Trainer 设置、推送到 Hub）
- 推理（pipeline、手动预测）

---

图像分类为图像分配标签或类别。与文本或音频分类不同，输入是构成图像的像素值。图像分类有许多应用，例如自然灾害后的损害检测、作物健康监测或帮助筛查医学图像中的疾病迹象。

本指南演示如何：

1. 在 [Food-101](https://huggingface.co/datasets/ethz/food101) 数据集上微调 [ViT](../model_doc/vit) 以分类图像中的食物项。
2. 使用微调后的模型进行推理。

要查看与此任务兼容的所有架构和检查点，我们建议查看[任务页面](https://huggingface.co/tasks/image-classification)

开始之前，请确保已安装所有必要的库：

```bash
pip install transformers datasets evaluate accelerate pillow torchvision scikit-learn trackio
```

我们建议您登录 Hugging Face 账户以上传和与社区分享您的模型。出现提示时，输入您的令牌进行登录：

```py
>>> from huggingface_hub import notebook_login

>>> notebook_login()
```

## 加载 Food-101 数据集

首先从 🤗 Datasets 库加载 Food-101 数据集的较小子集。这将让您有机会进行实验，确保一切正常，然后再花更多时间在完整数据集上训练。

```py
>>> from datasets import load_dataset

>>> food = load_dataset("ethz/food101", split="train[:5000]")
```

使用 [train_test_split](https://huggingface.co/docs/datasets/v4.5.0/en/package_reference/main_classes#datasets.Dataset.train_test_split) 方法将数据集的 `train` 分割拆分为训练集和测试集：

```py
>>> food = food.train_test_split(test_size=0.2)
```

然后查看一个示例：

```py
>>> food["train"][0]
{'image': ,
 'label': 79}
```

数据集中的每个示例有两个字段：

- `image`：食物项的 PIL 图像
- `label`：食物项的标签类别

为了让模型更容易从标签 ID 获取标签名称，创建一个将标签名称映射到整数及其反向映射的字典：

```py
>>> labels = food["train"].features["label"].names
>>> label2id, id2label = dict(), dict()
>>> for i, label in enumerate(labels):
...     label2id[label] = str(i)
...     id2label[str(i)] = label
```

现在可以将标签 ID 转换为标签名称：

```py
>>> id2label[str(79)]
'prime_rib'
```

## 预处理

下一步是加载 ViT 图像处理器，将图像处理为张量：

```py
>>> from transformers import AutoImageProcessor

>>> checkpoint = "google/vit-base-patch16-224-in21k"
>>> image_processor = AutoImageProcessor.from_pretrained(checkpoint)
```

对图像应用一些图像变换，使模型更鲁棒，防止过拟合。这里使用 torchvision 的 [`transforms`](https://pytorch.org/vision/stable/transforms.html) 模块，但您也可以使用任何喜欢的图像库。

裁剪图像的随机部分，调整大小，并使用图像均值和标准差进行归一化：

```py
>>> from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

>>> normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
>>> size = (
...     image_processor.size["shortest_edge"]
...     if "shortest_edge" in image_processor.size
...     else (image_processor.size["height"], image_processor.size["width"])
... )
>>> _transforms = Compose([RandomResizedCrop(size), ToTensor(), normalize])
```

然后创建一个预处理函数来应用变换并返回图像的 `pixel_values`——模型的输入：

```py
>>> def transforms(examples):
...     examples["pixel_values"] = [_transforms(img.convert("RGB")) for img in examples["image"]]
...     del examples["image"]
...     return examples
```

要对整个数据集应用预处理函数，使用 🤗 Datasets 的 [with_transform](https://huggingface.co/docs/datasets/v4.5.0/en/package_reference/main_classes#datasets.Dataset.with_transform) 方法。变换在加载数据集元素时即时应用：

```py
>>> food = food.with_transform(transforms)
```

现在使用 [DefaultDataCollator](/docs/transformers/v5.2.0/en/main_classes/data_collator#transformers.DefaultDataCollator) 创建一批示例。与 🤗 Transformers 中的其他数据整理器不同，`DefaultDataCollator` 不应用额外的预处理，如填充。

```py
>>> from transformers import DefaultDataCollator

>>> data_collator = DefaultDataCollator()
```

## 评估

在训练期间包含指标通常有助于评估模型性能。您可以使用 🤗 [Evaluate](https://huggingface.co/docs/evaluate/index) 库快速加载评估方法。对于此任务，加载 [accuracy](https://huggingface.co/spaces/evaluate-metric/accuracy) 指标（参见 🤗 Evaluate [快速入门](https://huggingface.co/docs/evaluate/a_quick_tour) 了解如何加载和计算指标）：

```py
>>> import evaluate

>>> accuracy = evaluate.load("accuracy")
```

然后创建一个函数，将预测和标签传递给 [compute](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/main_classes#evaluate.EvaluationModule.compute) 以计算准确率：

```py
>>> import numpy as np

>>> def compute_metrics(eval_pred):
...     predictions, labels = eval_pred
...     predictions = np.argmax(predictions, axis=1)
...     return accuracy.compute(predictions=predictions, references=labels)
```

您的 `compute_metrics` 函数现在已准备就绪，设置训练时将返回使用它。

## 训练

如果您不熟悉使用 [Trainer](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.Trainer) 微调模型，请查看[此处](../training#train-with-pytorch-trainer)的基本教程！

现在可以开始训练模型了！使用 [AutoModelForImageClassification](/docs/transformers/v5.2.0/en/model_doc/auto#transformers.AutoModelForImageClassification) 加载 ViT。指定标签数量以及预期标签数量和标签映射：

```py
>>> from transformers import AutoModelForImageClassification, TrainingArguments, Trainer

>>> model = AutoModelForImageClassification.from_pretrained(
...     checkpoint,
...     num_labels=len(labels),
...     id2label=id2label,
...     label2id=label2id,
... )
```

此时，只剩下三个步骤：

1. 在 [TrainingArguments](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.TrainingArguments) 中定义训练超参数。重要的是不要删除未使用的列，因为这会删除 `image` 列。没有 `image` 列，就无法创建 `pixel_values`。设置 `remove_unused_columns=False` 以防止此行为！唯一必需的其他参数是 `output_dir`，用于指定保存模型的位置。通过设置 `push_to_hub=True` 将此模型推送到 Hub（需要登录 Hugging Face 才能上传模型）。在每个 epoch 结束时，[Trainer](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.Trainer) 将评估准确率并保存训练检查点。
2. 将训练参数传递给 [Trainer](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.Trainer)，连同模型、数据集、分词器、数据整理器和 `compute_metrics` 函数。
3. 调用 [train()](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.Trainer.train) 微调模型。

```py
>>> training_args = TrainingArguments(
...     output_dir="my_awesome_food_model",
...     remove_unused_columns=False,
...     eval_strategy="epoch",
...     save_strategy="epoch",
...     learning_rate=5e-5,
...     per_device_train_batch_size=16,
...     gradient_accumulation_steps=4,
...     per_device_eval_batch_size=16,
...     num_train_epochs=3,
...     warmup_steps=0.1,
...     logging_steps=10,
...     report_to="trackio",
...     run_name="food101",
...     load_best_model_at_end=True,
...     metric_for_best_model="accuracy",
...     push_to_hub=True,
... )

>>> trainer = Trainer(
...     model=model,
...     args=training_args,
...     data_collator=data_collator,
...     train_dataset=food["train"],
...     eval_dataset=food["test"],
...     processing_class=image_processor,
...     compute_metrics=compute_metrics,
... )

>>> trainer.train()
```

训练完成后，使用 [push_to_hub()](/docs/transformers/v5.2.0/en/main_classes/trainer#transformers.Trainer.push_to_hub) 方法将模型分享到 Hub，这样每个人都可以使用您的模型：

```py
>>> trainer.push_to_hub()
```

有关如何为图像分类微调模型的更深入示例，请查看相应的 [PyTorch notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/image_classification.ipynb)。

## 推理

很好，现在您已经微调了模型，可以使用它进行推理了！

加载要进行推理的图像：

```py
>>> ds = load_dataset("ethz/food101", split="validation[:10]")
>>> image = ds["image"][0]
```

    

尝试微调模型进行推理的最简单方法是在 [pipeline()](/docs/transformers/v5.2.0/en/main_classes/pipelines#transformers.pipeline) 中使用它。使用您的模型实例化一个图像分类的 `pipeline`，并将图像传递给它：

```py
>>> from transformers import pipeline

>>> classifier = pipeline("image-classification", model="my_awesome_food_model")
>>> classifier(image)
[{'score': 0.31856709718704224, 'label': 'beignets'},
 {'score': 0.015232225880026817, 'label': 'bruschetta'},
 {'score': 0.01519392803311348, 'label': 'chicken_wings'},
 {'score': 0.013022331520915031, 'label': 'pork_chop'},
 {'score': 0.012728818692266941, 'label': 'prime_rib'}]
```

如果需要，也可以手动复制 `pipeline` 的结果：

加载图像处理器以预处理图像并将 `input` 返回为 PyTorch 张量：

```py
>>> from transformers import AutoImageProcessor
>>> import torch

>>> image_processor = AutoImageProcessor.from_pretrained("my_awesome_food_model")
>>> inputs = image_processor(image, return_tensors="pt")
```

将输入传递给模型并返回 logits：

```py
>>> from transformers import AutoModelForImageClassification

>>> model = AutoModelForImageClassification.from_pretrained("my_awesome_food_model")
>>> with torch.no_grad():
...     logits = model(**inputs).logits
```

获取概率最高的预测标签，并使用模型的 `id2label` 映射将其转换为标签：

```py
>>> predicted_label = logits.argmax(-1).item()
>>> model.config.id2label[predicted_label]
'beignets'
```