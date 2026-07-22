# 2slides API 参考

2slides 幻灯片生成服务的完整 API 文档。

## 基础 URL

```
https://2slides.com/api/v1
```

## 认证

所有 API 请求都需要在 Authorization 请求头中携带 Bearer 令牌进行身份认证：

```
Authorization: Bearer YOUR_API_KEY
```

获取 API 密钥：https://2slides.com/api

请将 API 密钥保存到环境变量中：`SLIDES_2SLIDES_API_KEY`

## 端点

### 1. 生成幻灯片

根据用户输入生成幻灯片，可选择主题。

**端点：** `POST /slides/generate`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**请求体：**
```json
{
  "userInput": "string (required) - Content to convert into slides",
  "themeId": "string (required) - Theme ID from themes/search",
  "responseLanguage": "string (optional, default: 'Auto') - Language code",
  "mode": "string (optional, default: 'sync') - 'sync' or 'async'"
}
```

**支持的语言：**
Auto, English, Simplified Chinese (简体中文), Traditional Chinese (繁體中文), Spanish, Arabic, Portuguese, Indonesian, Japanese, Russian, Hindi, French, German, Vietnamese, Turkish, Polish, Italian, Korean

**响应（同步模式）：**
```json
{
  "slideUrl": "https://2slides.com/slides/...",
  "pdfUrl": "https://2slides.com/slides/.../download",
  "status": "completed"
}
```

**响应（异步模式）：**
```json
{
  "jobId": "abc123...",
  "status": "pending"
}
```

**说明：**
- **同步模式**：阻塞等待生成完成后直接返回结果（耗时约 30-60 秒）
- **异步模式**：立即返回 jobId，需通过 `/jobs/{jobId}` 轮询获取结果

---

### 2. 仿照此风格生成（参考图）

生成匹配参考图风格的幻灯片（Nano Banana Pro 模式）。

**端点：** `POST /slides/create-like-this`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**请求体：**
```json
{
  "userInput": "string (required) - Content for slides",
  "referenceImageUrl": "string (required) - URL or base64 of reference image",
  "responseLanguage": "string (optional, default: 'Auto')",
  "aspectRatio": "string (optional, default: '16:9') - width:height format",
  "resolution": "string (optional, default: '2K') - '1K', '2K', or '4K'",
  "page": "number (optional, default: 1) - 0 for auto-detection, max 100",
  "contentDetail": "string (optional, default: 'concise') - 'concise' or 'standard'"
}
```

**分辨率选项：**
- **1K**：标准画质
- **2K**：高画质（默认）
- **4K**：超高清画质

**内容详略选项：**
- **concise**：简洁模式，以关键词为主
- **standard**：标准模式，内容详尽

**页数参数：**
- 设为 `0` 启用自动检测页数
- 设为具体数字（1-100）指定精确页数

**响应：**
```json
{
  "success": true,
  "data": {
    "jobId": "608f8997-5207-480c-9ff2-d2475cba6b9d",
    "status": "success",
    "message": "Successfully generated N slides",
    "downloadUrl": "https://...pdf...",
    "jobUrl": "https://2slides.com/workspace?jobId=...",
    "createdAt": 1770108913384,
    "updatedAt": 1770108934015,
    "slidePageCount": 3,
    "successCount": 3,
    "failedCount": 0
  }
}
```

**响应字段：**
- `success`：请求是否成功的布尔值
- `data.jobId`：唯一的任务标识符
- `data.status`：生成状态（"success" 或 "failed"）
- `data.message`：人类可读的状态消息
- `data.downloadUrl`：PDF 直链（临时链接，1 小时后失效）
- `data.jobUrl`：在 2slides 工作区中查看幻灯片的链接
- `data.slidePageCount`：生成的幻灯片总数
- `data.successCount`：成功生成的幻灯片数
- `data.failedCount`：生成失败的幻灯片数

**说明：**
- 该端点始终以同步方式执行
- 处理时间：每页约 30 秒
- 典型响应时间：1-2 页通常需要 30-60 秒
- 自动生成 PDF 文件
- 匹配参考图的风格与设计
- **超时建议**：将超时设置为 `max(120, pages * 40)` 秒

---

### 3. 创建 PDF 幻灯片

基于文本内容并结合可选的设计规格，生成自定义设计的幻灯片。

