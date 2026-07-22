---
title: 初始化 Client 以进行外部访问
impact: HIGH
impactDescription: 允许外部应用程序与 DBOS 工作流交互
tags: client, external, setup, initialization
---

## 初始化 Client 以进行外部访问

使用 `dbos.NewClient` 从外部应用程序（如 API 服务器、CLI 工具或独立服务）与 DBOS 交互。Client 直接连接到 DBOS 系统数据库。

**错误示例（从外部应用使用完整 DBOS 上下文）：**

```go
// 完整 DBOS 上下文需要 Launch() - 对外部 Client 来说过于重量级
ctx, _ := dbos.NewDBOSContext(context.Background(), config)
dbos.Launch(ctx)
```

**正确示例（使用 Client）：**

```go
client, err := dbos.NewClient(context.Background(), dbos.ClientConfig{
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
})
if err != nil {
	log.Fatal(err)
}
defer client.Shutdown(10 * time.Second)

// 向工作流发送消息
err = client.Send(workflowID, "notification", "topic")

// 获取工作流事件
event, err := client.GetEvent(workflowID, "status", 60*time.Second)

// 检索工作流句柄
handle, err := client.RetrieveWorkflow(workflowID)
result, err := handle.GetResult()

// 列出工作流
workflows, err := client.ListWorkflows(
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusError}),
)

// 工作流管理
err = client.CancelWorkflow(workflowID)
handle, err = client.ResumeWorkflow(workflowID)

// 读取流
values, closed, err := client.ClientReadStream(workflowID, "results")

// 异步读取流
ch, err := client.ClientReadStreamAsync(workflowID, "results")
```

ClientConfig 选项：
- `DatabaseURL`（必填，除非设置了 `SystemDBPool`）：PostgreSQL 连接字符串
- `SystemDBPool`：自定义 `*pgxpool.Pool`
- `DatabaseSchema`：Schema 名称（默认：`"dbos"`）
- `Logger`：自定义 `*slog.Logger`

使用完毕务必调用 `client.Shutdown()`。

参考：[DBOS Client](https://docs.dbos.dev/golang/reference/client)
