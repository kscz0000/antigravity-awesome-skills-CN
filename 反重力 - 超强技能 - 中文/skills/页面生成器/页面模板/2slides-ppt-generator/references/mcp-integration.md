# MCP 集成指南

2slides 提供 MCP（Model Context Protocol）服务器，可与 Claude Desktop 和其他兼容 MCP 的 AI 智能体无缝集成。

## MCP 服务器是什么？

2slides MCP 服务器把直接 API 调用所具备的相同 API 功能，通过标准化的工具接口暴露出来，Claude 可直接使用，无需执行脚本。

**可用工具：**
1. `slides_generate` - 根据内容生成幻灯片
2. `slides_create_like_this` - 根据参考图生成幻灯片
3. `slides_create_pdf_slides` - 生成自定义设计幻灯片（新）
4. `slides_generate_narration` - 添加 AI 语音旁白（新）
5. `slides_download_pages_voices` - 把幻灯片和语音导出为 ZIP（新）
6. `themes_search` - 搜索可用主题
7. `jobs_get` - 查看任务状态

**注意：** 新工具（3-5）可能需要把 MCP 服务器升级到最新版。

## 安装与配置

2slides MCP 服务器支持两种集成模式：

### 模式 1：Streamable HTTP 协议（推荐）

使用 HTTP 接口的最简配置，无需本地安装。

**步骤 1：** 在 https://2slides.com/api 获取 API 密钥

**步骤 2：** 配置 Claude Desktop

编辑：`~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）

```json
{
  "mcpServers": {
    "2slides": {
      "url": "https://2slides.com/api/mcp?apikey=YOUR_2SLIDES_API_KEY"
    }
  }
}
```

**步骤 3：** 完全重启 Claude Desktop

**优点：**
- ✅ 无需 Node.js 或 npm
- ✅ 始终使用最新版
- ✅ 配置更快
- ✅ 无本地依赖

---

### 模式 2：NPM 包（stdio）

使用本地 npm 包作为 MCP 服务器。

**步骤 1：** 在 https://2slides.com/api 获取 API 密钥

**步骤 2：** 配置 Claude Desktop

编辑：`~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）

```json
{
  "mcpServers": {
    "2slides": {
      "command": "npx",
      "args": ["2slides-mcp"],
      "env": {
        "API_KEY": "YOUR_2SLIDES_API_KEY"
      }
    }
  }
}
```

**步骤 3：** 完全重启 Claude Desktop

**要求：**
- 已安装 Node.js 和 npm
- 首次下载包时需要联网

---

### 验证安装

重启后，2slides 工具应可用。通过以下请求测试：
"用 2slides 搜索商务主题"

## 何时使用 MCP，何时使用直接 API

### 适合用 MCP 服务器：
- 在 Claude Desktop 或其他兼容 MCP 的环境中工作
- 希望工具集成顺畅，不需管理脚本
- 希望 Claude 直接处理 API 调用
- 需要实时交互和反馈

### 适合用直接 API 脚本：
- 在 Claude Code CLI 中工作
- 未配置或不可用 MCP 服务器
- 需要更细粒度的参数控制和错误处理
- 集成到自定义工作流或自动化中
- 需要批处理多个请求

## MCP 工具详情

### slides_generate

根据用户内容生成幻灯片。

**参数：**
- `userInput`（string，必填）：要转换的内容
- `themeId`（string，必填）：来自 themes_search 的主题 ID
- `responseLanguage`（string，可选，默认 "Auto"）：语言名称
- `mode`（string，可选，默认 "sync"）："sync" 或 "async"

**示例：**
```
先搜索主题：
使用 themes_search：
- query: "business"

然后用主题 ID 生成：
使用 slides_generate：
- userInput: "Introduction to Python: Variables, Functions, Classes"
- themeId: "theme_abc123"
- mode: "sync"
```

### slides_create_like_this

生成与参考图风格一致的幻灯片。

**参数：**
- `userInput`（string，必填）：幻灯片内容
- `referenceImageUrl`（string，必填）：参考图的 URL 或 base64
- `responseLanguage`（string，可选，默认 "Auto"）：语言名称
- `aspectRatio`（string，可选，默认 "16:9"）：宽:高 格式
- `resolution`（string，可选，默认 "2K"）："1K"、"2K" 或 "4K"
- `page`（number，可选，默认 1）：幻灯片数（0 表示自动检测，最多 100）
- `contentDetail`（string，可选，默认 "concise"）："concise" 或 "standard"

