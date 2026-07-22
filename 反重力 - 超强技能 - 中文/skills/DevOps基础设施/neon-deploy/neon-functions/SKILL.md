---
name: neon-functions
description: 长运行、无服务器 Node.js HTTP 函数，部署在你的 Neon 分支上，DATABASE_URL 自动注入，计算资源紧邻你的数据运行。当用户想要托管 API、具有长流式响应的 AI Agent、WebSocket 或服务器推送事件（SSE）时使用。
risk: unknown
source: https://github.com/neondatabase/agent-skills/tree/main/skills/neon-functions
source_repo: neondatabase/agent-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/neondatabase/agent-skills/blob/main/LICENSE
---

# Neon Functions

这是一个预览功能，目前仅在 `us-east-2` 可用。Neon Functions 是部署在 Neon 分支上的长运行 Node.js HTTP 处理器。每个函数拥有一个公开的 HTTPS URL，与数据库在同一区域运行——如果分支启用了 Postgres，`DATABASE_URL` 会自动注入。你通过已有的 Neon CLI（`neon.ts`）和 API 来部署和管理它们。

使用此技能帮助用户定义、本地运行、部署和管理紧邻其数据库的函数。交付一个已部署的函数及其调用 URL、一个可用的本地 `neon dev` 循环，或者来自官方 Neon 文档的精确答案。

## 适用场景

当工作负载是一个能从保持存活和靠近数据中受益的请求/响应处理器时，使用 Neon Functions：

- **超出 Lambda 风格执行时限的长运行请求/响应流。** 每个请求需要多次 LLM 调用和工具调用的 Agent，或图像/视频生成，通常会突破传统无服务器函数约 10–60 秒的执行上限和短暂的流式窗口。Neon Functions 是长运行的：处理器只需在 15 分钟内**开始**响应，只要有字节持续流动，打开的流就能保持存活。这为真实的 Agent 工作负载留出了足够的余量。
- **无需外挂 Redis 的有状态流。** 因为函数在请求之间保持存活，它可以托管 SSE 端点或 WebSocket 服务器并在进程内保持连接打开——不需要外部状态存储（Redis 等）来维持流的连贯性。模块作用域状态（如 `pg` 连接池、内存计数器）在同一 isolate 的跨请求间持久化。
- **必须紧邻 Postgres 的计算资源。** 函数与分支数据库在同一区域运行，因此每次查询没有跨区域往返。`DATABASE_URL` 会自动为你注入。
- **随数据分支的后端。** 每个分支以自己的 URL 运行自己版本的函数，针对自己独立的数据库（以及存储和网关）状态。预览部署、CI 和开发环境各自获得独立的后端——向子分支部署永远不会影响父分支。
- **Webhook、Bot 和响应后工作。** 扩散为多次数据库写入的 Webhook 处理器、Discord/WebSocket Bot，以及通过 `waitUntil` 触发的"发后不管"后续操作（分析日志、审计日志），都适用。

如果工作负载是纯静态站点、需要自身生命周期的 cron/后台任务，或当前必须在 `us-east-2` 以外运行，那么它还不是合适的工具（见下方的"超时与可用性"）。

## 功能概要

