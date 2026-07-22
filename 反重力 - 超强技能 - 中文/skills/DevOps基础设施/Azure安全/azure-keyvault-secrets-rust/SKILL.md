---
name: azure-keyvault-secrets-rust
description: 'Azure Key Vault Secrets Rust SDK，用于安全存储和检索密码、API 密钥等机密信息。当用户要求"keyvault secrets rust"、"SecretClient rust"、"get secret rust"、"set secret rust"时使用。'
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Key Vault Secrets SDK for Rust

Azure Key Vault Secrets 的客户端库——用于密码、API 密钥及其他机密的安全存储。

## 安装

```sh
cargo add azure_security_keyvault_secrets azure_identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 身份认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_secrets::SecretClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = SecretClient::new(
    "https://<vault-name>.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

## 核心操作

### 获取机密

```rust
let secret = client
    .get_secret("secret-name", None)
    .await?
    .into_model()?;

println!("Secret value: {:?}", secret.value);
```

### 设置机密

```rust
use azure_security_keyvault_secrets::models::SetSecretParameters;

let params = SetSecretParameters {
    value: Some("secret-value".into()),
    ..Default::default()
};

let secret = client
    .set_secret("secret-name", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 更新机密属性

```rust
use azure_security_keyvault_secrets::models::UpdateSecretPropertiesParameters;
use std::collections::HashMap;

let params = UpdateSecretPropertiesParameters {
    content_type: Some("text/plain".into()),
    tags: Some(HashMap::from([("env".into(), "prod".into())])),
    ..Default::default()
};

client
    .update_secret_properties("secret-name", params.try_into()?, None)
    .await?;
```

### 删除机密

```rust
client.delete_secret("secret-name", None).await?;
```

### 列出机密

```rust
use azure_security_keyvault_secrets::ResourceExt;
use futures::TryStreamExt;

let mut pager = client.list_secret_properties(None)?.into_stream();
while let Some(secret) = pager.try_next().await? {
    let name = secret.resource_id()?.name;
    println!("Secret: {}", name);
}
```

### 获取指定版本

```rust
use azure_security_keyvault_secrets::models::SecretClientGetSecretOptions;

let options = SecretClientGetSecretOptions {
    secret_version: Some("version-id".into()),
    ..Default::default()
};

let secret = client
    .get_secret("secret-name", Some(options))
    .await?
    .into_model()?;
```

## 最佳实践

1. **使用 Entra ID 认证** — 开发环境用 `DeveloperToolsCredential`，生产环境用 `ManagedIdentityCredential`
2. **使用 `into_model()?`** — 用于反序列化响应
3. **使用 `ResourceExt` trait** — 用于从 ID 中提取名称
4. **处理软删除** — 已删除的机密在保留期内可恢复
5. **设置内容类型** — 有助于识别机密格式
6. **使用标签** — 用于组织和筛选机密
7. **版本化机密** — 新值会自动创建新版本

## RBAC 权限

分配以下 Key Vault 角色：
- `Key Vault Secrets User` — 获取和列出
- `Key Vault Secrets Officer` — 完整 CRUD

## 参考链接

| 资源 | 链接 |
|------|------|
| API 参考 | https://docs.rs/azure_security_keyvault_secrets |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_secrets |
| crates.io | https://crates.io/crates/azure_security_keyvault_secrets |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
