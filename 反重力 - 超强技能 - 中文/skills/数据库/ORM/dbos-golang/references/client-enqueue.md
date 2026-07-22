---
title: 从外部应用程序入队工作流
impact: HIGH
impactDescription: 允许外部服务向 DBOS 队列提交任务
tags: client, enqueue, external, queue
---

## 从外部应用程序入队工作流

使用 `client.Enqueue()` 从 DBOS 应用程序外部提交工作流。由于 Client 在外部运行，工作流和队列的元数据必须通过名称显式指定。

**错误示例（尝试从外部代码使用 RunWorkflow）：**

```go
// RunWorkflow 需要带有已注册工作流的完整 DBOS 上下文
dbos.RunWorkflow(ctx, processTask, "data", dbos.WithQueue("myQueue"))
```

**正确示例（使用 Client.Enqueue）：**

```go
client, err := dbos.NewClient(context.Background(), dbos.ClientConfig{
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
})
if err != nil {
	log.Fatal(err)
}
defer client.Shutdown(10 * time.Second)

// 基本入队 - 按名称指定工作流和队列
handle, err := client.Enqueue("task_queue", "processTask", "task-data")
if err != nil {
	log.Fatal(err)
}

// 等待结果
result, err := handle.GetResult()
```

**带选项的入队：**

```go
handle, err := client.Enqueue("task_queue", "processTask", "task-data",
	dbos.WithEnqueueWorkflowID("custom-id"),
	dbos.WithEnqueueDeduplicationID("unique-id"),
	dbos.WithEnqueuePriority(10),
	dbos.WithEnqueueTimeout(5*time.Minute),
	dbos.WithEnqueueQueuePartitionKey("user-123"),
	dbos.WithEnqueueApplicationVersion("2.0.0"),
)
```

入队选项：
- `WithEnqueueWorkflowID`：自定义工作流 ID
- `WithEnqueueDeduplicationID`：防止重复入队
- `WithEnqueuePriority`：队列优先级（数值越小优先级越高）
- `WithEnqueueTimeout`：工作流超时
- `WithEnqueueQueuePartitionKey`：分区队列的分区键
- `WithEnqueueApplicationVersion`：覆盖应用版本

工作流名称必须与注册时的名称或通过 `WithWorkflowName` 设置的自定义名称一致。

使用完毕务必调用 `client.Shutdown()`。

参考：[DBOS Client Enqueue](https://docs.dbos.dev/golang/reference/client#enqueue)