- **长运行 & 无服务器** — 为 WebSocket 服务器（见 [WebSocket 服务器](#websocket-服务器)）、SSE 端点（见 [服务器推送事件 (SSE)](#服务器推送事件-sse)）、长运行 Agent HTTP 流和 API 构建。空闲时仍可缩容至零。
- **Web 标准处理器** — 函数是任何导出 `fetch(request)` 方法并返回 `Response` 的默认导出（兼容 Workers/WinterTC）。Hono 应用正好导出这种形态，所以 `export default app` 直接可用。运行于 Node.js 24，所有 Node API 均可用。
- **紧邻数据库** — 在分支区域运行；分支启用 Postgres 时自动注入 `DATABASE_URL`。
- **可分支** — 每个分支以自己的 URL 运行自己的函数版本，针对自己独立的状态。
- **同一 CLI/API** — 通过 `neon`、`neon.ts` 或 Neon API 进行部署和管理。

## 架构定位：Functions 在哪里

Neon（含 Functions）是**后端原语，而非全栈应用托管**。将应用托管在 **Vercel**（或 Netlify、或其他前端/应用托管平台）；Functions 是你后端中紧邻数据的那部分长运行、有状态的切片。它与宿主平台以两种方式组合：

- **给全栈应用添加 Function。** 你在 Vercel（或 Netlify）上的 Next.js / TanStack Start 应用负责 UI、认证（如 Neon Auth），并直接与 Neon Postgres 和 Object Storage 对话。当某个工作负载超出宿主的短无服务器限制——WebSocket 或 SSE 服务器、或会超时的长运行 Agent——就把那一块移到 Neon Function 上。（见 [Functions 作为 Agent 后端](#functions-作为-agent-后端-nextjs-及类似框架) 了解客户端直连模式。）
- **在 Functions 上运行整个后端控制平面。** 尤其是前端是**纯客户端**的情况——TanStack Router、React Router 客户端模式、以及托管在 Vercel 或 Netlify 上的类似 SPA——客户端**直接**调用 Functions。构建 REST API 和请求/响应 Agent，托管 **MCP 服务器**，运行任何有状态的或属于 Postgres / Object Storage 紧邻的计算任务。

无论哪种方式，都像保护任何独立 REST API 那样保护 Function：在处理器顶部验证 JWT 或 API 密钥（见 [Functions 作为 Agent 后端](#functions-作为-agent-后端-nextjs-及类似框架) 中的 WARNING）。因为 Function 就是你的后端，你可以在**宿主和 Neon 之间迁移组件**——当 Agent 或有状态的 WebSocket 服务器需要更多运行时时移到 Function 上，需要时再移回来。

## 初始化

函数在 `neon.ts` 中声明（参见 `neon` 技能了解分支优先工作流和 `neon.ts` 基础知识）。添加 `@neon/config` 并在 `preview.functions` 下声明函数，以 **slug** 为键：

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  preview: {
    functions: {
      todos: {
        // slug: ^[a-z0-9]{1,20}$ — 仅小写字母/数字，不含连字符
        name: "todo api", // 仅用于显示的标签
        source: "src/index.ts", // 入口文件，相对于 neon.ts
      },
    },
  },
});
```

slug 是函数的永久标识符（出现在调用 URL 和 CLI 命令中），首次部署后不可更改。用 `name` 作为人类可读标签。

一个最小化的函数——一个通过注入的 `DATABASE_URL` 查询分支 Postgres 的 Hono 应用：

```typescript
// src/index.ts
import { Hono } from "hono";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import { parseEnv } from "@neon/env";
import config from "../neon";
import { todos } from "./db/schema";

const env = parseEnv(config);
const pool = new Pool({ connectionString: env.postgres.databaseUrl, max: 5 });
const db = drizzle(pool);

const app = new Hono();
app.get("/", (c) => c.text("Neon + Hono + Drizzle"));
app.post("/todos", async (c) => {
  const { text } = await c.req.json<{ text: string }>();
  const [row] = await db.insert(todos).values({ text }).returning();
  return c.json(row, 201);
});
app.get("/todos", async (c) => c.json(await db.select().from(todos)));

export default app;
```

在模块作用域创建 `pg` 连接池（同一 isolate 上的跨请求复用），并将 `max` 设小（例如 5），因为每个 isolate 维护自己的连接池。

`parseEnv(config)` 需要 config 所隐含的**每一个**环境变量。一个只通过连接池 URL 与 Postgres 通信的函数可以将其范围限定到仅该键——`parseEnv` 随后会验证并只返回你所要求的内容（键名从你的 `neon.ts` 自动补全）：

```typescript
const { postgres } = parseEnv(config, ["DATABASE_URL"]); // 不是非连接池 URL、auth 等
const pool = new Pool({ connectionString: postgres.databaseUrl, max: 5 });
```

## 本地开发与部署

```bash
neon dev      # 启动 neon.ts 中每个函数并支持热重载；注入 DATABASE_URL 及相关变量
neon deploy   # 用 esbuild 打包、上传，将 neon.ts 应用到关联分支
```

不使用 `neon.ts` 部署单个函数：`neon functions deploy <slug> --path . --entry src/index.ts`。用 `neon functions get <slug>` 获取公开 URL（`invocation_url` 字段，格式为 `https://<branch_id>-<slug>.compute.c-1.us-east-2.aws.neon.tech`）。用 `neon functions list|get|delete` 进行管理。

当 `neon checkout`**创建**新分支且存在 `neon.ts` 时，它会自动应用策略——将函数部署到新分支。检出已有分支不会重新部署；需显式运行 `neon deploy`。

## Neon 即代码 (`neon.ts`)

[初始化](#初始化) 中的 `preview.functions` 块是 `neon.ts` 的一部分，Neon 的即代码文件——一个 TypeScript 文件声明了每个函数（其 `source`、显示 `name`、和 `env`）以及其他分支服务，全部纳入版本控制（参见 `neon` 技能获取完整参考）。把它当作分支的 Terraform 来对待：

```bash
neon config status   # 输出分支的实时配置（已部署的函数）
neon config plan     # 预览 apply 会变更的内容的差异
neon config apply    # 打包 + 部署已声明的函数  （neon deploy 是别名）
```

函数是**分支作用域**的：每个分支在自己的 URL 上运行自己的部署。当 `neon.ts` 存在时，`neon checkout` 在**创建**分支时自动应用策略，所以新的预览/CI 分支启动时函数已经部署完毕。检出一个**已有**分支不会重新部署——运行 `neon deploy` 来应用变更。

按分支调整部署参数（如 `runtime`）位于 `branch` 闭包中以 slug 为键，这样不同分支可以有不同的配置而不改变哪些函数存在：

```typescript
export default defineConfig({
  preview: {
    functions: { todos: { name: "todo api", source: "src/index.ts" } },
  },
  branch: (branch) => ({
    preview: { functions: { todos: { runtime: "nodejs24" } } },
  }),
});
```

## 环境变量

Neon 在运行时注入分支作用域连接字符串和服务 URL——你不需要声明它们或在部署时传入：

| 变量 | 说明 |
| --- | --- |
| `NEON_BRANCH` | 分支**名称**（如 `main`、`preview/foo`）。在每个分支上注入，包括默认分支。 |
| `DATABASE_URL` | 连接池连接字符串。用于大多数查询。仅当分支启用 Postgres 时存在。 |
| `DATABASE_URL_UNPOOLED` | 直连连接字符串。用于迁移、`LISTEN`/`NOTIFY`、多轮事务。 |
| `NEON_AUTH_BASE_URL` | 当分支启用 Neon Auth 时存在。 |
| `NEON_DATA_API_URL` | 当分支启用 Data API 时存在。 |

对象存储（`AWS_*`）和 AI Gateway（`OPENAI_*`、`NEON_AI_GATEWAY_*`）变量在相应服务被声明时也会注入——参见 `neon-object-storage` 和 `neon-ai-gateway` 技能。

`neon env pull` / `neon-env run` / `neon dev` 也会将 `NEON_BRANCH`（及连接字符串）输出到本地开发环境，使本地运行镜像部署时的运行时。

**你自己的密钥**是每次部署级别的。通过 `neon functions deploy` 的 `--env KEY=VALUE` 设置（可重复；`--env KEY=` 删除一个键，未提及的键保留），或在 `neon.ts` 中函数的 `env` 下声明（部署时解析，因此从 `process.env` 读取以避免硬编码）：

```typescript
functions: {
  todos: {
    name: "todo api",
    source: "src/index.ts",
    env: { OPENAI_API_KEY: process.env.OPENAI_API_KEY! },
  },
}
```

部署前加载 `.env` 文件：`neon deploy --env .env.production`。用 `neon env pull` 将分支的 Neon 管理变量拉取到磁盘供本地开发使用（`link`/`checkout` 会自动执行；传 `--no-env-pull` 跳过并用 `neon-env run -- <cmd>` 进行运行时注入）。限制：≤1,000 个变量，总计 ≤64 KiB，`NEON_` 前缀保留。

## 连接 Postgres

当分支启用 Postgres 时，Neon**在运行时注入连接字符串**——你不需要声明它们、在部署时传入或硬编码任何内容。你会用到的两个：

- `DATABASE_URL` — **连接池**连接字符串（经 Neon 的连接池路由）。用于普通请求/响应查询流量。不加前缀是因为每个 Postgres ORM（Drizzle、Prisma、Knex 等）默认读取 `DATABASE_URL`。
- `DATABASE_URL_UNPOOLED` — 到同一个数据库的**直连**连接字符串。用于迁移、`LISTEN`/`NOTIFY` 和长事务。

**查询和 schema 管理请在 node-postgres（`pg`）之上使用 Drizzle（或其他 ORM）**，不要用 Neon 的无服务器驱动。函数是长运行的，在多个请求间复用 isolate，所以持久的 `pg` 连接池才是正确的选择；无服务器驱动的 HTTP 传输是完全隔离、Lambda 风格运行时用的。

在**模块作用域创建一次**连接池并在请求间复用——不要每请求打开一个连接：

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

// 每个 isolate 创建一次；由该 isolate 处理的每个请求复用。
const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 5 });
const db = drizzle(pool);
```

**推荐使用连接池，因为 isolate 在多个请求间被复用**（且多个请求可能同时在同一 isolate 上飞行——见 [超时与运行时限制](#超时与运行时限制)）。模块作用域连接池在冷启动时打开一次，之后由该 isolate 提供服务的每个后续请求共享，因此你可以摊薄连接建立开销而不是每次请求都支付，同时避免在高负载下耗尽 Postgres 连接。

将 `max` 保持较小（如 `5`）：每个 isolate 维护自己的连接池，所以到 Postgres 的总连接数随存活的 isolate 数量伸缩。关闭时无需手动关闭连接池——当运行时驱逐 isolate 时发送 `SIGINT`/`SIGTERM`，Neon 的连接池器会回收这些连接，因此显式的 drain handler 是多余的。

> 直接读取 `process.env.DATABASE_URL` 在各处都可行。[初始化](#初始化) 中的函数改用 `@neon/env` 的 `parseEnv(config)` 来以类型安全、经过验证的方式读取同样的值——两种都可以。

## WebSocket 服务器

WebSocket 服务器是最典型的 Functions 工作负载：一个长运行的处理器在进程内保持连接打开，无需外部状态存储即可保持流连贯性。因为函数是一个真正的 Node.js 进程（不是 Lambda），WebSocket 握手的工作方式和任何 Node 服务器一样——[`ws`](https://github.com/websockets/ws) 库升级套接字，只要字节流动连接就保持存活（15 分钟心跳，见 [超时](#超时与运行时限制)）。

**返回签名是关键所在。** 函数的正常默认导出是 `{ fetch }`。若同时接受 WebSocket，则额外导出 `upgrade` 方法——运行时将普通 HTTP 路由到 `fetch`，将 WebSocket 握手路由到 `upgrade`：

```typescript
export default {
  fetch(request: Request): Response | Promise<Response> { /* HTTP */ },
  async upgrade(req: IncomingMessage, socket: Duplex, head: Buffer) { /* WS 握手 */ },
};
```

**简单示例** — 原生 `ws`，不用框架，带认证。浏览器无法在 WebSocket 上设置请求头，所以在接受连接前用 `?token=` 查询参数进行认证（验证方式同 [Agent 后端](#functions-作为-agent-后端-nextjs-及类似框架)：用 `jwtVerify` 对照你的 JWKS 验证）：

```typescript
// src/index.ts
import type { IncomingMessage } from "node:http";
import type { Duplex } from "node:stream";
import { WebSocketServer, type WebSocket } from "ws";

