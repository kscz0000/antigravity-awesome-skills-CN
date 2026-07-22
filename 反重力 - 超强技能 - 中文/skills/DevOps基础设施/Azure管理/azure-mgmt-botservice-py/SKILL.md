---
name: azure-mgmt-botservice-py
description: Azure Bot Service 管理 SDK for Python，用于创建、管理和配置 Azure Bot Service 资源。当用户要求'管理Azure机器人服务'、'创建Azure Bot'、'配置Bot频道'或'管理Bot连接'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Bot Service Management SDK for Python

管理 Azure Bot Service 资源，包括机器人、频道和连接。

## 安装

```bash
pip install azure-mgmt-botservice
pip install azure-identity
```

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.botservice import AzureBotService
import os

credential = DefaultAzureCredential()
client = AzureBotService(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## 创建机器人

```python
from azure.mgmt.botservice import AzureBotService
from azure.mgmt.botservice.models import Bot, BotProperties, Sku
from azure.identity import DefaultAzureCredential
import os

credential = DefaultAzureCredential()
client = AzureBotService(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)

resource_group = os.environ["AZURE_RESOURCE_GROUP"]
bot_name = "my-chat-bot"

bot = client.bots.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    parameters=Bot(
        location="global",
        sku=Sku(name="F0"),  # Free tier
        kind="azurebot",
        properties=BotProperties(
            display_name="My Chat Bot",
            description="A conversational AI bot",
            endpoint="https://my-bot-app.azurewebsites.net/api/messages",
            msa_app_id="<your-app-id>",
            msa_app_type="MultiTenant"
        )
    )
)

print(f"Bot created: {bot.name}")
```

## 获取机器人详情

```python
bot = client.bots.get(
    resource_group_name=resource_group,
    resource_name=bot_name
)

print(f"Bot: {bot.properties.display_name}")
print(f"Endpoint: {bot.properties.endpoint}")
print(f"SKU: {bot.sku.name}")
```

## 列出资源组中的机器人

```python
bots = client.bots.list_by_resource_group(resource_group_name=resource_group)

for bot in bots:
    print(f"Bot: {bot.name} - {bot.properties.display_name}")
```

## 列出订阅中的所有机器人

```python
all_bots = client.bots.list()

for bot in all_bots:
    print(f"Bot: {bot.name} in {bot.id.split('/')[4]}")
```

## 更新机器人

```python
bot = client.bots.update(
    resource_group_name=resource_group,
    resource_name=bot_name,
    properties=BotProperties(
        display_name="Updated Bot Name",
        description="Updated description"
    )
)
```

## 删除机器人

```python
client.bots.delete(
    resource_group_name=resource_group,
    resource_name=bot_name
)
```

## 配置频道

### 添加 Teams 频道

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    MsTeamsChannel,
    MsTeamsChannelProperties
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="MsTeamsChannel",
    parameters=BotChannel(
        location="global",
        properties=MsTeamsChannel(
            properties=MsTeamsChannelProperties(
                is_enabled=True
            )
        )
    )
)
```

### 添加 Direct Line 频道

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    DirectLineChannel,
    DirectLineChannelProperties,
    DirectLineSite
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel",
    parameters=BotChannel(
        location="global",
        properties=DirectLineChannel(
            properties=DirectLineChannelProperties(
                sites=[
                    DirectLineSite(
                        site_name="Default Site",
                        is_enabled=True,
                        is_v1_enabled=False,
                        is_v3_enabled=True
                    )
                ]
            )
        )
    )
)
```

### 添加 Web Chat 频道

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    WebChatChannel,
    WebChatChannelProperties,
    WebChatSite
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="WebChatChannel",
    parameters=BotChannel(
        location="global",
        properties=WebChatChannel(
            properties=WebChatChannelProperties(
                sites=[
                    WebChatSite(
                        site_name="Default Site",
                        is_enabled=True
                    )
                ]
            )
        )
    )
)
```

## 获取频道详情

```python
channel = client.channels.get(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel"
)
```

## 列出频道密钥

```python
keys = client.channels.list_with_keys(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel"
)

# Access Direct Line keys
if hasattr(keys.properties, 'properties'):
    for site in keys.properties.properties.sites:
        print(f"Site: {site.site_name}")
        print(f"Key: {site.key}")
```

## 机器人连接（OAuth）

### 创建连接设置

```python
from azure.mgmt.botservice.models import (
    ConnectionSetting,
    ConnectionSettingProperties
)

connection = client.bot_connection.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    connection_name="graph-connection",
    parameters=ConnectionSetting(
        location="global",
        properties=ConnectionSettingProperties(
            client_id="<oauth-client-id>",
            client_secret="<oauth-client-secret>",
            scopes="User.Read",
            service_provider_id="<service-provider-id>"
        )
    )
)
```

### 列出连接

```python
connections = client.bot_connection.list_by_bot_service(
    resource_group_name=resource_group,
    resource_name=bot_name
)

for conn in connections:
    print(f"Connection: {conn.name}")
```

## 客户端操作

| 操作 | 方法 |
|------|------|
| `client.bots` | 机器人 CRUD 操作 |
| `client.channels` | 频道配置 |
| `client.bot_connection` | OAuth 连接设置 |
| `client.direct_line` | Direct Line 频道操作 |
| `client.email` | Email 频道操作 |
| `client.operations` | 可用操作 |
| `client.host_settings` | 主机设置操作 |

## SKU 选项

| SKU | 说明 |
|-----|------|
| `F0` | 免费层（消息数受限） |
| `S1` | 标准层（无限消息） |

## 频道类型

| 频道 | 类 | 用途 |
|------|---|------|
| `MsTeamsChannel` | Microsoft Teams | Teams 集成 |
| `DirectLineChannel` | Direct Line | 自定义客户端集成 |
| `WebChatChannel` | Web Chat | 可嵌入的 Web 组件 |
| `SlackChannel` | Slack | Slack 工作区集成 |
| `FacebookChannel` | Facebook | Messenger 集成 |
| `EmailChannel` | Email | 邮件通信 |

## 最佳实践

1. **使用 DefaultAzureCredential** 进行身份验证
2. **开发时使用 F0 SKU**，生产环境升级到 S1
3. **安全存储 MSA App ID/Secret** — 使用 Key Vault
4. **仅启用所需频道** — 减少攻击面
5. **定期轮换 Direct Line 密钥**
6. **尽可能使用托管标识** 进行机器人连接
7. **为 Web Chat 频道配置正确的 CORS**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
