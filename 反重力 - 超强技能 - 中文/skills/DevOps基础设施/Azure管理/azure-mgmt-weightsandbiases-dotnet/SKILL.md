---
name: azure-mgmt-weightsandbiases-dotnet
description: Azure Weights & Biases .NET SDK。通过 Azure Marketplace 进行 ML 实验追踪和模型管理。当用户要求'创建 W&B 实例、管理 SSO、Marketplace 集成、ML 可观测性'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.WeightsAndBiases (.NET)

Azure Resource Manager SDK，用于通过 Azure Marketplace 部署和管理 Weights & Biases ML 实验追踪实例。

## 安装

```bash
dotnet add package Azure.ResourceManager.WeightsAndBiases --prerelease
dotnet add package Azure.Identity
```

**当前版本**：v1.0.0-beta.1 (preview)
**API 版本**：2024-09-18-preview

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_WANDB_INSTANCE_NAME=<your-wandb-instance>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.WeightsAndBiases;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## 资源层级

```
Subscription
└── ResourceGroup
    └── WeightsAndBiasesInstance    # 来自 Azure Marketplace 的 W&B 部署
        ├── Properties
        │   ├── Marketplace          # 套餐详情、计划、发布者
        │   ├── User                 # 管理员用户信息
        │   ├── PartnerProperties    # W&B 特定配置（区域、子域）
        │   └── SingleSignOnPropertiesV2  # Entra ID SSO 配置
        └── Identity                 # 托管标识（可选）
```

## 核心工作流

### 1. 创建 Weights & Biases 实例

```csharp
using Azure.ResourceManager.WeightsAndBiases;
using Azure.ResourceManager.WeightsAndBiases.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

WeightsAndBiasesInstanceCollection instances = resourceGroup.GetWeightsAndBiasesInstances();

WeightsAndBiasesInstanceData data = new WeightsAndBiasesInstanceData(AzureLocation.EastUS)
{
    Properties = new WeightsAndBiasesInstanceProperties
    {
        // Marketplace configuration
        Marketplace = new WeightsAndBiasesMarketplaceDetails
        {
            SubscriptionId = "<marketplace-subscription-id>",
            OfferDetails = new WeightsAndBiasesOfferDetails
            {
                PublisherId = "wandb",
                OfferId = "wandb-pay-as-you-go",
                PlanId = "wandb-payg",
                PlanName = "Pay As You Go",
                TermId = "monthly",
                TermUnit = "P1M"
            }
        },
        // Admin user
        User = new WeightsAndBiasesUserDetails
        {
            FirstName = "Admin",
            LastName = "User",
            EmailAddress = "admin@example.com",
            Upn = "admin@example.com"
        },
        // W&B-specific configuration
        PartnerProperties = new WeightsAndBiasesPartnerProperties
        {
            Region = WeightsAndBiasesRegion.EastUS,
            Subdomain = "my-company-wandb"
        }
    },
    // Optional: Enable managed identity
    Identity = new ManagedServiceIdentity(ManagedServiceIdentityType.SystemAssigned)
};

ArmOperation<WeightsAndBiasesInstanceResource> operation = await instances
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb-instance", data);

WeightsAndBiasesInstanceResource instance = operation.Value;

Console.WriteLine($"W&B Instance created: {instance.Data.Name}");
Console.WriteLine($"Provisioning state: {instance.Data.Properties.ProvisioningState}");
```

### 2. 获取现有实例

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

Console.WriteLine($"Instance: {instance.Data.Name}");
Console.WriteLine($"Location: {instance.Data.Location}");
Console.WriteLine($"State: {instance.Data.Properties.ProvisioningState}");

if (instance.Data.Properties.PartnerProperties != null)
{
    Console.WriteLine($"Region: {instance.Data.Properties.PartnerProperties.Region}");
    Console.WriteLine($"Subdomain: {instance.Data.Properties.PartnerProperties.Subdomain}");
}
```

### 3. 列出所有实例

```csharp
// List in resource group
await foreach (WeightsAndBiasesInstanceResource instance in 
    resourceGroup.GetWeightsAndBiasesInstances())
{
    Console.WriteLine($"Instance: {instance.Data.Name}");
    Console.WriteLine($"  Location: {instance.Data.Location}");
    Console.WriteLine($"  State: {instance.Data.Properties.ProvisioningState}");
}