const clients = new Set<WebSocket>();
const wss = new WebSocketServer({ noServer: true });

export default {
  // 普通 HTTP（健康检查、REST）由 fetch 处理。
  fetch: () => new Response("WebSocket endpoint — connect with ?token=<jwt>"),

  // 运行时将 WebSocket 握手交给 upgrade()。
  async upgrade(req: IncomingMessage, socket: Duplex, head: Buffer) {
    const url = new URL(req.url ?? "/", "http://localhost");
    const identity = await verifyToken(url.searchParams.get("token")); // 无效则拒绝
    if (!identity) {
      socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
      socket.destroy();
      return;
    }
    wss.handleUpgrade(req, socket, head, (ws) => {
      clients.add(ws);
      ws.on("close", () => clients.delete(ws));
      ws.on("message", (data) => broadcast(data.toString())); // 见下方广播部分
    });
  },
};
```

**Hono 变体。** 如果你只在 HTTP 侧使用 Hono 并愿意自行驱动 `ws`，只需把简单示例中的 `fetch` 替换为 `app.fetch` 并保留原生 `upgrade`——Hono 负责路由/中间件，`ws` 负责套接字。

如果你想在 Hono 应用**内部**声明 WebSocket 路由——`app.get("/ws", upgradeWebSocket(...))` 配合标准的 `onOpen`/`onMessage`/`onClose` 生命周期——你需要一个适配器来桥接 Hono 的 `upgradeWebSocket()` 辅助方法和 Neon 的 `upgrade(req, socket, head)`。Hono 附带了 Cloudflare/Deno/Bun/Node 的适配器，但**没有 Neon 的**，而 Node 适配器（`@hono/node-ws`）已被废弃且假定自己拥有 HTTP 服务器。[references/hono-websockets.md](references/hono-websockets.md) 中有一个小型自包含的 `createNeonWebSocket(app)` 适配器可供复制——它只依赖 `hono` 和 `ws`（无废弃包；改编自 `@hono/node-ws`，MIT 协议），返回可直接导出的 `{ fetch, upgrade }` 处理器。用法是地道的 Hono 写法，且由于握手经由 `app.request` 路由，**认证就是普通路由中间件**：

```typescript
// src/index.ts
import { Hono } from "hono";
import { createNeonWebSocket } from "./hono-ws";

