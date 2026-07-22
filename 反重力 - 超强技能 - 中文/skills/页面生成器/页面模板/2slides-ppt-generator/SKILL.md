---
name: 2slides-ppt-generator
description: "通过 2slides API 实现 AI 驱动的演示文稿生成——根据文本创建幻灯片、匹配参考图风格、将文档摘要成演示稿、添加 AI 语音旁白，以及导出页面/音频。适用于任何"制作幻灯片"、"创建演示稿"或"从文档生成幻灯片"的请求。触发词：制作幻灯片、创建 PPT、生成演示文稿、文档转幻灯片、参考图生成幻灯片、添加语音旁白。"
category: api-integration
risk: safe
source: community
source_repo: 2slides/slides-generation-2slides-skills
source_type: community
date_added: "2026-06-05"
author: 2slides
tags: [presentations, slides, powerpoint, ai, api-integration, pdf, narration, document-summarization]
tools: [claude, cursor, gemini, codex, antigravity]
plugin:
  setup:
    type: manual
    summary: "运行生成脚本前，先安装 Python 依赖并配置 2slides API 密钥。"
    docs: SKILL.md
---

# 2slides 演示文稿生成

## 概览

使用 2slides AI API 生成专业演示文稿。本技能支持基于内容的生成（主题驱动的 Fast PPT）、参考图风格匹配、自定义 PDF 设计、文档摘要、AI 语音旁白，以及导出页面/音频。会同时返回可交互的幻灯片链接和可下载的 PDF。

