---
name: azure-mgmt-applicationinsights-dotnet
description: Azure Application Insights .NET SDK。应用程序性能监控和可观测性资源管理。当用户要求'管理 Azure Application Insights 资源'、'配置应用性能监控'、'创建 Application Insights 组件'、'管理 Web 测试和工作簿'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.ApplicationInsights (.NET)

用于管理 Application Insights 资源的 Azure Resource Manager SDK，实现应用程序性能监控。

## 安装

```bash
dotnet add package Azure.ResourceManager.ApplicationInsights
dotnet add package Azure.Identity
```

**当前版本**：v1.0.0 (GA)
**API 版本**：2022-06-15

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_APPINSIGHTS_NAME=<your-appinsights-component>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ApplicationInsights;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## 资源层级

```
Subscription
└── ResourceGroup
    └── ApplicationInsightsComponent          # App Insights 资源
        ├── ApplicationInsightsComponentApiKey  # 编程访问的 API 密钥
        ├── ComponentLinkedStorageAccount      # 数据导出的关联存储
        └── (via component ID)
            ├── WebTest                        # 可用性测试
            ├── Workbook                       # 分析工作簿
            ├── WorkbookTemplate               # 工作簿模板
            └── MyWorkbook                     # 私有工作簿
```

## 核心工作流

### 1. 创建 Application Insights 组件（基于工作区）

```csharp
using Azure.ResourceManager.ApplicationInsights;
using Azure.ResourceManager.ApplicationInsights.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

ApplicationInsightsComponentCollection components = resourceGroup.GetApplicationInsightsComponents();

// Workspace-based Application Insights (recommended)
ApplicationInsightsComponentData data = new ApplicationInsightsComponentData(
    AzureLocation.EastUS,
    ApplicationInsightsApplicationType.Web)
{
    Kind = "web",
    WorkspaceResourceId = new ResourceIdentifier(
        "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>"),
    IngestionMode = IngestionMode.LogAnalytics,
    PublicNetworkAccessForIngestion = PublicNetworkAccessType.Enabled,
    PublicNetworkAccessForQuery = PublicNetworkAccessType.Enabled,
    RetentionInDays = 90,
    SamplingPercentage = 100,
    DisableIPMasking = false,
    ImmediatePurgeDataOn30Days = false,
    Tags =
    {
        { "environment", "production" },
        { "application", "mywebapp" }
    }
};

ArmOperation<ApplicationInsightsComponentResource> operation = await components
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", data);

ApplicationInsightsComponentResource component = operation.Value;

Console.WriteLine($"Component created: {component.Data.Name}");
Console.WriteLine($"Instrumentation Key: {component.Data.InstrumentationKey}");
Console.WriteLine($"Connection String: {component.Data.ConnectionString}");
```

### 2. 获取连接字符串和密钥

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

// Get connection string for SDK configuration
string connectionString = component.Data.ConnectionString;
string instrumentationKey = component.Data.InstrumentationKey;
string appId = component.Data.AppId;

Console.WriteLine($"Connection String: {connectionString}");
Console.WriteLine($"Instrumentation Key: {instrumentationKey}");
Console.WriteLine($"App ID: {appId}");
```

### 3. 创建 API 密钥

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

ApplicationInsightsComponentApiKeyCollection apiKeys = component.GetApplicationInsightsComponentApiKeys();

// API key for reading telemetry
ApplicationInsightsApiKeyContent keyContent = new ApplicationInsightsApiKeyContent
{
    Name = "ReadTelemetryKey",
    LinkedReadProperties =
    {
        $"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/{component.Data.Name}/api",
        $"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/{component.Data.Name}/agentconfig"
    }
};

ApplicationInsightsComponentApiKeyResource apiKey = await apiKeys
    .CreateOrUpdateAsync(WaitUntil.Completed, keyContent);

Console.WriteLine($"API Key Name: {apiKey.Data.Name}");
Console.WriteLine($"API Key: {apiKey.Data.ApiKey}"); // Only shown once!
```

### 4. 创建 Web 测试（可用性测试）

