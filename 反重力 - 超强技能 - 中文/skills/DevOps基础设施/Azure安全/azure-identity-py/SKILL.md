---
name: azure-identity-py
description: Azure Identity SDK for Python 身份认证。涵盖 DefaultAzureCredential、托管标识、服务主体和 token 缓存。当用户要求'Azure身份认证'、'Python Azure认证'、'DefaultAzureCredential'、'托管标识'、'服务主体认证'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Identity SDK for Python

使用 Microsoft Entra ID（原 Azure AD）的 Azure SDK 客户端身份认证库。

## 安装

```bash
pip install azure-identity
```

## 环境变量

```bash
# Service Principal (for production/CI)
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>

# User-assigned Managed Identity (optional)
AZURE_CLIENT_ID=<managed-identity-client-id>
```

## DefaultAzureCredential

适用于大多数场景的推荐凭据。按顺序尝试多种认证方式：

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Works in local dev AND production without code changes
credential = DefaultAzureCredential()

client = BlobServiceClient(
    account_url="https://<account>.blob.core.windows.net",
    credential=credential
)
```

### 凭据链顺序

| 顺序 | 凭据 | 环境 |
|-------|-----------|-------------|
| 1 | EnvironmentCredential | CI/CD、容器 |
| 2 | WorkloadIdentityCredential | Kubernetes |
| 3 | ManagedIdentityCredential | Azure VM、App Service、Functions |
| 4 | SharedTokenCacheCredential | 仅 Windows |
| 5 | VisualStudioCodeCredential | 安装了 Azure 扩展的 VS Code |
| 6 | AzureCliCredential | `az login` |
| 7 | AzurePowerShellCredential | `Connect-AzAccount` |
| 8 | AzureDeveloperCliCredential | `azd auth login` |

### 自定义 DefaultAzureCredential

```python
# Exclude credentials you don't need
credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_shared_token_cache_credential=True,
    managed_identity_client_id="<user-assigned-mi-client-id>"  # For user-assigned MI
)

# Enable interactive browser (disabled by default)
credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=False
)
```

## 特定凭据类型

### ManagedIdentityCredential

适用于 Azure 托管资源（VM、App Service、Functions、AKS）：

```python
from azure.identity import ManagedIdentityCredential

# System-assigned managed identity
credential = ManagedIdentityCredential()

# User-assigned managed identity
credential = ManagedIdentityCredential(
    client_id="<user-assigned-mi-client-id>"
)
```

### ClientSecretCredential

使用密钥的服务主体：

```python
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)
```

### AzureCliCredential

使用 `az login` 的账户：

```python
from azure.identity import AzureCliCredential

credential = AzureCliCredential()
```

### ChainedTokenCredential

自定义凭据链：

```python
from azure.identity import (
    ChainedTokenCredential,
    ManagedIdentityCredential,
    AzureCliCredential
)

# Try managed identity first, fall back to CLI
credential = ChainedTokenCredential(
    ManagedIdentityCredential(client_id="<user-assigned-mi-client-id>"),
    AzureCliCredential()
)
```

## 凭据类型对照表

| 凭据 | 使用场景 | 认证方式 |
|------------|----------|-------------|
| `DefaultAzureCredential` | 大多数场景 | 自动检测 |
| `ManagedIdentityCredential` | Azure 托管应用 | 托管标识 |
| `ClientSecretCredential` | 服务主体 | 客户端密钥 |
| `ClientCertificateCredential` | 服务主体 | 证书 |
| `AzureCliCredential` | 本地开发 | Azure CLI |
| `AzureDeveloperCliCredential` | 本地开发 | Azure Developer CLI |
| `InteractiveBrowserCredential` | 用户登录 | 浏览器 OAuth |
| `DeviceCodeCredential` | 无头/SSH 环境 | 设备代码流 |

## 直接获取 Token

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# Get token for a specific scope
token = credential.get_token("https://management.azure.com/.default")
print(f"Token expires: {token.expires_on}")

# For Azure Database for PostgreSQL
token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
```

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def main():
    credential = DefaultAzureCredential()
    
    async with BlobServiceClient(
        account_url="https://<account>.blob.core.windows.net",
        credential=credential
    ) as client:
        # ... async operations
        pass
    
    await credential.close()
```

## 最佳实践

1. **使用 DefaultAzureCredential** 编写在本地和 Azure 中均可运行的代码
2. **切勿硬编码凭据** — 使用环境变量或托管标识
3. **生产环境优先使用托管标识** 部署到 Azure 时
4. **使用 ChainedTokenCredential** 需要自定义凭据顺序时
5. **显式关闭异步凭据** 或使用上下文管理器
6. **设置 AZURE_CLIENT_ID** 用于用户分配的托管标识
7. **排除未使用的凭据** 以加速认证

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代针对特定环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