本技能改编自官方 2slides 技能仓库（[`2slides/slides-generation-2slides-skills`](https://github.com/2slides/slides-generation-2slides-skills)）。它调用 2slides 托管 API，需要用户自备 API 密钥和积分。

## 何时使用本技能

- 用户要"创建演示文稿"、"制作幻灯片"或"生成演示稿"（基于文本或大纲）。
- 用户希望幻灯片匹配参考图的风格（"按这张图的风格创建幻灯片"）。
- 用户希望无需参考图、自定义设计的 PDF 幻灯片。
- 用户上传文档，并要求"从这份文档创建幻灯片"。
- 用户要为已生成的幻灯片添加 AI 语音旁白，或将幻灯片导出为 PNG 图片、旁白导出为 WAV 音频。
- 用户问"有哪些可用主题？"或希望浏览/选择主题。

## 配置要求

用户必须拥有 2slides API 密钥和积分：

1. **获取 API 密钥：** 访问 https://2slides.com/api 创建账号和 API 密钥
   - 新用户获赠 **500 免费积分**（约 50 页 Fast PPT）
2. **购买积分（可选）：** 访问 https://2slides.com/pricing 购买更多积分
   - 按量付费，无订阅
   - 积分永不过期
   - 大套餐最高 20% 折扣
3. **设置 API 密钥：** 将密钥存到环境变量：`SLIDES_2SLIDES_API_KEY`

```bash
read -r -s SLIDES_2SLIDES_API_KEY
export SLIDES_2SLIDES_API_KEY
```

4. **安装脚本依赖：** 在本技能目录下，使用 Python 脚本前先安装锁定的本地依赖：

```bash
python -m pip install -r requirements.txt
```

**积分消耗：**
- Fast PPT：10 积分/页
- Nano Banana 1K/2K：100 积分/页
- Nano Banana 4K：200 积分/页
- 语音旁白：210 积分/页
- 下载导出：免费

详细定价信息见 [references/pricing.md](references/pricing.md)。

## 工作流决策树

根据用户请求选择合适的方式：

```
用户请求
│
├─ "根据这段内容/文本创建幻灯片"
│  └─> 使用基于内容的生成（第 1 节）
│
├─ "按这张图的风格创建幻灯片"
│  └─> 使用参考图生成（第 2 节）
│
├─ "创建自定义设计幻灯片" 或 "创建 PDF 幻灯片"
│  └─> 使用自定义 PDF 生成（第 3 节）
│
├─ "从这份文档创建幻灯片"
│  └─> 使用文档摘要（第 4 节）
│
├─ "添加语音旁白" 或 "为幻灯片生成音频"
│  └─> 使用语音旁白（第 5 节）
│
├─ "把幻灯片下载为图片" 或 "导出幻灯片和语音"
│  └─> 使用下载导出（第 6 节）
│
└─ "搜索主题" 或 "有哪些可用主题？"
   └─> 使用主题搜索（第 7 节）
```

---

## 1. 基于内容的生成

根据用户提供的文本内容生成幻灯片。

### 何时使用
- 用户在消息中直接提供内容
- 用户说"创建一个关于 X 的演示文稿"
- 用户提供结构化大纲或要点

### 工作流程

**步骤 1：准备内容**

清晰地组织内容以获得最佳效果：

```
Title: [Main Topic]

Section 1: [Subtopic]
- Key point 1
- Key point 2
- Key point 3

Section 2: [Subtopic]
- Key point 1
- Key point 2
```

**步骤 2：选择主题（必填）**

搜索合适的主题（需要 themeId）：

```bash
python scripts/search_themes.py --query "business"
python scripts/search_themes.py --query "professional"
python scripts/search_themes.py --query "creative"
```

从结果中选一个主题 ID。

**步骤 3：生成幻灯片**

使用 `generate_slides.py` 脚本和主题 ID：

```bash
# 基础生成（主题 ID 必填）
python scripts/generate_slides.py --content "Your content here" --theme-id "theme123"

# 使用其他语言
python scripts/generate_slides.py --content "Your content" --theme-id "theme123" --language "Spanish"

# 长演示稿使用异步模式
python scripts/generate_slides.py --content "Your content" --theme-id "theme123" --mode async
```

**步骤 4：处理结果**

**同步模式响应：**
```json
{
  "slideUrl": "https://2slides.com/slides/abc123",
  "pdfUrl": "https://2slides.com/slides/abc123/download",
  "status": "completed"
}
```

把两个链接都提供给用户：
- `slideUrl`：可交互的在线幻灯片
- `pdfUrl`：可下载的 PDF 版本

**异步模式响应：**
```json
{
  "jobId": "job123",
  "status": "pending"
}
```

轮询结果：
```bash
python scripts/get_job_status.py --job-id "job123"
```

---

## 2. 参考图生成

生成与参考图风格一致的幻灯片。

### 何时使用
- 用户提供图片链接并说"按这个风格创建幻灯片"
- 用户希望匹配现有的品牌/设计风格
- 用户有想要参照的模板图

### 工作流程

**步骤 1：校验图片链接**

确保参考图满足：
- 公开可访问的 URL
- 有效的图片格式（PNG、JPG 等）
- 能体现期望的幻灯片风格

**步骤 2：生成幻灯片**

使用 `generate_slides.py` 脚本和 `--reference-image` 参数：

```bash
python scripts/generate_slides.py \
  --content "Your presentation content" \
  --reference-image "https://example.com/template.jpg" \
  --language "Auto"
```

**可选参数（取值见 [2slides API](https://2slides.com/api.md)）：**
```bash
--language LANG                 # Auto, English, Spanish, Arabic, Portuguese, Indonesian,
                                 # Japanese, Russian, Hindi, French, German, Greek, Vietnamese,
                                 # Turkish, Polish, Italian, Korean, Simplified Chinese,
                                 # Traditional Chinese, Thai (default: Auto)
--mode sync|async                # default: sync for theme, async for reference-image
--aspect-ratio RATIO             # 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 (default: 16:9)
--resolution 1K|2K|4K            # default: 2K
--page N                         # 0=auto, 1-100 (default: 1)
--content-detail concise|standard # default: concise
```

**注意：** 该模式使用 Nano Banana Pro，积分消耗为：
- 1K/2K：100 积分/页
- 4K：200 积分/页

**步骤 3：处理结果**

该模式始终同步执行，返回：
```json
{
  "slideUrl": "https://2slides.com/workspace?jobId=...",
  "pdfUrl": "https://...pdf...",
  "status": "completed",
  "message": "Successfully generated N slides",
  "slidePageCount": N
}
```

把两个链接都提供给用户：
- `slideUrl`：在 2slides 工作区查看幻灯片
- `pdfUrl`：PDF 直链（1 小时后失效）

**处理时间：** 每页约 30 秒（1-2 页通常 30-60 秒）

---

## 3. 自定义 PDF 生成

无需参考图，从文本生成自定义设计的幻灯片。

### 何时使用
- 用户希望自定义设计但不提供参考图
- 用户请求"创建 PDF 幻灯片"
- 用户希望指定设计特征
- 主题生成之外、设计更灵活的替代方案

### 工作流程

**步骤 1：准备内容**

清晰地组织内容：

```
Title: [Main Topic]

Section 1: [Subtopic]
- Key point 1
- Key point 2

Section 2: [Subtopic]
- Key point 1
- Key point 2
```

**步骤 2：生成幻灯片**

使用 `create_pdf_slides.py` 脚本：

```bash
# 基础生成
python scripts/create_pdf_slides.py --content "Your content here"

# 指定设计风格（API: designStyle）
python scripts/create_pdf_slides.py \
  --content "Sales Report Q4 2025" \
  --design-style "modern minimalist, blue color scheme"

# 高分辨率 + 自动检测页数
python scripts/create_pdf_slides.py \
  --content "Marketing Plan" \
  --resolution 4K \
  --page 0 \
  --content-detail standard
```

**可选参数：**
```bash
--design-style "text"           # 设计说明（API: designStyle）
--language LANG                 # 与 generate_slides 相同（默认: Auto）
--aspect-ratio RATIO           # 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 (default: 16:9)
--resolution 1K|2K|4K          # default: 2K
--page N                        # 0=自动，1-100（默认: 1）
--content-detail concise|standard # default: standard
```

**步骤 3：处理结果**

返回结构与 create-like-this 相同：
```json
{
  "slideUrl": "https://2slides.com/workspace?jobId=...",
  "pdfUrl": "https://...pdf...",
  "status": "completed",
  "message": "Successfully generated N slides",
  "slidePageCount": N
}
```

**说明：**
- 积分消耗与 create-like-this 相同（1K/2K 100 积分/页，4K 200 积分/页）
- 处理时间：每页约 30 秒
- 自动生成 PDF
- 根据内容和规格，由 AI 创建自定义设计

---

## 4. 文档摘要

从文档内容生成幻灯片。

### 何时使用
- 用户上传文档（PDF、DOCX、TXT 等）
- 用户说"从这份文档创建幻灯片"
- 用户希望把长内容摘要成演示格式

### 工作流程

**步骤 1：读取文档**

使用合适的工具读取文档内容：
- PDF：使用 PDF 读取工具
- DOCX：使用 DOCX 读取工具
- TXT/MD：使用 Read 工具

**步骤 2：提取要点**

分析文档并提取：
- 主题和要点
- 各节的关键点
- 重要的数据、引文或示例
- 逻辑流程和结构

**步骤 3：组织内容**

把提取的信息格式化成演示结构：

```
Title: [Document Main Topic]

Introduction
- Context
- Purpose
- Overview

[Section 1 from document]
- Key point 1
- Key point 2
- Supporting detail

[Section 2 from document]
- Key point 1
- Key point 2
- Supporting detail

Conclusion
- Summary
- Key takeaways
- Next steps
```

**步骤 4：生成幻灯片**

使用基于内容的生成流程（第 1 节）。先搜索主题，再生成：

```bash
# 搜索合适的主题
python scripts/search_themes.py --query "business"

# 用主题 ID 生成
python scripts/generate_slides.py --content "[Structured content from step 3]" --theme-id "theme123"
```

**技巧：**
- 保持幻灯片简洁（每页 3-5 个要点）
- 聚焦关键洞察，而非全文
- 用文档的标题作为幻灯片标题
- 包含重要的统计数据或引文
- 询问用户是否要突出特定章节

---

## 5. 语音旁白

为幻灯片添加 AI 生成的语音旁白。

### 何时使用
- 用户希望为幻灯片添加音频
- 用户请求"添加语音旁白"或"生成音频"
- 用户希望演示包含朗读内容
- 用户需要多角色旁白

### 前置条件

**重要：** 必须先完成幻灯片生成任务，才能添加旁白。

1. 先用任意方式生成幻灯片（第 1、2、3 或 4 节）
2. 从生成结果中获取任务 ID
3. 确认任务状态为 "completed" 后再请求旁白

### 工作流程

**步骤 1：选择语音**

共 30 种语音可选，包括：
- Puck（默认）
- Aoede
- Charon
- Kore
- Fenrir
- Phoebe
- 以及其他 24 种...

列出全部语音：
```bash
python scripts/generate_narration.py --list-voices
```

**步骤 2：生成旁白**

使用 `generate_narration.py` 脚本和任务 ID：

```bash
# 默认语音基础旁白
python scripts/generate_narration.py --job-id "abc-123-def-456"

# 单人配音，指定语音
python scripts/generate_narration.py --job-id "abc-123-def-456" --voice Aoede

# 多角色模式
python scripts/generate_narration.py --job-id "abc-123-def-456" --multi-speaker
```

**参数（与 [2slides API](https://2slides.com/api.md) 对齐）：**
- `--job-id`：任务 ID（必填，Nano Banana 用 UUID）
- `--voice`：语音名称（默认: Puck）；用 `--list-voices` 查看全部 30 种
- `--language`：旁白语言（默认: Auto）
- `--multi-speaker`：启用多角色模式
- `--list-voices`：仅打印支持的语音，不调用 API

**步骤 3：检查状态**

旁白生成异步执行：

```bash
python scripts/get_job_status.py --job-id "abc-123-def-456"
```

**步骤 4：处理结果**

完成后任务将包含旁白文件。使用下载接口（第 6 节）获取音频文件。

**说明：**
- **费用：** 每页 210 积分（文本 10，音频 200）
- 处理时间因页数而异
- 共 30 种语音可选
- 支持 19 种语言加自动检测
- 多角色模式使用不同语音以增加丰富度

---

## 6. 下载导出

把幻灯片下载为 PNG 图片，把语音旁白下载为 WAV 文件。

### 何时使用
- 用户希望把幻灯片下载为图片
- 用户需要单独的语音文件
- 用户需要文字稿
- 用户需要其他工具能用的图片格式幻灯片

### 工作流程

**步骤 1：确认任务已完成**

确保幻灯片（可选旁白）已生成，且任务已完成。

**步骤 2：下载压缩包**

使用 `download_slides_pages_voices.py` 脚本：

```bash
# 用默认文件名（<job_id>.zip）下载
python scripts/download_slides_pages_voices.py --job-id "abc-123-def-456"

# 下载到指定路径
python scripts/download_slides_pages_voices.py \
  --job-id "abc-123-def-456" \
  --output "my-presentation.zip"
```

**步骤 3：解压内容**

ZIP 包内容：
- **Pages：** 每页幻灯片的 PNG 文件
- **Voices：** WAV 音频文件（如果生成了旁白）
- **Transcripts：** 旁白的文字稿

**说明：**
- **费用：** 完全免费（不消耗积分）
- 下载链接仅 **1 小时** 内有效
- 包含所有页面和语音文件
- 高质量 PNG 导出
- 音频为 WAV 格式

---

## 7. 主题搜索

为演示文稿查找合适的主题。

### 何时使用
- 生成具有特定样式的幻灯片前
- 用户问"有哪些可用主题？"
- 用户希望呈现专业或品牌化的外观

### 工作流程

**搜索主题：**

```bash
# 按风格搜索（query 必填）
python scripts/search_themes.py --query "business"
python scripts/search_themes.py --query "creative"
python scripts/search_themes.py --query "education"
python scripts/search_themes.py --query "professional"

# 获取更多结果
python scripts/search_themes.py --query "modern" --limit 50
```

**主题选择：**

1. 向用户展示可用主题的名称和描述
2. 让用户选择或使用默认
3. 在生成请求中使用主题 ID

---

## 使用 MCP 服务器

如果在 Claude Desktop 中配置了 2slides MCP 服务器，使用集成工具代替脚本。

**两种配置模式：**

1. **Streamable HTTP 协议（推荐）**
   - 最简单的配置，无需本地安装
   - 配置：`"url": "https://2slides.com/api/mcp?apikey=YOUR_API_KEY"`

2. **NPM 包（stdio）**
   - 使用本地 npm 包
   - 配置：`"command": "npx", "args": ["2slides-mcp"]`

**可用的 MCP 工具：**
- `slides_generate` - 根据内容生成幻灯片
- `slides_create_like_this` - 根据参考图生成
- `themes_search` - 搜索主题
- `jobs_get` - 查看任务状态

完整配置说明和详细工具文档见 [mcp-integration.md](references/mcp-integration.md)。

**何时使用 MCP，何时使用脚本：**
- 在 Claude Desktop 中配置后，**使用 MCP**
- 在 Claude Code CLI 或 MCP 不可用时，**使用脚本**

---

## 高级特性

### 同步与异步模式

**同步模式（默认）：**
- 等待生成完成（30-60 秒）
- 立即返回结果
- 适合快速演示

**异步模式：**
- 立即返回任务 ID
- 用 `get_job_status.py` 轮询结果
- 适合大型演示或批处理
- **推荐轮询：** 每 20-30 秒一次，避免给服务器造成压力

### 速率限制

不同接口有不同的速率限制：

- **Fast PPT（generate）：** 每分钟 10 次
- **Nano Banana（create-like-this、create-pdf-slides）：** 每分钟 6 次

如遇限流，等待后重试或查看套餐限额。

### 积分消耗

- **Fast PPT（generate 接口）：** 10 积分/页
- **Nano Banana 1K/2K（create-like-this、create-pdf-slides）：** 100 积分/页
- **Nano Banana 4K：** 200 积分/页
- **语音旁白：** 210 积分/页（文本 10，音频 200）
- **下载导出：** 免费（不消耗积分）

### 购买积分

2slides 采用按量付费的积分制，无需订阅。

**积分套餐：** （当前优惠：最高 20% 折扣）
- 2,000 积分：$5.00
- 4,000 积分：$9.50（95 折）
- 10,000 积分：$22.50（9 折）
- 20,000 积分：$42.50（85 折）
- 40,000 积分：$80.00（8 折）

**新用户获赠 500 免费积分** 作为入门（约 50 页 Fast PPT）。

**积分永不过期** —— 按自己的节奏使用。

**购买地址：** https://2slides.com/pricing

### 下载链接有效期

所有下载链接（PDF、ZIP 包）仅 **1 小时** 内有效。请在生成后及时下载。

### 语言支持

支持多语言生成（使用完整的语言名）：

```bash
--language "Auto"                # 自动检测（默认）
--language "English"             # English
--language "Simplified Chinese"  # 简体中文
--language "Traditional Chinese" # 繁體中文
--language "Spanish"             # Español
--language "French"              # Français
--language "German"              # Deutsch
--language "Japanese"            # 日本語
--language "Korean"              # 한국어
```

更多语言：Arabic、Portuguese、Indonesian、Russian、Hindi、Vietnamese、Turkish、Polish、Italian

### 错误处理

**常见错误码：**

1. **缺少 API 密钥**
   ```
   Error: API key not found
   Solution: Set SLIDES_2SLIDES_API_KEY environment variable
   ```

2. **RATE_LIMIT_EXCEEDED（超出速率限制）**
   ```
   Error: 429 Too Many Requests
   Solution: Wait 20-30 seconds before retrying
   Rate limits: Fast PPT (10/min), Nano Banana (6/min)
   ```

3. **INSUFFICIENT_CREDITS（积分不足）**
   ```
   Error: Not enough credits
   Solution: Add credits at https://2slides.com/api
   ```

4. **INVALID_JOB_ID（无效任务 ID）**
   ```
   Error: Job ID not found or invalid
   Solution: Verify job ID format (must be UUID for Nano Banana)
   ```

5. **无效内容**
   ```
   Error: 400 Bad Request
   Solution: Verify content format and parameters
   ```

---

## 脚本参数参考（2slides API）

所有脚本接收的参数与 [2slides API](https://2slides.com/api.md) 一致。允许值在 `scripts/api_constants.py` 中定义，并在适用处强制执行。

| 脚本 | 关键参数 | 允许值（见脚本 `--help` 或 api_constants.py） |
|--------|----------------|----------------------------------------------------------|
| `generate_slides.py` | `--language` | Auto, English, Spanish, Arabic, Portuguese, Indonesian, Japanese, Russian, Hindi, French, German, Greek, Vietnamese, Turkish, Polish, Italian, Korean, Simplified Chinese, Traditional Chinese, Thai |
| | `--mode` | sync, async |
| | `--aspect-ratio` | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| | `--resolution` | 1K, 2K, 4K |
| | `--content-detail` | concise, standard |
| `create_pdf_slides.py` | 同上 + `--design-style` / `--design-spec`（自由文本） | |
| `generate_narration.py` | `--voice` | 30 种语音（Puck, Aoede, Charon, …）；用 `--list-voices` |
| | `--language` | Auto, English, Spanish, Arabic, Portuguese, Indonesian, Japanese, Russian, Hindi, French, German, Vietnamese, Turkish, Polish, Italian, Korean, Simplified Chinese, Traditional Chinese |
| | `--multi-speaker` | 出现时启用 |
| `search_themes.py` | `--query`（必填）、`--limit`（1–100） | |
| `get_job_status.py` | `--job-id`（必填） | |
| `download_slides_pages_voices.py` | `--job-id`（必填）、`--output`（路径） | |

---

## 补充文档

### API 参考
见 [api-reference.md](references/api-reference.md)：
- 所有接口和参数
- 请求/响应格式
- 认证详情
- 速率限制和最佳实践
- 错误码和处理

### 定价信息
见 [pricing.md](references/pricing.md)：
- 积分套餐和定价
- 费用示例和计算
- 免费试用详情
- 退款政策
- 企业版选项

---

## 最佳实践提示

**内容结构：**
- 使用清晰的标题和副标题
- 保持要点简洁
- 每个章节控制在 3-5 个要点
- 包含相关示例或数据

**主题选择：**
- 标准生成需要主题 ID
- 用与演示目的匹配的关键词搜索
- 常用搜索词："business"、"professional"、"creative"、"education"、"modern"
- 每个主题都有独特的样式和布局

**参考图：**
- 使用高质量图片以获得最佳效果
- 可使用 URL 或 base64 编码图片
- 公开 URL 必须可访问
- 根据质量需求选择分辨率（1K/2K/4K）
- 使用 page=0 自动检测页数

**文档处理：**
- 只提取关键信息
- 不要试图把整篇文档塞进幻灯片
- 聚焦主要洞察和要点
- 询问用户希望突出哪些章节

---

## 安全说明

- **凭证：** 本技能从环境变量 `SLIDES_2SLIDES_API_KEY` 读取 API 密钥。切勿将密钥硬编码到命令中、提交到代码库或回显给用户。脚本仅通过 HTTPS 把密钥作为 bearer/`apikey` 值发送到 `https://2slides.com`。
- **网络与付费变更：** 每次生成调用都会向 2slides API 发起网络请求，并 **消耗用户积分**（根据模式不同，每页 10–210 积分）。把生成、参考图、自定义 PDF、旁白调用视为付费操作 —— 生成大型或高分辨率（4K）演示前先确认意图，并在费用/规模较大时提示预期页数和费用。
- **无破坏性本地操作：** 脚本只读取用户指定的内容/文件，并把生成产物（例如下载的 ZIP）写入用户指定的路径。不会修改或删除无关文件。
- **输入处理：** 参考图和文档输入会被发送到 2slides 服务进行处理。未经用户授权，请勿提交保密材料给第三方处理。
- **下载链接 1 小时后失效** —— 及时获取产物，不要把链接当作持久存储。

## 局限性

- 需要有效的 2slides 账号、API 密钥和充足积分；本技能不提供或支付积分。
- 输出是 AI 生成的草稿，作为起点使用，不是经过事实核查的最终成品 —— 使用前请审阅内容。
- 本技能不能替代特定环境的验证或专家审查。如果缺少 API 密钥、必需输入或预期费用/规模，先停下来询问清楚。
- 存在速率限制（Fast PPT 10/分钟，Nano Banana 6/分钟）；轮询异步任务时每 20–30 秒一次，不要紧密循环。

## 相关技能

- `@youtube-full` — 获取可由本技能摘要为演示稿的源材料（转录文本）。