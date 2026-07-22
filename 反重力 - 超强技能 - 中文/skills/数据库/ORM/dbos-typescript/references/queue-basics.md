---
title: 使用队列处理并发工作流
impact: HIGH
impactDescription: 队列提供托管的并发和流控能力
tags: queue, concurrency, enqueue, workflow
---

## 使用队列处理并发工作流

队列以托管的流控同时运行多个工作流。当需要控制同时运行多少个工作流时使用队列。

**错误（不受控的并发）：**

```typescript
async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// 不加控制地启动多个工作流 - 可能耗尽资源
for (const task of tasks) {
  await DBOS.startWorkflow(processTask)(task);
}
```

**正确（使用队列）：**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const queue = new WorkflowQueue("task_queue");

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

async function processAllTasksFn(tasks: string[]) {
  const handles = [];
  for (const task of tasks) {
    // 通过给 startWorkflow 传 queueName 来入队
    const handle = await DBOS.startWorkflow(processTask, {
      queueName: queue.name,
    })(task);
    handles.push(handle);
  }
  // 等待所有任务
  const results = [];
  for (const h of handles) {
    results.push(await h.getResult());
  }
  return results;
}
const processAllTasks = DBOS.registerWorkflow(processAllTasksFn);
```

队列以 FIFO 顺序处理工作流。所有队列应在 `DBOS.launch()` 之前创建。

参考：[DBOS Queues](https://docs.dbos.dev/typescript/tutorials/queue-tutorial)
