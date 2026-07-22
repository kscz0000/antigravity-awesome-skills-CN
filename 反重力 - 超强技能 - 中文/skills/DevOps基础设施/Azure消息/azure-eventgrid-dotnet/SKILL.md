---
name: azure-eventgrid-dotnet
description: Azure Event Grid .NET SDK。用于向 Azure Event Grid 发布和消费事件的客户端库。当用户要求'Azure Event Grid'、'事件网格'、'EventGrid'、'CloudEvents'、'事件驱动架构'、'发布订阅消息'、'pull delivery'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Messaging.EventGrid (.NET)

用于向 Azure Event Grid 主题、域和命名空间发布事件的客户端库。

## 安装

```bash
# For topics and domains (push delivery)
dotnet add package Azure.Messaging.EventGrid

# For namespaces (pull delivery)
dotnet add package Azure.Messaging.EventGrid.Namespaces

# For CloudNative CloudEvents interop
dotnet add package Microsoft.Azure.Messaging.EventGrid.CloudNativeCloudEvents
```

**当前版本**：4.28.0（稳定版）

## 环境变量

```bash
# Topic/Domain endpoint
EVENT_GRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENT_GRID_TOPIC_KEY=<access-key>

# Namespace endpoint (for pull delivery)
EVENT_GRID_NAMESPACE_ENDPOINT=https://<namespace>.<region>.eventgrid.azure.net
EVENT_GRID_TOPIC_NAME=<topic-name>
EVENT_GRID_SUBSCRIPTION_NAME=<subscription-name>
```

## 客户端层次结构

```
Push Delivery (Topics/Domains)
└── EventGridPublisherClient
    ├── SendEventAsync(EventGridEvent)
    ├── SendEventsAsync(IEnumerable<EventGridEvent>)
    ├── SendEventAsync(CloudEvent)
    └── SendEventsAsync(IEnumerable<CloudEvent>)

Pull Delivery (Namespaces)
├── EventGridSenderClient
│   └── SendAsync(CloudEvent)
└── EventGridReceiverClient
    ├── ReceiveAsync()
    ├── AcknowledgeAsync()
    ├── ReleaseAsync()
    └── RejectAsync()
```

## 身份验证

### API Key 身份验证

```csharp
using Azure;
using Azure.Messaging.EventGrid;

EventGridPublisherClient client = new(
    new Uri("https://mytopic.eastus-1.eventgrid.azure.net/api/events"),
    new AzureKeyCredential("<access-key>"));
```

### Microsoft Entra ID（推荐）

```csharp
using Azure.Identity;
using Azure.Messaging.EventGrid;

EventGridPublisherClient client = new(
    new Uri("https://mytopic.eastus-1.eventgrid.azure.net/api/events"),
    new DefaultAzureCredential());
```

### SAS Token 身份验证

```csharp
string sasToken = EventGridPublisherClient.BuildSharedAccessSignature(
    new Uri(topicEndpoint),
    DateTimeOffset.UtcNow.AddHours(1),
    new AzureKeyCredential(topicKey));

var sasCredential = new AzureSasCredential(sasToken);
EventGridPublisherClient client = new(
    new Uri(topicEndpoint),
    sasCredential);
```

## 发布事件

### EventGridEvent 架构

```csharp
EventGridPublisherClient client = new(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey));

// Single event
EventGridEvent egEvent = new(
    subject: "orders/12345",
    eventType: "Order.Created",
    dataVersion: "1.0",
    data: new { OrderId = "12345", Amount = 99.99 });

await client.SendEventAsync(egEvent);

// Batch of events
List<EventGridEvent> events = new()
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new OrderData { OrderId = "12345", Amount = 99.99 }),
    new EventGridEvent(
        subject: "orders/12346",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new OrderData { OrderId = "12346", Amount = 149.99 })
};

await client.SendEventsAsync(events);
```

### CloudEvent 架构

```csharp
CloudEvent cloudEvent = new(
    source: "/orders/system",
    type: "Order.Created",
    data: new { OrderId = "12345", Amount = 99.99 });

cloudEvent.Subject = "orders/12345";
cloudEvent.Id = Guid.NewGuid().ToString();
cloudEvent.Time = DateTimeOffset.UtcNow;

await client.SendEventAsync(cloudEvent);

// Batch of CloudEvents
List<CloudEvent> cloudEvents = new()
{
    new CloudEvent("/orders", "Order.Created", new { OrderId = "1" }),
    new CloudEvent("/orders", "Order.Updated", new { OrderId = "2" })
};

await client.SendEventsAsync(cloudEvents);
```

