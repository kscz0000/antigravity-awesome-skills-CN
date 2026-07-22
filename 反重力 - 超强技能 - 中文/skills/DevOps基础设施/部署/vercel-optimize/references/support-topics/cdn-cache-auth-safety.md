---
id: cdn-cache-auth-safety
title: CDN cache auth safety
status: active
candidateKinds: ["uncached_route", "cache_header_gap"]
frameworks: ["*"]
priority: 100
citations: ["https://vercel.com/docs/caching/cdn-cache", "https://vercel.com/docs/caching/cache-control-headers", "https://vercel.com/docs/project-configuration"]
maxBriefChars: 900
---

## 调查简报
将边缘缓存视为安全问题。在允许共享缓存建议之前，路由必须是公共的、可缓存的 GET 路径。

## 需要检查的证据
使用 `methodDistribution`、`cacheBreakdown` 和头。在 `s-maxage` 之前，排除 cookies、会话、授权、草稿状态和用户特定数据。

## 何时不建议
不要缓存变更、仪表板、账户数据、请求个性化的响应或每个查看者价值变化的路由。不要将 `private` 与共享缓存指令混合。

## 验证
命名 GET 份额、缓存混合、文件行和策略：机制、范围、TTL/新鲜度以及 `Vary`。如果正确的策略是 `no-store`，发出无改动/观察。