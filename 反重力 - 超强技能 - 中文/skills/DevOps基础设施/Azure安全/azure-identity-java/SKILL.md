---
name: azure-identity-java
description: "使用 Microsoft Entra ID (Azure AD) 对 Java 应用程序进行 Azure 服务身份验证。当用户要求'Azure身份验证Java'、'DefaultAzureCredential Java'、'托管标识Java'、'服务主体Java'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Identity (Java)

使用 Microsoft Entra ID (Azure AD) 对 Java 应用程序进行 Azure 服务身份验证。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.15.0</version>
</dependency>
```

## 核心概念

| 凭据 | 使用场景 |
|------------|----------|
| `DefaultAzureCredential` | **推荐** - 适用于开发和生产环境 |
| `ManagedIdentityCredential` | Azure 托管应用（App Service、Functions、VM） |
| `EnvironmentCredential` | 使用环境变量的 CI/CD 管道 |
| `ClientSecretCredential` | 使用密钥的服务主体 |
| `ClientCertificateCredential` | 使用证书的服务主体 |
| `AzureCliCredential` | 使用 `az login` 的本地开发 |
| `InteractiveBrowserCredential` | 交互式登录流程 |
| `DeviceCodeCredential` | 无头设备身份验证 |

## DefaultAzureCredential（推荐）

`DefaultAzureCredential` 按顺序尝试多种身份验证方法：

1. 环境变量
2. Workload Identity
3. Managed Identity
4. Azure CLI
5. Azure PowerShell
6. Azure Developer CLI

```java
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

// 简单用法
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

// 配合任意 Azure 客户端使用
BlobServiceClient blobClient = new BlobServiceClientBuilder()
    .endpoint("https://<storage-account>.blob.core.windows.net")
    .credential(credential)
    .buildClient();

KeyClient keyClient = new KeyClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(credential)
    .buildClient();
```

### 配置 DefaultAzureCredential

```java
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
    .managedIdentityClientId("<user-assigned-identity-client-id>")  // 用于用户分配的托管标识
    .tenantId("<tenant-id>")                                        // 限定到特定租户
    .excludeEnvironmentCredential()                                 // 跳过环境变量
    .excludeAzureCliCredential()                                    // 跳过 Azure CLI
    .build();
```

## 托管标识

适用于 Azure 托管应用程序（App Service、Functions、AKS、VM）。

```java
import com.azure.identity.ManagedIdentityCredential;
import com.azure.identity.ManagedIdentityCredentialBuilder;

// 系统分配的托管标识
ManagedIdentityCredential credential = new ManagedIdentityCredentialBuilder()
    .build();

// 用户分配的托管标识（按客户端 ID）
ManagedIdentityCredential credential = new ManagedIdentityCredentialBuilder()
    .clientId("<user-assigned-client-id>")
    .build();

// 用户分配的托管标识（按资源 ID）
ManagedIdentityCredential credential = new ManagedIdentityCredentialBuilder()
    .resourceId("/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>")
    .build();
```

## 使用密钥的服务主体

```java
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

ClientSecretCredential credential = new ClientSecretCredentialBuilder()
    .tenantId("<tenant-id>")
    .clientId("<client-id>")
    .clientSecret("<client-secret>")
    .build();
```

## 使用证书的服务主体

```java
import com.azure.identity.ClientCertificateCredential;
import com.azure.identity.ClientCertificateCredentialBuilder;

// 从 PEM 文件
ClientCertificateCredential credential = new ClientCertificateCredentialBuilder()
    .tenantId("<tenant-id>")
    .clientId("<client-id>")
    .pemCertificate("<path-to-cert.pem>")
    .build();

// 从带密码的 PFX 文件
ClientCertificateCredential credential = new ClientCertificateCredentialBuilder()
    .tenantId("<tenant-id>")
    .clientId("<client-id>")
    .pfxCertificate("<path-to-cert.pfx>", "<pfx-password>")
    .build();

// 发送证书链用于 SNI
ClientCertificateCredential credential = new ClientCertificateCredentialBuilder()
    .tenantId("<tenant-id>")
    .clientId("<client-id>")
    .pemCertificate("<path-to-cert.pem>")
    .sendCertificateChain(true)
    .build();
```

## 环境凭据

从环境变量读取凭据。

```java
import com.azure.identity.EnvironmentCredential;
import com.azure.identity.EnvironmentCredentialBuilder;

EnvironmentCredential credential = new EnvironmentCredentialBuilder().build();
```

### 所需环境变量

**使用密钥的服务主体：**
```bash
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

**使用证书的服务主体：**
```bash
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_CERTIFICATE_PATH=/path/to/cert.pem
AZURE_CLIENT_CERTIFICATE_PASSWORD=<optional-password>
```

**使用用户名/密码：**
```bash
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_USERNAME=<username>
AZURE_PASSWORD=<password>
```

## Azure CLI 凭据

用于使用 `az login` 的本地开发。

```java
import com.azure.identity.AzureCliCredential;
import com.azure.identity.AzureCliCredentialBuilder;

AzureCliCredential credential = new AzureCliCredentialBuilder()
    .tenantId("<tenant-id>")  // 可选：指定租户
    .build();
```

## 交互式浏览器

用于需要用户登录的桌面应用程序。

