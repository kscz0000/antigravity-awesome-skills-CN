---
id: use-cache-remote-shared-origin-data
title: Remote cache for shared origin data
status: active
candidateKinds: ["external_api_slow", "slow_route", "uncached_route"]
frameworks: ["next@>=16.0.0"]
priority: 87
citations: ["https://vercel.com/docs/caching/runtime-cache", "https://nextjs.org/docs/app/api-reference/directives/use-cache-remote"]
maxBriefChars: 950
---

## 调查简报
对于 Next 16 候选，检查共享的源数据或可重用的路由处理器工作是否属于远程缓存。在 Vercel 上默认的 `'use cache'` 不是跨请求的。使用 `'use cache: remote'` 或 `generateStaticParams`。

## 需要检查的证据
主机名 p75、调用者路由、调用计数、字节。验证数据是共享的并能容忍新鲜度窗口。确认 `'use cache: remote'`。

## 何时不建议
跳过每用户、变更、密钥或新鲜度关键的数据。上游快或很少调用时跳过。避免亚毫秒读取（Edge Config）——开销超过源延迟。

## 验证
命名主机名、共享数据、新鲜度窗口以及确切边界。声明 `'use cache: remote'`。