---
name: hono
description: "使用 Hono 构建超快的 Web API 和全栈应用 — 运行于 Cloudflare Workers、Deno、Bun、Node.js 及任何 WinterCG 兼容运行时。触发词：Hono、Hono框架、边缘API、Cloudflare Workers API、Bun服务器、Deno API、TypeScript后端、RPC客户端、hc客户端、Hono路由、Hono中间件、c.req、c.json"
category: backend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [hono, edge, cloudflare-workers, bun, deno, api, typescript, web-standards]
tools: [claude, cursor, gemini]
---

# Hono Web 框架

## 概述

Hono（炎，日语中的"火焰"）是一个基于 Web 标准（`Request`/`Response`/`fetch`）构建的小型、超快 Web 框架。它可以在任何地方运行：Cloudflare Workers、Deno Deploy、Bun、Node.js、AWS Lambda 以及任何 WinterCG 兼容的运行时 —— 使用相同的代码。Hono 的路由器是现有最快的之一，其中间件系统、内置 JSX 支持和 RPC 客户端使其成为边缘 API、BFF（Backend for Frontend）和轻量级全栈应用的强力选择。

## 何时使用此技能

- 构建用于边缘部署的 REST 或 RPC API 时使用（Cloudflare Workers、Deno Deploy）
- 需要为 Bun 或 Node.js 提供极简但类型安全的服务器框架时使用
- 构建低延迟要求的 BFF（Backend for Frontend）层时使用
- 从 Express 迁移但希望获得更好的 TypeScript 支持和边缘兼容性时使用
- 用户询问 Hono 路由、中间件、`c.req`、`c.json` 或 `hc()` RPC 客户端时使用

## 工作原理

### 步骤 1：项目设置

**Cloudflare Workers（推荐用于边缘部署）：**
```bash
npm create hono@latest my-api
# Select: cloudflare-workers
cd my-api
npm install
npm run dev    # Wrangler local dev
npm run deploy # Deploy to Cloudflare
```

**Bun / Node.js：**
```bash
mkdir my-api && cd my-api
bun init
bun add hono
```

```typescript
// src/index.ts (Bun)
import { Hono } from 'hono';

const app = new Hono();

app.get('/', c => c.text('Hello Hono!'));

export default {
  port: 3000,
  fetch: app.fetch,
};
```

### 步骤 2：路由

```typescript
import { Hono } from 'hono';

const app = new Hono();

// 基本方法
app.get('/posts', c => c.json({ posts: [] }));
app.post('/posts', c => c.json({ created: true }, 201));
app.put('/posts/:id', c => c.json({ updated: true }));
app.delete('/posts/:id', c => c.json({ deleted: true }));

// 路由参数和查询字符串
app.get('/posts/:id', async c => {
  const id = c.req.param('id');
  const format = c.req.query('format') ?? 'json';
  return c.json({ id, format });
});

// 通配符
app.get('/static/*', c => c.text('static file'));

export default app;
```

**链式路由：**
```typescript
app
  .get('/users', listUsers)
  .post('/users', createUser)
  .get('/users/:id', getUser)
  .patch('/users/:id', updateUser)
  .delete('/users/:id', deleteUser);
```

### 步骤 3：中间件

Hono 中间件的工作方式与 `fetch` 拦截器完全相同 —— 在处理程序之前和之后执行：

```typescript
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { cors } from 'hono/cors';
import { bearerAuth } from 'hono/bearer-auth';

const app = new Hono();

// 内置中间件
app.use('*', logger());
app.use('/api/*', cors({ origin: 'https://myapp.com' }));
app.use('/api/admin/*', bearerAuth({ token: process.env.API_TOKEN! }));

// 自定义中间件
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID());
  await next();
  c.header('X-Request-Id', c.get('requestId'));
});
```

**可用的内置中间件：** `logger`、`cors`、`csrf`、`etag`、`cache`、`basicAuth`、`bearerAuth`、`jwt`、`compress`、`bodyLimit`、`timeout`、`prettyJSON`、`secureHeaders`。

### 步骤 4：请求和响应辅助方法

```typescript
app.post('/submit', async c => {
  // 解析请求体
  const body = await c.req.json<{ name: string; email: string }>();
  const form = await c.req.formData();
  const text = await c.req.text();

  // 请求头和 Cookie
  const auth = c.req.header('authorization');
  const token = getCookie(c, 'session');

  // 响应
  return c.json({ ok: true });                        // JSON
  return c.text('hello');                             // 纯文本
  return c.html('<h1>Hello</h1>');                    // HTML
  return c.redirect('/dashboard', 302);              // 重定向
  return new Response(stream, { status: 200 });       // 原始 Response
});
```

### 步骤 5：Zod 验证器中间件

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(1),
  tags: z.array(z.string()).default([]),
});

app.post(
  '/posts',
  zValidator('json', createPostSchema),
  async c => {
    const data = c.req.valid('json'); // 完全类型化
    const post = await db.post.create({ data });
    return c.json(post, 201);
  }
);
```

### 步骤 6：路由组和应用组合

```typescript
// src/routes/posts.ts
import { Hono } from 'hono';

const posts = new Hono();

posts.get('/', async c => { /* 列出文章 */ });
posts.post('/', async c => { /* 创建文章 */ });
posts.get('/:id', async c => { /* 获取文章 */ });

export default posts;
```

```typescript
// src/index.ts
import { Hono } from 'hono';
import posts from './routes/posts';
import users from './routes/users';

const app = new Hono().basePath('/api');

