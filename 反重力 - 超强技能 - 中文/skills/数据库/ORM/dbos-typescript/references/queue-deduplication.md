---
title: 队列工作流去重
impact: HIGH
impactDescription: 防止工作流重复执行
tags: queue, deduplication, idempotent, duplicate
---

## 队列工作流去重

入队时设置去重 ID 以防止工作流重复执行。如果已存在具有相同去重 ID 的已入队或执行中的工作流，会抛出 `DBOSQueueDuplicatedError`。

**错误（不去重）：**

```typescript
// 多次点击可能入队重复项
async function handleClick(userId: string) {
  await DBOS.startWorkflow(processTask, { queueName: queue.name })("task");
}
```

**正确（带去重）：**

```typescript
const queue = new WorkflowQueue("task_queue");

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

async function handleClick(userId: string) {
  try {
    await DBOS.startWorkflow(processTask, {
      queueName: queue.name,
      enqueueOptions: { deduplicationID: userId },
    })("task");
  } catch (e) {
    // DBOSQueueDuplicatedError - 该用户的工作流已激活
    console.log("Task already in progress for user:", userId);
  }
}
```

去重是按队列的。当工作流状态为 `ENQUEUED` 或 `PENDING` 时去重 ID 处于激活状态。一旦工作流完成，可以使用相同的去重 ID 入队新工作流。

适用场景：
- 确保每个用户只有一个活动任务
- 防止表单重复提交
- 幂等的事件处理

参考：[Deduplication](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#deduplication)
