# Neon Functions 上的 AI SDK Agent

Neon Function 是一个长驻 Node.js 24 进程，这使它成为承载 [Vercel AI SDK](https://ai-sdk.dev) Agent 的天然环境：处理器在请求生命周期内持续流式传输（15 分钟预算，见 [超时](../SKILL.md#超时与运行时限制)），所以多步工具循环和图像/视频生成不会像在 Lambda 风格无服务器上那样被截断。将模型指向 **Neon AI Gateway**（参见 `neon-ai-gateway` 技能）就无需管理额外的 Provider Key——一个 Neon 凭据即可访问全部模型目录。

AI SDK 是从 TypeScript 构建 Agent 的**推荐**方式：一套原语（`streamText`、`generateText`、工具调用、结构化输出）覆盖所有模型。对于需要内存和工作流重度的内置追踪 Agent，改用 Mastra（参见 [references/mastra-studio.md](mastra-studio.md)）；两者都指向同一个网关。

以下模式是一个完整的 Agent：它流式输出聊天内容，并在被要求时生成图片、上传到 Object Storage 并在 Postgres 中建立索引。

## 1. 声明网关和函数

Agent 需要 AI Gateway（以及示例中需要的 Object Storage 存储桶）。将两者与函数一起在 `neon.ts` 中声明——`neon deploy` 会预配它们并在运行时注入凭据（参见 `neon-ai-gateway` 和 `neon-object-storage` 技能）：

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  preview: {
    aiGateway: true,
    buckets: { images: {} },
    functions: {
      agent: { name: "ai agent", source: "src/index.ts" },
    },
  },
});
```

## 2. 处理器：流式工具调用 Agent

函数的默认导出是 Web 标准 `{ fetch }` 处理器。`@neon/ai-sdk-provider` 自动读取注入的网关凭据，所以 `neon("<model>")` 就是你需要的全部模型配置——它将每个模型路由到正确的方言（Anthropic → Messages、OpenAI/Codex → Responses、其他 → MLflow）。返回 `result.toUIMessageStreamResponse()` 以便 AI SDK 的 `useChat` 钩子消费流：

```typescript
// src/index.ts
import { neon } from "@neon/ai-sdk-provider";
import { streamText, tool, stepCountIs, type ModelMessage } from "ai";
import { z } from "zod";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import { todos } from "./db/schema";

const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 5 });
const db = drizzle(pool);

export default {
  async fetch(request: Request) {
    if (request.method !== "POST") {
      return new Response("POST chat messages here", { status: 405 });
    }
    const { messages } = (await request.json()) as { messages: ModelMessage[] };

    const result = streamText({
      model: neon("claude-sonnet-4-6"), // 可切换为 gpt-5-mini、gemini-2.5-flash 等
      system: "You are a concise assistant with access to the user's todos.",
      messages,
      tools: {
        countOpenTodos: tool({
          description: "Count the user's open todos.",
          inputSchema: z.object({}),
          execute: async () => ({ open: await db.$count(todos) }),
        }),
      },
      // 让模型调用工具然后总结，而不是第一次工具调用后停止。
      // 循环在进程内运行 —— 无宿主超时。
      stopWhen: stepCountIs(5),
      onError({ error }) {
        console.error("[streamText] error:", error);
      },
    });

    return result.toUIMessageStreamResponse({
      onError: (error) => (error instanceof Error ? error.message : String(error)),
    });
  },
};
```

`tool({ inputSchema, execute })` 是 AI SDK v5+ 形态（参数名是 `inputSchema`，不是旧的 `parameters`）。工具的 `execute` 在函数**内部**运行，紧邻 Postgres——没有额外的网络跳转。

## 3. 生成图片并持久化

网关暴露 OpenAI Responses 内置的 **`image_generation`** 工具（仅 GPT-5 模型；图片以 base64 行内返回）。将生成的资源持久化到 Object Storage 并在 Postgres 中索引以便它们随分支一起迁移——**推荐**的存储客户端是 Files SDK `neon` 适配器（参见 `neon-object-storage` 技能）：

```typescript
import { neon } from "@neon/ai-sdk-provider";
import { streamText } from "ai";
import { Files } from "files-sdk";
import { neon as neonFiles } from "files-sdk/neon";
import { randomUUID } from "node:crypto";

const files = new Files({ adapter: neonFiles({ bucket: "images" }) });

const result = streamText({
  model: neon("gpt-5-mini"),
  system: "Use image_generation when the user asks for a picture, then describe it.",
  messages,
  tools: {
    image_generation: neon.tools.imageGeneration({
      outputFormat: "jpeg",
      quality: "low", // 网关限制单次响应约 640 KB — 保持图片小
      size: "1024x1024",
    }),
  },
  async onStepFinish({ toolResults }) {
    for (const tr of toolResults) {
      if (tr.toolName !== "image_generation") continue;
      const base64 = imageResultBase64(tr.output);
      if (!base64) continue;
      const key = `generated/${randomUUID()}.jpg`;
      await files.upload(key, Buffer.from(base64, "base64"), { contentType: "image/jpeg" });
      // …向 Postgres 插入一行并以 `key` 为键；之后通过 files.url(key) 提供
    }
  },
});
```

保持生成的图片较小：网关将单次响应限制在约 640 KB 且有上游超时，因此请求压缩 JPEG 而非全尺寸 PNG。

## 4. 从客户端直接调用（不要代理流）

这样长流不会被 Web 宿主的无服务器限制截断，让**浏览器直接调用函数**并在处理器顶部认证——参见 [Functions 作为 Agent 后端](../SKILL.md#functions-作为-agent-后端-nextjs-及类似框架) 了解 JWT 验证 + CORS 模式和 AI SDK `DefaultChatTransport` 接线。

## 5. 运行与部署

```bash
neon dev      # 注入 DATABASE_URL + 网关/存储凭据；热重载
neon deploy   # 预配网关 + 存储桶并部署函数
```

```bash
curl -N -X POST "$(neon functions get agent -o json | jq -r .invocation_url)" \
  -H "content-type: application/json" \
  -d '{"messages":[{"role":"user","content":"How many open todos do I have?"}]}'
```

## 延伸阅读

- Neon AI Gateway 方言、模型及 `@neon/ai-sdk-provider`：`neon-ai-gateway` 技能
- 存储随数据库分支的生成资源：`neon-object-storage` 技能
- AI SDK Agent / 工具：https://ai-sdk.dev/docs/foundations/agents
