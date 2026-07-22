---
title: 为工作流设置队列优先级
impact: HIGH
impactDescription: 优先处理重要工作流
tags: queue, priority, ordering, importance
---

## 为工作流设置队列优先级

在队列上启用优先级，以优先处理高优先级工作流。数值越小表示优先级越高。

**错误（无优先级 - 仅 FIFO）：**

```typescript
const queue = new WorkflowQueue("tasks");
// 所有任务按 FIFO 顺序处理，无论重要性
```

**正确（启用优先级的队列）：**

```typescript
const queue = new WorkflowQueue("tasks", { priorityEnabled: true });

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// 高优先级任务（数值越小 = 优先级越高）
await DBOS.startWorkflow(processTask, {
  queueName: queue.name,
  enqueueOptions: { priority: 1 },
})("urgent-task");

// 低优先级任务
await DBOS.startWorkflow(processTask, {
  queueName: queue.name,
  enqueueOptions: { priority: 100 },
})("background-task");
```

优先级规则：
- 范围：`1` 到 `2,147,483,647`
- 数值越小 = 优先级越高
- **未指定**优先级的工作流具有最高优先级（最先运行）
- 具有相同优先级的工作流按 FIFO 顺序出队

参考：[Priority](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#priority)
