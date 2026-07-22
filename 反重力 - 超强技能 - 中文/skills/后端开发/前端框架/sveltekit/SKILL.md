---
name: sveltekit
description: "使用 SvelteKit 构建全栈 Web 应用——文件路由、SSR、SSG、API 路由和表单操作一体化框架。触发词：SvelteKit、Svelte全栈、文件路由、SSR、SSG、表单操作、+page.svelte、+layout.svelte、load函数"
category: frontend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [svelte, sveltekit, fullstack, ssr, ssg, typescript]
tools: [claude, cursor, gemini]
---

# SvelteKit 全栈开发

## 概述

SvelteKit 是基于 Svelte 构建的官方全栈框架。它提供文件路由、服务端渲染（SSR）、静态站点生成（SSG）、API 路由和渐进式表单操作——所有这些都依托于 Svelte 的编译时响应式模型，向浏览器交付零运行时开销。当构建既重视开发体验又重视性能的快速现代 Web 应用时，使用此技能。

## 何时使用此技能

- 使用 Svelte 构建新的全栈 Web 应用时使用
- 需要对每个路由精细控制 SSR 或 SSG 时使用
- 将 SPA 迁移到具有服务端能力的框架时使用
- 项目需要文件路由和同位 API 端点时使用
- 用户询问 `+page.svelte`、`+layout.svelte`、`load` 函数或表单操作时使用

## 工作原理

### 第 1 步：项目设置

```bash
npm create svelte@latest my-app
cd my-app
npm install
npm run dev
```

在提示时选择 **Skeleton project** + **TypeScript** + **ESLint/Prettier**。

脚手架生成后的目录结构：

```
src/
  routes/
    +page.svelte        ← 根页面组件
    +layout.svelte      ← 根布局（包裹所有页面）
    +error.svelte       ← 错误边界
  lib/
    server/             ← 仅服务端代码（不会打包到客户端）
    components/         ← 共享组件
  app.html              ← HTML 外壳
static/                 ← 静态资源
```

### 第 2 步：文件路由

`src/routes/` 中的每个 `+page.svelte` 文件直接映射到一个 URL：

```
src/routes/+page.svelte          → /
src/routes/about/+page.svelte    → /about
src/routes/blog/[slug]/+page.svelte  → /blog/:slug
src/routes/shop/[...path]/+page.svelte → /shop/* (catch-all)
```

**路由分组**（不产生 URL 段）：用 `(group)/` 文件夹包裹。
**私有路由**（不可作为 URL 访问）：以 `_` 或 `(group)` 为前缀。

### 第 3 步：使用 `load` 函数加载数据

在页面旁使用 `+page.ts`（通用）或 `+page.server.ts`（仅服务端）文件：

```typescript
// src/routes/blog/[slug]/+page.server.ts
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const post = await fetch(`/api/posts/${params.slug}`).then(r => r.json());

  if (!post) {
    error(404, 'Post not found');
  }

  return { post };
};
```

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>{data.post.title}</h1>
<article>{@html data.post.content}</article>
```

### 第 4 步：API 路由（服务端端点）

创建 `+server.ts` 文件用于 REST 风格的端点：

```typescript
// src/routes/api/posts/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 10);
  const posts = await db.post.findMany({ take: limit });
  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const post = await db.post.create({ data: body });
  return json(post, { status: 201 });
};
```

### 第 5 步：表单操作

表单操作是 SvelteKit 原生的变更处理方式——无需客户端 fetch：

```typescript
// src/routes/contact/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return fail(400, { email, missing: true });
    }

    await sendEmail(String(email));
    redirect(303, '/thank-you');
  }
};
```

```svelte
<!-- src/routes/contact/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';
  export let form: ActionData;
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  {#if form?.missing}<p class="error">Email is required</p>{/if}
  <button type="submit">Subscribe</button>
</form>
```

### 第 6 步：布局与嵌套路由

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';
  export let data: LayoutData;
</script>

<nav>
  <a href="/">Home</a>
  <a href="/blog">Blog</a>
  {#if data.user}
    <a href="/dashboard">Dashboard</a>
  {/if}
</nav>

<slot />  <!-- 子页面在此渲染 -->
```

```typescript
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  return { user: locals.user ?? null };
};
```

### 第 7 步：渲染模式

通过页面选项按路由控制渲染：

```typescript
// src/routes/docs/+page.ts
export const prerender = true;   // 静态 — 构建时生成
export const ssr = true;         // 默认 — 每次请求在服务端渲染
export const csr = false;        // 完全禁用客户端水合
```

## 示例

### 示例 1：受保护的仪表盘路由

```typescript
// src/routes/dashboard/+layout.server.ts
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(303, '/login');
  }
  return { user: locals.user };
};
```

### 示例 2：Hooks — 会话中间件

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { verifyToken } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('session');
  if (token) {
    event.locals.user = await verifyToken(token);
  }
  return resolve(event);
};
```

### 示例 3：预加载与失效

```svelte
<script lang="ts">
  import { invalidateAll } from '$app/navigation';

  async function refresh() {
    await invalidateAll(); // 重新运行页面上的所有 load 函数
  }
