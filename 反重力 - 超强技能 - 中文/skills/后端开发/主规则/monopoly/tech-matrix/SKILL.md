---
name: tech-matrix
description: >
  monopoly 技术决策矩阵参考文档。涵盖数据库选型（SQL/NoSQL）、缓存选型、
  消息队列/事件流选型、API 协议、搜索引擎、对象存储、容器编排、负载均衡、可观测性栈和 CDN。
risk: safe
reports-to: monopoly
---

# MONOPOLY — 技术决策矩阵

## 目录
1. 数据库选型
2. 缓存选型
3. 消息队列 / 事件流
4. API 协议
5. 搜索引擎
6. 对象存储
7. 容器编排
8. 负载均衡器
9. 可观测性栈
10. CDN

---

## 1. 数据库选型

### 关系型（SQL）

| 数据库 | 最适合 | 避免场景 | 规模上限 |
|----------|----------|------------|---------------|
| **PostgreSQL** | 复杂查询、JSONB、GIS、强一致性、大多数默认场景 | 超高写入吞吐（>100K 写/s） | 单节点 ~10TB；水平扩展用 Citus |
| **MySQL / MariaDB** | 读密集应用、遗留系统、WordPress/Drupal 生态 | 复杂查询、大规模完整 ACID | ~10TB；分片用 Vitess |
| **CockroachDB** | 全球分布式 SQL、地理分区、多区域 | 简单单区域应用（大材小用） | PB 级 |
| **PlanetScale** | MySQL 兼容、无服务器、分支工作流 | 复杂 JOIN（设计上移除了外键） | 极高 — 基于 Vitess |
| **Amazon Aurora** | AWS 原生应用、托管 PostgreSQL/MySQL、高可用 | 非 AWS 环境 | 最高 128TB，15 个副本 |

### NoSQL

| 数据库 | 最适合 | 避免场景 | 规模上限 |
|----------|----------|------------|---------------|
| **MongoDB** | 灵活 Schema、文档模型、原型开发 | 需要 ACID 的金融事务 | 分片后 PB 级 |
| **DynamoDB** | 大规模键值、AWS 原生、无服务器、可预测延迟 | 复杂查询、即席分析、JOIN | 无限（AWS 托管） |
| **Cassandra** | 写密集、时序、宽列、地理分布 | 读密集且复杂查询 | PB 级；Apple、Netflix 在用 |
| **Redis** | 缓存、会话、排行榜、发布/订阅、限流 | 复杂模型的主数据存储 | 单节点 ~1TB；更多用集群 |
| **Elasticsearch** | 全文搜索、日志聚合、分析 | 主数据库（持久性风险） | 集群后 PB 级 |
| **InfluxDB** | 时序指标、IoT、监控数据 | 通用数据 | 极高写入吞吐 |
| **Neo4j** | 图数据、社交网络、推荐引擎、欺诈检测 | 非图数据（开销不值得） | 数十亿节点 |

### 决策框架

```
Is your data relational (joins, foreign keys, transactions)?
  YES → Start with PostgreSQL
  NO  → Continue below

Is your primary access pattern key-value?
  YES, need extreme scale → DynamoDB or Cassandra
  YES, need speed/cache → Redis

Is your data document-shaped (nested, flexible schema)?
  YES → MongoDB

Is it time-series (metrics, logs, IoT)?
  YES → InfluxDB or TimescaleDB

Is it graph (relationships are the data)?
  YES → Neo4j

Is it search?
  YES → Elasticsearch / OpenSearch
```

---

## 2. 缓存选型

| 技术 | 最适合 | 单节点最大 | 集群支持 |
|------------|----------|----------------|----------------|
| **Redis** | 会话、排行榜、发布/订阅、复杂数据结构、Lua 脚本 | ~1TB 内存 | 支持（Redis Cluster、Redis Sentinel） |
| **Memcached** | 简单键值、多线程、大对象缓存 | ~64GB 内存 | 支持（客户端分片） |
| **Varnish** | HTTP 反向代理缓存、整页缓存 | 受内存限制 | 有限 |
| **CloudFront / CDN** | 静态资源、全球边缘缓存 | 不适用（分布式） | 内置全球分发 |

**默认推荐：Redis** — 功能更多、生态更好、活跃开发。

仅在以下情况用 **Memcached**：需要多线程处理 CPU 密集型缓存负载，且不需要字符串以外的数据结构。

---

## 3. 消息队列 / 事件流

