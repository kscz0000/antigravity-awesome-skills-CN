---
name: azure-ai-vision-imageanalysis-py
description: Azure AI Vision 图像分析 SDK，支持图像描述、标签、物体检测、OCR、人员检测和智能裁剪。用于计算机视觉和图像理解任务。触发词：Azure图像分析、图像描述、OCR文字提取、物体检测、智能裁剪、人员检测、图像标签、计算机视觉、Image Analysis、Vision SDK
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Vision Image Analysis SDK for Python

Azure AI Vision 4.0 图像分析客户端库，支持图像描述、标签、物体检测、OCR 等功能。

## 安装

```bash
pip install azure-ai-vision-imageanalysis
```

## 环境变量

```bash
VISION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
VISION_KEY=<your-api-key>  # 如果使用 API 密钥
```

## 身份验证

### API 密钥

```python
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["VISION_ENDPOINT"]
key = os.environ["VISION_KEY"]

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
```

### Entra ID（推荐）

```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.identity import DefaultAzureCredential

client = ImageAnalysisClient(
    endpoint=os.environ["VISION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 从 URL 分析图像

```python
from azure.ai.vision.imageanalysis.models import VisualFeatures

image_url = "https://example.com/image.jpg"

result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[
        VisualFeatures.CAPTION,
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
        VisualFeatures.READ,
        VisualFeatures.PEOPLE,
        VisualFeatures.SMART_CROPS,
        VisualFeatures.DENSE_CAPTIONS
    ],
    gender_neutral_caption=True,
    language="en"
)
```

## 从文件分析图像

```python
with open("image.jpg", "rb") as f:
    image_data = f.read()

result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS]
)
```

## 图像描述

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.CAPTION],
    gender_neutral_caption=True
)

if result.caption:
    print(f"Caption: {result.caption.text}")
    print(f"Confidence: {result.caption.confidence:.2f}")
```

## 密集描述（多区域）

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.DENSE_CAPTIONS]
)

if result.dense_captions:
    for caption in result.dense_captions.list:
        print(f"Caption: {caption.text}")
        print(f"  Confidence: {caption.confidence:.2f}")
        print(f"  Bounding box: {caption.bounding_box}")
```

## 标签

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.TAGS]
)

if result.tags:
    for tag in result.tags.list:
        print(f"Tag: {tag.name} (confidence: {tag.confidence:.2f})")
```

## 物体检测

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.OBJECTS]
)

if result.objects:
    for obj in result.objects.list:
        print(f"Object: {obj.tags[0].name}")
        print(f"  Confidence: {obj.tags[0].confidence:.2f}")
        box = obj.bounding_box
        print(f"  Bounding box: x={box.x}, y={box.y}, w={box.width}, h={box.height}")
```

## OCR（文字提取）

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.READ]
)

if result.read:
    for block in result.read.blocks:
        for line in block.lines:
            print(f"Line: {line.text}")
            print(f"  Bounding polygon: {line.bounding_polygon}")
            
            # 单词级别详情
            for word in line.words:
                print(f"  Word: {word.text} (confidence: {word.confidence:.2f})")
```

## 人员检测

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.PEOPLE]
)

if result.people:
    for person in result.people.list:
        print(f"Person detected:")
        print(f"  Confidence: {person.confidence:.2f}")
        box = person.bounding_box
        print(f"  Bounding box: x={box.x}, y={box.y}, w={box.width}, h={box.height}")
```

## 智能裁剪

```python
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.SMART_CROPS],
    smart_crops_aspect_ratios=[0.9, 1.33, 1.78]  # 竖屏、4:3、16:9
)

if result.smart_crops:
    for crop in result.smart_crops.list:
        print(f"Aspect ratio: {crop.aspect_ratio}")
        box = crop.bounding_box
        print(f"  Crop region: x={box.x}, y={box.y}, w={box.width}, h={box.height}")
```

## 异步客户端

```python
from azure.ai.vision.imageanalysis.aio import ImageAnalysisClient
from azure.identity.aio import DefaultAzureCredential

async def analyze_image():
    async with ImageAnalysisClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        result = await client.analyze_from_url(
            image_url=image_url,
            visual_features=[VisualFeatures.CAPTION]
        )
        print(result.caption.text)
```

## 视觉功能

| 功能 | 描述 |
|---------|-------------|
| `CAPTION` | 描述图像的单句描述 |
| `DENSE_CAPTIONS` | 多个区域的描述 |
| `TAGS` | 内容标签（物体、场景、动作） |
| `OBJECTS` | 带边界框的物体检测 |
| `READ` | OCR 文字提取 |
| `PEOPLE` | 带边界框的人员检测 |
| `SMART_CROPS` | 缩略图建议裁剪区域 |

## 错误处理

```python
from azure.core.exceptions import HttpResponseError

try:
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION]
    )
except HttpResponseError as e:
    print(f"Status code: {e.status_code}")
    print(f"Reason: {e.reason}")
    print(f"Message: {e.error.message}")
```

## 图像要求

- 格式：JPEG、PNG、GIF、BMP、WEBP、ICO、TIFF、MPO
- 最大大小：20 MB
- 尺寸：50x50 到 16000x16000 像素

## 最佳实践

1. **仅选择所需功能**以优化延迟和成本
2. **使用异步客户端**处理高吞吐量场景
3. **处理 HttpResponseError**以应对无效图像或认证问题
4. **启用 gender_neutral_caption**以获得包容性描述
5. **指定语言**以获得本地化描述
6. **使用匹配缩略图需求的 smart_crops_aspect_ratios**
7. **缓存结果**当多次分析同一图像时

## 适用场景
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
