---
title: 使用 Events 发布工作流状态
impact: MEDIUM
impactDescription: 启用实时进度监控和交互式工作流
tags: communication, events, status, key-value
---

## 使用 Events 发布工作流状态

工作流可以通过 `dbos.SetEvent` 发布事件（键值对）。其他代码通过 `dbos.GetEvent` 读取事件。事件被持久化，对实时进度监控非常有用。

**错误示例（使用外部状态记录进度）：**

```go
var progress int // 全局变量 - 不具备持久性！

func processData(ctx dbos.DBOSContext, input string) (string, error) {
	progress = 50 // 未持久化，重启后丢失
	return input, nil
}
```

**正确示例（使用 events）：**

```go
func processData(ctx dbos.DBOSContext, input string) (string, error) {
	dbos.SetEvent(ctx, "status", "processing")
	_, err := dbos.RunAsStep(ctx, stepOne, dbos.WithStepName("stepOne"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "progress", 50)
	_, err = dbos.RunAsStep(ctx, stepTwo, dbos.WithStepName("stepTwo"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "progress", 100)
	dbos.SetEvent(ctx, "status", "complete")
	return "done", nil
}

// 从工作流外部读取事件
status, err := dbos.GetEventstring
progress, err := dbos.GetEventint
```

事件在交互式工作流中非常有用。例如，结账工作流可以发布支付 URL 供调用方重定向：

```go
func checkoutWorkflow(ctx dbos.DBOSContext, order Order) (string, error) {
	paymentURL, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return createPayment(order)
	}, dbos.WithStepName("createPayment"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "paymentURL", paymentURL)
	// 继续处理...
	return "success", nil
}

// HTTP 处理器启动工作流并读取支付 URL
handle, _ := dbos.RunWorkflow(ctx, checkoutWorkflow, order)
url, _ := dbos.GetEventstring, "paymentURL", 300*time.Second)
```

`GetEvent` 会阻塞，直到事件被设置或超时。若超时则返回该类型的零值。

参考：[Workflow Events](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-events)
