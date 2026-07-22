---
name: neon-ai-gateway
description: 一个 API 和一个凭证即可访问前沿与开源 LLM，内置于 Neon 分支，由 Databricks 驱动。当用户想要调用 LLM、为应用添加 AI/聊天/智能体、在模型提供商之间路由（OpenAI、Anthropic、Google/Gemini、Meta、Alibaba、DeepSeek）时使用，或...
risk: unknown
source: https://github.com/neondatabase/agent-skills/tree/main/skills/neon-ai-gateway
source_repo: neondatabase/agent-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/neondatabase/agent-skills/blob/main/LICENSE
---

# Neon AI 网关

这是预览功能，仅在 `us-east-2` 区域可用。Neon AI 网关是内置于 Neon 分支的 LLM 推理层：一个 API 和一个 Neon 凭证即可访问来自 Anthropic、OpenAI、Google、Meta、Alibaba、DeepSeek 和 Databricks 的前沿与开源模型——由 Databricks 驱动。你现有的 OpenAI/Anthropic/Gemini SDK 只需更换 base URL 即可使用。

使用此技能帮助用户通过网关发送模型调用、将其接入 AI SDK 或 Mastra，以及在不改代码的情况下切换提供商。交付可运行的推理请求、已配置的智能体，或来自 Neon 官方文档的精确解答。

## 何时使用

当应用或智能体需要调用 LLM，而用户不想自己管理模型提供商时，就应使用 AI 网关：

- **一个凭证替代多个提供商账号。** 单个 Neon 凭证即可访问七个提供商的完整模型目录。无需分别注册、配置和轮换 OpenAI / Anthropic / Google 的账单、密钥或账号。
- **切换模型无需改代码。** 统一端点兼容 OpenAI 格式，支持目录中的每个模型——只改一个 `model` 字段即可在 Claude、GPT 和 Gemini 之间切换。标准 SDK（OpenAI、Anthropic、google-genai）只需更换 base URL 即可使用。
- **AI 跟随你的分支。** 每个分支有自己的网关端点，与数据库具有相同的血统隔离。来自预览/功能分支的 AI 请求被隔离在该分支——与数据已有的隔离一致——使预览、CI 和智能体环境各自独立。
- **无需额外基础设施，且已紧邻数据。** 网关运行在你的 Neon 项目内部（并自动注入到 Neon Functions），运行在 Databricks 每月服务数万亿 token 的同一基础设施上，开箱即支持流式传输（SSE）。

如果用户已有深度的单一提供商集成，且对 Neon 分支或多模型路由没有兴趣，直接用提供商 SDK 也可以——但一旦他们想要单一凭证、模型可移植性或分支级 AI 隔离，这就是使用它的理由。

## 功能概述

- **一个 API 对接所有模型** — 前沿与开源模型统一在一个端点之后，通过目录 ID 寻址（如 `claude-sonnet-4-6`、`gpt-5-mini`、`gemini-2-5-flash`）。
- **标准 SDK，只改一个 URL** — OpenAI SDK 和 AI SDK（兼容 OpenAI 的 MLflow/Responses 路由）、Anthropic SDK（原生 Messages）、google-genai（原生 Gemini）。
- **分支级隔离** — 每个分支获得独立的网关主机；Neon 凭证授权该分支及其后代的请求。
- **流式传输** — 所有端点均支持服务器推送事件，无需额外配置。

## 配置

网关是 `neon.ts` 的一部分（分支优先工作流和 `neon.ts` 基础用法见 `neon` 技能）。在 `preview.aiGateway` 下启用：

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  preview: {
    aiGateway: true,
  },
});
```

```bash
neon deploy   # provisions the gateway on the linked branch
```

## Neon 基础设施即代码（`neon.ts`）

上方的 `preview.aiGateway` 开关是 `neon.ts` 的一部分——Neon 的基础设施即代码文件，一个 TypeScript 文件即可在版本控制中声明网关及其他所有分支服务（完整参考见 `neon` 技能）。按照 Terraform 方式对分支进行调和：

```bash
neon config status   # print the branch's live config (is the gateway on?)
neon config plan     # dry-run diff of what apply would change
neon config apply    # enable the gateway on the branch  (neon deploy is an alias)
```

网关是**分支级隔离**的：每个分支获得独立的网关主机。当 `neon.ts` 存在时，`neon checkout` 在_创建_分支时应用策略，因此新的预览/CI 分支一上来就启用了网关。检出_已有_分支不会触发调和——需运行 `neon deploy` 来应用变更。配置执行（`config apply` / `deploy`）、`link` 和 `checkout` 还会将分支的网关凭证拉取到本地 `.env.local`，这样本地运行也使用与部署函数相同的分支网关（无需手动 `env pull`）。

如需类型安全的、经过验证的注入凭证访问，将同一配置对象传给 `@neon/env` 的 `parseEnv`——它返回一个 `env.aiGateway` 命名空间（`apiKey`、`baseUrl`），源自你的 `neon.ts`。

## 环境变量

当 `preview.aiGateway` 启用时，Neon 将网关凭证以 **OpenAI 标准**环境变量注入（这样 OpenAI SDK 和 AI SDK 无需配置即可从环境变量工作），同时提供 `NEON_` 前缀的别名。在已部署的 Neon Function 内，这些变量自动注入；本地环境下，`neon env pull` 将它们写入 `.env`/`.env.local`（或使用 `neon-env run -- <cmd>` 在运行时注入而无需文件）：

| 变量                       | 含义                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPENAI_API_KEY`           | 网关 bearer token（Neon 凭证，`nt_live_...`）                                                                                                |
| `OPENAI_BASE_URL`          | 完整的 OpenAI 方式路由，**包含** `/ai-gateway/openai/v1`：`https://<branch-id>-api.ai.<region>.aws.neon.tech/ai-gateway/openai/v1`           |
| `NEON_AI_GATEWAY_TOKEN`    | 与 `OPENAI_API_KEY` 相同的 bearer（即使用户用自己的密钥覆盖了 `OPENAI_*`，此值仍保留）                                                      |
| `NEON_AI_GATEWAY_BASE_URL` | **裸分支网关主机**（`scheme://host`，**无路径**——不含 `/ai-gateway`）：`https://<branch-id>-api.ai.<region>.aws.neon.tech`                    |