```java
import com.azure.identity.InteractiveBrowserCredential;
import com.azure.identity.InteractiveBrowserCredentialBuilder;

InteractiveBrowserCredential credential = new InteractiveBrowserCredentialBuilder()
    .clientId("<client-id>")
    .redirectUrl("http://localhost:8080")  // 必须与应用注册匹配
    .build();
```

## 设备代码

用于无头设备（IoT、CLI 工具）。

```java
import com.azure.identity.DeviceCodeCredential;
import com.azure.identity.DeviceCodeCredentialBuilder;

DeviceCodeCredential credential = new DeviceCodeCredentialBuilder()
    .clientId("<client-id>")
    .challengeConsumer(challenge -> {
        // 显示给用户
        System.out.println(challenge.getMessage());
    })
    .build();
```

## 链式凭据

创建自定义身份验证链。

```java
import com.azure.identity.ChainedTokenCredential;
import com.azure.identity.ChainedTokenCredentialBuilder;

ChainedTokenCredential credential = new ChainedTokenCredentialBuilder()
    .addFirst(new ManagedIdentityCredentialBuilder().build())
    .addLast(new AzureCliCredentialBuilder().build())
    .build();
```

## Workload Identity (AKS)

用于配置了工作负载标识的 Azure Kubernetes Service。

```java
import com.azure.identity.WorkloadIdentityCredential;
import com.azure.identity.WorkloadIdentityCredentialBuilder;

// 从 AZURE_TENANT_ID、AZURE_CLIENT_ID、AZURE_FEDERATED_TOKEN_FILE 读取
WorkloadIdentityCredential credential = new WorkloadIdentityCredentialBuilder().build();

// 或显式配置
WorkloadIdentityCredential credential = new WorkloadIdentityCredentialBuilder()
    .tenantId("<tenant-id>")
    .clientId("<client-id>")
    .tokenFilePath("/var/run/secrets/azure/tokens/azure-identity-token")
    .build();
```

## Token 缓存

启用持久化 token 缓存以提升性能。

```java
// 启用 token 缓存（默认内存缓存）
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
    .enableAccountIdentifierLogging()
    .build();

// 使用共享 token 缓存（适用于多凭据场景）
SharedTokenCacheCredential credential = new SharedTokenCacheCredentialBuilder()
    .clientId("<client-id>")
    .build();
```

## 主权云

```java
import com.azure.identity.AzureAuthorityHosts;

// Azure Government
DefaultAzureCredential govCredential = new DefaultAzureCredentialBuilder()
    .authorityHost(AzureAuthorityHosts.AZURE_GOVERNMENT)
    .build();

// Azure 中国
DefaultAzureCredential chinaCredential = new DefaultAzureCredentialBuilder()
    .authorityHost(AzureAuthorityHosts.AZURE_CHINA)
    .build();
```

## 错误处理

```java
import com.azure.identity.CredentialUnavailableException;
import com.azure.core.exception.ClientAuthenticationException;

try {
    DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
    AccessToken token = credential.getToken(new TokenRequestContext()
        .addScopes("https://management.azure.com/.default"));
} catch (CredentialUnavailableException e) {
    // 没有凭据能够完成身份验证
    System.out.println("Authentication failed: " + e.getMessage());
} catch (ClientAuthenticationException e) {
    // 身验证错误（凭据错误、过期等）
    System.out.println("Auth error: " + e.getMessage());
}
```

## 日志

启用身份验证日志用于调试。

```java
// 通过环境变量
// AZURE_LOG_LEVEL=verbose

// 或编程方式
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
    .enableAccountIdentifierLogging()  // 记录账户信息
    .build();
```

## 环境变量

```bash
# DefaultAzureCredential 配置
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>

# 托管标识
AZURE_CLIENT_ID=<user-assigned-mi-client-id>

# Workload Identity (AKS)
AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token

# 日志
AZURE_LOG_LEVEL=verbose

# 权限主机
AZURE_AUTHORITY_HOST=https://login.microsoftonline.com/
```

## 最佳实践

1. **使用 DefaultAzureCredential** - 从开发到生产无缝切换
2. **生产环境使用托管标识** - 无需管理密钥，自动轮换
3. **本地开发使用 Azure CLI** - 运行应用前先执行 `az login`
4. **最小权限原则** - 仅授予服务主体所需权限
5. **Token 缓存** - 默认启用，减少身份验证往返
6. **环境变量** - 用于 CI/CD，不要硬编码密钥

## 凭据选择矩阵

| 环境 | 推荐凭据 |
|-------------|----------------------|
| 本地开发 | `DefaultAzureCredential`（使用 Azure CLI） |
| Azure App Service | `DefaultAzureCredential`（使用托管标识） |
| Azure Functions | `DefaultAzureCredential`（使用托管标识） |
| Azure Kubernetes Service | `WorkloadIdentityCredential` |
| Azure VM | `DefaultAzureCredential`（使用托管标识） |
| CI/CD 管道 | `EnvironmentCredential` |
| 桌面应用 | `InteractiveBrowserCredential` |
| CLI 工具 | `DeviceCodeCredential` |

## 触发短语

- "Azure authentication Java"、"DefaultAzureCredential Java"
- "managed identity Java"、"service principal Java"
- "Azure login Java"、"Azure credentials Java"
- "AZURE_CLIENT_ID"、"AZURE_TENANT_ID"

## 何时使用
本技能适用于执行概述中所述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
