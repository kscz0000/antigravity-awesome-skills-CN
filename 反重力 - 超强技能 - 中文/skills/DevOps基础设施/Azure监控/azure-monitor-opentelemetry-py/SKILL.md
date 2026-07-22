---
name: azure-monitor-opentelemetry-py
description: Azure Monitor OpenTelemetry Python 发行版。一行代码完成 Application Insights 设置与自动检测。当用户要求'配置 Azure Monitor OpenTelemetry Python'、'设置 Application Insights 自动检测'、'Python 应用监控接入'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor OpenTelemetry Python 发行版

一行代码完成 Application Insights 与 OpenTelemetry 自动检测的设置。

## 安装

```bash
pip install azure-monitor-opentelemetry
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## 快速开始

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# One-line setup - reads connection string from environment
configure_azure_monitor()

# Your application code...
```

## 显式配置

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/"
)
```

## 配合 Flask

```python
from flask import Flask
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
```

## 配合 Django

```python
# settings.py
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

# Django settings...
```

## 配合 FastAPI

```python
from fastapi import FastAPI
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## 自定义 Traces

```python
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Do work...
```

## 自定义 Metrics

```python
from opentelemetry import metrics
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

meter = metrics.get_meter(__name__)
counter = meter.create_counter("my_counter")

counter.add(1, {"dimension": "value"})
```

## 自定义日志

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("This will appear in Application Insights")
logger.error("Errors are captured too", exc_info=True)
```

## 采样

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Sample 10% of requests
configure_azure_monitor(
    sampling_ratio=0.1
)
```

## 云角色名称

为 Application Map 设置云角色名称：

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

configure_azure_monitor(
    resource=Resource.create({SERVICE_NAME: "my-service-name"})
)
```

## 禁用特定检测

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    instrumentations=["flask", "requests"]  # Only enable these
)
```

## 启用实时指标

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    enable_live_metrics=True
)
```

## Azure AD 认证

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.identity import DefaultAzureCredential

configure_azure_monitor(
    credential=DefaultAzureCredential()
)
```

## 包含的自动检测

| 库 | 遥测类型 |
|---------|---------------|
| Flask | Traces |
| Django | Traces |
| FastAPI | Traces |
| Requests | Traces |
| urllib3 | Traces |
| httpx | Traces |
| aiohttp | Traces |
| psycopg2 | Traces |
| pymysql | Traces |
| pymongo | Traces |
| redis | Traces |

## 配置选项

| 参数 | 说明 | 默认值 |
|-----------|-------------|---------|
| `connection_string` | Application Insights 连接字符串 | 从环境变量读取 |
| `credential` | 用于 AAD 认证的 Azure 凭据 | None |
| `sampling_ratio` | 采样率（0.0 到 1.0） | 1.0 |
| `resource` | OpenTelemetry Resource | 自动检测 |
| `instrumentations` | 要启用的检测列表 | 全部 |
| `enable_live_metrics` | 启用实时指标流 | False |

## 最佳实践

1. **尽早调用 configure_azure_monitor()** — 在导入被检测的库之前
2. **在生产环境中使用环境变量** 存放连接字符串
3. **为多服务应用设置云角色名称**
4. **在高流量应用中启用采样**
5. **使用结构化日志** 以获得更好的日志分析查询
6. **为 span 添加自定义属性** 以便更好地调试
7. **在生产工作负载中使用 AAD 认证**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
