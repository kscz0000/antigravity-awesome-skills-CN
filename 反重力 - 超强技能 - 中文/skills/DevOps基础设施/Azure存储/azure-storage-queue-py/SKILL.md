---
name: azure-storage-queue-py
description: Azure Queue Storage Python SDK，用于可靠的消息队列、任务分发和异步处理。当用户要求'Azure队列存储'、'消息队列Python'、'Azure Queue Storage'、'异步消息处理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Queue Storage SDK for Python

简单、低成本的消息队列，用于异步通信。

## 安装

```bash
pip install azure-storage-queue azure-identity
```

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_URL=https://<account>.queue.core.windows.net
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient

credential = DefaultAzureCredential()
account_url = "https://<account>.queue.core.windows.net"

# Service client
service_client = QueueServiceClient(account_url=account_url, credential=credential)

# Queue client
queue_client = QueueClient(account_url=account_url, queue_name="myqueue", credential=credential)
```

## 队列操作

```python
# Create queue
service_client.create_queue("myqueue")

# Get queue client
queue_client = service_client.get_queue_client("myqueue")

# Delete queue
service_client.delete_queue("myqueue")

# List queues
for queue in service_client.list_queues():
    print(queue.name)
```

## 发送消息

```python
# Send message (string)
queue_client.send_message("Hello, Queue!")

# Send with options
queue_client.send_message(
    content="Delayed message",
    visibility_timeout=60,  # Hidden for 60 seconds
    time_to_live=3600       # Expires in 1 hour
)

# Send JSON
import json
data = {"task": "process", "id": 123}
queue_client.send_message(json.dumps(data))
```

## 接收消息

```python
# Receive messages (makes them invisible temporarily)
messages = queue_client.receive_messages(
    messages_per_page=10,
    visibility_timeout=30  # 30 seconds to process
)

for message in messages:
    print(f"ID: {message.id}")
    print(f"Content: {message.content}")
    print(f"Dequeue count: {message.dequeue_count}")
    
    # Process message...
    
    # Delete after processing
    queue_client.delete_message(message)
```

## 查看消息

```python
# Peek without hiding (doesn't affect visibility)
messages = queue_client.peek_messages(max_messages=5)

for message in messages:
    print(message.content)
```

## 更新消息

```python
# Extend visibility or update content
messages = queue_client.receive_messages()
for message in messages:
    # Extend timeout (need more time)
    queue_client.update_message(
        message,
        visibility_timeout=60
    )
    
    # Update content and timeout
    queue_client.update_message(
        message,
        content="Updated content",
        visibility_timeout=60
    )
```

## 删除消息

```python
# Delete after successful processing
messages = queue_client.receive_messages()
for message in messages:
    try:
        # Process...
        queue_client.delete_message(message)
    except Exception:
        # Message becomes visible again after timeout
        pass
```

## 清空队列

```python
# Delete all messages
queue_client.clear_messages()
```

## 队列属性

```python
# Get queue properties
properties = queue_client.get_queue_properties()
print(f"Approximate message count: {properties.approximate_message_count}")

# Set/get metadata
queue_client.set_queue_metadata(metadata={"environment": "production"})
properties = queue_client.get_queue_properties()
print(properties.metadata)
```

## 异步客户端

```python
from azure.storage.queue.aio import QueueServiceClient, QueueClient
from azure.identity.aio import DefaultAzureCredential

async def queue_operations():
    credential = DefaultAzureCredential()
    
    async with QueueClient(
        account_url="https://<account>.queue.core.windows.net",
        queue_name="myqueue",
        credential=credential
    ) as client:
        # Send
        await client.send_message("Async message")
        
        # Receive
        async for message in client.receive_messages():
            print(message.content)
            await client.delete_message(message)

import asyncio
asyncio.run(queue_operations())
```

## Base64 编码

```python
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

# For binary data
queue_client = QueueClient(
    account_url=account_url,
    queue_name="myqueue",
    credential=credential,
    message_encode_policy=BinaryBase64EncodePolicy(),
    message_decode_policy=BinaryBase64DecodePolicy()
)

# Send bytes
queue_client.send_message(b"Binary content")
```

## 最佳实践

1. **处理后删除消息**，防止重复处理
2. **根据处理时间设置合适的可见性超时**
3. **处理 `dequeue_count`**，用于检测毒消息
4. **高吞吐场景使用异步客户端**
5. **使用 `peek_messages`** 监控队列而不影响消息可见性
6. **设置 `time_to_live`**，防止过期消息堆积
7. **需要高级功能（会话、主题）时考虑 Service Bus**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