const app = new Hono();
const { upgradeWebSocket, handler } = createNeonWebSocket(app);

app.get(
  "/ws",
  async (c, next) => {
    if (!(await verifyToken(c.req.query("token")))) return c.text("Unauthorized", 401);
    await next();
  },
  upgradeWebSocket(() => ({
    onOpen: (_evt, ws) => ws.send("welcome"),
    onMessage: (evt, ws) => ws.send(`echo: ${evt.data}`),
    onClose: () => console.log("disconnected"),
  })),
);

export default handler; // Neon 的 { fetch, upgrade } 契约
```

> 不要在 `upgradeWebSocket` 路由上放置修改请求头的中间件（如 CORS）——辅助方法内部重写请求头且会抛异常。下方关于 [广播](#跨-isolate-广播-不要跳过本节)和 [客户端重连](#客户端必须重新连接) 的指引同样适用。

### 心跳（保持套接字存活）

连接保持打开**仅在有字节流动时**：Neon 在 15 分钟后驱逐静默流（见 [超时与运行时限制](#超时与运行时限制)），而中间代理/负载均衡器通常严格得多（通常几十秒）。不要依赖应用自身足够活跃——定期从服务端发送 ping 使套接字永不静默。`ws.ping()` 发送一个 WebSocket ping 帧，浏览器自动回复 pong，因此无需编写客户端代码：

```typescript
const HEARTBEAT_MS = 25_000; // 远低于代理空闲超时

