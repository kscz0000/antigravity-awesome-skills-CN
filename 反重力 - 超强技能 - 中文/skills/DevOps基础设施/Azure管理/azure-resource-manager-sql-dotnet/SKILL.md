---
name: azure-resource-manager-sql-dotnet
description: .NET 中的 Azure SQL Azure Resource Manager SDK。当用户要求"管理 Azure SQL 资源、创建 SQL Server/数据库/弹性池、配置防火墙规则、管理故障转移组"时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.Sql (.NET)

通过 Azure Resource Manager 预配和管理 Azure SQL 资源的管理平面 SDK。

> **⚠️ 管理平面 vs 数据平面**
> - **本 SDK (Azure.ResourceManager.Sql)**：创建服务器、数据库、弹性池，配置防火墙规则，管理故障转移组
> - **数据平面 SDK (Microsoft.Data.SqlClient)**：执行查询、存储过程，管理连接

## 安装

```bash
dotnet add package Azure.ResourceManager.Sql
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.3.0，预览版 v1.4.0-beta.3

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
using Azure.ResourceManager.Sql;

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
        └── SqlServerResource
            ├── SqlDatabaseResource
            ├── ElasticPoolResource
            │   └── ElasticPoolDatabaseResource
            ├── SqlFirewallRuleResource
            ├── FailoverGroupResource
            ├── ServerBlobAuditingPolicyResource
            ├── EncryptionProtectorResource
            └── VirtualNetworkRuleResource
```

## 核心工作流

### 1. 创建 SQL Server

```csharp
using Azure.ResourceManager.Sql;
using Azure.ResourceManager.Sql.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define server
var serverData = new SqlServerData(AzureLocation.EastUS)
{
    AdministratorLogin = "sqladmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = "12.0",
    MinimalTlsVersion = SqlMinimalTlsVersion.Tls1_2,
    PublicNetworkAccess = ServerNetworkAccessFlag.Enabled
};

// Create server (long-running operation)
var serverCollection = resourceGroup.Value.GetSqlServers();
var operation = await serverCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-sql-server",
    serverData);

SqlServerResource server = operation.Value;
```

### 2. 创建 SQL 数据库

```csharp
var databaseData = new SqlDatabaseData(AzureLocation.EastUS)
{
    Sku = new SqlSku("S0") { Tier = "Standard" },
    MaxSizeBytes = 2L * 1024 * 1024 * 1024, // 2 GB
    Collation = "SQL_Latin1_General_CP1_CI_AS",
    RequestedBackupStorageRedundancy = SqlBackupStorageRedundancy.Local
};

var databaseCollection = server.GetSqlDatabases();
var dbOperation = await databaseCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-database",
    databaseData);

SqlDatabaseResource database = dbOperation.Value;
```

### 3. 创建弹性池

```csharp
var poolData = new ElasticPoolData(AzureLocation.EastUS)
{
    Sku = new SqlSku("StandardPool")
    {
        Tier = "Standard",
        Capacity = 100 // 100 eDTUs
    },
    PerDatabaseSettings = new ElasticPoolPerDatabaseSettings
    {
        MinCapacity = 0,
        MaxCapacity = 100
    }
};

var poolCollection = server.GetElasticPools();
var poolOperation = await poolCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-elastic-pool",
    poolData);

ElasticPoolResource pool = poolOperation.Value;
```

### 4. 将数据库添加到弹性池

```csharp
var databaseData = new SqlDatabaseData(AzureLocation.EastUS)
{
    ElasticPoolId = pool.Id
};

await databaseCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "pooled-database",
    databaseData);
```

### 5. 配置防火墙规则

```csharp
// Allow Azure services
var azureServicesRule = new SqlFirewallRuleData
{
    StartIPAddress = "0.0.0.0",
    EndIPAddress = "0.0.0.0"
};

var firewallCollection = server.GetSqlFirewallRules();
await firewallCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "AllowAzureServices",
    azureServicesRule);

// Allow specific IP range
var clientRule = new SqlFirewallRuleData
{
    StartIPAddress = "203.0.113.0",
    EndIPAddress = "203.0.113.255"
};

await firewallCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "AllowClientIPs",
    clientRule);
```

### 6. 列出资源

