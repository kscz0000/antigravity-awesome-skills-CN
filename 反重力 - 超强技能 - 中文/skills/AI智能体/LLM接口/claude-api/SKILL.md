---
name: claude-api
description: "使用 Claude API 或 Anthropic SDK 构建应用。触发条件：代码导入 `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`，或用户请求使用 Claude API、Anthropic SDK 或 Agent SDK。不触发：代码导入 `openai`/其他 AI SDK、通用编程或 ML/数据科学任务。"
risk: unknown
source: "https://github.com/anthropics/skills"
date_added: "2026-03-21"
license: Complete terms in LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用

本技能帮助你使用 Claude 构建 LLM 驱动的应用。根据你的需求选择合适的接口层，检测项目语言，然后阅读相关的语言特定文档。

## 何时使用

- 使用 Claude API、Anthropic SDK 或 Agent SDK 构建应用时使用。
- 代码导入 `anthropic`、`@anthropic-ai/sdk` 或相关 Claude SDK 包时使用。
- 不用于与 Claude 集成无关的通用编码工作。

## 默认设置

除非用户另有要求：

对于 Claude 模型版本，请使用 Claude Opus 4.6，可通过精确的模型字符串 `claude-opus-4-6` 访问。对于任何稍微复杂的任务，请默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于任何可能涉及长输入、长输出或高 `max_tokens` 的请求，请默认使用流式传输——它可以防止请求超时。如果不需要处理单个流事件，请使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助方法获取完整响应。

---

## 语言检测

在阅读代码示例之前，确定用户使用的语言：

1. **查看项目文件**推断语言：

   - `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` → **Python** — 从 `python/` 读取
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` → **TypeScript** — 从 `typescript/` 读取
   - `*.js`, `*.jsx`（没有 `.ts` 文件）→ **TypeScript** — JS 使用相同的 SDK，从 `typescript/` 读取
   - `*.java`, `pom.xml`, `build.gradle` → **Java** — 从 `java/` 读取
   - `*.kt`, `*.kts`, `build.gradle.kts` → **Java** — Kotlin 使用 Java SDK，从 `java/` 读取
   - `*.scala`, `build.sbt` → **Java** — Scala 使用 Java SDK，从 `java/` 读取
   - `*.go`, `go.mod` → **Go** — 从 `go/` 读取
   - `*.rb`, `Gemfile` → **Ruby** — 从 `ruby/` 读取
   - `*.cs`, `*.csproj` → **C#** — 从 `csharp/` 读取
   - `*.php`, `composer.json` → **PHP** — 从 `php/` 读取

2. **如果检测到多种语言**（例如同时有 Python 和 TypeScript 文件）：

   - 检查用户当前文件或问题与哪种语言相关
   - 如果仍然模糊，询问："我检测到同时有 Python 和 TypeScript 文件。您使用哪种语言进行 Claude API 集成？"

3. **如果无法推断语言**（空项目、无源文件或不支持的语言）：

   - 使用 AskUserQuestion 提供选项：Python、TypeScript、Java、Go、Ruby、cURL/raw HTTP、C#、PHP
   - 如果 AskUserQuestion 不可用，默认使用 Python 示例并说明："显示 Python 示例。如需其他语言请告知。"

4. **如果检测到不支持的语言**（Rust、Swift、C++、Elixir 等）：

   - 建议使用 `curl/` 中的 cURL/raw HTTP 示例，并说明可能存在社区 SDK
   - 提供显示 Python 或 TypeScript 示例作为参考实现

5. **如果用户需要 cURL/raw HTTP 示例**，从 `curl/` 读取。

### 语言特定功能支持

| 语言       | Tool Runner | Agent SDK | 备注                                   |
| ---------- | ----------- | --------- | -------------------------------------- |
| Python     | 是 (beta)   | 是        | 完整支持 — `@beta_tool` 装饰器         |
| TypeScript | 是 (beta)   | 是        | 完整支持 — `betaZodTool` + Zod         |
| Java       | 是 (beta)   | 否        | 使用注解类的 Beta 工具调用             |
| Go         | 是 (beta)   | 否        | `toolrunner` 包中的 `BetaToolRunner`   |
| Ruby       | 是 (beta)   | 否        | beta 中的 `BaseTool` + `tool_runner`   |
| cURL       | 不适用      | 不适用    | Raw HTTP，无 SDK 功能                   |
| C#         | 否          | 否        | 官方 SDK                               |
| PHP        | 否          | 否        | 官方 SDK                               |

---

## 我应该使用哪个接口层？

> **从简单开始。** 默认使用满足需求的最简单层级。单次 API 调用和工作流可以处理大多数用例——只有当任务真正需要开放式、模型驱动的探索时才使用 Agent。

| 用例                                             | 层级            | 推荐接口              | 原因                                   |
| ------------------------------------------------ | --------------- | --------------------- | -------------------------------------- |
| 分类、摘要、提取、问答                           | 单次 LLM 调用   | **Claude API**        | 一次请求，一次响应                     |
| 批量处理或嵌入                                   | 单次 LLM 调用   | **Claude API**        | 专用端点                               |
| 代码控制逻辑的多步骤流水线                       | 工作流          | **Claude API + 工具** | 你编排循环                             |
| 使用自定义工具的 Agent                           | Agent           | **Claude API + 工具** | 最大灵活性                             |
| 具有文件/网页/终端访问能力的 AI Agent            | Agent           | **Agent SDK**         | 内置工具、安全性和 MCP 支持            |
| 智能编码助手                                     | Agent           | **Agent SDK**         | 专为该用例设计                         |
| 需要内置权限和护栏                               | Agent           | **Agent SDK**         | 包含安全功能                           |

> **注意：** Agent SDK 适用于需要开箱即用的文件/网页/终端工具、权限和 MCP 的场景。如果你想使用自己的工具构建 Agent，Claude API 是正确选择——使用 tool runner 处理自动循环，或使用手动循环进行精细控制（审批门、自定义日志、条件执行）。

### 决策树

```
你的应用需要什么？