const beat = setInterval(() => {
  for (const ws of clients) if (ws.readyState === ws.OPEN) ws.ping();
}, HEARTBEAT_MS);
beat.unref?.();
```

（使用 Hono 的 `upgradeWebSocket` 辅助方法时不持有原始套接字，因此改为发送应用级保活消息——例如以相同间隔发送 `ws.send("ping")`，客户端会忽略它。）

### 跨 isolate 广播（不要跳过本节）

在高负载下运行时会并行运行**多个 isolate，每个都有自己的一份模块状态副本**——所以每个 isolate 都有自己的 `clients` 集合。仅向本地集合广播意味着连接到 isolate A 的客户端永远看不到 isolate B 上客户端发送的消息。聊天会静默分裂。

使用 **Postgres `LISTEN`/`NOTIFY`** 跨每个 isolate 广播：每个 isolate 通过一条专用的**非连接池**连接在频道上执行 `LISTEN`，广播即 `NOTIFY`（所以每个 isolate，包括发送方的，都会重新广播到自己的套接字）。这也是为什么消息状态必须存储在 Postgres 中而非模块内存中——模块状态不能幸免于驱逐。

```typescript
import { Pool, Client } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 5 });
const CHANNEL = "chat_events";

// 每个 isolate 一条专用的直连连接，仅用于接收事件。
// 使用 DATABASE_URL_UNPOOLED —— LISTEN 需要真实会话，不是连接池连接。
const listener = new Client({ connectionString: process.env.DATABASE_URL_UNPOOLED });
listener.connect().then(() => listener.query(`LISTEN ${CHANNEL}`));
listener.on("notification", (msg) => {
  if (!msg.payload) return;
  for (const ws of clients) if (ws.readyState === ws.OPEN) ws.send(msg.payload);
});

