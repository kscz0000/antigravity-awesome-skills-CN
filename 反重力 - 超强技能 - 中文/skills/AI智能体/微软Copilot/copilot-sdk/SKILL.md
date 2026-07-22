---
name: copilot-sdk
description: "构建以编程方式与 GitHub Copilot 交互的应用程序。SDK 通过 JSON-RPC 封装 Copilot CLI，提供会话管理、自定义工具、钩子、MCP 服务器集成和流式传输，支持 Node.js、Python、Go 和 .NET。触发词：Copilot SDK、GitHub Copilot SDK、Copilot CLI 集成、Copilot 工具开发、Copilot 会话管理、Copilot MCP 集成、Copilot 流式响应、Copilot 自定义工具"
risk: unknown
source: community
date_added: "2026-02-27"
---

# GitHub Copilot SDK

构建以编程方式与 GitHub Copilot 交互的应用程序。SDK 通过 JSON-RPC 封装 Copilot CLI，提供会话管理、自定义工具、钩子、MCP 服务器集成和流式传输，支持 Node.js、Python、Go 和 .NET。

## 前置条件

- **GitHub Copilot CLI** 已安装并认证（使用 `copilot --version` 验证）
- **GitHub Copilot 订阅**（个人版、商业版或企业版）— BYOK 模式不需要
- **运行时环境：** Node.js 18+ / Python 3.8+ / Go 1.21+ / .NET 8.0+

## 安装

| 语言 | 包名 | 安装命令 |
|----------|---------|---------|
| Node.js | `@github/copilot-sdk` | `npm install @github/copilot-sdk` |
| Python | `github-copilot-sdk` | `pip install github-copilot-sdk` |
| Go | `github.com/github/copilot-sdk/go` | `go get github.com/github/copilot-sdk/go` |
| .NET | `GitHub.Copilot.SDK` | `dotnet add package GitHub.Copilot.SDK` |

---

## 核心模式：客户端 → 会话 → 消息

所有 SDK 使用都遵循此模式：创建客户端、创建会话、发送消息。

### Node.js / TypeScript

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
```

### Python

```python
import asyncio
from copilot import CopilotClient

async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})
    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Go

```go
client := copilot.NewClient(nil)
if err := client.Start(ctx); err != nil { log.Fatal(err) }
defer client.Stop()

session, _ := client.CreateSession(ctx, &copilot.SessionConfig{Model: "gpt-4.1"})
response, _ := session.SendAndWait(ctx, copilot.MessageOptions{Prompt: "What is 2 + 2?"})
fmt.Println(*response.Data.Content)
```

### .NET

```csharp
await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-4.1" });
var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = "What is 2 + 2?" });
Console.WriteLine(response?.Data.Content);
```

---

## 流式响应

通过设置 `streaming: true` 并订阅增量事件来启用实时输出。

```typescript
const session = await client.createSession({ model: "gpt-4.1", streaming: true });

session.on("assistant.message_delta", (event) => {
    process.stdout.write(event.data.deltaContent);
});
session.on("session.idle", () => console.log());

await session.sendAndWait({ prompt: "Tell me a joke" });
```

**Python 等效代码：**

```python
from copilot.generated.session_events import SessionEventType

session = await client.create_session({"model": "gpt-4.1", "streaming": True})

def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        sys.stdout.write(event.data.delta_content)
        sys.stdout.flush()

session.on(handle_event)
await session.send_and_wait({"prompt": "Tell me a joke"})
```

### 事件订阅

| 方法 | 描述 |
|--------|-------------|
| `on(handler)` | 订阅所有事件；返回取消订阅函数 |
| `on(eventType, handler)` | 订阅特定事件类型（仅 Node.js） |

---

## 自定义工具

定义 Copilot 可以调用的工具以扩展其能力。

### Node.js

```typescript
import { CopilotClient, defineTool } from "@github/copilot-sdk";

const getWeather = defineTool("get_weather", {
    description: "Get the current weather for a city",
    parameters: {
        type: "object",
        properties: { city: { type: "string", description: "The city name" } },
        required: ["city"],
    },
    handler: async ({ city }) => ({ city, temperature: "72°F", condition: "sunny" }),
});

const session = await client.createSession({
    model: "gpt-4.1",
    tools: [getWeather],
});
```

### Python

```python
from copilot.tools import define_tool
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="The city name")

@define_tool(description="Get the current weather for a city")
async def get_weather(params: GetWeatherParams) -> dict:
    return {"city": params.city, "temperature": "72°F", "condition": "sunny"}

session = await client.create_session({"model": "gpt-4.1", "tools": [get_weather]})
```

### Go

