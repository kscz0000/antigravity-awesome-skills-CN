---
title: 控制队列并发
impact: HIGH
impactDescription: 通过并发限制防止资源耗尽
tags: queue, concurrency, workerConcurrency, limits
---

## 控制队列并发

队列支持 worker 级和全局并发限制，以防止资源耗尽。

**错误（无并发控制）：**

```typescript
const queue = new WorkflowQueue("heavy_tasks"); // 无限制 - 可能耗尽内存
```

**正确（worker 并发）：**

```typescript
// 每个进程最多从该队列运行 5 个任务
const queue = new WorkflowQueue("heavy_tasks", { workerConcurrency: 5 });
```

**正确（全局并发）：**

```typescript
// 跨所有进程最多运行 10 个任务
const queue = new WorkflowQueue("limited_tasks", { concurrency: 10 });
```

**按序处理（顺序执行）：**

```typescript
// 一次只处理一个任务 - 保证顺序
const serialQueue = new WorkflowQueue("sequential_queue", { concurrency: 1 });

async function processEventFn(event: string) {
  // ...
}
const processEvent = DBOS.registerWorkflow(processEventFn);

app.post("/events", async (req, res) => {
  await DBOS.startWorkflow(processEvent, { queueName: serialQueue.name })(req.body.event);
  res.send("Queued!");
});
```

大多数场景推荐使用 worker 并发。使用全局并发时需注意：队列上任何 `PENDING` 状态的工作流都计入限制，包括之前应用版本的工作流。

使用 worker 并发时，每个进程必须在配置中设置唯一的 `executorID`（使用 DBOS Conductor 或 Cloud 时自动设置）。

参考：[Managing Concurrency](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#managing-concurrency)
