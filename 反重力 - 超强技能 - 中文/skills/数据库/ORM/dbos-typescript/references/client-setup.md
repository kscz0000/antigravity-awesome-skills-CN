---
title: 初始化 DBOSClient 以进行外部访问
impact: MEDIUM
impactDescription: 支持外部应用与 DBOS 工作流交互
tags: client, external, setup, initialization
---

## 初始化 DBOSClient 以进行外部访问

使用 `DBOSClient` 从外部应用（如 API 服务器、CLI 工具或独立服务）与 DBOS 交互。`DBOSClient` 直接连接 DBOS 系统数据库。

**错误（直接从外部应用使用 DBOS）：**

```typescript
// DBOS 需要完整的 setup 和 launch() - 对外部客户端来说过于重量级
DBOS.setConfig({ ... });
await DBOS.launch();
```

**正确（使用 DBOSClient）：**

```typescript
import { DBOSClient } from "@dbos-inc/dbos-sdk";

const client = await DBOSClient.create({
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});

// 向工作流发送消息
await client.send(workflowID, "notification", "topic");

// 从工作流获取事件
const event = await client.getEvent<string>(workflowID, "status");

// 读取工作流的流
for await (const value of client.readStream(workflowID, "results")) {
  console.log(value);
}

// 检索工作流句柄
const handle = client.retrieveWorkflow<string>(workflowID);
const result = await handle.getResult();

// 列出工作流
const workflows = await client.listWorkflows({ status: "ERROR" });

// 工作流管理
await client.cancelWorkflow(workflowID);
await client.resumeWorkflow(workflowID);

// 使用完毕务必销毁
await client.destroy();
```

构造函数选项：
- `systemDatabaseUrl`：Postgres 系统数据库的连接字符串（必填）
- `systemDatabasePool`：可选的自定义 `node-postgres` 连接池
- `serializer`：可选的自定义序列化器（必须与 DBOS 应用的序列化器一致）

参考：[DBOS Client](https://docs.dbos.dev/typescript/reference/client)
