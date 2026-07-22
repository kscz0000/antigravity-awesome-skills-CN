---
name: azure-servicebus-rust
description: '面向 Rust 的 Azure Service Bus 客户端库。使用队列、主题和订阅发送与接收消息。触发词：service bus rust、ServiceBusClient rust、send message servicebus rust、receive message servicebus rust、queue rust messaging、topic subscription rust。'
risk: unknown
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-rust/skills/azure-servicebus-rust
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# 面向 Rust 的 Azure Service Bus 客户端库
## 使用时机

当你需要在 Rust 中使用 Azure Service Bus 客户端库时，可使用本技能。通过队列、主题与订阅发送与接收消息。触发词："service bus rust"、"ServiceBusClient rust"、"send message servicebus rust"、"receive message servicebus rust"、"queue rust messaging"、"topic subscription rust"。


Azure Service Bus 的客户端库——企业级消息代理，支持队列与发布订阅主题。

> **⚠️ 警告：** 本 crate 处于早期开发阶段，**不应**用于生产环境。API 可能随时变更且不再另行通知。

在以下场景中使用本技能：

- 应用需要通过 Azure Service Bus 从 Rust 发送或接收消息
- 需要使用队列实现竞争消费者模式的消息传递
- 需要使用主题与订阅实现发布订阅模式的消息传递
- 需要借助完成（completion）语义实现可靠的消息投递

> **重要提示：** 只能使用由 [azure-sdk](https://crates.io/users/azure-sdk) crates.io 用户发布的官方 `azure_messaging_servicebus` crate。**不得**使用非官方或社区发布的 crate。官方 crate 名称中带有下划线，且没有任何版本号为 0.21.0。

## 安装

```sh
cargo add azure_messaging_servicebus azure_identity tokio
```

> 如果你的代码直接使用了 `azure_core` 类型，请将 `azure_core` 添加到 `Cargo.toml`。如果仅使用 `azure_messaging_servicebus` 的 re-export，则对 `azure_core` 的直接依赖是可选的。

## 环境变量

```bash
SERVICEBUS_NAMESPACE=<namespace>.servicebus.windows.net # 必填 —— 完全限定命名空间
```

## 核心概念

| 概念          | 描述                                                     |
| ---------------- | --------------------------------------------------------------- |
| **Namespace（命名空间）**    | 所有消息传递组件的容器                          |
| **Queue（队列）**        | 基于竞争消费者模式的点对点消息传递               |
| **Topic（主题）**        | 发布订阅消息传递——一个发送者，多个订阅者      |
| **Subscription（订阅）** | 从主题接收消息                                  |
| **Message（消息）**      | 携带数据与元数据的包，具有 complete（完成）/abandon（放弃）语义 |

## 身份认证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_messaging_servicebus::ServiceBusClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 本地开发：使用 DeveloperToolsCredential。生产环境：请使用 ManagedIdentityCredential。
    let credential = DeveloperToolsCredential::new(None)?;
    let client = ServiceBusClient::builder()
        .open("your_namespace.servicebus.windows.net", credential.clone())
        .await?;
    Ok(())
}
```

## 核心工作流

### 向队列发送消息

```rust
use azure_identity::DeveloperToolsCredential;
use azure_messaging_servicebus::{ServiceBusClient, Message};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let client = ServiceBusClient::builder()
        .open("your_namespace.servicebus.windows.net", credential.clone())
        .await?;
    let sender = client.create_sender("my_queue", None).await?;

    let message = Message::from("Hello, Service Bus!");
    sender.send_message(message, None).await?;
    Ok(())
}
```

### 从队列接收消息

```rust
use azure_identity::DeveloperToolsCredential;
use azure_messaging_servicebus::ServiceBusClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let client = ServiceBusClient::builder()
        .open("your_namespace.servicebus.windows.net", credential.clone())
        .await?;
    let receiver = client.create_receiver("my_queue", None).await?;

    let messages = receiver.receive_messages(5, None).await?;
    for message in messages {
        println!("Received: {}", message.body_as_string()?);
        receiver.complete_message(&message, None).await?;
    }
    Ok(())
}
```

### 向主题发送消息

```rust
let sender = client.create_sender("my_topic", None).await?;
let message = Message::from("Hello, Topic subscribers!");
sender.send_message(message, None).await?;
```

### 从订阅接收消息

```rust
let receiver = client
    .create_receiver_for_subscription("my_topic", "my_subscription", None)
    .await?;

let messages = receiver.receive_messages(5, None).await?;
for message in messages {
    println!("Received: {}", message.body_as_string()?);
    receiver.complete_message(&message, None).await?;
}
```

## 消息结算

| 动作     | 用途                                            |
| ---------- | -------------------------------------------------- |
| `complete` | 将消息从队列中移除——表示处理成功   |
| `abandon`  | 释放锁——消息将变为可重新投递状态 |

处理成功后必须调用 complete，以避免消息被重新投递。

## RBAC 角色

对于 Entra ID 身份认证，请分配以下角色之一：

| 角色                              | 访问权限           |
| --------------------------------- | ---------------- |
| `Azure Service Bus Data Sender`   | 发送消息    |
| `Azure Service Bus Data Receiver` | 接收消息 |
| `Azure Service Bus Data Owner`    | 完全访问权限      |

## 最佳实践

1. **使用 `cargo add` 管理依赖，切勿直接编辑 `Cargo.toml`。** 应通过 cargo 命令添加与删除 Rust SDK 依赖，而非手动编辑清单文件。
2. **仅在直接导入 `azure_core` 类型时才添加 `azure_core`。** 如果代码中导入 `azure_core::http::Url`、`azure_core::http::RequestContent` 或 `azure_core::error::ErrorKind`，则需包含 `azure_core`；否则该直接依赖是可选的。
3. **使用 `DeveloperToolsCredential`** 进行本地开发，使用 **`ManagedIdentityCredential`** 进行生产部署——Rust 并不提供统一的 `DefaultAzureCredential` 类型
4. **切勿硬编码凭据**——应使用环境变量或托管标识
5. **分配 RBAC 角色**——确保身份拥有合适的 Service Bus 数据角色
6. **始终完成消息**——处理完成后调用 `complete_message` 将消息从队列中移除
7. **使用主题实现扇出**——当多个消费者需要接收相同消息时，请结合订阅使用主题
8. **本 crate 尚处预生产阶段**——API 可能变更；请在依赖管理工作流中通过 cargo 命令锁定依赖版本

## 参考链接

| 资源      | 链接                                                                                            |
| ------------- | ----------------------------------------------------------------------------------------------- |
| API 参考 | https://docs.rs/azure_messaging_servicebus/latest/azure_messaging_servicebus                    |
| crates.io     | https://crates.io/crates/azure_messaging_servicebus                                             |
| 源代码   | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/servicebus/azure_messaging_servicebus |

## 限制

- 仅当任务与上游来源及本地项目上下文清晰匹配时才使用本技能。
- 在应用变更前，请校验命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。