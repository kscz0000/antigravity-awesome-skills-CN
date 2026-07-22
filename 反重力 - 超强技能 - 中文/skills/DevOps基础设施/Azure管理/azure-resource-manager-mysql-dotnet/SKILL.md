---
name: azure-resource-manager-mysql-dotnet
description: Azure MySQL Flexible Server .NET SDK。用于 MySQL Flexible Server 部署的数据库管理。当用户要求'管理 Azure MySQL Flexible Server'、'创建 MySQL 灵活服务器'、'配置 MySQL 防火墙规则'或'.NET Azure MySQL SDK'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.MySql (.NET)

用于管理 MySQL Flexible Server 部署的 Azure Resource Manager SDK。

## 安装

```bash
dotnet add package Azure.ResourceManager.MySql
dotnet add package Azure.Identity
```

**当前版本**：v1.2.0 (GA)
**API 版本**：2023-12-30

> **注意**：本技能聚焦于 MySQL Flexible Server。Single Server 已弃用并计划停用。

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_MYSQL_SERVER_NAME=<your-mysql-server>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.MySql;
using Azure.ResourceManager.MySql.FlexibleServers;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## 资源层次结构

```
Subscription
└── ResourceGroup
    └── MySqlFlexibleServer                 # MySQL Flexible Server 实例
        ├── MySqlFlexibleServerDatabase     # 服务器内的数据库
        ├── MySqlFlexibleServerFirewallRule # IP 防火墙规则
        ├── MySqlFlexibleServerConfiguration # 服务器参数
        ├── MySqlFlexibleServerBackup       # 备份信息
        ├── MySqlFlexibleServerMaintenanceWindow # 维护计划
        └── MySqlFlexibleServerAadAdministrator # Entra ID 管理员
```

## 核心工作流

### 1. 创建 MySQL Flexible Server

```csharp
using Azure.ResourceManager.MySql.FlexibleServers;
using Azure.ResourceManager.MySql.FlexibleServers.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

MySqlFlexibleServerCollection servers = resourceGroup.GetMySqlFlexibleServers();

MySqlFlexibleServerData data = new MySqlFlexibleServerData(AzureLocation.EastUS)
{
    Sku = new MySqlFlexibleServerSku("Standard_D2ds_v4", MySqlFlexibleServerSkuTier.GeneralPurpose),
    AdministratorLogin = "mysqladmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = MySqlFlexibleServerVersion.Ver8_0_21,
    Storage = new MySqlFlexibleServerStorage
    {
        StorageSizeInGB = 128,
        AutoGrow = MySqlFlexibleServerEnableStatusEnum.Enabled,
        Iops = 3000
    },
    Backup = new MySqlFlexibleServerBackupProperties
    {
        BackupRetentionDays = 7,
        GeoRedundantBackup = MySqlFlexibleServerEnableStatusEnum.Disabled
    },
    HighAvailability = new MySqlFlexibleServerHighAvailability
    {
        Mode = MySqlFlexibleServerHighAvailabilityMode.ZoneRedundant,
        StandbyAvailabilityZone = "2"
    },
    AvailabilityZone = "1"
};

ArmOperation<MySqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql-server", data);

MySqlFlexibleServerResource server = operation.Value;
Console.WriteLine($"Server created: {server.Data.FullyQualifiedDomainName}");
```

### 2. 创建数据库

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

MySqlFlexibleServerDatabaseCollection databases = server.GetMySqlFlexibleServerDatabases();

MySqlFlexibleServerDatabaseData dbData = new MySqlFlexibleServerDatabaseData
{
    Charset = "utf8mb4",
    Collation = "utf8mb4_unicode_ci"
};

ArmOperation<MySqlFlexibleServerDatabaseResource> operation = await databases
    .CreateOrUpdateAsync(WaitUntil.Completed, "myappdb", dbData);

MySqlFlexibleServerDatabaseResource database = operation.Value;
Console.WriteLine($"Database created: {database.Data.Name}");
```

### 3. 配置防火墙规则

```csharp
MySqlFlexibleServerFirewallRuleCollection firewallRules = server.GetMySqlFlexibleServerFirewallRules();

// 允许特定 IP 范围
MySqlFlexibleServerFirewallRuleData ruleData = new MySqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("10.0.0.1"),
    EndIPAddress = System.Net.IPAddress.Parse("10.0.0.255")
};

