---
title: 使用消息进行工作流通知
impact: MEDIUM
impactDescription: 支持可靠的工作流间和外部到工作流通信
tags: communication, messages, send, recv, notification
---

## 使用消息进行工作流通知

使用 `DBOS.send` 向工作流发送消息，使用 `DBOS.recv` 接收消息。消息按主题排队并持久化，确保可靠投递。

**错误（使用外部消息系统进行工作流通信）：**

```typescript
// 外部消息队列未与工作流恢复集成
import { Queue } from "some-external-queue";
```

**正确（使用 DBOS 消息）：**

```typescript
async function checkoutWorkflowFn() {
  // 等待支付通知（超时 120 秒）
  const notification = await DBOS.recv<string>("payment_status", 120);

  if (notification && notification === "paid") {
    await DBOS.runStep(fulfillOrder, { name: "fulfillOrder" });
  } else {
    await DBOS.runStep(cancelOrder, { name: "cancelOrder" });
  }
}
const checkoutWorkflow = DBOS.registerWorkflow(checkoutWorkflowFn);

// 从 webhook 处理器发送消息
async function paymentWebhook(workflowID: string, status: string) {
  await DBOS.send(workflowID, status, "payment_status");
}
```

关键行为：
- `recv` 等待并消费指定主题的下一条消息
- 若等待超时则返回 `null`（默认超时：60 秒）
- 没有主题的消息只能被没有主题的 `recv` 接收
- 消息按主题排队（FIFO）

**可靠性保证：**
- 所有消息都持久化到数据库
- 从工作流内发送的消息精确投递一次
- 从非工作流代码发送的消息可使用幂等性键：

```typescript
await DBOS.send(workflowID, message, "topic", "idempotency-key-123");
```

参考：[Workflow Messaging](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-messaging-and-notifications)
