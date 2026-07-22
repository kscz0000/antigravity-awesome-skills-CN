---
id: nextjs-version-cache-semantics
title: Next.js cache semantics by version
status: active
candidateKinds: ["uncached_route"]
frameworks: ["next@>=15.0.0"]
priority: 85
citations: ["https://nextjs.org/docs/app/api-reference/directives/use-cache", "https://nextjs.org/docs/app/api-reference/functions/cacheLife", "https://nextjs.org/docs/app/building-your-application/caching"]
maxBriefChars: 800
---

## 调查简报
在 Next.js 15+ 上，将修复与已在使用的缓存原语相匹配。

## 需要检查的证据
检查 `'use cache'`、`cacheLife`、`cacheTag`、`fetch` 缓存选项、路由处理器和动态 API。

## 何时不建议
不要建议已检测到的 Next.js 版本之外的 API。不要声称 `cacheLife()` 发出 CDN `Cache-Control` 头或单独缺少 `cacheLife()` 会使 `'use cache'` 路由按请求运行。省略的 `cacheLife()` 调用使用默认配置文件。

## 验证
命名已检测到的 Next.js 版本以及确切的缓存原语或路由头。