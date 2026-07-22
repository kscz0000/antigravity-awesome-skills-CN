---
name: trpc-fullstack
description: "使用 tRPC 构建端到端类型安全的 API —— 路由、过程、中间件、订阅及 Next.js/React 集成模式。"
category: framework
risk: none
source: community
date_added: "2026-03-17"
author: suhaibjanjua
tags: [typescript, trpc, api, fullstack, nextjs, react, type-safety]
tools: [claude, cursor, gemini]
---

# tRPC 全栈开发

## 概述

tRPC 让你无需编写 schema 或代码生成步骤，就能构建完全类型安全的 API。TypeScript 类型从服务端路由直接流向客户端——每次 API 调用都有自动补全、编译时验证和重构安全保障。构建 TypeScript monorepo、Next.js 应用或任何服务端与客户端共享代码库的项目时使用此技能。

## 适用场景

- 构建客户端和服务端共享单一仓库的 TypeScript 全栈应用（Next.js、Remix、Express + React）
- 需要 API 调用的端到端类型安全，又不想承担 REST/GraphQL schema 的额外开销
- 为现有 tRPC 项目添加实时功能（订阅）
- 在 tRPC 过程上设计多步中间件（认证、限流、租户隔离）
- 将现有 REST/GraphQL API 渐进式迁移到 tRPC

## 核心概念

### 路由与过程

**路由**将相关的**过程**（相当于端点）组织在一起。过程是带类型的函数——`query` 用于读取，`mutation` 用于写入，`subscription` 用于实时流。

### 使用 Zod 进行输入验证

所有过程输入都通过 Zod schema 验证。验证后的带类型输入在过程处理函数中可直接使用——无需手动解析。

### 上下文

`context` 是传递给每个过程的共享状态——认证会话、数据库客户端、请求头等。它在上下文工厂中每个请求构建一次。**重要提示：** Next.js App Router 和 Pages Router 需要独立的上下文工厂，因为 App Router 处理函数接收的是 fetch `Request`，而非 Node.js 的 `NextApiRequest`。

### 中间件

中间件链在过程执行前运行。用于认证、日志记录和请求增强。它们可以为下游过程扩展上下文。

---

## 工作原理

### 步骤 1：安装与初始化

```bash
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

创建 tRPC 实例和可复用的构建器：

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { type Context } from './context';
import { ZodError } from 'zod';

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
```

### 步骤 2：定义两个上下文工厂

Next.js App Router 处理函数接收 fetch `Request`（而非 Node.js 的 `NextApiRequest`），因此上下文的构建方式取决于调用位置。为每种场景定义一个工厂：

```typescript
// src/server/context.ts
import { type FetchCreateContextFnOptions } from '@trpc/server/adapters/fetch';
import { auth } from '@/server/auth'; // Next-Auth v5 / your auth helper
import { db } from './db';

/**
 * Context for the HTTP handler (App Router Route Handler).
 * `opts.req` is the fetch Request — auth is resolved server-side via `auth()`.
 */
export async function createTRPCContext(opts: FetchCreateContextFnOptions) {
  const session = await auth(); // server-side auth — no req/res needed
  return { session, db, headers: opts.req.headers };
}

/**
 * Context for direct server-side callers (Server Components, RSC, cron jobs).
 * No HTTP request is involved, so we call auth() directly from the server.
 */
export async function createServerContext() {
  const session = await auth();
  return { session, db };
}

export type Context = Awaited<ReturnType<typeof createTRPCContext>>;
```

### 步骤 3：构建认证中间件和受保护过程

```typescript
// src/server/trpc.ts (continued)
const enforceAuth = middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: {
      // Narrows type: session is non-null from here
      session: { ...ctx.session, user: ctx.session.user },
    },
  });
});

export const protectedProcedure = t.procedure.use(enforceAuth);
```

### 步骤 4：创建路由

