---
name: azure-ai-projects-java
description: Azure AI Projects Java SDK。Azure AI Foundry 项目管理高级 SDK，涵盖连接、数据集、索引和评估。触发词：Azure AI Projects、Java SDK、AI Foundry、项目管理、连接管理、数据集管理、索引管理、模型评估
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Projects SDK for Java

Azure AI Foundry 项目管理高级 SDK，可访问连接、数据集、索引和评估功能。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-projects</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
```

## 认证

```java
import com.azure.ai.projects.AIProjectClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

AIProjectClientBuilder builder = new AIProjectClientBuilder()
    .endpoint(System.getenv("PROJECT_ENDPOINT"))
    .credential(new DefaultAzureCredentialBuilder().build());
```

## 客户端层级

SDK 为不同操作提供多个子客户端：

| 客户端 | 用途 |
|--------|------|
| `ConnectionsClient` | 枚举已连接的 Azure 资源 |
| `DatasetsClient` | 上传文档和管理数据集 |
| `DeploymentsClient` | 枚举 AI 模型部署 |
| `IndexesClient` | 创建和管理搜索索引 |
| `EvaluationsClient` | 运行 AI 模型评估 |
| `EvaluatorsClient` | 管理评估器配置 |
| `SchedulesClient` | 管理计划操作 |

```java
// 从 builder 构建子客户端
ConnectionsClient connectionsClient = builder.buildConnectionsClient();
DatasetsClient datasetsClient = builder.buildDatasetsClient();
DeploymentsClient deploymentsClient = builder.buildDeploymentsClient();
IndexesClient indexesClient = builder.buildIndexesClient();
EvaluationsClient evaluationsClient = builder.buildEvaluationsClient();
```

## 核心操作

### 列出连接

```java
import com.azure.ai.projects.models.Connection;
import com.azure.core.http.rest.PagedIterable;

PagedIterable<Connection> connections = connectionsClient.listConnections();
for (Connection connection : connections) {
    System.out.println("Name: " + connection.getName());
    System.out.println("Type: " + connection.getType());
    System.out.println("Credential Type: " + connection.getCredentials().getType());
}
```

### 列出索引

```java
indexesClient.listLatest().forEach(index -> {
    System.out.println("Index name: " + index.getName());
    System.out.println("Version: " + index.getVersion());
    System.out.println("Description: " + index.getDescription());
});
```

### 创建或更新索引

```java
import com.azure.ai.projects.models.AzureAISearchIndex;
import com.azure.ai.projects.models.Index;

String indexName = "my-index";
String indexVersion = "1.0";
String searchConnectionName = System.getenv("AI_SEARCH_CONNECTION_NAME");
String searchIndexName = System.getenv("AI_SEARCH_INDEX_NAME");

Index index = indexesClient.createOrUpdate(
    indexName,
    indexVersion,
    new AzureAISearchIndex()
        .setConnectionName(searchConnectionName)
        .setIndexName(searchIndexName)
);

System.out.println("Created index: " + index.getName());
```

### 访问 OpenAI 评估

SDK 暴露 OpenAI 官方 SDK 用于评估：

```java
import com.openai.services.EvalService;

EvalService evalService = evaluationsClient.getOpenAIClient();
// 直接使用 OpenAI 评估 API
```

## 最佳实践

1. **使用 DefaultAzureCredential** 进行生产环境认证
2. **复用客户端构建器** 高效创建多个子客户端
3. **处理分页** 使用 `PagedIterable` 列出资源时
4. **使用环境变量** 存储连接名称和配置
5. **检查连接类型** 在访问凭据之前

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    Index index = indexesClient.get(indexName, version);
} catch (ResourceNotFoundException e) {
    System.err.println("Index not found: " + indexName);
} catch (HttpResponseException e) {
    System.err.println("Error: " + e.getResponse().getStatusCode());
}
```

## 参考链接

| 资源 | URL |
|------|-----|
| 产品文档 | https://learn.microsoft.com/azure/ai-studio/ |
| API 参考 | https://learn.microsoft.com/rest/api/aifoundry/aiprojects/ |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-projects |
| 示例代码 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-projects/src/samples |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