**端点：** `POST /slides/create-pdf-slides`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**请求体：**
```json
{
  "userInput": "string (required) - Content for slides",
  "responseLanguage": "string (optional, default: 'Auto')",
  "aspectRatio": "string (optional, default: '16:9') - width:height format",
  "resolution": "string (optional, default: '2K') - '1K', '2K', or '4K'",
  "page": "number (optional, default: 1) - 0 for auto-detection, max 100",
  "contentDetail": "string (optional, default: 'concise') - 'concise' or 'standard'",
  "designSpec": "string (optional) - Design specifications (e.g., 'modern minimalist')"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "jobId": "608f8997-5207-480c-9ff2-d2475cba6b9d",
    "status": "success",
    "message": "Successfully generated N slides",
    "downloadUrl": "https://...pdf...",
    "jobUrl": "https://2slides.com/workspace?jobId=...",
    "slidePageCount": 3,
    "successCount": 3,
    "failedCount": 0
  }
}
```

**说明：**
- 与 create-like-this 类似，但无需提供参考图
- 根据内容和设计规格，由 AI 自动生成自定义设计
- 积分消耗相同：100 积分/页（1K/2K），200 积分/页（4K）
- 处理时间：每页约 30 秒
- 始终以同步方式执行

---

### 4. 生成旁白

为幻灯片添加 AI 语音旁白，支持单角色或多角色模式。

**端点：** `POST /slides/generate-narration`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**请求体：**
```json
{
  "jobId": "string (required) - Job ID from slide generation (UUID format)",
  "language": "string (optional, default: 'Auto') - Language for narration",
  "voice": "string (optional, default: 'Puck') - Voice name from available voices",
  "multiSpeaker": "boolean (optional, default: false) - Enable multi-speaker mode"
}
```

**可用语音（共 30 种）：**
Puck, Aoede, Charon, Kore, Fenrir, Phoebe, Asteria, Luna, Stella, Theia, Helios, Atlas, Clio, Melpomene, Calliope, Erato, Euterpe, Polyhymnia, Terpsichore, Thalia, Urania, Zeus, Hera, Poseidon, Athena, Apollo, Artemis, Ares, Aphrodite, Hephaestus

**响应：**
```json
{
  "success": true,
  "jobId": "abc123...",
  "status": "pending",
  "message": "Narration generation started"
}
```

**说明：**
- 任务必须完成后才能添加旁白
- Nano Banana 任务的任务 ID 必须为 UUID 格式
- 费用：每页 210 积分（文本 10 积分，音频 200 积分）
- 异步执行 —— 通过 /jobs/{jobId} 轮询获取结果
- 多角色模式使用不同的语音以增加多样性
- 支持 19 种语言外加自动检测

---

### 5. 下载幻灯片页面与语音

将幻灯片导出为 PNG 文件，将语音旁白导出为 WAV 文件，并打包为 ZIP 压缩包。

**端点：** `POST /slides/download-slides-pages-voices`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**请求体：**
```json
{
  "jobId": "string (required) - Job ID from slide generation"
}
```

**响应：**
```json
{
  "success": true,
  "downloadUrl": "https://...zip...",
  "message": "Download ready"
}
```

**压缩包内容：**
- Pages：每页幻灯片对应的 PNG 文件
- Voices：WAV 音频文件（前提是已生成旁白）
- Transcripts：旁白对应的文本文字稿

**说明：**
- **费用：完全免费**（不消耗任何积分）
- 下载链接仅 **1 小时** 内有效
- 高质量 PNG 导出
- 音频采用 WAV 格式
- 包含全部幻灯片与语音文件

---

### 6. 搜索主题

搜索可用的演示文稿主题。

