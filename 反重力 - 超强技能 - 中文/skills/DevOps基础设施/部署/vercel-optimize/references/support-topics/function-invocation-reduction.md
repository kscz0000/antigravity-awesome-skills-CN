---
id: function-invocation-reduction
title: Function invocation reduction
status: active
candidateKinds: ["slow_route"]
frameworks: ["next@>=13.0.0"]
priority: 70
citations: ["https://react.dev/reference/react/cache", "vercel-react-best-practices:server-parallel-fetching", "vercel-react-best-practices:server-cache-react"]
maxBriefChars: 850
---

## 调查简报
对于慢路由，在推荐合并或记忆化之前，证明列出的文件中存在重复的请求内工作。

## 需要检查的证据
查找重复的 await、重复的 fetch、同应用的路由处理器调用以及每个请求运行多次的辅助函数。

## 何时不建议
不要折叠由不同客户端独立调用的端点。不要持续缓存用户特定数据。除非跟踪/跨度证据显示有等待时间可以重叠，否则不要为 CPU 密集型或编译密集型工作推荐 `Promise.all`。靠近 `latency.p95` 的高 `cpu.p95` 是警告标志，而不是延迟胜利的证明。

## 验证
引用重复的调用站点及其 `latency.p95`、`cpu.p95` 或请求计数证据。如果修复重叠 await，请引用测得的辅助函数/跨度时间或声明影响未测量。