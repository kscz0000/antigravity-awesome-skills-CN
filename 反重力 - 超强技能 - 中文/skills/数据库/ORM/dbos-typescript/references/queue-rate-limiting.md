---
title: 限制队列执行速率
impact: HIGH
impactDescription: 防止请求过多压垮外部 API
tags: queue, rate-limit, throttle, api
---

## 限制队列执行速率

在队列上设置速率限制，以控制在给定时间段内启动多少个工作流。速率限制在所有 DBOS 进程中全局生效。

**错误（无速率限制）：**

```typescript
const queue = new WorkflowQueue("llm_tasks");
// 可能每秒向受速率限制的 API 发送数百个请求
```

**正确（带速率限制的队列）：**

```typescript
const queue = new WorkflowQueue("llm_tasks", {
  rateLimit: { limitPerPeriod: 50, periodSec: 30 },
});
```

该队列每 30 秒最多启动 50 个工作流。

**结合速率限制与并发：**

```typescript
// 最多 5 个并发 且 每 30 秒 50 个
const queue = new WorkflowQueue("api_tasks", {
  workerConcurrency: 5,
  rateLimit: { limitPerPeriod: 50, periodSec: 30 },
});
```

常见使用场景：
- LLM API 速率限制（OpenAI、Anthropic 等）
- 第三方 API 节流
- 防止数据库过载

参考：[Rate Limiting](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#rate-limiting)