</script>

<button on:click={refresh}>Refresh</button>
```

## 最佳实践

- ✅ 使用 `+page.server.ts` 处理数据库/认证逻辑——它永远不会发送到客户端
- ✅ 使用 `$lib/server/` 存放共享的仅服务端模块（数据库客户端、认证辅助函数）
- ✅ 使用表单操作而非客户端 `fetch` 处理变更——无需 JS 也能工作
- ✅ 使用生成的 `$types`（`PageData`、`LayoutData`）为所有 `load` 返回值添加类型
- ✅ 在 hooks 中使用 `event.locals` 将服务端上下文传递给 load 函数
- ❌ 不要在 `+page.svelte` 或 `+layout.svelte` 中直接导入仅服务端代码
- ❌ 不要在 store 中存储敏感状态——应在服务端使用 `locals`
- ❌ 不要在表单上跳过 `use:enhance`——没有它，表单将失去渐进增强能力

## 安全注意事项

- `+page.server.ts`、`+server.ts` 和 `$lib/server/` 中的所有代码仅在服务端运行——适合数据库查询、密钥和会话验证。
- 在写入数据库前始终验证和清理表单数据。
- 使用 `@sveltejs/kit` 的 `error(403)` 或 `redirect(303)`，而非返回原始错误对象。
- 在所有认证 cookie 上设置 `httpOnly: true` 和 `secure: true`。
- 表单操作内置 CSRF 防护——在生产环境中不要禁用 `checkOrigin`。

## 常见陷阱

- **问题：** `+page.server.ts` 中出现 `Cannot use import statement in a module`
  **解决方案：** 文件必须是 `.ts` 或 `.js`，而非 `.svelte`。服务端文件和 Svelte 组件是分开的。

- **问题：** Store 值在首次 SSR 渲染时为 `undefined`
  **解决方案：** 从 `load` 函数的返回值（`data` 属性）填充 store，而非从客户端的 `onMount`。

- **问题：** 表单操作提交后未重定向
  **解决方案：** 使用 `@sveltejs/kit` 的 `redirect(303, '/path')`，而非普通的 `return`。POST 重定向必须使用 303 状态码。

- **问题：** `locals.user` 在 `+page.server.ts` 的 load 函数中为 undefined
  **解决方案：** 在 `src/hooks.server.ts` 的 `resolve()` 调用之前设置 `event.locals.user`。

## 相关技能

- `@nextjs-app-router-patterns` — 当你更倾向使用 React 而非 Svelte 进行 SSR/SSG 时
- `@trpc-fullstack` — 为 SvelteKit API 路由添加端到端类型安全
- `@auth-implementation-patterns` — 可与 SvelteKit hooks 配合使用的认证模式
- `@tailwind-patterns` — 使用 Tailwind CSS 为 SvelteKit 应用添加样式

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
