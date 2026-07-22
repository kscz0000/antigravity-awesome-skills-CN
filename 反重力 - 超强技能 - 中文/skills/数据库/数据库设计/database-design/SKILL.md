---
name: database-design
description: "数据库设计原则与决策。Schema 设计、索引策略、ORM 选型、无服务器数据库。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Database Design

> **学会思考，而不是复制 SQL 模式。**

## 🎯 选择性阅读规则

**只读取与请求相关的文件！** 查看内容地图，找到你需要的内容。

| 文件 | 描述 | 何时阅读 |
|------|------|----------|
| `database-selection.md` | PostgreSQL vs Neon vs Turso vs SQLite | 选择数据库时 |
| `orm-selection.md` | Drizzle vs Prisma vs Kysely | 选择 ORM 时 |
| `schema-design.md` | 规范化、主键、关系 | 设计 Schema 时 |
| `indexing.md` | 索引类型、复合索引 | 性能调优时 |
| `optimization.md` | N+1 问题、EXPLAIN ANALYZE | 查询优化时 |
| `migrations.md` | 安全迁移、无服务器数据库 | Schema 变更时 |

---

## ⚠️ 核心原则

- 不明确时询问用户的数据库偏好
- 根据上下文选择数据库/ORM
- 不要默认所有场景都用 PostgreSQL

---

## 决策检查清单

设计 Schema 之前：

- [ ] 是否询问过用户的数据库偏好？
- [ ] 是否为此上下文选择了合适的数据库？
- [ ] 是否考虑了部署环境？
- [ ] 是否规划了索引策略？
- [ ] 是否定义了关系类型？

---

## 反模式

❌ 简单应用默认使用 PostgreSQL（SQLite 可能就足够了）
❌ 跳过索引设计
❌ 在生产环境使用 SELECT *
❌ 当结构化数据更合适时存储 JSON
❌ 忽略 N+1 查询问题

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
