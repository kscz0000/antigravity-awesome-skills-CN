# Postgres 参考文档编写指南

本文档提供编写有效 Postgres 最佳实践参考的指南，使其适用于 AI 代理和 LLM。

## 核心原则

### 1. 具体的转换模式

展示精确的 SQL 重写。避免抽象的建议。

**好：** "使用 `WHERE id = ANY(ARRAY[...])` 代替 `WHERE id IN (SELECT ...)`"
**差：** "设计好的模式"

### 2. 错误优先结构

始终先展示有问题的模式，然后展示解决方案。这训练代理识别反模式。

```markdown
**错误做法（顺序查询）：** [错误示例]

**正确做法（批量查询）：** [正确示例]
```

### 3. 量化影响

包含具体指标。帮助代理优先处理修复。

**好：** "查询快 10 倍"，"索引小 50%"，"消除 N+1"
**差：** "更快"，"更好"，"更高效"

### 4. 自包含示例

示例应当完整且可运行（或接近可运行）。需要上下文时包含 `CREATE TABLE`。

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

使用有意义的表名/列名。名称对 LLM 传递意图。

**好：** `users`、`email`、`created_at`、`is_active`
**差：** `table1`、`col1`、`field`、`flag`

---

## 代码示例标准

### SQL 格式化

```sql
-- 使用小写关键字，清晰的格式
CREATE INDEX CONCURRENTLY users_email_idx
  ON users(email)
  WHERE deleted_at IS NULL;

-- 不要挤在一起或全大写
CREATE INDEX CONCURRENTLY USERS_EMAIL_IDX ON USERS(EMAIL) WHERE DELETED_AT IS NULL;
```

### 注释

- 解释_为什么_，而不是_什么_
- 强调性能影响
- 指出常见陷阱

### 语言标签

- `sql` - 标准 SQL 查询
- `plpgsql` - 存储过程/函数
- `typescript` - 应用代码（需要时）
- `python` - 应用代码（需要时）

---

## 何时包含应用代码

**默认：仅 SQL**

大多数参考应聚焦于纯 SQL 模式。这保持示例的可移植性。

**在以下情况包含应用代码：**

- 连接池配置
- 应用上下文中的事务管理
- ORM 反模式（Prisma/TypeORM 中的 N+1）
- 预处理语句的使用

**混合示例格式：**

````markdown
**错误做法（应用中的 N+1）：**

```typescript
for (const user of users) {
  const posts = await db.query("SELECT * FROM posts WHERE user_id = $1", [
    user.id,
  ]);
}
```
````

**正确做法（批量查询）：**

```typescript
const posts = await db.query("SELECT * FROM posts WHERE user_id = ANY($1)", [
  userIds,
]);
```

---

## 影响等级指南

| 等级 | 改善幅度 | 适用场景 |
|-------|-------------|----------|
| **CRITICAL** | 10-100 倍 | 缺失索引、连接耗尽、大表上的顺序扫描 |
| **HIGH** | 5-20 倍 | 错误的索引类型、糟糕的分区、缺失覆盖索引 |
| **MEDIUM-HIGH** | 2-5 倍 | N+1 查询、低效分页、RLS 优化 |
| **MEDIUM** | 1.5-3 倍 | 冗余索引、查询计划不稳定 |
| **LOW-MEDIUM** | 1.2-2 倍 | VACUUM 调优、配置调整 |
| **LOW** | 渐进式 | 高级模式、边界情况 |

---

## 参考标准

**主要来源：**

- 官方 Postgres 文档
- Supabase 文档
- Postgres wiki
- 知名博客（2ndQuadrant、Crunchy Data）

**格式：**

```markdown
参考：
[Postgres 索引](https://www.postgresql.org/docs/current/indexes.html)
```

---

## 审查清单

提交参考前：

- [ ] 标题清晰且行动导向
- [ ] 影响等级与性能提升匹配
- [ ] impactDescription 包含量化数据
- [ ] 解释简洁（1-2 句话）
- [ ] 至少有 1 个**错误做法** SQL 示例
- [ ] 至少有 1 个**正确做法** SQL 示例
- [ ] SQL 使用语义化命名
- [ ] 注释解释_为什么_，而不是_什么_
- [ ] 如适用，提到了权衡
- [ ] 包含参考链接
- [ ] `pnpm test` 通过
