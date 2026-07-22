---
name: azure-mgmt-fabric-dotnet
description: Azure Resource Manager .NET SDK，用于管理 Fabric 容量资源。当用户要求'管理 Azure Fabric 容量'、'Fabric SDK .NET'、'Azure Fabric 资源管理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.Fabric (.NET)

管理平面 SDK，用于通过 Azure Resource Manager 预配和管理 Microsoft Fabric 容量资源。

> **仅限管理平面**
> 本 SDK 管理 Fabric *容量*（计算资源）。如需操作 Fabric 工作区、lakehouse、warehouse 和数据项，请使用 Microsoft Fabric REST API 或数据平面 SDK。

## 安装

```bash
dotnet add package Azure.ResourceManager.Fabric
dotnet add package Azure.Identity
```

**当前版本**：1.0.0（GA - 2025年9月）
**API 版本**：2023-11-01
**目标框架**：.NET 8.0、.NET Standard 2.0

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
using Azure.ResourceManager.Fabric;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscription = await armClient.GetDefaultSubscriptionAsync();
```

## 资源层级

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── FabricCapacityResource
```

## 核心工作流

### 1. 创建 Fabric 容量

```csharp
using Azure.ResourceManager.Fabric;
using Azure.ResourceManager.Fabric.Models;
using Azure.Core;

// Get resource group
var resourceGroup = await subscription.GetResourceGroupAsync("my-resource-group");

// Define capacity configuration
var administration = new FabricCapacityAdministration(
    new[] { "admin@contoso.com" }  // Capacity administrators (UPNs or object IDs)
);

var properties = new FabricCapacityProperties(administration);

var sku = new FabricSku("F64", FabricSkuTier.Fabric);

var capacityData = new FabricCapacityData(
    AzureLocation.WestUS2,
    properties,
    sku)
{
    Tags = { ["Environment"] = "Production" }
};

// Create capacity (long-running operation)
var capacityCollection = resourceGroup.Value.GetFabricCapacities();
var operation = await capacityCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-fabric-capacity",
    capacityData);

FabricCapacityResource capacity = operation.Value;
Console.WriteLine($"Created capacity: {capacity.Data.Name}");
Console.WriteLine($"State: {capacity.Data.Properties.State}");
```

### 2. 获取 Fabric 容量

```csharp
// Get existing capacity
var capacity = await resourceGroup.Value
    .GetFabricCapacityAsync("my-fabric-capacity");

Console.WriteLine($"Name: {capacity.Value.Data.Name}");
Console.WriteLine($"Location: {capacity.Value.Data.Location}");
Console.WriteLine($"SKU: {capacity.Value.Data.Sku.Name}");
Console.WriteLine($"State: {capacity.Value.Data.Properties.State}");
Console.WriteLine($"Provisioning State: {capacity.Value.Data.Properties.ProvisioningState}");
```

### 3. 更新容量（扩缩 SKU 或更改管理员）

```csharp
var capacity = await resourceGroup.Value
    .GetFabricCapacityAsync("my-fabric-capacity");

var patch = new FabricCapacityPatch
{
    Sku = new FabricSku("F128", FabricSkuTier.Fabric),  // Scale up
    Properties = new FabricCapacityUpdateProperties
    {
        Administration = new FabricCapacityAdministration(
            new[] { "admin@contoso.com", "newadmin@contoso.com" }
        )
    }
};

var updateOperation = await capacity.Value.UpdateAsync(
    WaitUntil.Completed,
    patch);

Console.WriteLine($"Updated SKU: {updateOperation.Value.Data.Sku.Name}");
```

### 4. 暂停和恢复容量

```csharp
// Suspend capacity (stop billing for compute)
await capacity.Value.SuspendAsync(WaitUntil.Completed);
Console.WriteLine("Capacity suspended");

// Resume capacity
var resumeOperation = await capacity.Value.ResumeAsync(WaitUntil.Completed);
Console.WriteLine($"Capacity resumed. State: {resumeOperation.Value.Data.Properties.State}");
```

### 5. 删除容量

```csharp
await capacity.Value.DeleteAsync(WaitUntil.Completed);
Console.WriteLine("Capacity deleted");
```

### 6. 列出所有容量

```csharp
// In a resource group
await foreach (var cap in resourceGroup.Value.GetFabricCapacities())
{
    Console.WriteLine($"- {cap.Data.Name} ({cap.Data.Sku.Name})");
}

// In a subscription
await foreach (var cap in subscription.GetFabricCapacitiesAsync())
{
    Console.WriteLine($"- {cap.Data.Name} in {cap.Data.Location}");
}
```

### 7. 检查名称可用性

```csharp
var checkContent = new FabricNameAvailabilityContent
{
    Name = "my-new-capacity",
    ResourceType = "Microsoft.Fabric/capacities"
};

var result = await subscription.CheckFabricCapacityNameAvailabilityAsync(
    AzureLocation.WestUS2,
    checkContent);

if (result.Value.IsNameAvailable == true)
{
    Console.WriteLine("Name is available!");
}
else
{
    Console.WriteLine($"Name unavailable: {result.Value.Reason} - {result.Value.Message}");
}
```

### 8. 列出可用 SKU

