---
name: azure-eventgrid-java
description: "使用 Azure Event Grid SDK for Java 构建事件驱动应用程序。涵盖发布事件、实现发布/订阅模式以及通过事件集成 Azure 服务。当用户要求'Event Grid Java'、'发布事件 Azure'、'CloudEvent SDK'、'事件驱动消息'、'pub/sub Azure'、'webhook 事件'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Event Grid SDK for Java

使用 Azure Event Grid SDK for Java 构建事件驱动应用程序。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-messaging-eventgrid</artifactId>
    <version>4.27.0</version>
</dependency>
```

## 客户端创建

### EventGridPublisherClient

```java
import com.azure.messaging.eventgrid.EventGridPublisherClient;
import com.azure.messaging.eventgrid.EventGridPublisherClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

// With API Key
EventGridPublisherClient<EventGridEvent> client = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildEventGridEventPublisherClient();

// For CloudEvents
EventGridPublisherClient<CloudEvent> cloudClient = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildCloudEventPublisherClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

EventGridPublisherClient<EventGridEvent> client = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildEventGridEventPublisherClient();
```

### 异步客户端

```java
import com.azure.messaging.eventgrid.EventGridPublisherAsyncClient;

EventGridPublisherAsyncClient<EventGridEvent> asyncClient = new EventGridPublisherClientBuilder()
    .endpoint("<topic-endpoint>")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildEventGridEventPublisherAsyncClient();
```

## 事件类型

| 类型 | 描述 |
|------|------|
| `EventGridEvent` | Azure Event Grid 原生架构 |
| `CloudEvent` | CNCF CloudEvents 1.0 规范 |
| `BinaryData` | 自定义架构事件 |

## 核心模式

### 发布 EventGridEvent

```java
import com.azure.messaging.eventgrid.EventGridEvent;
import com.azure.core.util.BinaryData;

EventGridEvent event = new EventGridEvent(
    "resource/path",           // subject
    "MyApp.Events.OrderCreated", // eventType
    BinaryData.fromObject(new OrderData("order-123", 99.99)), // data
    "1.0"                      // dataVersion
);

client.sendEvent(event);
```

### 批量发布事件

```java
List<EventGridEvent> events = Arrays.asList(
    new EventGridEvent("orders/1", "Order.Created", 
        BinaryData.fromObject(order1), "1.0"),
    new EventGridEvent("orders/2", "Order.Created", 
        BinaryData.fromObject(order2), "1.0")
);

client.sendEvents(events);
```

### 发布 CloudEvent

```java
import com.azure.core.models.CloudEvent;
import com.azure.core.models.CloudEventDataFormat;

CloudEvent cloudEvent = new CloudEvent(
    "/myapp/orders",           // source
    "order.created",           // type
    BinaryData.fromObject(orderData), // data
    CloudEventDataFormat.JSON  // dataFormat
);
cloudEvent.setSubject("orders/12345");
cloudEvent.setId(UUID.randomUUID().toString());

cloudClient.sendEvent(cloudEvent);
```

### 批量发布 CloudEvents

```java
List<CloudEvent> cloudEvents = Arrays.asList(
    new CloudEvent("/app", "event.type1", BinaryData.fromString("data1"), CloudEventDataFormat.JSON),
    new CloudEvent("/app", "event.type2", BinaryData.fromString("data2"), CloudEventDataFormat.JSON)
);

cloudClient.sendEvents(cloudEvents);
```

### 异步发布

```java
asyncClient.sendEvent(event)
    .subscribe(
        unused -> System.out.println("Event sent successfully"),
        error -> System.err.println("Error: " + error.getMessage())
    );

// With multiple events
asyncClient.sendEvents(events)
    .doOnSuccess(unused -> System.out.println("All events sent"))
    .doOnError(error -> System.err.println("Failed: " + error))
    .block(); // Block if needed
```

### 自定义事件数据类

```java
public class OrderData {
    private String orderId;
    private double amount;
    private String customerId;
    
    public OrderData(String orderId, double amount) {
        this.orderId = orderId;
        this.amount = amount;
    }
    