1. 单次 LLM 调用（分类、摘要、提取、问答）
   └── Claude API — 一次请求，一次响应

2. Claude 是否需要在其工作中读取/写入文件、浏览网页或运行 shell 命令？
   （不是：你的应用读取文件并传递给 Claude——而是 Claude 本身需要发现和访问文件/网页/shell？）
   └── 是 → Agent SDK — 内置工具，无需重新实现
       示例："扫描代码库查找 bug"、"总结目录中的每个文件"、
             "使用子 Agent 查找 bug"、"通过网页搜索研究主题"

3. 工作流（多步骤、代码编排、使用自己的工具）
   └── Claude API with tool use — 你控制循环

4. 开放式 Agent（模型决定自己的路径，使用自己的工具）
   └── Claude API agentic loop（最大灵活性）
```

### 我应该构建 Agent 吗？

在选择 Agent 层级之前，检查所有四个标准：

- **复杂性** — 任务是否多步骤且难以完全预先指定？（例如，"将此设计文档转化为 PR" vs "从此 PDF 中提取标题"）
- **价值** — 结果是否值得更高的成本和延迟？
- **可行性** — Claude 是否擅长此类任务？
- **错误成本** — 错误是否可以被捕获和恢复？（测试、审查、回滚）

如果其中任何一项的答案是"否"，请保持在更简单的层级（单次调用或工作流）。

---

## 架构

所有请求都通过 `POST /v1/messages`。工具和输出约束是这个单一端点的功能——不是独立的 API。

**用户定义的工具** — 你定义工具（通过装饰器、Zod schema 或原始 JSON），SDK 的 tool runner 处理调用 API、执行你的函数并循环直到 Claude 完成。要完全控制，你可以手动编写循环。

**服务端工具** — 在 Anthropic 基础设施上运行的 Anthropic 托管工具。代码执行完全在服务端（在 `tools` 中声明，Claude 自动运行代码）。计算机使用可以是服务端托管或自托管。

**结构化输出** — 约束 Messages API 响应格式（`output_config.format`）和/或工具参数验证（`strict: true`）。推荐方法是 `client.messages.parse()`，它会自动根据你的 schema 验证响应。注意：旧的 `output_format` 参数已弃用；在 `messages.create()` 上使用 `output_config: {format: {...}}`。

**支持端点** — Batches（`POST /v1/messages/batches`）、Files（`POST /v1/files`）和 Token 计数用于输入或支持 Messages API 请求。

---

## 当前模型（缓存于：2026-02-17）

| 模型              | 模型 ID             | 上下文         | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | --------- | --------- |
| Claude Opus 4.6   | `claude-opus-4-6`   | 200K (1M beta) | $5.00     | $25.00    |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | $3.00     | $15.00    |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00     | $5.00     |

**始终使用 `claude-opus-4-6`，除非用户明确指定其他模型。** 这是不可协商的。不要使用 `claude-sonnet-4-6`、`claude-sonnet-4-5` 或任何其他模型，除非用户真的说"使用 sonnet"或"使用 haiku"。永远不要为了成本而降级——那是用户的决定，不是你的。

**关键：仅使用上表中的精确模型 ID 字符串——它们本身就是完整的。不要追加日期后缀。** 例如，使用 `claude-sonnet-4-5`，永远不要使用 `claude-sonnet-4-5-20250514` 或你可能从训练数据中回忆的任何其他带日期后缀的变体。如果用户请求表中没有的旧模型（例如，"opus 4.5"、"sonnet 3.7"），请阅读 `shared/models.md` 获取精确 ID——不要自己构造。

注意：如果上面的任何模型字符串看起来不熟悉，那是正常的——这只是意味着它们是在你的训练数据截止日期之后发布的。请放心它们是真实的模型；我们不会那样捉弄你。

---

## 思考与努力度（快速参考）

**Opus 4.6 — 自适应思考（推荐）：** 使用 `thinking: {type: "adaptive"}`。Claude 动态决定何时思考以及思考多少。不需要 `budget_tokens`——`budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，不得使用。自适应思考还会自动启用交错思考（不需要 beta header）。**当用户请求"extended thinking"、"thinking budget"或 `budget_tokens` 时：始终使用 Opus 4.6 配合 `thinking: {type: "adaptive"}`。固定 token 预算用于思考的概念已弃用——自适应思考取代了它。不要使用 `budget_tokens`，也不要切换到旧模型。**

