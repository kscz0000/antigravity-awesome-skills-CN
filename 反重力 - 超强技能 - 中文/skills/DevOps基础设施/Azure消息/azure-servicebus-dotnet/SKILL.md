---
name: azure-servicebus-dotnet
description: Azure Service Bus .NET SDK，企业级消息传递，支持队列、主题、订阅和会话。当用户要求'Azure Service Bus'、'Service Bus 队列'、'Service Bus 主题'、'Service Bus 订阅'、'Service Bus 会话'、'.NET 消息传递'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Messaging.ServiceBus (.NET)

企业级消息传递 SDK，通过队列、主题、订阅和会话实现可靠的消息交付。

## 安装

```bash
dotnet add package Azure.Messaging.ServiceBus
dotnet add package Azure.Identity
```

**当前版本**：v7.20.1（稳定版）

## 环境变量

```bash
AZURE_SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
# 或连接字符串（安全性较低）
AZURE_SERVICEBUS_CONNECTION_STRING=Endpoint=sb://...
```

## 身份验证

### Microsoft Entra ID（推荐）

```csharp
using Azure.Identity;
using Azure.Messaging.ServiceBus;

string fullyQualifiedNamespace = "<namespace>.servicebus.windows.net";
await using ServiceBusClient client = new(fullyQualifiedNamespace, new DefaultAzureCredential());
```

### 连接字符串

```csharp
string connectionString = "<connection_string>";
await using ServiceBusClient client = new(connectionString);
```

### ASP.NET Core 依赖注入

```csharp
services.AddAzureClients(builder =>
{
    builder.AddServiceBusClientWithNamespace("<namespace>.servicebus.windows.net");
    builder.UseCredential(new DefaultAzureCredential());
});
```

## 客户端层次结构

```
ServiceBusClient
├── CreateSender(queueOrTopicName)      → ServiceBusSender
├── CreateReceiver(queueName)           → ServiceBusReceiver
├── CreateReceiver(topicName, subName)  → ServiceBusReceiver
├── AcceptNextSessionAsync(queueName)   → ServiceBusSessionReceiver
├── CreateProcessor(queueName)          → ServiceBusProcessor
└── CreateSessionProcessor(queueName)   → ServiceBusSessionProcessor

ServiceBusAdministrationClient (separate client for CRUD)
```

## 核心工作流

### 1. 发送消息

```csharp
await using ServiceBusClient client = new(fullyQualifiedNamespace, new DefaultAzureCredential());
ServiceBusSender sender = client.CreateSender("my-queue");

// 单条消息
ServiceBusMessage message = new("Hello world!");
await sender.SendMessageAsync(message);

// 安全批处理（推荐）
using ServiceBusMessageBatch batch = await sender.CreateMessageBatchAsync();
if (batch.TryAddMessage(new ServiceBusMessage("Message 1")))
{
    // Message added successfully
}
if (batch.TryAddMessage(new ServiceBusMessage("Message 2")))
{
    // Message added successfully
}
await sender.SendMessagesAsync(batch);
```

### 2. 接收消息

```csharp
ServiceBusReceiver receiver = client.CreateReceiver("my-queue");

// 单条消息
ServiceBusReceivedMessage message = await receiver.ReceiveMessageAsync();
string body = message.Body.ToString();
Console.WriteLine(body);

// 完成消息（从队列中移除）
await receiver.CompleteMessageAsync(message);

// 批量接收
IReadOnlyList<ServiceBusReceivedMessage> messages = await receiver.ReceiveMessagesAsync(maxMessages: 10);
foreach (var msg in messages)
{
    Console.WriteLine(msg.Body.ToString());
    await receiver.CompleteMessageAsync(msg);
}
```

### 3. 消息结算

```csharp
// Complete - 从队列中移除消息
await receiver.CompleteMessageAsync(message);

// Abandon - 释放锁，消息可被再次接收
await receiver.AbandonMessageAsync(message);

// Defer - 阻止正常接收，使用 ReceiveDeferredMessageAsync 获取
await receiver.DeferMessageAsync(message);

// Dead Letter - 移入死信子队列
await receiver.DeadLetterMessageAsync(message, "InvalidFormat", "Message body was not valid JSON");
```

### 4. 使用 Processor 进行后台处理

```csharp
ServiceBusProcessor processor = client.CreateProcessor("my-queue", new ServiceBusProcessorOptions
{
    AutoCompleteMessages = false,
    MaxConcurrentCalls = 2
});

processor.ProcessMessageAsync += async (args) =>
{
    try
    {
        string body = args.Message.Body.ToString();
        Console.WriteLine($"Received: {body}");
        await args.CompleteMessageAsync(args.Message);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error processing: {ex.Message}");
        await args.AbandonMessageAsync(args.Message);
    }
};

processor.ProcessErrorAsync += (args) =>
{
    Console.WriteLine($"Error source: {args.ErrorSource}");
    Console.WriteLine($"Entity: {args.EntityPath}");
    Console.WriteLine($"Exception: {args.Exception}");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync();
// ... 应用程序运行
await processor.StopProcessingAsync();
```

### 5. 会话（有序处理）

