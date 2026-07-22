---
name: drizzle-orm-expert
description: "Drizzle ORM TypeScript 专家 — 模式设计、关系查询、迁移和无服务器数据库集成。使用 Drizzle 构建类型安全的数据库层时使用。"
risk: safe
source: community
date_added: "2026-03-04"
---

# Drizzle ORM 专家

你是生产级 Drizzle ORM 专家。帮助开发者使用 Drizzle ORM 和 TypeScript 构建类型安全、高性能的数据库层。你精通模式设计、关系查询 API、Drizzle Kit 迁移，以及与 Next.js、tRPC 和无服务器数据库（Neon、PlanetScale、Turso、Supabase）的集成。

## 何时使用此技能

- 当用户要求在新项目或现有项目中设置 Drizzle ORM 时使用
- 当使用 Drizzle 的 TypeScript 优先方法设计数据库模式时使用
- 当编写复杂的关系查询（连接、子查询、聚合）时使用
- 当设置或排查 Drizzle Kit 迁移问题时使用
- 当将 Drizzle 与 Next.js App Router、tRPC 或 Hono 集成时使用
- 当优化数据库性能（预处理语句、批处理、连接池）时使用
- 当从 Prisma、TypeORM 或 Knex 迁移到 Drizzle 时使用

## 核心概念

### 为什么选择 Drizzle

Drizzle ORM 是一个 TypeScript 优先的 ORM，生成零运行时开销。与 Prisma（使用查询引擎二进制文件）不同，Drizzle 编译为原生 SQL — 这使其成为边缘运行时和无服务器环境的理想选择。主要优势：

- **类 SQL API**：如果你懂 SQL，你就懂 Drizzle
- **零依赖**：极小的包体积，可在 Cloudflare Workers、Vercel Edge、Deno 中运行
- **完整类型推断**：模式 → 类型 → 查询在编译时全部关联
- **关系查询 API**：类似 Prisma 的嵌套 includes，无 N+1 问题

## 模式设计模式

### 表定义

```typescript
// db/schema.ts
import { pgTable, text, integer, timestamp, boolean, uuid, pgEnum } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// 枚举
export const roleEnum = pgEnum("role", ["admin", "user", "moderator"]);

// 用户表
export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
  role: roleEnum("role").default("user").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// 带外键的文章表
export const posts = pgTable("posts", {
  id: uuid("id").defaultRandom().primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  published: boolean("published").default(false).notNull(),
  authorId: uuid("author_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

### 关系定义

```typescript
// db/relations.ts
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### 类型推断

```typescript
// 直接从模式推断类型 — 无需单独的类型文件
import type { InferSelectModel, InferInsertModel } from "drizzle-orm";

export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;
export type Post = InferSelectModel<typeof posts>;
export type NewPost = InferInsertModel<typeof posts>;
```

## 查询模式

### Select 查询（类 SQL API）

```typescript
import { eq, and, like, desc, count, sql } from "drizzle-orm";

// 基础查询
const allUsers = await db.select().from(users);

// 带条件过滤
const admins = await db.select().from(users).where(eq(users.role, "admin"));

// 部分查询（仅特定列）
const emails = await db.select({ email: users.email }).from(users);

// 连接查询
const postsWithAuthors = await db
  .select({
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.published, true))
  .orderBy(desc(posts.createdAt))
  .limit(10);

// 聚合查询
const postCounts = await db
  .select({
    authorId: posts.authorId,
    postCount: count(posts.id),
  })
  .from(posts)
  .groupBy(posts.authorId);
```

### 关系查询（类 Prisma API）

```typescript
// 嵌套 includes — Drizzle 在单次查询中解析
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: eq(posts.published, true),
      orderBy: [desc(posts.createdAt)],
      limit: 5,
    },
  },
});

// 查询单个并带嵌套数据
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { posts: true },
});
```

### Insert、Update、Delete

```typescript
// 插入并返回
const [newUser] = await db
  .insert(users)
  .values({ email: "dev@example.com", name: "Dev" })
  .returning();

// 批量插入
await db.insert(posts).values([
  { title: "Post 1", authorId: newUser.id },
  { title: "Post 2", authorId: newUser.id },
]);

// 更新
await db.update(users).set({ name: "Updated" }).where(eq(users.id, userId));

// 删除
await db.delete(posts).where(eq(posts.authorId, userId));
```

### 事务

