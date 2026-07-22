# Agent SDK — TypeScript

Claude Agent SDK 提供更高级的接口，用于构建具有内置工具、安全功能和 Agent 能力的 AI Agent。

## 安装

```bash
npm install @anthropic-ai/claude-agent-sdk
```

---

## 快速入门

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Explain this codebase",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if ("result" in message) {
    console.log(message.result);
  }
}
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

## 权限系统

```typescript
for await (const message of query({
  prompt: "Refactor the authentication module",
  options: {
    allowedTools: ["Read", "Edit", "Write"],
    permissionMode: "acceptEdits",
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

权限模式：

- `"default"`：危险操作时提示
- `"plan"`：仅规划，不执行
- `"acceptEdits"`：自动接受文件编辑
- `"dontAsk"`：不提示（适用于 CI/CD）
- `"bypassPermissions"`：跳过所有提示（需要在 options 中设置 `allowDangerouslySkipPermissions: true`）

---

## MCP（Model Context Protocol）支持

```typescript
for await (const message of query({
  prompt: "Open example.com and describe what you see",
  options: {
    mcpServers: {
      playwright: { command: "npx", args: ["@playwright/mcp@latest"] },
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

### 进程内 MCP 工具

你可以使用 `tool()` 和 `createSdkMcpServer` 定义在进程内运行的自定义工具：

```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const myTool = tool("my-tool", "Description", { input: z.string() }, async (args) => {
  return { content: [{ type: "text", text: "result" }] };
});

const server = createSdkMcpServer({ name: "my-server", tools: [myTool] });

// 传递给 query
for await (const message of query({
  prompt: "Use my-tool to do something",
  options: { mcpServers: { myServer: server } },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## Hooks

```typescript
import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFileSync } from "fs";

const logFileChange: HookCallback = async (input) => {
  const filePath = (input as any).tool_input?.file_path ?? "unknown";
  appendFileSync(
    "./audit.log",
    `${new Date().toISOString()}: modified ${filePath}\n`,
  );
  return {};
};

for await (const message of query({
  prompt: "Refactor utils.py to improve readability",
  options: {
    allowedTools: ["Read", "Edit", "Write"],
    permissionMode: "acceptEdits",
    hooks: {
      PostToolUse: [{ matcher: "Edit|Write", hooks: [logFileChange] }],
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

可用的 hook 事件：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`Notification`、`UserPromptSubmit`、`SessionStart`、`SessionEnd`、`Stop`、`SubagentStart`、`SubagentStop`、`PreCompact`、`PermissionRequest`、`Setup`、`TeammateIdle`、`TaskCompleted`、`ConfigChange`

---

## 常用选项

`query()` 接受顶层 `prompt`（字符串）和 `options` 对象：

```typescript
query({ prompt: "...", options: { ... } })
```

| Option                              | Type   | Description                                                                |
| ----------------------------------- | ------ | -------------------------------------------------------------------------- |
| `cwd`                               | string | 文件操作的工作目录                                                         |
| `allowedTools`                      | array  | Agent 可以使用的工具（例如 `["Read", "Edit", "Bash"]`）                   |
| `tools`                             | array  | 要提供的内置工具（限制默认集合）                                           |
| `disallowedTools`                   | array  | 明确禁止的工具                                                             |
| `permissionMode`                    | string | 如何处理权限提示                                                           |
| `allowDangerouslySkipPermissions`   | bool   | 必须为 `true` 才能使用 `permissionMode: "bypassPermissions"`               |
| `mcpServers`                        | object | 要连接的 MCP 服务器                                                        |
| `hooks`                             | object | 用于自定义行为的 hooks                                                     |
| `systemPrompt`                      | string | 自定义系统提示                                                             |
| `maxTurns`                          | number | 停止前最大 Agent 轮数                                                      |
| `maxBudgetUsd`                      | number | 查询的最大预算（美元）                                                     |
| `model`                             | string | 模型 ID（默认：由 CLI 决定）                                               |
| `agents`                            | object | 子 Agent 定义（`Record<string, AgentDefinition>`）                         |
| `outputFormat`                      | object | 结构化输出 schema                                                          |
| `thinking`                          | object | 思考/推理控制                                                              |
| `betas`                             | array  | 要启用的 beta 功能（例如 `["context-1m-2025-08-07"]`）                    |
| `settingSources`                    | array  | 要加载的设置（例如 `["project"]`）。默认：无（不加载 CLAUDE.md 文件）      |
| `env`                               | object | 为会话设置的环境变量                                                       |

---

## 子 Agent

```typescript
for await (const message of query({
  prompt: "Use the code-reviewer agent to review this codebase",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "code-reviewer": {
        description: "Expert code reviewer for quality and security reviews.",
        prompt: "Analyze code quality and suggest improvements.",
        tools: ["Read", "Glob", "Grep"],
      },
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## 消息类型

```typescript
for await (const message of query({
  prompt: "Find TODO comments",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if ("result" in message) {
    console.log(message.result);
  } else if (message.type === "system" && message.subtype === "init") {
    const sessionId = message.session_id; // 捕获以便稍后恢复
  }
}
```

---

## 最佳实践

1. **始终指定 allowedTools** — 明确列出 Agent 可以使用的工具
2. **设置工作目录** — 始终为文件操作指定 `cwd`
3. **使用适当的权限模式** — 从 `"default"` 开始，仅在需要时升级
4. **处理所有消息类型** — 检查 `result` 属性以获取 Agent 输出
5. **限制 maxTurns** — 用合理的限制防止 Agent 失控
