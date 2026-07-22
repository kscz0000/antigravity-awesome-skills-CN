---
title: 队列分区实现按实体限制
impact: HIGH
impactDescription: 支持按实体粒度的并发控制
tags: queue, partition, per-user, dynamic
---

## 队列分区实现按实体限制

分区队列按分区键应用流控限制，而不是对整个队列应用。每个分区充当动态的"子队列"。

**错误（对按用户限制使用全局并发）：**

```typescript
// 全局 concurrency=1 阻塞所有用户，而非按用户
const queue = new WorkflowQueue("tasks", { concurrency: 1 });
```

**正确（分区队列）：**

```typescript
const queue = new WorkflowQueue("tasks", {
  partitionQueue: true,
  concurrency: 1,
});

async function onUserTask(userID: string, task: string) {
  // 每个用户拥有自己的分区 - 每个用户最多 1 个任务
  // 但不同用户的任务可并发运行
  await DBOS.startWorkflow(processTask, {
    queueName: queue.name,
    enqueueOptions: { queuePartitionKey: userID },
  })(task);
}
```

**两级队列（按用户 + 全局限制）：**

```typescript
const concurrencyQueue = new WorkflowQueue("concurrency-queue", { concurrency: 5 });
const partitionedQueue = new WorkflowQueue("partitioned-queue", {
  partitionQueue: true,
  concurrency: 1,
});

// 每个用户最多 1 个任务 且 全局最多 5 个任务
async function onUserTask(userID: string, task: string) {
  await DBOS.startWorkflow(concurrencyManager, {
    queueName: partitionedQueue.name,
    enqueueOptions: { queuePartitionKey: userID },
  })(task);
}

async function concurrencyManagerFn(task: string) {
  const handle = await DBOS.startWorkflow(processTask, {
    queueName: concurrencyQueue.name,
  })(task);
  return await handle.getResult();
}
const concurrencyManager = DBOS.registerWorkflow(concurrencyManagerFn);
```

参考：[Partitioning Queues](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#partitioning-queues)