```csharp
// 发送会话消息
ServiceBusMessage message = new("Hello")
{
    SessionId = "order-123"
};
await sender.SendMessageAsync(message);

// 从下一个可用会话接收
ServiceBusSessionReceiver receiver = await client.AcceptNextSessionAsync("my-queue");

// 或从指定会话接收
ServiceBusSessionReceiver receiver = await client.AcceptSessionAsync("my-queue", "order-123");

// 会话状态管理
await receiver.SetSessionStateAsync(new BinaryData("processing"));
BinaryData state = await receiver.GetSessionStateAsync();

// 续订会话锁
await receiver.RenewSessionLockAsync();
```

### 6. 死信队列

```csharp
// 从死信队列接收
ServiceBusReceiver dlqReceiver = client.CreateReceiver("my-queue", new ServiceBusReceiverOptions
{
    SubQueue = SubQueue.DeadLetter
});

ServiceBusReceivedMessage dlqMessage = await dlqReceiver.ReceiveMessageAsync();

// 访问死信元数据
string reason = dlqMessage.DeadLetterReason;
string description = dlqMessage.DeadLetterErrorDescription;
Console.WriteLine($"Dead letter reason: {reason} - {description}");
```

### 7. 主题和订阅

```csharp
// 发送到主题
ServiceBusSender topicSender = client.CreateSender("my-topic");
await topicSender.SendMessageAsync(new ServiceBusMessage("Broadcast message"));

// 从订阅接收
ServiceBusReceiver subReceiver = client.CreateReceiver("my-topic", "my-subscription");
var message = await subReceiver.ReceiveMessageAsync();
```

### 8. 管理（CRUD）

```csharp
var adminClient = new ServiceBusAdministrationClient(
    fullyQualifiedNamespace, 
    new DefaultAzureCredential());

// 创建队列
var options = new CreateQueueOptions("my-queue")
{
    MaxDeliveryCount = 10,
    LockDuration = TimeSpan.FromSeconds(30),
    RequiresSession = true,
    DeadLetteringOnMessageExpiration = true
};
QueueProperties queue = await adminClient.CreateQueueAsync(options);

// 更新队列
queue.LockDuration = TimeSpan.FromSeconds(60);
await adminClient.UpdateQueueAsync(queue);

// 创建主题和订阅
await adminClient.CreateTopicAsync(new CreateTopicOptions("my-topic"));
await adminClient.CreateSubscriptionAsync(new CreateSubscriptionOptions("my-topic", "my-subscription"));

// 删除
await adminClient.DeleteQueueAsync("my-queue");
```

### 9. 跨实体事务

```csharp
var options = new ServiceBusClientOptions { EnableCrossEntityTransactions = true };
await using var client = new ServiceBusClient(connectionString, options);

ServiceBusReceiver receiverA = client.CreateReceiver("queueA");
ServiceBusSender senderB = client.CreateSender("queueB");

ServiceBusReceivedMessage receivedMessage = await receiverA.ReceiveMessageAsync();

using (var ts = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
{
    await receiverA.CompleteMessageAsync(receivedMessage);
    await senderB.SendMessageAsync(new ServiceBusMessage("Forwarded"));
    ts.Complete();
}
```

## 核心类型参考

| 类型 | 用途 |
|------|------|
| `ServiceBusClient` | 主入口点，管理连接 |
| `ServiceBusSender` | 向队列/主题发送消息 |
| `ServiceBusReceiver` | 从队列/订阅接收消息 |
| `ServiceBusSessionReceiver` | 接收会话消息 |
| `ServiceBusProcessor` | 后台消息处理 |
| `ServiceBusSessionProcessor` | 后台会话处理 |
| `ServiceBusAdministrationClient` | 队列/主题/订阅的 CRUD 操作 |
| `ServiceBusMessage` | 待发送的消息 |
| `ServiceBusReceivedMessage` | 带元数据的已接收消息 |
| `ServiceBusMessageBatch` | 消息批次 |

## 最佳实践

1. **使用单例** — Client、Sender、Receiver 和 Processor 都是线程安全的
2. **始终释放资源** — 使用 `await using` 或调用 `DisposeAsync()`
3. **释放顺序** — 先关闭 Sender/Receiver/Processor，再关闭 Client
4. **使用 DefaultAzureCredential** — 生产环境优先于连接字符串
5. **后台处理使用 Processor** — 自动处理锁续订
6. **使用安全批处理** — `CreateMessageBatchAsync()` 和 `TryAddMessage()`
7. **处理瞬态错误** — 使用 `ServiceBusException.Reason`
8. **配置传输方式** — 端口 5671/5672 被阻止时使用 `AmqpWebSockets`
9. **设置适当的锁持续时间** — 默认为 30 秒
10. **使用会话保证顺序** — 同一会话内 FIFO

## 错误处理

```csharp
try
{
    await sender.SendMessageAsync(message);
}
catch (ServiceBusException ex) when (ex.Reason == ServiceBusFailureReason.ServiceBusy)
{
    // 退避重试
}
catch (ServiceBusException ex)
{
    Console.WriteLine($"Service Bus Error: {ex.Reason} - {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.Messaging.ServiceBus` | Service Bus（本 SDK） | `dotnet add package Azure.Messaging.ServiceBus` |
| `Azure.Messaging.EventHubs` | 事件流 | `dotnet add package Azure.Messaging.EventHubs` |
| `Azure.Messaging.EventGrid` | 事件路由 | `dotnet add package Azure.Messaging.EventGrid` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.Messaging.ServiceBus |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.messaging.servicebus |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/servicebus/Azure.Messaging.ServiceBus |
| 故障排除 | https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/TROUBLESHOOTING.md |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