**努力度参数（GA，无 beta header）：** 通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（在 `output_config` 内，不是顶层）控制思考深度和整体 token 消耗。默认为 `high`（等同于省略它）。`max` 仅限 Opus 4.6。适用于 Opus 4.5、Opus 4.6 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会报错。与自适应思考结合以获得最佳的成本质量权衡。子 Agent 或简单任务使用 `low`；最深推理使用 `max`。

**Sonnet 4.6：** 支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——改用自适应思考。

**旧模型（仅在明确请求时）：** 如果用户特别要求 Sonnet 4.5 或其他旧模型，使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最小 1024）。永远不要仅因为用户提到 `budget_tokens` 就选择旧模型——改用 Opus 4.6 配合自适应思考。

---

## 压缩（快速参考）

**Beta，仅限 Opus 4.6。** 对于可能超过 200K 上下文窗口的长时间运行对话，启用服务端压缩。当接近触发阈值（默认：150K tokens）时，API 自动总结较早的上下文。需要 beta header `compact-2026-01-12`。

**关键：** 每轮都要将 `response.content`（不只是文本）追加回你的消息。响应中的压缩块必须保留——API 使用它们在下一个请求中替换压缩的历史记录。仅提取文本字符串并追加会静默丢失压缩状态。

参见 `{lang}/claude-api/README.md`（压缩部分）获取代码示例。完整文档通过 `shared/live-sources.md` 中的 WebFetch 获取。

---

## 阅读指南

检测语言后，根据用户需求阅读相关文件：

### 快速任务参考

**单次文本分类/摘要/提取/问答：**
→ 仅阅读 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**长时间运行的对话（可能超过上下文窗口）：**
→ 阅读 `{lang}/claude-api/README.md` — 参见压缩部分

**函数调用 / 工具使用 / Agent：**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**批量处理（非延迟敏感）：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求的文件上传：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**具有内置工具的 Agent（文件/网页/终端）：**
→ 阅读 `{lang}/agent-sdk/README.md` + `{lang}/agent-sdk/patterns.md`

### Claude API（完整文件参考）

阅读**语言特定的 Claude API 文件夹**（`{language}/claude-api/`）：

