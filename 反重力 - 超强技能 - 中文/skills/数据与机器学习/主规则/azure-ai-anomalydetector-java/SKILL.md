---
name: azure-ai-anomalydetector-java
description: "使用 Azure AI Anomaly Detector Java SDK 构建异常检测应用。触发词：异常检测Java、时间序列异常、多元异常检测、单变量异常检测、流式异常检测、变点检测、Azure AI Anomaly Detector、anomaly detection Java、detect anomalies time series、multivariate anomaly Java"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Anomaly Detector SDK for Java

使用 Azure AI Anomaly Detector Java SDK 构建异常检测应用。

## 安装

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-ai-anomalydetector</artifactId>
  <version>3.0.0-beta.6</version>
</dependency>
```

## 客户端创建

### 同步和异步客户端

```java
import com.azure.ai.anomalydetector.AnomalyDetectorClientBuilder;
import com.azure.ai.anomalydetector.MultivariateClient;
import com.azure.ai.anomalydetector.UnivariateClient;
import com.azure.core.credential.AzureKeyCredential;

String endpoint = System.getenv("AZURE_ANOMALY_DETECTOR_ENDPOINT");
String key = System.getenv("AZURE_ANOMALY_DETECTOR_API_KEY");

// 多元客户端，用于多个相关信号
MultivariateClient multivariateClient = new AnomalyDetectorClientBuilder()
    .credential(new AzureKeyCredential(key))
    .endpoint(endpoint)
    .buildMultivariateClient();

// 单变量客户端，用于单变量分析
UnivariateClient univariateClient = new AnomalyDetectorClientBuilder()
    .credential(new AzureKeyCredential(key))
    .endpoint(endpoint)
    .buildUnivariateClient();
```

### 使用 DefaultAzureCredential

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

MultivariateClient client = new AnomalyDetectorClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(endpoint)
    .buildMultivariateClient();
```

## 核心概念

### 单变量异常检测
- **批量检测**：一次性分析整个时间序列
- **流式检测**：对最新数据点进行实时检测
- **变点检测**：检测时间序列中的趋势变化

### 多元异常检测
- 检测 300+ 个相关信号中的异常
- 使用图注意力网络处理变量间相关性
- 三步流程：训练 → 推理 → 结果

## 核心模式

### 单变量批量检测

```java
import com.azure.ai.anomalydetector.models.*;
import java.time.OffsetDateTime;
import java.util.List;

List<TimeSeriesPoint> series = List.of(
    new TimeSeriesPoint(OffsetDateTime.parse("2023-01-01T00:00:00Z"), 1.0),
    new TimeSeriesPoint(OffsetDateTime.parse("2023-01-02T00:00:00Z"), 2.5),
    // ... 更多数据点（至少需要 12 个点）
);

UnivariateDetectionOptions options = new UnivariateDetectionOptions(series)
    .setGranularity(TimeGranularity.DAILY)
    .setSensitivity(95);

UnivariateEntireDetectionResult result = univariateClient.detectUnivariateEntireSeries(options);

// 检查异常
for (int i = 0; i < result.getIsAnomaly().size(); i++) {
    if (result.getIsAnomaly().get(i)) {
        System.out.printf("在索引 %d 检测到异常，值为 %.2f%n",
            i, series.get(i).getValue());
    }
}
```

### 单变量最后点检测（流式）

```java
UnivariateLastDetectionResult lastResult = univariateClient.detectUnivariateLastPoint(options);

if (lastResult.isAnomaly()) {
    System.out.println("最新点是异常！");
    System.out.printf("期望值: %.2f, 上限: %.2f, 下限: %.2f%n",
        lastResult.getExpectedValue(),
        lastResult.getUpperMargin(),
        lastResult.getLowerMargin());
}
```

### 变点检测

```java
UnivariateChangePointDetectionOptions changeOptions = 
    new UnivariateChangePointDetectionOptions(series, TimeGranularity.DAILY);

UnivariateChangePointDetectionResult changeResult = 
    univariateClient.detectUnivariateChangePoint(changeOptions);

for (int i = 0; i < changeResult.getIsChangePoint().size(); i++) {
    if (changeResult.getIsChangePoint().get(i)) {
        System.out.printf("索引 %d 处有变点，置信度 %.2f%n",
            i, changeResult.getConfidenceScores().get(i));
    }
}
```

