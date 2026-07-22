---
name: azure-resource-manager-postgresql-dotnet
description: Azure PostgreSQL Flexible Server .NET SDK。用于 PostgreSQL Flexible Server 部署的数据库管理。当用户要求'管理 Azure PostgreSQL Flexible Server'、'创建 PostgreSQL 服务器'、'配置 PostgreSQL 防火墙规则'、'PostgreSQL 备份与还原'、'PostgreSQL 读副本'或'Azure PostgreSQL .NET SDK'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.PostgreSql (.NET)

Azure Resource Manager SDK，用于管理 PostgreSQL Flexible Server 部署。

## 安装

```bash
dotnet add package Azure.ResourceManager.PostgreSql
dotnet add package Azure.Identity
```

**当前版本**：v1.2.0 (GA)
**API 版本**：2023-12-01-preview

> **注意**：本技能聚焦于 PostgreSQL Flexible Server。Single Server 已弃用并计划停用。

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_POSTGRESQL_SERVER_NAME=<your-postgresql-server>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.PostgreSql;
using Azure.ResourceManager.PostgreSql.FlexibleServers;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## 资源层级

```
Subscription
└── ResourceGroup
    └── PostgreSqlFlexibleServer              # PostgreSQL Flexible Server 实例
        ├── PostgreSqlFlexibleServerDatabase  # 服务器内的数据库
        ├── PostgreSqlFlexibleServerFirewallRule # IP 防火墙规则
        ├── PostgreSqlFlexibleServerConfiguration # 服务器参数
        ├── PostgreSqlFlexibleServerBackup    # 备份信息
        ├── PostgreSqlFlexibleServerActiveDirectoryAdministrator # Entra ID 管理员
        └── PostgreSqlFlexibleServerVirtualEndpoint # 读副本端点
```

## 核心工作流

### 1. 创建 PostgreSQL Flexible Server

```csharp
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

PostgreSqlFlexibleServerCollection servers = resourceGroup.GetPostgreSqlFlexibleServers();

PostgreSqlFlexibleServerData data = new PostgreSqlFlexibleServerData(AzureLocation.EastUS)
{
    Sku = new PostgreSqlFlexibleServerSku("Standard_D2ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose),
    AdministratorLogin = "pgadmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = PostgreSqlFlexibleServerVersion.Ver16,
    Storage = new PostgreSqlFlexibleServerStorage
    {
        StorageSizeInGB = 128,
        AutoGrow = StorageAutoGrow.Enabled,
        Tier = PostgreSqlStorageTierName.P30
    },
    Backup = new PostgreSqlFlexibleServerBackupProperties
    {
        BackupRetentionDays = 7,
        GeoRedundantBackup = PostgreSqlFlexibleServerGeoRedundantBackupEnum.Disabled
    },
    HighAvailability = new PostgreSqlFlexibleServerHighAvailability
    {
        Mode = PostgreSqlFlexibleServerHighAvailabilityMode.ZoneRedundant,
        StandbyAvailabilityZone = "2"
    },
    AvailabilityZone = "1",
    AuthConfig = new PostgreSqlFlexibleServerAuthConfig
    {
        ActiveDirectoryAuth = PostgreSqlFlexibleServerActiveDirectoryAuthEnum.Enabled,
        PasswordAuth = PostgreSqlFlexibleServerPasswordAuthEnum.Enabled
    }
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-server", data);

PostgreSqlFlexibleServerResource server = operation.Value;
Console.WriteLine($"Server created: {server.Data.FullyQualifiedDomainName}");
```

### 2. 创建数据库

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

PostgreSqlFlexibleServerDatabaseCollection databases = server.GetPostgreSqlFlexibleServerDatabases();

PostgreSqlFlexibleServerDatabaseData dbData = new PostgreSqlFlexibleServerDatabaseData
{
    Charset = "UTF8",
    Collation = "en_US.utf8"
};

ArmOperation<PostgreSqlFlexibleServerDatabaseResource> operation = await databases
    .CreateOrUpdateAsync(WaitUntil.Completed, "myappdb", dbData);

PostgreSqlFlexibleServerDatabaseResource database = operation.Value;
Console.WriteLine($"Database created: {database.Data.Name}");
```

### 3. 配置防火墙规则

```csharp
PostgreSqlFlexibleServerFirewallRuleCollection firewallRules = server.GetPostgreSqlFlexibleServerFirewallRules();

// Allow specific IP range
PostgreSqlFlexibleServerFirewallRuleData ruleData = new PostgreSqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("10.0.0.1"),
    EndIPAddress = System.Net.IPAddress.Parse("10.0.0.255")
};

ArmOperation<PostgreSqlFlexibleServerFirewallRuleResource> operation = await firewallRules
    .CreateOrUpdateAsync(WaitUntil.Completed, "allow-internal", ruleData);

