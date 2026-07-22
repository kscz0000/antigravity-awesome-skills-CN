---
title: 为队列分区以实施按实体限制
impact: HIGH
impactDescription: 支持按实体的并发控制
tags: queue, partition, per-user, dynamic
---

## 为队列分区以实施按实体限制

分区队列对每个分区键（而不是整个队列）应用流量控制限制。每个分区相当于一个动态的"子队列"。

**错误示例（按用户的限制使用了全局并发）：**

```go
// 全局并发=1 会阻塞所有用户，而不是按用户限制
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithGlobalConcurrency(1),
)
```

**正确示例（分区队列）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithPartitionQueue(),
	dbos.WithGlobalConcurrency(1),
)

func onUserTask(ctx dbos.DBOSContext, userID, task string) error {
	// 每个用户拥有自己的分区 - 每用户最多 1 个任务
	// 但不同用户的任务可以并发执行
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
		dbos.WithQueuePartitionKey(userID),
	)
	return err
}
```

当队列启用 `WithPartitionQueue()` 时，入队时**必须**提供 `WithQueuePartitionKey()`。分区键与去重 ID 不能同时使用。

参考：[Partitioning Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial#partitioning-queues)