ArmOperation<MySqlFlexibleServerFirewallRuleResource> operation = await firewallRules
    .CreateOrUpdateAsync(WaitUntil.Completed, "allow-internal", ruleData);

// 允许 Azure 服务
MySqlFlexibleServerFirewallRuleData azureServicesRule = new MySqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("0.0.0.0"),
    EndIPAddress = System.Net.IPAddress.Parse("0.0.0.0")
};

await firewallRules.CreateOrUpdateAsync(WaitUntil.Completed, "AllowAllAzureServicesAndResourcesWithinAzureIps", azureServicesRule);
```

### 4. 更新服务器配置

```csharp
MySqlFlexibleServerConfigurationCollection configurations = server.GetMySqlFlexibleServerConfigurations();

// 获取当前配置
MySqlFlexibleServerConfigurationResource config = await configurations
    .GetAsync("max_connections");

// 更新配置
MySqlFlexibleServerConfigurationData configData = new MySqlFlexibleServerConfigurationData
{
    Value = "500",
    Source = MySqlFlexibleServerConfigurationSource.UserOverride
};

ArmOperation<MySqlFlexibleServerConfigurationResource> operation = await configurations
    .CreateOrUpdateAsync(WaitUntil.Completed, "max_connections", configData);

// 常见调优参数
string[] commonParams = { "max_connections", "innodb_buffer_pool_size", "slow_query_log", "long_query_time" };
```

### 5. 配置 Entra ID 管理员

```csharp
MySqlFlexibleServerAadAdministratorCollection admins = server.GetMySqlFlexibleServerAadAdministrators();

MySqlFlexibleServerAadAdministratorData adminData = new MySqlFlexibleServerAadAdministratorData
{
    AdministratorType = MySqlFlexibleServerAdministratorType.ActiveDirectory,
    Login = "aad-admin@contoso.com",
    Sid = Guid.Parse("<entra-object-id>"),
    TenantId = Guid.Parse("<tenant-id>"),
    IdentityResourceId = new ResourceIdentifier("/subscriptions/.../userAssignedIdentities/mysql-identity")
};

ArmOperation<MySqlFlexibleServerAadAdministratorResource> operation = await admins
    .CreateOrUpdateAsync(WaitUntil.Completed, "ActiveDirectory", adminData);
```

### 6. 列出和管理服务器

```csharp
// 列出资源组中的服务器
await foreach (MySqlFlexibleServerResource server in resourceGroup.GetMySqlFlexibleServers())
{
    Console.WriteLine($"Server: {server.Data.Name}");
    Console.WriteLine($"  FQDN: {server.Data.FullyQualifiedDomainName}");
    Console.WriteLine($"  Version: {server.Data.Version}");
    Console.WriteLine($"  State: {server.Data.State}");
    Console.WriteLine($"  SKU: {server.Data.Sku.Name} ({server.Data.Sku.Tier})");
}

// 列出服务器中的数据库
await foreach (MySqlFlexibleServerDatabaseResource db in server.GetMySqlFlexibleServerDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}");
}
```

### 7. 备份和还原

```csharp
// 列出可用备份
await foreach (MySqlFlexibleServerBackupResource backup in server.GetMySqlFlexibleServerBackups())
{
    Console.WriteLine($"Backup: {backup.Data.Name}");
    Console.WriteLine($"  Type: {backup.Data.BackupType}");
    Console.WriteLine($"  Completed: {backup.Data.CompletedOn}");
}

// 时间点还原
MySqlFlexibleServerData restoreData = new MySqlFlexibleServerData(AzureLocation.EastUS)
{
    CreateMode = MySqlFlexibleServerCreateMode.PointInTimeRestore,
    SourceServerResourceId = server.Id,
    RestorePointInTime = DateTimeOffset.UtcNow.AddHours(-2)
};

ArmOperation<MySqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql-restored", restoreData);
```

### 8. 停止和启动服务器

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

// 停止服务器（不使用时节省成本）
await server.StopAsync(WaitUntil.Completed);

// 启动服务器
await server.StartAsync(WaitUntil.Completed);

// 重启服务器
await server.RestartAsync(WaitUntil.Completed, new MySqlFlexibleServerRestartParameter
{
    RestartWithFailover = MySqlFlexibleServerEnableStatusEnum.Enabled,
    MaxFailoverSeconds = 60
});
```

