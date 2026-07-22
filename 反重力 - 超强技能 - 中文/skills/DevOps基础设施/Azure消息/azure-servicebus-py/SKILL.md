---
name: azure-servicebus-py
description: Azure Service Bus Python SDK 消息传递。当用户要求"使用 Azure Service Bus 进行队列、主题、订阅和企业消息传递"时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Service Bus SDK for Python

通过队列和发布/订阅主题实现可靠云通信的企业级消息传递。

## 安装

```bash
pip install azure-servicebus azure-identity
```

## 环境变量

```bash
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
SERVICEBUS_QUEUE_NAME=myqueue
SERVICEBUS_TOPIC_NAME=mytopic
SERVICEBUS_SUBSCRIPTION_NAME=mysubscription
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

credential = DefaultAzureCredential()
namespace = "<namespace>.servicebus.windows.net"

client = ServiceBusClient(
    fully_qualified_namespace=namespace,
    credential=credential
)
```

## 客户端类型

| 客户端 | 用途 | 获取方式 |
|--------|------|----------|
| `ServiceBusClient` | 连接管理 | 直接实例化 |
| `ServiceBusSender` | 发送消息 | `client.get_queue_sender()` / `get_topic_sender()` |
| `ServiceBusReceiver` | 接收消息 | `client.get_queue_receiver()` / `get_subscription_receiver()` |

## 发送消息（异步）

```python
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.identity.aio import DefaultAzureCredential

async def send_messages():
    credential = DefaultAzureCredential()
    
    async with ServiceBusClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        credential=credential
    ) as client:
        sender = client.get_queue_sender(queue_name="myqueue")
        
        async with sender:
            # Single message
            message = ServiceBusMessage("Hello, Service Bus!")
            await sender.send_messages(message)
            
            # Batch of messages
            messages = [ServiceBusMessage(f"Message {i}") for i in range(10)]
            await sender.send_messages(messages)
            
            # Message batch (for size control)
            batch = await sender.create_message_batch()
            for i in range(100):
                try:
                    batch.add_message(ServiceBusMessage(f"Batch message {i}"))
                except ValueError:  # Batch full
                    await sender.send_messages(batch)
                    batch = await sender.create_message_batch()
                    batch.add_message(ServiceBusMessage(f"Batch message {i}"))
            await sender.send_messages(batch)

asyncio.run(send_messages())
```

## 接收消息（异步）

```python
async def receive_messages():
    credential = DefaultAzureCredential()
    
    async with ServiceBusClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        credential=credential
    ) as client:
        receiver = client.get_queue_receiver(queue_name="myqueue")
        
        async with receiver:
            # Receive batch
            messages = await receiver.receive_messages(
                max_message_count=10,
                max_wait_time=5  # seconds
            )
            
            for msg in messages:
                print(f"Received: {str(msg)}")
                await receiver.complete_message(msg)  # Remove from queue

asyncio.run(receive_messages())
```

## 接收模式

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| `PEEK_LOCK`（默认） | 消息被锁定，必须完成/放弃 | 可靠处理 |
| `RECEIVE_AND_DELETE` | 接收后立即移除 | 最多一次投递 |

```python
from azure.servicebus import ServiceBusReceiveMode

receiver = client.get_queue_receiver(
    queue_name="myqueue",
    receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE
)
```

## 消息处置

```python
async with receiver:
    messages = await receiver.receive_messages(max_message_count=1)
    
    for msg in messages:
        try:
            # Process message...
            await receiver.complete_message(msg)  # Success - remove from queue
        except ProcessingError:
            await receiver.abandon_message(msg)  # Retry later
        except PermanentError:
            await receiver.dead_letter_message(
                msg,
                reason="ProcessingFailed",
                error_description="Could not process"
            )
```

| 操作 | 效果 |
|------|------|
| `complete_message()` | 从队列中移除（成功） |
| `abandon_message()` | 释放锁，立即重试 |
| `dead_letter_message()` | 移至死信队列 |
| `defer_message()` | 暂置，按序列号接收 |

## 主题和订阅

```python
# Send to topic
sender = client.get_topic_sender(topic_name="mytopic")
async with sender:
    await sender.send_messages(ServiceBusMessage("Topic message"))

# Receive from subscription
receiver = client.get_subscription_receiver(
    topic_name="mytopic",
    subscription_name="mysubscription"
)
async with receiver:
    messages = await receiver.receive_messages(max_message_count=10)
```

## 会话（FIFO）

```python
# Send with session
message = ServiceBusMessage("Session message")
message.session_id = "order-123"
await sender.send_messages(message)

# Receive from specific session
receiver = client.get_queue_receiver(
    queue_name="session-queue",
    session_id="order-123"
)

# Receive from next available session
from azure.servicebus import NEXT_AVAILABLE_SESSION
receiver = client.get_queue_receiver(
    queue_name="session-queue",
    session_id=NEXT_AVAILABLE_SESSION
)
```

## 计划消息

```python
from datetime import datetime, timedelta, timezone

message = ServiceBusMessage("Scheduled message")
scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=10)

# Schedule message
sequence_number = await sender.schedule_messages(message, scheduled_time)

# Cancel scheduled message
await sender.cancel_scheduled_messages(sequence_number)
```

## 死信队列

```python
from azure.servicebus import ServiceBusSubQueue

# Receive from dead-letter queue
dlq_receiver = client.get_queue_receiver(
    queue_name="myqueue",
    sub_queue=ServiceBusSubQueue.DEAD_LETTER
)

async with dlq_receiver:
    messages = await dlq_receiver.receive_messages(max_message_count=10)
    for msg in messages:
        print(f"Dead-lettered: {msg.dead_letter_reason}")
        await dlq_receiver.complete_message(msg)
```

## 同步客户端（用于简单脚本）

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=DefaultAzureCredential()
) as client:
    with client.get_queue_sender("myqueue") as sender:
        sender.send_messages(ServiceBusMessage("Sync message"))
    
    with client.get_queue_receiver("myqueue") as receiver:
        for msg in receiver:
            print(str(msg))
            receiver.complete_message(msg)
```

## 最佳实践

1. **生产负载使用异步客户端**
2. **使用上下文管理器**（`async with`）确保正确清理
3. **处理成功后完成消息**
4. **对有害消息使用死信队列**
5. **使用会话**实现有序的 FIFO 处理
6. **使用消息批次**应对高吞吐场景
7. **设置 `max_wait_time`** 避免无限阻塞

## 参考文件

| 文件 | 内容 |
|------|------|
| references/patterns.md | 竞争消费者、会话、重试模式、请求-响应、事务 |
| references/dead-letter.md | 死信队列处理、有害消息、重处理策略 |
| scripts/setup_servicebus.py | 队列/主题/订阅管理和死信队列监控的 CLI 工具 |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