| 技术 | 模型 | 最适合 | 吞吐量 | 消息保留 |
|------------|-------|----------|------------|-----------|
| **Apache Kafka** | 基于日志的流 | 事件溯源、高吞吐管道、重放、审计 | 百万级消息/s | 天到永久 |
| **RabbitMQ** | AMQP 消息代理 | 任务队列、RPC、路由、扇出 | 50K–100K 消息/s | 直到被消费 |
| **AWS SQS** | 托管队列 | AWS 原生、简单任务队列、无服务器 | 极高（托管） | 最多 14 天 |
| **AWS SNS** | 发布/订阅通知 | 扇出到多个订阅者（邮件、短信、Lambda、SQS） | 极高（托管） | 无保留 |
| **Google Pub/Sub** | 托管流 | GCP 原生、全球、无服务器 | 极高（托管） | 最多 7 天 |
| **Redis Pub/Sub** | 内存发布/订阅 | 实时通知、低延迟、即发即忘 | 极高 | 无（不保留） |
| **NATS** | 轻量消息 | IoT、微服务、低延迟 | 极高 | JetStream 增加保留 |

### 决策矩阵

```
Need event replay / audit trail?
  YES → Kafka or Kinesis

Need simple task queue with retries and DLQ?
  AWS shop → SQS
  Self-hosted → RabbitMQ

Need real-time pub/sub with no persistence?
  Redis Pub/Sub or NATS

Need fan-out to multiple consumers?
  Kafka (consumer groups) or SNS → SQS fan-out

Need < 5 minutes guaranteed delivery, AWS-native, zero ops?
  SQS

Volume > 1 million messages/second?
  Kafka (self-hosted) or Kinesis (managed)
```

---

## 4. API 协议

| 协议 | 最适合 | 避免场景 |
|----------|----------|------------|
| **REST（HTTP/JSON）** | 公开 API、CRUD、浏览器客户端、简单性 | 需要强类型；高性能内部服务 |
| **GraphQL** | 复杂客户端数据需求、移动端（减少过度获取）、BFF 模式 | 简单 CRUD；复杂度不值得 |
| **gRPC（HTTP/2 + Protobuf）** | 内部微服务通信、低延迟、严格契约、流式 | 公开浏览器 API（需要 gRPC-web） |
| **WebSocket** | 实时双向（聊天、实时仪表盘、多人游戏） | 单向服务端推送（改用 SSE） |
| **SSE（Server-Sent Events）** | 服务端 → 客户端推送（通知、实时动态） | 双向通信 |
| **GraphQL Subscriptions** | 需与 GraphQL Schema 保持一致的实时功能 | 简单推送场景 |

**默认推荐：**
- 对外 / 公开：**REST**
- 内部服务间：**gRPC**
- 实时功能：**WebSocket** 或 **SSE**

---

## 5. 搜索引擎

| 技术 | 最适合 | 避免场景 |
|------------|----------|------------|
| **Elasticsearch** | 全文搜索、日志分析（ELK）、复杂聚合 | 简单查找；运维开销高 |
| **OpenSearch** | AWS 原生 Elasticsearch 替代 | 非 AWS 偏好环境 |
| **Typesense** | 简单、快速全文搜索、容错、易运维 | 大规模复杂聚合 |
| **Algolia** | 托管搜索即服务、快速接入、优秀 UI | 高量（昂贵）；偏好自建 |
| **Meilisearch** | 自建、开发者友好、快速相关性 | 企业级分析 |
| **PostgreSQL FTS** | 基础全文搜索、已在使用 PostgreSQL | 高相关性需求或大数据集 |

**经验法则：** 100 万文档以下用 PostgreSQL FTS。超过则用 Typesense 或 Elasticsearch。

---

## 6. 对象存储

| 服务 | 最适合 | 出站成本 |
|---------|----------|------------|
| **AWS S3** | AWS 原生应用、事实标准、庞大生态 | $0.09/GB（较贵） |
| **Cloudflare R2** | S3 兼容、**零出站成本**、全球 | $0.00 出站 |
| **GCS** | GCP 原生 | $0.12/GB |
| **Azure Blob** | Azure 原生 | $0.087/GB |
| **Backblaze B2** | 成本敏感、S3 兼容 | 与 Cloudflare 搭配免费 |
| **MinIO** | 自建 S3 兼容 | 自管理 |

**成本优化提示：** 面向用户的媒体分发用 **Cloudflare R2**（零出站）。内部/AWS 集成存储用 **S3**。

---

## 7. 容器编排

| 技术 | 最适合 | 避免场景 |
|------------|----------|------------|
| **Kubernetes（K8s）** | 大团队、复杂部署、多云、完全控制 | 小团队（运维开销很高） |
| **AWS ECS + Fargate** | AWS 原生、无服务器容器、比 K8s 简单 | 多云或需要 K8s 生态工具 |
| **AWS EKS** | AWS 上的托管 K8s、两全其美 | 小团队；Fargate 可能就够了 |
| **GKE（Google）** | 最佳托管 K8s、GCP 原生、Autopilot 模式 | 非 GCP 环境 |
| **Docker Compose** | 本地开发、小型单服务器部署 | 任何有规模的生产环境 |
| **Nomad** | HashiCorp 生态、比 K8s 简单、多工作负载 | 需要 K8s 生态工具 |

