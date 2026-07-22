---
id: post-response-work-waituntil
title: Post-response work with waitUntil
status: active
candidateKinds: ["slow_route", "external_api_slow"]
frameworks: ["next@<15.0.0", "sveltekit@*", "astro@*", "nuxt@*", "unknown@*"]
priority: 78
citations: ["https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package"]
maxBriefChars: 800
---

## 调查简报
对于没有 Next.js `after()` 的栈，检查非关键工作是否可以在响应后运行，而不是延长用户可见的延迟。

## 需要检查的证据
检查列出的路由中在响应数据准备好之后发生的分析、日志记录、通知、缓存预热、指标或 webhook 副作用。

## 何时不建议
不要移动决定响应、必须使请求失败、同步更改可见状态或需要持久重试保证的工作。

## 验证
命名阻塞的副作用、观察到的延迟或上游信号，以及可以移到 `waitUntil` 后面的确切行。