```csharp
WebTestCollection webTests = resourceGroup.GetWebTests();

// URL Ping Test
WebTestData urlPingTest = new WebTestData(AzureLocation.EastUS)
{
    Kind = WebTestKind.Ping,
    SyntheticMonitorId = "webtest-ping-myapp",
    WebTestName = "Homepage Availability",
    Description = "Checks if homepage is available",
    IsEnabled = true,
    Frequency = 300, // 5 minutes
    Timeout = 120,   // 2 minutes
    WebTestKind = WebTestKind.Ping,
    IsRetryEnabled = true,
    Locations =
    {
        new WebTestGeolocation { WebTestLocationId = "us-ca-sjc-azr" },  // West US
        new WebTestGeolocation { WebTestLocationId = "us-tx-sn1-azr" },  // South Central US
        new WebTestGeolocation { WebTestLocationId = "us-il-ch1-azr" },  // North Central US
        new WebTestGeolocation { WebTestLocationId = "emea-gb-db3-azr" }, // UK South
        new WebTestGeolocation { WebTestLocationId = "apac-sg-sin-azr" }  // Southeast Asia
    },
    Configuration = new WebTestConfiguration
    {
        WebTest = """
            <WebTest Name="Homepage" Enabled="True" Timeout="120" 
                     xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010">
                <Items>
                    <Request Method="GET" Version="1.1" Url="https://myapp.example.com" 
                             ThinkTime="0" Timeout="120" ParseDependentRequests="False" 
                             FollowRedirects="True" RecordResult="True" Cache="False" 
                             ResponseTimeGoal="0" Encoding="utf-8" ExpectedHttpStatusCode="200" />
                </Items>
            </WebTest>
        """
    },
    Tags =
    {
        { $"hidden-link:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/my-appinsights", "Resource" }
    }
};

ArmOperation<WebTestResource> operation = await webTests
    .CreateOrUpdateAsync(WaitUntil.Completed, "webtest-homepage", urlPingTest);

WebTestResource webTest = operation.Value;
Console.WriteLine($"Web test created: {webTest.Data.Name}");
```

### 5. 创建多步骤 Web 测试

```csharp
WebTestData multiStepTest = new WebTestData(AzureLocation.EastUS)
{
    Kind = WebTestKind.MultiStep,
    SyntheticMonitorId = "webtest-multistep-login",
    WebTestName = "Login Flow Test",
    Description = "Tests login functionality",
    IsEnabled = true,
    Frequency = 900, // 15 minutes
    Timeout = 300,   // 5 minutes
    WebTestKind = WebTestKind.MultiStep,
    IsRetryEnabled = true,
    Locations =
    {
        new WebTestGeolocation { WebTestLocationId = "us-ca-sjc-azr" }
    },
    Configuration = new WebTestConfiguration
    {
        WebTest = """
            <WebTest Name="LoginFlow" Enabled="True" Timeout="300"
                     xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010">
                <Items>
                    <Request Method="GET" Version="1.1" Url="https://myapp.example.com/login" 
                             ThinkTime="0" Timeout="60" />
                    <Request Method="POST" Version="1.1" Url="https://myapp.example.com/api/auth" 
                             ThinkTime="0" Timeout="60">
                        <Headers>
                            <Header Name="Content-Type" Value="application/json" />
                        </Headers>
                        <Body>{"username":"testuser","password":"{{TestPassword}}"}</Body>
                    </Request>
                </Items>
            </WebTest>
        """
    },
    Tags =
    {
        { $"hidden-link:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/my-appinsights", "Resource" }
    }
};

await webTests.CreateOrUpdateAsync(WaitUntil.Completed, "webtest-login-flow", multiStepTest);
```

### 6. 创建工作簿

```csharp
WorkbookCollection workbooks = resourceGroup.GetWorkbooks();

WorkbookData workbookData = new WorkbookData(AzureLocation.EastUS)
{
    DisplayName = "Application Performance Dashboard",
    Category = "workbook",
    Kind = WorkbookSharedTypeKind.Shared,
    SerializedData = """
    {
        "version": "Notebook/1.0",
        "items": [
            {
                "type": 1,
                "content": {
                    "json": "# Application Performance\n\nThis workbook shows application performance metrics."
                },
                "name": "header"
            },
            {
                "type": 3,
                "content": {
                    "version": "KqlItem/1.0",
                    "query": "requests\n| summarize count() by bin(timestamp, 1h)\n| render timechart",
                    "size": 0,
                    "title": "Requests per Hour",
                    "timeContext": {
                        "durationMs": 86400000
                    },
                    "queryType": 0,
                    "resourceType": "microsoft.insights/components"
                },
                "name": "requestsChart"
            }
        ],
        "isLocked": false
    }
    """,
    SourceId = component.Id,
    Tags =
    {
        { "environment", "production" }
    }
};

// Note: Workbook ID should be a new GUID
string workbookId = Guid.NewGuid().ToString();

ArmOperation<WorkbookResource> operation = await workbooks
    .CreateOrUpdateAsync(WaitUntil.Completed, workbookId, workbookData);

WorkbookResource workbook = operation.Value;
Console.WriteLine($"Workbook created: {workbook.Data.DisplayName}");
```

### 7. 关联存储账户

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

ComponentLinkedStorageAccountCollection linkedStorage = component.GetComponentLinkedStorageAccounts();

ComponentLinkedStorageAccountData storageData = new ComponentLinkedStorageAccountData
{
    LinkedStorageAccount = new ResourceIdentifier(
        "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>")
};

ArmOperation<ComponentLinkedStorageAccountResource> operation = await linkedStorage
    .CreateOrUpdateAsync(WaitUntil.Completed, StorageType.ServiceProfiler, storageData);
```

### 8. 列出和管理组件

```csharp
// List all Application Insights components in resource group
await foreach (ApplicationInsightsComponentResource component in 
    resourceGroup.GetApplicationInsightsComponents())
{
    Console.WriteLine($"Component: {component.Data.Name}");
    Console.WriteLine($"  App ID: {component.Data.AppId}");
    Console.WriteLine($"  Type: {component.Data.ApplicationType}");
    Console.WriteLine($"  Ingestion Mode: {component.Data.IngestionMode}");
    Console.WriteLine($"  Retention: {component.Data.RetentionInDays} days");
}

