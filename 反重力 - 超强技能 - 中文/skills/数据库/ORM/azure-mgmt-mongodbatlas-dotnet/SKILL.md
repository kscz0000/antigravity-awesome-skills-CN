---
name: azure-mgmt-mongodbatlas-dotnet
description: "将 MongoDB Atlas 组织作为 Azure ARM 资源管理，通过 Azure Marketplace 实现统一计费。当用户要求'管理 Azure 上的 MongoDB Atlas 组织'、'通过 Azure Marketplace 集成 MongoDB Atlas'、'使用 Azure SDK 管理 MongoDB Atlas'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure.ResourceManager.MongoDBAtlas SDK

将 MongoDB Atlas 组织作为 Azure ARM 资源管理，通过 Azure Marketplace 实现统一计费。

## 包信息

| 属性 | 值 |
|------|-----|
| 包 | `Azure.ResourceManager.MongoDBAtlas` |
| 版本 | 1.0.0 (GA) |
| API 版本 | 2025-06-01 |
| 资源类型 | `MongoDB.Atlas/organizations` |
| NuGet | [Azure.ResourceManager.MongoDBAtlas](https://www.nuget.org/packages/Azure.ResourceManager.MongoDBAtlas) |

## 安装

```bash
dotnet add package Azure.ResourceManager.MongoDBAtlas
dotnet add package Azure.Identity
dotnet add package Azure.ResourceManager
```

## 重要范围限制

此 SDK 管理**MongoDB Atlas 组织作为 Azure ARM 资源**，用于 Marketplace 集成。它不能直接管理：
- Atlas 集群
- 数据库
- 集合
- 用户/角色

如需管理集群，请在创建组织后直接使用 MongoDB Atlas API。

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.MongoDBAtlas;
using Azure.ResourceManager.MongoDBAtlas.Models;

// Create ARM client with DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);
```

## 核心类型

| 类型 | 用途 |
|------|------|
| `MongoDBAtlasOrganizationResource` | 表示 Atlas 组织的 ARM 资源 |
| `MongoDBAtlasOrganizationCollection` | 资源组中的组织集合 |
| `MongoDBAtlasOrganizationData` | 组织资源的数据模型 |
| `MongoDBAtlasOrganizationProperties` | 组织特有属性 |
| `MongoDBAtlasMarketplaceDetails` | Azure Marketplace 订阅详情 |
| `MongoDBAtlasOfferDetails` | Marketplace 产品/服务配置 |
| `MongoDBAtlasUserDetails` | 组织的用户信息 |
| `MongoDBAtlasPartnerProperties` | MongoDB 特有属性（组织名称、ID） |

## 工作流

### 获取组织集合

```csharp
// Get resource group
var subscription = await armClient.GetDefaultSubscriptionAsync();
var resourceGroup = await subscription.GetResourceGroupAsync("my-resource-group");

// Get organizations collection
MongoDBAtlasOrganizationCollection organizations = 
    resourceGroup.Value.GetMongoDBAtlasOrganizations();
```

### 创建组织

```csharp
var organizationName = "my-atlas-org";
var location = AzureLocation.EastUS2;

// Build organization data
var organizationData = new MongoDBAtlasOrganizationData(location)
{
    Properties = new MongoDBAtlasOrganizationProperties(
        marketplace: new MongoDBAtlasMarketplaceDetails(
            subscriptionId: "your-azure-subscription-id",
            offerDetails: new MongoDBAtlasOfferDetails(
                publisherId: "mongodb",
                offerId: "mongodb_atlas_azure_native_prod",
                planId: "private_plan",
                planName: "Pay as You Go (Free) (Private)",
                termUnit: "P1M",
                termId: "gmz7xq9ge3py"
            )
        ),
        user: new MongoDBAtlasUserDetails(
            emailAddress: "admin@example.com",
            upn: "admin@example.com"
        )
        {
            FirstName = "Admin",
            LastName = "User"
        }
    )
    {
        PartnerProperties = new MongoDBAtlasPartnerProperties
        {
            OrganizationName = organizationName
        }
    },
    Tags = { ["Environment"] = "Production" }
};

// Create the organization (long-running operation)
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Completed,
    organizationName,
    organizationData
);

MongoDBAtlasOrganizationResource organization = operation.Value;
Console.WriteLine($"Created: {organization.Id}");
```

### 获取已有组织

```csharp
// Option 1: From collection
MongoDBAtlasOrganizationResource org = 
    await organizations.GetAsync("my-atlas-org");

// Option 2: From resource identifier
var resourceId = MongoDBAtlasOrganizationResource.CreateResourceIdentifier(
    subscriptionId: "subscription-id",
    resourceGroupName: "my-resource-group",
    organizationName: "my-atlas-org"
);
MongoDBAtlasOrganizationResource org2 = 
    armClient.GetMongoDBAtlasOrganizationResource(resourceId);
await org2.GetAsync(); // Fetch data
```

### 列出组织

```csharp
// List in resource group
await foreach (var org in organizations.GetAllAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}");
    Console.WriteLine($"  Location: {org.Data.Location}");
    Console.WriteLine($"  State: {org.Data.Properties?.ProvisioningState}");
}

// List across subscription
await foreach (var org in subscription.GetMongoDBAtlasOrganizationsAsync())
{
    Console.WriteLine($"Org: {org.Data.Name} in {org.Data.Id}");
}
```

### 更新标签

```csharp
// Add a single tag
await organization.AddTagAsync("CostCenter", "12345");

