---
title: 取消、恢复和分叉工作流
impact: CRITICAL
impactDescription: 支持对长时间运行工作流的运维控制
tags: workflow, cancel, resume, fork, management
---

## 取消、恢复和分叉工作流

DBOS 提供取消、恢复和分叉工作流的方法，以进行运维控制。

**错误（无法处理卡住或失败的工作流）：**

```typescript
// 工作流卡住或失败 - 无恢复机制
const handle = await DBOS.startWorkflow(processTask)("data");
// 如果工作流失败，无法重试或恢复
```

**正确（使用 cancel、resume 和 fork）：**

```typescript
// 取消工作流 - 在下一步停止
await DBOS.cancelWorkflow(workflowID);

// 从最后完成的步骤恢复
const handle = await DBOS.resumeWorkflow<string>(workflowID);
const result = await handle.getResult();
```

取消会将工作流状态设置为 `CANCELLED`，并在下一步开始时抢占执行。取消也会取消所有子工作流。

恢复从最后完成的步骤重启工作流。用于已取消或超过最大恢复尝试次数的工作流。也可以用来立即启动已入队的工作流，绕过其队列。

从特定步骤分叉工作流：

```typescript
// 列出步骤以找到正确的步骤 ID
const steps = await DBOS.listWorkflowSteps(workflowID);
// steps[i].functionID 是步骤的 ID

// 从特定步骤分叉
const forkHandle = await DBOS.forkWorkflow<string>(
  workflowID,
  startStep,
  {
    newWorkflowID: "new-wf-id",
    applicationVersion: "2.0.0",
    timeoutMS: 60000,
  }
);
const forkResult = await forkHandle.getResult();
```

分叉会创建一个具有新 ID 的新工作流，复制原工作流的输入和所选步骤之前的所有步骤输出。可用于从下游服务中断中恢复，或修补因 bug 而失败的工作流。

参考：[Workflow Management](https://docs.dbos.dev/typescript/tutorials/workflow-management)
