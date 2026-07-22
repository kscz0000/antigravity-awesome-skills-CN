---
name: azure-resource-manager-durabletask-dotnet
description: Azure Resource Manager SDK for Durable Task Scheduler in .NET 的中文技能。当用户要求'管理 Azure Durable Task Scheduler 资源、创建调度器、配置 Task Hub、设置保留策略、使用 Azure Resource Manager 管理 Durable Task 资源'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.DurableTask (.NET)

管理平面 SDK，用于通过 Azure Resource Manager 预配和管理 Azure Durable Task Scheduler 资源。

> **⚠️ 管理平面 vs 数据平面**
> - **本 SDK (Azure.ResourceManager.DurableTask)**：创建调度器、Task Hub，配置保留策略
> - **数据平面 SDK (Microsoft.DurableTask.Client.AzureManaged)**：启动编排、查询实例、发送事件

## 安装

```bash
dotnet add package Azure.ResourceManager.DurableTask
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.0.0 (2025-11-03)，预览版 v1.0.0-beta.1 (2025-04-24)
**API 版本**：2025-11-01

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.DurableTask;

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
        └── DurableTaskSchedulerResource
            ├── DurableTaskHubResource
            └── DurableTaskRetentionPolicyResource
```

## 核心工作流

### 1. 创建 Durable Task Scheduler

```csharp
using Azure.ResourceManager.DurableTask;
using Azure.ResourceManager.DurableTask.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define scheduler with Dedicated SKU
var schedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 1  // Number of instances
        },
        // Optional: IP allowlist for network security
        IPAllowlist = { "10.0.0.0/24", "192.168.1.0/24" }
    }
};

// Create scheduler (long-running operation)
var schedulerCollection = resourceGroup.Value.GetDurableTaskSchedulers();
var operation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-scheduler",
    schedulerData);

DurableTaskSchedulerResource scheduler = operation.Value;
Console.WriteLine($"Scheduler created: {scheduler.Data.Name}");
Console.WriteLine($"Endpoint: {scheduler.Data.Properties.Endpoint}");
```

### 2. 使用 Consumption SKU 创建调度器

```csharp
// Consumption SKU (serverless)
var consumptionSchedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Consumption)
        // No capacity needed for consumption
    }
};

var operation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-serverless-scheduler",
    consumptionSchedulerData);
```

### 3. 创建 Task Hub

```csharp
// Task hubs are created under a scheduler
var taskHubData = new DurableTaskHubData
{
    // Properties are optional for basic task hub
};

var taskHubCollection = scheduler.GetDurableTaskHubs();
var hubOperation = await taskHubCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-taskhub",
    taskHubData);

DurableTaskHubResource taskHub = hubOperation.Value;
Console.WriteLine($"Task Hub created: {taskHub.Data.Name}");
```

### 4. 列出调度器

```csharp
// List all schedulers in subscription
await foreach (var sched in subscription.GetDurableTaskSchedulersAsync())
{
    Console.WriteLine($"Scheduler: {sched.Data.Name}");
    Console.WriteLine($"  Location: {sched.Data.Location}");
    Console.WriteLine($"  SKU: {sched.Data.Properties.Sku?.Name}");
    Console.WriteLine($"  Endpoint: {sched.Data.Properties.Endpoint}");
}

// List schedulers in resource group
var schedulers = resourceGroup.Value.GetDurableTaskSchedulers();
await foreach (var sched in schedulers.GetAllAsync())
{
    Console.WriteLine($"Scheduler: {sched.Data.Name}");
}
```

### 5. 按名称获取调度器

```csharp
// Get existing scheduler
var existingScheduler = await schedulerCollection.GetAsync("my-scheduler");
Console.WriteLine($"Found: {existingScheduler.Value.Data.Name}");

// Or use extension method
var schedulerResource = armClient.GetDurableTaskSchedulerResource(
    DurableTaskSchedulerResource.CreateResourceIdentifier(
        subscriptionId,
        "my-resource-group",
        "my-scheduler"));
var scheduler = await schedulerResource.GetAsync();
```

### 6. 更新调度器

```csharp
// Get current scheduler
var scheduler = await schedulerCollection.GetAsync("my-scheduler");

// Update with new configuration
var updateData = new DurableTaskSchedulerData(scheduler.Value.Data.Location)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 2  // Scale up
        },
        IPAllowlist = { "10.0.0.0/16" }  // Update IP allowlist
    }
};

var updateOperation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-scheduler",
    updateData);
```

### 7. 删除资源

```csharp
// Delete task hub first
var taskHub = await scheduler.GetDurableTaskHubs().GetAsync("my-taskhub");
await taskHub.Value.DeleteAsync(WaitUntil.Completed);

// Then delete scheduler
await scheduler.DeleteAsync(WaitUntil.Completed);
```

### 8. 管理保留策略

