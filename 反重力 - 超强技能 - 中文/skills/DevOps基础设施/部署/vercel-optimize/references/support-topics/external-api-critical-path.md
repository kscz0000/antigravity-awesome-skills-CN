---
id: external-api-critical-path
title: External API critical path
status: active
candidateKinds: ["external_api_slow"]
frameworks: ["next@>=13.0.0"]
priority: 90
citations: ["vercel-react-best-practices:async-parallel", "vercel-react-best-practices:server-parallel-fetching", "vercel-react-best-practices:server-cache-react"]
maxBriefChars: 850
---

## 调查简报
对于外部 API 候选，识别等待慢主机名的客户路由，以及该调用是否在关键路径上。

## 需要检查的证据
使用调用者路由证据、传输大小和源 await。检查上游调用是否可以并行运行、安全地缓存、减少有效负载大小或移到响应后。

## 何时不建议
不要缓存变更、密钥、每用户响应或新鲜度需求未知的上游调用。

## 验证
命名主机名、调用者路由、p75 或 p95 延迟，以及等待该调用的确切源行。