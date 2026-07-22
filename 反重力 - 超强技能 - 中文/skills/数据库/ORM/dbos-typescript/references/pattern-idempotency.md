---
title: 使用工作流 ID 实现幂等性
impact: MEDIUM
impactDescription: 防止重复的副作用（如重复扣款）
tags: pattern, idempotency, workflow-id, deduplication
---

## 使用工作流 ID 实现幂等性

分配工作流 ID 以确保工作流只执行一次，即使被多次调用。这可防止重复的副作用（如重复扣款）。

**错误（无幂等性）：**

```typescript
async function processPaymentFn(orderId: string, amount: number) {
  await DBOS.runStep(() => chargeCard(amount), { name: "chargeCard" });
  await DBOS.runStep(() => updateOrder(orderId), { name: "updateOrder" });
}
const processPayment = DBOS.registerWorkflow(processPaymentFn);

// 多次调用可能多次扣款！
await processPayment("order-123", 50);
await processPayment("order-123", 50); // 重复扣款！
```

**正确（使用工作流 ID）：**

```typescript
async function processPaymentFn(orderId: string, amount: number) {
  await DBOS.runStep(() => chargeCard(amount), { name: "chargeCard" });
  await DBOS.runStep(() => updateOrder(orderId), { name: "updateOrder" });
}
const processPayment = DBOS.registerWorkflow(processPaymentFn);

// 相同的工作流 ID = 只执行一次
const workflowID = `payment-${orderId}`;
await DBOS.startWorkflow(processPayment, { workflowID })("order-123", 50);
await DBOS.startWorkflow(processPayment, { workflowID })("order-123", 50);
// 第二次调用返回第一次执行的结果
```

在工作流内部访问当前工作流 ID：

```typescript
async function myWorkflowFn() {
  const currentID = DBOS.workflowID;
  console.log(`Running workflow: ${currentID}`);
}
```

工作流 ID 必须在你的应用中**全局唯一**。如果未设置，会生成随机 UUID。

参考：[Workflow IDs and Idempotency](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-ids-and-idempotency)