### 9. 更新服务器（扩缩容）

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

MySqlFlexibleServerPatch patch = new MySqlFlexibleServerPatch
{
    Sku = new MySqlFlexibleServerSku("Standard_D4ds_v4", MySqlFlexibleServerSkuTier.GeneralPurpose),
    Storage = new MySqlFlexibleServerStorage
    {
        StorageSizeInGB = 256,
        Iops = 6000
    }
};

ArmOperation<MySqlFlexibleServerResource> operation = await server
    .UpdateAsync(WaitUntil.Completed, patch);
```

### 10. 删除服务器

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

await server.DeleteAsync(WaitUntil.Completed);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `MySqlFlexibleServerResource` | Flexible Server 实例 |
| `MySqlFlexibleServerData` | 服务器配置数据 |
| `MySqlFlexibleServerCollection` | 服务器集合 |
| `MySqlFlexibleServerDatabaseResource` | 服务器内的数据库 |
| `MySqlFlexibleServerFirewallRuleResource` | IP 防火墙规则 |
| `MySqlFlexibleServerConfigurationResource` | 服务器参数 |
| `MySqlFlexibleServerBackupResource` | 备份元数据 |
| `MySqlFlexibleServerAadAdministratorResource` | Entra ID 管理员 |
| `MySqlFlexibleServerSku` | SKU（计算层 + 规格） |
| `MySqlFlexibleServerStorage` | 存储配置 |
| `MySqlFlexibleServerHighAvailability` | 高可用配置 |
| `MySqlFlexibleServerBackupProperties` | 备份设置 |

## SKU 层级

| 层级 | 使用场景 | SKU 示例 |
|------|----------|----------|
| `Burstable` | 开发/测试、轻量工作负载 | Standard_B1ms, Standard_B2s |
| `GeneralPurpose` | 生产工作负载 | Standard_D2ds_v4, Standard_D4ds_v4 |
| `MemoryOptimized` | 高内存需求 | Standard_E2ds_v4, Standard_E4ds_v4 |

## 高可用模式

| 模式 | 说明 |
|------|------|
| `Disabled` | 无高可用（单服务器） |
| `SameZone` | 同可用区内高可用 |
| `ZoneRedundant` | 跨可用区高可用 |

## 最佳实践

1. **使用 Flexible Server** — Single Server 已弃用
2. **启用区域冗余高可用** — 用于生产工作负载
3. **使用 DefaultAzureCredential** — 优先于连接字符串
4. **配置 Entra ID 身份验证** — 比 SQL 身份验证更安全
5. **启用存储自动增长** — 防止空间不足问题
6. **设置适当的备份保留期** — 根据合规要求设置 7-35 天
7. **使用私有终结点** — 用于安全的网络访问
8. **调优服务器参数** — 根据工作负载特征调整
9. **使用 Azure Monitor 监控** — 启用指标和日志
10. **停止开发/测试服务器** — 不使用时节省成本

## 错误处理

```csharp
using Azure;

try
{
    ArmOperation<MySqlFlexibleServerResource> operation = await servers
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql", data);
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
// ADO.NET 连接字符串
string connectionString = $"Server={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    "User Id=mysqladmin;" +
    "Password=YourSecurePassword123!;" +
    "SslMode=Required;";

// 使用 Entra ID 令牌（推荐）
var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://ossrdbms-aad.database.windows.net/.default" }));

string connectionString = $"Server={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    $"User Id=aad-admin@contoso.com;" +
    $"Password={token.Token};" +
    "SslMode=Required;";
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.MySql` | MySQL 管理（本 SDK） | `dotnet add package Azure.ResourceManager.MySql` |
| `Azure.ResourceManager.PostgreSql` | PostgreSQL 管理 | `dotnet add package Azure.ResourceManager.PostgreSql` |
| `MySqlConnector` | MySQL 数据访问 | `dotnet add package MySqlConnector` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.MySql |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.mysql |
| 产品文档 | https://learn.microsoft.com/azure/mysql/flexible-server/ |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/mysql/Azure.ResourceManager.MySql |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
