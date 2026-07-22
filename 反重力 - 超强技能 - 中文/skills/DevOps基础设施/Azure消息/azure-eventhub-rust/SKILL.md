---
name: azure-eventhub-rust
description: Azure Event Hubs Rust SDK，用于发送和接收事件、流式数据摄取。当用户要求'Azure Event Hubs Rust'、'Rust事件中心'、'Event Hubs SDK'、'事件流处理'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Event Hubs SDK for Rust

Azure Event Hubs 的客户端库——大数据流式平台和事件摄取服务。

## 安装

```sh
cargo add azure_messaging_eventhubs azure_identity
```

## 环境变量

```bash
EVENTHUBS_HOST=<namespace>.servicebus.windows.net
EVENTHUB_NAME=<eventhub-name>
```

## 核心概念

- **Namespace（命名空间）** — Event Hub 的容器
- **Event Hub（事件中心）** — 分区并行处理的事件流
- **Partition（分区）** — 有序的事件序列
- **Producer（生产者）** — 向 Event Hub 发送事件
- **Consumer（消费者）** — 从分区接收事件

## Producer Client（生产者客户端）

### 创建 Producer

```rust
use azure_identity::DeveloperToolsCredential;
use azure_messaging_eventhubs::ProducerClient;

let credential = DeveloperToolsCredential::new(None)?;
let producer = ProducerClient::builder()
    .open("<namespace>.servicebus.windows.net", "eventhub-name", credential.clone())
    .await?;
```

### 发送单个事件

```rust
producer.send_event(vec![1, 2, 3, 4], None).await?;
```

### 批量发送

```rust
let batch = producer.create_batch(None).await?;
batch.try_add_event_data(b"event 1".to_vec(), None)?;
batch.try_add_event_data(b"event 2".to_vec(), None)?;

producer.send_batch(batch, None).await?;
```

## Consumer Client（消费者客户端）

### 创建 Consumer

```rust
use azure_messaging_eventhubs::ConsumerClient;

let credential = DeveloperToolsCredential::new(None)?;
let consumer = ConsumerClient::builder()
    .open("<namespace>.servicebus.windows.net", "eventhub-name", credential.clone())
    .await?;
```

### 接收事件

```rust
// Open receiver for specific partition
let receiver = consumer.open_partition_receiver("0", None).await?;

// Receive events
let events = receiver.receive_events(100, None).await?;
for event in events {
    println!("Event data: {:?}", event.body());
}
```

### 获取 Event Hub 属性

```rust
let properties = consumer.get_eventhub_properties(None).await?;
println!("Partitions: {:?}", properties.partition_ids);
```

### 获取分区属性

```rust
let partition_props = consumer.get_partition_properties("0", None).await?;
println!("Last sequence number: {}", partition_props.last_enqueued_sequence_number);
```

## 最佳实践

1. **复用客户端** — 创建一次，发送多个事件
2. **使用批量发送** — 比逐条发送更高效
3. **检查批量容量** — `try_add_event_data` 在满时返回 false
4. **并行处理分区** — 每个分区可以独立消费
5. **使用消费者组** — 隔离不同的消费应用
6. **处理检查点** — 分布式消费者使用 `azure_messaging_eventhubs_checkpointstore_blob`

## Checkpoint Store（检查点存储，可选）

用于带检查点的分布式消费者：

```sh
cargo add azure_messaging_eventhubs_checkpointstore_blob
```

## 参考链接

| 资源 | 链接 |
|------|------|
| API 参考 | https://docs.rs/azure_messaging_eventhubs |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/eventhubs/azure_messaging_eventhubs |
| crates.io | https://crates.io/crates/azure_messaging_eventhubs |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
