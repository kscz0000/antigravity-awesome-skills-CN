# 内容站点

文档、博客、知识库、营销相邻的内容，主要是静态页面。创作可能是 headless CMS 驱动或仓库内 markdown。

## 典型计费形态

边缘请求主导（每个页面查看都是一个边缘请求；静态资产更多）。图像优化通常是第二项。函数时长往往较低——大多数页面应该是静态或 ISR。

## 优先级模式

1. **预渲染所有可以预渲染的内容。** 博客索引、单篇文章、文档页面、分类页面。对 App Router 使用 `generateStaticParams`，对 Pages Router 使用 `getStaticPaths`。任何 CMS 驱动的内容都应在 webhook 重新验证上运行，而不是每个请求。
2. **具有合理节奏的 ISR。** 需要相对新鲜内容但不需要实时准确性的页面走 ISR。`revalidate: 3600`（每小时）是文档的一个良好起点；博客索引页面为 `60s`。
3. **`next/image` 用于每个图像资产。** Hero 图像、作者照片、文章内联图像、OG 图像。即使是仅缩略图的网站也受益于格式协商（WebP/AVIF）。
4. **`next/font` 用于自托管字体。** 消除 FOIT/FOUT，消除第三方请求，防止 CLS。
5. **悬停时预取。** `next/link` 默认这样做。对于其他框架，考虑在可见的链接集上基于 intersection-observer 的预取。

## 常见陷阱

- **博客索引上的 `force-dynamic`。** 几乎从来没必要。索引可以 ISR 或完全静态。
- **每个请求的 Markdown 渲染。** 如果你在请求时解析 MDX，你将在本应是静态资产的内容上支付函数时长成本。构建时 MDX → 静态 HTML。
- **每个请求重建搜索。** 由函数支持的站点搜索，每次按键查询 CMS。改为使用搜索索引（Algolia、Pagefind、构建时生成）并从 CDN 提供服务。
- **CMS 预览路由泄漏到生产流量。** 一个 `/preview/[slug]` 路由实际上是另一个渲染路径；有时会因错误从生产调用。审查引用来源。

## 交叉引用

- `https://nextjs.org/docs/app/api-reference/functions/generate-static-params` — 用于预渲染
- `https://vercel.com/docs/incremental-static-regeneration` — 用于 ISR 修复
- `https://nextjs.org/docs/app/api-reference/components/image` — 图像优化
- `https://nextjs.org/docs/app/api-reference/components/font` — 自托管字体
- `vercel-react-best-practices:bundle-defer-third-party` — 延迟分析/cookie 横幅