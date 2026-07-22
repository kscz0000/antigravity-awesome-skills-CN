# Postgres 规则编写指南

本文档为创建适用于 AI 智能体和 LLM 的 Postgres 最佳实践规则提供指导。

## 核心原则

### 1. 具体的转换模式

展示精确的 SQL 改写。避免空泛的建议。

**好的：** "用 `WHERE id = ANY(ARRAY[...])` 代替 `WHERE id IN (SELECT ...)`"
**差的：** "设计好的 Schema"

### 2. 错误优先结构

始终先展示有问题的模式，再给出方案。这能训练智能体识别反模式。

```markdown
**错误（顺序查询）：** [错误示例]

**正确（批量查询）：** [正确示例]
```

### 3. 量化影响

包含具体指标。帮助智能体确定修复优先级。

**好的：** "查询快 10 倍"、"索引小 50%"、"消除 N+1"
**差的：** "更快"、"更好"、"更高效"

### 4. 示例自包含

示例应完整且可运行（或接近可运行）。需要上下文时包含 `CREATE TABLE`。

```sql
-- 需要时包含表定义以提高清晰度
CREATE TABLE users (
  id bigint PRIMARY KEY,
  email text NOT NULL,
  deleted_at timestamptz
);

-- 然后展示索引
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;
```

### 5. 语义化命名

使用有意义的表名/列名。名称对 LLM 承载语义意图。

**好的：** `users`、`email`、`created_at`、`is_active`
**差的：** `table1`、`col1`、`field`、`flag`

---

## 代码示例标准

### SQL 格式

```sql
-- 使用小写关键字，清晰的格式
CREATE INDEX CONCURRENTLY users_email_idx
  ON users(email)
  WHERE deleted_at IS NULL;

-- 不要拥挤或全大写
CREATE INDEX CONCURRENTLY USERS_EMAIL_IDX ON USERS(EMAIL) WHERE DELETED_AT IS NULL;
```

### 注释

- 解释 _为什么_，而非 _是什么_
- 突出性能影响
- 指出常见陷阱

### 语言标签

- `sql` — 标准 SQL 查询
- `plpgsql` — 存储过程/函数
- `typescript` — 应用代码（需要时）
- `python` — 应用代码（需要时）

---

## 何时包含应用代码

**默认：仅 SQL**

大多数规则应聚焦纯 SQL 模式。这保持了示例的可移植性。

**以下情况包含应用代码：**

- 连接池配置
- 应用上下文中的事务管理
- ORM 反模式（Prisma/TypeORM 中的 N+1）
- Prepared statement 用法

**混合示例格式：**

````markdown
**错误（应用中的 N+1）：**

```typescript
for (const user of users) {
  const posts = await db.query("SELECT * FROM posts WHERE user_id = $1", [
    user.id,
  ]);
}
```
````

**正确（批量查询）：**

```typescript
const posts = await db.query("SELECT * FROM posts WHERE user_id = ANY($1)", [
  userIds,
]);
```

---

## 影响等级指南

| 等级 | 改善幅度 | 适用场景 |
|------|---------|---------|
| **CRITICAL** | 10-100x | 缺失索引、连接耗尽、大表顺序扫描 |
| **HIGH** | 5-20x | 索引类型错误、分区不当、缺失覆盖索引 |
| **MEDIUM-HIGH** | 2-5x | N+1 查询、低效分页、RLS 优化 |
| **MEDIUM** | 1.5-3x | 冗余索引、查询计划不稳定 |
| **LOW-MEDIUM** | 1.2-2x | VACUUM 调优、配置调整 |
| **LOW** | 增量改善 | 高级模式、边界情况 |

---

## 参考标准

**主要来源：**

- Postgres 官方文档
- Supabase 文档
- Postgres wiki
- 知名博客（2ndQuadrant、Crunchy Data）

**格式：**

```markdown
Reference:
[Postgres 索引](https://www.postgresql.org/docs/current/indexes.html)
```

---

## 提交前检查清单

- [ ] 标题清晰且面向操作
- [ ] 影响等级与性能提升匹配
- [ ] impactDescription 包含量化指标
- [ ] 说明简洁（1-2 句）
- [ ] 至少有 1 个**错误** SQL 示例
- [ ] 至少有 1 个**正确** SQL 示例
- [ ] SQL 使用语义化命名
- [ ] 注释解释 _为什么_，而非 _是什么_
- [ ] 如适用，提及权衡取舍
- [ ] 包含参考链接
- [ ] `npm run validate` 通过
- [ ] `npm run build` 生成正确输出
