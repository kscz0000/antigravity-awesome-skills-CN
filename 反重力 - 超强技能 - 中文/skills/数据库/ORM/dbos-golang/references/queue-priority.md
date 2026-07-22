---
title: 为工作流设置队列优先级
impact: HIGH
impactDescription: 让重要工作流优先于低优先级工作流
tags: queue, priority, ordering, importance
---

## 为工作流设置队列优先级

在队列上启用优先级，让高优先级工作流优先处理。数值越小表示优先级越高。

**错误示例（无优先级 - 仅 FIFO）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks")
// 无论重要性，所有任务均按 FIFO 顺序处理
```

**正确示例（启用优先级的队列）：**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithPriorityEnabled(),
)

// 高优先级任务（数值越小 = 优先级越高）
dbos.RunWorkflow(ctx, processTask, "urgent-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(1),
)

// 低优先级任务
dbos.RunWorkflow(ctx, processTask, "background-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(100),
)
```

优先级规则：
- 范围：`1` 到 `2,147,483,647`
- 数值越小 = 优先级越高
- **没有**指定优先级的工作流具有最高优先级（最先执行）
- 相同优先级的工作流按 FIFO 顺序出队

参考：[Priority](https://docs.dbos.dev/golang/tutorials/queue-tutorial#priority)
