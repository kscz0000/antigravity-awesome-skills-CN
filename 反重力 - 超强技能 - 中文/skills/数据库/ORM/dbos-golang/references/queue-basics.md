---
title: 使用队列管理并发工作流
impact: HIGH
impactDescription: 队列提供受控的并发与流量管理
tags: queue, concurrency, enqueue, workflow
---

## 使用队列管理并发工作流

队列以受控的流量管理方式并发运行大量工作流。当你需要控制同时运行的工作流数量时，应使用队列。

**错误示例（不受控的并发）：**

```go
// 不加控制地启动大量工作流 - 可能压垮资源
for _, task := range tasks {
	dbos.RunWorkflow(ctx, processTask, task)
}
```

**正确示例（使用队列）：**

```go
// 在 Launch() 之前创建队列
queue := dbos.NewWorkflowQueue(ctx, "task_queue")

func processAllTasks(ctx dbos.DBOSContext, tasks []string) ([]string, error) {
	var handles []dbos.WorkflowHandle[string]
	for _, task := range tasks {
		handle, err := dbos.RunWorkflow(ctx, processTask, task,
			dbos.WithQueue(queue.Name),
		)
		if err != nil {
			return nil, err
		}
		handles = append(handles, handle)
	}
	// 等待所有任务完成
	var results []string
	for _, h := range handles {
		result, err := h.GetResult()
		if err != nil {
			return nil, err
		}
		results = append(results, result)
	}
	return results, nil
}
```

队列按 FIFO 顺序处理工作流。所有队列必须在 `Launch()` 之前通过 `dbos.NewWorkflowQueue` 创建。

参考：[DBOS Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial)
