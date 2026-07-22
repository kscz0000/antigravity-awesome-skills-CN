---
name: azure-eventhub-java
description: "使用 Azure Event Hubs SDK for Java 构建实时流处理应用程序。当用户要求'Azure事件中心Java开发'、'事件流处理'、'高吞吐量数据摄入'或'构建事件驱动架构'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Event Hubs SDK for Java

使用 Azure Event Hubs SDK for Java 构建实时流处理应用程序。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-eventhubs</artifactId>
    <version>5.19.0</version>
</dependency>

<!-- For checkpoint store (production) -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-eventhubs-checkpointstore-blob</artifactId>
    <version>1.20.0</version>
</dependency>
```

## 客户端创建

### EventHubProducerClient

```java
import com.azure.messaging.eventhubs.EventHubProducerClient;
import com.azure.messaging.eventhubs.EventHubClientBuilder;

// With connection string
EventHubProducerClient producer = new EventHubClientBuilder()
    .connectionString("<connection-string>", "<event-hub-name>")
    .buildProducerClient();

// Full connection string with EntityPath
EventHubProducerClient producer = new EventHubClientBuilder()
    .connectionString("<connection-string-with-entity-path>")
    .buildProducerClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

EventHubProducerClient producer = new EventHubClientBuilder()
    .fullyQualifiedNamespace("<namespace>.servicebus.windows.net")
    .eventHubName("<event-hub-name>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildProducerClient();
```

### EventHubConsumerClient

```java
import com.azure.messaging.eventhubs.EventHubConsumerClient;

EventHubConsumerClient consumer = new EventHubClientBuilder()
    .connectionString("<connection-string>", "<event-hub-name>")
    .consumerGroup(EventHubClientBuilder.DEFAULT_CONSUMER_GROUP_NAME)
    .buildConsumerClient();
```

### 异步客户端

```java
import com.azure.messaging.eventhubs.EventHubProducerAsyncClient;
import com.azure.messaging.eventhubs.EventHubConsumerAsyncClient;

EventHubProducerAsyncClient asyncProducer = new EventHubClientBuilder()
    .connectionString("<connection-string>", "<event-hub-name>")
    .buildAsyncProducerClient();

EventHubConsumerAsyncClient asyncConsumer = new EventHubClientBuilder()
    .connectionString("<connection-string>", "<event-hub-name>")
    .consumerGroup("$Default")
    .buildAsyncConsumerClient();
```

## 核心模式

### 发送单个事件

```java
import com.azure.messaging.eventhubs.EventData;

EventData eventData = new EventData("Hello, Event Hubs!");
producer.send(Collections.singletonList(eventData));
```

### 发送事件批次

```java
import com.azure.messaging.eventhubs.EventDataBatch;
import com.azure.messaging.eventhubs.models.CreateBatchOptions;

// Create batch
EventDataBatch batch = producer.createBatch();

// Add events (returns false if batch is full)
for (int i = 0; i < 100; i++) {
    EventData event = new EventData("Event " + i);
    if (!batch.tryAdd(event)) {
        // Batch is full, send and create new batch
        producer.send(batch);
        batch = producer.createBatch();
        batch.tryAdd(event);
    }
}

// Send remaining events
if (batch.getCount() > 0) {
    producer.send(batch);
}
```

### 发送到指定分区

```java
CreateBatchOptions options = new CreateBatchOptions()
    .setPartitionId("0");

EventDataBatch batch = producer.createBatch(options);
batch.tryAdd(new EventData("Partition 0 event"));
producer.send(batch);
```

### 使用分区键发送

```java
CreateBatchOptions options = new CreateBatchOptions()
    .setPartitionKey("customer-123");

EventDataBatch batch = producer.createBatch(options);
batch.tryAdd(new EventData("Customer event"));
producer.send(batch);
```

### 带属性的事件

```java
EventData event = new EventData("Order created");
event.getProperties().put("orderId", "ORD-123");
event.getProperties().put("customerId", "CUST-456");
event.getProperties().put("priority", 1);

producer.send(Collections.singletonList(event));
```

### 接收事件（简单方式）

```java
import com.azure.messaging.eventhubs.models.EventPosition;
import com.azure.messaging.eventhubs.models.PartitionEvent;

// Receive from specific partition
Iterable<PartitionEvent> events = consumer.receiveFromPartition(
    "0",                           // partitionId
    10,                            // maxEvents
    EventPosition.earliest(),      // startingPosition
    Duration.ofSeconds(30)         // timeout
);

for (PartitionEvent partitionEvent : events) {
    EventData event = partitionEvent.getData();
    System.out.println("Body: " + event.getBodyAsString());
    System.out.println("Sequence: " + event.getSequenceNumber());
    System.out.println("Offset: " + event.getOffset());
}
```

### EventProcessorClient（生产环境）

```java
import com.azure.messaging.eventhubs.EventProcessorClient;
import com.azure.messaging.eventhubs.EventProcessorClientBuilder;
import com.azure.messaging.eventhubs.checkpointstore.blob.BlobCheckpointStore;
import com.azure.storage.blob.BlobContainerAsyncClient;
import com.azure.storage.blob.BlobContainerClientBuilder;

// Create checkpoint store
BlobContainerAsyncClient blobClient = new BlobContainerClientBuilder()
    .connectionString("<storage-connection-string>")
    .containerName("checkpoints")
    .buildAsyncClient();

// Create processor
EventProcessorClient processor = new EventProcessorClientBuilder()
    .connectionString("<eventhub-connection-string>", "<event-hub-name>")
    .consumerGroup("$Default")
    .checkpointStore(new BlobCheckpointStore(blobClient))
    .processEvent(eventContext -> {
        EventData event = eventContext.getEventData();
        System.out.println("Processing: " + event.getBodyAsString());
        
        // Checkpoint after processing
        eventContext.updateCheckpoint();
    })
    .processError(errorContext -> {
        System.err.println("Error: " + errorContext.getThrowable().getMessage());
        System.err.println("Partition: " + errorContext.getPartitionContext().getPartitionId());
    })
    .buildEventProcessorClient();

// Start processing
processor.start();

// Keep running...
Thread.sleep(Duration.ofMinutes(5).toMillis());

// Stop gracefully
processor.stop();
```

### 批量处理

```java
EventProcessorClient processor = new EventProcessorClientBuilder()
    .connectionString("<connection-string>", "<event-hub-name>")
    .consumerGroup("$Default")
    .checkpointStore(new BlobCheckpointStore(blobClient))
    .processEventBatch(eventBatchContext -> {
        List<EventData> events = eventBatchContext.getEvents();
        System.out.printf("Received %d events%n", events.size());
        
        for (EventData event : events) {
            // Process each event
            System.out.println(event.getBodyAsString());
        }
        
        // Checkpoint after batch
        eventBatchContext.updateCheckpoint();
    }, 50) // maxBatchSize
    .processError(errorContext -> {
        System.err.println("Error: " + errorContext.getThrowable());
    })
    .buildEventProcessorClient();
```

### 异步接收

```java
asyncConsumer.receiveFromPartition("0", EventPosition.latest())
    .subscribe(
        partitionEvent -> {
            EventData event = partitionEvent.getData();
            System.out.println("Received: " + event.getBodyAsString());
        },
        error -> System.err.println("Error: " + error),
        () -> System.out.println("Complete")
    );
```

### 获取事件中心属性

```java
// Get hub info
EventHubProperties hubProps = producer.getEventHubProperties();
System.out.println("Hub: " + hubProps.getName());
System.out.println("Partitions: " + hubProps.getPartitionIds());

// Get partition info
PartitionProperties partitionProps = producer.getPartitionProperties("0");
System.out.println("Begin sequence: " + partitionProps.getBeginningSequenceNumber());
System.out.println("Last sequence: " + partitionProps.getLastEnqueuedSequenceNumber());
System.out.println("Last offset: " + partitionProps.getLastEnqueuedOffset());
```

## 事件位置

```java
// Start from beginning
EventPosition.earliest()

// Start from end (new events only)
EventPosition.latest()

// From specific offset
EventPosition.fromOffset(12345L)

// From specific sequence number
EventPosition.fromSequenceNumber(100L)

// From specific time
EventPosition.fromEnqueuedTime(Instant.now().minus(Duration.ofHours(1)))
```

## 错误处理

```java
import com.azure.messaging.eventhubs.models.ErrorContext;

.processError(errorContext -> {
    Throwable error = errorContext.getThrowable();
    String partitionId = errorContext.getPartitionContext().getPartitionId();
    
    if (error instanceof AmqpException) {
        AmqpException amqpError = (AmqpException) error;
        if (amqpError.isTransient()) {
            System.out.println("Transient error, will retry");
        }
    }
    
    System.err.printf("Error on partition %s: %s%n", partitionId, error.getMessage());
})
```

## 资源清理

```java
// Always close clients
try {
    producer.send(batch);
} finally {
    producer.close();
}

// Or use try-with-resources
try (EventHubProducerClient producer = new EventHubClientBuilder()
        .connectionString(connectionString, eventHubName)
        .buildProducerClient()) {
    producer.send(events);
}
```

## 环境变量

```bash
EVENT_HUBS_CONNECTION_STRING=Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=...
EVENT_HUBS_NAME=<event-hub-name>
STORAGE_CONNECTION_STRING=<for-checkpointing>
```

## 最佳实践

1. **使用 EventProcessorClient**：生产环境中使用，提供负载均衡和检查点功能
2. **批量发送事件**：使用 `EventDataBatch` 实现高效发送
3. **分区键**：用于保证同一分区内的顺序性
4. **检查点**：处理后进行检查点以避免重复处理
5. **错误处理**：通过重试处理瞬态错误
6. **关闭客户端**：使用完毕后务必关闭 producer/consumer

## 触发词

- "Event Hubs Java"
- "event streaming Azure"
- "real-time data ingestion"
- "EventProcessorClient"
- "event hub producer consumer"
- "partition processing"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
