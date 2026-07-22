---
id: external-api-critical-path-platform
title: Cross-framework external API critical path
status: active
candidateKinds: ["external_api_slow"]
frameworks: ["*"]
priority: 86
citations: ["https://vercel.com/docs/functions/debug-slow-functions", "https://vercel.com/docs/caching/runtime-cache", "https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package"]
maxBriefChars: 850
---

## 调查简报
只有当慢的主机名在客户路由的关键路径上时，外部 API 候选才是可操作的。在建议缓存、有效负载或响应后更改之前，证明路由在等待它。

## 需要检查的证据
使用主机名延迟、调用者路由、传输字节和源 await。检查顺序调用、过宽的有效负载、重复的共享数据以及可以移到响应后的副作用。

## 何时不建议
不要缓存变更、密钥、每用户响应或未知的新鲜度契约。当上游拥有延迟时，不要归咎于 Vercel runtime。

## 验证
命名主机名、调用者路由、观察到的 p75/p95 或字节，以及阻塞响应的确切 await 或 fetch 行。