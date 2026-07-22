---
title: 在后台启动工作流
impact: CRITICAL
impactDescription: 后台工作流支持可靠的异步处理
tags: workflow, background, handle, async
---

## 在后台启动工作流

使用 `dbos.RunWorkflow` 启动一个工作流并获取跟踪用的句柄。即使应用被中断，该工作流也保证会运行到完成。

**错误示例（无法跟踪后台工作）：**

```go
func processData(ctx dbos.DBOSContext, data string) (string, error) {
	// ...
	return "processed: " + data, nil
}

// 在 goroutine 中 fire-and-forget - 没有持久性，无法跟踪
go func() {
	processData(ctx, data)
}()
```

**正确示例（使用 RunWorkflow）：**

```go
func processData(ctx dbos.DBOSContext, data string) (string, error) {
	return "processed: " + data, nil
}

func main() {
	// ... 初始化并启动 ...

	// 启动工作流，获取句柄
	handle, err := dbos.RunWorkflow(ctx, processData, "input")
	if err != nil {
		log.Fatal(err)
	}

	// 获取工作流 ID
	fmt.Println(handle.GetWorkflowID())

	// 等待结果
	result, err := handle.GetResult()

	// 检查状态
	status, err := handle.GetStatus()
}
```

之后通过工作流 ID 重新获取句柄：

```go
handle, err := dbos.RetrieveWorkflowstring
result, err := handle.GetResult()
```

`GetResult` 支持以下选项：
- `dbos.WithHandleTimeout(timeout)`：若工作流在指定时间内未完成则返回超时错误
- `dbos.WithHandlePollingInterval(interval)`：控制数据库轮询完成的频率

参考：[Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial)
