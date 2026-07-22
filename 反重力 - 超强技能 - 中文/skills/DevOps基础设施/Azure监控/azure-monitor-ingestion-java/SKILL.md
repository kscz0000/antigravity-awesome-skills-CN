---
name: azure-monitor-ingestion-java
description: Azure Monitor Ingestion SDK for Java，通过 Data Collection Rules (DCR) 和 Data Collection Endpoints (DCE) 向 Azure Monitor 发送自定义日志。当用户要求'使用Java向Azure Monitor发送自定义日志'、'Azure Monitor日志采集Java SDK'、'Logs Ingestion API Java'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Monitor Ingestion SDK for Java

用于通过 Logs Ingestion API 经由 Data Collection Rules 向 Azure Monitor 发送自定义日志的客户端库。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-ingestion</artifactId>
    <version>1.2.11</version>
</dependency>
```

或使用 Azure SDK BOM：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-sdk-bom</artifactId>
            <version>{bom_version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-monitor-ingestion</artifactId>
    </dependency>
</dependencies>
```

## 前提条件

- Data Collection Endpoint (DCE)
- Data Collection Rule (DCR)
- Log Analytics 工作区
- 目标表（自定义或内置：CommonSecurityLog、SecurityEvents、Syslog、WindowsEvents）

## 环境变量

```bash
DATA_COLLECTION_ENDPOINT=https://<dce-name>.<region>.ingest.monitor.azure.com
DATA_COLLECTION_RULE_ID=dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STREAM_NAME=Custom-MyTable_CL
```

## 客户端创建

### 同步客户端

```java
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.monitor.ingestion.LogsIngestionClient;
import com.azure.monitor.ingestion.LogsIngestionClientBuilder;

DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

LogsIngestionClient client = new LogsIngestionClientBuilder()
    .endpoint("<data-collection-endpoint>")
    .credential(credential)
    .buildClient();
```

### 异步客户端

```java
import com.azure.monitor.ingestion.LogsIngestionAsyncClient;

LogsIngestionAsyncClient asyncClient = new LogsIngestionClientBuilder()
    .endpoint("<data-collection-endpoint>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

## 核心概念

| 概念 | 说明 |
|------|------|
| Data Collection Endpoint (DCE) | 区域的日志采集端点 URL |
| Data Collection Rule (DCR) | 定义数据转换和到表的路由规则 |
| Stream Name | DCR 中的目标流（例如 `Custom-MyTable_CL`） |
| Log Analytics Workspace | 已采集日志的目标工作区 |

## 核心操作

### 上传自定义日志

```java
import java.util.List;
import java.util.ArrayList;

List<Object> logs = new ArrayList<>();
logs.add(new MyLogEntry("2024-01-15T10:30:00Z", "INFO", "Application started"));
logs.add(new MyLogEntry("2024-01-15T10:30:05Z", "DEBUG", "Processing request"));

client.upload("<data-collection-rule-id>", "<stream-name>", logs);
System.out.println("Logs uploaded successfully");
```

### 并发上传

对于大量日志集合，启用并发上传：

```java
import com.azure.monitor.ingestion.models.LogsUploadOptions;
import com.azure.core.util.Context;

List<Object> logs = getLargeLogs(); // Large collection

LogsUploadOptions options = new LogsUploadOptions()
    .setMaxConcurrency(3);

client.upload("<data-collection-rule-id>", "<stream-name>", logs, options, Context.NONE);
```

### 带错误处理的上传

优雅地处理部分上传失败：

```java
LogsUploadOptions options = new LogsUploadOptions()
    .setLogsUploadErrorConsumer(uploadError -> {
        System.err.println("Upload error: " + uploadError.getResponseException().getMessage());
        System.err.println("Failed logs count: " + uploadError.getFailedLogs().size());
        
        // Option 1: Log and continue
        // Option 2: Throw to abort remaining uploads
        // throw uploadError.getResponseException();
    });

client.upload("<data-collection-rule-id>", "<stream-name>", logs, options, Context.NONE);
```

### 使用 Reactor 异步上传

```java
import reactor.core.publisher.Mono;

List<Object> logs = getLogs();

asyncClient.upload("<data-collection-rule-id>", "<stream-name>", logs)
    .doOnSuccess(v -> System.out.println("Upload completed"))
    .doOnError(e -> System.err.println("Upload failed: " + e.getMessage()))
    .subscribe();
```

## 日志条目模型示例

```java
public class MyLogEntry {
    private String timeGenerated;
    private String level;
    private String message;
    
    public MyLogEntry(String timeGenerated, String level, String message) {
        this.timeGenerated = timeGenerated;
        this.level = level;
        this.message = message;
    }
    
    // Getters required for JSON serialization
    public String getTimeGenerated() { return timeGenerated; }
    public String getLevel() { return level; }
    public String getMessage() { return message; }
}
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.upload(ruleId, streamName, logs);
} catch (HttpResponseException e) {
    System.err.println("HTTP Status: " + e.getResponse().getStatusCode());
    System.err.println("Error: " + e.getMessage());
    
    if (e.getResponse().getStatusCode() == 403) {
        System.err.println("Check DCR permissions and managed identity");
    } else if (e.getResponse().getStatusCode() == 404) {
        System.err.println("Verify DCE endpoint and DCR ID");
    }
}
```

## 最佳实践

1. **批量上传日志** — 分批上传而非逐条发送
2. **使用并发** — 为大批量上传设置 `maxConcurrency`
3. **处理部分失败** — 使用错误消费者记录失败条目
4. **匹配 DCR schema** — 日志条目字段必须匹配 DCR 转换预期
5. **包含 TimeGenerated** — 大多数表要求包含时间戳字段
6. **复用客户端** — 创建一次，在整个应用中复用
7. **高吞吐量使用异步** — 使用 `LogsIngestionAsyncClient` 实现响应式模式

## 查询已上传的日志

使用 azure-monitor-query 查询已采集的日志：

```java
// See azure-monitor-query skill for LogsQueryClient usage
String query = "MyTable_CL | where TimeGenerated > ago(1h) | limit 10";
```

## 参考链接

| 资源 | URL |
|------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-monitor-ingestion |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/monitor/azure-monitor-ingestion |
| 产品文档 | https://learn.microsoft.com/azure/azure-monitor/logs/logs-ingestion-api-overview |
| DCE 概述 | https://learn.microsoft.com/azure/azure-monitor/essentials/data-collection-endpoint-overview |
| DCR 概述 | https://learn.microsoft.com/azure/azure-monitor/essentials/data-collection-rule-overview |
| 故障排除 | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-ingestion/TROUBLESHOOTING.md |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
