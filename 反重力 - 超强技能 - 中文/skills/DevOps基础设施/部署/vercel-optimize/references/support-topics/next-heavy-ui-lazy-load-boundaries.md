---
id: next-heavy-ui-lazy-load-boundaries
title: Next.js heavy UI lazy-load boundaries
status: active
candidateKinds: ["cwv_poor"]
frameworks: ["next@*"]
metrics: ["LCP", "INP"]
priority: 82
citations: ["https://nextjs.org/docs/app/guides/lazy-loading", "https://web.dev/articles/optimize-inp"]
maxBriefChars: 850
---

## 调查简报
重型首屏或很少使用的 UI 在首次加载时交付过多 JavaScript 时会损害 LCP 和 INP。查找具体的路由本地 UI，而不是通用 bundle 建议。

## 需要检查的证据
检查客户端组件、菜单、搜索覆盖层、个性化小部件、地图、编辑器和大型导入的库。检查它们是否可以使用 `next/dynamic` 或动态导入在交互、视口或路由入口上加载。

## 何时不建议
不要对初始含义或可访问性所需的首屏内容进行延迟加载。不要从 Server Component 使用 `ssr: false`。

## 验证
命名不佳的指标、重型 UI 边界、导入的库或组件以及要拆分的确切行。