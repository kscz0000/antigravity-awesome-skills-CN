---
name: saas-multi-tenant
description: "设计和实现多租户 SaaS 架构，涵盖行级安全、租户作用域查询、共享 schema 隔离，以及 PostgreSQL 和 TypeScript 中安全的跨租户管理端点模式。触发词：multi-tenant、多租户、租户隔离、行级安全、RLS、tenant isolation、tenant scoping、SaaS 架构、共享schema、跨租户管理"
risk: safe
source: community
date_added: "2026-03-28"
tags: [multi-tenancy, saas, row-level-security, postgresql, tenant-isolation]
tools: [claude, cursor, gemini]
---

# SaaS 多租户架构

## 何时使用此技能

- 用户正在构建多个客户共享同一数据库的 SaaS 应用
- 用户询问租户隔离、行级安全或数据泄露防护
- 用户需要将每条数据库查询限定到特定租户，而不手动编写 WHERE 子句
- 用户询问共享 schema vs 每租户 schema vs 每租户数据库的权衡取舍
- 用户正在实现需要跨租户访问数据的管理端点
- 用户需要在现有的单租户应用中添加 `tenant_id` 列
- 用户询问 PostgreSQL RLS 策略用于租户隔离
- 用户正在 Express、Fastify 或 Next.js API 路由中构建租户感知中间件

不适用场景：
- 用户构建的是没有共享基础设施的单用户应用
- 用户只询问认证而不涉及租户作用域（应使用认证技能）
- 用户需要通用数据库 schema 设计，无多租户需求

## 核心工作流

1. 确定租户模型。询问用户的规模预期和隔离需求。对于 1000 个租户以下的大多数 SaaS 应用，在每张表上加 `tenant_id` 列的共享 schema 是正确的默认方案。每租户 schema 会增加运维开销（迁移要执行 N 次）。每租户数据库只有在租户有合规性数据驻留要求时才合理。

2. 在每张租户作用域表中添加 `tenant_id`。该列必须为 `NOT NULL`，类型为 `UUID` 或 `TEXT`，并纳入每个复合索引。绝不允许缺少此列的租户作用域表存在——缺失的 `tenant_id` 就是潜在的数据泄露。

3. 配置 PostgreSQL 行级安全（RLS）。在每张租户作用域表上创建策略，通过 `current_setting('app.current_tenant_id')` 过滤行。这充当数据库级别的安全网——即使应用代码遗漏了 WHERE 子句，RLS 也会阻止跨租户读取。

4. 构建租户感知中间件。在每个请求开始时，从已认证的会话或 JWT claims 中提取 `tenant_id`。通过事务内的 `SET LOCAL app.current_tenant_id = '...'` 设置到数据库连接上。该请求中后续的所有查询自动继承租户作用域。

5. 对所有 ORM 查询进行租户作用域限定。使用 Prisma 时，应用全局中间件向每个 `findMany`、`findFirst`、`update` 和 `delete` 调用注入 `where: { tenantId }`。使用 Drizzle 时，创建包含租户过滤器的基础查询构建器。绝不要依赖开发人员手动添加过滤器。

6. 处理租户感知迁移。每个新表迁移都必须包含 `tenant_id` 列。编写 lint 规则或 CI 检查，拒绝任何创建表时缺少 `tenant_id` 的迁移，除非该表被显式标记为全局表（如 `plans`、`feature_flags`）。

7. 单独构建跨租户管理路由。跨租户聚合数据的管理端点必须通过 `SET LOCAL role = 'admin_bypass'` 或专用数据库角色显式绕过 RLS。这些路由必须受独立的管理认证流程保护——绝不要复用租户用户会话进行管理访问。

8. 实现租户配置。新客户注册时，创建租户记录、填充默认数据（角色、设置、引导状态）并分配创始用户。将此操作包装在数据库事务中，避免部分配置留下孤立记录。

## 示例

### 示例 1：用于租户隔离的 PostgreSQL RLS 策略