### 发布到 Event Grid 域

```csharp
// Events must specify the Topic property for domain routing
List<EventGridEvent> events = new()
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "Order.Created",
        dataVersion: "1.0",
        data: new { OrderId = "12345" })
    {
        Topic = "orders-topic"  // Domain topic name
    },
    new EventGridEvent(
        subject: "inventory/item-1",
        eventType: "Inventory.Updated",
        dataVersion: "1.0",
        data: new { ItemId = "item-1" })
    {
        Topic = "inventory-topic"
    }
};

await client.SendEventsAsync(events);
```

### 自定义序列化

```csharp
using System.Text.Json;

var serializerOptions = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
};

var customSerializer = new JsonObjectSerializer(serializerOptions);

EventGridEvent egEvent = new(
    subject: "orders/12345",
    eventType: "Order.Created",
    dataVersion: "1.0",
    data: customSerializer.Serialize(new OrderData { OrderId = "12345" }));

await client.SendEventAsync(egEvent);
```

## 拉取交付（命名空间）

### 向命名空间主题发送事件

```csharp
using Azure;
using Azure.Messaging;
using Azure.Messaging.EventGrid.Namespaces;

var senderClient = new EventGridSenderClient(
    new Uri(namespaceEndpoint),
    topicName,
    new AzureKeyCredential(topicKey));

// Send single event
CloudEvent cloudEvent = new("employee_source", "Employee.Created", 
    new { Name = "John", Age = 30 });
await senderClient.SendAsync(cloudEvent);

// Send batch
await senderClient.SendAsync(new[]
{
    new CloudEvent("source", "type", new { Name = "Alice" }),
    new CloudEvent("source", "type", new { Name = "Bob" })
});
```

### 接收和处理事件

```csharp
var receiverClient = new EventGridReceiverClient(
    new Uri(namespaceEndpoint),
    topicName,
    subscriptionName,
    new AzureKeyCredential(topicKey));

// Receive events
ReceiveResult result = await receiverClient.ReceiveAsync(maxEvents: 10);

List<string> lockTokensToAck = new();
List<string> lockTokensToRelease = new();

foreach (ReceiveDetails detail in result.Details)
{
    CloudEvent cloudEvent = detail.Event;
    string lockToken = detail.BrokerProperties.LockToken;
    
    try
    {
        // Process the event
        Console.WriteLine($"Event: {cloudEvent.Type}, Data: {cloudEvent.Data}");
        lockTokensToAck.Add(lockToken);
    }
    catch (Exception)
    {
        // Release for retry
        lockTokensToRelease.Add(lockToken);
    }
}

// Acknowledge successfully processed events
if (lockTokensToAck.Any())
{
    await receiverClient.AcknowledgeAsync(lockTokensToAck);
}

// Release events for retry
if (lockTokensToRelease.Any())
{
    await receiverClient.ReleaseAsync(lockTokensToRelease);
}
```

### 拒绝事件（死信）

```csharp
// Reject events that cannot be processed
await receiverClient.RejectAsync(new[] { lockToken });
```

## 消费事件（Azure Functions）

### EventGridEvent 触发器

```csharp
using Azure.Messaging.EventGrid;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;

public static class EventGridFunction
{
    [FunctionName("ProcessEventGridEvent")]
    public static void Run(
        [EventGridTrigger] EventGridEvent eventGridEvent,
        ILogger log)
    {
        log.LogInformation($"Event Type: {eventGridEvent.EventType}");
        log.LogInformation($"Subject: {eventGridEvent.Subject}");
        log.LogInformation($"Data: {eventGridEvent.Data}");
    }
}
```

### CloudEvent 触发器

```csharp
using Azure.Messaging;
using Microsoft.Azure.Functions.Worker;

public class CloudEventFunction
{
    [Function("ProcessCloudEvent")]
    public void Run(
        [EventGridTrigger] CloudEvent cloudEvent,
        FunctionContext context)
    {
        var logger = context.GetLogger("ProcessCloudEvent");
        logger.LogInformation($"Event Type: {cloudEvent.Type}");
        logger.LogInformation($"Source: {cloudEvent.Source}");
        logger.LogInformation($"Data: {cloudEvent.Data}");
    }
}
```

## 解析事件

### 解析 EventGridEvent

```csharp
// From JSON string
string json = "..."; // Event Grid webhook payload
EventGridEvent[] events = EventGridEvent.ParseMany(BinaryData.FromString(json));

foreach (EventGridEvent egEvent in events)
{
    if (egEvent.TryGetSystemEventData(out object systemEvent))
    {
        // Handle system event
        switch (systemEvent)
        {
            case StorageBlobCreatedEventData blobCreated:
                Console.WriteLine($"Blob created: {blobCreated.Url}");
                break;
        }
    }
    else
    {
        // Handle custom event
        var customData = egEvent.Data.ToObjectFromJson<MyCustomData>();
    }
}
```

