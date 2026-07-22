---
name: azure-keyvault-keys-rust
description: 'Azure Key Vault Keys Rust SDK。用于创建、管理和使用加密密钥。当用户要求"keyvault keys rust"、"KeyClient rust"、"create key rust"、"encrypt rust"、"sign rust"时使用。'
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Key Vault Keys SDK for Rust

Azure Key Vault Keys 的客户端库——用于加密密钥的安全存储和管理。

## 安装

```sh
cargo add azure_security_keyvault_keys azure_identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 身份认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_keys::KeyClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = KeyClient::new(
    "https://<vault-name>.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

## 密钥类型

| 类型 | 说明 |
|------|------|
| RSA | RSA 密钥（2048、3072、4096 位） |
| EC | 椭圆曲线密钥（P-256、P-384、P-521） |
| RSA-HSM | HSM 保护的 RSA 密钥 |
| EC-HSM | HSM 保护的 EC 密钥 |

## 核心操作

### 获取密钥

```rust
let key = client
    .get_key("key-name", None)
    .await?
    .into_model()?;

println!("Key ID: {:?}", key.key.as_ref().map(|k| &k.kid));
```

### 创建密钥

```rust
use azure_security_keyvault_keys::models::{CreateKeyParameters, KeyType};

let params = CreateKeyParameters {
    kty: KeyType::Rsa,
    key_size: Some(2048),
    ..Default::default()
};

let key = client
    .create_key("key-name", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 创建 EC 密钥

```rust
use azure_security_keyvault_keys::models::{CreateKeyParameters, KeyType, CurveName};

let params = CreateKeyParameters {
    kty: KeyType::Ec,
    curve: Some(CurveName::P256),
    ..Default::default()
};

let key = client
    .create_key("ec-key", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 删除密钥

```rust
client.delete_key("key-name", None).await?;
```

### 列出密钥

```rust
use azure_security_keyvault_keys::ResourceExt;
use futures::TryStreamExt;

let mut pager = client.list_key_properties(None)?.into_stream();
while let Some(key) = pager.try_next().await? {
    let name = key.resource_id()?.name;
    println!("Key: {}", name);
}
```

### 备份密钥

```rust
let backup = client.backup_key("key-name", None).await?;
// Store backup.value safely
```

### 恢复密钥

```rust
use azure_security_keyvault_keys::models::RestoreKeyParameters;

let params = RestoreKeyParameters {
    key_bundle_backup: backup_bytes,
};

client.restore_key(params.try_into()?, None).await?;
```

## 加密操作

Key Vault 可以在不暴露私钥的情况下执行加密操作：

```rust
// For cryptographic operations, use the key's operations
// Available operations depend on key type and permissions:
// - encrypt/decrypt (RSA)
// - sign/verify (RSA, EC)
// - wrapKey/unwrapKey (RSA)
```

## 最佳实践

1. **使用 Entra ID 认证** — 开发环境用 `DeveloperToolsCredential`，生产环境用 `ManagedIdentityCredential`
2. **敏感工作负载使用 HSM 密钥** — 硬件保护的密钥
3. **签名使用 EC** — 比 RSA 更高效
4. **加密使用 RSA** — 加密数据时使用
5. **备份密钥** — 用于灾难恢复
6. **启用软删除** — 生产环境保管库必需
7. **使用密钥轮换** — 定期创建新版本

## RBAC 权限

分配以下 Key Vault 角色：
- `Key Vault Crypto User` — 使用密钥执行加密操作
- `Key Vault Crypto Officer` — 密钥的完整 CRUD 权限

## 参考链接

| 资源 | 链接 |
|------|------|
| API 参考 | https://docs.rs/azure_security_keyvault_keys |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_keys |
| crates.io | https://crates.io/crates/azure_security_keyvault_keys |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