```csharp
// List all SKUs available in subscription
await foreach (var skuDetails in subscription.GetSkusFabricCapacitiesAsync())
{
    Console.WriteLine($"SKU: {skuDetails.Name}");
    Console.WriteLine($"  Resource Type: {skuDetails.ResourceType}");
    foreach (var location in skuDetails.Locations)
    {
        Console.WriteLine($"  Location: {location}");
    }
}

// List SKUs available for an existing capacity (for scaling)
await foreach (var skuDetails in capacity.Value.GetSkusForCapacityAsync())
{
    Console.WriteLine($"Can scale to: {skuDetails.Sku.Name}");
}
```

## SKU 参考

| SKU 名称 | 容量单位 (CU) | Power BI 等效 |
|----------|---------------------|---------------------|
| F2 | 2 | - |
| F4 | 4 | - |
| F8 | 8 | EM1/A1 |
| F16 | 16 | EM2/A2 |
| F32 | 32 | EM3/A3 |
| F64 | 64 | P1/A4 |
| F128 | 128 | P2/A5 |
| F256 | 256 | P3/A6 |
| F512 | 512 | P4/A7 |
| F1024 | 1024 | P5/A8 |
| F2048 | 2048 | - |

## 关键类型参考

| 类型 | 用途 |
|------|---------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `FabricCapacityResource` | 表示 Fabric 容量实例 |
| `FabricCapacityCollection` | 容量 CRUD 操作的集合 |
| `FabricCapacityData` | 容量创建/读取数据模型 |
| `FabricCapacityPatch` | 容量更新载荷 |
| `FabricCapacityProperties` | 容量属性（管理、状态） |
| `FabricCapacityAdministration` | 管理员成员配置 |
| `FabricSku` | SKU 配置（名称和层级） |
| `FabricSkuTier` | 定价层级（当前仅有 "Fabric"） |
| `FabricProvisioningState` | 预配状态（Succeeded、Failed 等） |
| `FabricResourceState` | 资源状态（Active、Suspended 等） |
| `FabricNameAvailabilityContent` | 名称可用性检查请求 |
| `FabricNameAvailabilityResult` | 名称可用性检查响应 |

## 预配和资源状态

### 预配状态（`FabricProvisioningState`）
- `Succeeded` - 操作成功完成
- `Failed` - 操作失败
- `Canceled` - 操作已取消
- `Deleting` - 容量正在删除
- `Provisioning` - 初始预配进行中
- `Updating` - 更新操作进行中

### 资源状态（`FabricResourceState`）
- `Active` - 容量正在运行且可用
- `Provisioning` - 正在预配
- `Failed` - 处于失败状态
- `Updating` - 正在更新
- `Deleting` - 正在删除
- `Suspending` - 正在转换为暂停
- `Suspended` - 已暂停（不收取计算费用）
- `Pausing` - 正在转换为停用
- `Paused` - 已停用
- `Resuming` - 正在从暂停/停用恢复
- `Scaling` - 正在缩放到不同 SKU
- `Preparing` - 正在准备资源

## 最佳实践

1. **使用 `WaitUntil.Completed`** 确保操作在继续前完成
2. **使用 `WaitUntil.Started`** 当需要手动轮询或并行运行操作时
3. **始终使用 `DefaultAzureCredential`** — 绝不硬编码凭据
4. **处理 `RequestFailedException`** 以应对 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 实现幂等操作
6. **不使用时暂停** — Fabric 容量即使空闲也会按计算计费
7. **操作前检查预配状态** — 在对容量执行操作前确认状态
8. **使用合适的 SKU** — 开发/测试从小规格（F2/F4）开始，生产环境再扩容

## 错误处理

```csharp
using Azure;

try
{
    var operation = await capacityCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, capacityName, capacityData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Capacity already exists or conflict");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Insufficient permissions or quota exceeded");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 常见陷阱

1. **容量名称必须全局唯一** — Fabric 容量名称在所有 Azure 订阅中必须唯一
2. **暂停不等于删除** — 暂停的容量仍然存在，但不收取计算费用
3. **SKU 变更可能需要停机** — 扩缩操作可能需要数分钟
4. **管理员 UPN 必须有效** — 容量管理员必须是有效的 Azure AD 用户
5. **区域限制** — 并非所有 SKU 在所有区域都可用；使用 `GetSkusFabricCapacitiesAsync` 检查
6. **预配时间较长** — 容量创建可能需要 5-15 分钟

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|---------|---------|
| `Azure.ResourceManager.Fabric` | 管理平面（本 SDK） | `dotnet add package Azure.ResourceManager.Fabric` |
| `Microsoft.Fabric.Api` | 数据平面操作（beta） | `dotnet add package Microsoft.Fabric.Api --prerelease` |
| `Azure.ResourceManager` | 核心 ARM SDK | `dotnet add package Azure.ResourceManager` |
| `Azure.Identity` | 身份验证 | `dotnet add package Azure.Identity` |

## 参考

- [Azure.ResourceManager.Fabric NuGet](https://www.nuget.org/packages/Azure.ResourceManager.Fabric)
- [GitHub Source](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/fabric/Azure.ResourceManager.Fabric)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Fabric Capacity Management](https://learn.microsoft.com/fabric/admin/service-admin-portal-capacity-settings)

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
