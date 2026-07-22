---
name: azure-postgres-ts
description: 使用 pg (node-postgres) 包从 Node.js/TypeScript 连接到 Azure Database for PostgreSQL Flexible Server。当用户要求'连接Azure PostgreSQL'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure PostgreSQL for TypeScript (node-postgres)

使用 `pg` (node-postgres) 包连接到 Azure Database for PostgreSQL Flexible Server，支持密码和 Microsoft Entra ID（无密码）认证。

## 安装

```bash
npm install pg @azure/identity
npm install -D @types/pg
```

## 环境变量

```bash
# Required
AZURE_POSTGRESQL_HOST=<server>.postgres.database.azure.com
AZURE_POSTGRESQL_DATABASE=<database>
AZURE_POSTGRESQL_PORT=5432

# For password authentication
AZURE_POSTGRESQL_USER=<username>
AZURE_POSTGRESQL_PASSWORD=<password>

# For Entra ID authentication
AZURE_POSTGRESQL_USER=<entra-user>@<server>   # e.g., user@contoso.com
AZURE_POSTGRESQL_CLIENTID=<managed-identity-client-id>  # For user-assigned identity
```

## 认证

### 方式一：密码认证

```typescript
import { Client, Pool } from "pg";

const client = new Client({
  host: process.env.AZURE_POSTGRESQL_HOST,
  database: process.env.AZURE_POSTGRESQL_DATABASE,
  user: process.env.AZURE_POSTGRESQL_USER,
  password: process.env.AZURE_POSTGRESQL_PASSWORD,
  port: Number(process.env.AZURE_POSTGRESQL_PORT) || 5432,
  ssl: { rejectUnauthorized: true }  // Required for Azure
});

await client.connect();
```

### 方式二：Microsoft Entra ID（无密码）— 推荐

```typescript
import { Client, Pool } from "pg";
import { DefaultAzureCredential } from "@azure/identity";

// For system-assigned managed identity
const credential = new DefaultAzureCredential();

// For user-assigned managed identity
// const credential = new DefaultAzureCredential({
//   managedIdentityClientId: process.env.AZURE_POSTGRESQL_CLIENTID
// });

// Acquire access token for Azure PostgreSQL
const tokenResponse = await credential.getToken(
  "https://ossrdbms-aad.database.windows.net/.default"
);

const client = new Client({
  host: process.env.AZURE_POSTGRESQL_HOST,
  database: process.env.AZURE_POSTGRESQL_DATABASE,
  user: process.env.AZURE_POSTGRESQL_USER,  // Entra ID user
  password: tokenResponse.token,             // Token as password
  port: Number(process.env.AZURE_POSTGRESQL_PORT) || 5432,
  ssl: { rejectUnauthorized: true }
});

await client.connect();
```

## 核心工作流

### 1. 单客户端连接

```typescript
import { Client } from "pg";

const client = new Client({
  host: process.env.AZURE_POSTGRESQL_HOST,
  database: process.env.AZURE_POSTGRESQL_DATABASE,
  user: process.env.AZURE_POSTGRESQL_USER,
  password: process.env.AZURE_POSTGRESQL_PASSWORD,
  port: 5432,
  ssl: { rejectUnauthorized: true }
});

try {
  await client.connect();
  
  const result = await client.query("SELECT NOW() as current_time");
  console.log(result.rows[0].current_time);
} finally {
  await client.end();  // Always close connection
}
```

### 2. 连接池（生产环境推荐）

```typescript
import { Pool } from "pg";

const pool = new Pool({
  host: process.env.AZURE_POSTGRESQL_HOST,
  database: process.env.AZURE_POSTGRESQL_DATABASE,
  user: process.env.AZURE_POSTGRESQL_USER,
  password: process.env.AZURE_POSTGRESQL_PASSWORD,
  port: 5432,
  ssl: { rejectUnauthorized: true },
  
  // Pool configuration
  max: 20,                    // Maximum connections in pool
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 10000  // Timeout for new connections
});

// Query using pool (automatically acquires and releases connection)
const result = await pool.query("SELECT * FROM users WHERE id = $1", [userId]);

// Explicit checkout for multiple queries
const client = await pool.connect();
try {
  const res1 = await client.query("SELECT * FROM users");
  const res2 = await client.query("SELECT * FROM orders");
} finally {
  client.release();  // Return connection to pool
}

// Cleanup on shutdown
await pool.end();
```