// List web tests
await foreach (WebTestResource webTest in resourceGroup.GetWebTests())
{
    Console.WriteLine($"Web Test: {webTest.Data.WebTestName}");
    Console.WriteLine($"  Enabled: {webTest.Data.IsEnabled}");
    Console.WriteLine($"  Frequency: {webTest.Data.Frequency}s");
}

// List workbooks
await foreach (WorkbookResource workbook in resourceGroup.GetWorkbooks())
{
    Console.WriteLine($"Workbook: {workbook.Data.DisplayName}");
}
```

### 9. 更新组件

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

// Update using full data (PUT operation)
ApplicationInsightsComponentData updateData = component.Data;
updateData.RetentionInDays = 180;
updateData.SamplingPercentage = 50;
updateData.Tags["updated"] = "true";

ArmOperation<ApplicationInsightsComponentResource> operation = await resourceGroup
    .GetApplicationInsightsComponents()
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", updateData);
```

### 10. 删除资源

```csharp
// Delete Application Insights component
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");
await component.DeleteAsync(WaitUntil.Completed);

// Delete web test
WebTestResource webTest = await resourceGroup.GetWebTestAsync("webtest-homepage");
await webTest.DeleteAsync(WaitUntil.Completed);
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ApplicationInsightsComponentResource` | App Insights 组件 |
| `ApplicationInsightsComponentData` | 组件配置 |
| `ApplicationInsightsComponentCollection` | 组件集合 |
| `ApplicationInsightsComponentApiKeyResource` | 编程访问的 API 密钥 |
| `WebTestResource` | 可用性/Web 测试 |
| `WebTestData` | Web 测试配置 |
| `WorkbookResource` | 分析工作簿 |
| `WorkbookData` | 工作簿配置 |
| `ComponentLinkedStorageAccountResource` | 导出的关联存储 |

## 应用程序类型

| 类型 | 枚举值 |
|------|--------|
| Web 应用程序 | `Web` |
| iOS 应用程序 | `iOS` |
| Java 应用程序 | `Java` |
| Node.js 应用程序 | `NodeJS` |
| .NET 应用程序 | `MRT` |
| 其他 | `Other` |

## Web 测试位置

| 位置 ID | 区域 |
|---------|------|
| `us-ca-sjc-azr` | 美国西部 |
| `us-tx-sn1-azr` | 美国中南部 |
| `us-il-ch1-azr` | 美国中北部 |
| `us-va-ash-azr` | 美国东部 |
| `emea-gb-db3-azr` | 英国南部 |
| `emea-nl-ams-azr` | 西欧 |
| `emea-fr-pra-edge` | 法国中部 |
| `apac-sg-sin-azr` | 东南亚 |
| `apac-hk-hkn-azr` | 东亚 |
| `apac-jp-kaw-edge` | 日本东部 |
| `latam-br-gru-edge` | 巴西南部 |
| `emea-au-syd-edge` | 澳大利亚东部 |

## 最佳实践

1. **使用基于工作区的部署** — 基于工作区的 App Insights 是当前标准
2. **关联 Log Analytics** — 将数据存储在 Log Analytics 中以获得更好的查询能力
3. **设置适当的保留期** — 平衡成本与数据可用性
4. **使用采样** — 为高流量应用降低成本
5. **安全存储连接字符串** — 使用 Key Vault 或托管标识
6. **启用多个测试位置** — 以获得准确的可用性监控
7. **使用工作簿** — 用于自定义仪表盘和分析
8. **设置告警** — 基于可用性测试和指标
9. **标记资源** — 用于成本分配和组织管理
10. **使用私有端点** — 用于安全的数据摄取

## 错误处理

```csharp
using Azure;

try
{
    ArmOperation<ApplicationInsightsComponentResource> operation = await components
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Component already exists");
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

## SDK 集成

将连接字符串与 Application Insights SDK 配合使用：

```csharp
// Program.cs in ASP.NET Core
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = configuration["ApplicationInsights:ConnectionString"];
});

// Or set via environment variable
// APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.ApplicationInsights` | 资源管理（本 SDK） | `dotnet add package Azure.ResourceManager.ApplicationInsights` |
| `Microsoft.ApplicationInsights` | 遥测 SDK | `dotnet add package Microsoft.ApplicationInsights` |
| `Microsoft.ApplicationInsights.AspNetCore` | ASP.NET Core 集成 | `dotnet add package Microsoft.ApplicationInsights.AspNetCore` |
| `Azure.Monitor.OpenTelemetry.Exporter` | OpenTelemetry 导出 | `dotnet add package Azure.Monitor.OpenTelemetry.Exporter` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.ApplicationInsights |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.applicationinsights |
| 产品文档 | https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/applicationinsights/Azure.ResourceManager.ApplicationInsights |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
