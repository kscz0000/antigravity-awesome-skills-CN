---
name: azure-resource-manager-cosmosdb-dotnet
description: .NET 中的 Azure Resource Manager Cosmos DB SDK。当用户要求"管理 Azure Cosmos DB 资源、创建账户/数据库/容器、配置吞吐量、管理 RBAC"时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.CosmosDB (.NET)

管理平面 SDK，用于通过 Azure Resource Manager 预配和管理 Azure Cosmos DB 资源。

> **⚠️ 管理平面 vs 数据平面**
> - **本 SDK (Azure.ResourceManager.CosmosDB)**：创建账户、数据库、容器，配置吞吐量，管理 RBAC
> - **数据平面 SDK (Microsoft.Azure.Cosmos)**：对文档执行 CRUD 操作、查询、存储过程执行

## 安装

```bash
dotnet add package Azure.ResourceManager.CosmosDB
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.4.0，预览版 v1.4.0-beta.13

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.CosmosDB;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
```

## 资源层级

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── CosmosDBAccountResource
            ├── CosmosDBSqlDatabaseResource
            │   └── CosmosDBSqlContainerResource
            │       ├── CosmosDBSqlStoredProcedureResource
            │       ├── CosmosDBSqlTriggerResource
            │       └── CosmosDBSqlUserDefinedFunctionResource
            ├── CassandraKeyspaceResource
            ├── GremlinDatabaseResource
            ├── MongoDBDatabaseResource
            └── CosmosDBTableResource
```

## 核心工作流

### 1. 创建 Cosmos DB 账户

```csharp
using Azure.ResourceManager.CosmosDB;
using Azure.ResourceManager.CosmosDB.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define account
var accountData = new CosmosDBAccountCreateOrUpdateContent(
    location: AzureLocation.EastUS,
    locations: new[]
    {
        new CosmosDBAccountLocation
        {
            LocationName = AzureLocation.EastUS,
            FailoverPriority = 0,
            IsZoneRedundant = false
        }
    })
{
    Kind = CosmosDBAccountKind.GlobalDocumentDB,
    ConsistencyPolicy = new ConsistencyPolicy(DefaultConsistencyLevel.Session),
    EnableAutomaticFailover = true
};

// Create account (long-running operation)
var accountCollection = resourceGroup.Value.GetCosmosDBAccounts();
var operation = await accountCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-cosmos-account",
    accountData);

CosmosDBAccountResource account = operation.Value;
```

### 2. 创建 SQL 数据库

```csharp
var databaseData = new CosmosDBSqlDatabaseCreateOrUpdateContent(
    new CosmosDBSqlDatabaseResourceInfo("my-database"));

var databaseCollection = account.GetCosmosDBSqlDatabases();
var dbOperation = await databaseCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-database",
    databaseData);

CosmosDBSqlDatabaseResource database = dbOperation.Value;
```

### 3. 创建 SQL 容器

```csharp
var containerData = new CosmosDBSqlContainerCreateOrUpdateContent(
    new CosmosDBSqlContainerResourceInfo("my-container")
    {
        PartitionKey = new CosmosDBContainerPartitionKey
        {
            Paths = { "/partitionKey" },
            Kind = CosmosDBPartitionKind.Hash
        },
        IndexingPolicy = new CosmosDBIndexingPolicy
        {
            Automatic = true,
            IndexingMode = CosmosDBIndexingMode.Consistent
        },
        DefaultTtl = 86400 // 24 hours
    });

var containerCollection = database.GetCosmosDBSqlContainers();
var containerOperation = await containerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-container",
    containerData);

CosmosDBSqlContainerResource container = containerOperation.Value;
```

### 4. 配置吞吐量

```csharp
// Manual throughput
var throughputData = new ThroughputSettingsUpdateData(
    new ThroughputSettingsResourceInfo
    {
        Throughput = 400
    });

// Autoscale throughput
var autoscaleData = new ThroughputSettingsUpdateData(
    new ThroughputSettingsResourceInfo
    {
        AutoscaleSettings = new AutoscaleSettingsResourceInfo
        {
            MaxThroughput = 4000
        }
    });

// Apply to database
await database.CreateOrUpdateCosmosDBSqlDatabaseThroughputAsync(
    WaitUntil.Completed,
    throughputData);
```

### 5. 获取连接信息

```csharp
// Get keys
var keys = await account.GetKeysAsync();
Console.WriteLine($"Primary Key: {keys.Value.PrimaryMasterKey}");

// Get connection strings
var connectionStrings = await account.GetConnectionStringsAsync();
foreach (var cs in connectionStrings.Value.ConnectionStrings)
{
    Console.WriteLine($"{cs.Description}: {cs.ConnectionString}");
}
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `CosmosDBAccountResource` | 表示 Cosmos DB 账户 |
| `CosmosDBAccountCollection` | 账户 CRUD 集合 |
| `CosmosDBSqlDatabaseResource` | SQL API 数据库 |
| `CosmosDBSqlContainerResource` | SQL API 容器 |
| `CosmosDBAccountCreateOrUpdateContent` | 账户创建载荷 |
| `CosmosDBSqlDatabaseCreateOrUpdateContent` | 数据库创建载荷 |
| `CosmosDBSqlContainerCreateOrUpdateContent` | 容器创建载荷 |
| `ThroughputSettingsUpdateData` | 吞吐量配置 |

## 最佳实践

1. **使用 `WaitUntil.Completed`** 处理必须在继续前完成的操作
2. **使用 `WaitUntil.Started`** 当你想手动轮询或并行运行操作时
3. **始终使用 `DefaultAzureCredential`** — 永远不要硬编码密钥
4. **处理 `RequestFailedException`** 以应对 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 实现幂等操作
6. **通过 `Get*` 方法导航层级**（例如 `account.GetCosmosDBSqlDatabases()`）

## 错误处理

```csharp
using Azure;

try
{
    var operation = await accountCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, accountName, accountData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Account already exists");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 参考文件

| 文件 | 何时阅读 |
|------|----------|
| references/account-management.md | 账户 CRUD、故障转移、密钥、连接字符串、网络 |
| references/sql-resources.md | SQL 数据库、容器、存储过程、触发器、UDF |
| references/throughput.md | 手动/自动缩放吞吐量、模式间迁移 |

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Microsoft.Azure.Cosmos` | 数据平面（文档 CRUD、查询） | `dotnet add package Microsoft.Azure.Cosmos` |
| `Azure.ResourceManager.CosmosDB` | 管理平面（本 SDK） | `dotnet add package Azure.ResourceManager.CosmosDB` |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
