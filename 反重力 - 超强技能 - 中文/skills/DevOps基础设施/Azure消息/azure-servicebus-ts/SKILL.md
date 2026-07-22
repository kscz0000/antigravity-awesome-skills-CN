---
name: azure-servicebus-ts
description: "使用队列、主题和订阅进行企业级消息传递。当用户要求'Azure Service Bus消息队列'、'Service Bus主题订阅'、'TypeScript消息传递'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Service Bus SDK for TypeScript

使用队列、主题和订阅进行企业级消息传递。

## 安装

```bash
npm install @azure/service-bus @azure/identity
```

## 环境变量

```bash
SERVICEBUS_NAMESPACE=<namespace>.servicebus.windows.net
SERVICEBUS_QUEUE_NAME=my-queue
SERVICEBUS_TOPIC_NAME=my-topic
SERVICEBUS_SUBSCRIPTION_NAME=my-subscription
```

## 身份认证

```typescript
import { ServiceBusClient } from "@azure/service-bus";
import { DefaultAzureCredential } from "@azure/identity";

const fullyQualifiedNamespace = process.env.SERVICEBUS_NAMESPACE!;
const client = new ServiceBusClient(fullyQualifiedNamespace, new DefaultAzureCredential());
```

## 核心工作流

### 向队列发送消息

```typescript
const sender = client.createSender("my-queue");

// Single message
await sender.sendMessages({
  body: { orderId: "12345", amount: 99.99 },
  contentType: "application/json",
});

// Batch messages
const batch = await sender.createMessageBatch();
batch.tryAddMessage({ body: "Message 1" });
batch.tryAddMessage({ body: "Message 2" });
await sender.sendMessages(batch);

await sender.close();
```

### 从队列接收消息

```typescript
const receiver = client.createReceiver("my-queue");

// Receive batch
const messages = await receiver.receiveMessages(10, { maxWaitTimeInMs: 5000 });
for (const message of messages) {
  console.log(`Received: ${message.body}`);
  await receiver.completeMessage(message);
}

await receiver.close();
```

### 订阅消息（事件驱动）

```typescript
const receiver = client.createReceiver("my-queue");

const subscription = receiver.subscribe({
  processMessage: async (message) => {
    console.log(`Processing: ${message.body}`);
    // Message auto-completed on success
  },
  processError: async (args) => {
    console.error(`Error: ${args.error}`);
  },
});

// Stop after some time
setTimeout(async () => {
  await subscription.close();
  await receiver.close();
}, 60000);
```

### 主题与订阅

```typescript
// Send to topic
const topicSender = client.createSender("my-topic");
await topicSender.sendMessages({
  body: { event: "order.created", data: { orderId: "123" } },
  applicationProperties: { eventType: "order.created" },
});

// Receive from subscription
const subscriptionReceiver = client.createReceiver("my-topic", "my-subscription");
const messages = await subscriptionReceiver.receiveMessages(10);
```

## 消息会话

```typescript
// Send session message
const sender = client.createSender("session-queue");
await sender.sendMessages({
  body: { step: 1, data: "First step" },
  sessionId: "workflow-123",
});

// Receive session messages
const sessionReceiver = await client.acceptSession("session-queue", "workflow-123");
const messages = await sessionReceiver.receiveMessages(10);

// Get/set session state
const state = await sessionReceiver.getSessionState();
await sessionReceiver.setSessionState(Buffer.from(JSON.stringify({ progress: 50 })));

await sessionReceiver.close();
```

## 死信处理

```typescript
// Move to dead-letter
await receiver.deadLetterMessage(message, {
  deadLetterReason: "Validation failed",
  deadLetterErrorDescription: "Missing required field: orderId",
});

// Process dead-letter queue
const dlqReceiver = client.createReceiver("my-queue", { subQueueType: "deadLetter" });
const dlqMessages = await dlqReceiver.receiveMessages(10);
for (const msg of dlqMessages) {
  console.log(`DLQ Reason: ${msg.deadLetterReason}`);
  // Reprocess or log
  await dlqReceiver.completeMessage(msg);
}
```

## 计划消息

```typescript
const sender = client.createSender("my-queue");

// Schedule for future delivery
const scheduledTime = new Date(Date.now() + 60000); // 1 minute from now
const sequenceNumber = await sender.scheduleMessages(
  { body: "Delayed message" },
  scheduledTime
);

// Cancel scheduled message
await sender.cancelScheduledMessages(sequenceNumber);
```

## 消息延迟

```typescript
// Defer message for later
await receiver.deferMessage(message);

// Receive deferred message by sequence number
const deferredMessage = await receiver.receiveDeferredMessages(message.sequenceNumber!);
await receiver.completeMessage(deferredMessage[0]);
```

## 查看消息（非破坏性）

```typescript
const receiver = client.createReceiver("my-queue");

// Peek without removing
const peekedMessages = await receiver.peekMessages(10);
for (const msg of peekedMessages) {
  console.log(`Peeked: ${msg.body}`);
}
```

## 核心类型

```typescript
import {
  ServiceBusClient,
  ServiceBusSender,
  ServiceBusReceiver,
  ServiceBusSessionReceiver,
  ServiceBusMessage,
  ServiceBusReceivedMessage,
  ProcessMessageCallback,
  ProcessErrorCallback,
} from "@azure/service-bus";
```

## 接收模式

```typescript
// Peek-Lock (default) - message locked until completed/abandoned
const receiver = client.createReceiver("my-queue", { receiveMode: "peekLock" });
await receiver.completeMessage(message);   // Remove from queue
await receiver.abandonMessage(message);    // Return to queue
await receiver.deferMessage(message);      // Defer for later
await receiver.deadLetterMessage(message); // Move to DLQ

// Receive-and-Delete - message removed immediately
const receiver = client.createReceiver("my-queue", { receiveMode: "receiveAndDelete" });
```

## 最佳实践

1. **使用 Entra ID 认证** - 生产环境中避免使用连接字符串
2. **复用客户端** - 只创建一次 `ServiceBusClient`，在多个 sender/receiver 间共享
3. **关闭资源** - 使用完毕后务必关闭 sender/receiver
4. **处理错误** - 为订阅接收器实现 `processError` 回调
5. **使用会话保证顺序** - 当组内消息顺序很重要时使用会话
6. **配置死信** - 始终处理 DLQ 消息
7. **批量发送** - 多条消息时使用 `createMessageBatch()`

## 参考文档

详细模式请参阅：

- Queues vs Topics Patterns - 队列/主题模式、会话、接收模式、消息结算
- Error Handling and Reliability - ServiceBusError 错误码、DLQ 处理、锁续期、优雅关闭

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
