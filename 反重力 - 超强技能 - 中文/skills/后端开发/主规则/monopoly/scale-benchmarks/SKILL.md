---
name: scale-benchmarks
description: >
  monopoly 规模基准与估算公式参考文档。涵盖用户到 RPS 转换、存储估算、带宽估算、
  常用技术的规模极限、按用户规模的容量规划、SLO 目标和延迟预算。
risk: safe
reports-to: monopoly
---

# MONOPOLY — 规模基准与估算公式

## 快速估算公式

### 用户 → RPS 转换
```
Requests per second (avg) = DAU × avg_requests_per_user_per_day / 86400
Requests per second (peak) = avg_RPS × peak_multiplier

Peak multipliers by app type:
  Social media:      5–10×
  E-commerce:        3–5× (higher during sales)
  News / media:      10–20× (breaking news spike)
  B2B SaaS:          2–3× (business hours spike)
  Gaming:            5–15× (event-driven)
```

### 存储估算
```
Storage per day    = requests_per_day × avg_payload_size
Storage per year   = storage_per_day × 365
With replication   = storage_per_year × replication_factor (3× typical)
With CDN/cache     = reduce by cache_hit_ratio (80% hit = 20% origin load)

Common payload sizes:
  Tweet / short text:    500B
  Social post with text: 2KB
  Profile data:          5KB
  Image (compressed):    200KB–2MB
  Video (per minute):    50MB (720p), 150MB (1080p)
  API JSON response:     1–20KB
```

### 带宽估算
```
Inbound bandwidth  = avg_request_size × RPS
Outbound bandwidth = avg_response_size × RPS

Convert: 1 Gbps = 125 MB/s
         10 Gbps = 1.25 GB/s
```

---

## 常用技术的已知规模极限

### 数据库

| 技术 | 单节点写入 | 读取（含副本） | 建议分片/集群触发条件 |
|------------|-------------------|----------------------|----------------------------------|
| PostgreSQL | ~5K–20K 写/s | ~50K–200K 读/s | >5TB 数据或 >20K 写/s |
| MySQL | ~10K–25K 写/s | ~60K–250K 读/s | >5TB 或 >25K 写/s |
| MongoDB | ~20K–50K 写/s | ~50K–100K 读/s | >100GB 或 >50K 写/s |
| Cassandra | ~200K–1M 写/s | ~200K–500K 读/s | 几乎不需要显式分片 |
| DynamoDB | 无限（托管） | 无限（托管） | 使用预配置容量模式 |
| Redis | ~500K–1M 操作/s | 同上 | >50GB 数据或需要集群 |
| Elasticsearch | ~10K–50K 文档/s | ~1K–10K 查询/s | 每索引 >1 亿文档 |

### 队列 / 流

| 技术 | 最大吞吐量 | 最大消费者 | 消息保留 |
|------------|----------------|---------------|-----------|
| Kafka | 每集群 1M+ 消息/s | 无限消费者组 | 可配置（天到永久） |
| RabbitMQ | ~50K–100K 消息/s | 受连接数限制 | 直到被消费 |
| SQS 标准队列 | 无限（AWS 托管） | 无限 | 14 天 |
| SQS FIFO | 每队列 3K 消息/s | 按组 | 14 天 |
| Redis Pub/Sub | ~1M 消息/s | 受订阅者限制 | 无（即发即忘） |

### 缓存

| 技术 | 单节点最大内存 | 最大吞吐量 | 延迟 |
|------------|--------------------|--------------|----|
| Redis | ~1TB 内存 | ~1M 操作/s | <1ms |
| Memcached | ~64GB 内存 | ~1M 操作/s | <1ms |
| 进程内（Caffeine/Guava） | JVM 堆 | 无限（本地） | <0.1ms |

---

## 按用户规模的容量规划

### 1K DAU
```
Avg RPS:       ~1–5 RPS
Peak RPS:      ~10–50 RPS
DB size/year:  ~10–50GB
Infra needed:  Single server, managed DB (RDS t3.medium), basic CDN
Monthly cost:  $50–200
```

### 10K DAU
```
Avg RPS:       ~10–50 RPS
Peak RPS:      ~100–500 RPS
DB size/year:  ~100–500GB
Infra needed:  2–4 app servers, RDS r5.large, Redis t3.medium, CDN
Monthly cost:  $300–800
```

### 100K DAU
```
Avg RPS:       ~100–500 RPS
Peak RPS:      ~1K–5K RPS
DB size/year:  ~1–5TB
Infra needed:  ASG (5–10 app servers), RDS r5.xlarge + 2 replicas, Redis cluster, CDN, ALB
Monthly cost:  $2K–8K
```

### 1M DAU
```
Avg RPS:       ~1K–5K RPS
Peak RPS:      ~10K–50K RPS
DB size/year:  ~10–50TB
Infra needed:  ASG (20–50 servers), DB sharding or Aurora, Redis cluster, Kafka, CDN, WAF
Monthly cost:  $20K–80K
```

### 10M DAU
```
Avg RPS:       ~10K–50K RPS
Peak RPS:      ~100K–500K RPS
DB size/year:  ~100–500TB
Infra needed:  Multi-region, microservices, distributed DB (Cassandra/CockroachDB), full CDN, dedicated SRE
Monthly cost:  $200K–2M+
```

---

## 常见 SLO 目标

| 等级 | 可用性 | 每月允许停机时间 |
|------|-------------|--------------------------|
| 99% | 基础 | 7.2 小时/月 |
| 99.9%（三个九） | 标准生产 | 43.8 分钟/月 |
| 99.95% | 重要服务 | 21.9 分钟/月 |
| 99.99%（四个九） | 关键服务 | 4.38 分钟/月 |
| 99.999%（五个九） | 电信 / 支付 | 26 秒/月 |

**达到四个九需要：** 多可用区部署、自动故障转移、零停机部署、混沌工程、7×24 值班。

---

## 延迟预算指南

```
User perceived latency targets:
  < 100ms  → Feels instant
  100–300ms → Acceptable for most interactions
  300ms–1s → Noticeable; optimize if possible
  > 1s     → Frustrating; unacceptable for critical paths

Network latency by distance (approximate):
  Same datacenter:    0.5ms
  Same region (AZ):   1–2ms
  Cross-region US:    30–60ms
  US to Europe:       80–120ms
  US to Asia:         150–250ms

Database query targets:
  Simple key-value:   < 1ms (cache)
  Simple DB query:    < 5ms
  Complex query:      < 50ms
  Reporting query:    < 500ms (async if > 1s)
```


## 局限性
- 本文档为参考性质，可能未覆盖所有边界情况。在生产环境前务必验证架构方案。
