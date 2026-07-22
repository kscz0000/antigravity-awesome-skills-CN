---
name: azure-messaging-webpubsubservice-py
description: Azure Web PubSub Service Python SDK，用于实时消息传递、WebSocket 连接和发布/订阅模式。当用户要求'Azure Web PubSub'、'实时消息'、'WebSocket 发布订阅'、'Python 实时通信'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Web PubSub Service SDK for Python

使用 WebSocket 连接实现大规模实时消息传递。

## 安装

```bash
# Service SDK (server-side)
pip install azure-messaging-webpubsubservice

# Client SDK (for Python WebSocket clients)
pip install azure-messaging-webpubsubclient
```

## 环境变量

```bash
AZURE_WEBPUBSUB_CONNECTION_STRING=Endpoint=https://<name>.webpubsub.azure.com;AccessKey=...
AZURE_WEBPUBSUB_HUB=my-hub
```

## 服务客户端（服务端）

### 身份认证

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# Connection string
client = WebPubSubServiceClient.from_connection_string(
    connection_string=os.environ["AZURE_WEBPUBSUB_CONNECTION_STRING"],
    hub="my-hub"
)

# Entra ID
from azure.identity import DefaultAzureCredential

client = WebPubSubServiceClient(
    endpoint="https://<name>.webpubsub.azure.com",
    hub="my-hub",
    credential=DefaultAzureCredential()
)
```

### 生成客户端访问令牌

```python
# Token for anonymous user
token = client.get_client_access_token()
print(f"URL: {token['url']}")

# Token with user ID
token = client.get_client_access_token(
    user_id="user123",
    roles=["webpubsub.sendToGroup", "webpubsub.joinLeaveGroup"]
)

# Token with groups
token = client.get_client_access_token(
    user_id="user123",
    groups=["group1", "group2"]
)
```

### 向所有客户端发送消息

```python
# Send text
client.send_to_all(message="Hello everyone!", content_type="text/plain")

# Send JSON
client.send_to_all(
    message={"type": "notification", "data": "Hello"},
    content_type="application/json"
)
```

### 向指定用户发送消息

```python
client.send_to_user(
    user_id="user123",
    message="Hello user!",
    content_type="text/plain"
)
```

### 向指定组发送消息

```python
client.send_to_group(
    group="my-group",
    message="Hello group!",
    content_type="text/plain"
)
```

### 向指定连接发送消息

```python
client.send_to_connection(
    connection_id="abc123",
    message="Hello connection!",
    content_type="text/plain"
)
```

### 组管理

```python
# Add user to group
client.add_user_to_group(group="my-group", user_id="user123")

# Remove user from group
client.remove_user_from_group(group="my-group", user_id="user123")

# Add connection to group
client.add_connection_to_group(group="my-group", connection_id="abc123")

# Remove connection from group
client.remove_connection_from_group(group="my-group", connection_id="abc123")
```

### 连接管理

```python
# Check if connection exists
exists = client.connection_exists(connection_id="abc123")

# Check if user has connections
exists = client.user_exists(user_id="user123")

# Check if group has connections
exists = client.group_exists(group="my-group")

# Close connection
client.close_connection(connection_id="abc123", reason="Session ended")

# Close all connections for user
client.close_all_connections(user_id="user123")
```

### 授予/撤销权限

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# Grant permission
client.grant_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# Revoke permission
client.revoke_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# Check permission
has_permission = client.check_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)
```

## 客户端 SDK（Python WebSocket 客户端）

```python
from azure.messaging.webpubsubclient import WebPubSubClient

client = WebPubSubClient(credential=token["url"])

# Event handlers
@client.on("connected")
def on_connected(e):
    print(f"Connected: {e.connection_id}")

@client.on("server-message")
def on_message(e):
    print(f"Message: {e.data}")

@client.on("group-message")
def on_group_message(e):
    print(f"Group {e.group}: {e.data}")

# Connect and send
client.open()
client.send_to_group("my-group", "Hello from Python!")
```

## 异步服务客户端

```python
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.identity.aio import DefaultAzureCredential

async def broadcast():
    credential = DefaultAzureCredential()
    client = WebPubSubServiceClient(
        endpoint="https://<name>.webpubsub.azure.com",
        hub="my-hub",
        credential=credential
    )
    
    await client.send_to_all("Hello async!", content_type="text/plain")
    
    await client.close()
    await credential.close()
```

## 客户端操作

| 操作 | 描述 |
|-----------|-------------|
| `get_client_access_token` | 生成 WebSocket 连接 URL |
| `send_to_all` | 向所有连接广播 |
| `send_to_user` | 向指定用户发送 |
| `send_to_group` | 向组成员发送 |
| `send_to_connection` | 向指定连接发送 |
| `add_user_to_group` | 将用户添加到组 |
| `remove_user_from_group` | 将用户从组中移除 |
| `close_connection` | 断开客户端连接 |
| `connection_exists` | 检查连接状态 |

## 最佳实践

1. **使用角色** 限制客户端权限
2. **使用组** 进行定向消息传递
3. **生成短期令牌** 以确保安全
4. **使用用户 ID** 跨连接向用户发送消息
5. **处理重连** 在客户端应用中
6. **使用 JSON** 内容类型传递结构化数据
7. **优雅关闭连接** 并附上原因

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
