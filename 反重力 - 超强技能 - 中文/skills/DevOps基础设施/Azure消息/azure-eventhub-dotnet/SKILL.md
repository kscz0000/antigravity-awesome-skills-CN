---
name: azure-eventhub-dotnet
description: Azure Event Hubs .NET SDK，用于通过 Azure Event Hubs 发送和接收事件的高吞吐量事件流处理。当用户要求'Azure Event Hubs .NET 开发'、'EventHub 事件发送接收'、'EventProcessorClient 使用'或'Azure 事件流处理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Messaging.EventHubs (.NET)

通过 Azure Event Hubs 发送和接收事件的高吞吐量事件流 SDK。

## 安装

```bash
# Core package (sending and simple receiving)
dotnet add package Azure.Messaging.EventHubs

# Processor package (production receiving with checkpointing)
dotnet add package Azure.Messaging.EventHubs.Processor

# Authentication
dotnet add package Azure.Identity

# For checkpointing (required by EventProcessorClient)
dotnet add package Azure.Storage.Blobs
```

**当前版本**：Azure.Messaging.EventHubs v5.12.2，Azure.Messaging.EventHubs.Processor v5.12.2

## 环境变量

```bash
EVENTHUB_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
EVENTHUB_NAME=<event-hub-name>

# For checkpointing (EventProcessorClient)
BLOB_STORAGE_CONNECTION_STRING=<storage-connection-string>
BLOB_CONTAINER_NAME=<checkpoint-container>

# Alternative: Connection string auth (not recommended for production)
EVENTHUB_CONNECTION_STRING=Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=...
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;

// Always use DefaultAzureCredential for production
var credential = new DefaultAzureCredential();

var fullyQualifiedNamespace = Environment.GetEnvironmentVariable("EVENTHUB_FULLY_QUALIFIED_NAMESPACE");
var eventHubName = Environment.GetEnvironmentVariable("EVENTHUB_NAME");

var producer = new EventHubProducerClient(
    fullyQualifiedNamespace,
    eventHubName,
    credential);
```

**所需 RBAC 角色**：
- **发送**：`Azure Event Hubs Data Sender`
- **接收**：`Azure Event Hubs Data Receiver`
- **两者兼有**：`Azure Event Hubs Data Owner`

## 客户端类型

| 客户端 | 用途 | 何时使用 |
|--------|------|----------|
| `EventHubProducerClient` | 立即批量发送事件 | 实时发送，完全控制批处理 |
| `EventHubBufferedProducerClient` | 自动批处理与后台发送 | 高吞吐量、即发即忘场景 |
| `EventHubConsumerClient` | 简单事件读取 | 仅用于原型开发，不适用于生产环境 |
| `EventProcessorClient` | 生产级事件处理 | **生产环境接收事件时务必使用此客户端** |

## 核心工作流

### 1. 发送事件（批量）

```csharp
using Azure.Identity;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;

await using var producer = new EventHubProducerClient(
    fullyQualifiedNamespace,
    eventHubName,
    new DefaultAzureCredential());

// Create a batch (respects size limits automatically)
using EventDataBatch batch = await producer.CreateBatchAsync();

// Add events to batch
var events = new[]
{
    new EventData(BinaryData.FromString("{\"id\": 1, \"message\": \"Hello\"}")),
    new EventData(BinaryData.FromString("{\"id\": 2, \"message\": \"World\"}"))
};

foreach (var eventData in events)
{
    if (!batch.TryAdd(eventData))
    {
        // Batch is full - send it and create a new one
        await producer.SendAsync(batch);
        batch = await producer.CreateBatchAsync();
        
        if (!batch.TryAdd(eventData))
        {
            throw new Exception("Event too large for empty batch");
        }
    }
}

// Send remaining events
if (batch.Count > 0)
{
    await producer.SendAsync(batch);
}
```

### 2. 发送事件（缓冲模式 - 高吞吐量）

```csharp
using Azure.Messaging.EventHubs.Producer;

var options = new EventHubBufferedProducerClientOptions
{
    MaximumWaitTime = TimeSpan.FromSeconds(1)
};

await using var producer = new EventHubBufferedProducerClient(
    fullyQualifiedNamespace,
    eventHubName,
    new DefaultAzureCredential(),
    options);

// Handle send success/failure
producer.SendEventBatchSucceededAsync += args =>
{
    Console.WriteLine($"Batch sent: {args.EventBatch.Count} events");
    return Task.CompletedTask;
};

producer.SendEventBatchFailedAsync += args =>
{
    Console.WriteLine($"Batch failed: {args.Exception.Message}");
    return Task.CompletedTask;
};

// Enqueue events (sent automatically in background)
for (int i = 0; i < 1000; i++)
{
    await producer.EnqueueEventAsync(new EventData($"Event {i}"));
}

// Flush remaining events before disposing
await producer.FlushAsync();
```

### 3. 接收事件（生产环境 - EventProcessorClient）

