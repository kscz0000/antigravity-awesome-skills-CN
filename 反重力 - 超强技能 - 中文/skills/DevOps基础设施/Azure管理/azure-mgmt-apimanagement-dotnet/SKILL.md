---
name: azure-mgmt-apimanagement-dotnet
description: Azure Resource Manager SDK for API Management in .NET. 当用户要求'管理 Azure API Management 资源'、'创建 APIM 服务/API/产品/订阅/策略'、'使用 .NET SDK 管理 API Management'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.ApiManagement (.NET)

管理平面 SDK，用于通过 Azure Resource Manager 预配和管理 Azure API Management 资源。

> **⚠️ 管理平面 vs 数据平面**
> - **本 SDK (Azure.ResourceManager.ApiManagement)**：创建服务、API、产品、订阅、策略、用户、组
> - **数据平面**：直接调用 APIM 网关端点的 API

## 安装

```bash
dotnet add package Azure.ResourceManager.ApiManagement
dotnet add package Azure.Identity
```

**当前版本**：v1.3.0

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
using Azure.ResourceManager.ApiManagement;

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
        └── ApiManagementServiceResource
            ├── ApiResource
            │   ├── ApiOperationResource
            │   │   └── ApiOperationPolicyResource
            │   ├── ApiPolicyResource
            │   ├── ApiSchemaResource
            │   └── ApiDiagnosticResource
            ├── ApiManagementProductResource
            │   ├── ProductApiResource
            │   ├── ProductGroupResource
            │   └── ProductPolicyResource
            ├── ApiManagementSubscriptionResource
            ├── ApiManagementPolicyResource
            ├── ApiManagementUserResource
            ├── ApiManagementGroupResource
            ├── ApiManagementBackendResource
            ├── ApiManagementGatewayResource
            ├── ApiManagementCertificateResource
            ├── ApiManagementNamedValueResource
            └── ApiManagementLoggerResource
```

## 核心工作流

### 1. 创建 API Management 服务

```csharp
using Azure.ResourceManager.ApiManagement;
using Azure.ResourceManager.ApiManagement.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define service
var serviceData = new ApiManagementServiceData(
    location: AzureLocation.EastUS,
    sku: new ApiManagementServiceSkuProperties(
        ApiManagementServiceSkuType.Developer, 
        capacity: 1),
    publisherEmail: "admin@contoso.com",
    publisherName: "Contoso");

// Create service (long-running operation - can take 30+ minutes)
var serviceCollection = resourceGroup.Value.GetApiManagementServices();
var operation = await serviceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-apim-service",
    serviceData);

ApiManagementServiceResource service = operation.Value;
```

### 2. 创建 API

```csharp
var apiData = new ApiCreateOrUpdateContent
{
    DisplayName = "My API",
    Path = "myapi",
    Protocols = { ApiOperationInvokableProtocol.Https },
    ServiceUri = new Uri("https://backend.contoso.com/api")
};

var apiCollection = service.GetApis();
var apiOperation = await apiCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-api",
    apiData);

ApiResource api = apiOperation.Value;
```

### 3. 创建产品

```csharp
var productData = new ApiManagementProductData
{
    DisplayName = "Starter",
    Description = "Starter tier with limited access",
    IsSubscriptionRequired = true,
    IsApprovalRequired = false,
    SubscriptionsLimit = 1,
    State = ApiManagementProductState.Published
};

var productCollection = service.GetApiManagementProducts();
var productOperation = await productCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "starter",
    productData);

ApiManagementProductResource product = productOperation.Value;

// Add API to product
await product.GetProductApis().CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-api");
```

### 4. 创建订阅

```csharp
var subscriptionData = new ApiManagementSubscriptionCreateOrUpdateContent
{
    DisplayName = "My Subscription",
    Scope = $"/products/{product.Data.Name}",
    State = ApiManagementSubscriptionState.Active
};

