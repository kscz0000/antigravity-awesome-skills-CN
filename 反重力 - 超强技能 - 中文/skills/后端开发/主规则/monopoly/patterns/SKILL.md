---
name: patterns
description: >
  monopoly 设计模式参考文档。涵盖 CQRS、事件溯源、Saga、熔断器、舱壁、绞杀者无花果、
  发件箱、一致性哈希、背压、领导者选举、两阶段提交等分布式系统设计模式。
risk: safe
reports-to: monopoly
---

# MONOPOLY — 设计模式深入解析

## 目录
1. CQRS
2. Event Sourcing
3. Saga 模式
4. Circuit Breaker
5. Bulkhead
6. Strangler Fig
7. Sidecar / 服务网格
8. Outbox 模式
9. 一致性哈希
10. 背压
11. 领导者选举
12. 两阶段提交

---

## 1. CQRS（命令查询职责分离）

**是什么：** 将读模型（Query）与写模型（Command）拆分到不同的服务、数据库或代码路径。

**何时使用：**
- 读负载是写负载的 10 倍以上（大多数 Web 应用）
- 读查询是对写入数据的复杂聚合
- 需要独立优化读写路径
- 领域模型复杂（DDD 上下文）

**实现方式：**
```
Write Path:  Client → Command API → Write DB (normalized, PostgreSQL)
Read Path:   Client → Query API  → Read DB (denormalized, Redis / Elasticsearch)
Sync:        Write DB → CDC (Debezium) → Message Queue → Read DB updater
```

**权衡：**
- ✅ 独立扩缩容读写
- ✅ 为每种操作类型优化 Schema
- ❌ 读写模型之间的最终一致性
- ❌ 复杂度增加；需要维护两个模型

**实际案例：** Amazon（订单服务）、LinkedIn（信息流）

---

## 2. Event Sourcing（事件溯源）

**是什么：** 将状态存储为一系列不可变事件，而非当前状态。通过重放事件重建当前状态。

**何时使用：**
- 完整审计追踪是合规要求（金融科技、医疗）
- 需要重放历史用于调试或分析
- 复杂领域，状态转换很多
- 需要从同一数据派生多个读投影

**实现方式：**
```
Event Store: append-only log (Kafka, EventStoreDB)
Snapshots:   periodic snapshots to speed up state rebuild
Projections: consumers build read models from events
```

**权衡：**
- ✅ 完整的审计历史；天然适合合规
- ✅ 可重放和时间旅行调试
- ❌ 查询当前状态需要维护投影
- ❌ 事件 Schema 演进困难
- ❌ 长期存储开销大

---

## 3. Saga 模式

**是什么：** 通过一系列本地事务管理跨微服务的分布式事务，每个事务发布一个事件。如果某步失败，补偿事务撤销之前的步骤。

**两种变体：**
- **编排式（Choreography）：** 各服务自主响应事件（去中心化）
- **协调式（Orchestration）：** 中心 Saga 协调器协调各步骤（中心化）

**何时使用：**
- 跨服务的工作流，无法实现跨服务 ACID
- 长时间运行的业务事务（下单 → 支付 → 库存 → 发货）
- 需要跨服务边界的回滚

**编排式示例：**
```
OrderService creates order →
  [event: OrderCreated] →
    PaymentService charges card →
      [event: PaymentProcessed] →
        InventoryService reserves stock →
          [event: StockReserved] →
            ShippingService books courier
```

**补偿事务（失败时）：**
```
ShippingService fails →
  [event: ShippingFailed] →
    InventoryService releases stock →
      PaymentService refunds card →
        OrderService marks order failed
```

**权衡：**
- ✅ 无分布式锁；高可用
- ✅ 跨服务扩展性好
- ❌ 难以调试；需要分布式链路追踪
- ❌ 补偿事务正确实现很复杂

---

## 4. Circuit Breaker（熔断器）

**是什么：** 监控服务调用的代理。如果失败率超过阈值，熔断器"打开"，调用快速失败而非等待超时。

**状态：**
```
CLOSED  → calls pass through; monitor failure rate
OPEN    → calls fail immediately; no calls to downstream
HALF-OPEN → let a probe call through; if success, close; if fail, stay open
```

**何时使用：**
- 调用任何外部服务（支付网关、短信、邮件）
- 微服务之间互相调用
- 防止下游慢时超时级联

**实现工具：** Hystrix（已弃用）、Resilience4j、Polly（.NET）、Envoy 代理

**阈值（起点）：**
- 10 次请求中失败率超 50% 时打开
- 保持打开 30 秒
- 半开：允许 1 个探测请求

**权衡：**
- ✅ 防止级联故障
- ✅ 给下游恢复时间
- ❌ 监控增加延迟开销
- ❌ 熔断打开时需要降级行为

---

## 5. Bulkhead（舱壁）

**是什么：** 隔离组件，使一个组件的故障不会消耗其他组件的资源。得名于船体中的水密舱壁。

**类型：**
- **线程池舱壁：** 每个服务调用使用独立线程池
- **信号量舱壁：** 限制每个服务的并发调用数
- **进程舱壁：** 每种服务类型使用独立进程/容器

**何时使用：**
- 多租户共享基础设施（SaaS）
- 某个慢服务占满所有连接池
- 保护关键服务不被非关键服务饿死

