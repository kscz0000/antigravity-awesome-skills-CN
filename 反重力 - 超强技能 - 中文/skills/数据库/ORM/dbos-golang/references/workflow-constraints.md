---
title: 遵守工作流约束
impact: CRITICAL
impactDescription: 违反约束会破坏恢复机制与持久化保证
tags: workflow, constraints, rules, best-practices
---

## 遵守工作流约束

工作流有特定的约束以维持持久化保证。违反它们会破坏恢复机制。

**错误示例（从步骤中启动工作流）：**

```go
func myStep(ctx context.Context) (string, error) {
	// 不要从步骤启动工作流！
	// 步骤的 context.Context 不支持工作流操作
	return "", nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 在步骤中启动子工作流会破坏确定性
	dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		handle, _ := dbos.RunWorkflow(ctx.(dbos.DBOSContext), otherWorkflow, "data") // 错误
		return handle.GetWorkflowID(), nil
	})
	return "", nil
}
```

**正确示例（仅在工作流中执行工作流操作）：**

```go
func fetchData(ctx context.Context) (string, error) {
	// 步骤只做外部操作
	resp, err := http.Get("https://api.example.com")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	// 从父工作流中启动子工作流
	handle, err := dbos.RunWorkflow(ctx, otherWorkflow, data)
	if err != nil {
		return "", err
	}
	// 在工作流中接收消息
	msg, err := dbos.Recvstring
	// 在工作流中设置事件
	dbos.SetEvent(ctx, "status", "done")
	return data, nil
}
```

其他约束：
- 不要在工作流或步骤中修改全局变量
- 所有工作流和队列必须在 `Launch()` **之前**注册
- 并发步骤必须使用 `dbos.Go`/`dbos.Select` 按确定性顺序启动

参考：[Workflow Guarantees](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-guarantees)