// 通过连接池 NOTIFY 广播 —— 每个 isolate 的监听器都会触发。
function broadcast(event: unknown) {
  return pool.query("SELECT pg_notify($1, $2)", [CHANNEL, JSON.stringify(event)]);
}
```

### 客户端必须重新连接

空闲函数会被驱逐（isolate 因运营原因也会重启），所以客户端套接字**必定**会断开——把重连视为常态，而非异常情况。使用指数退避重连（设上限），并且**每次尝试都生成新的 token**（token 有效期短，过期的会在 `upgrade` 认证检查中失败）：

```typescript
let closed = false, retry = 0, timer: ReturnType<typeof setTimeout>;

async function connect() {
  if (closed) return;
  const token = await getToken(); // 每次尝试重新生成；短期有效
  const ws = new WebSocket(`${WS_URL}?token=${encodeURIComponent(token)}`);
  ws.onopen = () => { retry = 0; };          // 成功时重置退避
  ws.onmessage = (e) => { /* 处理事件 */ };
  ws.onclose = () => {
    if (!closed) timer = setTimeout(connect, Math.min(1000 * 2 ** retry++, 15000));
  };
  ws.onerror = () => ws.close();             // 让 onclose 驱动重试逻辑
}
connect();
```

综合起来——Hono `fetch` + `ws` `upgrade`、通过 `?token=` 进行的 JWT 认证、`LISTEN`/`NOTIFY` 广播、客户端退避——这些组合成单函数上的完整实时聊天后端。

## 服务器推送事件 (SSE)

当你只需要**服务器 → 客户端**单向流式传输（实时计数器、通知、进度、token 流）时，SSE 比 WebSocket 更简单，不需要 `upgrade` 方法或额外的库：普通的 `fetch` 处理器返回一个 `Response`，其 body 为 `Content-Type: text/event-stream` 的 `ReadableStream`，只要字节流动运行时就保持打开。浏览器用 `EventSource` 消费它，后者**自动重连**——因此无需编写客户端退避逻辑。

```typescript
// src/index.ts — 最小化 SSE 端点
const encoder = new TextEncoder();
export default {
  fetch: () =>
    new Response(
      new ReadableStream<Uint8Array>({
        start(controller) {
          controller.enqueue(encoder.encode("data: hello\n\n"));
          const t = setInterval(() => controller.enqueue(encoder.encode(": ping\n\n")), 25_000);
          return () => clearInterval(t); // 客户端断开时触发
        },
      }),
      { headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache, no-transform" } },
    ),
};
```

与 WebSocket 相同的规则适用。**心跳**：流只在有字节流动时保持打开——Neon 的窗口为 15 分钟（见 [超时与运行时限制](#超时与运行时限制)），但代理通常更严格，所以大约每 25–30 秒发出一个 `: ping\n\n` 注释（如上所示）以防空闲流被丢弃。状态存储在 Postgres 中，用 [`LISTEN`/`NOTIFY`](#跨-isolate-广播-不要跳过本节) 跨 isolate 广播（维护一组 stream controller 并对每个 `enqueue`）。`EventSource` 只支持 GET 且无法设置请求头，因此用 `?token=` 查询参数或 cookie 认证，方式与 WebSocket 完全相同。[references/sse.md](references/sse.md) 包含完整模式——Hono 变体、跨 isolate 广播、线路格式、客户端和注意事项。

## MCP 服务器

[MCP](https://modelcontextprotocol.io) 服务器是天然的 Functions 工作负载：一个长运行 HTTP 处理器，向 AI 客户端（Cursor、Claude、ChatGPT、Agent）暴露工具，这些工具读写分支的 Postgres 数据库就在计算旁边。MCP 的**可流式 HTTP 传输**是单个端点上普通的 `POST`/`GET`（约定为 `/mcp`），所以直接映射到函数的 `fetch` 处理器，无需 `upgrade` 方法或额外的协议——使用官方 [`@modelcontextprotocol/sdk`](https://github.com/modelcontextprotocol/typescript-sdk) 加 [`@hono/mcp`](https://github.com/honojs/middleware/tree/main/packages/mcp)（将传输层桥接到路由）的 Hono 应用是最简单的宿主。构建服务器、注册工具、在模块作用域创建一次传输实例，然后将每个 `/mcp` 请求交给它：

```typescript
const transport = new StreamableHTTPTransport();
app.all("/mcp", async (c) => {
  if (!mcpServer.isConnected()) await mcpServer.connect(transport);
  return transport.handleRequest(c);
});
```

因为函数的 URL 是公开的，**连接传输前必须进行认证**——[Better Auth](https://better-auth.com) 同时支持 OAuth（其 MCP 插件使你的应用成为授权服务器，第三方客户端按 MCP 规范自授权）和更简单的 API Key / Session JWT 校验。[references/mcp.md](references/mcp.md) 包含完整模式——基于 Drizzle 的 Postgres 工具服务器、两种 Better Auth 认证选项，以及使用 `mcporter` / `add-mcp` 测试。

## 集成与可观测性

函数是一个长驻 Node.js 进程，运行 Web 标准请求/响应处理器，所以标准 Node 集成 SDK 无需修改即可使用——在模块加载时初始化一次，用环境变量门控以便本地开发和未配置的分支保持空操作，通过 `--env` 或 `neon.ts` `env` 传递密钥。关于在 HTTP 框架、函数运行时和 Agent 自身捕获/兜底失败（Functions 目标的长运行场景）之间接入 **Sentry** 错误监控，参见 [references/sentry.md](references/sentry.md)。关于在函数上运行 **Mastra** Agent 并将其追踪发送到 **Mastra Studio (Mastra Cloud)** 项目进行可观测性，参见 [references/mastra-studio.md](references/mastra-studio.md)。

## 超时与运行时限制

Functions 是长运行但**仍然是无服务器**的——它是请求/响应运行时，不是后台作业运行器。硬性限制：

- **首字节时间：15 分钟。** 你的处理器必须在收到请求后的 15 分钟内**开始**返回响应。大多数处理器在秒级完成；15 分钟的上限是为图像/视频生成等 Agent 工作负载预留的空间。
- **心跳：15 分钟。** 打开的 WebSocket/SSE 连接只要数据流动就保持存活。超时仅在连接静默时触发——至少每 15 分钟发送一个字节以保持安静流的存活。
- **`waitUntil`：15 分钟。** 通过 `waitUntil` 注册的工作在响应发送后保持调用的存活，最长 15 分钟——适用于清理操作如分析写入和审计日志，**不适用**于后台作业运行。（预览期间来自 `@neon/functions` 的 `waitUntil` 目前是桩实现。）
- **空闲驱逐。** 平台在没有活跃连接时关闭函数；也可能因运营原因驱逐/重启——如维护或将函数迁移到不同的计算节点（活跃函数可以先运行数小时）。将驱逐视为进程重启——WebSocket/SSE 客户端必须重连。平台在驱逐前发送 `SIGINT`，所以 `process.on("SIGINT", ...)` 处理器可以让你检测到函数即将被驱逐并执行最后的清理工作。仅为了关闭 Postgres 连接而不需要一个——Neon 的连接池器会自行回收。
- **运行时：** Node.js 24，预览期间内存固定为 2048 MiB。Slug 必须匹配 `^[a-z0-9]{1,20}$`。**isolate 在多个请求间被复用**——多个请求可能在同一 isolate 上同时飞行（在 Node 单线程事件循环上交错），高负载时运行时会并行运行多个 isolate，每个拥有自己的一份模块状态副本。因此模块作用域的状态是 per-isolate（该 isolate 处理的所有请求共享）且仅存在于内存中——任何需要在驱逐后存活的数据必须持久化到 Postgres。这种复用正是你在模块作用域创建一次连接池而不是每请求创建的原因（见 [连接 Postgres](#连接-postgres)）。

## Functions 作为 Agent 后端（Next.js 及类似框架）

Neon Function 正是 AI Agent 的理想载体，因为它**不像 Lambda 风格的无服务器那样会超时**（15 分钟预算，见上方）。但当你**通过 Web 应用的后端代理 Agent 流**时，这个优势就消失了——Next.js 路由处理器、Remix/SvelteKit/Nuxt action 等，托管在 Vercel、Netlify、Cloudflare 等平台。这些平台将无服务器/边缘执行限制在短窗口内（通常约 10–60 秒，有时最多约 300 秒），所以长 Agent 或图像/视频生成流即使 Neon Function 本身可以继续也会中途被截断。

**构建 Agent 本身。** [Vercel AI SDK](https://ai-sdk.dev) 和 [Mastra](https://mastra.ai) 是推荐的 Agent 构建方式——将模型指向 Neon AI Gateway（参见 `neon-ai-gateway` 技能）即可用一个凭据访问所有模型，无需额外的 Provider Key。关于完整的 AI SDK Agent 作为 Function 运行（流式 `toUIMessageStreamResponse`、Postgres 旁的多步工具调用、将生成的图片持久化到 Object Storage），参见 [references/ai-sdk.md](references/ai-sdk.md)；关于 Mastra 的等效方案及内置追踪，参见 [references/mastra-studio.md](references/mastra-studio.md)。

**解决方案：从客户端直接调用函数。** 不要把长请求路由到你应用的服务器。

```
Browser ──(Authorization: Bearer <JWT>)──▶  Neon Function (agent)   ✅ 无宿主超时
Browser ──▶ your app backend ──▶ Neon Function                       ❌ 宿主截断流
```

- 在你的应用后端生成一个**短期 JWT**（如 better-auth 的 `jwt` 插件、NextAuth 或你自己的签名器）——这个调用很快，远在宿主限制之内。
- 将 token 交给客户端，让它**直接**调用 Neon Function（跨域），例如配合 Vercel AI SDK：`new DefaultChatTransport({ api: NEON_FUNCTION_URL, fetch })` 其中 `fetch` 附加 `Authorization: Bearer <token>`。你的应用服务器不在长流路径上。
- 添加 **CORS** 以便浏览器可达（处理 `OPTIONS`、设置 `Access-Control-Allow-Origin`/`-Headers`）。

> [!WARNING]
> Neon Function 有一个**公开的 HTTPS URL——任何人都能访问它。** 客户端→函数的直接调用意味着前面没有应用后端做访问控制，所以**你必须自行对函数进行身份认证。** 验证 JWT（如对照应用的 JWKS）、检查共享密钥/API Key、或在处理器顶部校验 session token 并拒绝其他一切。永远不要部署未认证的 Agent。

```typescript
// src/index.ts — 在执行任何工作之前验证调用方
import { createRemoteJWKSet, jwtVerify } from "jose";

const jwks = createRemoteJWKSet(new URL(`${process.env.AUTH_BASE_URL}/api/auth/jwks`));

export default {
  async fetch(request: Request) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(request) });

    const auth = request.headers.get("authorization");
    if (!auth?.toLowerCase().startsWith("bearer ")) {
      return new Response("Unauthorized", { status: 401, headers: cors(request) });
    }
    try {
      const { payload } = await jwtVerify(auth.slice(7), jwks, {
        issuer: process.env.AUTH_BASE_URL,
        audience: process.env.AUTH_BASE_URL,
      });
      const userId = payload.sub; // 将 Agent 限定于此用户
      // ... 运行 Agent，返回 result.toUIMessageStreamResponse({ headers: cors(request) })
    } catch {
      return new Response("Unauthorized", { status: 401, headers: cors(request) });
    }
  },
};
```

通过函数的 `env` 传递 JWKS/issuer URL（参见[环境变量](#环境变量)）。将需要持久化的内容（生成的图片、历史记录）保存到 Postgres——模块状态不能幸免于驱逐。

## 可用性

Neon Functions 是预览功能（早期访问），仅限 `us-east-2` 区域的新项目使用。确认用户的 Neon 项目是 `us-east-2` 中的新项目；现有项目无法启用。私有预览期间 Functions 用量不计费。如果用户尚未获得访问权限，引导他们到私有测试版注册页面：https://neon.com/blog/were-building-backends#access

## Neon 文档

Neon 文档是权威来源且 Functions 快速迭代，所以务必对照官方文档验证。任何文档页可通过在 URL 后加 `.md` 或请求 `Accept: text/markdown` 获取 Markdown 格式。从文档索引（https://neon.com/docs/llms.txt）找到正确的页面，以及 changelog 公告。

## 延伸阅读

- https://neon.com/docs/compute/functions/overview.md
- https://neon.com/docs/compute/functions/get-started.md
- https://neon.com/docs/compute/functions/deploy.md
- https://neon.com/docs/compute/functions/environment-variables.md
- https://neon.com/docs/compute/functions/reference/neon-ts.md
- https://neon.com/docs/compute/functions/reference/runtime-limits.md
- https://neon.com/docs/compute/functions/preview-access.md

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时使用此技能。
- 在做出更改前，对照当前官方文档验证命令、API 行为、定价、配额、凭据和部署影响。
- 不要将生成的示例作为环境特定测试、安全审查或用户审批破坏性/昂贵操作的替代品。
