---
name: azure-storage-queue-rust
description: 'Rust 语言的 Azure Queue Storage 客户端库。用于发送、接收和管理队列消息。触发词：azure-storage-queue-rust'
risk: unknown
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-rust/skills/azure-storage-queue-rust
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# Rust 语言的 Azure Queue Storage 客户端库
## 使用场景

当你在 Rust 中需要使用 Azure Queue Storage 客户端库时，请使用本技能。用于发送、接收和管理队列消息。触发词：azure-storage-queue-rust


Rust 的 Azure Queue Storage 客户端库——发送、接收和管理队列消息。

在以下场景中使用本技能：

- 应用需要在 Rust 中向 Azure Queue Storage 发送或接收消息
- 你需要创建或管理队列
- 你需要查看、接收或删除队列消息
- 你需要使用基于 RBAC 的身份验证来执行队列操作

> **重要提示**：仅使用由 [azure-sdk](https://crates.io/users/azure-sdk) 这个 crates.io 用户发布的官方 `azure_storage_queue` crate。请勿使用非官方或社区版本。官方 crate 的名称使用下划线，且没有任何版本号为 0.21.0。

## 安装

```sh
cargo add azure_storage_queue azure_identity azure_core tokio
```

> 如果你的代码直接使用了 `azure_core` 中的类型，请将 `azure_core` 添加到 `Cargo.toml`。如果你只使用 `azure_storage_queue` 的重新导出项，那么直接依赖 `azure_core` 是可选的。

## 环境变量

```bash
AZURE_STORAGE_QUEUE_ENDPOINT=https://<account>.queue.core.windows.net/ # 必需，所有操作都依赖此变量
```

## 身份验证

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::QueueServiceClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 本地开发：使用 DeveloperToolsCredential。生产环境：使用 ManagedIdentityCredential。
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;

    // 通过队列名称获取队列客户端。
    let queue_client = service_client.queue_client("<queue_name>")?;
    Ok(())
}
```

## 客户端类型

| 客户端               | 用途                               | 获取方式                                   |
| -------------------- | ------------------------------------- | ---------------------------------------- |
| `QueueServiceClient` | 账户级操作，列出队列 | `QueueServiceClient::new()`              |
| `QueueClient`        | 队列操作，发送/接收/删除消息 | `service_client.queue_client("<name>")?` |

## 核心工作流

### 发送消息

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::{models::QueueMessage, QueueServiceClient};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;
    let queue_client = service_client.queue_client("<queue_name>")?;

    let message = QueueMessage {
        message_text: Some("hello world".to_string()),
    };
    queue_client.send_message(message.try_into()?, None).await?;
    Ok(())
}
```

### 接收消息

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::QueueServiceClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;
    let queue_client = service_client.queue_client("<queue_name>")?;

    let response = queue_client.receive_messages(None).await?;
    let messages = response.into_model()?;
    for msg in messages.items.unwrap_or_default() {
        println!("{}", msg.message_text.as_deref().unwrap_or("<empty>"));
    }
    Ok(())
}
```

### 删除消息

接收到消息后，使用消息 ID 和 pop 回执将其删除：

```rust
let response = queue_client.receive_messages(None).await?;
let messages = response.into_model()?;
for msg in messages.items.unwrap_or_default() {
    if let (Some(id), Some(pop_receipt)) = (&msg.message_id, &msg.pop_receipt) {
        queue_client.delete_message(id, pop_receipt, None).await?;
    }
}
```

### 查看消息（Peek）

在不将消息从队列中移除的前提下查看消息内容：

```rust
let response = queue_client.peek_messages(None).await?;
let messages = response.into_model()?;
for msg in messages.items.unwrap_or_default() {
    println!("Peeked: {}", msg.message_text.as_deref().unwrap_or("<empty>"));
}
```

## RBAC 角色

对于 Entra ID 身份验证，请为该身份分配以下角色之一：

| 角色                                   | 权限                 |
| -------------------------------------- | ---------------------- |
| `Storage Queue Data Reader`            | 读取和查看消息 |
| `Storage Queue Data Contributor`       | 读取/写入消息    |
| `Storage Queue Data Message Sender`    | 仅发送消息     |
| `Storage Queue Data Message Processor` | 接收与删除     |

## 最佳实践

1. **使用 `cargo add` 管理依赖，绝不要直接编辑 `Cargo.toml`** —— 应通过 cargo 命令添加和移除 Rust SDK 依赖，而不是手动修改清单文件。
2. **只有在直接导入 `azure_core` 类型时才需要添加 `azure_core`** —— 如果你的代码导入了 `azure_core::http::Url`、`azure_core::http::RequestContent` 或 `azure_core::error::ErrorKind`，则需要引入 `azure_core`；否则直接依赖是可选的。
3. 本地开发使用 **`DeveloperToolsCredential`**，生产环境使用 **`ManagedIdentityCredential`** —— Rust 不提供单一的 `DefaultAzureCredential` 类型。
4. **永远不要硬编码凭据** —— 应使用环境变量或托管身份。
5. **分配 RBAC 角色** —— 为该身份赋予适当的队列数据角色。
6. **以 `QueueServiceClient` 作为入口**，并通过 `queue_client()` 从中获取 `QueueClient`。
7. **处理完后删除消息** —— 使用从 `receive_messages` 返回的消息 ID 和 pop 回执。
8. **复用客户端** —— 客户端是线程安全的；创建一次，即可在多个任务间共享。

## 参考链接

| 资源      | 链接                                                                                  |
| ------------- | ------------------------------------------------------------------------------------- |
| API 参考 | https://docs.rs/crate/azure_storage_queue/latest                                      |
| crates.io     | https://crates.io/crates/azure_storage_queue                                          |
| 源代码   | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/storage/azure_storage_queue |

## 局限性

- 仅当任务与上游来源及本地项目上下文明确匹配时才使用本技能。
- 在应用变更之前，请验证命令、生成的代码、依赖项、凭据以及外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。
