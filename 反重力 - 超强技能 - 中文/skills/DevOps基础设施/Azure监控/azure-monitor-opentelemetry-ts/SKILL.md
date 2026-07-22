---
name: azure-monitor-opentelemetry-ts
description: "自动为 Node.js 应用注入分布式追踪、指标和日志。当用户要求'Azure Monitor OpenTelemetry 集成'、'Node.js 分布式追踪'、'应用性能监控'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Monitor OpenTelemetry SDK for TypeScript

自动为 Node.js 应用注入分布式追踪、指标和日志。

## 安装

```bash
# Distro（推荐 - 自动插桩）
npm install @azure/monitor-opentelemetry

# 底层导出器（自定义 OpenTelemetry 配置）
npm install @azure/monitor-opentelemetry-exporter

# 自定义日志摄取
npm install @azure/monitor-ingestion
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

## 快速开始（自动插桩）

**重要：** 在导入其他模块之前调用 `useAzureMonitor()`。

```typescript
import { useAzureMonitor } from "@azure/monitor-opentelemetry";

useAzureMonitor({
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
  }
});

// 然后导入你的应用
import express from "express";
const app = express();
```

## ESM 支持（Node.js 18.19+）

```bash
node --import @azure/monitor-opentelemetry/loader ./dist/index.js
```

**package.json：**
```json
{
  "scripts": {
    "start": "node --import @azure/monitor-opentelemetry/loader ./dist/index.js"
  }
}
```

## 完整配置

```typescript
import { useAzureMonitor, AzureMonitorOpenTelemetryOptions } from "@azure/monitor-opentelemetry";
import { resourceFromAttributes } from "@opentelemetry/resources";

const options: AzureMonitorOpenTelemetryOptions = {
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
    storageDirectory: "/path/to/offline/storage",
    disableOfflineStorage: false
  },
  
  // 采样
  samplingRatio: 1.0,  // 0-1，追踪的百分比
  
  // 功能开关
  enableLiveMetrics: true,
  enableStandardMetrics: true,
  enablePerformanceCounters: true,
  
  // 插桩库
  instrumentationOptions: {
    azureSdk: { enabled: true },
    http: { enabled: true },
    mongoDb: { enabled: true },
    mySql: { enabled: true },
    postgreSql: { enabled: true },
    redis: { enabled: true },
    bunyan: { enabled: false },
    winston: { enabled: false }
  },
  
  // 自定义资源
  resource: resourceFromAttributes({ "service.name": "my-service" })
};

useAzureMonitor(options);
```

## 自定义追踪

```typescript
import { trace } from "@opentelemetry/api";

const tracer = trace.getTracer("my-tracer");

const span = tracer.startSpan("doWork");
try {
  span.setAttribute("component", "worker");
  span.setAttribute("operation.id", "42");
  span.addEvent("processing started");
  
  // 你的业务逻辑
  
} catch (error) {
  span.recordException(error as Error);
  span.setStatus({ code: 2, message: (error as Error).message });
} finally {
  span.end();
}
```

## 自定义指标

```typescript
import { metrics } from "@opentelemetry/api";

const meter = metrics.getMeter("my-meter");

// Counter（计数器）
const counter = meter.createCounter("requests_total");
counter.add(1, { route: "/api/users", method: "GET" });

// Histogram（直方图）
const histogram = meter.createHistogram("request_duration_ms");
histogram.record(150, { route: "/api/users" });

// Observable Gauge（可观测仪表）
const gauge = meter.createObservableGauge("active_connections");
gauge.addCallback((result) => {
  result.observe(getActiveConnections(), { pool: "main" });
});
```

## 手动导出器配置

### Trace 导出器

```typescript
import { AzureMonitorTraceExporter } from "@azure/monitor-opentelemetry-exporter";
import { NodeTracerProvider, BatchSpanProcessor } from "@opentelemetry/sdk-trace-node";

const exporter = new AzureMonitorTraceExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const provider = new NodeTracerProvider({
  spanProcessors: [new BatchSpanProcessor(exporter)]
});

provider.register();
```

### Metric 导出器

```typescript
import { AzureMonitorMetricExporter } from "@azure/monitor-opentelemetry-exporter";
import { PeriodicExportingMetricReader, MeterProvider } from "@opentelemetry/sdk-metrics";
import { metrics } from "@opentelemetry/api";