// Replace all tags
await organization.SetTagsAsync(new Dictionary<string, string>
{
    ["Environment"] = "Production",
    ["Team"] = "Platform"
});

// Remove a tag
await organization.RemoveTagAsync("OldTag");
```

### 更新组织属性

```csharp
var patch = new MongoDBAtlasOrganizationPatch
{
    Tags = { ["UpdatedAt"] = DateTime.UtcNow.ToString("o") },
    Properties = new MongoDBAtlasOrganizationUpdateProperties
    {
        // Update user details if needed
        User = new MongoDBAtlasUserDetails(
            emailAddress: "newadmin@example.com",
            upn: "newadmin@example.com"
        )
    }
};

var updateOperation = await organization.UpdateAsync(
    WaitUntil.Completed,
    patch
);
```

### 删除组织

```csharp
// Delete (long-running operation)
await organization.DeleteAsync(WaitUntil.Completed);
```

## 模型属性参考

### MongoDBAtlasOrganizationProperties

| 属性 | 类型 | 说明 |
|------|------|------|
| `Marketplace` | `MongoDBAtlasMarketplaceDetails` | 必填。Marketplace 订阅详情 |
| `User` | `MongoDBAtlasUserDetails` | 必填。组织管理员用户 |
| `PartnerProperties` | `MongoDBAtlasPartnerProperties` | MongoDB 特有属性 |
| `ProvisioningState` | `MongoDBAtlasResourceProvisioningState` | 只读。当前预配状态 |

### MongoDBAtlasMarketplaceDetails

| 属性 | 类型 | 说明 |
|------|------|------|
| `SubscriptionId` | `string` | 必填。用于计费的 Azure 订阅 ID |
| `OfferDetails` | `MongoDBAtlasOfferDetails` | 必填。Marketplace 产品/服务配置 |
| `SubscriptionStatus` | `MarketplaceSubscriptionStatus` | 只读。订阅状态 |

### MongoDBAtlasOfferDetails

| 属性 | 类型 | 说明 |
|------|------|------|
| `PublisherId` | `string` | 必填。发布者 ID（通常为 "mongodb"） |
| `OfferId` | `string` | 必填。产品/服务 ID |
| `PlanId` | `string` | 必填。计划 ID |
| `PlanName` | `string` | 必填。计划的显示名称 |
| `TermUnit` | `string` | 必填。计费期限单位（如 "P1M"） |
| `TermId` | `string` | 必填。期限标识符 |

### MongoDBAtlasUserDetails

| 属性 | 类型 | 说明 |
|------|------|------|
| `EmailAddress` | `string` | 必填。用户邮箱地址 |
| `Upn` | `string` | 必填。用户主体名称 |
| `FirstName` | `string` | 可选。用户名 |
| `LastName` | `string` | 可选。用户姓氏 |

### MongoDBAtlasPartnerProperties

| 属性 | 类型 | 说明 |
|------|------|------|
| `OrganizationName` | `string` | MongoDB Atlas 组织名称 |
| `OrganizationId` | `string` | 只读。MongoDB Atlas 组织 ID |

## 预配状态

| 状态 | 说明 |
|------|------|
| `Succeeded` | 资源预配成功 |
| `Failed` | 预配失败 |
| `Canceled` | 预配已取消 |
| `Provisioning` | 资源正在预配中 |
| `Updating` | 资源正在更新中 |
| `Deleting` | 资源正在删除中 |
| `Accepted` | 请求已接受，预配正在启动 |

## Marketplace 订阅状态

| 状态 | 说明 |
|------|------|
| `PendingFulfillmentStart` | 订阅待激活 |
| `Subscribed` | 订阅活跃 |
| `Suspended` | 订阅已暂停 |
| `Unsubscribed` | 订阅已取消 |

## 最佳实践

### 使用异步方法

```csharp
// Prefer async for all operations
var org = await organizations.GetAsync("my-org");
await org.Value.AddTagAsync("key", "value");
```

### 处理长时间运行的操作

```csharp
// Wait for completion
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Completed,  // Blocks until done
    name,
    data
);

// Or start and poll later
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Started,  // Returns immediately
    name,
    data
);

// Poll for completion
while (!operation.HasCompleted)
{
    await Task.Delay(TimeSpan.FromSeconds(5));
    await operation.UpdateStatusAsync();
}
```

### 检查预配状态

```csharp
var org = await organizations.GetAsync("my-org");
if (org.Value.Data.Properties?.ProvisioningState == 
    MongoDBAtlasResourceProvisioningState.Succeeded)
{
    Console.WriteLine("Organization is ready");
}
```

### 使用资源标识符

```csharp
// Create identifier without API call
var resourceId = MongoDBAtlasOrganizationResource.CreateResourceIdentifier(
    subscriptionId,
    resourceGroupName,
    organizationName
);

// Get resource handle (no data yet)
var orgResource = armClient.GetMongoDBAtlasOrganizationResource(resourceId);

// Fetch data when needed
var response = await orgResource.GetAsync();
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ResourceNotFound` | 组织不存在 | 验证名称和资源组 |
| `AuthorizationFailed` | 权限不足 | 检查资源组上的 RBAC 角色 |
| `InvalidParameter` | 缺少必填属性 | 确保所有必填字段已设置 |
| `MarketplaceError` | Marketplace 订阅问题 | 验证产品/服务详情和订阅 |

## 相关资源

- [Microsoft Learn: MongoDB Atlas on Azure](https://learn.microsoft.com/en-us/azure/partner-solutions/mongodb-atlas/)
- [API Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.mongodbatlas)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/mongodbatlas)

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