```go
type WeatherParams struct {
    City string `json:"city" jsonschema:"The city name"`
}

getWeather := copilot.DefineTool("get_weather", "Get weather for a city",
    func(params WeatherParams, inv copilot.ToolInvocation) (WeatherResult, error) {
        return WeatherResult{City: params.City, Temperature: "72°F"}, nil
    },
)

session, _ := client.CreateSession(ctx, &copilot.SessionConfig{
    Model: "gpt-4.1",
    Tools: []copilot.Tool{getWeather},
})
```

### .NET

```csharp
var getWeather = AIFunctionFactory.Create(
    ([Description("The city name")] string city) => new { city, temperature = "72°F" },
    "get_weather", "Get the current weather for a city");

await using var session = await client.CreateSessionAsync(new SessionConfig {
    Model = "gpt-4.1", Tools = [getWeather],
});
```

---

## 钩子

在关键生命周期节点拦截和自定义会话行为。

| 钩子 | 触发时机 | 用途 |
|------|---------|----------|
| `onPreToolUse` | 工具执行前 | 权限控制、参数修改 |
| `onPostToolUse` | 工具执行后 | 结果转换、日志记录 |
| `onUserPromptSubmitted` | 用户发送消息时 | 提示词修改、过滤 |
| `onSessionStart` | 会话开始时 | 添加上下文、配置会话 |
| `onSessionEnd` | 会话结束时 | 清理、分析 |
| `onErrorOccurred` | 发生错误时 | 自定义错误处理、重试逻辑 |

### 示例：工具权限控制

```typescript
const session = await client.createSession({
    hooks: {
        onPreToolUse: async (input) => {
            if (["shell", "bash"].includes(input.toolName)) {
                return { permissionDecision: "deny", permissionDecisionReason: "Shell access not permitted" };
            }
            return { permissionDecision: "allow" };
        },
    },
});
```

### 工具执行前输出

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `permissionDecision` | `"allow"` \| `"deny"` \| `"ask"` | 是否允许工具调用 |
| `permissionDecisionReason` | string | 拒绝/询问的原因说明 |
| `modifiedArgs` | object | 传递的修改后参数 |
| `additionalContext` | string | 对话的额外上下文 |
| `suppressOutput` | boolean | 在对话中隐藏工具输出 |

---

## MCP 服务器集成

连接 MCP 服务器以获取预构建的工具能力。

### 远程 HTTP 服务器

```typescript
const session = await client.createSession({
    mcpServers: {
        github: { type: "http", url: "https://api.githubcopilot.com/mcp/" },
    },
});
```

### 本地 Stdio 服务器

```typescript
const session = await client.createSession({
    mcpServers: {
        filesystem: {
            type: "local",
            command: "npx",
            args: ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
            tools: ["*"],
        },
    },
});
```

### MCP 配置字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `type` | `"local"` \| `"http"` | 服务器传输类型 |
| `command` | string | 可执行文件路径（本地） |
| `args` | string[] | 命令参数（本地） |
| `url` | string | 服务器 URL（http） |
| `tools` | string[] | `["*"]` 或特定工具名称 |
| `env` | object | 环境变量 |
| `cwd` | string | 工作目录（本地） |
| `timeout` | number | 超时时间（毫秒） |

---

## 认证

### 方法（优先级顺序）

1. **显式令牌** — 构造函数中的 `githubToken`
2. **环境变量** — `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN`
3. **存储的 OAuth** — 来自 `copilot auth login`
4. **GitHub CLI** — `gh auth` 凭据

### 编程式令牌

```typescript
const client = new CopilotClient({ githubToken: process.env.GITHUB_TOKEN });
```

### BYOK（自带密钥）

使用您自己的 API 密钥 — 无需 Copilot 订阅。

```typescript
const session = await client.createSession({
    model: "gpt-5.2-codex",
    provider: {
        type: "openai",
        baseUrl: "https://your-resource.openai.azure.com/openai/v1/",
        wireApi: "responses",
        apiKey: process.env.FOUNDRY_API_KEY,
    },
});
```

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| OpenAI | `"openai"` | OpenAI API 及兼容端点 |
| Azure OpenAI | `"azure"` | 原生 Azure 端点（不包含 `/openai/v1`） |
| Azure AI Foundry | `"openai"` | OpenAI 兼容的 Foundry 端点 |
| Anthropic | `"anthropic"` | Claude 模型 |
| Ollama | `"openai"` | 本地模型，无需 API 密钥 |

**Wire API：** GPT-5 系列使用 `"responses"`，其他模型使用 `"completions"`（默认）。

---

## 会话持久化

通过提供自己的会话 ID，在重启后恢复会话。

```typescript
// 使用显式 ID 创建
const session = await client.createSession({
    sessionId: "user-123-task-456",
    model: "gpt-4.1",
});

// 稍后恢复
const resumed = await client.resumeSession("user-123-task-456");
await resumed.sendAndWait({ prompt: "What did we discuss?" });
```

