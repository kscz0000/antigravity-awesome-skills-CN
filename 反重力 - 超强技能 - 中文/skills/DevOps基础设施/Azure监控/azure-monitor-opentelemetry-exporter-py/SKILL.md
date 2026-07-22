---
name: azure-monitor-opentelemetry-exporter-py
description: Python 版 Azure Monitor OpenTelemetry Exporter。用于向 Application Insights 进行底层 OpenTelemetry 导出。当用户要求'配置 Azure Monitor OpenTelemetry 导出器'、'向 Application Insights 发送 OpenTelemetry 遥测数据'、'Python OpenTelemetry Azure 集成'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor OpenTelemetry Exporter for Python

用于向 Application Insights 发送 OpenTelemetry traces、metrics 和 logs 的底层导出器。

## 安装

```bash
pip install azure-monitor-opentelemetry-exporter
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## 何时使用
| 场景 | 使用 |
|------|------|
| 快速设置，自动插桩 | `azure-monitor-opentelemetry` (distro) |
| 自定义 OpenTelemetry 管道 | `azure-monitor-opentelemetry-exporter`（本包） |
| 对遥测数据进行细粒度控制 | `azure-monitor-opentelemetry-exporter`（本包） |

## Trace 导出器

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Create exporter
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure tracer provider
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporter)
)

# Use tracer
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-span"):
    print("Hello, World!")
```

## Metric 导出器

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

# Create exporter
exporter = AzureMonitorMetricExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure meter provider
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))

# Use meter
meter = metrics.get_meter(__name__)
counter = meter.create_counter("requests_total")
counter.add(1, {"route": "/api/users"})
```

## Log 导出器

```python
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

# Create exporter
exporter = AzureMonitorLogExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure logger provider
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
set_logger_provider(logger_provider)

# Add handler to Python logging
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Use logging
logger = logging.getLogger(__name__)
logger.info("This will be sent to Application Insights")
```

## 从环境变量读取

导出器会自动读取 `APPLICATIONINSIGHTS_CONNECTION_STRING`：

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Connection string from environment
exporter = AzureMonitorTraceExporter()
```

## Azure AD 认证

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    credential=DefaultAzureCredential()
)
```

## 采样

使用 `ApplicationInsightsSampler` 进行一致性采样：

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from azure.monitor.opentelemetry.exporter import ApplicationInsightsSampler

# Sample 10% of traces
sampler = ApplicationInsightsSampler(sampling_ratio=0.1)

trace.set_tracer_provider(TracerProvider(sampler=sampler))
```

## 离线存储

配置离线存储以支持重试：

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    connection_string="...",
    storage_directory="/path/to/storage",  # Custom storage path
    disable_offline_storage=False  # Enable retry (default)
)
```

## 禁用离线存储

```python
exporter = AzureMonitorTraceExporter(
    connection_string="...",
    disable_offline_storage=True  # No retry on failure
)
```

## 主权云

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.us/",
    credential=credential
)
```

## 导出器类型

| 导出器 | 遥测类型 | Application Insights 表 |
|--------|----------|------------------------|
| `AzureMonitorTraceExporter` | Traces/Spans | requests, dependencies, exceptions |
| `AzureMonitorMetricExporter` | Metrics | customMetrics, performanceCounters |
| `AzureMonitorLogExporter` | Logs | traces, customEvents |

## 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `connection_string` | Application Insights 连接字符串 | 从环境变量读取 |
| `credential` | 用于 AAD 认证的 Azure 凭据 | None |
| `disable_offline_storage` | 禁用重试存储 | False |
| `storage_directory` | 自定义存储路径 | 临时目录 |

## 最佳实践

1. **生产环境使用 BatchSpanProcessor**（而非 SimpleSpanProcessor）
2. **使用 ApplicationInsightsSampler** 在跨服务间保持一致的采样
3. **生产环境启用离线存储** 以提高可靠性
4. **使用 AAD 认证** 而非 instrumentation key
5. **设置适合工作负载的导出间隔**
6. **除非需要自定义管道，否则使用 distro**（`azure-monitor-opentelemetry`）

## 限制
- 仅当任务明确符合上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