**端点：** `GET /themes/search`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
```

**查询参数：**
```
query: string (required) - Search keyword
limit: number (optional, default: 20, max: 100)
```

**响应：**
```json
{
  "themes": [
    {
      "id": "theme_id_123",
      "name": "Professional Blue",
      "description": "Clean professional theme with blue accents",
      "previewUrl": "https://..."
    }
  ],
  "count": 1
}
```

---

### 7. 查询任务状态

获取异步生成任务的状态与结果。

**端点：** `GET /jobs/{jobId}`

**请求头：**
```
Authorization: Bearer YOUR_API_KEY
```

**路径参数：**
```
jobId: string (required) - Job ID from async generation
```

**响应：**
```json
{
  "jobId": "abc123",
  "status": "completed|pending|failed",
  "slideUrl": "https://2slides.com/slides/...",
  "pdfUrl": "https://2slides.com/slides/.../download",
  "narrationStatus": "completed|pending|not_started",
  "error": "error message if failed"
}
```

**状态取值：**
- `pending`：任务仍在处理中
- `completed`：幻灯片已生成完成
- `failed`：生成失败（详见 error 字段）

**旁白状态取值：**
- `not_started`：尚未请求生成旁白
- `pending`：旁白正在生成中
- `completed`：旁白已生成完成

**轮询建议：**
建议每 20-30 秒轮询一次，避免给服务器造成压力

---

## 错误处理

所有端点均返回标准的 HTTP 状态码：

- `200 OK`：请求成功
- `400 Bad Request`：参数无效
- `401 Unauthorized`：缺失或无效的 API 密钥
- `404 Not Found`：资源未找到
- `429 Too Many Requests`：超出速率限制
- `500 Internal Server Error`：服务器内部错误

**错误响应格式：**
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

**常见错误码：**
- `INSUFFICIENT_CREDITS`：账户积分不足
- `INVALID_JOB_ID`：任务 ID 不存在或格式无效
- `RATE_LIMIT_EXCEEDED`：请求过于频繁（详见下文的速率限制）
- `JOB_NOT_COMPLETED`：必须等待任务完成后才能添加旁白
- `INVALID_UUID`：任务 ID 必须为 UUID 格式（适用于 Nano Banana 任务）

---

## 积分消耗

- **Fast PPT（generate 端点）**：每页 10 积分
- **Nano Banana 1K/2K（create-like-this、create-pdf-slides）**：每页 100 积分
- **Nano Banana 4K**：每页 200 积分
- **语音旁白**：每页 210 积分（文本 10 积分，音频 200 积分）
- **下载导出**：免费（不消耗积分）

## 购买积分

2slides 采用**按量付费的积分制**，不设订阅套餐。

**积分套餐**（当前优惠：最高 8 折）：

| 积分数 | 价格 | 单千积分成本 | 折扣 |
|---------|-------|---------------|---------|
| 2,000 | $5.00 | $2.50 | — |
| 4,000 | $9.50 | $2.38 | 5% |
| 10,000 | $22.50 | $2.25 | 10% |
| 20,000 | $42.50 | $2.13 | 15% |
| 40,000 | $80.00 | $2.00 | 20% |

**主要权益：**
- 新用户注册即赠 **500 免费积分**（约可生成 50 页 Fast PPT）
- **积分永久有效，不过期**
- 无月费订阅
- 3 天无理由退款窗口
- 购买地址：https://2slides.com/pricing

**费用示例：**
- 10 页 Fast PPT 演示稿：100 积分（使用最大套餐时约 $0.25）
- 10 页 Nano Banana 2K 演示稿：1,000 积分（使用最大套餐时约 $2.00）
- 10 页带旁白的演示稿：2,100 积分（使用最大套餐时约 $4.20）

## 速率限制

不同端点有不同的速率限制：

- **Fast PPT（generate）**：每分钟 10 次请求
- **Nano Banana（create-like-this、create-pdf-slides）**：每分钟 6 次请求

**最佳实践：**
- 每 20-30 秒轮询一次异步任务，避免给服务器造成压力
- 遇到限流（429 错误）时，请等待一段时间后再重试
- 在 https://2slides.com/api 查看你所购套餐的速率限制

## 下载链接有效期

所有下载链接（PDF、ZIP 包）仅在 **1 小时** 内有效。请在生成完成后及时下载文件。

---

## 最佳实践

### 内容格式化

**为获得最佳效果，建议清晰地组织内容结构：**

```
Title: Introduction to AI

Section 1: Machine Learning
- Definition
- Key concepts
- Applications

Section 2: Deep Learning
- Neural networks
- Training process
- Use cases
```

### 选择同步还是异步模式

- 快速生成（少于 5 页）时**使用同步模式**
- 大型演示稿（超过 5 页）时**使用异步模式**
- 集成到支持轮询的工作流中时**使用异步模式**

### 主题选择

1. 使用相关关键词搜索主题
2. 如有预览链接，可先预览主题效果
3. 在生成请求中使用主题 ID
4. 留空主题字段则使用默认样式

### 语言支持

通过指定 `responseLanguage` 来生成不同语言的幻灯片：
- `"Auto"` - 自动语言检测（默认）
- `"English"` - English
- `"Simplified Chinese"` - 简体中文
- `"Traditional Chinese"` - 繁體中文
- `"Spanish"` - Español
- `"Arabic"` - العربية
- `"Portuguese"` - Português
- `"Indonesian"` - Bahasa Indonesia
- `"Japanese"` - 日本語
- `"Russian"` - Русский
- `"Hindi"` - हिन्दी
- `"French"` - Français
- `"German"` - Deutsch
- `"Vietnamese"` - Tiếng Việt
- `"Turkish"` - Türkçe
- `"Polish"` - Polski
- `"Italian"` - Italiano
- `"Korean"` - 한국어