---
title: 控制 Worker 监听的队列
impact: HIGH
impactDescription: 支持异构 worker 池
tags: queue, listen, worker, process, configuration
---

## 控制 Worker 监听的队列

在 DBOS 配置中配置 `listenQueues`，使进程仅从指定队列出队。这支持异构 worker 池。

**错误（所有 worker 处理所有队列）：**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

// 每个 worker 同时处理 CPU 和 GPU 任务
// CPU worker 上的 GPU 任务会失败或变慢！
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});
await DBOS.launch();
```

**正确（选择性监听队列）：**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

async function main() {
  const workerType = process.env.WORKER_TYPE; // "cpu" 或 "gpu"

  const config: any = {
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  };

  if (workerType === "gpu") {
    config.listenQueues = [gpuQueue];
  } else if (workerType === "cpu") {
    config.listenQueues = [cpuQueue];
  }

  DBOS.setConfig(config);
  await DBOS.launch();
}
```

`listenQueues` 仅控制出队。CPU worker 仍可将任务入队到 GPU 队列：

```typescript
// 从 CPU worker 入队到 GPU 队列
await DBOS.startWorkflow(gpuTask, { queueName: gpuQueue.name })("data");
```

参考：[Explicit Queue Listening](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#explicit-queue-listening)