```typescript
const result = await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ email, name }).returning();
  await tx.insert(posts).values({ title: "Welcome Post", authorId: user.id });
  return user;
});
```

## 迁移工作流（Drizzle Kit）

### 配置

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### 命令

```bash
# 从模式变更生成迁移 SQL
npx drizzle-kit generate

# 直接将模式推送到数据库（仅开发环境 — 跳过迁移文件）
npx drizzle-kit push

# 运行待处理的迁移（生产环境）
npx drizzle-kit migrate

# 打开 Drizzle Studio（GUI 数据库浏览器）
npx drizzle-kit studio
```

## 数据库客户端设置

### PostgreSQL（Neon Serverless）

```typescript
// db/index.ts
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### SQLite（Turso/LibSQL）

```typescript
import { drizzle } from "drizzle-orm/libsql";
import { createClient } from "@libsql/client";
import * as schema from "./schema";

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN,
});
export const db = drizzle(client, { schema });
```

### MySQL（PlanetScale）

```typescript
import { drizzle } from "drizzle-orm/planetscale-serverless";
import { Client } from "@planetscale/database";
import * as schema from "./schema";

const client = new Client({ url: process.env.DATABASE_URL! });
export const db = drizzle(client, { schema });
```

## 性能优化

### 预处理语句

```typescript
// 准备一次，多次执行
const getUserById = db.query.users
  .findFirst({
    where: eq(users.id, sql.placeholder("id")),
  })
  .prepare("get_user_by_id");

// 带参数执行
const user = await getUserById.execute({ id: "abc-123" });
```

### 批量操作

```typescript
// 使用 db.batch() 在一次往返中执行多个独立查询
const [allUsers, recentPosts] = await db.batch([
  db.select().from(users),
  db.select().from(posts).orderBy(desc(posts.createdAt)).limit(10),
]);
```

### 模式中的索引

```typescript
import { index, uniqueIndex } from "drizzle-orm/pg-core";

export const posts = pgTable(
  "posts",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    title: text("title").notNull(),
    authorId: uuid("author_id").references(() => users.id).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => [
    index("posts_author_idx").on(table.authorId),
    index("posts_created_idx").on(table.createdAt),
  ]
);
```

## Next.js 集成

### Server Component 使用

```typescript
// app/users/page.tsx（React Server Component）
import { db } from "@/db";
import { users } from "@/db/schema";

export default async function UsersPage() {
  const allUsers = await db.select().from(users);
  return (
    <ul>
      {allUsers.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  );
}
```

### Server Action

```typescript
// app/actions.ts
"use server";
import { db } from "@/db";
import { users } from "@/db/schema";

export async function createUser(formData: FormData) {
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;
  await db.insert(users).values({ name, email });
}
```

## 最佳实践

- ✅ **推荐：** 将所有模式定义放在单个 `db/schema.ts` 中，或按领域拆分（`db/schema/users.ts`、`db/schema/posts.ts`）
- ✅ **推荐：** 使用 `InferSelectModel` 和 `InferInsertModel` 实现类型安全，而非手动定义接口
- ✅ **推荐：** 使用关系查询 API（`db.query.*`）获取嵌套数据以避免 N+1 问题
- ✅ **推荐：** 在生产环境中对频繁执行的查询使用预处理语句
- ✅ **推荐：** 在生产环境中使用 `drizzle-kit generate` + `migrate`（绝不使用 `push`）
- ✅ **推荐：** 向 `drizzle()` 传递 `{ schema }` 以启用关系查询 API
- ❌ **禁止：** 在生产环境中使用 `drizzle-kit push` — 可能导致数据丢失
- ❌ **禁止：** 当 Drizzle 查询构建器支持该操作时编写原生 SQL
- ❌ **禁止：** 如果要使用带 `with` 的 `db.query.*`，却忘记定义 `relations()`
- ❌ **禁止：** 在无服务器环境中为每个请求创建新的数据库连接 — 使用连接池

## 故障排查

**问题：** `db.query.tableName` 未定义
**解决方案：** 将所有模式对象（包括关系）传递给 `drizzle()`：`drizzle(client, { schema })`

**问题：** 模式变更后迁移冲突
**解决方案：** 运行 `npx drizzle-kit generate` 创建新迁移，然后运行 `npx drizzle-kit migrate`

**问题：** MySQL 上 `.returning()` 类型错误
**解决方案：** MySQL 不支持 `RETURNING`。使用 `.execute()` 并从结果中读取 `insertId`。

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
