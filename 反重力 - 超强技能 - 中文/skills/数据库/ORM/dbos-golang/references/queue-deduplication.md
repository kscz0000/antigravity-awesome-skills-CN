---
title: 对入队工作流去重
impact: HIGH
impactDescription: 防止重复执行工作流
tags: queue, deduplication, idempotent, duplicate
---

## 对入队工作流去重

入队时设置去重 ID 可防止重复执行工作流。如果已存在具有相同去重 ID 的入队或执行中的工作流，将返回 code 为 `QueueDeduplicated` 的 `DBOSError`。

**错误示例（没有去重）：**

```go
// 多次调用可能入队重复任务
func handleClick(ctx dbos.DBOSContext, userID, task string) error {
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
	)
	return err
}
```

**正确示例（使用去重）：**

```go
func handleClick(ctx dbos.DBOSContext, userID, task string) error {
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
		dbos.WithDeduplicationID(userID),
	)
	if err != nil {
		// 检查是否被去重
		var dbosErr *dbos.DBOSError
		if errors.As(err, &dbosErr) && dbosErr.Code == dbos.QueueDeduplicated {
			fmt.Println("Task already in progress for user:", userID)
			return nil
		}
		return err
	}
	return nil
}
```

去重按队列进行。去重 ID 在工作流状态为 `ENQUEUED` 或 `PENDING` 时生效。工作流完成后，相同去重 ID 的新工作流可以再次入队。

适用场景：
- 确保每个用户只有一个活跃任务
- 防止重复表单提交
- 幂等的事件处理

参考：[Deduplication](https://docs.dbos.dev/golang/tutorials/queue-tutorial#deduplication)
