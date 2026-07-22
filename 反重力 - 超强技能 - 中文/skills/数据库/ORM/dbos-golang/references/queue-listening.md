---
title: 控制 Worker 监听的队列
impact: HIGH
impactDescription: 启用异构 worker 池
tags: queue, listen, worker, process, configuration
---

## 控制 Worker 监听的队列

使用 `ListenQueues` 让进程只从特定队列出队。这可以启用异构 worker 池。

**错误示例（所有 worker 处理所有队列）：**

```go
cpuQueue := dbos.NewWorkflowQueue(ctx, "cpu_queue")
gpuQueue := dbos.NewWorkflowQueue(ctx, "gpu_queue")

// 每个 worker 同时处理 CPU 和 GPU 任务
// CPU worker 上的 GPU 任务会失败或变慢！
dbos.Launch(ctx)
```

**正确示例（选择性监听队列）：**

```go
cpuQueue := dbos.NewWorkflowQueue(ctx, "cpu_queue")
gpuQueue := dbos.NewWorkflowQueue(ctx, "gpu_queue")

workerType := os.Getenv("WORKER_TYPE") // "cpu" 或 "gpu"

if workerType == "gpu" {
	ctx.ListenQueues(ctx, gpuQueue)
} else if workerType == "cpu" {
	ctx.ListenQueues(ctx, cpuQueue)
}

dbos.Launch(ctx)
```

`ListenQueues` 仅控制出队。CPU worker 仍可以将任务入队到 GPU 队列：

```go
// 从 CPU worker 入队到 GPU 队列
dbos.RunWorkflow(ctx, gpuTask, "data",
	dbos.WithQueue(gpuQueue.Name),
)
```

参考：[Listening to Specific Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial#listening-to-specific-queues)
