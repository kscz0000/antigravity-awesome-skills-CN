---
name: neon-postgres
description: Neon serverless Postgres 的专家模式，涵盖分支管理、连接池以及
  Prisma/Drizzle 集成。当用户要求"neon database"、"serverless postgres"、"database branching"、"connection pooling"或"preview environments"时使用。
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Neon Postgres

Neon serverless Postgres 的专家模式，涵盖分支管理、连接池以及 Prisma/Drizzle 集成

## 模式

### Prisma 连接 Neon

为 Neon 配置 Prisma 并启用连接池。

使用两个连接字符串：
- DATABASE_URL：用于 Prisma Client 的池化连接
- DIRECT_URL：用于 Prisma Migrate 的直连

池化连接通过 PgBouncer 支持最多 10K 个连接。
迁移操作（DDL 操作）需要使用直连。

### Code_example

# .env
# Pooled connection for application queries
DATABASE_URL="postgres://user:password@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
# Direct connection for migrations
DIRECT_URL="postgres://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

// Run migrations
// Uses DIRECT_URL automatically
npx prisma migrate dev
npx prisma migrate deploy

### Anti_patterns

- 模式：迁移时使用池化连接 | 原因：DDL 操作通过 PgBouncer 会失败 | 修复：在 schema.prisma 中设置 directUrl
- 模式：未使用连接池 | 原因：Serverless 函数会耗尽连接限制 | 修复：在 DATABASE_URL 中使用 -pooler 端点

### References

- https://neon.com/docs/guides/prisma
- https://www.prisma.io/docs/orm/overview/databases/neon

### Drizzle 配合 Neon Serverless Driver

在 edge/serverless 环境中使用 Drizzle ORM 搭配 Neon 的 serverless HTTP driver。

两种驱动选项：
- neon-http：通过 HTTP 发送单次查询（一次性查询最快）
- neon-serverless：通过 WebSocket 处理事务和会话

### Code_example

# Install dependencies
npm install drizzle-orm @neondatabase/serverless
npm install -D drizzle-kit

// lib/db/schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// lib/db/index.ts (for serverless - HTTP driver)
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });

// Usage in API route
import { db } from '@/lib/db';
import { users } from '@/lib/db/schema';

export async function GET() {
  const allUsers = await db.select().from(users);
  return Response.json(allUsers);
}

// lib/db/index.ts (for WebSocket - transactions)
import { Pool } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-serverless';
import * as schema from './schema';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });

// With transactions
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'test@example.com' });
  await tx.update(users).set({ name: 'Updated' });
});

// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './lib/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});

// Run migrations
npx drizzle-kit generate
npx drizzle-kit migrate

### Anti_patterns

- 模式：在 serverless 中使用 pg driver | 原因：TCP 连接并非在所有 edge 环境中可用 | 修复：使用 @neondatabase/serverless driver
- 模式：使用 HTTP driver 处理事务 | 原因：HTTP driver 不支持事务 | 修复：使用 WebSocket driver（Pool）处理事务

### References

- https://neon.com/docs/guides/drizzle
- https://orm.drizzle.team/docs/connect-neon

### 使用 PgBouncer 进行连接池管理

Neon 通过 PgBouncer 提供内置连接池。

关键限制：
- 连接池最多支持 10,000 个并发连接
- 连接仍会消耗底层 Postgres 连接
- 7 个连接保留给 Neon 超级用户

应用使用池化端点，迁移使用直连。

### Code_example

# Connection string formats

# Pooled connection (for application)
# Note: -pooler in hostname
postgres://user:pass@ep-cool-name-pooler.us-east-2.aws.neon.tech/neondb

# Direct connection (for migrations)
# Note: No -pooler
postgres://user:pass@ep-cool-name.us-east-2.aws.neon.tech/neondb

// Prisma with pooling
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")      // Pooled
  directUrl = env("DIRECT_URL")        // Direct
}

// Connection pool settings for high-traffic
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  // Connection pool settings
  // Adjust based on compute size
});

// For Drizzle with connection pool
import { Pool } from '@neondatabase/serverless';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,  // Max connections in local pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
});

// Compute size connection limits
// 0.25 CU: 112 connections (105 available after reserved)
// 0.5 CU: 225 connections
// 1 CU: 450 connections
// 2 CU: 901 connections
// 4 CU: 1802 connections
// 8 CU: 3604 connections

### Anti_patterns

- 模式：每次请求都新建连接 | 原因：快速耗尽连接限制 | 修复：使用连接池，复用连接
- 模式：在 serverless 中设置过大的连接池 | 原因：多个函数实例 = 多个连接池 = 大量连接 | 修复：保持本地连接池较小（5-10），依赖 PgBouncer

### References

- https://neon.com/docs/connect/connection-pooling

### 数据库分支用于开发

