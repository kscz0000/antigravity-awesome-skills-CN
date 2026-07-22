---
title: 控制队列并发度
impact: HIGH
impactDescription: 通过并发限制防止资源耗尽
tags: queue, concurrency, workerConcurrency, limits
---

## 控制队列并发度

队列支持 worker 级和全局并发限制，以防止资源耗尽。

**错误示例（无并发控制）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "heavy_tasks") // 没有限制 - 可能耗尽内存
```

**正确示例（worker 并发）：**

```go
// 每个进程最多运行该队列的 5 个任务
queue := dbos.NewWorkflowQueue(ctx, "heavy_tasks",
	dbos.WithWorkerConcurrency(5),
)
```

**正确示例（全局并发）：**

```go
// 跨所有进程最多同时运行 10 个任务
queue := dbos.NewWorkflowQueue(ctx, "limited_tasks",
	dbos.WithGlobalConcurrency(10),
)
```

**按顺序处理（串行）：**

```go
// 一次只处理一个任务 - 保证顺序
serialQueue := dbos.NewWorkflowQueue(ctx, "sequential_queue",
	dbos.WithGlobalConcurrency(1),
)
```

大多数场景推荐使用 worker 并发。使用全局并发时需注意：队列上任何 `PENDING` 状态的工作流都计入限制，包括来自旧应用版本的工作流。

使用 worker 并发时，每个进程必须在配置中设置唯一的 `ExecutorID`（使用 DBOS Conductor 或 Cloud 时会自动设置）。

参考：[Managing Concurrency](https://docs.dbos.dev/golang/tutorials/queue-tutorial#managing-concurrency)
