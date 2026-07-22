---
name: azure-mgmt-apicenter-dotnet
description: Azure API Center .NET SDK。集中式 API 清单管理，支持治理、版本控制和发现。当用户要求'Azure API Center .NET 开发'、'API 清单管理'、'API 治理'或'API 版本控制'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.ApiCenter (.NET)

集中式 API 清单和治理 SDK，用于管理组织内的所有 API。

## 安装

```bash
dotnet add package Azure.ResourceManager.ApiCenter
dotnet add package Azure.Identity
```

**当前版本**: v1.0.0 (GA)  
**API 版本**: 2024-03-01

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_APICENTER_SERVICE_NAME=<your-apicenter-service>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ApiCenter;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## 资源层级

```
Subscription
└── ResourceGroup
    └── ApiCenterService                    # API 清单服务
        ├── Workspace                       # API 的逻辑分组
        │   ├── Api                         # API 定义
        │   │   └── ApiVersion              # API 版本
        │   │       └── ApiDefinition       # OpenAPI/GraphQL 等规范
        │   ├── Environment                 # 部署目标（开发/预发布/生产）
        │   └── Deployment                  # API 部署到环境
        └── MetadataSchema                  # 自定义元数据定义
```

## 核心工作流

### 1. 创建 API Center 服务

```csharp
using Azure.ResourceManager.ApiCenter;
using Azure.ResourceManager.ApiCenter.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

ApiCenterServiceCollection services = resourceGroup.GetApiCenterServices();

ApiCenterServiceData data = new ApiCenterServiceData(AzureLocation.EastUS)
{
    Identity = new ManagedServiceIdentity(ManagedServiceIdentityType.SystemAssigned)
};

ArmOperation<ApiCenterServiceResource> operation = await services
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-api-center", data);

ApiCenterServiceResource service = operation.Value;
```

### 2. 创建工作区

```csharp
ApiCenterWorkspaceCollection workspaces = service.GetApiCenterWorkspaces();

ApiCenterWorkspaceData workspaceData = new ApiCenterWorkspaceData
{
    Title = "Engineering APIs",
    Description = "APIs owned by the engineering team"
};

ArmOperation<ApiCenterWorkspaceResource> operation = await workspaces
    .CreateOrUpdateAsync(WaitUntil.Completed, "engineering", workspaceData);

ApiCenterWorkspaceResource workspace = operation.Value;
```

### 3. 创建 API

```csharp
ApiCenterApiCollection apis = workspace.GetApiCenterApis();

ApiCenterApiData apiData = new ApiCenterApiData
{
    Title = "Orders API",
    Description = "API for managing customer orders",
    Kind = ApiKind.Rest,
    LifecycleStage = ApiLifecycleStage.Production,
    TermsOfService = new ApiTermsOfService
    {
        Uri = new Uri("https://example.com/terms")
    },
    ExternalDocumentation = 
    {
        new ApiExternalDocumentation
        {
            Title = "Documentation",
            Uri = new Uri("https://docs.example.com/orders")
        }
    },
    Contacts =
    {
        new ApiContact
        {
            Name = "API Support",
            Email = "api-support@example.com"
        }
    }
};

// Add custom metadata
apiData.CustomProperties = BinaryData.FromObjectAsJson(new
{
    team = "orders-team",
    costCenter = "CC-1234"
});

ArmOperation<ApiCenterApiResource> operation = await apis
    .CreateOrUpdateAsync(WaitUntil.Completed, "orders-api", apiData);

ApiCenterApiResource api = operation.Value;
```

### 4. 创建 API 版本

```csharp
ApiCenterApiVersionCollection versions = api.GetApiCenterApiVersions();

ApiCenterApiVersionData versionData = new ApiCenterApiVersionData
{
    Title = "v1.0.0",
    LifecycleStage = ApiLifecycleStage.Production
};

ArmOperation<ApiCenterApiVersionResource> operation = await versions
    .CreateOrUpdateAsync(WaitUntil.Completed, "v1-0-0", versionData);

ApiCenterApiVersionResource version = operation.Value;
```

