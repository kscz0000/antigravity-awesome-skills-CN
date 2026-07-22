# 工具使用概念

本文件介绍 Claude API 工具使用的概念基础。有关特定语言的代码示例，请参阅 `python/`、`typescript/` 或其他语言文件夹。

## 用户定义工具

### 工具定义结构

> **注意：** 使用 Tool Runner（beta）时，工具 schema 会从函数签名（Python）、Zod schema（TypeScript）、注解类（Java）、`jsonschema` 结构体标签（Go）或 `BaseTool` 子类（Ruby）自动生成。下面的原始 JSON schema 格式适用于手动方法或不支持 tool runner 的 SDK。

每个工具都需要名称、描述和输入的 JSON Schema：

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City and state, e.g., San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Temperature unit"
      }
    },
    "required": ["location"]
  }
}
```

**工具定义最佳实践：**

- 使用清晰、描述性的名称（例如 `get_weather`、`search_database`、`send_email`）
- 编写详细的描述 — Claude 使用这些来决定何时使用工具
- 为每个属性包含描述
- 对具有固定值集合的参数使用 `enum`
- 在 `required` 中标记真正必需的参数；其他参数设为可选并提供默认值

---

### 工具选择选项

控制 Claude 何时使用工具：

| Value                             | Behavior                                      |
| --------------------------------- | --------------------------------------------- |
| `{"type": "auto"}`                | Claude 决定是否使用工具（默认）               |
| `{"type": "any"}`                 | Claude 必须使用至少一个工具                   |
| `{"type": "tool", "name": "..."}` | Claude 必须使用指定工具                       |
| `{"type": "none"}`                | Claude 不能使用工具                           |

任何 `tool_choice` 值也可以包含 `"disable_parallel_tool_use": true` 以强制 Claude 在每次响应中最多使用一个工具。默认情况下，Claude 可能在单个响应中请求多个工具调用。

---

### Tool Runner 与手动循环

**Tool Runner（推荐）：** SDK 的 tool runner 自动处理 Agent 循环 — 它调用 API、检测工具使用请求、执行你的工具函数、将结果反馈给 Claude，并重复直到 Claude 停止调用工具。在 Python、TypeScript、Java、Go 和 Ruby SDK 中可用（beta）。Python SDK 还提供 MCP 转换辅助工具（`anthropic.lib.tools.mcp`）将 MCP 工具、提示词和资源转换为 tool runner 可用的格式 — 详情请参阅 `python/claude-api/tool-use.md`。

**手动 Agent 循环：** 当你需要对循环进行精细控制时使用（例如自定义日志记录、条件工具执行、人工审批）。循环直到 `stop_reason == "end_turn"`，始终追加完整的 `response.content` 以保留 tool_use 块，并确保每个 `tool_result` 包含匹配的 `tool_use_id`。

**服务端工具的停止原因：** 使用服务端工具（代码执行、网络搜索等）时，API 运行服务端采样循环。如果此循环达到默认限制 10 次迭代，响应将具有 `stop_reason: "pause_turn"`。要继续，重新发送用户消息和助手响应并发出另一个 API 请求 — 服务端将从停止处恢复。不要添加额外的用户消息如"继续" — API 会检测到末尾的 `server_tool_use` 块并知道自动恢复。

```python
# 在 Agent 循环中处理 pause_turn
if response.stop_reason == "pause_turn":
    messages = [
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": response.content},
    ]
    # 发出另一个 API 请求 — 服务端自动恢复
    response = client.messages.create(
        model="claude-opus-4-6", messages=messages, tools=tools
    )