为开发、测试和预览环境创建数据库的即时副本。

分支共享底层存储（copy-on-write），使其创建即时且经济高效。

### Code_example

# Create branch via Neon CLI
neon branches create --name feature/new-feature --parent main

# Create branch from specific point in time
neon branches create --name debug/yesterday \
  --parent main \
  --timestamp "2024-01-15T10:00:00Z"

# List branches
neon branches list

# Get connection string for branch
neon connection-string feature/new-feature

# Delete branch when done
neon branches delete feature/new-feature

// In CI/CD (GitHub Actions)
// .github/workflows/preview.yml
name: Preview Environment
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  create-branch:
    runs-on: ubuntu-latest
    steps:
      - uses: neondatabase/create-branch-action@v5
        id: create-branch
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          branch_name: preview/pr-${{ github.event.pull_request.number }}
          api_key: ${{ secrets.NEON_API_KEY }}
          username: ${{ secrets.NEON_ROLE_NAME }}

      - name: Run migrations
        env:
          DATABASE_URL: ${{ steps.create-branch.outputs.db_url_with_pooler }}
        run: npx prisma migrate deploy

      - name: Deploy to Vercel
        env:
          DATABASE_URL: ${{ steps.create-branch.outputs.db_url_with_pooler }}
        run: vercel deploy --prebuilt

// Cleanup on PR close
on:
  pull_request:
    types: [closed]

jobs:
  delete-branch:
    runs-on: ubuntu-latest
    steps:
      - uses: neondatabase/delete-branch-action@v3
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          branch: preview/pr-${{ github.event.pull_request.number }}
          api_key: ${{ secrets.NEON_API_KEY }}

### Anti_patterns

- 模式：开发环境共享生产数据库 | 原因：有数据损坏风险，无隔离 | 修复：从生产库创建开发分支
- 模式：未清理旧分支 | 原因：存储累积，环境混乱 | 修复：PR 关闭时自动删除分支

### References

- https://neon.com/blog/branching-with-preview-environments
- https://github.com/neondatabase/create-branch-action

### Vercel 预览环境集成

为 Vercel 预览部署自动创建数据库分支。每个 PR 拥有独立的隔离数据库。

两种集成选项：
- Vercel-Managed：在 Vercel 计费，自动设置
- Neon-Managed：在 Neon 计费，更多控制权

### Code_example

# Vercel-Managed Integration
# 1. Go to Vercel Dashboard > Storage > Create Database
# 2. Select Neon Postgres
# 3. Enable "Create a branch for each preview deployment"
# 4. Environment variables automatically injected

# Neon-Managed Integration
# 1. Install from Neon Dashboard > Integrations > Vercel
# 2. Select Vercel project to connect
# 3. Enable "Create a branch for each preview deployment"
# 4. Optionally enable auto-delete on branch delete

// vercel.json - Add migration to build
{
  "buildCommand": "prisma migrate deploy && next build",
  "framework": "nextjs"
}

// Or in package.json
{
  "scripts": {
    "vercel-build": "prisma generate && prisma migrate deploy && next build"
  }
}

// Environment variables injected by integration
// DATABASE_URL - Pooled connection for preview branch
// DATABASE_URL_UNPOOLED - Direct connection for migrations
// PGHOST, PGUSER, PGDATABASE, PGPASSWORD - Individual vars

// Prisma schema for Vercel integration
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DATABASE_URL_UNPOOLED")  // Vercel variable
}

// For Drizzle in Next.js on Vercel
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';

// Use pooled URL for queries
const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql);

### Anti_patterns

- 模式：所有预览环境使用同一个数据库 | 原因：预览环境互相干扰 | 修复：在集成中启用每个预览一个分支
- 模式：预览环境未运行迁移 | 原因：代码与数据库之间 schema 不匹配 | 修复：在构建步骤中添加 migrate 命令

### References

- https://neon.com/docs/guides/vercel-managed-integration
- https://neon.com/docs/guides/neon-managed-vercel-integration

### 自动扩缩与冷启动管理

Neon 自动扩缩计算资源并支持缩容至零。

冷启动延迟：从空闲状态唤醒时 500ms 至数秒。
生产建议：禁用 scale-to-zero，设置最低计算资源。

### Code_example

# Neon Console settings for production
# Project Settings > Compute > Default compute size
# - Set minimum to 0.5 CU or higher
# - Disable "Suspend compute after inactivity"

// Handle cold starts in application
// lib/db-with-retry.ts
import { prisma } from './prisma';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

export async function queryWithRetry<T>(
  query: () => Promise<T>
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      return await query();
    } catch (error) {
      lastError = error as Error;

      // Retry on connection errors (cold start)
      if (error.code === 'P1001' || error.code === 'P1002') {
        console.log(`Retry attempt ${attempt}/${MAX_RETRIES}`);
        await new Promise(r => setTimeout(r, RETRY_DELAY * attempt));
        continue;
      }

      throw error;
    }
  }

  throw lastError;
}

