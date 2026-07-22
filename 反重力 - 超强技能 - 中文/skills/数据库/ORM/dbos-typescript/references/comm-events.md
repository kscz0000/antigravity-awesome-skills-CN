---
title: 使用事件发布工作流状态
impact: MEDIUM
impactDescription: 支持实时进度监控和交互式工作流
tags: communication, events, status, key-value
---

## 使用事件发布工作流状态

工作流可通过 `DBOS.setEvent` 发布事件（键值对）。其他代码可通过 `DBOS.getEvent` 读取事件。事件被持久化，可用于实时进度监控。

**错误（使用外部状态跟踪进度）：**

```typescript
let progress = 0; // 全局变量 - 不持久！

async function processDataFn() {
  progress = 50; // 未持久化，重启时丢失
}
const processData = DBOS.registerWorkflow(processDataFn);
```

**正确（使用事件）：**

```typescript
async function processDataFn() {
  await DBOS.setEvent("status", "processing");
  await DBOS.runStep(stepOne, { name: "stepOne" });
  await DBOS.setEvent("progress", 50);
  await DBOS.runStep(stepTwo, { name: "stepTwo" });
  await DBOS.setEvent("progress", 100);
  await DBOS.setEvent("status", "complete");
}
const processData = DBOS.registerWorkflow(processDataFn);

// 从工作流外部读取事件
const status = await DBOS.getEvent<string>(workflowID, "status", 0);
const progress = await DBOS.getEvent<number>(workflowID, "progress", 0);
// 若事件在超时时间内（默认 60s）不存在则返回 null
```

事件对交互式工作流非常有用。例如，结账工作流可以发布支付 URL 供调用方重定向：

```typescript
async function checkoutWorkflowFn() {
  const paymentURL = await DBOS.runStep(createPayment, { name: "createPayment" });
  await DBOS.setEvent("paymentURL", paymentURL);
  // 继续处理...
}
const checkoutWorkflow = DBOS.registerWorkflow(checkoutWorkflowFn);

// HTTP 处理器启动工作流并读取支付 URL
const handle = await DBOS.startWorkflow(checkoutWorkflow)();
const url = await DBOS.getEvent<string>(handle.workflowID, "paymentURL", 300);
```

参考：[Workflow Events](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-events)