### 5. 创建 API 定义（上传 OpenAPI 规范）

```csharp
ApiCenterApiDefinitionCollection definitions = version.GetApiCenterApiDefinitions();

ApiCenterApiDefinitionData definitionData = new ApiCenterApiDefinitionData
{
    Title = "OpenAPI Specification",
    Description = "Orders API OpenAPI 3.0 definition"
};

ArmOperation<ApiCenterApiDefinitionResource> operation = await definitions
    .CreateOrUpdateAsync(WaitUntil.Completed, "openapi", definitionData);

ApiCenterApiDefinitionResource definition = operation.Value;

// Import specification
string openApiSpec = await File.ReadAllTextAsync("orders-api.yaml");

ApiSpecImportContent importContent = new ApiSpecImportContent
{
    Format = ApiSpecImportSourceFormat.Inline,
    Value = openApiSpec,
    Specification = new ApiSpecImportSpecification
    {
        Name = "openapi",
        Version = "3.0.1"
    }
};

await definition.ImportSpecificationAsync(WaitUntil.Completed, importContent);
```

### 6. 导出 API 规范

```csharp
ApiCenterApiDefinitionResource definition = await client
    .GetApiCenterApiDefinitionResource(definitionResourceId)
    .GetAsync();

ArmOperation<ApiSpecExportResult> operation = await definition
    .ExportSpecificationAsync(WaitUntil.Completed);

ApiSpecExportResult result = operation.Value;

// result.Format - e.g., "inline"
// result.Value - the specification content
```

### 7. 创建环境

```csharp
ApiCenterEnvironmentCollection environments = workspace.GetApiCenterEnvironments();

ApiCenterEnvironmentData envData = new ApiCenterEnvironmentData
{
    Title = "Production",
    Description = "Production environment",
    Kind = ApiCenterEnvironmentKind.Production,
    Server = new ApiCenterEnvironmentServer
    {
        ManagementPortalUris = { new Uri("https://portal.azure.com") }
    },
    Onboarding = new EnvironmentOnboardingModel
    {
        Instructions = "Contact platform team for access",
        DeveloperPortalUris = { new Uri("https://developer.example.com") }
    }
};

ArmOperation<ApiCenterEnvironmentResource> operation = await environments
    .CreateOrUpdateAsync(WaitUntil.Completed, "production", envData);
```

### 8. 创建部署

```csharp
ApiCenterDeploymentCollection deployments = workspace.GetApiCenterDeployments();

// Get environment resource ID
ResourceIdentifier envResourceId = ApiCenterEnvironmentResource.CreateResourceIdentifier(
    subscriptionId, resourceGroupName, serviceName, workspaceName, "production");

// Get API definition resource ID
ResourceIdentifier definitionResourceId = ApiCenterApiDefinitionResource.CreateResourceIdentifier(
    subscriptionId, resourceGroupName, serviceName, workspaceName, 
    "orders-api", "v1-0-0", "openapi");

ApiCenterDeploymentData deploymentData = new ApiCenterDeploymentData
{
    Title = "Orders API - Production",
    Description = "Production deployment of Orders API v1.0.0",
    EnvironmentId = envResourceId,
    DefinitionId = definitionResourceId,
    State = ApiCenterDeploymentState.Active,
    Server = new ApiCenterDeploymentServer
    {
        RuntimeUris = { new Uri("https://api.example.com/orders") }
    }
};

ArmOperation<ApiCenterDeploymentResource> operation = await deployments
    .CreateOrUpdateAsync(WaitUntil.Completed, "orders-api-prod", deploymentData);
```

### 9. 创建元数据 Schema

