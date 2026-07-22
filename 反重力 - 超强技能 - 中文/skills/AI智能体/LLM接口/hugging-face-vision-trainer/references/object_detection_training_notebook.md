# 目标检测训练参考

## 目录
- 加载 CPPE-5 数据集
- 数据预处理（Albumentations 增强、COCO 标注格式化）
- 准备 mAP 计算函数
- 训练检测模型（TrainingArguments、Trainer 设置）
- 评估
- 推理（从 Hub 加载、运行预测、可视化结果）

---

目标检测是检测图像中实例（如人、建筑或汽车）的计算机视觉任务。目标检测模型接收图像作为输入，输出检测到的对象的边界框坐标和关联标签。一张图像可以包含多个对象，每个对象有自己的边界框和标签（例如可以同时有汽车和建筑），每个对象可以出现在图像的不同位置（例如图像中可以有多辆汽车）。此任务常用于自动驾驶中检测行人、路标和交通灯等。其他应用包括图像中的对象计数、图像搜索等。

本指南将介绍如何：

1. 在 [CPPE-5](https://huggingface.co/datasets/cppe-5) 数据集上微调 [DETR](https://huggingface.co/docs/transformers/model_doc/detr)——一个结合卷积骨干与编码器-解码器 Transformer 的模型。
2. 使用微调后的模型进行推理。

查看与此任务兼容的所有架构和检查点，推荐访问[任务页面](https://huggingface.co/tasks/object-detection)

开始前，确保安装了所有必要的库：

```bash
pip install -q datasets transformers accelerate timm trackio
pip install -q -U albumentations>=1.4.5 torchmetrics pycocotools
```

你将使用 🤗 Datasets 从 Hugging Face Hub 加载数据集，🤗 Transformers 训练模型，`albumentations` 增强数据。

我们鼓励你与社区分享模型。登录 Hugging Face 账户上传到 Hub。提示时输入 token 登录：

```py
>>> from huggingface_hub import notebook_login

>>> notebook_login()
```

首先定义全局常量，即模型名称和图像尺寸。本教程使用 conditional DETR 模型，因为它收敛更快。你可以选择 `transformers` 库中任何可用的目标检测模型。

```py
>>> MODEL_NAME = "microsoft/conditional-detr-resnet-50"  # 或 "facebook/detr-resnet-50"
>>> IMAGE_SIZE = 480
```

## 加载 CPPE-5 数据集

[CPPE-5 数据集](https://huggingface.co/datasets/cppe-5)包含 COVID-19 疫情背景下识别医疗个人防护装备（PPE）的图像标注。

首先加载数据集并从 `train` 创建 `validation` 划分：

```py
>>> from datasets import load_dataset

>>> cppe5 = load_dataset("cppe-5")

>>> if "validation" not in cppe5:
...     split = cppe5["train"].train_test_split(0.15, seed=1337)
...     cppe5["train"] = split["train"]
...     cppe5["validation"] = split["test"]

>>> cppe5
DatasetDict({
    train: Dataset({
        features: ['image_id', 'image', 'width', 'height', 'objects'],
        num_rows: 850
    })
    test: Dataset({
        features: ['image_id', 'image', 'width', 'height', 'objects'],
        num_rows: 29
    })
    validation: Dataset({
        features: ['image_id', 'image', 'width', 'height', 'objects'],
        num_rows: 150
    })
})
```

你会看到该数据集有 1000 张训练和验证图像，以及 29 张测试图像。

要熟悉数据，先看看样本长什么样。

```py
>>> cppe5["train"][0]
{
  'image_id': 366,
  'image': ,
  'width': 500,
  'height': 500,
  'objects': {
    'id': [1932, 1933, 1934],
    'area': [27063, 34200, 32431],
    'bbox': [[29.0, 11.0, 97.0, 279.0],
      [201.0, 1.0, 120.0, 285.0],
      [382.0, 0.0, 113.0, 287.0]],
    'category': [0, 0, 0]
  }
}
```

数据集中的样本有以下字段：

- `image_id`：样本图像 ID
- `image`：包含图像的 `PIL.Image.Image` 对象
- `width`：图像宽度
- `height`：图像高度
- `objects`：包含图像中对象边界框元数据的字典：
  - `id`：标注 ID
  - `area`：边界框面积
  - `bbox`：对象的边界框（[COCO 格式](https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/#coco)）
  - `category`：对象类别，可能值包括 `Coverall (0)`、`Face_Shield (1)`、`Gloves (2)`、`Goggles (3)` 和 `Mask (4)`

你可能注意到 `bbox` 字段遵循 COCO 格式，这正是 DETR 模型期望的格式。但 `objects` 内部的字段分组与 DETR 要求的标注格式不同。你需要在使用此数据训练前应用一些预处理转换。

要更深入了解数据，可视化数据集中的一个样本。

```py
>>> import numpy as np
>>> import os
>>> from PIL import Image, ImageDraw

>>> image = cppe5["train"][2]["image"]
>>> annotations = cppe5["train"][2]["objects"]
>>> draw = ImageDraw.Draw(image)

>>> categories = cppe5["train"].features["objects"]["category"].feature.names

>>> id2label = {index: x for index, x in enumerate(categories, start=0)}
>>> label2id = {v: k for k, v in id2label.items()}

>>> for i in range(len(annotations["id"])):
...     box = annotations["bbox"][i]
...     class_idx = annotations["category"][i]
...     x, y, w, h = tuple(box)
...     # 检查坐标是否归一化
...     if max(box) > 1.0:
...         # 坐标未归一化，无需重新缩放
...         x1, y1 = int(x), int(y)
...         x2, y2 = int(x + w), int(y + h)
...     else:
...         # 坐标已归一化，重新缩放
...         x1 = int(x * width)
...         y1 = int(y * height)
...         x2 = int((x + w) * width)
...         y2 = int((y + h) * height)
...     draw.rectangle((x, y, x + w, y + h), outline="red", width=1)
...     draw.text((x, y), id2label[class_idx], fill="white")

>>> image
```

要可视化带标签的边界框，可以从数据集元数据（特别是 `category` 字段）获取标签。你还需要创建标签 ID 到标签类别的映射（`id2label`）和反向映射（`label2id`）。设置模型时会用到它们。包含这些映射后，如果你在 Hugging Face Hub 上分享模型，其他人也能复用。请注意，上面绘制边界框的代码假设使用 `COCO` 格式 `(x_min, y_min, width, height)`。如需适配 `(x_min, y_min, x_max, y_max)` 等其他格式，需要调整代码。

作为熟悉数据的最后一步，检查潜在问题。目标检测数据集的一个常见问题是边界框"延伸"到图像边缘之外。这种"越界"边界框会在训练时引发错误，应当处理。此数据集中有少量此类样本。为简化本指南，我们在下方的变换中为 `BboxParams` 设置 `clip=True`。

## 数据预处理

微调模型时，必须预处理数据以精确匹配预训练模型使用的方法。[AutoImageProcessor](/docs/transformers/v5.1.0/en/model_doc/auto#transformers.AutoImageProcessor) 负责处理图像数据，创建 DETR 模型训练所需的 `pixel_values`、`pixel_mask` 和 `labels`。图像处理器有一些你无需关心的属性：

- `image_mean = [0.485, 0.456, 0.406 ]`
- `image_std = [0.229, 0.224, 0.225]`

这些是模型预训练时用于图像归一化的均值和标准差。在推理或微调预训练图像模型时，复制这些值至关重要。

从与要微调的模型相同的检查点实例化图像处理器。

```py
>>> from transformers import AutoImageProcessor

>>> MAX_SIZE = IMAGE_SIZE

>>> image_processor = AutoImageProcessor.from_pretrained(
...     MODEL_NAME,
...     do_resize=True,
...     size={"max_height": MAX_SIZE, "max_width": MAX_SIZE},
...     do_pad=True,
...     pad_size={"height": MAX_SIZE, "width": MAX_SIZE},
... )
```

在将图像传给 `image_processor` 前，对数据集应用两个预处理转换：

- 图像增强
- 重新格式化标注以满足 DETR 要求

首先，为防止模型在训练数据上过拟合，可以使用任何数据增强库对图像进行增强。这里使用 [Albumentations](https://albumentations.ai/docs/)。该库确保变换同时作用于图像并相应更新边界框。🤗 Datasets 库文档有详细的[目标检测图像增强指南](https://huggingface.co/docs/datasets/object_detection)，使用了相同的数据集作为示例。对图像应用一些几何和颜色变换。更多增强选项，探索 [Albumentations 演示空间](https://huggingface.co/spaces/qubvel-hf/albumentations-demo)。

```py
>>> import albumentations as A

>>> train_augment_and_transform = A.Compose(
...     [
...         A.Perspective(p=0.1),
...         A.HorizontalFlip(p=0.5),
...         A.RandomBrightnessContrast(p=0.5),
...         A.HueSaturationValue(p=0.1),
...     ],
...     bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True, min_area=25),
... )

>>> validation_transform = A.Compose(
...     [A.NoOp()],
...     bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True),
... )
```

`image_processor` 期望标注格式为：`{'image_id': int, 'annotations': list[Dict]}`，其中每个字典是一个 COCO 对象标注。添加一个函数来重新格式化单个样本的标注：

```py
>>> def format_image_annotations_as_coco(image_id, categories, areas, bboxes):
...     """将一组图像标注格式化为 COCO 格式

...     Args:
...         image_id (str): 图像 ID。如 "0001"
...         categories (list[int]): 与边界框对应的类别/类标签列表
...         areas (list[float]): 与边界框对应的面积列表
...         bboxes (list[tuple[float]]): COCO 格式的边界框列表
...             ([center_x, center_y, width, height]，绝对坐标)

...     Returns:
...         dict: {
...             "image_id": 图像 ID,
...             "annotations": 格式化后的标注列表
...         }
...     """
...     annotations = []
...     for category, area, bbox in zip(categories, areas, bboxes):
...         formatted_annotation = {
...             "image_id": image_id,
...             "category_id": category,
...             "iscrowd": 0,
...             "area": area,
...             "bbox": list(bbox),
...         }
...         annotations.append(formatted_annotation)

...     return {
...         "image_id": image_id,
...         "annotations": annotations,
...     }

```

现在可以组合图像和标注变换，用于一批样本：

```py
>>> def augment_and_transform_batch(examples, transform, image_processor, return_pixel_mask=False):
...     """为目标检测任务应用增强并将标注格式化为 COCO 格式"""

...     images = []
...     annotations = []
...     for image_id, image, objects in zip(examples["image_id"], examples["image"], examples["objects"]):
...         image = np.array(image.convert("RGB"))

...         # 应用增强
...         output = transform(image=image, bboxes=objects["bbox"], category=objects["category"])
...         images.append(output["image"])

...         # 将标注格式化为 COCO 格式
...         formatted_annotations = format_image_annotations_as_coco(
...             image_id, output["category"], objects["area"], output["bboxes"]
...         )
...         annotations.append(formatted_annotations)

...     # 应用图像处理器变换：调整大小、缩放、归一化
...     result = image_processor(images=images, annotations=annotations, return_tensors="pt")

...     if not return_pixel_mask:
...         result.pop("pixel_mask", None)

...     return result
```

使用 🤗 Datasets 的 [with_transform](https://huggingface.co/docs/datasets/v4.5.0/en/package_reference/main_classes#datasets.Dataset.with_transform) 方法将此预处理函数应用到整个数据集。此方法在加载数据集元素时即时应用变换。

此时可以检查变换后数据集中样本的样子。你应该看到 `pixel_values` 张量、`pixel_mask` 张量和 `labels`。

```py
>>> from functools import partial

>>> # 为批量创建变换函数并应用到数据集划分
>>> train_transform_batch = partial(
...     augment_and_transform_batch, transform=train_augment_and_transform, image_processor=image_processor
... )
>>> validation_transform_batch = partial(
...     augment_and_transform_batch, transform=validation_transform, image_processor=image_processor
... )

>>> cppe5["train"] = cppe5["train"].with_transform(train_transform_batch)
>>> cppe5["validation"] = cppe5["validation"].with_transform(validation_transform_batch)
>>> cppe5["test"] = cppe5["test"].with_transform(validation_transform_batch)

>>> cppe5["train"][15]
{'pixel_values': tensor([[[ 1.9235,  1.9407,  1.9749,  ..., -0.7822, -0.7479, -0.6965],
          [ 1.9578,  1.9749,  1.9920,  ..., -0.7993, -0.7650, -0.7308],
          [ 2.0092,  2.0092,  2.0263,  ..., -0.8507, -0.8164, -0.7822],
          ...,
          [ 0.0741,  0.0741,  0.0741,  ...,  0.0741,  0.0741,  0.0741],
          [ 0.0741,  0.0741,  0.0741,  ...,  0.0741,  0.0741,  0.0741],
          [ 0.0741,  0.0741,  0.0741,  ...,  0.0741,  0.0741,  0.0741]],

          [[ 1.6232,  1.6408,  1.6583,  ...,  0.8704,  1.0105,  1.1331],
          [ 1.6408,  1.6583,  1.6758,  ...,  0.8529,  0.9930,  1.0980],
          [ 1.6933,  1.6933,  1.7108,  ...,  0.8179,  0.9580,  1.0630],
          ...,
          [ 0.2052,  0.2052,  0.2052,  ...,  0.2052,  0.2052,  0.2052],
          [ 0.2052,  0.2052,  0.2052,  ...,  0.2052,  0.2052,  0.2052],
          [ 0.2052,  0.2052,  0.2052,  ...,  0.2052,  0.2052,  0.2052]],

          [[ 1.8905,  1.9080,  1.9428,  ..., -0.1487, -0.0964, -0.0615],
          [ 1.9254,  1.9428,  1.9603,  ..., -0.1661, -0.1138, -0.0790],
          [ 1.9777,  1.9777,  1.9951,  ..., -0.2010, -0.1138, -0.0790],
          ...,
          [ 0.4265,  0.4265,  0.4265,  ...,  0.4265,  0.4265,  0.4265],
          [ 0.4265,  0.4265,  0.4265,  ...,  0.4265,  0.4265,  0.4265],
          [ 0.4265,  0.4265,  0.4265,  ...,  0.4265,  0.4265,  0.4265]]]),
  'labels': {'image_id': tensor([688]), 'class_labels': tensor([3, 4, 2, 0, 0]), 'boxes': tensor([[0.4700, 0.1933, 0.1467, 0.0767],
          [0.4858, 0.2600, 0.1150, 0.1000],
          [0.4042, 0.4517, 0.1217, 0.1300],
          [0.4242, 0.3217, 0.3617, 0.5567],
          [0.6617, 0.4033, 0.5400, 0.4533]]), 'area': tensor([ 4048.,  4140.,  5694., 72478., 88128.]), 'iscrowd': tensor([0, 0, 0, 0, 0]), 'orig_size': tensor([480, 480])}}
```

你已成功增强各个图像并准备了标注。但预处理还没完成。最后一步，创建自定义 `collate_fn` 将图像批量组合。将图像（现在是 `pixel_values`）填充到批次中最大图像的大小，并创建对应的 `pixel_mask` 指示哪些像素是真实的（1）哪些是填充的（0）。

```py
>>> import torch

>>> def collate_fn(batch):
...     data = {}
...     data["pixel_values"] = torch.stack([x["pixel_values"] for x in batch])
...     data["labels"] = [x["labels"] for x in batch]
...     if "pixel_mask" in batch[0]:
...         data["pixel_mask"] = torch.stack([x["pixel_mask"] for x in batch])
...     return data

```

## 准备 mAP 计算函数

目标检测模型通常用一组 COCO 风格的指标评估。我们将使用 `torchmetrics` 计算 `mAP`（平均精度均值）和 `mAR`（平均召回均值）指标，并将其封装为 `compute_metrics` 函数，以便在 [Trainer](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.Trainer) 中用于评估。

训练中使用的边界框中间格式是 `YOLO`（归一化），但我们将以 `Pascal VOC`（绝对）格式计算指标，以正确处理框面积。定义一个将边界框转换为 `Pascal VOC` 格式的函数：

```py
>>> from transformers.image_transforms import center_to_corners_format

>>> def convert_bbox_yolo_to_pascal(boxes, image_size):
...     """
...     将边界框从 YOLO 格式 (x_center, y_center, width, height) 范围 [0, 1]
...     转换为 Pascal VOC 格式 (x_min, y_min, x_max, y_max) 绝对坐标。

...     Args:
...         boxes (torch.Tensor): YOLO 格式的边界框
...         image_size (tuple[int, int]): 图像尺寸，格式 (height, width)

...     Returns:
...         torch.Tensor: Pascal VOC 格式的边界框 (x_min, y_min, x_max, y_max)
...     """
...     # 从中心格式转换为角点格式
...     boxes = center_to_corners_format(boxes)

...     # 转换为绝对坐标
...     height, width = image_size
...     boxes = boxes * torch.tensor([[width, height, width, height]])

...     return boxes
```

然后在 `compute_metrics` 函数中，从评估循环结果中收集 `predicted` 和 `target` 边界框、分数和标签，传给评分函数。

```py
>>> import numpy as np
>>> from dataclasses import dataclass
>>> from torchmetrics.detection.mean_ap import MeanAveragePrecision

>>> @dataclass
>>> class ModelOutput:
...     logits: torch.Tensor
...     pred_boxes: torch.Tensor

>>> @torch.no_grad()
>>> def compute_metrics(evaluation_results, image_processor, threshold=0.0, id2label=None):
...     """
...     计算目标检测任务的平均 mAP、mAR 及其变体。

...     Args:
...         evaluation_results (EvalPrediction): 评估的预测和目标。
...         threshold (float, optional): 按置信度过滤预测框的阈值。默认 0.0。
...         id2label (Optional[dict], optional): 类别 ID 到类别名的映射。默认 None。

...     Returns:
...         Mapping[str, float]: 字典形式的指标
...     """

...     predictions, targets = evaluation_results.predictions, evaluation_results.label_ids

...     # 指标计算需要提供：
...     #  - 目标格式为包含 "boxes"、"labels" 键的字典列表
...     #  - 预测格式为包含 "boxes"、"scores"、"labels" 键的字典列表

...     image_sizes = []
...     post_processed_targets = []
...     post_processed_predictions = []

...     # 以所需格式收集目标用于指标计算
...     for batch in targets:
...         # 收集图像尺寸，预测后处理时需要
...         batch_image_sizes = torch.tensor(np.array([x["orig_size"] for x in batch]))
...         image_sizes.append(batch_image_sizes)
...         # 以所需格式收集目标用于指标计算
...         # 框已转换为模型训练所需的 YOLO 格式
...         # 这里将它们转换为 Pascal VOC 格式 (x_min, y_min, x_max, y_max)
...         for image_target in batch:
...             boxes = torch.tensor(image_target["boxes"])
...             boxes = convert_bbox_yolo_to_pascal(boxes, image_target["orig_size"])
...             labels = torch.tensor(image_target["class_labels"])
...             post_processed_targets.append({"boxes": boxes, "labels": labels})

...     # 以所需格式收集预测用于指标计算，
...     # 模型生成 YOLO 格式的框，然后 image_processor 将其转换为 Pascal VOC 格式
...     for batch, target_sizes in zip(predictions, image_sizes):
...         batch_logits, batch_boxes = batch[1], batch[2]
...         output = ModelOutput(logits=torch.tensor(batch_logits), pred_boxes=torch.tensor(batch_boxes))
...         post_processed_output = image_processor.post_process_object_detection(
...             output, threshold=threshold, target_sizes=target_sizes
...         )
...         post_processed_predictions.extend(post_processed_output)

...     # 计算指标
...     metric = MeanAveragePrecision(box_format="xyxy", class_metrics=True)
...     metric.update(post_processed_predictions, post_processed_targets)
...     metrics = metric.compute()

...     # 将每类指标列表替换为每个类别的独立指标
...     classes = metrics.pop("classes")
...     map_per_class = metrics.pop("map_per_class")
...     mar_100_per_class = metrics.pop("mar_100_per_class")
...     for class_id, class_map, class_mar in zip(classes, map_per_class, mar_100_per_class):
...         class_name = id2label[class_id.item()] if id2label is not None else class_id.item()
...         metrics[f"map_{class_name}"] = class_map
...         metrics[f"mar_100_{class_name}"] = class_mar

...     metrics = {k: round(v.item(), 4) for k, v in metrics.items()}

...     return metrics

>>> eval_compute_metrics_fn = partial(
...     compute_metrics, image_processor=image_processor, id2label=id2label, threshold=0.0
... )
```

## 训练检测模型

前面几节已完成大部分工作，现在可以训练模型了！
此数据集中的图像即使调整大小后仍然很大。这意味着微调此模型至少需要一个 GPU。

训练步骤如下：

1. 使用 [AutoModelForObjectDetection](/docs/transformers/v5.1.0/en/model_doc/auto#transformers.AutoModelForObjectDetection) 从与预处理相同的检查点加载模型。
2. 在 [TrainingArguments](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.TrainingArguments) 中定义训练超参数。
3. 将训练参数连同模型、数据集、图像处理器和数据整理器传给 [Trainer](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.Trainer)。
4. 调用 [train()](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.Trainer.train) 微调模型。

从与预处理相同的检查点加载模型时，记得传递之前从数据集元数据创建的 `label2id` 和 `id2label` 映射。此外，指定 `ignore_mismatched_sizes=True` 以用新的分类头替换现有分类头。

```py
>>> from transformers import AutoModelForObjectDetection

>>> model = AutoModelForObjectDetection.from_pretrained(
...     MODEL_NAME,
...     id2label=id2label,
...     label2id=label2id,
...     ignore_mismatched_sizes=True,
... )
```

在 [TrainingArguments](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.TrainingArguments) 中使用 `output_dir` 指定模型保存位置，然后按需配置超参数。`num_train_epochs=30` 在 Google Colab T4 GPU 上训练约 35 分钟，增加 epoch 数可获得更好结果。

重要说明：

- 将 `remove_unused_columns` 设为 `False`。
- 设 `eval_do_concat_batches=False` 以获得正确的评估结果。图像有不同数量的目标框，如果批量拼接，将无法确定哪些框属于哪张图像。

如需通过推送到 Hub 分享模型，将 `push_to_hub` 设为 `True`（必须登录 Hugging Face 才能上传模型）。

```py
>>> from transformers import TrainingArguments

>>> training_args = TrainingArguments(
...     output_dir="detr_finetuned_cppe5",
...     num_train_epochs=30,
...     fp16=False,
...     per_device_train_batch_size=8,
...     dataloader_num_workers=4,
...     learning_rate=5e-5,
...     lr_scheduler_type="cosine",
...     weight_decay=1e-4,
...     max_grad_norm=0.01,
...     metric_for_best_model="eval_map",
...     greater_is_better=True,
...     load_best_model_at_end=True,
...     eval_strategy="epoch",
...     save_strategy="epoch",
...     save_total_limit=2,
...     remove_unused_columns=False,
...     report_to="trackio",
...     run_name="cppe",
...     eval_do_concat_batches=False,
...     push_to_hub=True,
... )
```

最后，将所有内容组合，调用 [train()](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.Trainer.train)：

```py
>>> from transformers import Trainer

>>> trainer = Trainer(
...     model=model,
...     args=training_args,
...     train_dataset=cppe5["train"],
...     eval_dataset=cppe5["validation"],
...     processing_class=image_processor,
...     data_collator=collate_fn,
...     compute_metrics=eval_compute_metrics_fn,
... )

>>> trainer.train()
```

训练运行 30 个 epoch（CPPE-5 在 T4 GPU 上约 26 分钟）。第 30 个 epoch 的结果：

| 指标 | 值 |
|------|-----|
| 训练损失 | 0.994 |
| 验证损失 | 1.346 |
| mAP | 0.277 |
| mAP@50 | 0.555 |
| mAP@75 | 0.253 |
| mAR@100 | 0.443 |

第 30 个 epoch 的各类别 mAP：Coverall 0.530，Face Shield 0.276，Gloves 0.175，Goggles 0.157，Mask 0.249。

关键观察：
- mAP 在早期 epoch 快速提升（epoch 1 为 0.009 → epoch 10 达 0.18），之后逐渐收敛
- 大对象检测更好（mAP_large=0.524）优于小对象（mAP_small=0.148）
- 类别不平衡明显：Coverall mAP 最高（0.530），Goggles 最低（0.157）

<!-- 完整的逐 epoch 训练指标表为简洁起见省略。 -->


如果在 `training_args` 中设置了 `push_to_hub=True`，训练检查点会推送到 Hugging Face Hub。训练完成后，调用 [push_to_hub()](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.Trainer.push_to_hub) 方法将最终模型也推送到 Hub。

```py
>>> trainer.push_to_hub()
```

## 评估

```py
>>> from pprint import pprint

>>> metrics = trainer.evaluate(eval_dataset=cppe5["test"], metric_key_prefix="test")
>>> pprint(metrics)
{'epoch': 30.0,
  'test_loss': 1.0877351760864258,
  'test_map': 0.4116,
  'test_map_50': 0.741,
  'test_map_75': 0.3663,
  'test_map_Coverall': 0.5937,
  'test_map_Face_Shield': 0.5863,
  'test_map_Gloves': 0.3416,
  'test_map_Goggles': 0.1468,
  'test_map_Mask': 0.3894,
  'test_map_large': 0.5637,
  'test_map_medium': 0.3257,
  'test_map_small': 0.3589,
  'test_mar_1': 0.323,
  'test_mar_10': 0.5237,
  'test_mar_100': 0.5587,
  'test_mar_100_Coverall': 0.6756,
  'test_mar_100_Face_Shield': 0.7294,
  'test_mar_100_Gloves': 0.4721,
  'test_mar_100_Goggles': 0.4125,
  'test_mar_100_Mask': 0.5038,
  'test_mar_large': 0.7283,
  'test_mar_medium': 0.4901,
  'test_mar_small': 0.4469,
  'test_runtime': 1.6526,
  'test_samples_per_second': 17.548,
  'test_steps_per_second': 2.42}
```

通过调整 [TrainingArguments](/docs/transformers/v5.1.0/en/main_classes/trainer#transformers.TrainingArguments) 中的超参数可以进一步提升这些结果。试试看！

## 推理

现在你已经微调了模型、完成了评估并上传到 Hugging Face Hub，可以用它进行推理了。

```py
>>> import torch
>>> import requests

>>> from PIL import Image, ImageDraw
>>> from transformers import AutoImageProcessor, AutoModelForObjectDetection

>>> url = "https://images.pexels.com/photos/8413299/pexels-photo-8413299.jpeg?auto=compress&cs=tinysrgb&w=630&h=375&dpr=2"
>>> image = Image.open(requests.get(url, stream=True).raw)
```

从 Hugging Face Hub 加载模型和图像处理器（跳过以使用本会话中已训练的模型）：

```py
>>> from accelerate import Accelerator

>>> device = Accelerator().device
>>> model_repo = "qubvel-hf/detr_finetuned_cppe5"

>>> image_processor = AutoImageProcessor.from_pretrained(model_repo)
>>> model = AutoModelForObjectDetection.from_pretrained(model_repo)
>>> model = model.to(device)
```

检测边界框：

```py

>>> with torch.no_grad():
...     inputs = image_processor(images=[image], return_tensors="pt")
...     outputs = model(**inputs.to(device))
...     target_sizes = torch.tensor([[image.size[1], image.size[0]]])
...     results = image_processor.post_process_object_detection(outputs, threshold=0.3, target_sizes=target_sizes)[0]

>>> for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
...     box = [round(i, 2) for i in box.tolist()]
...     print(
...         f"Detected {model.config.id2label[label.item()]} with confidence "
...         f"{round(score.item(), 3)} at location {box}"
...     )
Detected Gloves with confidence 0.683 at location [244.58, 124.33, 300.35, 185.13]
Detected Mask with confidence 0.517 at location [143.73, 64.58, 219.57, 125.89]
Detected Gloves with confidence 0.425 at location [179.15, 155.57, 262.4, 226.35]
Detected Coverall with confidence 0.407 at location [307.13, -1.18, 477.82, 318.06]
Detected Coverall with confidence 0.391 at location [68.61, 126.66, 309.03, 318.89]
```

绘制结果：

```py
>>> draw = ImageDraw.Draw(image)

>>> for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
...     box = [round(i, 2) for i in box.tolist()]
...     x, y, x2, y2 = tuple(box)
...     draw.rectangle((x, y, x2, y2), outline="red", width=1)
...     draw.text((x, y), model.config.id2label[label.item()], fill="white")

>>> image
```

    