app.route('/posts', posts);
app.route('/users', users);

export default app;
```

### 步骤 7：RPC 客户端（端到端类型安全）

Hono 的 RPC 模式导出路由类型，供 `hc` 客户端使用 —— 类似于 tRPC 但使用 fetch 约定：

```typescript
// server: src/routes/posts.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const posts = new Hono()
  .get('/', c => c.json({ posts: [{ id: '1', title: 'Hello' }] }))
  .post(
    '/',
    zValidator('json', z.object({ title: z.string() })),
    async c => {
      const { title } = c.req.valid('json');
      return c.json({ id: '2', title }, 201);
    }
  );

export default posts;
export type PostsType = typeof posts;
```

```typescript
// client: src/client.ts
import { hc } from 'hono/client';
import type { PostsType } from '../server/routes/posts';

const client = hc<PostsType>('/api/posts');

// 完全类型化 — 路由、参数和响应都有自动补全
const { posts } = await client.$get().json();
const newPost = await client.$post({ json: { title: 'New Post' } }).json();
```

## 示例

### 示例 1：JWT 认证中间件

```typescript
import { Hono } from 'hono';
import { jwt, sign } from 'hono/jwt';

const app = new Hono();
const SECRET = process.env.JWT_SECRET!;

app.post('/login', async c => {
  const { email, password } = await c.req.json();
  const user = await validateUser(email, password);
  if (!user) return c.json({ error: 'Invalid credentials' }, 401);

  const token = await sign({ sub: user.id, exp: Math.floor(Date.now() / 1000) + 3600 }, SECRET);
  return c.json({ token });
});

app.use('/api/*', jwt({ secret: SECRET }));
app.get('/api/me', async c => {
  const payload = c.get('jwtPayload');
  const user = await getUserById(payload.sub);
  return c.json(user);
});

export default app;
```

### 示例 2：Cloudflare Workers 配合 D1 数据库

```typescript
// src/index.ts
import { Hono } from 'hono';

type Bindings = {
  DB: D1Database;
  API_TOKEN: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/users', async c => {
  const { results } = await c.env.DB.prepare('SELECT * FROM users LIMIT 50').all();
  return c.json(results);
});

app.post('/users', async c => {
  const { name, email } = await c.req.json();
  await c.env.DB.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
    .bind(name, email)
    .run();
  return c.json({ created: true }, 201);
});

export default app;
```

### 示例 3：流式响应

```typescript
import { stream, streamText } from 'hono/streaming';

app.get('/stream', c =>
  streamText(c, async stream => {
    for (const chunk of ['Hello', ' ', 'World']) {
      await stream.write(chunk);
      await stream.sleep(100);
    }
  })
);
```

## 最佳实践

- ✅ 使用路由组（子应用）将处理程序保持在单独的文件中 — `app.route('/users', usersRouter)`
- ✅ 对所有请求体、查询和参数验证使用 `zValidator`
- ✅ 使用 `Bindings` 泛型为 Cloudflare Workers 绑定类型：`new Hono<{ Bindings: Env }>()`
- ✅ 当前端和后端共享同一仓库时使用 RPC 客户端（`hc`）
- ✅ 优先使用 `c.json()`/`c.text()` 而非 `new Response()` 以获得更简洁的代码
- ❌ 如果希望边缘可移植性，不要使用 Node.js 特定 API（`fs`、`path`、`process`）
- ❌ 不要添加重型依赖 — Hono 的价值在于其在边缘运行时上的极小体积
- ❌ 不要跳过中间件类型 — 使用泛型（`Variables`、`Bindings`）保持 `c.get()` 类型安全

## 安全与注意事项

- 在使用请求数据之前，始终使用 `zValidator` 验证输入。
- 在提供 HTML/表单的变更端点上使用 Hono 内置的 `csrf` 中间件。
- 对于 Cloudflare Workers，将密钥存储在 `wrangler.toml` 的 `[vars]`（非机密）或使用 `wrangler secret put`（机密）— 切勿在源代码中硬编码。
- 使用 `bearerAuth` 或 `jwt` 时，确保令牌在服务端验证 — 不要信任客户端提供的用户 ID。
- 对敏感端点（认证、密码重置）使用 Cloudflare Rate Limiting 或自定义中间件进行速率限制。

## 常见陷阱

- **问题：** 处理程序返回 `undefined` — 响应为空
  **解决方案：** 始终从处理程序 `return` 一个响应：`return c.json(...)` 而不是仅 `c.json(...)`。

- **问题：** 中间件在响应发送后运行
  **解决方案：** 在响应后逻辑之前调用 `await next()`；Hono 在 `next()` 之后的代码会在响应沿链返回时执行。

- **问题：** `c.env` 在 Node.js 上为 undefined
  **解决方案：** Cloudflare `env` 绑定仅存在于 Workers 中。在 Node.js 上使用 `process.env`。

- **问题：** 路由不匹配 — 返回 404
  **解决方案：** 检查 `app.route('/prefix', subRouter)` 使用的前缀与客户端调用的前缀是否相同。子路由器**不应**在自己的路由中重复前缀。

## 相关技能

- `@cloudflare-workers-expert` — 深入了解 Cloudflare Workers 平台特性
- `@trpc-fullstack` — TypeScript 全栈应用的替代 RPC 方案
- `@zod-validation-expert` — 与 `@hono/zod-validator` 配合使用的详细 Zod schema 模式
- `@nodejs-backend-patterns` — 当需要 Node.js 特定的后端（非边缘）时使用

## 限制

- 仅当任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
