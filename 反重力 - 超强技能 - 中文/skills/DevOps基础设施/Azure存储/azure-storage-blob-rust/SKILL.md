---
name: azure-storage-blob-rust
description: Azure Blob Storage Rust SDK。当用户要求'上传、下载或管理 Azure Blob 和容器'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Blob Storage SDK for Rust

Azure Blob Storage 的客户端库——微软面向云的对象存储解决方案。

## 安装

```sh
cargo add azure_storage_blob azure_identity
```

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_NAME=<storage-account-name>
# Endpoint: https://<account>.blob.core.windows.net/
```

## 身份认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_storage_blob::{BlobClient, BlobClientOptions};

let credential = DeveloperToolsCredential::new(None)?;
let blob_client = BlobClient::new(
    "https://<account>.blob.core.windows.net/",
    "container-name",
    "blob-name",
    Some(credential),
    Some(BlobClientOptions::default()),
)?;
```

## 客户端类型

| 客户端 | 用途 |
|--------|------|
| `BlobServiceClient` | 账户级操作，列出容器 |
| `BlobContainerClient` | 容器操作，列出 Blob |
| `BlobClient` | 单个 Blob 操作 |

## 核心操作

### 上传 Blob

```rust
use azure_core::http::RequestContent;

let data = b"hello world";
blob_client
    .upload(
        RequestContent::from(data.to_vec()),
        false,  // overwrite
        u64::try_from(data.len())?,
        None,
    )
    .await?;
```

### 下载 Blob

```rust
let response = blob_client.download(None).await?;
let content = response.into_body().collect_bytes().await?;
println!("Content: {:?}", content);
```

### 获取 Blob 属性

```rust
let properties = blob_client.get_properties(None).await?;
println!("Content-Length: {:?}", properties.content_length);
```

### 删除 Blob

```rust
blob_client.delete(None).await?;
```

## 容器操作

```rust
use azure_storage_blob::BlobContainerClient;

let container_client = BlobContainerClient::new(
    "https://<account>.blob.core.windows.net/",
    "container-name",
    Some(credential),
    None,
)?;

// Create container
container_client.create(None).await?;

// List blobs
let mut pager = container_client.list_blobs(None)?;
while let Some(blob) = pager.try_next().await? {
    println!("Blob: {}", blob.name);
}
```

## 最佳实践

1. **使用 Entra ID 认证** — 开发环境用 `DeveloperToolsCredential`，生产环境用 `ManagedIdentityCredential`
2. **指定内容长度** — 上传时必须提供
3. **使用 `RequestContent::from()`** — 包装上传数据
4. **处理异步操作** — 使用 `tokio` 运行时
5. **检查 RBAC 权限** — 确保拥有 "Storage Blob Data Contributor" 角色

## RBAC 权限

使用 Entra ID 认证时，分配以下角色之一：
- `Storage Blob Data Reader` — 只读
- `Storage Blob Data Contributor` — 读写
- `Storage Blob Data Owner` — 完全访问（包括 RBAC）

## 参考链接

| 资源 | 链接 |
|------|------|
| API 参考 | https://docs.rs/azure_storage_blob |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/storage/azure_storage_blob |
| crates.io | https://crates.io/crates/azure_storage_blob |

## 适用场景
本技能适用于执行概述中所述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，应停止并请求澄清。
