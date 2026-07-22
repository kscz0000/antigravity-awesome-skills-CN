---
name: astro
description: "使用 Astro 构建内容驱动的网站 — 默认零 JavaScript、岛屿架构、多框架组件支持、Markdown/MDX 支持。触发词：Astro、SSG、SSR、岛屿架构、内容网站、博客生成、文档站点、静态站点生成、Astro 组件、client:load、content collections、getStaticPaths、.astro 文件、Astro.props。"
category: frontend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [astro, ssg, ssr, islands, content, markdown, mdx, performance]
tools: [claude, cursor, gemini]
---

# Astro Web 框架

## 概述

Astro 是专为内容丰富的网站设计的 Web 框架 — 博客、文档、作品集、营销网站和电商站点。其核心创新是**岛屿架构**：默认情况下，Astro 向浏览器发送零 JavaScript。交互组件作为独立的"岛屿"选择性水合。Astro 支持在同一项目中同时使用 React、Vue、Svelte、Solid 等 UI 框架，让你为每个组件选择合适的工具。

## 何时使用此技能

- 构建博客、文档站点、营销页面或作品集时使用
- 性能和 Core Web Vitals 是首要优先级时使用
- 项目包含大量 Markdown 或 MDX 文件时使用
- 需要 SSG（静态）输出，同时可选 SSR 处理动态路由时使用
- 用户询问 `.astro` 文件、`Astro.props`、内容集合或 `client:` 指令时使用

## 工作原理

### 步骤 1：项目设置

```bash
npm create astro@latest my-site
cd my-site
npm install
npm run dev
```

按需添加集成：

```bash
npx astro add tailwind        # Tailwind CSS
npx astro add react           # React 组件支持
npx astro add mdx             # MDX 支持
npx astro add sitemap         # 自动生成 sitemap.xml
npx astro add vercel          # Vercel SSR 适配器
```

项目结构：

```
src/
  pages/          ← 基于文件的路由（.astro、.md、.mdx）
  layouts/        ← 可复用的页面外壳
  components/     ← UI 组件（.astro、.tsx、.vue 等）
  content/        ← 类型安全的内容集合（Markdown/MDX）
  styles/         ← 全局 CSS
public/           ← 静态资源（原样复制）
astro.config.mjs  ← 框架配置
```

### 步骤 2：Astro 组件语法

`.astro` 文件顶部有代码围栏（仅服务端），下方是模板：

```astro
---
// src/components/Card.astro
// 此代码块仅在服务端运行 — 永远不会在浏览器中执行
interface Props {
  title: string;
  href: string;
  description: string;
}

const { title, href, description } = Astro.props;
---

<article class="card">
  <h2><a href={href}>{title}</a></h2>
  <p>{description}</p>
</article>

<style>
  /* 自动作用于当前组件 */
  .card { border: 1px solid #eee; padding: 1rem; }
</style>
```

### 步骤 3：基于文件的页面和路由

```
src/pages/index.astro          → /
src/pages/about.astro          → /about
src/pages/blog/[slug].astro    → /blog/:slug（动态）
src/pages/blog/[...path].astro → /blog/*（捕获所有）
```

使用 `getStaticPaths` 的动态路由：

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<h1>{post.data.title}</h1>
<Content />
```

### 步骤 4：内容集合

内容集合为 Markdown 和 MDX 文件提供类型安全的访问：

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter(p => !p.data.draft)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---

<ul>
  {posts.map(post => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      <time>{post.data.date.toLocaleDateString()}</time>
    </li>
  ))}
</ul>
```

### 步骤 5：岛屿 — 选择性水合

默认情况下，UI 框架组件渲染为静态 HTML，不包含 JS。使用 `client:` 指令进行水合：

```astro
---
import Counter from '../components/Counter.tsx';  // React 组件
import VideoPlayer from '../components/VideoPlayer.svelte';
---

<!-- 静态 HTML — 不向浏览器发送 JavaScript -->
<Counter initialCount={0} />

<!-- 页面加载时立即水合 -->
<Counter initialCount={0} client:load />

<!-- 组件滚动到视口时水合 -->
<VideoPlayer src="/demo.mp4" client:visible />

<!-- 浏览器空闲时才水合 -->
<Analytics client:idle />

<!-- 仅在特定媒体查询下水合 -->
<MobileMenu client:media="(max-width: 768px)" />
```