### 3. 参数化查询（防止 SQL 注入）

```typescript
// ALWAYS use parameterized queries - never concatenate user input
const userId = 123;
const email = "user@example.com";

// Single parameter
const result = await pool.query(
  "SELECT * FROM users WHERE id = $1",
  [userId]
);

// Multiple parameters
const result = await pool.query(
  "INSERT INTO users (email, name, created_at) VALUES ($1, $2, NOW()) RETURNING *",
  [email, "John Doe"]
);

// Array parameter
const ids = [1, 2, 3, 4, 5];
const result = await pool.query(
  "SELECT * FROM users WHERE id = ANY($1::int[])",
  [ids]
);
```

### 4. 事务

```typescript
const client = await pool.connect();

try {
  await client.query("BEGIN");
  
  const userResult = await client.query(
    "INSERT INTO users (email) VALUES ($1) RETURNING id",
    ["user@example.com"]
  );
  const userId = userResult.rows[0].id;
  
  await client.query(
    "INSERT INTO orders (user_id, total) VALUES ($1, $2)",
    [userId, 99.99]
  );
  
  await client.query("COMMIT");
} catch (error) {
  await client.query("ROLLBACK");
  throw error;
} finally {
  client.release();
}
```

### 5. 事务辅助函数

```typescript
async function withTransaction<T>(
  pool: Pool,
  fn: (client: PoolClient) => Promise<T>
): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const result = await fn(client);
    await client.query("COMMIT");
    return result;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}

// Usage
const order = await withTransaction(pool, async (client) => {
  const user = await client.query(
    "INSERT INTO users (email) VALUES ($1) RETURNING *",
    ["user@example.com"]
  );
  const order = await client.query(
    "INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING *",
    [user.rows[0].id, 99.99]
  );
  return order.rows[0];
});
```

### 6. TypeScript 类型化查询

```typescript
import { Pool, QueryResult } from "pg";

interface User {
  id: number;
  email: string;
  name: string;
  created_at: Date;
}

// Type the query result
const result: QueryResult<User> = await pool.query<User>(
  "SELECT * FROM users WHERE id = $1",
  [userId]
);

const user: User | undefined = result.rows[0];

// Type-safe insert
async function createUser(
  pool: Pool,
  email: string,
  name: string
): Promise<User> {
  const result = await pool.query<User>(
    "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
    [email, name]
  );
  return result.rows[0];
}
```

## 带 Entra ID 令牌刷新的连接池

对于长时间运行的应用，令牌会过期，需要刷新：

```typescript
import { Pool, PoolConfig } from "pg";
import { DefaultAzureCredential, AccessToken } from "@azure/identity";

class AzurePostgresPool {
  private pool: Pool | null = null;
  private credential: DefaultAzureCredential;
  private tokenExpiry: Date | null = null;
  private config: Omit<PoolConfig, "password">;

  constructor(config: Omit<PoolConfig, "password">) {
    this.credential = new DefaultAzureCredential();
    this.config = config;
  }

  private async getToken(): Promise<string> {
    const tokenResponse = await this.credential.getToken(
      "https://ossrdbms-aad.database.windows.net/.default"
    );
    this.tokenExpiry = new Date(tokenResponse.expiresOnTimestamp);
    return tokenResponse.token;
  }

  private isTokenExpired(): boolean {
    if (!this.tokenExpiry) return true;
    // Refresh 5 minutes before expiry
    return new Date() >= new Date(this.tokenExpiry.getTime() - 5 * 60 * 1000);
  }

  async getPool(): Promise<Pool> {
    if (this.pool && !this.isTokenExpired()) {
      return this.pool;
    }

    // Close existing pool if token expired
    if (this.pool) {
      await this.pool.end();
    }

    const token = await this.getToken();
    this.pool = new Pool({
      ...this.config,
      password: token
    });

    return this.pool;
  }

  async query<T>(text: string, params?: any[]): Promise<QueryResult<T>> {
    const pool = await this.getPool();
    return pool.query<T>(text, params);
  }

  async end(): Promise<void> {
    if (this.pool) {
      await this.pool.end();
      this.pool = null;
    }
  }
}

// Usage
const azurePool = new AzurePostgresPool({
  host: process.env.AZURE_POSTGRESQL_HOST!,
  database: process.env.AZURE_POSTGRESQL_DATABASE!,
  user: process.env.AZURE_POSTGRESQL_USER!,
  port: 5432,
  ssl: { rejectUnauthorized: true },
  max: 20
});

const result = await azurePool.query("SELECT NOW()");
```