```csharp
ApiCenterMetadataSchemaCollection schemas = service.GetApiCenterMetadataSchemas();

string jsonSchema = """
{
    "type": "object",
    "properties": {
        "team": {
            "type": "string",
            "title": "Owning Team"
        },
        "costCenter": {
            "type": "string",
            "title": "Cost Center"
        },
        "dataClassification": {
            "type": "string",
            "enum": ["public", "internal", "confidential"],
            "title": "Data Classification"
        }
    },
    "required": ["team"]
}
""";

ApiCenterMetadataSchemaData schemaData = new ApiCenterMetadataSchemaData
{
    Schema = jsonSchema,
    AssignedTo =
    {
        new MetadataAssignment
        {
            Entity = MetadataAssignmentEntity.Api,
            Required = true
        }
    }
};

ArmOperation<ApiCenterMetadataSchemaResource> operation = await schemas
    .CreateOrUpdateAsync(WaitUntil.Completed, "api-metadata", schemaData);
```

### 10. 列出和搜索 API

```csharp
// List all APIs in a workspace
ApiCenterWorkspaceResource workspace = await client
    .GetApiCenterWorkspaceResource(workspaceResourceId)
    .GetAsync();

await foreach (ApiCenterApiResource api in workspace.GetApiCenterApis())
{
    Console.WriteLine($"API: {api.Data.Title}");
    Console.WriteLine($"  Kind: {api.Data.Kind}");
    Console.WriteLine($"  Stage: {api.Data.LifecycleStage}");
    
    // List versions
    await foreach (ApiCenterApiVersionResource version in api.GetApiCenterApiVersions())
    {
        Console.WriteLine($"  Version: {version.Data.Title}");
    }
}

// List environments
await foreach (ApiCenterEnvironmentResource env in workspace.GetApiCenterEnvironments())
{
    Console.WriteLine($"Environment: {env.Data.Title} ({env.Data.Kind})");
}

// List deployments
await foreach (ApiCenterDeploymentResource deployment in workspace.GetApiCenterDeployments())
{
    Console.WriteLine($"Deployment: {deployment.Data.Title}");
    Console.WriteLine($"  State: {deployment.Data.State}");
}
```

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ApiCenterServiceResource` | API Center 服务实例 |
| `ApiCenterWorkspaceResource` | API 的逻辑分组 |
| `ApiCenterApiResource` | 单个 API |
| `ApiCenterApiVersionResource` | API 的版本 |
| `ApiCenterApiDefinitionResource` | API 规范（OpenAPI 等） |
| `ApiCenterEnvironmentResource` | 部署环境 |
| `ApiCenterDeploymentResource` | API 部署到环境 |
| `ApiCenterMetadataSchemaResource` | 自定义元数据 Schema |
| `ApiKind` | rest、graphql、grpc、soap、webhook、websocket、mcp |
| `ApiLifecycleStage` | design、development、testing、preview、production、deprecated、retired |
| `ApiCenterEnvironmentKind` | development、testing、staging、production |
| `ApiCenterDeploymentState` | active、inactive |

## 最佳实践

1. **使用工作区组织** — 按团队、领域或产品对 API 进行分组
2. **使用元数据 Schema** — 定义自定义属性以实现治理
3. **跟踪生命周期阶段** — 保持 API 状态最新（设计 → 生产 → 弃用）
4. **记录环境** — 包含入门说明和门户 URI
5. **一致的版本管理** — 对 API 版本使用语义化版本号
6. **导入规范** — 上传 OpenAPI/GraphQL 规范以便发现
7. **关联部署** — 将 API 连接到其运行时环境
8. **使用托管标识** — 启用 SystemAssigned 标识以实现安全集成

## 错误处理

```csharp
using Azure;

try
{
    ArmOperation<ApiCenterApiResource> operation = await apis
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-api", apiData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("API already exists with conflicting configuration");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.ApiCenter` | API Center 管理（本 SDK） | `dotnet add package Azure.ResourceManager.ApiCenter` |
| `Azure.ResourceManager.ApiManagement` | API 网关和策略 | `dotnet add package Azure.ResourceManager.ApiManagement` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.ApiCenter |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.apicenter |
| 产品文档 | https://learn.microsoft.com/azure/api-center/ |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/apicenter/Azure.ResourceManager.ApiCenter |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