两个 base URL **不同**：`OPENAI_BASE_URL` 已包含完整的 `/ai-gateway/openai/v1`（Responses）路由，而 `NEON_AI_GATEWAY_BASE_URL` 仅是裸主机，你需要自行追加 `/ai-gateway/<dialect>`（这也是 `@neon/ai-sdk-provider` 替你做的事）。主机下的路由有：

- `/ai-gateway/mlflow/v1` — 统一的、兼容 OpenAI **Chat Completions** 的路由；推荐默认选择，适用于所有提供商。
- `/ai-gateway/openai/v1` — OpenAI **Responses** API（`gpt-5-…-codex` 变体和 `gpt-5-5-pro` 需要此路由）。这是 `OPENAI_BASE_URL` 已指向的路由，因为 `@ai-sdk/openai` 提供者默认使用 Responses API。
- `/ai-gateway/anthropic/v1` — 原生 Anthropic Messages（扩展思考、提示缓存）。
- `/ai-gateway/gemini/v1beta/...` — 原生 Gemini `generateContent`。

所以 `${NEON_AI_GATEWAY_BASE_URL}/ai-gateway/mlflow/v1` 是 chat-completions 端点，`${NEON_AI_GATEWAY_BASE_URL}/ai-gateway/openai/v1` 等于 `OPENAI_BASE_URL`，以此类推。如果你只有 `OPENAI_BASE_URL` 而需要 chat completions，替换方言即可：`baseUrl.replace("/openai/v1", "/mlflow/v1")`（Mastra 示例就是这么做的）。

如需类型安全的访问，`parseEnv`（来自 `@neon/env`）返回源自你 `neon.ts` 的 `env.aiGateway`（`apiKey`、`baseUrl`）。

## 使用 Vercel AI SDK 构建智能体（推荐）

