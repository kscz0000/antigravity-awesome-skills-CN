---
name: image-generator
description: 使用 Gemini 的 Nano Banana Pro 模型（gemini-3-pro-image-preview）生成和编辑图片。当用户要求生成图片、创建视觉内容、编辑照片、制作 Logo、生成产品模型或执行任何图片生成/编辑任务时使用此技能。触发词：生成图片、编辑图片、创建视觉、制作Logo、图片生成、AI绘画、文生图、图生图、图片编辑、image generator、generate image、edit image
allowed-tools: Read, Write, Bash, WebFetch
category: "media"
risk: "safe"
source: "official"
source_repo: "dair-ai/dair-academy-plugins"
source_type: "official"
date_added: "2026-06-19"
author: "DAIR.AI"
license: "MIT"
license_source: "https://github.com/dair-ai/dair-academy-plugins/blob/main/README.md#license"
tags:
  - dair-academy
  - ai
  - workflow
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 图片生成器

## 何时使用

当工作流匹配以下用户请求时使用：使用 Gemini 的 Nano Banana Pro 模型（gemini-3-pro-image-preview）生成和编辑图片。当用户要求生成图片、创建视觉内容、编辑照片、制作 Logo、生成产品模型或执行任何图片生成/编辑任务时使用此技能。


