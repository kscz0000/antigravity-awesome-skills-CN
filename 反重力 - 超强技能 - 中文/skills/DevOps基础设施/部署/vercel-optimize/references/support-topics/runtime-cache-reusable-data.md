---
id: runtime-cache-reusable-data
title: Runtime Cache for reusable server data
status: active
candidateKinds: ["slow_route", "external_api_slow"]
frameworks: ["*"]
priority: 84
citations: ["https://vercel.com/docs/caching/runtime-cache", "https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package"]
maxBriefChars: 850
---

## 调查简报
仅当相同的服务器端结果跨请求被重用时，Runtime Cache 才有用。当 CDN 响应缓存不安全或不完整时，将其视为一种测量替代方案。

## 需要检查的证据
使用 p75/p95 延迟、调用计数、调用者路由和传输字节。在源代码中，识别为许多查看者返回相同结果的数据库查询、外部 API 调用或昂贵的计算。

## 何时不建议
跳过每用户数据、变更、密钥、一次性请求或未知新鲜度。当 CDN 缓存解决路由时跳过 Runtime Cache。对于带有 Cache Components 的 Next，首先检查 `use cache: remote`；仅将 Runtime Cache 用作合理的回退。

## 验证
命名可重用的数据、观察到的路由或主机名压力、所需的新鲜度窗口以及要包装的确切调用站点。