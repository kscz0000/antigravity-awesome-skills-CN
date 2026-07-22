---
title: 使用 Messages 进行工作流通知
impact: MEDIUM
impactDescription: 启用可靠的工作流间及外部到工作流的通信
tags: communication, messages, send, recv, notification
---

## 使用 Messages 进行工作流通知

使用 `dbos.Send` 向工作流发送消息，使用 `dbos.Recv` 接收消息。消息按主题排队并持久化，保证可靠投递。

**错误示例（使用外部消息队列进行工作流通信）：**

```go
// 外部消息队列未与工作流恢复集成
ch := make(chan string) // 不具备持久性！
```

**正确示例（使用 DBOS 消息）：**

```go
func checkoutWorkflow(ctx dbos.DBOSContext, orderID string) (string, error) {
	// 等待支付通知（超时 120 秒）
	notification, err := dbos.Recvstring
	if err != nil {
		return "", err
	}

	if notification == "paid" {
		_, err = dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return fulfillOrder(orderID)
		}, dbos.WithStepName("fulfillOrder"))
		return "fulfilled", err
	}
	_, err = dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return cancelOrder(orderID)
	}, dbos.WithStepName("cancelOrder"))
	return "cancelled", err
}

// 从 webhook 处理器发送消息
func paymentWebhook(ctx dbos.DBOSContext, workflowID, status string) error {
	return dbos.Send(ctx, workflowID, status, "payment_status")
}
```

关键行为：
- `Recv` 等待并消费指定主题的下一条消息
- 若等待超时，返回零值，并附带 code 为 `TimeoutError` 的 `DBOSError`
- 没有主题的消息只能被没有主题的 `Recv` 接收
- 消息按主题排队（FIFO）

**可靠性保证：**
- 所有消息持久化到数据库
- 从工作流发送的消息保证恰好投递一次

参考：[Workflow Messaging and Notifications](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-messaging-and-notifications)
