# Neon Functions 上的 MCP 服务器

[Model Context Protocol](https://modelcontextprotocol.io) 服务器是教科书级的 Neon Functions 工作负载：它是一个长运行 HTTP 处理器，供 AI 客户端（Cursor、Claude、ChatGPT、Agent）调用来发现和调用工具，而这些工具通常需要读写数据库。作为 Neon Function 运行 MCP 服务器使其计算紧邻 Postgres 数据、获得公开 HTTPS URL、并可与后端其余部分一起分支——每个分支拥有自己的 MCP 服务器，针对自己独立的数据。

MCP 的**可流式 HTTP 传输**是单个端点上的普通 `POST`/`GET`（约定为 `/mcp`），因此直接映射到函数的 Web 标准 `fetch` 处理器——无需 [WebSocket](../SKILL.md#websocket-服务器) 的 `upgrade` 方法或额外协议。Hono 应用是最简单的宿主。

## 服务器

两个包完成工作：官方 [`@modelcontextprotocol/sdk`](https://github.com/modelcontextprotocol/typescript-sdk)（定义服务器及其工具）和 [`@hono/mcp`](https://github.com/honojs/middleware/tree/main/packages/mcp)（将 MCP 的可流式 HTTP 传输桥接到 Hono 路由）。工具通过 Drizzle 在模块作用域 `pg` 连接池上查询 Postgres，与任何其他函数相同（见 [连接 Postgres](../SKILL.md#连接-postgres)）。

```typescript
// src/index.ts
import { Hono } from "hono";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import { eq } from "drizzle-orm";
import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPTransport } from "@hono/mcp";
import { contacts } from "./db/schema";

// 每个 isolate 一个连接池，跨请求复用
const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 5 });
const db = drizzle(pool);

const mcpServer = new McpServer({ name: "contacts", version: "1.0.0" });

// 每个工具：名称、配置（描述 + Zod 输入 schema）、返回 MCP 内容的处理器
// Zod 形状变为工具的 JSON schema，供客户端正确调用
mcpServer.registerTool(
  "create_contact",
  {
    title: "Create contact",
    description: "Create a new contact.",
    inputSchema: {
      name: z.string().describe("Full name (required)."),
      email: z.string().optional().describe("Email address."),
    },
  },
  async ({ name, email }) => {
    const [row] = await db.insert(contacts).values({ name, email }).returning();
    return { content: [{ type: "text", text: JSON.stringify(row) }] };
  },
);

mcpServer.registerTool(
  "delete_contact",
  {
    title: "Delete contact",
    description: "Delete a contact by id.",
    inputSchema: { id: z.number().int().positive() },
  },
  async ({ id }) => {
    const [row] = await db.delete(contacts).where(eq(contacts.id, id)).returning();
    return { content: [{ type: "text", text: JSON.stringify(row ?? { error: "not found" }) }] };
  },
);

// 每个 isolate 连接一次传输层，然后由 Hono 路由
// 将每个 /mcp 请求（POST 调用、GET 流）交给传输层
const transport = new StreamableHTTPTransport();
const app = new Hono();

app.all("/mcp", async (c) => {
  if (!mcpServer.isConnected()) await mcpServer.connect(transport);
  return transport.handleRequest(c);
});

export default app;
```

要点：

- **模块作用域。** 在模块加载时一次性构建 `McpServer`、注册其工具、创建 `StreamableHTTPTransport` 并打开 `pg` 连接池——它们在 isolate 提供的每个请求间复用（见 [运行时限制](../SKILL.md#超时与运行时限制)）。用 `isConnected()` 守卫惰性连接传输层，确保只连接一次。
- **状态在 Postgres 中。** 模块内存不能幸免于 isolate 驱逐，且多个 isolate 并行运行——所以工具读写的任何数据的真实来源应在 Postgres 中，而非内存结构。
- **URL。** `neon deploy` 后，服务器位于 `https://<branch_id>-<slug>.compute.…neon.tech/mcp`。将任何可流式 HTTP MCP 客户端指向该 `/mcp` 路径。

## 服务器认证

> [!WARNING]
> Neon Function 有一个**公开的 HTTPS URL——任何人都能访问它。** 未认证的 MCP 服务器等于将你的工具（及其背后的数据库）交给每个调用者。在接触传输层之前在处理器顶部进行认证，方式与[任何面向客户端的函数](../SKILL.md#functions-作为-agent-后端-nextjs-及类似框架)相同。

[Better Auth](https://better-auth.com)（可自托管，与应用一起运行）是一个好选择，它覆盖两种常见形态。**Better Auth 发展迅速**——MCP 插件正从 `better-auth/plugins` 迁移到独立的 `@better-auth/mcp` 包（基于 OAuth Provider 插件构建），这会将 `withMcpAuth` → `requireMcpAuth`、`createMcpAuthClient` → `createMcpResourceClient` 重命名。在接线前对照 [Better Auth MCP 文档](https://better-auth.com/docs/plugins/mcp)验证当前的包名和导入路径。

### 选项 1 — 通过 Better Auth MCP 插件进行 OAuth（最适合第三方客户端）

[MCP 插件](https://better-auth.com/docs/plugins/mcp)使你的 **Better Auth 应用成为 MCP 的 OAuth 授权服务器**，端到端实现 MCP 授权规范：发现（`/.well-known/oauth-authorization-server`、`/.well-known/oauth-protected-resource`）、动态客户端注册、同意/token 流程。支持 OAuth 的 MCP 客户端（Cursor、Claude、ChatGPT）随后让用户登录并获取 token，无需复制 API Key。

你的 Neon Function 是**资源服务器**——与 Better Auth 应用是独立服务，不共享进程。使用 Better Auth 的**远程 MCP 客户端**对照认证服务器发布的 JWKS 验证传入的 Bearer token，并提供受保护资源元数据让客户端发现认证位置：

```typescript
// src/index.ts（草图）— 对照远程 Better Auth 服务器验证 bearer token。
// 导入路径/名称取决于你的 Better Auth 版本（better-auth/plugins/mcp/client 中的
// createMcpAuthClient，或 @better-auth/mcp/client 中的 createMcpResourceClient）— 查阅文档。
import { createMcpAuthClient } from "better-auth/plugins/mcp/client";

const mcpAuth = createMcpAuthClient({ authURL: process.env.AUTH_URL }); // 你的 Better Auth 基础 URL

app.all("/mcp", async (c) => {
  const session = await mcpAuth.verify?.(c.req.raw); // 通过远程 JWKS 验证 Bearer token
  if (!session) {
    // 告知客户端去哪里认证（RFC 9728 / MCP 规范）
    return c.json({ error: "unauthorized" }, 401, {
      "WWW-Authenticate": `Bearer resource_metadata="${process.env.AUTH_URL}/.well-known/oauth-protected-resource"`,
    });
  }
  if (!mcpServer.isConnected()) await mcpServer.connect(transport);
  return transport.handleRequest(c); // 将工具限定到 session.userId
});
```

通过函数 `neon.ts` 中的 `env` 传递 `AUTH_URL`（及任何签名/JWKS 配置）（见[环境变量](../SKILL.md#环境变量)）。因为函数只对照远程服务器验证 token，Better Auth 实例可以运行在任何地方——通常是你在 Vercel 上的 Next.js / 应用宿主。

### 选项 2 — 通过自托管 Better Auth 的 API Key 或 Session JWT（最简单）

当调用方是你自己的 Agent/服务或个人 MCP 服务器时，不需要完整的 OAuth 流程。运行自托管的 Better Auth，然后：

- **API Key** — 启用 Better Auth 的 [API Key 插件](https://better-auth.com/docs/plugins/api-key)，签发一个 key，函数在每个请求上验证 `Authorization: Bearer <key>`（或 `x-api-key` 请求头）；或
- **Session JWT** — 用 Better Auth 的 `jwt` 插件生成短期 JWT，在函数中对照应用的 JWKS 验证，与 [Agent 后端](../SKILL.md#functions-作为-agent-后端-nextjs-及类似-frameworks)相同的 `jose` 模式。

无论哪种方式，都是 `/mcp` 路由顶部的一次检查——拒绝不带有效 key/token 的任何请求后再连接传输层：

```typescript
app.all("/mcp", async (c) => {
  const auth = c.req.header("authorization");
  if (!(await isValidApiKey(auth))) return c.json({ error: "unauthorized" }, 401); // 你的检查
  if (!mcpServer.isConnected()) await mcpServer.connect(transport);
  return transport.handleRequest(c);
});
```

这使密钥保持在服务端，运行零成本，轮换也很简单——在你需要第三方客户端自授权前，这是一个可靠的默认选择，到那时就切换到选项 1。

## 测试

用任何 MCP 客户端驱动服务器。[`mcporter`](https://github.com/instructa/mcporter) 是一个快捷 CLI——`mcporter list <url>/mcp --schema` 列出工具，`mcporter call "<url>/mcp.<tool>" key=value` 调用工具（本地 `neon dev` URL 加 `--allow-http`）。要交互式接入客户端，`npx add-mcp <url>/mcp -a <agent>` 会为你编写客户端配置。
