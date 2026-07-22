---
name: azure-appconfiguration-py
description: Azure App Configuration Python SDK，用于集中化配置管理、功能开关和动态设置。触发词：Azure配置、App Configuration、配置中心、功能开关、feature flag、动态配置、Python配置管理、Azure SDK、配置管理、集中配置
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure App Configuration SDK for Python

集中化配置管理，支持功能开关和动态设置。

## 安装

```bash
pip install azure-appconfiguration
```

## 环境变量

```bash
AZURE_APPCONFIGURATION_CONNECTION_STRING=Endpoint=https://<name>.azconfig.io;Id=...;Secret=...
# 或使用 Entra ID：
AZURE_APPCONFIGURATION_ENDPOINT=https://<name>.azconfig.io
```

## 认证

### 连接字符串

```python
from azure.appconfiguration import AzureAppConfigurationClient

client = AzureAppConfigurationClient.from_connection_string(
    os.environ["AZURE_APPCONFIGURATION_CONNECTION_STRING"]
)
```

### Entra ID

```python
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential

client = AzureAppConfigurationClient(
    base_url=os.environ["AZURE_APPCONFIGURATION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 配置设置

### 获取设置

```python
setting = client.get_configuration_setting(key="app:settings:message")
print(f"{setting.key} = {setting.value}")
```

### 使用标签获取

```python
# 标签允许环境特定的值
setting = client.get_configuration_setting(
    key="app:settings:message",
    label="production"
)
```

### 设置值

```python
from azure.appconfiguration import ConfigurationSetting

setting = ConfigurationSetting(
    key="app:settings:message",
    value="Hello, World!",
    label="development",
    content_type="text/plain",
    tags={"environment": "dev"}
)

client.set_configuration_setting(setting)
```

### 删除设置

```python
client.delete_configuration_setting(
    key="app:settings:message",
    label="development"
)
```

## 列出设置

### 所有设置

```python
settings = client.list_configuration_settings()
for setting in settings:
    print(f"{setting.key} [{setting.label}] = {setting.value}")
```

### 按键前缀过滤

```python
settings = client.list_configuration_settings(
    key_filter="app:settings:*"
)
```

### 按标签过滤

```python
settings = client.list_configuration_settings(
    label_filter="production"
)
```

## 功能开关

### 设置功能开关

```python
from azure.appconfiguration import ConfigurationSetting
import json

feature_flag = ConfigurationSetting(
    key=".appconfig.featureflag/beta-feature",
    value=json.dumps({
        "id": "beta-feature",
        "enabled": True,
        "conditions": {
            "client_filters": []
        }
    }),
    content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8"
)

client.set_configuration_setting(feature_flag)
```

### 获取功能开关

```python
setting = client.get_configuration_setting(
    key=".appconfig.featureflag/beta-feature"
)
flag_data = json.loads(setting.value)
print(f"Feature enabled: {flag_data['enabled']}")
```

### 列出功能开关

```python
flags = client.list_configuration_settings(
    key_filter=".appconfig.featureflag/*"
)
for flag in flags:
    data = json.loads(flag.value)
    print(f"{data['id']}: {'enabled' if data['enabled'] else 'disabled'}")
```

## 只读设置

```python
# 将设置设为只读
client.set_read_only(
    configuration_setting=setting,
    read_only=True
)

# 取消只读
client.set_read_only(
    configuration_setting=setting,
    read_only=False
)
```

## 快照

### 创建快照

```python
from azure.appconfiguration import ConfigurationSnapshot, ConfigurationSettingFilter

snapshot = ConfigurationSnapshot(
    name="v1-snapshot",
    filters=[
        ConfigurationSettingFilter(key="app:*", label="production")
    ]
)

created = client.begin_create_snapshot(
    name="v1-snapshot",
    snapshot=snapshot
).result()
```

### 列出快照设置

```python
settings = client.list_configuration_settings(
    snapshot_name="v1-snapshot"
)
```

## 异步客户端

```python
from azure.appconfiguration.aio import AzureAppConfigurationClient
from azure.identity.aio import DefaultAzureCredential

async def main():
    credential = DefaultAzureCredential()
    client = AzureAppConfigurationClient(
        base_url=endpoint,
        credential=credential
    )
    
    setting = await client.get_configuration_setting(key="app:message")
    print(setting.value)
    
    await client.close()
    await credential.close()
```

## 客户端操作

| 操作 | 描述 |
|-----------|-------------|
| `get_configuration_setting` | 获取单个设置 |
| `set_configuration_setting` | 创建或更新设置 |
| `delete_configuration_setting` | 删除设置 |
| `list_configuration_settings` | 使用过滤器列出设置 |
| `set_read_only` | 锁定/解锁设置 |
| `begin_create_snapshot` | 创建时间点快照 |
| `list_snapshots` | 列出所有快照 |

## 最佳实践

1. **使用标签**进行环境分离（dev、staging、prod）
2. **使用键前缀**进行逻辑分组（app:database:*、app:cache:*）
3. **将生产设置设为只读**以防止意外更改
4. **在部署前创建快照**以便回滚
5. **在生产环境中使用 Entra ID**而非连接字符串
6. **在长时间运行的应用中定期刷新设置**
7. **使用功能开关**进行渐进式发布和 A/B 测试

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
