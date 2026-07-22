# 数据库迁移原则

> 面向零停机的安全迁移策略。

## 安全迁移策略

```
For zero-downtime changes:
│
├── Adding column
│   └── Add as nullable → backfill → add NOT NULL
│
├── Removing column
│   └── Stop using → deploy → remove column
│
├── Adding index
│   └── CREATE INDEX CONCURRENTLY (non-blocking)
│
└── Renaming column
    └── Add new → migrate data → deploy → drop old
```

## 迁移理念

- 永远不要一步到位地完成破坏性变更
- 先在数据副本上测试迁移
- 准备好回滚方案
- 尽可能在事务中执行

## 无服务器数据库

### Neon（无服务器 PostgreSQL）

| 特性 | 优势 |
|---------|---------|
| 缩容至零 | 节省成本 |
| 瞬时分支 | 开发/预览环境 |
| 完整 PostgreSQL | 兼容性 |
| 自动扩缩容 | 应对流量波动 |

### Turso（边缘 SQLite）

| 特性 | 优势 |
|---------|---------|
| 边缘节点 | 超低延迟 |
| 兼容 SQLite | 简单易用 |
| 慷慨的免费额度 | 控制成本 |
| 全球分布 | 性能保障 |
