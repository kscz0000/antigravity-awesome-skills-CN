---
title: 列出和检查工作流
impact: CRITICAL
impactDescription: 支持工作流执行的监控和调试
tags: workflow, list, inspect, status, monitoring
---

## 列出和检查工作流

使用 `DBOS.listWorkflows` 按状态、名称、时间范围等条件查询工作流执行。

**错误（无工作流状态监控）：**

```typescript
// 启动工作流后无法再检查它
await DBOS.startWorkflow(processTask)("data");
// 如果出现问题，无法查找或调试
```

**正确（列出和检查工作流）：**

```typescript
// 按状态列出工作流
const erroredWorkflows = await DBOS.listWorkflows({
  status: "ERROR",
});

for (const wf of erroredWorkflows) {
  console.log(`Workflow ${wf.workflowID}: ${wf.workflowName} - ${wf.error}`);
}
```

使用多个过滤器列出工作流：

```typescript
const workflows = await DBOS.listWorkflows({
  workflowName: "processOrder",
  status: "SUCCESS",
  limit: 100,
  sortDesc: true,
  loadOutput: true,
});
```

列出已入队工作流：

```typescript
const queued = await DBOS.listQueuedWorkflows({
  queueName: "task_queue",
});
```

列出工作流步骤：

```typescript
const steps = await DBOS.listWorkflowSteps(workflowID);
if (steps) {
  for (const step of steps) {
    console.log(`Step ${step.functionID}: ${step.name}`);
    if (step.error) console.log(`  Error: ${step.error}`);
    if (step.childWorkflowID) console.log(`  Child: ${step.childWorkflowID}`);
  }
}
```

工作流状态值：`ENQUEUED`、`PENDING`、`SUCCESS`、`ERROR`、`CANCELLED`、`RETRIES_EXCEEDED`

为优化性能，在不需要工作流输入或输出时设置 `loadInput: false` 和 `loadOutput: false`。

参考：[Workflow Management](https://docs.dbos.dev/typescript/tutorials/workflow-management)
