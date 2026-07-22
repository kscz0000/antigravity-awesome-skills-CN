---
id: cache-components-static-shell-boundaries
title: Cache Components static shell boundaries
status: active
candidateKinds: ["rendering_candidate"]
frameworks: ["next@>=16.0.0"]
priority: 94
citations: ["https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents", "https://nextjs.org/docs/app/getting-started/caching", "https://nextjs.org/docs/app/guides/migrating-to-cache-components"]
maxBriefChars: 900
---

## 调查简报
在带有 Cache Components 的 Next.js 16 上，避免较旧的段配置建议。正确的问题是路由是否可以在动态数据移到显式缓存或运行时边界之后保持静态外壳。

## 需要检查的证据
检查 `cacheComponents`、`use cache`、`cacheLife`、请求时 API、Suspense 边界以及扫描器证据（如 `force-dynamic` 或 `headers-in-page`）。

## 何时不建议
当启用 Cache Components 时，不要建议 `dynamic`、`revalidate` 或 `fetchCache` 作为主要修复。不要缓存请求个性化的内容。

## 验证
命名 Next.js 版本、Cache Components 状态、动态触发器以及可以更改的确切边界或指令。