// Usage
const users = await queryWithRetry(() =>
  prisma.user.findMany()
);

// Reduce cold start latency with SSL direct negotiation
# PostgreSQL 17+ connection string
postgres://user:pass@ep-xxx-pooler.aws.neon.tech/db?sslmode=require&sslnegotiation=direct

// Keep-alive for long-running apps
// lib/db-keepalive.ts
import { prisma } from './prisma';

// Ping database every 4 minutes to prevent suspend
const KEEPALIVE_INTERVAL = 4 * 60 * 1000;

if (process.env.NEON_KEEPALIVE === 'true') {
  setInterval(async () => {
    try {
      await prisma.$queryRaw`SELECT 1`;
    } catch (error) {
      console.error('Keepalive failed:', error);
    }
  }, KEEPALIVE_INTERVAL);
}

// Compute sizing recommendations
// Development: 0.25 CU, scale-to-zero enabled
// Staging: 0.5 CU, scale-to-zero enabled
// Production: 1+ CU, scale-to-zero DISABLED
// High-traffic: 2-4 CU minimum, autoscaling enabled

### Anti_patterns

- 模式：生产环境启用 scale-to-zero | 原因：冷启动为首个请求增加 500ms+ 延迟 | 修复：为生产分支禁用 scale-to-zero
- 模式：冷启动无重试逻辑 | 原因：空闲后的首次连接可能超时 | 修复：添加指数退避重试

### References

- https://neon.com/blog/scaling-serverless-postgres
- https://neon.com/docs/connect/connection-latency

## Sharp Edges

### 缩容至零后的冷启动延迟

严重级别：HIGH

### 迁移时使用池化连接

严重级别：HIGH

### Serverless 中连接池耗尽

严重级别：HIGH

### PgBouncer 功能限制

严重级别：MEDIUM

### 分支存储累积

严重级别：MEDIUM

### 保留连接减少可用连接池

严重级别：LOW

### HTTP Driver 不支持事务

严重级别：MEDIUM

### 删除父分支影响子分支

严重级别：HIGH

### 分支间的 Schema 漂移

严重级别：MEDIUM

## Validation Checks

### 客户端代码中暴露直连数据库 URL

严重级别：ERROR

直连数据库 URL 不应暴露给客户端

Message: Direct URL exposed to client. Only pooled URLs for server-side use.

### 硬编码数据库连接字符串

严重级别：ERROR

连接字符串应使用环境变量

Message: Hardcoded connection string. Use environment variables.

### 连接字符串缺少 SSL Mode

严重级别：WARNING

Neon 要求 SSL 连接

Message: Missing sslmode=require. Add to connection string.

### Prisma 缺少迁移所需的 directUrl

严重级别：ERROR

Prisma 通过 PgBouncer 迁移时需要 directUrl

Message: Using pooled URL without directUrl. Migrations will fail.

### Prisma directUrl 指向池化端点

严重级别：ERROR

directUrl 应为非池化连接

Message: directUrl points to pooler. Use non-pooled endpoint for migrations.

### Serverless 函数中连接池过大

严重级别：WARNING

过大的连接池在大量函数实例时会耗尽连接

Message: Pool size too high for serverless. Use max: 5-10.

### 每次请求创建新客户端

严重级别：WARNING

每次请求创建新客户端会浪费连接

Message: Creating client per request. Use connection pool or neon() driver.

### 创建分支时缺少清理策略

严重级别：WARNING

分支应有自动化清理机制

Message: Creating branch without cleanup. Add delete-branch-action to PR close.

### 生产环境启用 Scale-to-Zero

严重级别：WARNING

Scale-to-zero 在生产环境中增加延迟

Message: Scale-to-zero on production. Disable for low-latency.

### 使用 HTTP Driver 处理事务

严重级别：ERROR

neon() HTTP driver 不支持事务

Message: HTTP driver with transaction. Use Pool from @neondatabase/serverless.

## 协作

### 委派触发条件

- 用户需要认证 -> clerk-auth（User 表包含 clerkId 列）
- 用户需要缓存 -> redis-specialist（查询缓存、会话存储）
- 用户需要搜索 -> algolia-search（超越 Postgres 能力的全文搜索）
- 用户需要分析 -> segment-cdp（追踪数据库事件、用户行为）
- 用户需要部署 -> vercel-deployment（环境变量、预览数据库）

## 适用场景
- 用户提及或暗示：neon database
- 用户提及或暗示：serverless postgres
- 用户提及或暗示：database branching
- 用户提及或暗示：neon postgres
- 用户提及或暗示：postgres serverless
- 用户提及或暗示：connection pooling
- 用户提及或暗示：preview environments
- 用户提及或暗示：database per preview

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。