```csharp
// Get retention policy collection
var retentionPolicies = scheduler.GetDurableTaskRetentionPolicies();

// Create or update retention policy
var retentionData = new DurableTaskRetentionPolicyData
{
    Properties = new DurableTaskRetentionPolicyProperties
    {
        // Configure retention settings
    }
};

var retentionOperation = await retentionPolicies.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "default",  // Policy name
    retentionData);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `DurableTaskSchedulerResource` | 表示一个 Durable Task Scheduler |
| `DurableTaskSchedulerCollection` | 调度器 CRUD 集合 |
| `DurableTaskSchedulerData` | 调度器创建/更新载荷 |
| `DurableTaskSchedulerProperties` | 调度器配置（SKU、IPAllowlist） |
| `DurableTaskSchedulerSku` | SKU 配置（Name、Capacity、RedundancyState） |
| `DurableTaskSchedulerSkuName` | SKU 选项：`Dedicated`、`Consumption` |
| `DurableTaskHubResource` | 表示一个 Task Hub |
| `DurableTaskHubCollection` | Task Hub CRUD 集合 |
| `DurableTaskHubData` | Task Hub 创建载荷 |
| `DurableTaskRetentionPolicyResource` | 保留策略管理 |
| `DurableTaskRetentionPolicyData` | 保留策略配置 |
| `DurableTaskExtensions` | ARM 客户端扩展方法 |

## SKU 选项

| SKU | 描述 | 适用场景 |
|-----|------|----------|
| `Dedicated` | 固定容量，可配置实例数 | 生产工作负载，可预测性能 |
| `Consumption` | 无服务器，自动缩放 | 开发环境，可变工作负载 |

## 扩展方法

SDK 在 `SubscriptionResource` 和 `ResourceGroupResource` 上提供了扩展方法：

```csharp
// On SubscriptionResource
subscription.GetDurableTaskSchedulers();           // List all in subscription
subscription.GetDurableTaskSchedulersAsync();      // Async enumerable

// On ResourceGroupResource
resourceGroup.GetDurableTaskSchedulers();          // Get collection
resourceGroup.GetDurableTaskSchedulerAsync(name);  // Get by name

// On ArmClient
armClient.GetDurableTaskSchedulerResource(id);     // Get by resource ID
armClient.GetDurableTaskHubResource(id);           // Get task hub by ID
```

## 最佳实践

1. 对必须完成后才能继续的操作，**使用 `WaitUntil.Completed`**
2. 当你想手动轮询或并行运行操作时，**使用 `WaitUntil.Started`**
3. **始终使用 `DefaultAzureCredential`** — 绝不硬编码密钥
4. **处理 `RequestFailedException`** 以应对 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 实现幂等操作
6. **先删除 Task Hub 再删除调度器** — 包含 Task Hub 的调度器无法删除
7. **在生产环境中使用 IP 白名单** 保障网络安全

## 错误处理

```csharp
using Azure;

try
{
    var operation = await schedulerCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, schedulerName, schedulerData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Scheduler already exists");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Resource group not found");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 完整示例

```csharp
using Azure;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.DurableTask;
using Azure.ResourceManager.DurableTask.Models;
using Azure.ResourceManager.Resources;

// Setup
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID")!;
var resourceGroupName = Environment.GetEnvironmentVariable("AZURE_RESOURCE_GROUP")!;

var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
var resourceGroup = await subscription.GetResourceGroupAsync(resourceGroupName);

// Create scheduler
var schedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 1
        }
    }
};

var schedulerCollection = resourceGroup.Value.GetDurableTaskSchedulers();
var schedulerOp = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, "my-scheduler", schedulerData);
var scheduler = schedulerOp.Value;

Console.WriteLine($"Scheduler endpoint: {scheduler.Data.Properties.Endpoint}");

// Create task hub
var taskHubData = new DurableTaskHubData();
var taskHubOp = await scheduler.GetDurableTaskHubs().CreateOrUpdateAsync(
    WaitUntil.Completed, "my-taskhub", taskHubData);
var taskHub = taskHubOp.Value;

Console.WriteLine($"Task Hub: {taskHub.Data.Name}");

// Cleanup
await taskHub.DeleteAsync(WaitUntil.Completed);
await scheduler.DeleteAsync(WaitUntil.Completed);
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.DurableTask` | 管理平面（本 SDK） | `dotnet add package Azure.ResourceManager.DurableTask` |
| `Microsoft.DurableTask.Client.AzureManaged` | 数据平面（编排、活动） | `dotnet add package Microsoft.DurableTask.Client.AzureManaged` |
| `Microsoft.DurableTask.Worker.AzureManaged` | 运行编排的 Worker | `dotnet add package Microsoft.DurableTask.Worker.AzureManaged` |
| `Azure.Identity` | 身份验证 | `dotnet add package Azure.Identity` |
| `Azure.ResourceManager` | 基础 ARM SDK | `dotnet add package Azure.ResourceManager` |

## 源码参考

- [GitHub: Azure.ResourceManager.DurableTask](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/durabletask/Azure.ResourceManager.DurableTask)
- [NuGet: Azure.ResourceManager.DurableTask](https://www.nuget.org/packages/Azure.ResourceManager.DurableTask)

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
