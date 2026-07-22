---
name: azure-eventgrid-py
description: Azure Event Grid Python SDK，用于发布事件、处理 CloudEvents 和构建事件驱动架构。当用户要求'Azure Event Grid'、'发布事件'、'CloudEvents'、'事件驱动架构'、'Event Grid Python'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Event Grid SDK for Python

用于构建具有发布/订阅语义的事件驱动应用程序的事件路由服务。

## 安装

```bash
pip install azure-eventgrid azure-identity
```

## 环境变量

```bash
EVENTGRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENTGRID_NAMESPACE_ENDPOINT=https://<namespace>.<region>.eventgrid.azure.net
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.eventgrid import EventGridPublisherClient

credential = DefaultAzureCredential()
endpoint = "https://<topic-name>.<region>.eventgrid.azure.net/api/events"

client = EventGridPublisherClient(endpoint, credential)
```

## 事件类型

| 格式 | 类 | 用途 |
|--------|-------|----------|
| Cloud Events 1.0 | `CloudEvent` | 标准化、可互操作（推荐） |
| Event Grid Schema | `EventGridEvent` | Azure 原生格式 |

## 发布 CloudEvents

```python
from azure.eventgrid import EventGridPublisherClient, CloudEvent
from azure.identity import DefaultAzureCredential

client = EventGridPublisherClient(endpoint, DefaultAzureCredential())

# Single event
event = CloudEvent(
    type="MyApp.Events.OrderCreated",
    source="/myapp/orders",
    data={"order_id": "12345", "amount": 99.99}
)
client.send(event)

# Multiple events
events = [
    CloudEvent(
        type="MyApp.Events.OrderCreated",
        source="/myapp/orders",
        data={"order_id": f"order-{i}"}
    )
    for i in range(10)
]
client.send(events)
```

## 发布 EventGridEvents

```python
from azure.eventgrid import EventGridEvent
from datetime import datetime, timezone

event = EventGridEvent(
    subject="/myapp/orders/12345",
    event_type="MyApp.Events.OrderCreated",
    data={"order_id": "12345", "amount": 99.99},
    data_version="1.0"
)

client.send(event)
```

## 事件属性

### CloudEvent 属性

```python
event = CloudEvent(
    type="MyApp.Events.ItemCreated",      # Required: event type
    source="/myapp/items",                 # Required: event source
    data={"key": "value"},                 # Event payload
    subject="items/123",                   # Optional: subject/path
    datacontenttype="application/json",   # Optional: content type
    dataschema="https://schema.example",  # Optional: schema URL
    time=datetime.now(timezone.utc),      # Optional: timestamp
    extensions={"custom": "value"}         # Optional: custom attributes
)
```

### EventGridEvent 属性

```python
event = EventGridEvent(
    subject="/myapp/items/123",            # Required: subject
    event_type="MyApp.ItemCreated",        # Required: event type
    data={"key": "value"},                 # Required: event payload
    data_version="1.0",                    # Required: schema version
    topic="/subscriptions/.../topics/...", # Optional: auto-set
    event_time=datetime.now(timezone.utc)  # Optional: timestamp
)
```

## 异步客户端

```python
from azure.eventgrid.aio import EventGridPublisherClient
from azure.identity.aio import DefaultAzureCredential

async def publish_events():
    credential = DefaultAzureCredential()
    
    async with EventGridPublisherClient(endpoint, credential) as client:
        event = CloudEvent(
            type="MyApp.Events.Test",
            source="/myapp",
            data={"message": "hello"}
        )
        await client.send(event)

import asyncio
asyncio.run(publish_events())
```

## 命名空间主题（Event Grid Namespaces）

用于 Event Grid Namespaces（拉取交付模式）：

```python
from azure.eventgrid.aio import EventGridPublisherClient

# Namespace endpoint (different from custom topic)
namespace_endpoint = "https://<namespace>.<region>.eventgrid.azure.net"
topic_name = "my-topic"

async with EventGridPublisherClient(
    endpoint=namespace_endpoint,
    credential=DefaultAzureCredential()
) as client:
    await client.send(
        event,
        namespace_topic=topic_name
    )
```

## 最佳实践

1. **新应用使用 CloudEvents**（行业标准）
2. **批量发布**多个事件时使用批量发送
3. **包含有意义的 subject** 以便过滤
4. **高吞吐量场景使用异步客户端**
5. **处理重试** — Event Grid 内置重试机制
6. **设置合适的事件类型** 用于路由和过滤

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
