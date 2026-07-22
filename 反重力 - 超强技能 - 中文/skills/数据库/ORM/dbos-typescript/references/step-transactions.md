---
title: 对数据库操作使用事务
impact: HIGH
impactDescription: 事务在工作流中提供精确一次的数据库执行
tags: step, transaction, database, datasource
---

## 对数据库操作使用事务

在工作流内部使用数据源事务进行数据库操作。事务精确一次提交并被检查点化以支持恢复。

**错误（工作流中直接进行数据库查询）：**

```typescript
import { Pool } from "pg";
const pool = new Pool();

async function myWorkflowFn() {
  // 工作流中直接访问数据库 - 未被检查点化！
  const result = await pool.query("INSERT INTO orders ...");
}
```

**正确（使用数据源事务）：**

安装数据源包（例如 Knex）：
```
npm i @dbos-inc/knex-datasource
```

配置数据源：
```typescript
import { KnexDataSource } from "@dbos-inc/knex-datasource";

const config = { client: "pg", connection: process.env.DBOS_DATABASE_URL };
const dataSource = new KnexDataSource("app-db", config);
```

使用 `runTransaction` 内联运行事务：
```typescript
async function insertOrderFn(userId: string, amount: number) {
  const rows = await dataSource
    .client("orders")
    .insert({ user_id: userId, amount })
    .returning("id");
  return rows[0].id;
}

async function myWorkflowFn(userId: string, amount: number) {
  const orderId = await dataSource.runTransaction(
    () => insertOrderFn(userId, amount),
    { name: "insertOrder" }
  );
  return orderId;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

也可以使用 `dataSource.registerTransaction` 预注册事务函数：
```typescript
const insertOrder = dataSource.registerTransaction(insertOrderFn);
```

可用的数据源包：`@dbos-inc/knex-datasource`、`@dbos-inc/kysely-datasource`、`@dbos-inc/drizzle-datasource`、`@dbos-inc/typeorm-datasource`、`@dbos-inc/prisma-datasource`、`@dbos-inc/nodepg-datasource`、`@dbos-inc/postgres-datasource`。

数据源需要通过 `initializeDBOSSchema` 安装 DBOS schema（`transaction_completion` 表）。

参考：[Transactions & Datasources](https://docs.dbos.dev/typescript/tutorials/transaction-tutorial)