// List in subscription
SubscriptionResource subscription = await client.GetDefaultSubscriptionAsync();
await foreach (WeightsAndBiasesInstanceResource instance in 
    subscription.GetWeightsAndBiasesInstancesAsync())
{
    Console.WriteLine($"{instance.Data.Name} in {instance.Id.ResourceGroupName}");
}
```

### 4. 配置单点登录 (SSO)

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

// Update with SSO configuration
WeightsAndBiasesInstanceData updateData = instance.Data;

updateData.Properties.SingleSignOnPropertiesV2 = new WeightsAndBiasSingleSignOnPropertiesV2
{
    Type = WeightsAndBiasSingleSignOnType.Saml,
    State = WeightsAndBiasSingleSignOnState.Enable,
    EnterpriseAppId = "<entra-app-id>",
    AadDomains = { "example.com", "contoso.com" }
};

ArmOperation<WeightsAndBiasesInstanceResource> operation = await resourceGroup
    .GetWeightsAndBiasesInstances()
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb-instance", updateData);
```

### 5. 更新实例

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

// Update tags
WeightsAndBiasesInstancePatch patch = new WeightsAndBiasesInstancePatch
{
    Tags =
    {
        { "environment", "production" },
        { "team", "ml-platform" },
        { "costCenter", "CC-ML-001" }
    }
};

instance = await instance.UpdateAsync(patch);
Console.WriteLine($"Updated instance: {instance.Data.Name}");
```

### 6. 删除实例

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

await instance.DeleteAsync(WaitUntil.Completed);
Console.WriteLine("Instance deleted");
```

### 7. 检查资源名称可用性

```csharp
// Check if name is available before creating
// (Implement via direct ARM call if SDK doesn't expose this)
try
{
    await resourceGroup.GetWeightsAndBiasesInstanceAsync("desired-name");
    Console.WriteLine("Name is already taken");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Name is available");
}
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `WeightsAndBiasesInstanceResource` | W&B 实例资源 |
| `WeightsAndBiasesInstanceData` | 实例配置数据 |
| `WeightsAndBiasesInstanceCollection` | 实例集合 |
| `WeightsAndBiasesInstanceProperties` | 实例属性 |
| `WeightsAndBiasesMarketplaceDetails` | Marketplace 订阅信息 |
| `WeightsAndBiasesOfferDetails` | Marketplace 套餐详情 |
| `WeightsAndBiasesUserDetails` | 管理员用户信息 |
| `WeightsAndBiasesPartnerProperties` | W&B 特定配置 |
| `WeightsAndBiasSingleSignOnPropertiesV2` | SSO 配置 |
| `WeightsAndBiasesInstancePatch` | 更新补丁 |
| `WeightsAndBiasesRegion` | 支持的区域枚举 |

## 可用区域

| 区域枚举 | Azure 区域 |
|----------|-----------|
| `WeightsAndBiasesRegion.EastUS` | 美国东部 |
| `WeightsAndBiasesRegion.CentralUS` | 美国中部 |
| `WeightsAndBiasesRegion.WestUS` | 美国西部 |
| `WeightsAndBiasesRegion.WestEurope` | 西欧 |
| `WeightsAndBiasesRegion.JapanEast` | 日本东部 |
| `WeightsAndBiasesRegion.KoreaCentral` | 韩国中部 |

## Marketplace 套餐详情

用于 Azure Marketplace 集成：

| 属性 | 值 |
|------|-----|
| Publisher ID | `wandb` |
| Offer ID | `wandb-pay-as-you-go` |
| Plan ID | `wandb-payg` (按量付费) |

## 最佳实践

1. **使用 DefaultAzureCredential** — 自动支持多种身份验证方式
2. **启用托管标识** — 用于安全访问其他 Azure 资源
3. **配置 SSO** — 启用 Entra ID SSO 以实现企业级安全
4. **标记资源** — 使用标签进行成本追踪和组织管理
5. **检查预配状态** — 在使用实例前等待状态变为 `Succeeded`
6. **选择合适的区域** — 选择最靠近计算资源的区域
7. **使用 Azure 监控** — 使用 Azure Monitor 监控资源健康状态

## 错误处理

```csharp
using Azure;

try
{
    ArmOperation<WeightsAndBiasesInstanceResource> operation = await instances
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Instance already exists or name conflict");
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

## 与 W&B SDK 集成

创建 Azure 资源后，使用 W&B Python SDK 进行实验追踪：

```python
# Install: pip install wandb
import wandb

# Login with your W&B API key from the Azure-deployed instance
wandb.login(host="https://my-company-wandb.wandb.ai")

# Initialize a run
run = wandb.init(project="my-ml-project")

# Log metrics
wandb.log({"accuracy": 0.95, "loss": 0.05})

# Finish run
run.finish()
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.WeightsAndBiases` | W&B 实例管理（本 SDK） | `dotnet add package Azure.ResourceManager.WeightsAndBiases --prerelease` |
| `Azure.ResourceManager.MachineLearning` | Azure ML 工作区 | `dotnet add package Azure.ResourceManager.MachineLearning` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.WeightsAndBiases |
| W&B 文档 | https://docs.wandb.ai/ |
| Azure Marketplace | https://azuremarketplace.microsoft.com/marketplace/apps/wandb.wandb-pay-as-you-go |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/weightsandbiases |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
