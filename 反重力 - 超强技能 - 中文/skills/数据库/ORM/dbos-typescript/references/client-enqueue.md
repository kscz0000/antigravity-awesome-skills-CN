---
title: 从外部应用入队工作流
impact: MEDIUM
impactDescription: 支持外部服务向 DBOS 队列提交工作
tags: client, enqueue, external, queue
---

## 从外部应用入队工作流

使用 `client.enqueue()` 从 DBOS 应用外部提交工作流。由于 `DBOSClient` 在外部运行，工作流和队列元数据必须显式指定。

**错误（尝试在外部代码中使用 DBOS.startWorkflow）：**

```typescript
// DBOS.startWorkflow 需要完整的 DBOS 设置
await DBOS.startWorkflow(processTask, { queueName: "myQueue" })("data");
```

**正确（使用 DBOSClient.enqueue）：**

```typescript
import { DBOSClient } from "@dbos-inc/dbos-sdk";

const client = await DBOSClient.create({
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});

// 基础入队
const handle = await client.enqueue(
  {
    workflowName: "processTask",
    queueName: "task_queue",
  },
  "task-data"
);

// 等待结果
const result = await handle.getResult();
```

**类型安全的入队：**

```typescript
// 导入或声明工作流类型
declare class Tasks {
  static processTask(data: string): Promise<string>;
}

const handle = await client.enqueue<typeof Tasks.processTask>(
  {
    workflowName: "processTask",
    workflowClassName: "Tasks",
    queueName: "task_queue",
  },
  "task-data"
);

// TypeScript 自动推断结果类型
const result = await handle.getResult(); // 类型：string
```

**入队选项：**
- `workflowName`（必填）：工作流函数名称
- `queueName`（必填）：队列名称
- `workflowClassName`：若工作流是类方法则为类名
- `workflowConfigName`：若使用 `ConfiguredInstance` 则为实例名
- `workflowID`：自定义工作流 ID
- `workflowTimeoutMS`：超时时间（毫秒）
- `deduplicationID`：防止重复入队
- `priority`：队列优先级（数值越小优先级越高）
- `queuePartitionKey`：分区队列的分区键

使用完毕务必调用 `client.destroy()`。

参考：[DBOS Client Enqueue](https://docs.dbos.dev/typescript/reference/client#enqueue)