**示例：**
```
使用 slides_create_like_this：
- userInput: "Sales Report Q4 2025"
- referenceImageUrl: "https://example.com/template.jpg"
- resolution: "2K"
- page: 0  # 自动检测页数
- contentDetail: "standard"
```

### themes_search

搜索可用主题。

**参数：**
- `query`（string，必填）：搜索关键词
- `limit`（number，可选，默认 20，最多 100）：最大结果数

**示例：**
```
使用 themes_search：
- query: "business"
- limit: 10
```

**注意：** query 参数为必填。使用 "business"、"professional"、"creative"、"education"、"modern" 等关键词搜索合适的主题。

### slides_create_pdf_slides

无需参考图，从文本生成自定义设计幻灯片。

**参数：**
- `userInput`（string，必填）：幻灯片内容
- `responseLanguage`（string，可选，默认 "Auto"）：语言名称
- `aspectRatio`（string，可选，默认 "16:9"）：宽:高 格式
- `resolution`（string，可选，默认 "2K"）："1K"、"2K" 或 "4K"
- `page`（number，可选，默认 1）：幻灯片数（0 表示自动检测，最多 100）
- `contentDetail`（string，可选，默认 "concise"）："concise" 或 "standard"
- `designSpec`（string，可选）：设计规格

**示例：**
```
使用 slides_create_pdf_slides：
- userInput: "Sales Report Q4 2025"
- designSpec: "modern minimalist, blue color scheme"
- resolution: "2K"
- page: 0  # 自动检测页数
```

### slides_generate_narration

为已完成的幻灯片添加 AI 语音旁白。

**参数：**
- `jobId`（string，必填）：来自幻灯片生成的任务 ID（UUID 格式）
- `language`（string，可选，默认 "Auto"）：旁白语言
- `voice`（string，可选，默认 "Puck"）：语音名称（30 种可选）
- `multiSpeaker`（boolean，可选，默认 false）：启用多角色模式

**可用语音：**
Puck, Aoede, Charon, Kore, Fenrir, Phoebe, Asteria, Luna, Stella, Theia, Helios, Atlas, Clio, Melpomene, Calliope, Erato, Euterpe, Polyhymnia, Terpsichore, Thalia, Urania, Zeus, Hera, Poseidon, Athena, Apollo, Artemis, Ares, Aphrodite, Hephaestus

**示例：**
```
使用 slides_generate_narration：
- jobId: "abc-123-def-456"
- voice: "Aoede"
- multiSpeaker: true
- language: "English"
```

**注意：** 任务必须完成后才能添加旁白。费用：每页 210 积分。

### slides_download_pages_voices

把幻灯片下载为 PNG 图片，语音文件下载为 WAV，打包为 ZIP。

**参数：**
- `jobId`（string，必填）：来自幻灯片生成的任务 ID

**示例：**
```
使用 slides_download_pages_voices：
- jobId: "abc-123-def-456"
```

**注意：** 完全免费（不消耗积分）。下载链接仅 1 小时内有效。

### jobs_get

查询异步任务的状态。

**参数：**
- `jobId`（string，必填）：来自异步生成的任务 ID

**响应包含：**
- 幻灯片生成状态
- 旁白状态（如适用）
- 下载链接（完成后）

**示例：**
```
使用 jobs_get：
- jobId: "abc123..."
```

## 故障排查

### 工具未出现

1. 确认配置文件 JSON 语法正确
2. HTTP 模式下：检查 URL 中的 API 密钥是否正确
3. npm 模式下：确认 API 密钥正确设置在 `env` 部分
4. 完全重启 Claude Desktop（彻底退出，不是仅关闭窗口）
5. 检查 Claude Desktop 控制台中的错误消息

### API 密钥问题

- 在 https://2slides.com/api 确认 API 密钥处于激活状态
- 检查配置中是否有拼写错误
- 确认密钥两侧没有多余的引号或空格
- HTTP 模式下：API 密钥必须放在 URL 的查询参数中

### HTTP 模式问题

- 确认 URL 格式：`https://2slides.com/api/mcp?apikey=YOUR_KEY`
- 检查网络连接
- 确认 API 密钥没有需要 URL 编码的特殊字符

### NPM 模式问题

- 确认 `npx` 可用（需要 Node.js）
- 尝试手动运行 `npx 2slides-mcp` 检查错误
- 确认联网正常以便下载包
- 检查 Node.js 版本兼容性

## GitHub 仓库

更多信息请访问：https://github.com/2slides/mcp-2slides