---
name: azure-identity-dotnet
description: Azure Identity SDK for .NET 认证库，用于使用 Microsoft Entra ID 的 Azure SDK 客户端认证。涵盖 DefaultAzureCredential、托管标识、服务主体和开发者凭据。当用户要求'Azure认证'、'.NET Azure Identity'、'DefaultAzureCredential'、'托管标识'、'服务主体认证'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.Identity (.NET)

使用 Microsoft Entra ID（原 Azure AD）的 Azure SDK 客户端认证库。

## 安装

```bash
dotnet add package Azure.Identity

# For ASP.NET Core
dotnet add package Microsoft.Extensions.Azure

# For brokered authentication (Windows)
dotnet add package Azure.Identity.Broker
```

**当前版本**：稳定版 v1.17.1，预览版 v1.18.0-beta.2

## 环境变量

### 使用密钥的服务主体
```bash
AZURE_CLIENT_ID=<application-client-id>
AZURE_TENANT_ID=<directory-tenant-id>
AZURE_CLIENT_SECRET=<client-secret-value>
```

### 使用证书的服务主体
```bash
AZURE_CLIENT_ID=<application-client-id>
AZURE_TENANT_ID=<directory-tenant-id>
AZURE_CLIENT_CERTIFICATE_PATH=<path-to-pfx-or-pem>
AZURE_CLIENT_CERTIFICATE_PASSWORD=<certificate-password>  # Optional
```

### 托管标识
```bash
AZURE_CLIENT_ID=<user-assigned-managed-identity-client-id>  # Only for user-assigned
```

## DefaultAzureCredential

适用于大多数场景的推荐凭据。按顺序尝试多种认证方式：

| 顺序 | 凭据 | 默认启用 |
|-------|------------|-------------------|
| 1 | EnvironmentCredential | 是 |
| 2 | WorkloadIdentityCredential | 是 |
| 3 | ManagedIdentityCredential | 是 |
| 4 | VisualStudioCredential | 是 |
| 5 | VisualStudioCodeCredential | 是 |
| 6 | AzureCliCredential | 是 |
| 7 | AzurePowerShellCredential | 是 |
| 8 | AzureDeveloperCliCredential | 是 |
| 9 | InteractiveBrowserCredential | **否** |

### 基本用法

```csharp
using Azure.Identity;
using Azure.Storage.Blobs;

var credential = new DefaultAzureCredential();
var blobClient = new BlobServiceClient(
    new Uri("https://myaccount.blob.core.windows.net"),
    credential);
```

### ASP.NET Core 依赖注入

```csharp
using Azure.Identity;
using Microsoft.Extensions.Azure;

builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.AddBlobServiceClient(
        new Uri("https://myaccount.blob.core.windows.net"));
    clientBuilder.AddSecretClient(
        new Uri("https://myvault.vault.azure.net"));
    
    // Uses DefaultAzureCredential by default
    clientBuilder.UseCredential(new DefaultAzureCredential());
});
```

### 自定义 DefaultAzureCredential

```csharp
var credential = new DefaultAzureCredential(
    new DefaultAzureCredentialOptions
    {
        ExcludeEnvironmentCredential = true,
        ExcludeManagedIdentityCredential = false,
        ExcludeVisualStudioCredential = false,
        ExcludeAzureCliCredential = false,
        ExcludeInteractiveBrowserCredential = false, // Enable interactive
        TenantId = "<tenant-id>",
        ManagedIdentityClientId = "<user-assigned-mi-client-id>"
    });
```

## 凭据类型

### ManagedIdentityCredential（生产环境）

```csharp
// System-assigned managed identity
var credential = new ManagedIdentityCredential(ManagedIdentityId.SystemAssigned);

// User-assigned by client ID
var credential = new ManagedIdentityCredential(
    ManagedIdentityId.FromUserAssignedClientId("<client-id>"));

// User-assigned by resource ID
var credential = new ManagedIdentityCredential(
    ManagedIdentityId.FromUserAssignedResourceId("<resource-id>"));
```

### ClientSecretCredential

```csharp
var credential = new ClientSecretCredential(
    tenantId: "<tenant-id>",
    clientId: "<client-id>",
    clientSecret: "<client-secret>");

var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net"),
    credential);
```

### ClientCertificateCredential

```csharp
var certificate = X509CertificateLoader.LoadCertificateFromFile("MyCertificate.pfx");
var credential = new ClientCertificateCredential(
    tenantId: "<tenant-id>",
    clientId: "<client-id>",
    certificate);
```

### ChainedTokenCredential（自定义链）

```csharp
var credential = new ChainedTokenCredential(
    new ManagedIdentityCredential(),
    new AzureCliCredential());

var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net"),
    credential);
```

### 开发者凭据

```csharp
// Azure CLI
var credential = new AzureCliCredential();

// Azure PowerShell
var credential = new AzurePowerShellCredential();

// Azure Developer CLI (azd)
var credential = new AzureDeveloperCliCredential();

// Visual Studio
var credential = new VisualStudioCredential();

// Interactive Browser
var credential = new InteractiveBrowserCredential();
```