### 多元模型训练

```java
import com.azure.ai.anomalydetector.models.*;
import com.azure.core.util.polling.SyncPoller;

// 使用 Blob 存储数据准备训练请求
ModelInfo modelInfo = new ModelInfo()
    .setDataSource("https://storage.blob.core.windows.net/container/data.zip?sasToken")
    .setStartTime(OffsetDateTime.parse("2023-01-01T00:00:00Z"))
    .setEndTime(OffsetDateTime.parse("2023-06-01T00:00:00Z"))
    .setSlidingWindow(200)
    .setDisplayName("MyMultivariateModel");

// 训练模型（长时间运行操作）
AnomalyDetectionModel trainedModel = multivariateClient.trainMultivariateModel(modelInfo);

String modelId = trainedModel.getModelId();
System.out.println("模型 ID: " + modelId);

// 检查训练状态
AnomalyDetectionModel model = multivariateClient.getMultivariateModel(modelId);
System.out.println("状态: " + model.getModelInfo().getStatus());
```

### 多元批量推理

```java
MultivariateBatchDetectionOptions detectionOptions = new MultivariateBatchDetectionOptions()
    .setDataSource("https://storage.blob.core.windows.net/container/inference-data.zip?sasToken")
    .setStartTime(OffsetDateTime.parse("2023-07-01T00:00:00Z"))
    .setEndTime(OffsetDateTime.parse("2023-07-31T00:00:00Z"))
    .setTopContributorCount(10);

MultivariateDetectionResult detectionResult = 
    multivariateClient.detectMultivariateBatchAnomaly(modelId, detectionOptions);

String resultId = detectionResult.getResultId();

// 轮询结果
MultivariateDetectionResult result = multivariateClient.getBatchDetectionResult(resultId);
for (AnomalyState state : result.getResults()) {
    if (state.getValue().isAnomaly()) {
        System.out.printf("在 %s 检测到异常，严重程度: %.2f%n",
            state.getTimestamp(),
            state.getValue().getSeverity());
    }
}
```

### 多元最后点检测

```java
MultivariateLastDetectionOptions lastOptions = new MultivariateLastDetectionOptions()
    .setVariables(List.of(
        new VariableValues("variable1", List.of("timestamp1"), List.of(1.0f)),
        new VariableValues("variable2", List.of("timestamp1"), List.of(2.5f))
    ))
    .setTopContributorCount(5);

MultivariateLastDetectionResult lastResult = 
    multivariateClient.detectMultivariateLastAnomaly(modelId, lastOptions);

if (lastResult.getValue().isAnomaly()) {
    System.out.println("检测到异常！");
    // 检查贡献变量
    for (AnomalyContributor contributor : lastResult.getValue().getInterpretation()) {
        System.out.printf("变量: %s, 贡献度: %.2f%n",
            contributor.getVariable(),
            contributor.getContributionScore());
    }
}
```

### 模型管理

```java
// 列出所有模型
PagedIterable<AnomalyDetectionModel> models = multivariateClient.listMultivariateModels();
for (AnomalyDetectionModel m : models) {
    System.out.printf("模型: %s, 状态: %s%n",
        m.getModelId(),
        m.getModelInfo().getStatus());
}

// 删除模型
multivariateClient.deleteMultivariateModel(modelId);
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    univariateClient.detectUnivariateEntireSeries(options);
} catch (HttpResponseException e) {
    System.out.println("状态码: " + e.getResponse().getStatusCode());
    System.out.println("错误: " + e.getMessage());
}
```

## 环境变量

```bash
AZURE_ANOMALY_DETECTOR_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
AZURE_ANOMALY_DETECTOR_API_KEY=<your-api-key>
```

## 最佳实践

1. **最小数据点**：单变量检测至少需要 12 个点；更多数据可提高准确性
2. **粒度对齐**：将 `TimeGranularity` 与实际数据频率匹配
3. **灵敏度调优**：较高值（0-99）可检测更多异常
4. **多元训练**：根据模式复杂度使用 200-1000 的滑动窗口
5. **错误处理**：始终处理 `HttpResponseException` 以应对 API 错误

## 触发词

- "异常检测 Java"
- "检测时间序列异常"
- "多元异常 Java"
- "单变量异常检测"
- "流式异常检测"
- "变点检测"
- "Azure AI Anomaly Detector"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
