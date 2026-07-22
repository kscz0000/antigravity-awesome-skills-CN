---
name: m365-agents-ts
description: Microsoft 365 Agents SDK 的 TypeScript/Node.js 开发指南。当用户要求构建 Microsoft 365、Teams 或 Copilot Studio 企业智能体，或涉及 Express 托管、AgentApplication 路由、流式响应及 Copilot Studio 客户端集成时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Microsoft 365 Agents SDK (TypeScript)

使用 Microsoft 365 Agents SDK 构建面向 Microsoft 365、Teams 和 Copilot Studio 的企业智能体，支持 Express 托管、AgentApplication 路由、流式响应和 Copilot Studio 客户端集成。

## 实现前
- 使用 microsoft-docs MCP 验证 AgentApplication、startServer 和 CopilotStudioClient 的最新 API 签名。
- 在搭建示例或模板前，先确认 npm 上的包版本。

## 安装

```bash
npm install @microsoft/agents-hosting @microsoft/agents-hosting-express @microsoft/agents-activity
npm install @microsoft/agents-copilotstudio-client
```

## 环境变量

```bash
PORT=3978
AZURE_RESOURCE_NAME=<azure-openai-resource>
AZURE_API_KEY=<azure-openai-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

TENANT_ID=<tenant-id>
CLIENT_ID=<client-id>
CLIENT_SECRET=<client-secret>

COPILOT_ENVIRONMENT_ID=<environment-id>
COPILOT_SCHEMA_NAME=<schema-name>
COPILOT_CLIENT_ID=<copilot-app-client-id>
COPILOT_BEARER_TOKEN=<copilot-jwt>
```

## 核心工作流：Express 托管的 AgentApplication

```typescript
import { AgentApplication, TurnContext, TurnState } from "@microsoft/agents-hosting";
import { startServer } from "@microsoft/agents-hosting-express";

const agent = new AgentApplication<TurnState>();

agent.onConversationUpdate("membersAdded", async (context: TurnContext) => {
  await context.sendActivity("Welcome to the agent.");
});

agent.onMessage("hello", async (context: TurnContext) => {
  await context.sendActivity(`Echo: ${context.activity.text}`);
});

startServer(agent);
```

## 使用 Azure OpenAI 的流式响应

```typescript
import { azure } from "@ai-sdk/azure";
import { AgentApplication, TurnContext, TurnState } from "@microsoft/agents-hosting";
import { startServer } from "@microsoft/agents-hosting-express";
import { streamText } from "ai";

const agent = new AgentApplication<TurnState>();

agent.onMessage("poem", async (context: TurnContext) => {
  context.streamingResponse.setFeedbackLoop(true);
  context.streamingResponse.setGeneratedByAILabel(true);
  context.streamingResponse.setSensitivityLabel({
    type: "https://schema.org/Message",
    "@type": "CreativeWork",
    name: "Internal",
  });

  await context.streamingResponse.queueInformativeUpdate("starting a poem...");

  const { fullStream } = streamText({
    model: azure(process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini"),
    system: "You are a creative assistant.",
    prompt: "Write a poem about Apollo.",
  });

  try {
    for await (const part of fullStream) {
      if (part.type === "text-delta" && part.text.length > 0) {
        await context.streamingResponse.queueTextChunk(part.text);
      }
      if (part.type === "error") {
        throw new Error(`Streaming error: ${part.error}`);
      }
    }
  } finally {
    await context.streamingResponse.endStream();
  }
});

startServer(agent);
```

## Invoke 活动处理

```typescript
import { Activity, ActivityTypes } from "@microsoft/agents-activity";
import { AgentApplication, TurnContext, TurnState } from "@microsoft/agents-hosting";

const agent = new AgentApplication<TurnState>();

agent.onActivity("invoke", async (context: TurnContext) => {
  const invokeResponse = Activity.fromObject({
    type: ActivityTypes.InvokeResponse,
    value: { status: 200 },
  });

  await context.sendActivity(invokeResponse);
  await context.sendActivity("Thanks for submitting your feedback.");
});
```

## Copilot Studio 客户端（Direct to Engine）

```typescript
import { CopilotStudioClient } from "@microsoft/agents-copilotstudio-client";

const settings = {
  environmentId: process.env.COPILOT_ENVIRONMENT_ID!,
  schemaName: process.env.COPILOT_SCHEMA_NAME!,
  clientId: process.env.COPILOT_CLIENT_ID!,
};

const tokenProvider = async (): Promise<string> => {
  return process.env.COPILOT_BEARER_TOKEN!;
};

const client = new CopilotStudioClient(settings, tokenProvider);

const conversation = await client.startConversationAsync();
const reply = await client.askQuestionAsync("Hello!", conversation.id);
console.log(reply);
```

## Copilot Studio WebChat 集成

```typescript
import { CopilotStudioWebChat } from "@microsoft/agents-copilotstudio-client";

const directLine = CopilotStudioWebChat.createConnection(client, {
  showTyping: true,
});

window.WebChat.renderWebChat({
  directLine,
}, document.getElementById("webchat")!);
```

## 最佳实践

1. 使用 AgentApplication 进行路由，保持每个处理程序职责单一。
2. 长时间运行的补全任务优先使用 streamingResponse，并在 finally 块中调用 endStream。
3. 不要将密钥写入源代码；从环境变量或安全存储中加载令牌。
4. 复用 CopilotStudioClient 实例，在令牌提供者中缓存令牌。
5. 在记录或持久化反馈数据前，先验证 invoke 载荷。

## 参考文件

| 文件 | 内容 |
| --- | --- |
| references/acceptance-criteria.md | 导入路径、托管管道、流式响应及 Copilot Studio 模式 |

## 参考链接

| 资源 | URL |
| --- | --- |
| Microsoft 365 Agents SDK | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/ |
| JavaScript SDK overview | https://learn.microsoft.com/en-us/javascript/api/overview/agents-overview?view=agents-sdk-js-latest |
| @microsoft/agents-hosting-express | https://learn.microsoft.com/en-us/javascript/api/%40microsoft/agents-hosting-express?view=agents-sdk-js-latest |
| @microsoft/agents-copilotstudio-client | https://learn.microsoft.com/en-us/javascript/api/%40microsoft/agents-copilotstudio-client?view=agents-sdk-js-latest |
| Integrate with Copilot Studio | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/integrate-with-mcs |
| GitHub samples | https://github.com/microsoft/Agents/tree/main/samples/nodejs |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