```sql
-- Enable RLS on the table
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;

-- Policy: users can only see rows where tenant_id matches the session variable
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Policy for INSERT: new rows must match the current tenant
CREATE POLICY tenant_insert ON projects
  FOR INSERT
  WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### 示例 2：按请求设置租户上下文的 Express 中间件

```typescript
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function tenantMiddleware(req, res, next) {
  const tenantId = req.auth?.tenantId; // extracted from JWT during auth
  if (!tenantId) return res.status(403).json({ error: "No tenant context" });

  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    // Use set_config — SET LOCAL does not accept bind placeholders ($1)
    await client.query("SELECT set_config('app.current_tenant_id', $1, true)", [tenantId]);
    req.db = client;
    req.tenantId = tenantId;

    // Cleanup on response finish — guarantees release even if handler skips next()
    res.on("finish", async () => {
      try { await client.query("COMMIT"); } catch { await client.query("ROLLBACK"); }
      client.release();
    });

    next();
  } catch (err) {
    await client.query("ROLLBACK").catch(() => {});
    client.release();
    next(err);
  }
}
```

### 示例 3：自动租户作用域的 Prisma 中间件

```typescript
import { PrismaClient } from "@prisma/client";

// Tables that do NOT have tenant_id (global tables)
const GLOBAL_TABLES = new Set(["Plan", "FeatureFlag", "SystemConfig"]);

function createTenantPrisma(tenantId: string): PrismaClient {
  const prisma = new PrismaClient();

  prisma.$use(async (params, next) => {
    if (GLOBAL_TABLES.has(params.model ?? "")) return next(params);

    // Initialize args.where — Prisma passes undefined args for calls like findMany()
    params.args = params.args ?? {};
    params.args.where = params.args.where ?? {};

    // Inject tenant filter on reads (skip findUnique — it only accepts unique-field selectors)
    if (["findMany", "findFirst", "count", "aggregate"].includes(params.action)) {
      params.args.where = { ...params.args.where, tenantId };
    }

    // Inject tenant_id on creates
    if (["create", "createMany"].includes(params.action)) {
      params.args.data = params.args.data ?? {};
      if (params.action === "createMany") {
        params.args.data = params.args.data.map((d: any) => ({ ...d, tenantId }));
      } else {
        params.args.data = { ...params.args.data, tenantId };
      }
    }

    // Scope updates and deletes
    if (["update", "updateMany", "delete", "deleteMany"].includes(params.action)) {
      params.args.where = { ...params.args.where, tenantId };
    }

    return next(params);
  });

  return prisma;
}
```

## 绝对禁止

1. **查询租户作用域表时绝不能缺少 `tenant_id` 过滤器。** 即使 ORM 中间件会处理，原生 SQL 查询会完全绕过中间件。每条原生查询都必须包含 `WHERE tenant_id = $1` 或依赖 RLS。一条不带作用域的 `SELECT * FROM invoices` 就会泄露所有客户的账单数据。

2. **绝不能仅在应用会话中存储 `tenant_id` 而不在数据库层强制执行。** 应用层过滤只是建议，RLS 才是强制执行。如果中间件中的 bug 跳过了租户过滤器，只有 RLS 能阻止数据泄露。两层都要启用。

3. **绝不能对租户作用域资源使用自增整数 ID。** 顺序 ID（如 `invoice #1042`）允许攻击者通过递增 ID 枚举其他租户的资源。所有租户作用域主键使用 UUID。整数 ID 仅保留给内部表。

4. **绝不能让租户用户访问管理聚合端点。** 像 `GET /admin/metrics` 这样跨所有租户查询的路由，绝不能用普通租户 JWT 访问。跨租户路由使用独立的认证机制（API key、不同签发者的管理员角色声明）。

5. **绝不能在迁移连接上启用 RLS 运行迁移。** 迁移用户需要创建表、添加列和修改策略。如果迁移连接上 RLS 处于激活状态，`ALTER TABLE` 命令可能静默失败或仅影响"当前租户"的视图。迁移使用专用超级用户或 `bypassrls` 角色。

