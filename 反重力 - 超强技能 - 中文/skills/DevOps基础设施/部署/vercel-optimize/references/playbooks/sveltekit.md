# SvelteKit

针对 Vercel 上 SvelteKit 项目的框架特定剧本。除了适用的应用画像剧本（saas、ecommerce、content-site 等）外，还应用该剧本。SvelteKit-on-Vercel 通过 `@sveltejs/adapter-vercel` 部署，因此大多数平台级建议映射到 adapter 配置而不是每路由框架 API。

## 典型计费形态

函数时长主导服务端渲染路由（每个 `+page.server.ts` `load` + `+server.ts` POST 处理程序都作为函数运行）。边缘请求随 API 表面（`+server.ts` 和 form actions）增长。ISR 通过 adapter 支持；启用时，它在首次渲染后转换为 cache_result HIT。图像优化很少是 SvelteKit 特定杠杆（它与 Next.js 使用的 Vercel 图像服务相同）。

## 优先级模式

1. **Adapter ISR 用于可缓存的内容。** 默认情况下，不依赖于每请求数据的路由仍作为函数提供。Adapter 接受每路由的 `isr: { expiration: 60 }` 选项（在 `+page.server.ts` 中通过 `export const config` 设置）。这会将函数调用转换为缓存命中。引用 `https://kit.svelte.dev/docs/adapter-vercel` + `https://vercel.com/docs/incremental-static-regeneration`。
2. **静态内容预渲染。** 在 `+page.server.ts` 或 `+page.ts` 中的 `export const prerender = true` 将路由从函数移到 CDN。引用 `https://kit.svelte.dev/docs/page-options`。
3. **并行 `load` 获取。** 具有多个顺序 `await fetch(...)` 调用的 `load` 函数会在墙钟时间上留下时间——将它们包装在 `Promise.all` 中（或直接从 `load` 返回 promise，SvelteKit 会流式传输）。引用 `https://kit.svelte.dev/docs/load`。
4. **将每请求工作移到 `+server.ts` action handlers 并通过客户端的 `fetch` 运行它们。** 当只有页面的一小部分实际上在每个请求上需要服务器数据时，减少 SSR 成本。
5. **`hooks.server.ts` matcher 卫生。** 与 Next.js 中间件类似，`handle` hook 拦截每个请求，除非被过滤。沉重的 `handle` 代码按请求量乘以成本。当只有特定路由需要工作时，将工作移到该路由的 `load` 中。
6. **Adapter runtime + region 配置。** 单区域默认；如果项目的用户偏向不同区域，在 adapter 上设置 `regions: [...]` 以将 TTFB 减少 100-300ms。

## 常见陷阱

- **每路由 SSR 而预渲染就足够。** 营销页面、文档、博客文章常常最终作为函数，因为没有人添加 `prerender = true`。扫描器标记这些。
- **`+layout.server.ts` 数据获取阻塞每个子路由。** 布局中的鉴权检查 + 用户加载使每个函数调用等待这些查询——即使是不读取用户的路由。将用户加载推到需要它的路由中。
- **Adapter 版本漂移。** `adapter-vercel@5` 添加了新选项（ISR、split）。`adapter-vercel@3` 不添加。推荐器必须在建议 `isr: ...` 之前检查安装的版本。
- **`load` 中对自有 SvelteKit 路由的 `fetch` 调用。** SvelteKit 在 SSR 期间将这些优化为直接模块调用，但前提是 URL 是相对的。硬编码的 `https://your-domain.tld/api/...` 会破坏此优化。
- **Serverless 上没有连接池。** 与 Next.js 相同——没有 pooler 的 Postgres 在负载下耗尽数据库。

## 交叉引用

- `https://kit.svelte.dev/docs/adapter-vercel` — adapter 配置（ISR、regions、runtime）
- `https://kit.svelte.dev/docs/page-options` — prerender、ssr、csr
- `https://kit.svelte.dev/docs/load` — load 中的并行获取
- `https://kit.svelte.dev/docs/routing` — 文件约定
- `https://kit.svelte.dev/docs/hooks` — handle / handleFetch
- `https://kit.svelte.dev/docs/form-actions` — 服务端表单处理
- `https://kit.svelte.dev/docs/state-management` — 请求作用域状态
- `https://vercel.com/docs/incremental-static-regeneration` — Vercel 上的 ISR
- `https://vercel.com/docs/fluid-compute` — Fluid Compute（框架无关）