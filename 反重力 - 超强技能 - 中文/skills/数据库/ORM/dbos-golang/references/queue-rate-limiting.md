---
title: 对队列执行进行速率限制
impact: HIGH
impactDescription: 防止请求过多压垮外部 API
tags: queue, rate-limit, throttle, api
---

## 对队列执行进行速率限制

在队列上设置速率限制，以控制在给定时间段内启动多少工作流。速率限制跨所有 DBOS 进程全局生效。

**错误示例（无速率限制）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks")
// 可能每秒向有速率限制的 API 发送数百个请求
```

**正确示例（带速率限制的队列）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks",
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

此队列每 30 秒最多启动 50 个工作流。

**速率限制与并发结合：**

```go
// 最多 5 个并发，每 30 秒最多 50 个
queue := dbos.NewWorkflowQueue(ctx, "api_tasks",
	dbos.WithWorkerConcurrency(5),
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

常见使用场景：
- LLM API 速率限制（OpenAI、Anthropic 等）
- 第三方 API 节流
- 防止数据库过载

参考：[Rate Limiting](https://docs.dbos.dev/golang/tutorials/queue-tutorial#rate-limiting)
