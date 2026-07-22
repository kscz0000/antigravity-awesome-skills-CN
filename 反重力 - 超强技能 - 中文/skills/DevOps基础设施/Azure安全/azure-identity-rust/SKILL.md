---
name: azure-identity-rust
description: Azure Identity SDK for Rust 身份认证。涵盖 DeveloperToolsCredential、ManagedIdentityCredential、ClientSecretCredential 和基于 token 的身份认证。当用户要求'Rust Azure 身份认证'、'Azure Identity Rust'、'Azure SDK 认证'、'ManagedIdentityCredential'、'ClientSecretCredential'、'DeveloperToolsCredential'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Identity SDK for Rust

使用 Microsoft Entra ID（原 Azure AD）的 Azure SDK 客户端身份认证库。

## 安装

```sh
cargo add azure_identity
```

## 环境变量

```bash
# Service Principal（用于生产/CI 环境）
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>

# 用户分配的托管标识（可选）
AZURE_CLIENT_ID=<managed-identity-client-id>
```

## DeveloperToolsCredential

本地开发推荐的凭据。按顺序尝试开发者工具（Azure CLI、Azure Developer CLI）：

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_secrets::SecretClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = SecretClient::new(
    "https://my-vault.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

### 凭据链顺序

| 顺序 | 凭据 | 环境 |
|-------|-----------|-------------|
| 1 | AzureCliCredential | `az login` |
| 2 | AzureDeveloperCliCredential | `azd auth login` |

## 凭据类型

| 凭据 | 用途 |
|------------|-------|
| `DeveloperToolsCredential` | 本地开发 — 自动尝试 CLI 工具 |
| `ManagedIdentityCredential` | Azure 虚拟机、App Service、Functions、AKS |
| `WorkloadIdentityCredential` | Kubernetes 工作负载标识 |
| `ClientSecretCredential` | 使用密钥的服务主体 |
| `ClientCertificateCredential` | 使用证书的服务主体 |
| `AzureCliCredential` | 直接 Azure CLI 认证 |
| `AzureDeveloperCliCredential` | 直接 azd CLI 认证 |
| `AzurePipelinesCredential` | Azure Pipelines 服务连接 |
| `ClientAssertionCredential` | 自定义断言（联合身份） |

## ManagedIdentityCredential

用于 Azure 托管资源：

```rust
use azure_identity::ManagedIdentityCredential;

// 系统分配的托管标识
let credential = ManagedIdentityCredential::new(None)?;

// 用户分配的托管标识
let options = ManagedIdentityCredentialOptions {
    client_id: Some("<user-assigned-mi-client-id>".into()),
    ..Default::default()
};
let credential = ManagedIdentityCredential::new(Some(options))?;
```

## ClientSecretCredential

用于带密钥的服务主体：

```rust
use azure_identity::ClientSecretCredential;

let credential = ClientSecretCredential::new(
    "<tenant-id>".into(),
    "<client-id>".into(),
    "<client-secret>".into(),
    None,
)?;
```

## 最佳实践

1. **本地开发使用 `DeveloperToolsCredential`** — 自动获取 Azure CLI 凭据
2. **生产环境使用 `ManagedIdentityCredential`** — 无需管理密钥
3. **克隆凭据** — 凭据使用 `Arc` 包装，克隆开销极低
4. **复用凭据实例** — 同一凭据可用于多个客户端
5. **使用 `tokio` 特性** — `cargo add azure_identity --features tokio`

## 参考链接

| 资源 | 链接 |
|----------|------|
| API 参考 | https://docs.rs/azure_identity |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/identity/azure_identity |
| crates.io | https://crates.io/crates/azure_identity |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
