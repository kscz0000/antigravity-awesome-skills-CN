---
name: azure-cosmos-rust
description: Azure Cosmos DB Rust SDK（NoSQL API）。用于文档 CRUD、查询、容器和全球分布式数据。触发词：Cosmos DB Rust、Azure Cosmos、Rust NoSQL、文档数据库、分布式数据库、CosmosClient、ContainerClient、partition key、分区键、Azure 数据库 Rust
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Cosmos DB SDK for Rust

Azure Cosmos DB NoSQL API 的客户端库 — 全球分布式、多模型数据库。

## 安装

```sh
cargo add azure_data_cosmos azure_identity
```

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_DATABASE=mydb
COSMOS_CONTAINER=mycontainer
```

## 认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_data_cosmos::CosmosClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = CosmosClient::new(
    "https://<account>.documents.azure.com:443/",
    credential.clone(),
    None,
)?;
```

## 客户端层级

| 客户端 | 用途 | 获取方式 |
|--------|---------|----------|
| `CosmosClient` | 账户级操作 | 直接实例化 |
| `DatabaseClient` | 数据库操作 | `client.database_client()` |
| `ContainerClient` | 容器/项操作 | `database.container_client()` |

## 核心工作流

### 获取数据库和容器客户端

```rust
let database = client.database_client("myDatabase");
let container = database.container_client("myContainer");
```

### 创建项

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Item {
    pub id: String,
    pub partition_key: String,
    pub value: String,
}

let item = Item {
    id: "1".into(),
    partition_key: "partition1".into(),
    value: "hello".into(),
};

container.create_item("partition1", item, None).await?;
```

### 读取项

```rust
let response = container.read_item("partition1", "1", None).await?;
let item: Item = response.into_model()?;
```

### 替换项

```rust
let mut item: Item = container.read_item("partition1", "1", None).await?.into_model()?;
item.value = "updated".into();

container.replace_item("partition1", "1", item, None).await?;
```

### 补丁项

```rust
use azure_data_cosmos::models::PatchDocument;

let patch = PatchDocument::default()
    .with_add("/newField", "newValue")?
    .with_remove("/oldField")?;

container.patch_item("partition1", "1", patch, None).await?;
```

### 删除项

```rust
container.delete_item("partition1", "1", None).await?;
```

## 密钥认证（可选）

通过 feature flag 启用基于密钥的认证：

```sh
cargo add azure_data_cosmos --features key_auth
```

## 最佳实践

1. **始终指定分区键** — 点读取和写入操作必需
2. **使用 `into_model()?`** — 将响应反序列化为你的类型
3. **为所有文档类型派生 `Serialize` 和 `Deserialize`**
4. **使用 Entra ID 认证** — 优先使用 `DeveloperToolsCredential` 而非密钥认证
5. **复用客户端实例** — 客户端是线程安全且可复用的

## 参考链接

| 资源 | 链接 |
|----------|------|
| API 参考 | https://docs.rs/azure_data_cosmos |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/cosmos/azure_data_cosmos |
| crates.io | https://crates.io/crates/azure_data_cosmos |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