```csharp
// List all servers in subscription
await foreach (var srv in subscription.GetSqlServersAsync())
{
    Console.WriteLine($"Server: {srv.Data.Name} in {srv.Data.Location}");
}

// List databases in a server
await foreach (var db in server.GetSqlDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}, SKU: {db.Data.Sku?.Name}");
}

// List elastic pools
await foreach (var ep in server.GetElasticPools())
{
    Console.WriteLine($"Pool: {ep.Data.Name}, DTU: {ep.Data.Sku?.Capacity}");
}
```

### 7. 获取连接字符串

```csharp
// Build connection string (server FQDN is predictable)
var serverFqdn = $"{server.Data.Name}.database.windows.net";
var connectionString = $"Server=tcp:{serverFqdn},1433;" +
    $"Initial Catalog={database.Data.Name};" +
    "Persist Security Info=False;" +
    $"User ID={server.Data.AdministratorLogin};" +
    "Password=<your-password>;" +
    "MultipleActiveResultSets=False;" +
    "Encrypt=True;" +
    "TrustServerCertificate=False;" +
    "Connection Timeout=30;";
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `SqlServerResource` | 表示 Azure SQL 服务器 |
| `SqlServerCollection` | 服务器 CRUD 集合 |
| `SqlDatabaseResource` | 表示 SQL 数据库 |
| `SqlDatabaseCollection` | 数据库 CRUD 集合 |
| `ElasticPoolResource` | 表示弹性池 |
| `ElasticPoolCollection` | 弹性池 CRUD 集合 |
| `SqlFirewallRuleResource` | 表示防火墙规则 |
| `SqlFirewallRuleCollection` | 防火墙规则 CRUD 集合 |
| `SqlServerData` | 服务器创建/更新负载 |
| `SqlDatabaseData` | 数据库创建/更新负载 |
| `ElasticPoolData` | 弹性池创建/更新负载 |
| `SqlFirewallRuleData` | 防火墙规则创建/更新负载 |
| `SqlSku` | SKU 配置（层级、容量） |

## 常用 SKU

### 数据库 SKU

| SKU 名称 | 层级 | 说明 |
|----------|------|------|
| `Basic` | Basic | 5 DTU，最大 2 GB |
| `S0`-`S12` | Standard | 10-3000 DTU |
| `P1`-`P15` | Premium | 125-4000 DTU |
| `GP_Gen5_2` | GeneralPurpose | 基于 vCore，2 个 vCore |
| `BC_Gen5_2` | BusinessCritical | 基于 vCore，2 个 vCore |
| `HS_Gen5_2` | Hyperscale | 基于 vCore，2 个 vCore |

### 弹性池 SKU

| SKU 名称 | 层级 | 说明 |
|----------|------|------|
| `BasicPool` | Basic | 50-1600 eDTU |
| `StandardPool` | Standard | 50-3000 eDTU |
| `PremiumPool` | Premium | 125-4000 eDTU |
| `GP_Gen5_2` | GeneralPurpose | 基于 vCore |
| `BC_Gen5_2` | BusinessCritical | 基于 vCore |

## 最佳实践

1. **使用 `WaitUntil.Completed`** 处理必须在继续前完成的操作
2. **使用 `WaitUntil.Started`** 当你想手动轮询或并行运行操作时
3. **始终使用 `DefaultAzureCredential`** — 生产环境中绝不硬编码密码
4. **处理 `RequestFailedException`** 以应对 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 实现幂等操作
6. **通过 `Get*` 方法导航层级**（如 `server.GetSqlDatabases()`）
7. **使用弹性池** 在管理多个数据库时优化成本
8. **在尝试连接前配置防火墙规则**

## 错误处理

```csharp
using Azure;

try
{
    var operation = await serverCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, serverName, serverData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Server already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 参考文件

| 文件 | 何时阅读 |
|------|----------|
| references/server-management.md | 服务器 CRUD、管理员凭据、Azure AD 身份验证、网络 |
| references/database-operations.md | 数据库 CRUD、缩放、备份、还原、复制 |
| references/elastic-pools.md | 池管理、添加/移除数据库、缩放 |

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Microsoft.Data.SqlClient` | 数据平面（执行查询、存储过程） | `dotnet add package Microsoft.Data.SqlClient` |
| `Azure.ResourceManager.Sql` | 管理平面（本 SDK） | `dotnet add package Azure.ResourceManager.Sql` |
| `Microsoft.EntityFrameworkCore.SqlServer` | SQL Server 的 ORM | `dotnet add package Microsoft.EntityFrameworkCore.SqlServer` |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