```typescript
// src/server/routers/post.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';
import { TRPCError } from '@trpc/server';

export const postRouter = router({
  list: publicProcedure
    .input(
      z.object({
        limit: z.number().min(1).max(100).default(20),
        cursor: z.string().optional(),
      })
    )
    .query(async ({ ctx, input }) => {
      const posts = await ctx.db.post.findMany({
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: 'desc' },
      });
      const nextCursor =
        posts.length > input.limit ? posts.pop()!.id : undefined;
      return { posts, nextCursor };
    }),

  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } });
      if (!post) throw new TRPCError({ code: 'NOT_FOUND' });
      return post;
    }),

  create: protectedProcedure
    .input(
      z.object({
        title: z.string().min(1).max(200),
        body: z.string().min(1),
      })
    )
    .mutation(async ({ ctx, input }) => {
      return ctx.db.post.create({
        data: { ...input, authorId: ctx.session.user.id },
      });
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } });
      if (!post) throw new TRPCError({ code: 'NOT_FOUND' });
      if (post.authorId !== ctx.session.user.id)
        throw new TRPCError({ code: 'FORBIDDEN' });
      return ctx.db.post.delete({ where: { id: input.id } });
    }),
});
```

### 步骤 5：组合根路由并导出类型

```typescript
// src/server/root.ts
import { router } from './trpc';
import { postRouter } from './routers/post';
import { userRouter } from './routers/user';

export const appRouter = router({
  post: postRouter,
  user: userRouter,
});

// Export the type for the client — never import the appRouter itself on the client
export type AppRouter = typeof appRouter;
```

### 步骤 6：挂载 API 处理函数（Next.js App Router）

App Router 处理函数必须使用 `fetchRequestHandler` 和基于 **fetch 的**上下文工厂。`createTRPCContext` 接收 `FetchCreateContextFnOptions`（包含 fetch `Request`），而非 Pages Router 的 `req/res` 对。

```typescript
// src/app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { type FetchCreateContextFnOptions } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/root';
import { createTRPCContext } from '@/server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    // opts is FetchCreateContextFnOptions — req is the fetch Request
    createContext: (opts: FetchCreateContextFnOptions) => createTRPCContext(opts),
  });

export { handler as GET, handler as POST };
```

### 步骤 7：配置客户端（React Query）

```typescript
// src/utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '@/server/root';

export const trpc = createTRPCReact<AppRouter>();
```

```typescript
// src/app/providers.tsx
'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from '@/utils/trpc';

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
          headers: () => ({ 'x-trpc-source': 'react' }),
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </trpc.Provider>
  );
}
```

---

## 示例

### 示例 1：在组件中获取数据

```typescript
// components/PostList.tsx
'use client';
import { trpc } from '@/utils/trpc';

export function PostList() {
  const { data, isLoading, error } = trpc.post.list.useQuery({ limit: 10 });

  if (isLoading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <ul>
      {data?.posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### 示例 2：带缓存失效的变更

```typescript
'use client';
import { trpc } from '@/utils/trpc';

