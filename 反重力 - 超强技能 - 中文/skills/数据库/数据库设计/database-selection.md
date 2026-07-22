# 数据库选型（2025）

> 选型应基于上下文，而非默认选项。

## 决策树

```
What are your requirements?
│
├── Full relational features needed
│   ├── Self-hosted → PostgreSQL
│   └── Serverless → Neon, Supabase
│
├── Edge deployment / Ultra-low latency
│   └── Turso (edge SQLite)
│
├── AI / Vector search
│   └── PostgreSQL + pgvector
│
├── Simple / Embedded / Local
│   └── SQLite
│
└── Global distribution
    └── PlanetScale, CockroachDB, Turso
```

## 对比

| 数据库 | 最佳场景 | 权衡 |
|----------|----------|------------|
| **PostgreSQL** | 功能全面、复杂查询 | 需自行托管 |
| **Neon** | 无服务器 PG、数据库分支 | PG 复杂度仍在 |
| **Turso** | 边缘部署、低延迟 | 受限于 SQLite |
| **SQLite** | 简单、嵌入式、本地 | 单写者 |
| **PlanetScale** | MySQL、全球扩展 | 不支持外键 |

## 需要询问的问题

1. 部署环境是什么？
2. 查询复杂度如何？
3. 是否需要边缘/无服务器部署？
4. 是否需要向量搜索？
5. 是否需要全球分布？
