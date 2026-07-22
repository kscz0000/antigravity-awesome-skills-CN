# ORM 选型（2025）

> 选型应基于部署环境与开发体验需求。

## 决策树

```
What's the context?
│
├── Edge deployment / Bundle size matters
│   └── Drizzle (smallest, SQL-like)
│
├── Best DX / Schema-first
│   └── Prisma (migrations, studio)
│
├── Maximum control
│   └── Raw SQL with query builder
│
└── Python ecosystem
    └── SQLAlchemy 2.0 (async support)
```

## 对比

| ORM | 最佳场景 | 权衡 |
|-----|----------|------------|
| **Drizzle** | 边缘、TypeScript | 较新，示例较少 |
| **Prisma** | 开发体验、Schema 管理 | 较重，不适合边缘 |
| **Kysely** | 类型安全的 SQL 构建器 | 需手动管理迁移 |
| **原生 SQL** | 复杂查询、精细控制 | 需手动处理类型安全 |