```

设置 `max_continuations` 限制（例如 5）以防止无限循环。完整指南请参阅：`https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons`

> **安全：** Tool runner 会在 Claude 请求时自动执行你的工具函数。对于有副作用的工具（发送邮件、修改数据库、金融交易），请在工具函数内验证输入，并考虑对破坏性操作要求确认。如果需要在每次工具执行前进行人工审批，请使用手动 Agent 循环。

---

### 处理工具结果

当 Claude 使用工具时，响应包含 `tool_use` 块。你必须：

1. 使用提供的输入执行工具
2. 在 `tool_result` 消息中发送结果
3. 继续对话

**工具结果中的错误处理：** 当工具执行失败时，设置 `"is_error": true` 并提供信息丰富的错误消息。Claude 通常会确认错误并尝试不同的方法或请求澄清。

**多个工具调用：** Claude 可能在单个响应中请求多个工具。在继续之前处理所有工具 — 在单个 `user` 消息中发送所有结果。

---

## 服务端工具：代码执行

代码执行工具让 Claude 在安全的沙箱容器中运行代码。与用户定义工具不同，服务端工具在 Anthropic 的基础设施上运行 — 你不需要在客户端执行任何操作。只需包含工具定义，Claude 会处理其余工作。

### 关键事实

- 在隔离容器中运行（1 CPU、5 GiB RAM、5 GiB 磁盘）
- 无网络访问（完全沙箱化）
- Python 3.11，预装数据科学库
- 容器保留 30 天，可在请求间重用
- 与网络搜索/网络获取工具一起使用时免费；否则每月 1,550 小时免费额度后 $0.05/小时

### 工具定义

该工具不需要 schema — 只需在 `tools` 数组中声明：

```json
{
  "type": "code_execution_20260120",
  "name": "code_execution"
}
```

Claude 自动获得 `bash_code_execution`（运行 shell 命令）和 `text_editor_code_execution`（创建/查看/编辑文件）的访问权限。

### 预装 Python 库

- **数据科学**：pandas、numpy、scipy、scikit-learn、statsmodels
- **可视化**：matplotlib、seaborn
- **文件处理**：openpyxl、xlsxwriter、pillow、pypdf、pdfplumber、python-docx、python-pptx
- **数学**：sympy、mpmath
- **工具**：tqdm、python-dateutil、pytz、sqlite3

其他包可在运行时通过 `pip install` 安装。

### 支持的上传文件类型

| Type   | Extensions                         |
| ------ | ---------------------------------- |
| Data   | CSV, Excel (.xlsx/.xls), JSON, XML |
| Images | JPEG, PNG, GIF, WebP               |
| Text   | .txt, .md, .py, .js, 等            |

### 容器重用

在请求间重用容器以维护状态（文件、已安装的包、变量）。从第一个响应中提取 `container_id` 并传递给后续请求。

### 响应结构

响应包含交错的文本和工具结果块：

- `text` — Claude 的解释
- `server_tool_use` — Claude 正在做什么
- `bash_code_execution_tool_result` — 代码执行输出（检查 `return_code` 判断成功/失败）
- `text_editor_code_execution_tool_result` — 文件操作结果

> **安全：** 在将下载的文件写入磁盘之前，始终使用 `os.path.basename()` / `path.basename()` 清理文件名以防止路径遍历攻击。将文件写入专用输出目录。

---

## 服务端工具：网络搜索和网络获取

网络搜索和网络获取让 Claude 搜索网络并获取页面内容。它们在服务端运行 — 只需包含工具定义，Claude 会自动处理查询、获取和结果处理。

### 工具定义

```json
[
  { "type": "web_search_20260209", "name": "web_search" },
  { "type": "web_fetch_20260209", "name": "web_fetch" }
]
```

### 动态过滤（Opus 4.6 / Sonnet 4.6）

`web_search_20260209` 和 `web_fetch_20260209` 版本支持**动态过滤** — Claude 编写并执行代码在搜索结果进入上下文窗口之前进行过滤，提高准确性和 token 效率。动态过滤内置于这些工具版本中并自动激活；你不需要单独声明 `code_execution` 工具或传递任何 beta 请求头。

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

没有动态过滤的情况下，之前的 `web_search_20250305` 版本也可用。

> **注意：** 仅当你的应用程序需要独立于网络搜索的代码执行（数据分析、文件处理、可视化）时才包含独立的 `code_execution` 工具。将其与 `_20260209` 网络工具一起使用会创建第二个执行环境，可能会混淆模型。

---

## 服务端工具：程序化工具调用

程序化工具调用让 Claude 在代码中执行复杂的多工具工作流，将中间结果保持在上下文窗口之外。Claude 编写直接调用你的工具的代码，减少多步操作的 token 使用。

完整文档请使用 WebFetch：

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling`

---

## 服务端工具：工具搜索

工具搜索工具让 Claude 从大型库中动态发现工具，而无需将所有定义加载到上下文窗口。当你有许多工具但每个查询只有少数相关时很有用。

