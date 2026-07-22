# Mastra Agent 与 Mastra Studio 可观测性

Neon Function 是一个长驻 Node.js 24 进程，这使它成为承载 [Mastra](https://mastra.ai) Agent 的天然环境：Agent 在请求生命周期内持续运行，将其模型指向 Neon AI Gateway 即无需额外的 Provider Key。你可以保持**在 Neon Functions 上运行 Agent**，同时将追踪发送到 **Mastra Studio (Mastra Cloud) 项目**实现可观测性——Agent 运行在 Neon 上，追踪在 Mastra 中查看。

形态与任何其他 Node 集成相同（参见 `references/sentry.md`）：在模块加载时实例化，用环境变量门控以便本地开发和未配置分支保持空操作，在部署时通过 `neon.ts` 传递密钥。`@mastra/core` 和 `@mastra/observability` 通过 `neon deploy` 的 esbuild 干净打包，无需额外配置。

## 1. 基于 Neon AI Gateway 定义 Agent

使用网关的 **MLflow (chat-completions) 方言**，它服务所有 Provider（OpenAI、Anthropic 等）——从注入的 `aiGateway.baseUrl` 派生（参见 `neon-ai-gateway` 技能）。`parseEnv` 从你的 `neon.ts` 读取注入的网关凭据。

```typescript
// src/mastra/agents/pricing.ts
import { Agent } from "@mastra/core/agent";
import { parseEnv } from "@neon/env";
import config from "../../../neon";

const env = parseEnv(config);
const gatewayUrl = env.aiGateway.baseUrl.replace("/openai/v1", "/mlflow/v1");

export const pricingAgent = new Agent({
  id: "pricing-analyst",
  name: "pricing-analyst",
  instructions: "You are a meticulous pricing analyst. …",
  model: { id: "neon/gpt-5-mini", url: gatewayUrl, apiKey: env.aiGateway.apiKey },
});
```

## 2. 将可观测性接入 Mastra Studio

`MastraPlatformExporter`（来自 `@mastra/observability`）将追踪发送到 Mastra Studio 项目。它从环境读取 `MASTRA_PLATFORM_ACCESS_TOKEN` 和 `MASTRA_PROJECT_ID`。

注意：`Observability` 需要至少一个导出器——传入空 `exporters` 数组会抛 `OBSERVABILITY_INVALID_INSTANCE_CONFIG`。因此在平台凭据就绪前完全省略 `observability` 选项，让应用在 Mastra 项目创建前（及本地开发时）也能运行。

```typescript
// src/mastra/index.ts
import { Mastra } from "@mastra/core/mastra";
import { Observability, MastraPlatformExporter } from "@mastra/observability";
import { pricingAgent } from "./agents/pricing";

const platformReady = Boolean(
  process.env.MASTRA_PLATFORM_ACCESS_TOKEN && process.env.MASTRA_PROJECT_ID,
);

const observability = platformReady
  ? new Observability({
      configs: {
        default: { serviceName: "my-app", exporters: [new MastraPlatformExporter()] },
      },
    })
  : undefined;

export const mastra = new Mastra({
  agents: { pricingAgent },
  ...(observability ? { observability } : {}),
});
```

Agent 必须注册到 `Mastra` 实例（`agents` 映射）中，其 `.generate()` / `.stream()` 调用才会被追踪。通过 `mastra.getAgent("pricingAgent")` 调用它们。

## 3. 通过网关进行结构化输出

网关不强制**原生**结构化输出，所以裸 `structuredOutput: { schema }` 可能返回缺少字段的结果（如嵌套 `meta` 对象），导致 Zod 验证失败。设置 `jsonPromptInjection: true` 使 Mastra 将 schema 注入提示词，模型返回完整形状：

```typescript
const agent = mastra.getAgent("pricingAgent");
const result = await agent.generate(prompt, {
  structuredOutput: { schema: myZodSchema, jsonPromptInjection: true },
  abortSignal: AbortSignal.timeout(70_000), // 限制每次尝试；网关有上游超时
});
const data = result.object; // 经 myZodSchema 验证
```

为增强容错，可在不同模型上注册第二个 Agent（如 `neon/claude-haiku-4-5`）并在主尝试抛出异常时回退——同样的 Provider 回退模式可用，因为两者都可通过 MLflow 方言访问。

## 4. 用 CLI 创建 Mastra 项目和 token

安装 Mastra CLI（`npm i -g mastra`）并认证。项目/token 创建需要**实时登录会话**：

```bash
mastra auth login        # 打开浏览器；在以下步骤之前必须完成
mastra auth whoami       # 显示你的用户 + 组织 ID（org_…）
```

- **Access token（非交互式）：** `mastra auth tokens create <name>` 输出一次性密钥（`sk_…`）。这就是你的 `MASTRA_PLATFORM_ACCESS_TOKEN`。
- **项目：** 交互式的 `mastra studio projects create` TUI 难以脚本化。替代方案：作为 Studio 部署的一部分注册项目，用 `-y` 实现非交互式并将项目 ID 写入 `.mastra-project.json`：

```bash
mastra studio deploy --org org_xxx --project my-app -y
# → .mastra-project.json: { "projectId": "…", "projectName": "my-app", "organizationId": "org_…" }
```

将该 `projectId` 作为 `MASTRA_PROJECT_ID` 使用。

两个注意事项：

- **不要在环境变量中设置 `MASTRA_API_TOKEN` 用于项目/部署命令**——它会让 CLI 报告 `No organizations found`。依赖交互式登录会话。
- 如果你有多个 env 文件（如 `.env.deploy` 和 `.env.local`），`studio deploy` 会报 `Multiple env files found`；传 `--env-file <file>` 来消除歧义。

## 5. 通过 `neon.ts` 传递凭据（第三方环境变量）

Neon 注入的变量（`DATABASE_URL`、`OPENAI_*`、AI Gateway）是自动的。只在函数的 `env` 下声明第三方变量，从 `process.env` 在部署时解析：

```typescript
// neon.ts
functions: {
  myapp: {
    name: "my app",
    source: "src/index.ts",
    env: {
      MASTRA_PROJECT_ID: process.env.MASTRA_PROJECT_ID ?? "",
      MASTRA_PLATFORM_ACCESS_TOKEN: process.env.MASTRA_PLATFORM_ACCESS_TOKEN ?? "",
    },
  },
}
```

在部署时从 git-ignored 文件加载值：

```bash
neon deploy --env .env.deploy
```

## 6. 验证

发送一个触发 Agent 的请求，然后打开 Mastra Studio 项目的 **Observability / Traces** 视图——你会看到 Agent 运行（模型调用、延迟、token 用量）在你配置的 `serviceName` 下。仅导出 `SPAN_ENDED` 事件，定期缓冲刷新，所以追踪在 Agent 运行完成后几秒内出现。

## 延伸阅读

- https://mastra.ai/docs/observability/tracing/exporters/cloud
- https://mastra.ai/reference/observability/tracing/exporters/mastra-platform-exporter
- https://mastra.ai/docs/agents/structured-output
- Neon AI Gateway 方言：`neon-ai-gateway` 技能