## 基于环境的配置

```csharp
// Production vs Development
TokenCredential credential = builder.Environment.IsProduction()
    ? new ManagedIdentityCredential("<client-id>")
    : new DefaultAzureCredential();
```

## 主权云

```csharp
var credential = new DefaultAzureCredential(
    new DefaultAzureCredentialOptions
    {
        AuthorityHost = AzureAuthorityHosts.AzureGovernment
    });

// Available authority hosts:
// AzureAuthorityHosts.AzurePublicCloud (default)
// AzureAuthorityHosts.AzureGovernment
// AzureAuthorityHosts.AzureChina
// AzureAuthorityHosts.AzureGermany
```

## 凭据类型参考

| 类别 | 凭据 | 用途 |
|----------|------------|---------|
| **链式** | `DefaultAzureCredential` | 预配置的开发到生产链 |
| | `ChainedTokenCredential` | 自定义凭据链 |
| **Azure 托管** | `ManagedIdentityCredential` | Azure 托管标识 |
| | `WorkloadIdentityCredential` | Kubernetes 工作负载标识 |
| | `EnvironmentCredential` | 环境变量 |
| **服务主体** | `ClientSecretCredential` | 客户端 ID + 密钥 |
| | `ClientCertificateCredential` | 客户端 ID + 证书 |
| | `ClientAssertionCredential` | 签名的客户端断言 |
| **用户** | `InteractiveBrowserCredential` | 基于浏览器的认证 |
| | `DeviceCodeCredential` | 设备代码流程 |
| | `OnBehalfOfCredential` | 委派标识 |
| **开发者** | `AzureCliCredential` | Azure CLI |
| | `AzurePowerShellCredential` | Azure PowerShell |
| | `AzureDeveloperCliCredential` | Azure Developer CLI |
| | `VisualStudioCredential` | Visual Studio |

## 最佳实践

### 1. 在生产环境中使用确定性凭据

```csharp
// Development
var devCredential = new DefaultAzureCredential();

// Production - use specific credential
var prodCredential = new ManagedIdentityCredential("<client-id>");
```

### 2. 复用凭据实例

```csharp
// Good: Single credential instance shared across clients
var credential = new DefaultAzureCredential();
var blobClient = new BlobServiceClient(blobUri, credential);
var secretClient = new SecretClient(vaultUri, credential);
```

### 3. 配置重试策略

```csharp
var options = new ManagedIdentityCredentialOptions(
    ManagedIdentityId.FromUserAssignedClientId(clientId))
{
    Retry =
    {
        MaxRetries = 3,
        Delay = TimeSpan.FromSeconds(0.5),
    }
};
var credential = new ManagedIdentityCredential(options);
```

### 4. 启用调试日志

```csharp
using Azure.Core.Diagnostics;

using AzureEventSourceListener listener = new((args, message) =>
{
    if (args is { EventSource.Name: "Azure-Identity" })
    {
        Console.WriteLine(message);
    }
}, EventLevel.LogAlways);
```

## 错误处理

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net"),
    new DefaultAzureCredential());

try
{
    KeyVaultSecret secret = await client.GetSecretAsync("secret1");
}
catch (AuthenticationFailedException e)
{
    Console.WriteLine($"Authentication Failed: {e.Message}");
}
catch (CredentialUnavailableException e)
{
    Console.WriteLine($"Credential Unavailable: {e.Message}");
}
```

## 关键异常

| 异常 | 说明 |
|-----------|-------------|
| `AuthenticationFailedException` | 认证错误的基础异常 |
| `CredentialUnavailableException` | 凭据在当前环境中无法认证 |
| `AuthenticationRequiredException` | 需要交互式认证 |

## 托管标识支持

支持的 Azure 服务：
- Azure App Service 和 Azure Functions
- Azure Arc
- Azure Cloud Shell
- Azure Kubernetes Service (AKS)
- Azure Service Fabric
- Azure Virtual Machines
- Azure Virtual Machine Scale Sets

## 线程安全

所有凭据实现都是线程安全的。单个凭据实例可以安全地在多个客户端和线程之间共享。

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|---------|---------|
| `Azure.Identity` | 认证（本 SDK） | `dotnet add package Azure.Identity` |
| `Microsoft.Extensions.Azure` | DI 集成 | `dotnet add package Microsoft.Extensions.Azure` |
| `Azure.Identity.Broker` | 代理认证（Windows） | `dotnet add package Azure.Identity.Broker` |

## 参考链接

| 资源 | URL |
|----------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.Identity |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.identity |
| 凭据链 | https://learn.microsoft.com/dotnet/azure/sdk/authentication/credential-chains |
| 最佳实践 | https://learn.microsoft.com/dotnet/azure/sdk/authentication/best-practices |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/identity/Azure.Identity |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
