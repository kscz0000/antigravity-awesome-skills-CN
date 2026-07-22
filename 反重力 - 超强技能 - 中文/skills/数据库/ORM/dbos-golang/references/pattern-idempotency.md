---
title: 使用工作流 ID 实现幂等性
impact: MEDIUM
impactDescription: 防止重复扣款等重复副作用
tags: pattern, idempotency, workflow-id, deduplication
---

## 使用工作流 ID 实现幂等性

为工作流分配 ID 可确保工作流即使被多次调用也只执行一次，从而避免重复扣款等重复副作用。

**错误示例（没有幂等性）：**

```go
func processPayment(ctx dbos.DBOSContext, orderID string) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return chargeCard(orderID)
	}, dbos.WithStepName("chargeCard"))
	return "charged", err
}

// 多次调用可能导致重复扣款！
dbos.RunWorkflow(ctx, processPayment, "order-123")
dbos.RunWorkflow(ctx, processPayment, "order-123") // 重复扣款！
```

**正确示例（使用工作流 ID）：**

```go
func processPayment(ctx dbos.DBOSContext, orderID string) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return chargeCard(orderID)
	}, dbos.WithStepName("chargeCard"))
	return "charged", err
}

// 相同的工作流 ID = 仅执行一次
workflowID := fmt.Sprintf("payment-%s", orderID)
dbos.RunWorkflow(ctx, processPayment, "order-123",
	dbos.WithWorkflowID(workflowID),
)
dbos.RunWorkflow(ctx, processPayment, "order-123",
	dbos.WithWorkflowID(workflowID),
)
// 第二次调用返回第一次执行的结果
```

在工作流内部访问当前工作流 ID：

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	currentID, err := dbos.GetWorkflowID(ctx)
	if err != nil {
		return "", err
	}
	fmt.Printf("Running workflow: %s\n", currentID)
	return input, nil
}
```

工作流 ID 在你的应用程序中必须**全局唯一**。未设置时，会自动生成一个随机 UUID。

参考：[Workflow IDs and Idempotency](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-ids-and-idempotency)