### 步骤 6：布局

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}
const { title, description = 'My Astro Site' } = Astro.props;
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content={description} />
  </head>
  <body>
    <nav>...</nav>
    <main>
      <slot />  <!-- 页面内容在此渲染 -->
    </main>
    <footer>...</footer>
  </body>
</html>
```

```astro
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="About Us">
  <h1>About Us</h1>
  <p>Welcome to our company...</p>
</BaseLayout>
```

### 步骤 7：SSR 模式（按需渲染）

通过设置适配器启用 SSR 以支持动态页面：

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel/serverless';

export default defineConfig({
  output: 'hybrid',  // 'static' | 'server' | 'hybrid'
  adapter: vercel(),
});
```

使用 `export const prerender = false` 让单个页面启用 SSR。

## 示例

### 示例 1：带 RSS 订阅的博客

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog');
  return rss({
    title: 'My Blog',
    description: 'Latest posts',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.date,
      link: `/blog/${post.slug}/`,
    })),
  });
}
```

### 示例 2：API 端点（SSR）

```typescript
// src/pages/api/subscribe.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const { email } = await request.json();

  if (!email) {
    return new Response(JSON.stringify({ error: 'Email required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  await addToNewsletter(email);
  return new Response(JSON.stringify({ success: true }), { status: 200 });
};
```

### 示例 3：作为岛屿的 React 组件

```tsx
// src/components/SearchBox.tsx
import { useState } from 'react';

export default function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  async function search(e: React.FormEvent) {
    e.preventDefault();
    const data = await fetch(`/api/search?q=${query}`).then(r => r.json());
    setResults(data);
  }

  return (
    <form onSubmit={search}>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button type="submit">Search</button>
      <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>
    </form>
  );
}
```

```astro
---
import SearchBox from '../components/SearchBox.tsx';
---
<!-- 立即水合 — 此岛屿可交互 -->
<SearchBox client:load />
```

## 最佳实践

- ✅ 将大多数组件保持为静态 `.astro` 文件 — 仅对必须交互的组件进行水合
- ✅ 对所有 Markdown/MDX 内容使用内容集合 — 获得类型安全和自动验证
- ✅ 对首屏以下组件优先使用 `client:visible` 而非 `client:load` 以减少初始 JS
- ✅ 使用 `import.meta.env` 处理环境变量 — 公开变量使用 `PUBLIC_` 前缀
- ✅ 从 `astro:transitions` 添加 `<ViewTransitions />` 实现平滑页面导航，无需完整 SPA
- ❌ 不要对所有组件使用 `client:load` — 这会抵消 Astro 的性能优势
- ❌ 不要在客户端模板中使用的 `.astro` 前置配置中放置敏感信息
- ❌ 不要在静态模式下跳过动态路由的 `getStaticPaths` — 构建会失败

## 安全注意事项

- `.astro` 文件中的前置配置代码仅在服务端运行，永远不会暴露给浏览器。
- 仅对非敏感值使用 `import.meta.env.PUBLIC_*`。私有环境变量（无 `PUBLIC_` 前缀）永远不会发送到客户端。
- 使用 SSR 模式时，在数据库查询或 API 调用前验证所有 `Astro.request` 输入。
- 使用 `set:html` 渲染用户内容前进行清理 — 它会绕过自动转义。

## 常见陷阱

- **问题：** React/Vue 组件的 JavaScript 在浏览器中不执行
  **解决方案：** 添加 `client:` 指令（`client:load`、`client:visible` 等）— 没有它，组件仅渲染为静态 HTML。

- **问题：** 开发过程中内容更新后 `getStaticPaths` 数据过时
  **解决方案：** Astro 开发服务器监视内容文件 — 如果 `content/config.ts` 的更改未反映，请重启。

- **问题：** `Astro.props` 类型为 `any` — 无自动补全
  **解决方案：** 在前置配置中定义 `Props` 接口或类型，Astro 会自动推断。

- **问题：** `.astro` 组件的 CSS 渗透到其他组件
  **解决方案：** `.astro` `<style>` 标签中的样式自动作用域化。仅在有意针对子元素时使用 `:global()`。

## 相关技能

- `@sveltekit` — 需要具有响应式 UI 的全栈框架时（对比 Astro 的内容导向）
- `@nextjs-app-router-patterns` — 需要 React 优先的全栈框架时
- `@tailwind-patterns` — 使用 Tailwind CSS 为 Astro 站点设置样式
- `@progressive-web-app` — 为 Astro 站点添加 PWA 功能

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