**示例：**
```
Without bulkhead:
  [Recommendation Service hangs] → fills shared thread pool → [Payment Service starves]

With bulkhead:
  [Recommendation Service hangs] → fills its own thread pool (10 threads) → [Payment Service unaffected, has its own 50 threads]
```

---

## 6. Strangler Fig 模式（绞杀者无花果）

**是什么：** 逐步替换遗留单体，将新功能路由到新微服务，同时让单体继续服务未变更的功能。

**迁移步骤：**
```
Phase 1: Deploy proxy in front of monolith (no user impact)
Phase 2: Route one feature to new microservice
Phase 3: Verify; deprecate that feature in monolith
Phase 4: Repeat for each feature
Phase 5: Monolith is empty; decommission
```

**何时使用：**
- 将遗留单体迁移到微服务
- 无法一次性重写（风险太大）
- 迁移期间需要持续交付新功能

**权衡：**
- ✅ 零停机迁移
- ✅ 风险递增
- ❌ 迁移期间双重维护负担（单体 + 新服务）
- ❌ 代理增加延迟；需要仔细管理

---

## 7. Outbox 模式（发件箱）

**是什么：** 解决双写问题（同时写数据库和发布到队列）——在同一个数据库事务中把事件写入"发件箱"表，然后由独立的中继进程将其投递到队列。

**解决的问题：**
```
❌ WRONG (dual-write race):
  BEGIN;
  UPDATE orders SET status='paid';
  COMMIT;
  // Crash here → event never published, DB and queue are inconsistent
  publish(PaymentProcessed);
```

```
✅ CORRECT (outbox):
  BEGIN;
  UPDATE orders SET status='paid';
  INSERT INTO outbox (event_type, payload) VALUES ('PaymentProcessed', {...});
  COMMIT;
  // Relay process reads outbox and publishes to Kafka
  // At-least-once delivery guaranteed; make consumers idempotent
```

**中继选项：** Debezium（CDC）、轮询中继、事务日志追踪

---

## 8. 一致性哈希（Consistent Hashing）

**是什么：** 一种哈希方案，添加或删除节点时只需重新映射 K/N 个键（K = 键数，N = 节点数），而非重新映射所有键。

**何时使用：**
- 在 Redis 集群节点间分配缓存键
- 在分布式系统中将请求路由到服务器
- 在数据库节点间分区数据

**虚拟节点：** 在哈希环上为每个物理节点分配多个位置，确保节点较少时也能均匀分布。

---

## 9. 背压（Backpressure）

**是什么：** 消费者向生产者发出减速信号的机制，防止内存耗尽和级联故障。

**策略：**
- **丢弃：** 丢弃溢出消息（适用于指标、日志）
- **缓冲：** 排队到上限，然后阻塞或丢弃
- **阻塞：** 生产者等待消费者赶上（最简单，可能导致超时）
- **限流：** 在入口处限制生产者速率

**何时使用：**
- 消息队列消费者慢于生产者
- 实时数据管道摄入突增
- 对上游客户端的 API 限流

---

## 10. 领导者选举（Leader Election）

**是什么：** 在分布式系统中，选举一个节点执行特权任务（例如写入数据库、发送定时任务、协调工作）。

**算法：**
- **Raft：** etcd、CockroachDB、Consul 使用。实用且理解充分。
- **ZooKeeper（ZAB）：** Kafka、HBase 使用。成熟但运维负担重。
- **Bully 算法：** 简单；最高 ID 胜出。不具备容错性。

**何时使用：**
- 定时任务只应运行一次（替代 cron）
- 主/副本数据库故障转移协调
- 分布式锁管理

**工具：** etcd、ZooKeeper、Consul、Redis（Redlock — 谨慎使用）

---

## 11. 两阶段提交（2PC）

**是什么：** 一种分布式算法，确保事务中的所有参与者要么全部提交，要么全部中止。

**阶段：**
```
Phase 1 (Prepare): Coordinator asks all participants "can you commit?"
  All say YES → proceed to Phase 2
  Any says NO → abort

Phase 2 (Commit): Coordinator tells all participants to commit
```

**何时使用（慎用）：**
- 跨服务强一致性是绝对要求
- 数据丢失是灾难性的（金融结算）

**为何避免：**
- 协调器是单点故障
- 参与者故障时会阻塞
- 竞争下吞吐量很低
- 大多数微服务架构中优先使用 Saga 模式

---

## 12. Read-Through / Write-Through / Write-Behind 缓存

**Read-Through（读透传）：**
```
Client → Cache (miss) → Cache fetches from DB → Returns to client
```
缓存未命中时自动填充。对客户端简单。风险：冷启动。

**Write-Through（写透传）：**
```
Client → Cache → Cache writes to DB synchronously → Confirms
```
强一致性。写入延迟较高。适合对一致性有要求的读密集场景。

**Write-Behind / Write-Back（写回）：**
```
Client → Cache → Confirms immediately → Async flush to DB
```
写入延迟极低。缓存刷新前宕机会丢数据。适合高吞吐计数器、分析。

**Cache-Aside（懒加载）：**
```
Client → Cache (miss) → Client fetches from DB → Client writes to Cache
```
最常见。应用自行管理缓存逻辑。风险：冷启动时的惊群效应。


## 局限性
- 本文档为参考性质，可能未覆盖所有边界情况。在生产环境前务必验证架构方案。
