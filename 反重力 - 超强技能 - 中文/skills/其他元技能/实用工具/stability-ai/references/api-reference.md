# API 参考 — Stability AI v2beta

## 目录

1. [认证](#认证)
2. [生成端点](#生成端点)
3. [编辑端点](#编辑端点)
4. [放大端点](#放大端点)
5. [通用参数](#通用参数)
6. [响应格式](#响应格式)
7. [错误码](#错误码)

---

## 认证

所有请求使用 `Authorization` 头：

```
Authorization: Bearer sk-sua-chave-aqui
```

Base URL：`https://api.stability.ai/v2beta`

格式：所有请求使用 `multipart/form-data`（非 JSON）。

## 生成端点

### POST /stable-image/generate/sd3

使用 Stable Diffusion 3.5 生成图像。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | 是 | 文本提示词（最多 10000 字符） |
| `model` | string | 否 | `sd3.5-large`（默认）、`sd3.5-large-turbo`、`sd3.5-medium` |
| `aspect_ratio` | string | 否 | 比例如 `1:1`、`16:9` 等，默认：`1:1` |
| `negative_prompt` | string | 否 | 生成时需要排除的元素 |
| `seed` | int | 否 | 种子值，用于可复现生成（0 到 4294967294） |
| `output_format` | string | 否 | `png`（默认）、`jpeg`、`webp` |
| `image` | file | 否 | 图生图的基准图像 |
| `strength` | float | 否 | 图生图变换强度（0.0-1.0，默认 0.7） |
| `mode` | string | 否 | `text-to-image`（默认）或 `image-to-image` |

**可用模型：**
- `sd3.5-large` — 最佳综合品质（推荐）
- `sd3.5-large-turbo` — 快速，步数更少
- `sd3.5-medium` — 速度与品质平衡

### POST /stable-image/generate/ultra

最高品质的高端生成。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | 是 | 文本提示词 |
| `aspect_ratio` | string | 否 | 默认：`1:1` |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值，用于可复现生成 |
| `output_format` | string | 否 | `png`、`jpeg`、`webp` |

不支持 `model` 参数（固定使用 Ultra 模型）。

### POST /stable-image/generate/core

快速高效的生成。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | 是 | 文本提示词 |
| `aspect_ratio` | string | 否 | 默认：`1:1` |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值，用于可复现生成 |
| `output_format` | string | 否 | `png`、`jpeg`、`webp` |
| `style_preset` | string | 否 | 风格预设（如 `cinematic`） |

## 编辑端点

### POST /stable-image/edit/inpaint

使用蒙版编辑图像局部区域。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 原始图像 |
| `prompt` | string | 是 | 蒙版区域需要生成的内容 |
| `mask` | file | 否 | 蒙版（白色 = 待编辑区域） |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |

未上传 `mask` 时，模型会自动推断编辑区域。

### POST /stable-image/edit/search-and-replace

查找并替换图像中的对象。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 原始图像 |
| `prompt` | string | 是 | 替换后的内容 |
| `search_prompt` | string | 是 | 要查找/替换的内容 |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |

### POST /stable-image/edit/erase

擦除图像局部（用上下文填充）。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 原始图像 |
| `mask` | file | 否 | 待擦除区域的蒙版 |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |

### POST /stable-image/edit/outpaint

将图像扩展到原始边界之外。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 原始图像 |
| `prompt` | string | 否 | 扩展区域的内容描述 |
| `left` | int | 否 | 向左扩展的像素数（0-2000） |
| `right` | int | 否 | 向右扩展的像素数（0-2000） |
| `up` | int | 否 | 向上扩展的像素数（0-2000） |
| `down` | int | 否 | 向下扩展的像素数（0-2000） |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |

至少一个方向的值必须大于 0。

### POST /stable-image/edit/remove-background

移除图像背景。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 待移除背景的图像 |
| `output_format` | string | 否 | `png`（带透明通道） |

返回透明背景的 PNG 图像。

## 放大端点

### POST /stable-image/upscale/conservative

提升分辨率，最大程度保持原图忠实度。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 待放大的图像 |
| `prompt` | string | 是 | 图像描述 |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |
| `creativity` | float | 否 | 创意自由度（0.2-0.5） |

### POST /stable-image/upscale/creative

提升分辨率并创意性地添加细节。

两步流程：
1. POST 发起请求 — 返回 `generation_id`
2. GET 获取结果（可能需要等待）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | file | 是 | 待放大的图像 |
| `prompt` | string | 是 | 图像描述 |
| `negative_prompt` | string | 否 | 需要排除的元素 |
| `seed` | int | 否 | 种子值 |
| `output_format` | string | 否 | 输出格式 |
| `creativity` | float | 否 | 创意自由度（0.2-0.5） |

## 通用参数

### aspect_ratio
支持的比例：`1:1`、`2:3`、`3:2`、`4:5`、`5:4`、`9:16`、`16:9`、`9:21`、`21:9`

### output_format
- `png` — 无损，文件较大
- `jpeg` — 有损压缩，文件较小
- `webp` — 现代格式，均衡选择

### seed
- 范围：0 到 4294967294
- 相同种子 + 相同提示词 = 相同图像（可复现）
- 0 或省略 = 随机

## 响应格式

### 成功（200）
- 头部 `Content-Type: image/png`（或 jpeg/webp）
- Body：图像字节数据
- 头部 `seed`：生成使用的种子值
- 头部 `finish-reason`：`SUCCESS` 或 `CONTENT_FILTERED`

### 成功（JSON 格式）
如果请求带 `Accept: application/json`：
```json
{
  "image": "base64_encoded_image_data",
  "seed": 12345,
  "finish_reason": "SUCCESS"
}
```

## 错误码

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 400 | 请求格式错误 | 检查参数 |
| 401 | 未授权 | 检查 API Key |
| 402 | 需要付款 | 检查额度/套餐 |
| 403 | 禁止访问 | 内容被审核拦截 |
| 404 | 未找到 | 端点地址错误 |
| 429 | 请求频率超限 | 等待后重试（自动重试） |
| 500 | 服务器内部错误 | 等待几秒后重试 |

### 错误响应格式
```json
{
  "id": "error-id",
  "name": "bad_request",
  "errors": ["prompt must not be empty"]
}
```

## 重要请求头

### 请求头
```
Authorization: Bearer sk-...
Content-Type: multipart/form-data
Accept: image/* (ou application/json)
```

### 响应头
```
Content-Type: image/png
seed: 12345
finish-reason: SUCCESS
```