## 错误处理

```typescript
import { DatabaseError } from "pg";

try {
  await pool.query("INSERT INTO users (email) VALUES ($1)", [email]);
} catch (error) {
  if (error instanceof DatabaseError) {
    switch (error.code) {
      case "23505":  // unique_violation
        console.error("Duplicate entry:", error.detail);
        break;
      case "23503":  // foreign_key_violation
        console.error("Foreign key constraint failed:", error.detail);
        break;
      case "42P01":  // undefined_table
        console.error("Table does not exist:", error.message);
        break;
      case "28P01":  // invalid_password
        console.error("Authentication failed");
        break;
      case "57P03":  // cannot_connect_now (server starting)
        console.error("Server unavailable, retry later");
        break;
      default:
        console.error(`PostgreSQL error ${error.code}: ${error.message}`);
    }
  }
  throw error;
}
```

## 连接字符串格式

```typescript
// Alternative: Use connection string
const pool = new Pool({
  connectionString: `postgres://${user}:${password}@${host}:${port}/${database}?sslmode=require`
});

// With SSL required (Azure)
const connectionString = 
  `postgres://user:password@server.postgres.database.azure.com:5432/mydb?sslmode=require`;
```

## 连接池事件

```typescript
const pool = new Pool({ /* config */ });

pool.on("connect", (client) => {
  console.log("New client connected to pool");
});

pool.on("acquire", (client) => {
  console.log("Client checked out from pool");
});

pool.on("release", (err, client) => {
  console.log("Client returned to pool");
});

pool.on("remove", (client) => {
  console.log("Client removed from pool");
});

pool.on("error", (err, client) => {
  console.error("Unexpected pool error:", err);
});
```

## Azure 特定配置

| 设置 | 值 | 说明 |
|------|-----|------|
| `ssl.rejectUnauthorized` | `true` | Azure 始终使用 SSL |
| 默认端口 | `5432` | 标准 PostgreSQL 端口 |
| PgBouncer 端口 | `6432` | 启用 PgBouncer 时使用 |
| 令牌范围 | `https://ossrdbms-aad.database.windows.net/.default` | Entra ID 令牌范围 |
| 令牌有效期 | 约 1 小时 | 过期前刷新 |

## 连接池大小指南

| 负载 | `max` | `idleTimeoutMillis` |
|------|-------|---------------------|
| 轻量（开发/测试） | 5-10 | 30000 |
| 中等（生产） | 20-30 | 30000 |
| 重度（高并发） | 50-100 | 10000 |

> **注意**：Azure PostgreSQL 的连接数限制取决于 SKU。请查看你所在层级的最大连接数。

## 最佳实践

1. **生产环境始终使用连接池**
2. **使用参数化查询** — 永远不要拼接用户输入
3. **始终关闭连接** — 使用 `try/finally` 或连接池
4. **启用 SSL** — Azure 必须启用（`ssl: { rejectUnauthorized: true }`）
5. **处理令牌刷新** — Entra ID 令牌约 1 小时后过期
6. **设置连接超时** — 避免网络问题导致挂起
7. **使用事务** — 用于多语句操作
8. **监控连接池指标** — 追踪 `pool.totalCount`、`pool.idleCount`、`pool.waitingCount`
9. **优雅关闭** — 应用终止时调用 `pool.end()`
10. **使用 TypeScript 泛型** — 为查询结果添加类型以保证安全

## 关键类型

```typescript
import {
  Client,
  Pool,
  PoolClient,
  PoolConfig,
  QueryResult,
  QueryResultRow,
  DatabaseError,
  QueryConfig
} from "pg";
```

## 参考链接

| 资源 | URL |
|------|-----|
| node-postgres 文档 | https://node-postgres.com |
| npm 包 | https://www.npmjs.com/package/pg |
| GitHub 仓库 | https://github.com/brianc/node-postgres |
| Azure PostgreSQL 文档 | https://learn.microsoft.com/azure/postgresql/flexible-server/ |
| 无密码连接 | https://learn.microsoft.com/azure/postgresql/flexible-server/how-to-connect-with-managed-identity |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