### 解析 CloudEvent

```csharp
CloudEvent[] cloudEvents = CloudEvent.ParseMany(BinaryData.FromString(json));

foreach (CloudEvent cloudEvent in cloudEvents)
{
    var data = cloudEvent.Data.ToObjectFromJson<MyEventData>();
    Console.WriteLine($"Type: {cloudEvent.Type}, Data: {data}");
}
```

## 系统事件

```csharp
// Common system event types
using Azure.Messaging.EventGrid.SystemEvents;

// Storage events
StorageBlobCreatedEventData blobCreated;
StorageBlobDeletedEventData blobDeleted;

// Resource events
ResourceWriteSuccessEventData resourceCreated;
ResourceDeleteSuccessEventData resourceDeleted;

// App Service events
WebAppUpdatedEventData webAppUpdated;

// Container Registry events
ContainerRegistryImagePushedEventData imagePushed;

// IoT Hub events
IotHubDeviceCreatedEventData deviceCreated;
```

## 核心类型参考

| 类型 | 用途 |
|------|------|
| `EventGridPublisherClient` | 向主题/域发布事件 |
| `EventGridSenderClient` | 向命名空间主题发送事件 |
| `EventGridReceiverClient` | 从命名空间订阅接收事件 |
| `EventGridEvent` | Event Grid 原生架构 |
| `CloudEvent` | CloudEvents 1.0 架构 |
| `ReceiveResult` | 拉取交付响应 |
| `ReceiveDetails` | 包含代理属性的事件 |
| `BrokerProperties` | 锁定令牌、交付计数 |

## 事件架构对比

| 特性 | EventGridEvent | CloudEvent |
|------|----------------|------------|
| 标准 | Azure 专有 | CNCF 标准 |
| 必填字段 | subject、eventType、dataVersion、data | source、type |
| 可扩展性 | 有限 | 扩展属性 |
| 互操作性 | 仅 Azure | 跨平台 |

## 最佳实践

1. **使用 CloudEvents** — 新实现优先使用 CloudEvents（行业标准）
2. **批量发送事件** — 一次调用发送多个事件以提高效率
3. **使用 Entra ID** — 优先使用托管标识而非访问密钥
4. **幂等处理器** — 事件可能被多次交付
5. **设置事件 TTL** — 为命名空间事件配置生存时间
6. **处理部分失败** — 逐个确认/释放事件
7. **使用死信** — 为失败事件配置死信
8. **验证架构** — 处理前验证事件数据

## 错误处理

```csharp
using Azure;

try
{
    await client.SendEventAsync(cloudEvent);
}
catch (RequestFailedException ex) when (ex.Status == 401)
{
    Console.WriteLine("Authentication failed - check credentials");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Authorization failed - check RBAC permissions");
}
catch (RequestFailedException ex) when (ex.Status == 413)
{
    Console.WriteLine("Payload too large - max 1MB per event, 1MB total batch");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Event Grid error: {ex.Status} - {ex.Message}");
}
```

## 故障转移模式

```csharp
try
{
    var primaryClient = new EventGridPublisherClient(primaryUri, primaryKey);
    await primaryClient.SendEventsAsync(events);
}
catch (RequestFailedException)
{
    // Failover to secondary region
    var secondaryClient = new EventGridPublisherClient(secondaryUri, secondaryKey);
    await secondaryClient.SendEventsAsync(events);
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|----|------|------|
| `Azure.Messaging.EventGrid` | 主题/域（本 SDK） | `dotnet add package Azure.Messaging.EventGrid` |
| `Azure.Messaging.EventGrid.Namespaces` | 拉取交付 | `dotnet add package Azure.Messaging.EventGrid.Namespaces` |
| `Azure.Identity` | 身份验证 | `dotnet add package Azure.Identity` |
| `Microsoft.Azure.WebJobs.Extensions.EventGrid` | Azure Functions 触发器 | `dotnet add package Microsoft.Azure.WebJobs.Extensions.EventGrid` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.Messaging.EventGrid |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.messaging.eventgrid |
| 快速入门 | https://learn.microsoft.com/azure/event-grid/custom-event-quickstart |
| 拉取交付 | https://learn.microsoft.com/azure/event-grid/pull-delivery-overview |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/eventgrid/Azure.Messaging.EventGrid |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
