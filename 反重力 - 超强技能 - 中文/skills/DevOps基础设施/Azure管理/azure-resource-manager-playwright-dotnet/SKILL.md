---
name: azure-resource-manager-playwright-dotnet
description: Azure Resource Manager SDK for Microsoft Playwright Testing in .NET 的管理平面 SDK。当用户要求'管理 Playwright Testing 工作空间、配置配额、检查名称可用性'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.Playwright (.NET)

通过 Azure Resource Manager 预配和管理 Microsoft Playwright Testing 工作空间的管理平面 SDK。

> **⚠️ 管理平面 vs 测试执行**
> - **本 SDK (Azure.ResourceManager.Playwright)**：创建工作空间、管理配额、检查名称可用性
> - **测试执行 SDK (Azure.Developer.MicrosoftPlaywrightTesting.NUnit)**：在云端浏览器上大规模运行 Playwright 测试

## 安装

```bash
dotnet add package Azure.ResourceManager.Playwright
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.0.0，预览版 v1.0.0-beta.1

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
using Azure.ResourceManager.Playwright;

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
    ├── PlaywrightQuotaResource (subscription-level quotas)
    └── ResourceGroupResource
        └── PlaywrightWorkspaceResource
            └── PlaywrightWorkspaceQuotaResource (workspace-level quotas)
```

## 核心工作流

### 1. 创建 Playwright 工作空间

```csharp
using Azure.ResourceManager.Playwright;
using Azure.ResourceManager.Playwright.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define workspace
var workspaceData = new PlaywrightWorkspaceData(AzureLocation.WestUS3)
{
    // Optional: Configure regional affinity and local auth
    RegionalAffinity = PlaywrightRegionalAffinity.Enabled,
    LocalAuth = PlaywrightLocalAuth.Enabled,
    Tags =
    {
        ["Team"] = "Dev Exp",
        ["Environment"] = "Production"
    }
};

// Create workspace (long-running operation)
var workspaceCollection = resourceGroup.Value.GetPlaywrightWorkspaces();
var operation = await workspaceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-playwright-workspace",
    workspaceData);

PlaywrightWorkspaceResource workspace = operation.Value;

// Get the data plane URI for running tests
Console.WriteLine($"Data Plane URI: {workspace.Data.DataplaneUri}");
Console.WriteLine($"Workspace ID: {workspace.Data.WorkspaceId}");
```

### 2. 获取现有工作空间

```csharp
// Get by name
var workspace = await workspaceCollection.GetAsync("my-playwright-workspace");

// Or check if exists first
bool exists = await workspaceCollection.ExistsAsync("my-playwright-workspace");
if (exists)
{
    var existingWorkspace = await workspaceCollection.GetAsync("my-playwright-workspace");
    Console.WriteLine($"Workspace found: {existingWorkspace.Value.Data.Name}");
}
```

### 3. 列出工作空间

```csharp
// List in resource group
await foreach (var workspace in workspaceCollection.GetAllAsync())
{
    Console.WriteLine($"Workspace: {workspace.Data.Name}");
    Console.WriteLine($"  Location: {workspace.Data.Location}");
    Console.WriteLine($"  State: {workspace.Data.ProvisioningState}");
    Console.WriteLine($"  Data Plane URI: {workspace.Data.DataplaneUri}");
}

// List across subscription
await foreach (var workspace in subscription.GetPlaywrightWorkspacesAsync())
{
    Console.WriteLine($"Workspace: {workspace.Data.Name}");
}
```

### 4. 更新工作空间

```csharp
var patch = new PlaywrightWorkspacePatch
{
    Tags =
    {
        ["Team"] = "Dev Exp",
        ["Environment"] = "Staging",
        ["UpdatedAt"] = DateTime.UtcNow.ToString("o")
    }
};

var updatedWorkspace = await workspace.Value.UpdateAsync(patch);
```

### 5. 检查名称可用性

```csharp
using Azure.ResourceManager.Playwright.Models;

var checkRequest = new PlaywrightCheckNameAvailabilityContent
{
    Name = "my-new-workspace",
    ResourceType = "Microsoft.LoadTestService/playwrightWorkspaces"
};

var result = await subscription.CheckPlaywrightNameAvailabilityAsync(checkRequest);

if (result.Value.IsNameAvailable == true)
{
    Console.WriteLine("Name is available!");
}
else
{
    Console.WriteLine($"Name unavailable: {result.Value.Message}");
    Console.WriteLine($"Reason: {result.Value.Reason}");
}
```

### 6. 获取配额信息