**初创默认：** ECS + Fargate（零集群管理）。
**扩容默认：** 团队 >5 人或服务 >10 个时用 EKS 或 GKE。

---

## 8. 负载均衡器

| 技术 | 层级 | 最适合 |
|------------|-------|----------|
| **AWS ALB** | L7（HTTP/HTTPS） | AWS 应用、基于路径路由、WebSocket、HTTP/2 |
| **AWS NLB** | L4（TCP/UDP） | 超低延迟、静态 IP、非 HTTP 协议 |
| **GCP GLB** | L7 全局 | GCP 应用、全局任播、全球单 IP |
| **Nginx** | L4/L7 | 自建、反向代理、灵活配置 |
| **HAProxy** | L4/L7 | 高性能自建、高级路由 |
| **Cloudflare** | L7 全局 + DDoS | DDoS 防护 + CDN + 负载均衡一体 |
| **Traefik** | L7 | Kubernetes 原生、自动 SSL、服务发现 |

---

## 9. 可观测性栈

### 指标
| 工具 | 最适合 |
|------|----------|
| **Prometheus + Grafana** | 自建、开源、Kubernetes 原生 |
| **Datadog** | 托管、APM + 基础设施 + 日志统一、昂贵 |
| **CloudWatch** | AWS 原生、零设置、与 AWS 服务集成 |
| **New Relic** | APM 为主、适合应用层洞察 |

### 日志
| 工具 | 最适合 |
|------|----------|
| **ELK Stack**（Elasticsearch + Logstash + Kibana） | 自建、强大、高量 |
| **Loki + Grafana** | 轻量、Kubernetes 原生、便宜 |
| **Splunk** | 企业级、合规、昂贵 |
| **AWS CloudWatch Logs** | AWS 原生、零设置 |
| **Datadog Logs** | 与指标统一、昂贵 |

### 分布式链路追踪
| 工具 | 最适合 |
|------|----------|
| **Jaeger** | 开源、Kubernetes 原生、OpenTelemetry |
| **Zipkin** | 简单、轻量、良好集成 |
| **AWS X-Ray** | AWS 原生、与 Lambda/ECS 集成 |
| **Datadog APM** | 托管、与指标和日志统一 |
| **Honeycomb** | 高基数事件驱动可观测性 |

**推荐开源栈：** Prometheus + Grafana + Loki + Jaeger（均通过 OpenTelemetry 集成）
**推荐托管栈：** Datadog（贵但统一）或 Grafana Cloud

---

## 10. CDN

| 技术 | 最适合 | 边缘节点数 |
|------------|----------|----------------|
| **Cloudflare** | DDoS 防护 + CDN + DNS、最佳免费套餐、边缘计算 | 300+ |
| **AWS CloudFront** | AWS 原生、深度集成 S3 和 API 网关 | 450+ |
| **Akamai** | 企业级、最高性能、昂贵 | 4000+ |
| **Fastly** | 实时清除、流式、VCL 定制 | 90+ |
| **Vercel Edge / Netlify** | Jamstack、前端优先、零配置 | 100+ |

**默认推荐：** 大多数场景用 Cloudflare（性价比最佳、包含 DDoS、免费 SSL、Workers 边缘计算）。

---

## 规模基准快速参考

| 技术 | 写入吞吐量 | 读取吞吐量 | 备注 |
|------------|-----------------|----------------|-------|
| PostgreSQL（单节点） | ~10K 写/s | ~50K 读/s | 使用连接池 |
| PostgreSQL（含副本） | ~10K 写/s | ~200K 读/s | 4 个副本 |
| MySQL（单节点） | ~15K 写/s | ~60K 读/s | |
| Cassandra | ~1M 写/s | ~500K 读/s | 10 节点集群 |
| Redis | ~1M 操作/s | ~1M 操作/s | 单节点内存 |
| Kafka | ~1M 消息/s | ~1M 消息/s | 每分区 |
| Elasticsearch | ~50K 文档/s | ~10K 查询/s | 每节点 |
| MongoDB | ~50K 写/s | ~100K 读/s | 每副本集 |

*所有基准数据为近似值，严重依赖硬件、负载大小和查询复杂度。*


## 局限性
- 本文档为参考性质，可能未覆盖所有边界情况。在生产环境前务必验证架构方案。