完整文档请使用 WebFetch：

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool`

---

## 工具使用示例

你可以直接在工具定义中提供示例工具调用以演示使用模式并减少参数错误。这有助于 Claude 理解如何正确格式化工具输入，特别是对于具有复杂 schema 的工具。

完整文档请使用 WebFetch：

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use`

---

## 服务端工具：计算机使用

计算机使用让 Claude 与桌面环境交互（截图、鼠标、键盘）。它可以是 Anthropic 托管的（服务端，如代码执行）或自托管的（你提供环境并在客户端执行操作）。

完整文档请使用 WebFetch：

- URL: `https://platform.claude.com/docs/en/agents-and-tools/computer-use/overview`

---

## 客户端工具：记忆

记忆工具使 Claude 能够通过记忆文件目录在对话间存储和检索信息。Claude 可以创建、读取、更新和删除在会话间持久化的文件。

### 关键事实

- 客户端工具 — 你通过实现控制存储
- 支持命令：`view`、`create`、`str_replace`、`insert`、`delete`、`rename`
- 在 `/memories` 目录中操作文件
- SDK 提供辅助类/函数用于实现记忆后端

> **安全：** 切勿在记忆文件中存储 API 密钥、密码、令牌或其他机密。对个人身份信息（PII）要谨慎 — 在持久化用户数据之前检查数据隐私法规（GDPR、CCPA）。参考实现没有内置访问控制；在多用户系统中，在工具处理程序中实现每用户记忆目录和身份验证。

完整实现示例请使用 WebFetch：

- Docs: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md`

---

## 结构化输出

结构化输出约束 Claude 的响应遵循特定的 JSON schema，保证有效、可解析的输出。这不是一个单独的工具 — 它增强 Messages API 响应格式和/或工具参数验证。

两个功能可用：

- **JSON 输出**（`output_config.format`）：控制 Claude 的响应格式
- **严格工具使用**（`strict: true`）：保证有效的工具参数 schema

**支持的模型：** Claude Opus 4.6、Claude Sonnet 4.6 和 Claude Haiku 4.5。旧模型（Claude Opus 4.5、Claude Opus 4.1）也支持结构化输出。

> **推荐：** 使用 `client.messages.parse()` 自动根据 schema 验证响应。直接使用 `messages.create()` 时，使用 `output_config: {format: {...}}`。`output_format` 便捷参数也被某些 SDK 方法（例如 `.parse()`）接受，但 `output_config.format` 是规范级别的 API 参数。

### JSON Schema 限制

**支持：**

- 基本类型：object、array、string、integer、number、boolean、null
- `enum`、`const`、`anyOf`、`allOf`、`$ref`/`$def`
- 字符串格式：`date-time`、`time`、`date`、`duration`、`email`、`hostname`、`uri`、`ipv4`、`ipv6`、`uuid`
- `additionalProperties: false`（所有对象必需）

**不支持：**

- 递归 schema
- 数值约束（`minimum`、`maximum`、`multipleOf`）
- 字符串约束（`minLength`、`maxLength`）
- 复杂数组约束
- `additionalProperties` 设置为除 `false` 以外的任何值

Python 和 TypeScript SDK 通过从发送到 API 的 schema 中移除不支持的约束并在客户端验证它们来自动处理。

### 重要说明

- **首次请求延迟**：新 schema 会产生一次性编译成本。使用相同 schema 的后续请求使用 24 小时缓存。
- **拒绝**：如果 Claude 因安全原因拒绝（`stop_reason: "refusal"`），输出可能与你的 schema 不匹配。
- **Token 限制**：如果 `stop_reason: "max_tokens"`，输出可能不完整。增加 `max_tokens`。
- **不兼容**：引用（返回 400 错误）、消息预填充。
- **兼容**：Batches API、流式传输、token 计数、扩展思考。

---

## 有效工具使用技巧

1. **提供详细描述**：Claude 严重依赖描述来理解何时以及如何使用工具
2. **使用具体的工具名称**：`get_current_weather` 比 `weather` 更好
3. **验证输入**：在执行前始终验证工具输入
4. **优雅处理错误**：返回信息丰富的错误消息以便 Claude 调整
5. **限制工具数量**：太多工具会混淆模型 — 保持集合专注
6. **测试工具交互**：在各种场景中验证 Claude 正确使用工具

详细工具使用文档请使用 WebFetch：

- URL: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview`
