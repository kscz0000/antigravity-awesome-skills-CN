---
name: azure-eventhub-py
description: Azure Event Hubs Python SDK 流式处理。用于高吞吐量事件摄取、生产者、消费者和检查点。当用户要求'Azure事件中心'、'Event Hub'、'事件流处理'、'事件摄取'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Event Hubs SDK for Python

用于高吞吐量事件摄取的大数据流式平台。

## 安装

```bash
pip install azure-eventhub azure-identity
# For checkpointing with blob storage
pip install azure-eventhub-checkpointstoreblob-aio
```

## 环境变量

```bash
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
EVENT_HUB_NAME=my-eventhub
STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
CHECKPOINT_CONTAINER=checkpoints
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventHubConsumerClient

credential = DefaultAzureCredential()
namespace = "<namespace>.servicebus.windows.net"
eventhub_name = "my-eventhub"

# Producer
producer = EventHubProducerClient(
    fully_qualified_namespace=namespace,
    eventhub_name=eventhub_name,
    credential=credential
)

# Consumer
consumer = EventHubConsumerClient(
    fully_qualified_namespace=namespace,
    eventhub_name=eventhub_name,
    consumer_group="$Default",
    credential=credential
)
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `EventHubProducerClient` | 向 Event Hub 发送事件 |
| `EventHubConsumerClient` | 从 Event Hub 接收事件 |
| `BlobCheckpointStore` | 跟踪消费者进度 |

## 发送事件

```python
from azure.eventhub import EventHubProducerClient, EventData
from azure.identity import DefaultAzureCredential

producer = EventHubProducerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    credential=DefaultAzureCredential()
)

with producer:
    # Create batch (handles size limits)
    event_data_batch = producer.create_batch()
    
    for i in range(10):
        try:
            event_data_batch.add(EventData(f"Event {i}"))
        except ValueError:
            # Batch is full, send and create new one
            producer.send_batch(event_data_batch)
            event_data_batch = producer.create_batch()
            event_data_batch.add(EventData(f"Event {i}"))
    
    # Send remaining
    producer.send_batch(event_data_batch)
```

### 发送到指定分区

```python
# By partition ID
event_data_batch = producer.create_batch(partition_id="0")

# By partition key (consistent hashing)
event_data_batch = producer.create_batch(partition_key="user-123")
```

## 接收事件

### 简单接收

```python
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    print(f"Partition: {partition_context.partition_id}")
    print(f"Data: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

consumer = EventHubConsumerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    consumer_group="$Default",
    credential=DefaultAzureCredential()
)

with consumer:
    consumer.receive(
        on_event=on_event,
        starting_position="-1",  # Beginning of stream
    )
```

### 使用 Blob 检查点存储（生产环境）

```python
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore
from azure.identity import DefaultAzureCredential

checkpoint_store = BlobCheckpointStore(
    blob_account_url="https://<account>.blob.core.windows.net",
    container_name="checkpoints",
    credential=DefaultAzureCredential()
)

consumer = EventHubConsumerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    consumer_group="$Default",
    credential=DefaultAzureCredential(),
    checkpoint_store=checkpoint_store
)

def on_event(partition_context, event):
    print(f"Received: {event.body_as_str()}")
    # Checkpoint after processing
    partition_context.update_checkpoint(event)

with consumer:
    consumer.receive(on_event=on_event)
```

## 异步客户端

```python
from azure.eventhub.aio import EventHubProducerClient, EventHubConsumerClient
from azure.identity.aio import DefaultAzureCredential
import asyncio

async def send_events():
    credential = DefaultAzureCredential()
    
    async with EventHubProducerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="my-eventhub",
        credential=credential
    ) as producer:
        batch = await producer.create_batch()
        batch.add(EventData("Async event"))
        await producer.send_batch(batch)

async def receive_events():
    async def on_event(partition_context, event):
        print(event.body_as_str())
        await partition_context.update_checkpoint(event)
    
    async with EventHubConsumerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="my-eventhub",
        consumer_group="$Default",
        credential=DefaultAzureCredential()
    ) as consumer:
        await consumer.receive(on_event=on_event)

asyncio.run(send_events())
```

## 事件属性

```python
event = EventData("My event body")

# Set properties
event.properties = {"custom_property": "value"}
event.content_type = "application/json"

# Read properties (on receive)
print(event.body_as_str())
print(event.sequence_number)
print(event.offset)
print(event.enqueued_time)
print(event.partition_key)
```

## 获取 Event Hub 信息

```python
with producer:
    info = producer.get_eventhub_properties()
    print(f"Name: {info['name']}")
    print(f"Partitions: {info['partition_ids']}")
    
    for partition_id in info['partition_ids']:
        partition_info = producer.get_partition_properties(partition_id)
        print(f"Partition {partition_id}: {partition_info['last_enqueued_sequence_number']}")
```

## 最佳实践

1. **使用批次**发送多个事件
2. **使用检查点存储**确保生产环境的可靠处理
3. **使用异步客户端**应对高吞吐量场景
4. **使用分区键**实现分区内有序交付
5. **处理批次大小限制** — 批次满时捕获 ValueError
6. **使用上下文管理器**（`with`/`async with`）确保正确清理
7. **为不同应用设置合适的消费者组**

## 参考文件

| 文件 | 内容 |
|------|------|
| references/checkpointing.md | 检查点存储模式、Blob 检查点、检查点策略 |
| references/partitions.md | 分区管理、负载均衡、起始位置 |
| scripts/setup_consumer.py | Event Hub 信息查询、消费者设置和事件发送/接收的 CLI |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代针对特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