```csharp
using Azure.Identity;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Consumer;
using Azure.Messaging.EventHubs.Processor;
using Azure.Storage.Blobs;

// Blob container for checkpointing
var blobClient = new BlobContainerClient(
    Environment.GetEnvironmentVariable("BLOB_STORAGE_CONNECTION_STRING"),
    Environment.GetEnvironmentVariable("BLOB_CONTAINER_NAME"));

await blobClient.CreateIfNotExistsAsync();

// Create processor
var processor = new EventProcessorClient(
    blobClient,
    EventHubConsumerClient.DefaultConsumerGroup,
    fullyQualifiedNamespace,
    eventHubName,
    new DefaultAzureCredential());

// Handle events
processor.ProcessEventAsync += async args =>
{
    Console.WriteLine($"Partition: {args.Partition.PartitionId}");
    Console.WriteLine($"Data: {args.Data.EventBody}");
    
    // Checkpoint after processing (or batch checkpoints)
    await args.UpdateCheckpointAsync();
};

// Handle errors
processor.ProcessErrorAsync += args =>
{
    Console.WriteLine($"Error: {args.Exception.Message}");
    Console.WriteLine($"Partition: {args.PartitionId}");
    return Task.CompletedTask;
};

// Start processing
await processor.StartProcessingAsync();

// Run until cancelled
await Task.Delay(Timeout.Infinite, cancellationToken);

// Stop gracefully
await processor.StopProcessingAsync();
```

### 4. 分区操作

```csharp
// Get partition IDs
string[] partitionIds = await producer.GetPartitionIdsAsync();

// Send to specific partition (use sparingly)
var options = new SendEventOptions
{
    PartitionId = "0"
};
await producer.SendAsync(events, options);

// Use partition key (recommended for ordering)
var batchOptions = new CreateBatchOptions
{
    PartitionKey = "customer-123"  // Events with same key go to same partition
};
using var batch = await producer.CreateBatchAsync(batchOptions);
```

## EventPosition 选项

控制从何处开始读取：

```csharp
// Start from beginning
EventPosition.Earliest

// Start from end (new events only)
EventPosition.Latest

// Start from specific offset
EventPosition.FromOffset(12345)

// Start from specific sequence number
EventPosition.FromSequenceNumber(100)

// Start from specific time
EventPosition.FromEnqueuedTime(DateTimeOffset.UtcNow.AddHours(-1))
```

## ASP.NET Core 集成

```csharp
// Program.cs
using Azure.Identity;
using Azure.Messaging.EventHubs.Producer;
using Microsoft.Extensions.Azure;

builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.AddEventHubProducerClient(
        builder.Configuration["EventHub:FullyQualifiedNamespace"],
        builder.Configuration["EventHub:Name"]);
    
    clientBuilder.UseCredential(new DefaultAzureCredential());
});

// Inject in controller/service
public class EventService
{
    private readonly EventHubProducerClient _producer;
    
    public EventService(EventHubProducerClient producer)
    {
        _producer = producer;
    }
    
    public async Task SendAsync(string message)
    {
        using var batch = await _producer.CreateBatchAsync();
        batch.TryAdd(new EventData(message));
        await _producer.SendAsync(batch);
    }
}
```

## 最佳实践

1. **使用 `EventProcessorClient` 接收事件** — 生产环境中绝不使用 `EventHubConsumerClient`
2. **策略性检查点** — 每 N 个事件或按时间间隔设置检查点，而非每个事件
3. **使用分区键** — 保证同一分区内的顺序性
4. **复用客户端** — 创建一次，作为单例使用（线程安全）
5. **使用 `await using`** — 确保正确释放资源
6. **处理 `ProcessErrorAsync`** — 始终注册错误处理程序
7. **批量发送事件** — 使用 `CreateBatchAsync()` 遵守大小限制
8. **使用缓冲生产者** — 适用于需要自动批处理的高吞吐量场景

## 错误处理

```csharp
using Azure.Messaging.EventHubs;

try
{
    await producer.SendAsync(batch);
}
catch (EventHubsException ex) when (ex.Reason == EventHubsException.FailureReason.ServiceBusy)
{
    // Retry with backoff
    await Task.Delay(TimeSpan.FromSeconds(5));
}
catch (EventHubsException ex) when (ex.IsTransient)
{
    // Transient error - safe to retry
    Console.WriteLine($"Transient error: {ex.Message}");
}
catch (EventHubsException ex)
{
    // Non-transient error
    Console.WriteLine($"Error: {ex.Reason} - {ex.Message}");
}
```

## 检查点策略

| 策略 | 何时使用 |
|------|----------|
| 每个事件 | 低吞吐量、关键数据 |
| 每 N 个事件 | 平衡吞吐量与可靠性 |
| 基于时间 | 一致的检查点间隔 |
| 批次完成 | 处理完一个逻辑批次后 |

```csharp
// Checkpoint every 100 events
private int _eventCount = 0;

processor.ProcessEventAsync += async args =>
{
    // Process event...
    
    _eventCount++;
    if (_eventCount >= 100)
    {
        await args.UpdateCheckpointAsync();
        _eventCount = 0;
    }
};
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.Messaging.EventHubs` | 核心发送/接收 | `dotnet add package Azure.Messaging.EventHubs` |
| `Azure.Messaging.EventHubs.Processor` | 生产级处理 | `dotnet add package Azure.Messaging.EventHubs.Processor` |
| `Azure.ResourceManager.EventHubs` | 管理平面（创建 Hub） | `dotnet add package Azure.ResourceManager.EventHubs` |
| `Microsoft.Azure.WebJobs.Extensions.EventHubs` | Azure Functions 绑定 | `dotnet add package Microsoft.Azure.WebJobs.Extensions.EventHubs` |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