const exporter = new AzureMonitorMetricExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const meterProvider = new MeterProvider({
  readers: [new PeriodicExportingMetricReader({ exporter })]
});

metrics.setGlobalMeterProvider(meterProvider);
```

### Log 导出器

```typescript
import { AzureMonitorLogExporter } from "@azure/monitor-opentelemetry-exporter";
import { BatchLogRecordProcessor, LoggerProvider } from "@opentelemetry/sdk-logs";
import { logs } from "@opentelemetry/api-logs";

const exporter = new AzureMonitorLogExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const loggerProvider = new LoggerProvider();
loggerProvider.addLogRecordProcessor(new BatchLogRecordProcessor(exporter));

logs.setGlobalLoggerProvider(loggerProvider);
```

## 自定义日志摄取

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { LogsIngestionClient, isAggregateLogsUploadError } from "@azure/monitor-ingestion";

const endpoint = "https://<dce>.ingest.monitor.azure.com";
const ruleId = "<data-collection-rule-id>";
const streamName = "Custom-MyTable_CL";

const client = new LogsIngestionClient(endpoint, new DefaultAzureCredential());

const logs = [
  {
    Time: new Date().toISOString(),
    Computer: "Server1",
    Message: "Application started",
    Level: "Information"
  }
];

try {
  await client.upload(ruleId, streamName, logs);
} catch (error) {
  if (isAggregateLogsUploadError(error)) {
    for (const uploadError of error.errors) {
      console.error("Failed logs:", uploadError.failedLogs);
    }
  }
}
```

## 自定义 Span Processor

```typescript
import { SpanProcessor, ReadableSpan } from "@opentelemetry/sdk-trace-base";
import { Span, Context, SpanKind, TraceFlags } from "@opentelemetry/api";
import { useAzureMonitor } from "@azure/monitor-opentelemetry";

class FilteringSpanProcessor implements SpanProcessor {
  forceFlush(): Promise<void> { return Promise.resolve(); }
  shutdown(): Promise<void> { return Promise.resolve(); }
  onStart(span: Span, context: Context): void {}
  
  onEnd(span: ReadableSpan): void {
    // 添加自定义属性
    span.attributes["CustomDimension"] = "value";
    
    // 过滤掉内部 span
    if (span.kind === SpanKind.INTERNAL) {
      span.spanContext().traceFlags = TraceFlags.NONE;
    }
  }
}

useAzureMonitor({
  spanProcessors: [new FilteringSpanProcessor()]
});
```

## 采样

```typescript
import { ApplicationInsightsSampler } from "@azure/monitor-opentelemetry-exporter";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";

// 采样 75% 的追踪
const sampler = new ApplicationInsightsSampler(0.75);

const provider = new NodeTracerProvider({ sampler });
```

## 关闭

```typescript
import { useAzureMonitor, shutdownAzureMonitor } from "@azure/monitor-opentelemetry";

useAzureMonitor();

// 应用关闭时
process.on("SIGTERM", async () => {
  await shutdownAzureMonitor();
  process.exit(0);
});
```

## 核心类型

```typescript
import {
  useAzureMonitor,
  shutdownAzureMonitor,
  AzureMonitorOpenTelemetryOptions,
  InstrumentationOptions
} from "@azure/monitor-opentelemetry";

import {
  AzureMonitorTraceExporter,
  AzureMonitorMetricExporter,
  AzureMonitorLogExporter,
  ApplicationInsightsSampler,
  AzureMonitorExporterOptions
} from "@azure/monitor-opentelemetry-exporter";

import {
  LogsIngestionClient,
  isAggregateLogsUploadError
} from "@azure/monitor-ingestion";
```

## 最佳实践

1. **首先调用 useAzureMonitor()** - 在导入其他模块之前
2. **ESM 项目使用 ESM loader** - `--import @azure/monitor-opentelemetry/loader`
3. **启用离线存储** - 确保断连场景下的遥测可靠性
4. **设置采样比例** - 适用于高流量应用
5. **添加自定义维度** - 使用 span processor 进行数据丰富
6. **优雅关闭** - 调用 `shutdownAzureMonitor()` 刷新遥测数据

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
