---
name: azure-cosmos-java
description: Azure Cosmos DB Java SDK。支持全球分布、多模型和响应式模式的 NoSQL 数据库操作。触发词：Cosmos DB Java、Azure Cosmos、NoSQL Java、CosmosClient、CosmosAsyncClient、分区键、一致性级别、请求单元 RU、Azure 数据库 Java
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Cosmos DB SDK for Java

Azure Cosmos DB NoSQL API 的客户端库，支持全球分布和响应式模式。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-cosmos</artifactId>
    <version>LATEST</version>
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
        <artifactId>azure-cosmos</artifactId>
    </dependency>
</dependencies>
```

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_KEY=<your-primary-key>
```

## 身份认证

### 基于密钥的认证

```java
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;

CosmosClient client = new CosmosClientBuilder()
    .endpoint(System.getenv("COSMOS_ENDPOINT"))
    .key(System.getenv("COSMOS_KEY"))
    .buildClient();
```

### 异步客户端

```java
import com.azure.cosmos.CosmosAsyncClient;

CosmosAsyncClient asyncClient = new CosmosClientBuilder()
    .endpoint(serviceEndpoint)
    .key(key)
    .buildAsyncClient();
```

### 自定义配置

```java
import com.azure.cosmos.ConsistencyLevel;
import java.util.Arrays;

CosmosClient client = new CosmosClientBuilder()
    .endpoint(serviceEndpoint)
    .key(key)
    .directMode(directConnectionConfig, gatewayConnectionConfig)
    .consistencyLevel(ConsistencyLevel.SESSION)
    .connectionSharingAcrossClientsEnabled(true)
    .contentResponseOnWriteEnabled(true)
    .userAgentSuffix("my-application")
    .preferredRegions(Arrays.asList("West US", "East US"))
    .buildClient();
```

## 客户端层级

| 类 | 用途 |
|-------|---------|
| `CosmosClient` / `CosmosAsyncClient` | 账户级操作 |
| `CosmosDatabase` / `CosmosAsyncDatabase` | 数据库操作 |
| `CosmosContainer` / `CosmosAsyncContainer` | 容器/文档操作 |

## 核心工作流

### 创建数据库

```java
// 同步
client.createDatabaseIfNotExists("myDatabase")
    .map(response -> client.getDatabase(response.getProperties().getId()));

// 异步链式调用
asyncClient.createDatabaseIfNotExists("myDatabase")
    .map(response -> asyncClient.getDatabase(response.getProperties().getId()))
    .subscribe(database -> System.out.println("Created: " + database.getId()));
```

### 创建容器

```java
asyncClient.createDatabaseIfNotExists("myDatabase")
    .flatMap(dbResponse -> {
        String databaseId = dbResponse.getProperties().getId();
        return asyncClient.getDatabase(databaseId)
            .createContainerIfNotExists("myContainer", "/partitionKey")
            .map(containerResponse -> asyncClient.getDatabase(databaseId)
                .getContainer(containerResponse.getProperties().getId()));
    })
    .subscribe(container -> System.out.println("Container: " + container.getId()));
```

### CRUD 操作

```java
import com.azure.cosmos.models.PartitionKey;

CosmosAsyncContainer container = asyncClient
    .getDatabase("myDatabase")
    .getContainer("myContainer");

// 创建
container.createItem(new User("1", "John Doe", "john@example.com"))
    .flatMap(response -> {
        System.out.println("Created: " + response.getItem());
        // 读取
        return container.readItem(
            response.getItem().getId(),
            new PartitionKey(response.getItem().getId()),
            User.class);
    })
    .flatMap(response -> {
        System.out.println("Read: " + response.getItem());
        // 更新
        User user = response.getItem();
        user.setEmail("john.doe@example.com");
        return container.replaceItem(
            user,
            user.getId(),
            new PartitionKey(user.getId()));
    })
    .flatMap(response -> {
        // 删除
        return container.deleteItem(
            response.getItem().getId(),
            new PartitionKey(response.getItem().getId()));
    })
    .block();
```

### 查询文档

```java
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.util.CosmosPagedIterable;

CosmosContainer container = client.getDatabase("myDatabase").getContainer("myContainer");

String query = "SELECT * FROM c WHERE c.status = @status";
CosmosQueryRequestOptions options = new CosmosQueryRequestOptions();

CosmosPagedIterable<User> results = container.queryItems(
    query,
    options,
    User.class
);

results.forEach(user -> System.out.println("User: " + user.getName()));
```

## 核心概念

### 分区键

选择分区键时应考虑：
- 高基数性（大量不同的值）
- 数据和请求的均匀分布
- 在查询中频繁使用

### 一致性级别

| 级别 | 保证 |
|-------|-----------|
| Strong | 线性一致性 |
| Bounded Staleness | 一致性前缀，有界延迟 |
| Session | 会话内一致性前缀 |
| Consistent Prefix | 读取不会看到乱序写入 |
| Eventual | 无顺序保证 |

### 请求单元 (RU)

所有操作都会消耗 RU。检查响应头：

```java
CosmosItemResponse<User> response = container.createItem(user);
System.out.println("RU charge: " + response.getRequestCharge());
```

## 最佳实践

1. **复用 CosmosClient** — 创建一次，在整个应用程序中复用
2. **使用异步客户端** 处理高吞吐量场景
3. **谨慎选择分区键** — 影响性能和可扩展性
4. **启用写入内容响应** 以便立即访问创建的文档
5. **配置首选区域** 用于地理分布式应用程序
6. **处理 429 错误** 使用重试策略（默认内置）
7. **使用直连模式** 在生产环境中获得最低延迟

## 错误处理

```java
import com.azure.cosmos.CosmosException;

try {
    container.createItem(item);
} catch (CosmosException e) {
    System.err.println("Status: " + e.getStatusCode());
    System.err.println("Message: " + e.getMessage());
    System.err.println("Request charge: " + e.getRequestCharge());
    
    if (e.getStatusCode() == 409) {
        System.err.println("Item already exists");
    } else if (e.getStatusCode() == 429) {
        System.err.println("Rate limited, retry after: " + e.getRetryAfterDuration());
    }
}
```

## 参考链接

| 资源 | URL |
|----------|-----|
| Maven 包 | https://central.sonatype.com/artifact/com.azure/azure-cosmos |
| API 文档 | https://azuresdkdocs.z19.web.core.windows.net/java/azure-cosmos/latest/index.html |
| 产品文档 | https://learn.microsoft.com/azure/cosmos-db/ |
| 示例代码 | https://github.com/Azure-Samples/azure-cosmos-java-sql-api-samples |
| 性能指南 | https://learn.microsoft.com/azure/cosmos-db/performance-tips-java-sdk-v4-sql |
| 故障排查 | https://learn.microsoft.com/azure/cosmos-db/troubleshoot-java-sdk-v4-sql |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