_来源：[dair-ai/dair-academy-plugins](https://github.com/dair-ai/dair-academy-plugins)（MIT）。_

本技能使用 Google 的 Gemini Nano Banana Pro 模型（`gemini-3-pro-image-preview`）生成和编辑图片。

## 重要：需要预先配置

使用本技能前，用户必须设置 `GEMINI_API_KEY` 环境变量：

1. 从 [Google AI Studio](https://aistudio.google.com/) 获取免费 API 密钥
2. 在 shell 配置文件（`~/.zshrc`、`~/.bashrc` 等）中导出密钥：
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
3. 重启终端或运行 `source ~/.zshrc`（或 `~/.bashrc`）

**未完成此配置，技能将无法运行。**

## 预检

在发起任何 API 调用前，验证密钥是否已设置：

```bash
if [ -z "$GEMINI_API_KEY" ]; then
  echo "ERROR: GEMINI_API_KEY is not set. Please export it in your shell profile."
  exit 1
fi
```

如果密钥缺失，停止并告知用户按上述说明设置。

## 配置

**模型**：`gemini-3-pro-image-preview`

**API 密钥**：从 `GEMINI_API_KEY` 环境变量读取

## 迭代用户提供的图片

当用户提供要编辑或迭代的图片路径时，使用以下工作流：

### 步骤 1：读取图片并编码为 base64

```bash
# Get the image path from user
IMG_PATH="/path/to/user/image.png"

# Detect mime type
if [[ "$IMG_PATH" == *.png ]]; then
    MIME_TYPE="image/png"
elif [[ "$IMG_PATH" == *.jpg ]] || [[ "$IMG_PATH" == *.jpeg ]]; then
    MIME_TYPE="image/jpeg"
elif [[ "$IMG_PATH" == *.webp ]]; then
    MIME_TYPE="image/webp"
else
    MIME_TYPE="image/png"
fi

# Encode to base64 (works on both macOS and Linux)
if [[ "$(uname)" == "Darwin" ]]; then
    IMG_BASE64=$(base64 -i "$IMG_PATH")
else
    IMG_BASE64=$(base64 -w0 "$IMG_PATH")
fi
```

### 步骤 2：发送图片及编辑提示（基于文件的方式）

**重要：** 始终使用基于文件的方式构建请求体。Base64 编码的图片过大，无法作为命令行参数传递，会导致"参数列表过长"错误。

```bash
# User's edit request
EDIT_PROMPT="Add a santa hat to the person in this image"

# Write request to a JSON file (avoids command line length limits)
cat > /tmp/gemini_request.json << JSONEOF
{
  "contents": [{
    "parts": [
      {"text": "$EDIT_PROMPT"},
      {
        "inline_data": {
          "mime_type": "$MIME_TYPE",
          "data": "$IMG_BASE64"
        }
      }
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
JSONEOF

# Call the API using the file
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/gemini_request.json > /tmp/gemini_response.json
```

### 步骤 3：提取并保存编辑后的图片

```bash
# Extract image from response and save
python3 -c "
import json
import base64

with open('/tmp/gemini_response.json') as f:
    data = json.load(f)

for part in data['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        img_data = part['inlineData']['data']
        mime = part['inlineData']['mimeType']
        ext = 'png' if 'png' in mime else 'jpg'
        with open('edited_image.' + ext, 'wb') as out:
            out.write(base64.b64decode(img_data))
        print(f'Saved: edited_image.{ext}')
    elif 'text' in part:
        print(part['text'])
"
```

### 完整示例（基于文件）

迭代图片时，始终使用基于文件的请求：

```bash
# Variables
IMG_PATH="/path/to/image.png"
EDIT_PROMPT="Make the background a sunset beach"
OUTPUT_PATH="edited_output.png"
# Detect mime type and encode
MIME_TYPE=$([[ "$IMG_PATH" == *.png ]] && echo "image/png" || echo "image/jpeg")
IMG_BASE64=$(base64 -i "$IMG_PATH" 2>/dev/null || base64 -w0 "$IMG_PATH")

# Write request to file (required - base64 images are too large for command line)
cat > /tmp/gemini_request.json << JSONEOF
{
  "contents": [{
    "parts": [
      {"text": "$EDIT_PROMPT"},
      {"inline_data": {"mime_type": "$MIME_TYPE", "data": "$IMG_BASE64"}}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
JSONEOF

# Call API and extract image
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/gemini_request.json > /tmp/gemini_response.json

# Save the output image
python3 -c "
import json, base64
with open('/tmp/gemini_response.json') as f:
    data = json.load(f)
for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
    if 'inlineData' in part:
        with open('$OUTPUT_PATH', 'wb') as f:
            f.write(base64.b64decode(part['inlineData']['data']))
        print('Saved: $OUTPUT_PATH')
"
```

### 多图输入（组合/合成）

组合多张图片的元素时（同样使用基于文件的方式）：

```bash
IMG1_PATH="/path/to/image1.png"
IMG2_PATH="/path/to/image2.png"
PROMPT="Put the dress from the first image on the person in the second image"
IMG1_BASE64=$(base64 -i "$IMG1_PATH" 2>/dev/null || base64 -w0 "$IMG1_PATH")
IMG2_BASE64=$(base64 -i "$IMG2_PATH" 2>/dev/null || base64 -w0 "$IMG2_PATH")

# Write request to file
cat > /tmp/gemini_request.json << JSONEOF
{
  "contents": [{
    "parts": [
      {"text": "$PROMPT"},
      {"inline_data": {"mime_type": "image/png", "data": "$IMG1_BASE64"}},
      {"inline_data": {"mime_type": "image/png", "data": "$IMG2_BASE64"}}
    ]
  }],
  "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
JSONEOF

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/gemini_request.json > /tmp/gemini_response.json
```

## 功能

### 文生图
- 根据文本描述生成高质量图片
- 支持照片写实、风格化和艺术化输出
- 图片中准确渲染文字（Logo、信息图、图表）

### 图片编辑
- 在图片中添加或移除元素
- 基于语义遮罩的局部重绘（编辑特定区域）
- 风格迁移（将艺术风格应用于照片）
- 多图合成（组合多张图片的元素）

### 高级功能
- **高分辨率**：1K、2K 或 4K 输出
- **宽高比**：1:1、2:3、3:2、3:4、4:3、4:5、5:4、9:16、16:9、21:9
- **Google 搜索锚定**：基于实时数据生成图片
- **多轮编辑**：通过对话迭代优化图片
- **最多 14 张参考图**：组合多个输入进行复杂合成

## API 用法

### 基础文生图（Python）

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # Optional
            image_size="2K"       # Optional: "1K", "2K", "4K"
        )
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

### 基础文生图（JavaScript）

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
    model: "gemini-3-pro-image-preview",
    contents: "Your prompt here",
    config: {
        responseModalities: ['TEXT', 'IMAGE'],
        imageConfig: {
            aspectRatio: "16:9",
            imageSize: "2K"
        }
    }
});