// Allow Azure services
PostgreSqlFlexibleServerFirewallRuleData azureServicesRule = new PostgreSqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("0.0.0.0"),
    EndIPAddress = System.Net.IPAddress.Parse("0.0.0.0")
};

await firewallRules.CreateOrUpdateAsync(WaitUntil.Completed, "AllowAllAzureServicesAndResourcesWithinAzureIps", azureServicesRule);
```

### 4. 更新服务器配置

```csharp
PostgreSqlFlexibleServerConfigurationCollection configurations = server.GetPostgreSqlFlexibleServerConfigurations();

// Get current configuration
PostgreSqlFlexibleServerConfigurationResource config = await configurations
    .GetAsync("max_connections");

// Update configuration
PostgreSqlFlexibleServerConfigurationData configData = new PostgreSqlFlexibleServerConfigurationData
{
    Value = "500",
    Source = "user-override"
};

ArmOperation<PostgreSqlFlexibleServerConfigurationResource> operation = await configurations
    .CreateOrUpdateAsync(WaitUntil.Completed, "max_connections", configData);

// Common PostgreSQL configurations to tune
string[] commonParams = { 
    "max_connections", 
    "shared_buffers", 
    "work_mem", 
    "maintenance_work_mem",
    "effective_cache_size",
    "log_min_duration_statement"
};
```

### 5. 配置 Entra ID 管理员

```csharp
PostgreSqlFlexibleServerActiveDirectoryAdministratorCollection admins = 
    server.GetPostgreSqlFlexibleServerActiveDirectoryAdministrators();

PostgreSqlFlexibleServerActiveDirectoryAdministratorData adminData = 
    new PostgreSqlFlexibleServerActiveDirectoryAdministratorData
{
    PrincipalType = PostgreSqlFlexibleServerPrincipalType.User,
    PrincipalName = "aad-admin@contoso.com",
    TenantId = Guid.Parse("<tenant-id>")
};

ArmOperation<PostgreSqlFlexibleServerActiveDirectoryAdministratorResource> operation = await admins
    .CreateOrUpdateAsync(WaitUntil.Completed, "<entra-object-id>", adminData);
```

### 6. 列出和管理服务器

```csharp
// List servers in resource group
await foreach (PostgreSqlFlexibleServerResource server in resourceGroup.GetPostgreSqlFlexibleServers())
{
    Console.WriteLine($"Server: {server.Data.Name}");
    Console.WriteLine($"  FQDN: {server.Data.FullyQualifiedDomainName}");
    Console.WriteLine($"  Version: {server.Data.Version}");
    Console.WriteLine($"  State: {server.Data.State}");
    Console.WriteLine($"  SKU: {server.Data.Sku.Name} ({server.Data.Sku.Tier})");
    Console.WriteLine($"  HA: {server.Data.HighAvailability?.Mode}");
}

// List databases in server
await foreach (PostgreSqlFlexibleServerDatabaseResource db in server.GetPostgreSqlFlexibleServerDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}");
}
```

### 7. 备份和时间点还原

```csharp
// List available backups
await foreach (PostgreSqlFlexibleServerBackupResource backup in server.GetPostgreSqlFlexibleServerBackups())
{
    Console.WriteLine($"Backup: {backup.Data.Name}");
    Console.WriteLine($"  Type: {backup.Data.BackupType}");
    Console.WriteLine($"  Completed: {backup.Data.CompletedOn}");
}