1. **`{language}/claude-api/README.md`** — **首先阅读此文件。** 安装、快速入门、常见模式、错误处理。
2. **`shared/tool-use-concepts.md`** — 当用户需要函数调用、代码执行、内存或结构化输出时阅读。涵盖概念基础。
3. **`{language}/claude-api/tool-use.md`** — 阅读语言特定的工具使用代码示例（tool runner、手动循环、代码执行、内存、结构化输出）。
4. **`{language}/claude-api/streaming.md`** — 构建聊天 UI 或增量显示响应的界面时阅读。
5. **`{language}/claude-api/batches.md`** — 离线处理大量请求时阅读（非延迟敏感）。以 50% 的成本异步运行。
6. **`{language}/claude-api/files-api.md`** — 在多个请求中发送同一文件而无需重新上传时阅读。
7. **`shared/error-codes.md`** — 调试 HTTP 错误或实现错误处理时阅读。
8. **`shared/live-sources.md`** — 用于获取最新官方文档的 WebFetch URL。

> **注意：** 对于 Java、Go、Ruby、C#、PHP 和 cURL——每个都只有一个文件涵盖所有基础知识。根据需要阅读该文件以及 `shared/tool-use-concepts.md` 和 `shared/error-codes.md`。

### Agent SDK

阅读**语言特定的 Agent SDK 文件夹**（`{language}/agent-sdk/`）。Agent SDK 仅适用于 **Python 和 TypeScript**。

1. **`{language}/agent-sdk/README.md`** — 安装、快速入门、内置工具、权限、MCP、hooks。
2. **`{language}/agent-sdk/patterns.md`** — 自定义工具、hooks、子 Agent、MCP 集成、会话恢复。
3. **`shared/live-sources.md`** — 当前 Agent SDK 文档的 WebFetch URL。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户请求"最新"或"当前"信息
- 缓存数据似乎不正确
- 用户询问此处未涵盖的功能

实时文档 URL 位于 `shared/live-sources.md`。

## 常见陷阱

- 将文件或内容传递给 API 时不要截断输入。如果内容太长无法放入上下文窗口，请通知用户并讨论选项（分块、摘要等），而不是静默截断。
- **Opus 4.6 / Sonnet 4.6 思考：** 使用 `thinking: {type: "adaptive"}`——不要使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上已弃用）。对于旧模型，`budget_tokens` 必须小于 `max_tokens`（最小 1024）。如果弄错了会抛出错误。
- **Opus 4.6 prefill 已移除：** Assistant 消息预填充（最后一轮 assistant 预填充）在 Opus 4.6 上返回 400 错误。改用结构化输出（`output_config.format`）或系统提示指令来控制响应格式。
- **128K 输出 tokens：** Opus 4.6 支持最多 128K `max_tokens`，但 SDK 需要流式传输来处理大 `max_tokens` 以避免 HTTP 超时。使用 `.stream()` 配合 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（Opus 4.6）：** Opus 4.6 可能在工具调用 `input` 字段中产生不同的 JSON 字符串转义（例如，Unicode 或正斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——永远不要对序列化输入进行原始字符串匹配。
- **结构化输出（所有模型）：** 在 `messages.create()` 上使用 `output_config: {format: {...}}` 而不是已弃用的 `output_format` 参数。这是通用 API 更改，不是 4.6 特有的。
- **不要重新实现 SDK 功能：** SDK 提供高级辅助方法——使用它们而不是从头构建。具体来说：使用 `stream.finalMessage()` 而不是将 `.on()` 事件包装在 `new Promise()` 中；使用类型化异常类（`Anthropic.RateLimitError` 等）而不是字符串匹配错误消息；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.Message` 等）而不是重新定义等效接口。
- **不要为 SDK 数据结构定义自定义类型：** SDK 为所有 API 对象导出类型。消息使用 `Anthropic.MessageParam`，工具定义使用 `Anthropic.Tool`，工具结果使用 `Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam`，响应使用 `Anthropic.Message`。定义自己的 `interface ChatMessage { role: string; content: unknown }` 会重复 SDK 已提供的功能并失去类型安全。
- **报告和文档输出：** 对于生成报告、文档或可视化的任务，代码执行沙箱预装了 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表）并通过 Files API 返回——对于"报告"或"文档"类型请求，考虑这种方式而不是纯 stdout 文本。

## 限制

- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