    // Getters and setters
}

// Usage
OrderData order = new OrderData("ORD-123", 150.00);
EventGridEvent event = new EventGridEvent(
    "orders/" + order.getOrderId(),
    "MyApp.Order.Created",
    BinaryData.fromObject(order),
    "1.0"
);
```

## 接收事件

### 解析 EventGridEvent

```java
import com.azure.messaging.eventgrid.EventGridEvent;

// From JSON string (e.g., webhook payload)
String jsonPayload = "[{\"id\": \"...\", ...}]";
List<EventGridEvent> events = EventGridEvent.fromString(jsonPayload);

for (EventGridEvent event : events) {
    System.out.println("Event Type: " + event.getEventType());
    System.out.println("Subject: " + event.getSubject());
    System.out.println("Event Time: " + event.getEventTime());
    
    // Get data
    BinaryData data = event.getData();
    OrderData orderData = data.toObject(OrderData.class);
}
```

### 解析 CloudEvent

```java
import com.azure.core.models.CloudEvent;

String cloudEventJson = "[{\"specversion\": \"1.0\", ...}]";
List<CloudEvent> cloudEvents = CloudEvent.fromString(cloudEventJson);

for (CloudEvent event : cloudEvents) {
    System.out.println("Type: " + event.getType());
    System.out.println("Source: " + event.getSource());
    System.out.println("ID: " + event.getId());
    
    MyEventData data = event.getData().toObject(MyEventData.class);
}
```

### 处理系统事件

```java
import com.azure.messaging.eventgrid.systemevents.*;

for (EventGridEvent event : events) {
    if (event.getEventType().equals("Microsoft.Storage.BlobCreated")) {
        StorageBlobCreatedEventData blobData = 
            event.getData().toObject(StorageBlobCreatedEventData.class);
        System.out.println("Blob URL: " + blobData.getUrl());
    }
}
```

## Event Grid 命名空间（MQTT/拉取）

### 从命名空间主题接收

```java
import com.azure.messaging.eventgrid.namespaces.EventGridReceiverClient;
import com.azure.messaging.eventgrid.namespaces.EventGridReceiverClientBuilder;
import com.azure.messaging.eventgrid.namespaces.models.*;

EventGridReceiverClient receiverClient = new EventGridReceiverClientBuilder()
    .endpoint("<namespace-endpoint>")
    .credential(new AzureKeyCredential("<key>"))
    .topicName("my-topic")
    .subscriptionName("my-subscription")
    .buildClient();

// Receive events
ReceiveResult result = receiverClient.receive(10, Duration.ofSeconds(30));

for (ReceiveDetails detail : result.getValue()) {
    CloudEvent event = detail.getEvent();
    System.out.println("Event: " + event.getType());
    
    // Acknowledge the event
    receiverClient.acknowledge(Arrays.asList(detail.getBrokerProperties().getLockToken()));
}
```

### 拒绝或释放事件

```java
// Reject (don't retry)
receiverClient.reject(Arrays.asList(lockToken));

// Release (retry later)
receiverClient.release(Arrays.asList(lockToken));

// Release with delay
receiverClient.release(Arrays.asList(lockToken), 
    new ReleaseOptions().setDelay(ReleaseDelay.BY_60_SECONDS));
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.sendEvent(event);
} catch (HttpResponseException e) {
    System.out.println("Status: " + e.getResponse().getStatusCode());
    System.out.println("Error: " + e.getMessage());
}
```

## 环境变量

```bash
EVENT_GRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENT_GRID_ACCESS_KEY=<your-access-key>
```

## 最佳实践

1. **批量发送事件**：尽可能在一次调用中发送多个事件
2. **幂等性**：包含唯一事件 ID 以实现去重
3. **架构验证**：使用强类型事件数据类
4. **重试逻辑**：内置支持，但应考虑失败时的死信队列
5. **事件大小**：事件保持在 1MB 以下（基本层为 64KB）

## 触发词

- "Event Grid Java"
- "发布事件 Azure"
- "CloudEvent SDK"
- "事件驱动消息"
- "pub/sub Azure"
- "webhook 事件"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