export function CreatePost() {
  const utils = trpc.useUtils();

  const createPost = trpc.post.create.useMutation({
    onSuccess: () => {
      // Invalidate and refetch the post list
      utils.post.list.invalidate();
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    createPost.mutate({
      title: data.get('title') as string,
      body: data.get('body') as string,
    });
    form.reset();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" placeholder="Title" required />
      <textarea name="body" placeholder="Body" required />
      <button type="submit" disabled={createPost.isPending}>
        {createPost.isPending ? 'Creating…' : 'Create Post'}
      </button>
      {createPost.error && <p>{createPost.error.message}</p>}
    </form>
  );
}
```

### 示例 3：服务端调用（Server Components / SSR）

使用 `createServerContext`——专用的服务端工厂——确保 `auth()` 被正确调用，无需合成或空的请求对象：

```typescript
// app/posts/page.tsx (Next.js Server Component)
import { appRouter } from '@/server/root';
import { createCallerFactory } from '@trpc/server';
import { createServerContext } from '@/server/context';

const createCaller = createCallerFactory(appRouter);

export default async function PostsPage() {
  // Uses createServerContext — calls auth() server-side, no req/res cast needed
  const caller = createCaller(await createServerContext());
  const { posts } = await caller.post.list({ limit: 20 });

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### 示例 4：实时订阅（WebSocket）

```typescript
// server/routers/notifications.ts
import { observable } from '@trpc/server/observable';
import { EventEmitter } from 'events';

const ee = new EventEmitter();

export const notificationRouter = router({
  onNew: protectedProcedure.subscription(({ ctx }) => {
    return observable<{ message: string; at: Date }>((emit) => {
      const onNotification = (data: { message: string }) => {
        emit.next({ message: data.message, at: new Date() });
      };

      const channel = `user:${ctx.session.user.id}`;
      ee.on(channel, onNotification);
      return () => ee.off(channel, onNotification);
    });
  }),
});
```

```typescript
// Client usage — requires wsLink in the client config
trpc.notification.onNew.useSubscription(undefined, {
  onData(data) {
    toast(data.message);
  },
});
```

---

## 最佳实践

- ✅ **仅导出 `AppRouter` 类型**——客户端永远不要导入 `appRouter` 本身
- ✅ **使用独立的上下文工厂**——`createTRPCContext` 用于 HTTP 处理函数，`createServerContext` 用于 Server Components 和调用者
- ✅ **用 Zod 验证所有输入**——永远不要信任没有 schema 的原始 `input`
- ✅ **按领域拆分路由**（posts、users、billing）并在 `root.ts` 中合并
- ✅ **在中间件中扩展上下文**，而不是每个请求多次查询数据库
- ✅ **变更后调用 `utils.invalidate()`** 保持缓存新鲜
- ❌ **不要用 `as any` 强制转换上下文**来消除类型错误——当认证或会话查找返回 undefined 时，类型不匹配会变成运行时失败
- ❌ **不要在 Server Components 中使用 `createContext({} as any)`**——使用 `createServerContext()` 直接调用 `auth()`
- ❌ **不要把业务逻辑放在路由处理函数中**——保持在过程或服务层
- ❌ **不要全局共享 tRPC 客户端实例**——每个 Provider 单独创建以避免闭包过期

---

## 安全注意事项

- 始终在 `protectedProcedure` 中强制执行授权——永远不要仅依赖客户端检查
- 用 Zod 验证所有输入结构，包括分页游标和 ID，防止畸形输入注入
- 避免向客户端暴露内部错误详情——使用 `TRPCError` 配合公开安全的 `message`，堆栈跟踪仅保留在服务端
- 对公开过程使用中间件进行限流，防止滥用

---

## 常见陷阱

- **问题：** 即使用户已登录，受保护过程中认证会话仍为 `null`
  **解决方案：** 确保 `createTRPCContext` 使用正确的服务端认证调用（如 Next-Auth v5 的 `auth()`），且未在 App Router 处理函数中通过 `as any` 接收 Pages Router 的 `req/res` 转换

- **问题：** Server Components 调用者在依赖认证的查询中失败
  **解决方案：** 使用 `createServerContext()`（专用的服务端工厂），而不是向 `createContext` 传递空对象或合成对象

- **问题：** "类型错误：AppRouter 不可赋值给 AnyRouter"
  **解决方案：** 在客户端使用 `type` 导入 `AppRouter`（`import type { AppRouter }`），而非导入完整模块

- **问题：** 变更成功后 UI 未更新
  **解决方案：** 在 `onSuccess` 中调用 `utils.<router>.<procedure>.invalidate()` 触发 React Query 重新获取

- **问题：** App Router 报错"找不到模块 '@trpc/server/adapters/next'"
  **解决方案：** App Router 使用 `@trpc/server/adapters/fetch` 和 `fetchRequestHandler`；`nextjs` 适配器仅用于 Pages Router

- **问题：** 订阅无法连接
  **解决方案：** 订阅需要 `splitLink`——将订阅路由到 `wsLink`，将查询/变更路由到 `httpBatchLink`

---

## 相关技能

- `@typescript-expert` —— tRPC 路由和通用工具中使用的深层 TypeScript 模式
- `@react-patterns` —— 与 `trpc.*.useQuery` 和 `useMutation` 配套的 React hooks 模式
- `@test-driven-development` —— 使用 `createCallerFactory` 编写过程单元测试，无需 HTTP 服务器
- `@security-auditor` —— 审查 tRPC 中间件链的认证绕过和输入验证漏洞

## 扩展资源

- [tRPC 官方文档](https://trpc.io/docs)
- [create-t3-app](https://create.t3.gg) —— 内置 tRPC 的生产级 Next.js 起手模板
- [tRPC GitHub](https://github.com/trpc/trpc)
- [TanStack Query 文档](https://tanstack.com/query/latest)

## 限制

- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清