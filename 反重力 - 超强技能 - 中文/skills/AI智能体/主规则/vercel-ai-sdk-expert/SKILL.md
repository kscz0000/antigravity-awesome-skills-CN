---
name: vercel-ai-sdk-expert
description: "Vercel AI SDK 专家，涵盖 Core API（generateText、streamText）、UI 钩子（useChat、useCompletion）、工具调用，以及与 React 和 Next.js 配合使用的流式 UI 组件。触发词：Vercel AI SDK、generateText、streamText、useChat、useCompletion、工具调用、流式 UI。"
risk: safe
source: community
date_added: "2026-03-06"
---

# Vercel AI SDK 专家

你是一位生产级的 Vercel AI SDK 专家，帮助开发者构建 AI 驱动的应用、聊天机器人和生成式 UI 体验，主要使用 Next.js 和 React。你精通 `ai`（AI SDK Core）和 `@ai-sdk/react`（AI SDK UI）两个包。你理解流式输出、语言模型集成、系统提示、工具调用（函数调用）以及结构化数据生成。

## 何时使用此技能

- 在 React 或 Next.js 应用中添加 AI 聊天或文本生成功能时
- 将 LLM 响应流式传输到前端 UI 时
- 使用 LLM 实现工具调用/函数调用时
- 使用 `generateObject` 从 LLM 返回结构化数据（JSON）时
- 构建 AI 驱动的生成式 UI（流式 React 组件）时
- 从直接调用 OpenAI/Anthropic API 迁移到统一的 AI SDK 时
- 排查 `useChat` 或 `streamText` 的流式问题时

## 核心概念

### 为什么选择 Vercel AI SDK？

Vercel AI SDK 是一个统一框架，抽象了特定提供商的 API（OpenAI、Anthropic、Google Gemini、Mistral）。它提供两个主要层次：
1. **AI SDK Core (`ai`)**：与服务端 LLM 交互的函数（`generateText`、`streamText`、`generateObject`）。
2. **AI SDK UI (`@ai-sdk/react`)**：用于管理聊天状态和流式传输的前端钩子（`useChat`、`useCompletion`）。

## 服务端生成（Core API）

### 基本文本生成

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

// Returns the full string once completion is done (no streaming)
const { text, usage } = await generateText({
  model: openai("gpt-4o"),
  system: "You are a helpful assistant evaluating code.",
  prompt: "Review the following python code...",
});

console.log(text);
console.log(`Tokens used: ${usage.totalTokens}`);
```

### 流式文本

```typescript
// app/api/chat/route.ts (Next.js App Router API Route)
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'You are a friendly customer support bot.',
    messages,
  });

  // Automatically converts the stream to a readable web stream
  return result.toDataStreamResponse();
}
```

### 结构化数据（JSON）生成

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object } = await generateObject({
  model: openai('gpt-4o-2024-08-06'), // Use models good at structured output
  system: 'Extract information from the receipt text.',
  prompt: receiptText,
  // Pass a Zod schema to enforce output structure
  schema: z.object({
    storeName: z.string(),
    totalAmount: z.number(),
    items: z.array(z.object({
      name: z.string(),
      price: z.number(),
    })),
    date: z.string().describe("ISO 8601 date format"),
  }),
});

// `object` is automatically fully typed according to the Zod schema!
console.log(object.totalAmount); 
```

## 前端 UI 钩子

### `useChat`（对话式 UI）

```tsx
// app/page.tsx (Next.js Client Component)
"use client";

import { useChat } from "ai/react";

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat", // Points to the streamText route created above
    // Optional callbacks
    onFinish: (message) => console.log("Done streaming:", message),
    onError: (error) => console.error(error)
  });

  return (
    <div className="flex flex-col h-screen max-w-md mx-auto p-4">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((m) => (
          <div key={m.id} className={`mb-4 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`p-2 rounded-lg inline-block ${m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              {m.target || m.content}
            </span>
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Say something..."
          className="flex-1 p-2 border rounded"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} className="bg-black text-white p-2 rounded">
          Send
        </button>
      </form>
    </div>
  );
}
```

## 工具调用（Function Calling）

工具允许 LLM 与你的代码交互，在回复用户之前获取外部数据或执行操作。

### 服务端工具定义

```typescript
// app/api/chat/route.ts
import { streamText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      getWeather: tool({
        description: 'Get the current weather in a given location',
        parameters: z.object({
          location: z.string().describe('The city and state, e.g. San Francisco, CA'),
          unit: z.enum(['celsius', 'fahrenheit']).optional(),
        }),
        // Execute runs when the LLM decides to call this tool
        execute: async ({ location, unit = 'celsius' }) => {
          // Fetch from your actual weather API or database
          const temp = location.includes("San Francisco") ? 15 : 22;
          return `The weather in ${location} is ${temp}° ${unit}.`;
        },
      }),
    },
    // Allows the LLM to call tools automatically in a loop until it has the answer
    maxSteps: 5, 
  });

  return result.toDataStreamResponse();
}
```

### 多步骤工具调用的 UI

使用 `maxSteps` 时，如果你在 UI 中处理工具调用，`useChat` 钩子会显示中间的工具调用。

```tsx
// Inside the `useChat` messages.map loop
{m.role === 'assistant' && m.toolInvocations?.map((toolInvocation) => (
  <div key={toolInvocation.toolCallId} className="text-sm text-gray-500">
    {toolInvocation.state === 'result' ? (
      <p>✅ Fetched weather for {toolInvocation.args.location}</p>
    ) : (
      <p>⏳ Fetching weather for {toolInvocation.args.location}...</p>
    )}
  </div>
))}
```

## 最佳实践

- ✅ **建议：** 使用 `openai('gpt-4o')` 或 `anthropic('claude-3-5-sonnet-20240620')` 格式（来自特定的提供商包如 `@ai-sdk/openai`），而不是旧的 edge runtime 封装。
- ✅ **建议：** 使用 `generateObject()` 时提供严格的 Zod `schema` 和清晰的 `system` 提示。
- ✅ **建议：** 在使用 `streamText` 的 Next.js API 路由中设置 `maxDuration = 30`（如果是 Pro 计划可以更高），因为 LLM 流式响应需要时间，而 Vercel 的默认限制是 10-15 秒。
- ✅ **建议：** 使用 `tool()` 时为 Zod 参数添加详尽的 `description` 标签，因为 LLM 完全依赖这些字符串来理解何时以及如何调用工具。
- ✅ **建议：** 在提供工具时启用 `maxSteps: 5`（或类似值），否则 LLM 在看到工具结果后*无法*回复用户！
- ❌ **不要：** 在使用 `streamText` 的 Next.js App Router API 路由中忘记返回 `result.toDataStreamResponse()`；标准的 JSON 响应会破坏分块传输。
- ❌ **不要：** 在没有验证的情况下盲目信任 `generateObject` 的输出，即使 Zod 强制了结构——始终使用 `try/catch` 处理失败状态。

## 故障排查

**问题：** 流式聊天在 10-15 秒后突然中断。
**解决方案：** 无服务器函数超时。在 Next.js API 路由文件中添加 `export const maxDuration = 30;`（或你的计划限制允许的值）。

**问题：** 出现"Tool execution failed"或 LLM 在使用工具后没有返回答案。
**解决方案：** `streamText` 在工具调用完成后会立即停止，除非你提供 `maxSteps`。设置 `maxSteps: 2`（或更高）让 LLM 看到工具结果并构建最终的文本响应。

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为针对特定环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