[Vercel AI SDK](https://ai-sdk.dev) 是调用网关和用 TypeScript 构建智能体的推荐方式：一套原语（`generateText`、`streamText`、工具调用、结构化输出）覆盖目录中的每个模型，为 Neon Functions 所承载的长响应智能体提供一流的流式支持。

在流式文本并生成图像的 Neon Function 上，`@ai-sdk/openai` 提供者自动从注入的环境变量读取 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`——无需客户端配置；只需选择一个目录模型：

```typescript
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

const result = streamText({
  model: openai("gpt-5-mini"),
  messages,
  tools: {
    image_generation: openai.tools.imageGeneration({
      outputFormat: "jpeg",
      size: "1024x1024",
    }),
  },
});
return result.toUIMessageStreamResponse();
```

要从单次调用中实现多提供商路由，专用的 `@neon/ai-sdk-provider` 读取 `NEON_AI_GATEWAY_BASE_URL` + `NEON_AI_GATEWAY_TOKEN` 并将每个模型路由到最佳端点（Anthropic → Messages，OpenAI/Codex → Responses，其余 → MLflow）：

```typescript
import { neon } from "@neon/ai-sdk-provider";
import { generateText } from "ai";

const { text } = await generateText({
  model: neon("claude-haiku-4-5"), // or gpt-5-3-codex, gemini-2-5-flash, ...
  prompt: "Summarize Postgres for me.",
});
```

要构建**智能体**——一个循环调用工具然后回答的模型——添加 `tools` 和 `stopWhen` 预算。循环在进程内运行，所以在 Neon Function 上不会被 lambda 式超时截断：

```typescript
import { neon } from "@neon/ai-sdk-provider";
import { generateText, tool, stepCountIs } from "ai";
import { z } from "zod";

const { text } = await generateText({
  model: neon("claude-sonnet-4-6"),
  prompt: "How many open todos do I have, and what's the oldest one?",
  tools: {
    listTodos: tool({
      description: "List the user's open todos.",
      inputSchema: z.object({}), // AI SDK v5+: `inputSchema`, not `parameters`
      execute: async () => db.select().from(todos),
    }),
  },
  stopWhen: stepCountIs(5), // let the model call tools, then summarize
});
```

关于作为 Neon Function 部署的完整 AI SDK 智能体（流式传输、工具调用、图像生成、持久化），参见 `neon-functions` 技能的 `references/ai-sdk.md`。

## 使用 Mastra 构建智能体（推荐）

[Mastra](https://mastra.ai) 是当你需要开箱即用的智能体——内置记忆、工具、工作流和追踪——同时模型仍指向网关时的推荐框架。一个有记忆支持的智能体（通过 `@mastra/pg` 在 Postgres 中存储线程/消息）作为 Neon Function 运行时，从 `parseEnv` 读取 `env.aiGateway` 并使用 **chat-completions**（MLflow）方言：

```typescript
import { Agent } from "@mastra/core/agent";
import { parseEnv } from "@neon/env";
import config from "../neon";

const env = parseEnv(config);
const gatewayUrl = env.aiGateway.baseUrl.replace("/openai/v1", "/mlflow/v1");

export const personalAssistant = new Agent({
  id: "personal-assistant",
  name: "personal-assistant",
  instructions:
    "You are a warm, concise personal assistant with long-term memory.",
  model: {
    id: `neon/claude-haiku-4-5`,
    url: gatewayUrl,
    apiKey: env.aiGateway.apiKey,
  },
  memory,
});
```

## 使用原生 SDK（更底层）

当你不需要智能体框架——只需单次补全、已有的提供商 SDK 集成，或原生提供商功能——可以用原生 SDK 调用网关。注入的 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 符合 OpenAI 标准，所以 `new OpenAI()` **零配置**即可读取它们。由于 `OPENAI_BASE_URL` 是 OpenAI **Responses** 方言（`/openai/v1`），应调用 Responses API：

```typescript
import OpenAI from "openai";

const client = new OpenAI(); // reads OPENAI_API_KEY + OPENAI_BASE_URL from the env

const res = await client.responses.create({
  model: "gpt-5-mini", // swap to claude-sonnet-4-6, gemini-2-5-flash, ...
  input: "What is Neon?",
});
```

如果要使用统一的 **chat-completions** 方言（`/mlflow/v1`），将客户端指向它。便捷的做法是在注入的 base URL 上替换方言，而非重建 URL（与 Mastra 示例相同的操作）：

```typescript
const client = new OpenAI({
  baseURL: process.env.OPENAI_BASE_URL!.replace("/openai/v1", "/mlflow/v1"),
});

const res = await client.chat.completions.create({
  model: "claude-sonnet-4-6",
  messages: [{ role: "user", content: "What is Neon?" }],
});
```

Anthropic SDK 和 google-genai 的用法相同，用于原生提供商功能——将它们指向裸网关主机上的 `/anthropic` 和 `/gemini` 路由（`${NEON_AI_GATEWAY_BASE_URL}/ai-gateway/anthropic`、`${NEON_AI_GATEWAY_BASE_URL}/ai-gateway/gemini`）。

## 模型标识符

在 `model` 字段中直接使用模型的目录 ID——例如 `claude-sonnet-4-6`、`gpt-5-mini`、`gemini-2-5-flash`。无需提供商前缀。要查询网关提供的确切标识符、每个标识符映射的底层模型，以及它们的上下文窗口、定价和能力，可使用：

- **models.dev Neon 提供商页面：https://models.dev/providers/neon** — Neon 提供商模型 ID 及其底层模型的权威、实时列表。机器可读目录位于 https://models.dev/api.json（`neon` 键）。
- **模型文档：** 参见延伸阅读。

## 可用性

AI 网关是预览（早期访问）功能，仅对 `us-east-2` 区域的新项目可用；无法在已有项目上启用。基础模型访问需要 Neon 付费计划。确认用户的项目是 `us-east-2` 的新项目。如果用户尚未获得访问权限，引导他们前往私有测试注册页面：https://neon.com/blog/were-building-backends#access

## Neon 文档

Neon 文档是权威来源，AI 网关正在快速演进，因此务必对照官方文档验证。任何文档页面可通过在 URL 后追加 `.md` 或请求 `Accept: text/markdown` 获取 markdown 格式。从文档索引（https://neon.com/docs/llms.txt）和更新日志公告中找到正确的页面。

## 延伸阅读

- https://neon.com/docs/ai-gateway/overview.md
- https://neon.com/docs/ai-gateway/get-started.md
- https://neon.com/docs/ai-gateway/models.md
- https://neon.com/docs/ai-gateway/chat-completions.md
- https://neon.com/docs/ai-gateway/anthropic-messages.md
- https://neon.com/docs/ai-gateway/openai-responses.md
- https://neon.com/docs/ai-gateway/gemini.md
- https://neon.com/docs/ai-gateway/authentication.md
- https://neon.com/docs/ai-gateway/troubleshooting.md

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时才使用此技能。
- 在执行变更前，务必对照当前官方文档验证命令、API 行为、定价、配额、凭证和部署影响。
- 不要将生成的示例替代环境特定的测试、安全审查，或用户对破坏性/高成本操作的审批。
