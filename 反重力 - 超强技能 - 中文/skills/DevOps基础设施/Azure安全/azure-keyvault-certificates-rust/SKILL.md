---
name: azure-keyvault-certificates-rust
description: Azure Key Vault 证书 Rust SDK，用于创建、导入和管理证书。当用户要求'Azure Key Vault 证书管理'、'Rust 证书操作'、'Key Vault 证书 SDK'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Key Vault Certificates SDK for Rust

Azure Key Vault Certificates 的客户端库——安全存储和管理证书。

## 安装

```sh
cargo add azure_security_keyvault_certificates azure_identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 身份认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_certificates::CertificateClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = CertificateClient::new(
    "https://<vault-name>.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

## 核心操作

### 获取证书

```rust
use azure_core::base64;

let certificate = client
    .get_certificate("certificate-name", None)
    .await?
    .into_model()?;

println!(
    "Thumbprint: {:?}",
    certificate.x509_thumbprint.map(base64::encode_url_safe)
);
```

### 创建证书

```rust
use azure_security_keyvault_certificates::models::{
    CreateCertificateParameters, CertificatePolicy,
    IssuerParameters, X509CertificateProperties,
};

let policy = CertificatePolicy {
    issuer_parameters: Some(IssuerParameters {
        name: Some("Self".into()),
        ..Default::default()
    }),
    x509_certificate_properties: Some(X509CertificateProperties {
        subject: Some("CN=example.com".into()),
        ..Default::default()
    }),
    ..Default::default()
};

let params = CreateCertificateParameters {
    certificate_policy: Some(policy),
    ..Default::default()
};

let operation = client
    .create_certificate("cert-name", params.try_into()?, None)
    .await?;
```

### 导入证书

```rust
use azure_security_keyvault_certificates::models::ImportCertificateParameters;

let params = ImportCertificateParameters {
    base64_encoded_certificate: Some(base64_cert_data),
    password: Some("optional-password".into()),
    ..Default::default()
};

let certificate = client
    .import_certificate("cert-name", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 删除证书

```rust
client.delete_certificate("certificate-name", None).await?;
```

### 列出证书

```rust
use azure_security_keyvault_certificates::ResourceExt;
use futures::TryStreamExt;

let mut pager = client.list_certificate_properties(None)?.into_stream();
while let Some(cert) = pager.try_next().await? {
    let name = cert.resource_id()?.name;
    println!("Certificate: {}", name);
}
```

### 获取证书策略

```rust
let policy = client
    .get_certificate_policy("certificate-name", None)
    .await?
    .into_model()?;
```

### 更新证书策略

```rust
use azure_security_keyvault_certificates::models::UpdateCertificatePolicyParameters;

let params = UpdateCertificatePolicyParameters {
    // Update policy properties
    ..Default::default()
};

client
    .update_certificate_policy("cert-name", params.try_into()?, None)
    .await?;
```

## 证书生命周期

1. **创建** — 根据策略生成新证书
2. **导入** — 导入现有的 PFX/PEM 证书
3. **获取** — 检索证书（仅公钥）
4. **更新** — 修改证书属性
5. **删除** — 软删除（可恢复）
6. **清除** — 永久删除

## 最佳实践

1. **使用 Entra ID 认证** — 开发环境使用 `DeveloperToolsCredential`
2. **使用托管证书** — 通过支持的颁发者自动续期
3. **设置合理的有效期** — 平衡安全性与维护成本
4. **使用证书策略** — 定义续期和密钥属性
5. **监控过期时间** — 为即将过期的证书设置告警
6. **启用软删除** — 生产环境 Vault 必须启用

## RBAC 权限

分配以下 Key Vault 角色：
- `Key Vault Certificates Officer` — 证书的完整 CRUD 权限
- `Key Vault Reader` — 读取证书元数据

## 参考链接

| 资源 | 链接 |
|------|------|
| API 参考 | https://docs.rs/azure_security_keyvault_certificates |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_certificates |
| crates.io | https://crates.io/crates/azure_security_keyvault_certificates |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
