# Agent SDK — Python

Claude Agent SDK 提供更高级的接口，用于构建具有内置工具、安全功能和 Agent 能力的 AI Agent。

## 安装

```bash
pip install claude-agent-sdk
```

---

## 快速入门

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Explain this codebase",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

anyio.run(main)
```

---

## 内置工具

| Tool      | Description                          |
| --------- | ------------------------------------ |
| Read      | 读取工作区中的文件                   |
| Write     | 创建新文件                           |
| Edit      | 对现有文件进行精确编辑               |
| Bash      | 执行 shell 命令                      |
| Glob      | 按模式查找文件                       |
| Grep      | 按内容搜索文件                       |
| WebSearch | 在网上搜索信息                       |
| WebFetch        | 获取并分析网页                       |
| AskUserQuestion | 向用户提出澄清问题                   |
| Agent           | 生成子 Agent                         |

---

## 主要接口

### `query()` — 简单的一次性使用

`query()` 函数是运行 Agent 的最简单方式。它返回消息的异步迭代器。

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(
    prompt="Explain this codebase",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

### `ClaudeSDKClient` — 完全控制

`ClaudeSDKClient` 提供对 Agent 生命周期的完全控制。当你需要自定义工具、hooks、流式传输或中断执行的能力时使用它。

```python
import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Explain this codebase")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)

anyio.run(main)
```

`ClaudeSDKClient` 支持：

- **上下文管理器**（`async with`）用于自动资源清理
- **`client.query(prompt)`** 向 Agent 发送提示
- **`receive_response()`** 用于流式传输消息直到完成
- **`interrupt()`** 在任务中途停止 Agent 执行
- **自定义工具必需**（通过 SDK MCP 服务器）

---

## 权限系统

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(
    prompt="Refactor the authentication module",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Write"],
        permission_mode="acceptEdits"  # 自动接受文件编辑
    )
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

权限模式：

- `"default"`：危险操作时提示
- `"plan"`：仅规划，不执行
- `"acceptEdits"`：自动接受文件编辑
- `"dontAsk"`：不提示（适用于 CI/CD）
- `"bypassPermissions"`：跳过所有提示（需要在 options 中设置 `allow_dangerously_skip_permissions=True`）

---

## MCP（Model Context Protocol）支持

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(
    prompt="Open example.com and describe what you see",
    options=ClaudeAgentOptions(
        mcp_servers={
            "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
        }
    )
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

---

## Hooks

使用回调函数自定义 Agent 行为：

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, ResultMessage

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get('tool_input', {}).get('file_path', 'unknown')
    print(f"Modified: {file_path}")
    return {}

async for message in query(
    prompt="Refactor utils.py",
    options=ClaudeAgentOptions(
        permission_mode="acceptEdits",
        hooks={
            "PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]
        }
    )
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

可用的 hook 事件：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`Notification`、`UserPromptSubmit`、`SessionStart`、`SessionEnd`、`Stop`、`SubagentStart`、`SubagentStop`、`PreCompact`、`PermissionRequest`、`Setup`、`TeammateIdle`、`TaskCompleted`、`ConfigChange`

---

## 常用选项

`query()` 接受顶层 `prompt`（字符串）和 `options` 对象（`ClaudeAgentOptions`）：

```python
async for message in query(prompt="...", options=ClaudeAgentOptions(...)):
```

| Option                              | Type   | Description                                                                |
| ----------------------------------- | ------ | -------------------------------------------------------------------------- |
| `cwd`                               | string | 文件操作的工作目录                                                         |
| `allowed_tools`                     | list   | Agent 可以使用的工具（例如 `["Read", "Edit", "Bash"]`）                   |
| `tools`                             | list   | 要提供的内置工具（限制默认集合）                                           |
| `disallowed_tools`                  | list   | 明确禁止的工具                                                             |
| `permission_mode`                   | string | 如何处理权限提示                                                           |
| `allow_dangerously_skip_permissions`| bool   | 必须为 `True` 才能使用 `permission_mode="bypassPermissions"`               |
| `mcp_servers`                       | dict   | 要连接的 MCP 服务器                                                        |
| `hooks`                             | dict   | 用于自定义行为的 hooks                                                     |
| `system_prompt`                     | string | 自定义系统提示                                                             |
| `max_turns`                         | int    | 停止前最大 Agent 轮数                                                      |
| `max_budget_usd`                    | float  | 查询的最大预算（美元）                                                     |
| `model`                             | string | 模型 ID（默认：由 CLI 决定）                                               |
| `agents`                            | dict   | 子 Agent 定义（`dict[str, AgentDefinition]`）                              |
| `output_format`                     | dict   | 结构化输出 schema                                                          |
| `thinking`                          | dict   | 思考/推理控制                                                              |
| `betas`                             | list   | 要启用的 beta 功能（例如 `["context-1m-2025-08-07"]`）                    |
| `setting_sources`                   | list   | 要加载的设置（例如 `["project"]`）。默认：无（不加载 CLAUDE.md 文件）      |
| `env`                               | dict   | 为会话设置的环境变量                                                       |

---

## 消息类型

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

async for message in query(
    prompt="Find TODO comments",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
):
    if isinstance(message, ResultMessage):
        print(message.result)
    elif isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.session_id  # 捕获以便稍后恢复
```

---

## 子 Agent

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

async for message in query(
    prompt="Use the code-reviewer agent to review this codebase",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Agent"],
        agents={
            "code-reviewer": AgentDefinition(
                description="Expert code reviewer for quality and security reviews.",
                prompt="Analyze code quality and suggest improvements.",
                tools=["Read", "Glob", "Grep"]
            )
        }
    )
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

---

## 错误处理

```python
from claude_agent_sdk import query, ClaudeAgentOptions, CLINotFoundError, CLIConnectionError, ResultMessage

try:
    async for message in query(
        prompt="...",
        options=ClaudeAgentOptions(allowed_tools=["Read"])
    ):
        if isinstance(message, ResultMessage):
            print(message.result)
except CLINotFoundError:
    print("Claude Code CLI not found. Install with: pip install claude-agent-sdk")
except CLIConnectionError as e:
    print(f"Connection error: {e}")
```

---

## 最佳实践

1. **始终指定 allowed_tools** — 明确列出 Agent 可以使用的工具
2. **设置工作目录** — 始终为文件操作指定 `cwd`
3. **使用适当的权限模式** — 从 `"default"` 开始，仅在需要时升级
4. **处理所有消息类型** — 检查 `ResultMessage` 以获取 Agent 输出
5. **限制 max_turns** — 用合理的限制防止 Agent 失控