6. **使用 `SET LOCAL` 时绝不能跨租户共享连接池。** 在事务中使用 `SET LOCAL app.current_tenant_id` 时，该设置仅作用于事务范围。但如果前一个请求的事务未正确提交或回滚，连接会带着过期的租户上下文返回连接池。清理路径中务必执行 `RESET app.current_tenant_id`。

## 边界情况

1. **租户删除与数据保留。** 租户取消订阅时，不能简单执行 `DELETE FROM tenants WHERE id = $1`。外键级联在大数据集上可能超时。应软删除租户（设置 `deleted_at`）、撤销所有用户会话，然后运行后台任务在数小时或数天内批量删除租户数据。

2. **GDPR/合规的租户数据导出。** 租户请求完整数据导出时，需要查询每张租户作用域表中该 `tenant_id` 的数据并打包。构建所有租户作用域表的注册表（解析迁移文件或维护清单），确保导出任务不会遗漏在导出功能构建后新增的表。

3. **租户间共享资源。** 部分功能需要共享状态——例如市场场景中租户 A 的产品对租户 B 的用户可见。这些表需要不同的 RLS 策略：读取访问公开（无租户过滤器），但写入访问仍限定到所属租户。将这些建模为 `owner_tenant_id` 而非 `tenant_id`。

4. **租户感知后台任务。** cron 任务或队列 worker 处理任务时，没有 HTTP 请求可供提取 `tenant_id`。任务载荷必须包含 `tenant_id`，worker 在处理前必须设置数据库会话变量。绝不要在没有租户上下文的情况下运行后台任务——它们要么因 RLS 失败，要么完全绕过 RLS。

5. **每租户 schema 的连接池耗尽。** 如果每个租户使用独立的 PostgreSQL schema，且每个 schema 需要独立的连接池，500 个租户意味着 500 个连接池。这会快速耗尽 `max_connections`。使用 PgBouncer 等连接池器的事务模式，或在触及此瓶颈前切换到共享 schema。

## 最佳实践

1. **创建 `tenants` 表作为唯一数据源。** 每张表中的 `tenant_id` 外键都指向 `tenants.id`。包含 `name`、`slug`（用于子域路由）、`plan_id`、`created_at` 和 `deleted_at` 列。这张表是整个数据模型的根。

2. **将 `tenant_id` 作为每个复合索引的第一列。** PostgreSQL 使用复合索引的最左前缀匹配。`(tenant_id, created_at)` 索引同时服务于"租户 X 的所有条目"和"租户 X 按日期排序的条目"。`(created_at, tenant_id)` 索引仅帮助跨所有租户的日期范围查询。

3. **使用子域名或路径前缀进行租户路由。** `acme.yourapp.com` 或 `yourapp.com/org/acme` 都可以。在边缘层（中间件或反向代理）将子域名或路径映射到 `tenant_id` 查询。此查询应被缓存（Redis 或带 60 秒 TTL 的内存缓存），因为每个请求都会执行。

4. **显式区分租户作用域表和全局表。** 维护一个列表（代码常量或数据库表），标明哪些表是全局表（无 `tenant_id`）、哪些是租户作用域表。在 ORM 中间件、迁移 linter 和数据导出任务中使用此列表。如果某张表不在任何一个列表中，CI 检查应该失败。

5. **种子数据中至少用 3 个租户测试。** 开发中单个租户会隐藏所有多租户 bug。两个租户会隐藏第一个租户数据泄露到第二个但反向不会的 bug。三个租户才能捕获只在多个对等体之间出现的排序和过滤 bug。

6. **按租户限流和配额，而非全局。** 全局限流 1000 请求/分钟意味着一个活跃租户可以耗尽所有人的配额。使用 Redis 键模式 `ratelimit:{tenant_id}:{endpoint}` 配合滑动窗口计数器实现每租户限流。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