// Point-in-time restore
PostgreSqlFlexibleServerData restoreData = new PostgreSqlFlexibleServerData(AzureLocation.EastUS)
{
    CreateMode = PostgreSqlFlexibleServerCreateMode.PointInTimeRestore,
    SourceServerResourceId = server.Id,
    PointInTimeUtc = DateTimeOffset.UtcNow.AddHours(-2)
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-restored", restoreData);
```

### 8. 创建读副本

```csharp
PostgreSqlFlexibleServerData replicaData = new PostgreSqlFlexibleServerData(AzureLocation.WestUS)
{
    CreateMode = PostgreSqlFlexibleServerCreateMode.Replica,
    SourceServerResourceId = server.Id,
    Sku = new PostgreSqlFlexibleServerSku("Standard_D2ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose)
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-replica", replicaData);
```

### 9. 停止和启动服务器

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

// Stop server (saves costs when not in use)
await server.StopAsync(WaitUntil.Completed);

// Start server
await server.StartAsync(WaitUntil.Completed);

// Restart server
await server.RestartAsync(WaitUntil.Completed, new PostgreSqlFlexibleServerRestartParameter
{
    RestartWithFailover = true,
    FailoverMode = PostgreSqlFlexibleServerFailoverMode.PlannedFailover
});
```

### 10. 更新服务器（扩缩容）

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

PostgreSqlFlexibleServerPatch patch = new PostgreSqlFlexibleServerPatch
{
    Sku = new PostgreSqlFlexibleServerSku("Standard_D4ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose),
    Storage = new PostgreSqlFlexibleServerStorage
    {
        StorageSizeInGB = 256,
        Tier = PostgreSqlStorageTierName.P40
    }
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await server
    .UpdateAsync(WaitUntil.Completed, patch);
```

### 11. 删除服务器

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

await server.DeleteAsync(WaitUntil.Completed);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `PostgreSqlFlexibleServerResource` | Flexible Server 实例 |
| `PostgreSqlFlexibleServerData` | 服务器配置数据 |
| `PostgreSqlFlexibleServerCollection` | 服务器集合 |
| `PostgreSqlFlexibleServerDatabaseResource` | 服务器内的数据库 |
| `PostgreSqlFlexibleServerFirewallRuleResource` | IP 防火墙规则 |
| `PostgreSqlFlexibleServerConfigurationResource` | 服务器参数 |
| `PostgreSqlFlexibleServerBackupResource` | 备份元数据 |
| `PostgreSqlFlexibleServerActiveDirectoryAdministratorResource` | Entra ID 管理员 |
| `PostgreSqlFlexibleServerSku` | SKU（计算层 + 规格） |
| `PostgreSqlFlexibleServerStorage` | 存储配置 |
| `PostgreSqlFlexibleServerHighAvailability` | 高可用配置 |
| `PostgreSqlFlexibleServerBackupProperties` | 备份设置 |
| `PostgreSqlFlexibleServerAuthConfig` | 身份验证设置 |

## SKU 层级

| 层级 | 适用场景 | SKU 示例 |
|------|----------|----------|
| `Burstable` | 开发/测试、轻量工作负载 | Standard_B1ms, Standard_B2s |
| `GeneralPurpose` | 生产工作负载 | Standard_D2ds_v4, Standard_D4ds_v4 |
| `MemoryOptimized` | 高内存需求 | Standard_E2ds_v4, Standard_E4ds_v4 |

## PostgreSQL 版本

| 版本 | 枚举值 |
|------|--------|
| PostgreSQL 11 | `Ver11` |
| PostgreSQL 12 | `Ver12` |
| PostgreSQL 13 | `Ver13` |
| PostgreSQL 14 | `Ver14` |
| PostgreSQL 15 | `Ver15` |
| PostgreSQL 16 | `Ver16` |

## 高可用模式

| 模式 | 说明 |
|------|------|
| `Disabled` | 无高可用（单服务器） |
| `SameZone` | 同可用区内高可用 |
| `ZoneRedundant` | 跨可用区高可用 |

## 最佳实践

1. **使用 Flexible Server** — Single Server 已弃用
2. **启用跨可用区高可用** — 用于生产工作负载
3. **使用 DefaultAzureCredential** — 优于连接字符串
4. **配置 Entra ID 身份验证** — 比单独使用 SQL 身份验证更安全
5. **同时启用两种身份验证方式** — Entra ID + 密码，兼顾灵活性
6. **设置合适的备份保留期** — 根据合规要求设为 7-35 天
7. **使用专用端点** — 用于安全的网络访问
8. **调优服务器参数** — 根据工作负载特征调整
9. **使用读副本** — 用于读密集型工作负载
10. **停止开发/测试服务器** — 不使用时节省成本

## 错误处理

```csharp
using Azure;

try
{
    ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Server already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
```

## 连接字符串

创建服务器后，使用以下方式连接：

```csharp
// Npgsql connection string
string connectionString = $"Host={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    "Username=pgadmin;" +
    "Password=YourSecurePassword123!;" +
    "SSL Mode=Require;Trust Server Certificate=true;";

// With Entra ID token (recommended)
var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://ossrdbms-aad.database.windows.net/.default" }));

string connectionString = $"Host={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    $"Username=aad-admin@contoso.com;" +
    $"Password={token.Token};" +
    "SSL Mode=Require;";
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.PostgreSql` | PostgreSQL 管理（本 SDK） | `dotnet add package Azure.ResourceManager.PostgreSql` |
| `Azure.ResourceManager.MySql` | MySQL 管理 | `dotnet add package Azure.ResourceManager.MySql` |
| `Npgsql` | PostgreSQL 数据访问 | `dotnet add package Npgsql` |
| `Npgsql.EntityFrameworkCore.PostgreSQL` | EF Core 提供程序 | `dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.PostgreSql |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.postgresql |
| 产品文档 | https://learn.microsoft.com/azure/postgresql/flexible-server/ |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/postgresql/Azure.ResourceManager.PostgreSql |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
