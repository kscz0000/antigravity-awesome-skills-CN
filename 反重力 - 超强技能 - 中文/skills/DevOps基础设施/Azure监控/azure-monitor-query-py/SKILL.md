---
name: azure-monitor-query-py
description: Azure Monitor Query Python SDK。查询 Log Analytics 工作区和 Azure Monitor 指标。当用户要求"查询Azure Monitor日志"、"查询Log Analytics工作区"、"获取Azure指标数据"时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor Query SDK for Python

从 Azure Monitor 和 Log Analytics 工作区查询日志与指标。

## 安装

```bash
pip install azure-monitor-query
```

## 环境变量

```bash
# Log Analytics
AZURE_LOG_ANALYTICS_WORKSPACE_ID=<workspace-id>

# Metrics
AZURE_METRICS_RESOURCE_URI=/subscriptions/<sub>/resourceGroups/<rg>/providers/<provider>/<type>/<name>
```

## 身份认证

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
```

## 日志查询客户端

### 基本查询

```python
from azure.monitor.query import LogsQueryClient
from datetime import timedelta

client = LogsQueryClient(credential)

query = """
AppRequests
| where TimeGenerated > ago(1h)
| summarize count() by bin(TimeGenerated, 5m), ResultCode
| order by TimeGenerated desc
"""

response = client.query_workspace(
    workspace_id=os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"],
    query=query,
    timespan=timedelta(hours=1)
)

for table in response.tables:
    for row in table.rows:
        print(row)
```

### 带时间范围的查询

```python
from datetime import datetime, timezone

response = client.query_workspace(
    workspace_id=workspace_id,
    query="AppRequests | take 10",
    timespan=(
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 1, 2, tzinfo=timezone.utc)
    )
)
```

### 转换为 DataFrame

```python
import pandas as pd

response = client.query_workspace(workspace_id, query, timespan=timedelta(hours=1))

if response.tables:
    table = response.tables[0]
    df = pd.DataFrame(data=table.rows, columns=[col.name for col in table.columns])
    print(df.head())
```

### 批量查询

```python
from azure.monitor.query import LogsBatchQuery

queries = [
    LogsBatchQuery(workspace_id=workspace_id, query="AppRequests | take 5", timespan=timedelta(hours=1)),
    LogsBatchQuery(workspace_id=workspace_id, query="AppExceptions | take 5", timespan=timedelta(hours=1))
]

responses = client.query_batch(queries)

for response in responses:
    if response.tables:
        print(f"Rows: {len(response.tables[0].rows)}")
```

### 处理部分结果

```python
from azure.monitor.query import LogsQueryStatus

response = client.query_workspace(workspace_id, query, timespan=timedelta(hours=24))

if response.status == LogsQueryStatus.PARTIAL:
    print(f"Partial results: {response.partial_error}")
elif response.status == LogsQueryStatus.FAILURE:
    print(f"Query failed: {response.partial_error}")
```

## 指标查询客户端

### 查询资源指标

```python
from azure.monitor.query import MetricsQueryClient
from datetime import timedelta

metrics_client = MetricsQueryClient(credential)

response = metrics_client.query_resource(
    resource_uri=os.environ["AZURE_METRICS_RESOURCE_URI"],
    metric_names=["Percentage CPU", "Network In Total"],
    timespan=timedelta(hours=1),
    granularity=timedelta(minutes=5)
)

for metric in response.metrics:
    print(f"{metric.name}:")
    for time_series in metric.timeseries:
        for data in time_series.data:
            print(f"  {data.timestamp}: {data.average}")
```

### 聚合

```python
from azure.monitor.query import MetricAggregationType

response = metrics_client.query_resource(
    resource_uri=resource_uri,
    metric_names=["Requests"],
    timespan=timedelta(hours=1),
    aggregations=[
        MetricAggregationType.AVERAGE,
        MetricAggregationType.MAXIMUM,
        MetricAggregationType.MINIMUM,
        MetricAggregationType.COUNT
    ]
)
```

### 按维度筛选

```python
response = metrics_client.query_resource(
    resource_uri=resource_uri,
    metric_names=["Requests"],
    timespan=timedelta(hours=1),
    filter="ApiName eq 'GetBlob'"
)
```

### 列出指标定义

```python
definitions = metrics_client.list_metric_definitions(resource_uri)
for definition in definitions:
    print(f"{definition.name}: {definition.unit}")
```

### 列出指标命名空间

```python
namespaces = metrics_client.list_metric_namespaces(resource_uri)
for ns in namespaces:
    print(ns.fully_qualified_namespace)
```

## 异步客户端

```python
from azure.monitor.query.aio import LogsQueryClient, MetricsQueryClient
from azure.identity.aio import DefaultAzureCredential

async def query_logs():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    
    response = await client.query_workspace(
        workspace_id=workspace_id,
        query="AppRequests | take 10",
        timespan=timedelta(hours=1)
    )
    
    await client.close()
    await credential.close()
    return response
```

## 常用 Kusto 查询

```kusto
// Requests by status code
AppRequests
| summarize count() by ResultCode
| order by count_ desc

// Exceptions over time
AppExceptions
| summarize count() by bin(TimeGenerated, 1h)

// Slow requests
AppRequests
| where DurationMs > 1000
| project TimeGenerated, Name, DurationMs
| order by DurationMs desc

// Top errors
AppExceptions
| summarize count() by ExceptionType
| top 10 by count_
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `LogsQueryClient` | 查询 Log Analytics 工作区 |
| `MetricsQueryClient` | 查询 Azure Monitor 指标 |

## 最佳实践

1. **使用 timedelta** 表示相对时间范围
2. **处理部分结果** 以应对大型查询
3. **使用批量查询** 执行多个查询时
4. **设置合适的粒度** 以减少指标数据点
5. **转换为 DataFrame** 便于数据分析
6. **使用聚合** 汇总指标数据
7. **按维度筛选** 缩小指标结果范围

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