for (const part of response.candidates[0].content.parts) {
    if (part.text) {
        console.log(part.text);
    } else if (part.inlineData) {
        const buffer = Buffer.from(part.inlineData.data, "base64");
        fs.writeFileSync("generated_image.png", buffer);
    }
}
```

### REST API（curl）

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Your prompt here"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > output.png
```

### 图片编辑（含输入图片）

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

input_image = Image.open('input.png')
prompt = "Add a wizard hat to the cat in this image"

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt, input_image],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("edited_image.png")
```

### 多图合成

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

image1 = Image.open('dress.png')
image2 = Image.open('model.png')
prompt = "Put the dress from the first image on the model from the second image"

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[image1, image2, prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="3:4",
            image_size="2K"
        )
    )
)
```

### 使用 Google 搜索锚定

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Visualize the current weather forecast for San Francisco",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
        tools=[{"google_search": {}}]
    )
)
```

## 提示词最佳实践

### 1. 描述式而非关键词式
不要写：`cat, wizard hat, cute`
应写：`A fluffy orange cat wearing a small knitted wizard hat, sitting on a wooden floor with soft natural lighting from a window`

### 2. 指定风格和氛围
- 摄影术语："shot with 85mm lens"、"soft bokeh background"、"golden hour lighting"
- 艺术风格："in the style of Van Gogh"、"minimalist illustration"、"photorealistic"
- 氛围："warm and cozy atmosphere"、"dramatic noir lighting"

### 3. 图片中的文字
明确指定：
- 要渲染的准确文字内容
- 字体风格（描述性）："clean, bold, sans-serif font"
- 位置和大小

### 4. 编辑操作
- 描述要改变什么和保留什么
- 使用"keep everything else unchanged"
- 清晰引用特定元素

### 5. 产品/商业图片
提及：
- 灯光设置："three-point softbox lighting"
- 背景："clean white studio background"
- 拍摄角度："slightly elevated 45-degree shot"

## 分辨率与宽高比参考

| 宽高比 | 1K 分辨率 | 2K 分辨率 | 4K 分辨率 |
|--------|-----------|-----------|-----------|
| 1:1    | 1024x1024 | 2048x2048 | 4096x4096 |
| 16:9   | 1376x768  | 2752x1536 | 5504x3072 |
| 9:16   | 768x1376  | 1536x2752 | 3072x5504 |
| 3:2    | 1264x848  | 2528x1696 | 5056x3392 |
| 2:3    | 848x1264  | 1696x2528 | 3392x5056 |

## 常见用例

### Logo 创作
```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'.
The text should be in a clean, bold, sans-serif font.
Black and white color scheme. Put the logo in a circle.
```

### 产品摄影
```
A high-resolution, studio-lit product photograph of a minimalist ceramic
coffee mug in matte black on a polished concrete surface. Three-point
softbox lighting with soft, diffused highlights. Slightly elevated
45-degree camera angle. Sharp focus on steam rising from the coffee.
```

### 风格迁移
```
Transform this photograph of a city street at night into Vincent van Gogh's
'Starry Night' style. Preserve the composition but render with swirling,
impasto brushstrokes and deep blues with bright yellows.
```

### 信息图
```
Create a vibrant infographic explaining photosynthesis as a recipe.
Show "ingredients" (sunlight, water, CO2) and "finished dish" (sugar/energy).
Style like a colorful kids' cookbook, suitable for 4th graders.
```

## 错误处理

常见问题：
- **未返回图片**：检查 `response_modalities` 是否包含 `'IMAGE'`
- **安全过滤器**：某些提示词可能被阻止；尝试重新措辞
- **速率限制**：实现指数退避重试
- **大图片**：4K 输出需确保足够的超时设置

## 依赖

使用 Python SDK：
```bash
pip install google-genai pillow
```

使用 JavaScript：
```bash
npm install @google/genai
```

## 重要说明

- 所有生成的图片包含 SynthID 水印
- 模型对复杂提示词使用"思考"过程
- 为获得最佳文字渲染效果，先生成文字，再请求包含该文字的图片
- API 不存储图片——请在本地保存输出


## 局限性

- 当工作流指定了上游工具、账户、API 密钥或本地配置时，需要相应配置。
- 未经用户明确批准，不执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的产物或建议视为最终结果前，请对照用户的真实来源进行验证。
