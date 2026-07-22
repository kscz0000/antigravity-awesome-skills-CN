---
title: 设置工作流超时
impact: CRITICAL
impactDescription: 防止工作流无限期运行
tags: workflow, timeout, cancellation, duration
---

## 设置工作流超时

通过使用 Go 的 `context.WithTimeout` 或在 DBOS 上下文上使用 `dbos.WithTimeout` 为工作流设置超时。超时时，工作流及其所有子工作流都会被取消。

**错误示例（可能长时间运行的工作流没有超时）：**

```go
// 没有超时 - 可能无限期运行
handle, err := dbos.RunWorkflow(ctx, processTask, "data")
```

**正确示例（带超时）：**

```go
// 创建带 5 分钟超时的上下文
timedCtx, cancel := dbos.WithTimeout(ctx, 5*time.Minute)
defer cancel()

handle, err := dbos.RunWorkflow(timedCtx, processTask, "data")
if err != nil {
	log.Fatal(err)
}
```

关键超时行为：
- 超时是**启动到完成**：超时从工作流开始执行时计时，而不是入队时
- 超时是**持久化**的：跨重启持续生效，因此工作流可以拥有非常长的超时（小时、天、周）
- 取消发生在**下一步开始时** - 当前步骤会先完成
- 取消一个工作流也会取消其所有**子工作流**

参考：[Workflow Timeouts](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-timeouts)