var subscriptionCollection = service.GetApiManagementSubscriptions();
var subOperation = await subscriptionCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-subscription",
    subscriptionData);

ApiManagementSubscriptionResource subscription = subOperation.Value;

// Get subscription keys
var keys = await subscription.GetSecretsAsync();
Console.WriteLine($"Primary Key: {keys.Value.PrimaryKey}");
```

### 5. 设置 API 策略

```csharp
var policyXml = @"
<policies>
    <inbound>
        <rate-limit calls=""100"" renewal-period=""60"" />
        <set-header name=""X-Custom-Header"" exists-action=""override"">
            <value>CustomValue</value>
        </set-header>
        <base />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>";

var policyData = new PolicyContractData
{
    Value = policyXml,
    Format = PolicyContentFormat.Xml
};

await api.GetApiPolicy().CreateOrUpdateAsync(
    WaitUntil.Completed,
    policyData);
```

### 6. 备份与恢复

```csharp
// Backup
var backupParams = new ApiManagementServiceBackupRestoreContent(
    storageAccount: "mystorageaccount",
    containerName: "apim-backups",
    backupName: "backup-2024-01-15")
{
    AccessType = StorageAccountAccessType.SystemAssignedManagedIdentity
};

await service.BackupAsync(WaitUntil.Completed, backupParams);

// Restore
await service.RestoreAsync(WaitUntil.Completed, backupParams);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `ApiManagementServiceResource` | 表示 APIM 服务实例 |
| `ApiManagementServiceCollection` | 服务 CRUD 集合 |
| `ApiResource` | 表示一个 API |
| `ApiManagementProductResource` | 表示一个产品 |
| `ApiManagementSubscriptionResource` | 表示一个订阅 |
| `ApiManagementPolicyResource` | 服务级策略 |
| `ApiPolicyResource` | API 级策略 |
| `ApiManagementUserResource` | 表示一个用户 |
| `ApiManagementGroupResource` | 表示一个组 |
| `ApiManagementBackendResource` | 表示一个后端服务 |
| `ApiManagementGatewayResource` | 表示一个自托管网关 |

## SKU 类型

| SKU | 用途 | 容量 |
|-----|------|------|
| `Developer` | 开发/测试（无 SLA） | 1 |
| `Basic` | 入门级生产 | 1-2 |
| `Standard` | 中等负载 | 1-4 |
| `Premium` | 高可用、多区域 | 每区域 1-12 |
| `Consumption` | 无服务器，按调用付费 | N/A |

## 最佳实践

1. **使用 `WaitUntil.Completed`** 处理必须完成后才能继续的操作
2. **使用 `WaitUntil.Started`** 处理服务创建等长时间操作（30+ 分钟）
3. **始终使用 `DefaultAzureCredential`** — 绝不硬编码密钥
4. **处理 `RequestFailedException`** 以应对 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 实现幂等操作
6. **通过 `Get*` 方法导航层级**（例如 `service.GetApis()`）
7. **策略格式** — 使用 XML 格式定义策略；也支持 JSON
8. **服务创建** — Developer SKU 最适合测试（约 15-30 分钟）

## 错误处理

```csharp
using Azure;

try
{
    var operation = await serviceCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, serviceName, serviceData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Service already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Bad request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 参考文件

| 文件 | 何时阅读 |
|------|----------|
| references/service-management.md | 服务 CRUD、SKU、网络、备份/恢复 |
| references/apis-operations.md | API、操作、Schema、版本管理 |
| references/products-subscriptions.md | 产品、订阅、访问控制 |
| references/policies.md | 策略 XML 模式、作用域、常用策略 |

## 相关资源

| 资源 | 用途 |
|------|------|
| [API Management Documentation](https://learn.microsoft.com/en-us/azure/api-management/) | Azure 官方文档 |
| [Policy Reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies) | 完整策略参考 |
| [SDK Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.apimanagement) | .NET API 参考 |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
