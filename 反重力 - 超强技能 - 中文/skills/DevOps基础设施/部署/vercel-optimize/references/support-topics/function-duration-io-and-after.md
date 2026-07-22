---
id: function-duration-io-and-after
title: Function duration, I/O, and post-response work
status: active
candidateKinds: ["slow_route"]
frameworks: ["next@>=15.0.0"]
priority: 75
citations: ["https://nextjs.org/docs/app/api-reference/functions/after", "vercel-react-best-practices:async-parallel", "vercel-react-best-practices:server-after-nonblocking"]
maxBriefChars: 850
---

## 调查简报
当墙钟延迟远高于 CPU 时间时，在归咎于渲染或计算之前检查关键路径 await。

## 需要检查的证据
比较 `cpu.p95`、`ttfb.p95` 和 `latency.p95`。在源代码中，将依赖 await 与独立 await 分离，并识别可以在响应后运行的分析、日志记录或通知工作。

## 何时不建议
不要将依赖操作包装在 `Promise.all` 中。当部分失败处理是有意的时候，不要替换 `Promise.allSettled`。

## 验证
命名可以移动的 await、可以在响应后运行的工作，以及观察到的 CPU 与墙钟对比 gap。