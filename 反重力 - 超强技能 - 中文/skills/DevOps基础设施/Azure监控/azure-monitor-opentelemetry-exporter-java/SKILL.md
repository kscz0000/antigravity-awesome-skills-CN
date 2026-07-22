---
name: azure-monitor-opentelemetry-exporter-java
description: Azure Monitor OpenTelemetry Java 导出器。将 OpenTelemetry 追踪、指标和日志导出到 Azure Monitor/Application Insights。当用户要求'Azure Monitor OpenTelemetry Java导出'、'Java遥测数据导出到Application Insights'、'OpenTelemetry Java Azure集成'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor OpenTelemetry Exporter for Java

> **⚠️ 弃用通知**：此包已弃用。请迁移到 `azure-monitor-opentelemetry-autoconfigure`。
>
> 详见 [迁移指南](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md)。

将 OpenTelemetry 遥测数据导出到 Azure Monitor / Application Insights。

## 安装（已弃用）

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-opentelemetry-exporter</artifactId>
    <version>1.0.0-beta.x</version>
</dependency>
```

## 推荐：改用 Autoconfigure

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-opentelemetry-autoconfigure</artifactId>
    <version>LATEST</version>
</dependency>
```

## 环境变量

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## 使用 Autoconfigure 的基本设置（推荐）

### 使用环境变量

```java
import io.opentelemetry.sdk.autoconfigure.AutoConfiguredOpenTelemetrySdk;
import io.opentelemetry.sdk.autoconfigure.AutoConfiguredOpenTelemetrySdkBuilder;
import io.opentelemetry.api.OpenTelemetry;
import com.azure.monitor.opentelemetry.exporter.AzureMonitorExporter;

// Connection string from APPLICATIONINSIGHTS_CONNECTION_STRING env var
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder);
OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

### 使用显式连接字符串

```java
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder, "{connection-string}");
OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

## 创建 Span

```java
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.context.Scope;

// Get tracer
Tracer tracer = openTelemetry.getTracer("com.example.myapp");

// Create span
Span span = tracer.spanBuilder("myOperation").startSpan();

try (Scope scope = span.makeCurrent()) {
    // Your application logic
    doWork();
} catch (Throwable t) {
    span.recordException(t);
    throw t;
} finally {
    span.end();
}
```

## 添加 Span 属性

```java
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;

Span span = tracer.spanBuilder("processOrder")
    .setAttribute("order.id", "12345")
    .setAttribute("customer.tier", "premium")
    .startSpan();

try (Scope scope = span.makeCurrent()) {
    // Add attributes during execution
    span.setAttribute("items.count", 3);
    span.setAttribute("total.amount", 99.99);
    
    processOrder();
} finally {
    span.end();
}
```

## 自定义 Span Processor

```java
import io.opentelemetry.sdk.trace.SpanProcessor;
import io.opentelemetry.sdk.trace.ReadWriteSpan;
import io.opentelemetry.sdk.trace.ReadableSpan;
import io.opentelemetry.context.Context;

private static final AttributeKey<String> CUSTOM_ATTR = AttributeKey.stringKey("custom.attribute");

SpanProcessor customProcessor = new SpanProcessor() {
    @Override
    public void onStart(Context context, ReadWriteSpan span) {
        // Add custom attribute to every span
        span.setAttribute(CUSTOM_ATTR, "customValue");
    }

    @Override
    public boolean isStartRequired() {
        return true;
    }

    @Override
    public void onEnd(ReadableSpan span) {
        // Post-processing if needed
    }

    @Override
    public boolean isEndRequired() {
        return false;
    }
};

// Register processor
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder);

sdkBuilder.addTracerProviderCustomizer(
    (sdkTracerProviderBuilder, configProperties) -> 
        sdkTracerProviderBuilder.addSpanProcessor(customProcessor)
);

OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

## 嵌套 Span

```java
public void parentOperation() {
    Span parentSpan = tracer.spanBuilder("parentOperation").startSpan();
    try (Scope scope = parentSpan.makeCurrent()) {
        childOperation();
    } finally {
        parentSpan.end();
    }
}

public void childOperation() {
    // Automatically links to parent via Context
    Span childSpan = tracer.spanBuilder("childOperation").startSpan();
    try (Scope scope = childSpan.makeCurrent()) {
        // Child work
    } finally {
        childSpan.end();
    }
}
```

## 记录异常

```java
Span span = tracer.spanBuilder("riskyOperation").startSpan();
try (Scope scope = span.makeCurrent()) {
    performRiskyWork();
} catch (Exception e) {
    span.recordException(e);
    span.setStatus(StatusCode.ERROR, e.getMessage());
    throw e;
} finally {
    span.end();
}
```

## 指标（通过 OpenTelemetry）

```java
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.metrics.LongHistogram;

Meter meter = openTelemetry.getMeter("com.example.myapp");

// Counter
LongCounter requestCounter = meter.counterBuilder("http.requests")
    .setDescription("Total HTTP requests")
    .setUnit("requests")
    .build();

requestCounter.add(1, Attributes.of(
    AttributeKey.stringKey("http.method"), "GET",
    AttributeKey.longKey("http.status_code"), 200L
));

// Histogram
LongHistogram latencyHistogram = meter.histogramBuilder("http.latency")
    .setDescription("Request latency")
    .setUnit("ms")
    .ofLongs()
    .build();

latencyHistogram.record(150, Attributes.of(
    AttributeKey.stringKey("http.route"), "/api/users"
));
```

## 核心概念

| 概念 | 说明 |
|------|------|
| Connection String | 包含 instrumentation key 的 Application Insights 连接字符串 |
| Tracer | 为分布式追踪创建 span |
| Span | 表示一个带有计时和属性的工作单元 |
| SpanProcessor | 拦截 span 生命周期以进行自定义 |
| Exporter | 将遥测数据发送到 Azure Monitor |

## 迁移到 Autoconfigure

`azure-monitor-opentelemetry-autoconfigure` 包提供：
- 常用库的自动插桩
- 简化的配置
- 与 OpenTelemetry SDK 更好的集成

### 迁移步骤

1. 替换依赖：
   ```xml
   <!-- Remove -->
   <dependency>
       <groupId>com.azure</groupId>
       <artifactId>azure-monitor-opentelemetry-exporter</artifactId>
   </dependency>
   
   <!-- Add -->
   <dependency>
       <groupId>com.azure</groupId>
       <artifactId>azure-monitor-opentelemetry-autoconfigure</artifactId>
   </dependency>
   ```

2. 按照 [迁移指南](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md) 更新初始化代码

## 最佳实践

1. **使用 autoconfigure** — 迁移到 `azure-monitor-opentelemetry-autoconfigure`
2. **设置有意义的 span 名称** — 使用描述性的操作名称
3. **添加相关属性** — 包含用于调试的上下文数据
4. **处理异常** — 始终在 span 上记录异常
5. **使用语义约定** — 遵循 OpenTelemetry 语义约定
6. **在 finally 中结束 span** — 确保 span 始终被结束
7. **使用 try-with-resources** — 通过 try-with-resources 模式管理 Scope

## 参考链接

| 资源 | URL |
|------|-----|
| Maven 包 | https://central.sonatype.com/artifact/com.azure/azure-monitor-opentelemetry-exporter |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/monitor/azure-monitor-opentelemetry-exporter |
| 迁移指南 | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md |
| Autoconfigure 包 | https://central.sonatype.com/artifact/com.azure/azure-monitor-opentelemetry-autoconfigure |
| OpenTelemetry Java | https://opentelemetry.io/docs/languages/java/ |
| Application Insights | https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