**会话管理：**

```typescript
const sessions = await client.listSessions();          // 列出所有
await client.deleteSession("user-123-task-456");       // 删除
await session.destroy();                                // 销毁活动会话
```

**BYOK 会话：** 恢复时必须重新提供 `provider` 配置（密钥不会被持久化）。

### 无限会话

适用于可能超出上下文限制的长时间运行工作流：

```typescript
const session = await client.createSession({
    infiniteSessions: {
        enabled: true,
        backgroundCompactionThreshold: 0.80,
        bufferExhaustionThreshold: 0.95,
    },
});
```

---

## 自定义智能体

定义专门的 AI 角色：

```typescript
const session = await client.createSession({
    customAgents: [{
        name: "pr-reviewer",
        displayName: "PR Reviewer",
        description: "Reviews pull requests for best practices",
        prompt: "You are an expert code reviewer. Focus on security, performance, and maintainability.",
    }],
});
```

---

## 系统消息

控制 AI 行为和个性：

```typescript
const session = await client.createSession({
    systemMessage: { content: "You are a helpful assistant. Always be concise." },
});
```

---

## 技能集成

加载技能目录以扩展 Copilot 能力：

```typescript
const session = await client.createSession({
    skillDirectories: ["./skills/code-review", "./skills/documentation"],
    disabledSkills: ["experimental-feature"],
});
```

---

## 权限与输入处理器

以编程方式处理工具权限和用户输入请求：

```typescript
const session = await client.createSession({
    onPermissionRequest: async (request) => {
        // 仅自动批准 git 命令
        if (request.kind === "shell") {
            return { approved: request.command.startsWith("git") };
        }
        return { approved: true };
    },
    onUserInputRequest: async (request) => {
        // 处理 ask_user 工具调用
        return { response: "yes" };
    },
});
```

---

## 外部 CLI 服务器

连接到独立运行的 CLI，而非自动管理进程：

```bash
copilot --headless --port 4321
```

```typescript
const client = new CopilotClient({ cliUrl: "localhost:4321" });
```

---

## 客户端配置

| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `cliPath` | string | Copilot CLI 可执行文件路径 |
| `cliUrl` | string | 外部 CLI 服务器 URL |
| `githubToken` | string | 用于认证的 GitHub 令牌 |
| `useLoggedInUser` | boolean | 使用存储的 CLI 凭据（默认：true） |
| `logLevel` | string | `"none"` \| `"error"` \| `"warning"` \| `"info"` \| `"debug"` |
| `autoRestart` | boolean | CLI 崩溃时自动重启（默认：true） |
| `useStdio` | boolean | 使用 stdio 传输（默认：true） |

## 会话配置

| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `model` | string | 要使用的模型（如 `"gpt-4.1"`） |
| `sessionId` | string | 用于可恢复会话的自定义 ID |
| `streaming` | boolean | 启用流式响应 |
| `tools` | Tool[] | 自定义工具 |
| `mcpServers` | object | MCP 服务器配置 |
| `hooks` | object | 会话钩子 |
| `provider` | object | BYOK 提供商配置 |
| `customAgents` | object[] | 自定义智能体定义 |
| `systemMessage` | object | 系统消息覆盖 |
| `skillDirectories` | string[] | 加载技能的目录 |
| `disabledSkills` | string[] | 要禁用的技能 |
| `reasoningEffort` | string | 推理努力程度 |
| `availableTools` | string[] | 限制可用工具 |
| `excludedTools` | string[] | 排除特定工具 |
| `infiniteSessions` | object | 自动压缩配置 |
| `workingDirectory` | string | 工作目录 |

---

## 调试

启用调试日志以排查问题：

```typescript
const client = new CopilotClient({ logLevel: "debug" });
```

**常见问题：**
- `CLI not found` → 安装 CLI 或设置 `cliPath`
- `Not authenticated` → 运行 `copilot auth login` 或提供 `githubToken`
- `Session not found` → 不要在 `destroy()` 后使用会话
- `Connection refused` → 检查 CLI 进程，启用 `autoRestart`

---

## 关键 API 摘要

| 语言 | 客户端 | 创建会话 | 发送 | 停止 |
|----------|--------|---------------|------|------|
| Node.js | `new CopilotClient()` | `client.createSession()` | `session.sendAndWait()` | `client.stop()` |
| Python | `CopilotClient()` | `client.create_session()` | `session.send_and_wait()` | `client.stop()` |
| Go | `copilot.NewClient(nil)` | `client.CreateSession()` | `session.SendAndWait()` | `client.Stop()` |
| .NET | `new CopilotClient()` | `client.CreateSessionAsync()` | `session.SendAndWaitAsync()` | `client.DisposeAsync()` |

## 参考资料

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Copilot CLI Installation](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