```csharp
// Subscription-level quotas
await foreach (var quota in subscription.GetPlaywrightQuotasAsync(AzureLocation.WestUS3))
{
    Console.WriteLine($"Quota: {quota.Data.Name}");
    Console.WriteLine($"  Limit: {quota.Data.Limit}");
    Console.WriteLine($"  Used: {quota.Data.Used}");
}

// Workspace-level quotas
var workspaceQuotas = workspace.Value.GetAllPlaywrightWorkspaceQuota();
await foreach (var quota in workspaceQuotas.GetAllAsync())
{
    Console.WriteLine($"Workspace Quota: {quota.Data.Name}");
}
```

### 7. 删除工作空间

```csharp
// Delete (long-running operation)
await workspace.Value.DeleteAsync(WaitUntil.Completed);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `PlaywrightWorkspaceResource` | 表示一个 Playwright Testing 工作空间 |
| `PlaywrightWorkspaceCollection` | 工作空间 CRUD 集合 |
| `PlaywrightWorkspaceData` | 工作空间创建/响应负载 |
| `PlaywrightWorkspacePatch` | 工作空间更新负载 |
| `PlaywrightQuotaResource` | 订阅级配额信息 |
| `PlaywrightWorkspaceQuotaResource` | 工作空间级配额信息 |
| `PlaywrightExtensions` | ARM 资源的扩展方法 |
| `PlaywrightCheckNameAvailabilityContent` | 名称可用性检查请求 |

## 工作空间属性

| 属性 | 描述 |
|----------|-------------|
| `DataplaneUri` | 用于运行测试的 URI（例如 `https://api.dataplane.{guid}.domain.com`） |
| `WorkspaceId` | 唯一工作空间标识符（GUID） |
| `RegionalAffinity` | 启用/禁用测试执行的区域亲和性 |
| `LocalAuth` | 启用/禁用本地身份验证（访问令牌） |
| `ProvisioningState` | 当前预配状态（Succeeded、Failed 等） |

## 最佳实践

1. **使用 `WaitUntil.Completed`** 用于必须在继续之前完成的操作
2. **使用 `WaitUntil.Started`** 当你想手动轮询或并行运行操作时
3. **始终使用 `DefaultAzureCredential`** — 不要硬编码密钥
4. **处理 `RequestFailedException`** 用于 ARM API 错误
5. **使用 `CreateOrUpdateAsync`** 用于幂等操作
6. **通过 `Get*` 方法导航层级**（例如 `resourceGroup.GetPlaywrightWorkspaces()`）
7. **创建工作空间后存储 DataplaneUri**，用于测试执行配置

## 错误处理

```csharp
using Azure;

try
{
    var operation = await workspaceCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, workspaceName, workspaceData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Workspace already exists");
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

## 与测试执行的集成

创建工作空间后，使用 `DataplaneUri` 配置你的 Playwright 测试：

```csharp
// 1. Create workspace (this SDK)
var workspace = await workspaceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, "my-workspace", workspaceData);

// 2. Get the service URL
var serviceUrl = workspace.Value.Data.DataplaneUri;

// 3. Set environment variable for test execution
Environment.SetEnvironmentVariable("PLAYWRIGHT_SERVICE_URL", serviceUrl.ToString());

// 4. Run tests using Azure.Developer.MicrosoftPlaywrightTesting.NUnit
// (separate package for test execution)
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|---------|---------|
| `Azure.ResourceManager.Playwright` | 管理平面（本 SDK） | `dotnet add package Azure.ResourceManager.Playwright` |
| `Azure.Developer.MicrosoftPlaywrightTesting.NUnit` | 大规模运行 NUnit Playwright 测试 | `dotnet add package Azure.Developer.MicrosoftPlaywrightTesting.NUnit --prerelease` |
| `Azure.Developer.Playwright` | Playwright 客户端库 | `dotnet add package Azure.Developer.Playwright` |

## API 信息

- **资源提供程序**：`Microsoft.LoadTestService`
- **默认 API 版本**：`2025-09-01`
- **资源类型**：`Microsoft.LoadTestService/playwrightWorkspaces`

## 文档链接

- [Azure.ResourceManager.Playwright API Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.playwright)
- [Microsoft Playwright Testing Overview](https://learn.microsoft.com/en-us/azure/playwright-testing/overview-what-is-microsoft-playwright-testing)
- [Quickstart: Run Playwright Tests at Scale](https://learn.microsoft.com/en-us/azure/playwright-testing/quickstart-run-end-to-end-tests)

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
