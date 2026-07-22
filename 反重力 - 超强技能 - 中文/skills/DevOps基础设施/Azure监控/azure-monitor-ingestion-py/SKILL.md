---
name: azure-monitor-ingestion-py
description: Azure Monitor Ingestion Python SDK，用于通过 Logs Ingestion API 将自定义日志发送到 Log Analytics 工作区。当用户要求'发送自定义日志到Azure Monitor'、'使用Logs Ingestion API上传日志'、'Azure Monitor日志摄入'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor Ingestion SDK for Python

使用 Logs Ingestion API 将自定义日志发送到 Azure Monitor Log Analytics 工作区。

## 安装

```bash
pip install azure-monitor-ingestion
pip install azure-identity
```

## 环境变量

```bash
# Data Collection Endpoint (DCE)
AZURE_DCE_ENDPOINT=https://<dce-name>.<region>.ingest.monitor.azure.com

# Data Collection Rule (DCR) immutable ID
AZURE_DCR_RULE_ID=dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Stream name from DCR
AZURE_DCR_STREAM_NAME=Custom-MyTable_CL
```

## 前提条件

使用此 SDK 前，你需要：

1. **Log Analytics 工作区** — 日志的目标位置
2. **Data Collection Endpoint (DCE)** — 摄入端点
3. **Data Collection Rule (DCR)** — 定义 Schema 和目标
4. **自定义表** — 在 Log Analytics 中（通过 DCR 或手动创建）

## 身份认证

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 上传自定义日志

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)

rule_id = os.environ["AZURE_DCR_RULE_ID"]
stream_name = os.environ["AZURE_DCR_STREAM_NAME"]

logs = [
    {"TimeGenerated": "2024-01-15T10:00:00Z", "Computer": "server1", "Message": "Application started"},
    {"TimeGenerated": "2024-01-15T10:01:00Z", "Computer": "server1", "Message": "Processing request"},
    {"TimeGenerated": "2024-01-15T10:02:00Z", "Computer": "server2", "Message": "Connection established"}
]

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## 从 JSON 文件上传

```python
import json

with open("logs.json", "r") as f:
    logs = json.load(f)

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## 自定义错误处理

通过回调处理部分失败：

```python
failed_logs = []

def on_error(error):
    print(f"Upload failed: {error.error}")
    failed_logs.extend(error.failed_logs)

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=on_error
)

# Retry failed logs
if failed_logs:
    print(f"Retrying {len(failed_logs)} failed logs...")
    client.upload(rule_id=rule_id, stream_name=stream_name, logs=failed_logs)
```

## 忽略错误

```python
def ignore_errors(error):
    pass  # Silently ignore upload failures

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=ignore_errors
)
```

## 异步客户端

```python
import asyncio
from azure.monitor.ingestion.aio import LogsIngestionClient
from azure.identity.aio import DefaultAzureCredential

async def upload_logs():
    async with LogsIngestionClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        await client.upload(
            rule_id=rule_id,
            stream_name=stream_name,
            logs=logs
        )

asyncio.run(upload_logs())
```

## 主权云

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
client = LogsIngestionClient(
    endpoint="https://example.ingest.monitor.azure.us",
    credential=credential,
    credential_scopes=["https://monitor.azure.us/.default"]
)
```

## 批处理行为

SDK 自动执行以下操作：
- 将日志拆分为 1MB 或更小的块
- 使用 gzip 压缩每个块
- 并行上传各块

大型日志集无需手动批处理。

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `LogsIngestionClient` | 同步上传日志客户端 |
| `LogsIngestionClient` (aio) | 异步上传日志客户端 |

## 核心概念

| 概念 | 说明 |
|------|------|
| **DCE** | Data Collection Endpoint — 摄入 URL |
| **DCR** | Data Collection Rule — 定义 Schema、转换和目标 |
| **Stream** | DCR 中的命名数据流 |
| **自定义表** | Log Analytics 中的目标表（以 `_CL` 结尾） |

## DCR Stream 名称格式

Stream 名称遵循以下模式：
- `Custom-<TableName>_CL` — 用于自定义表
- `Microsoft-<TableName>` — 用于内置表

## 最佳实践

1. **使用 DefaultAzureCredential** 进行身份认证
2. **优雅处理错误** — 使用 `on_error` 回调处理部分失败
3. **包含 TimeGenerated** — 所有日志的必填字段
4. **匹配 DCR Schema** — 日志字段必须与 DCR 列定义匹配
5. **高吞吐场景使用异步客户端**
6. **批量上传** — SDK 处理批处理，但应发送合理的块大小
7. **监控摄入状态** — 检查 Log Analytics 中的摄入状态
8. **使用上下文管理器** — 确保客户端正确清理

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
