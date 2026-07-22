---
title: 设置工作流超时
impact: CRITICAL
impactDescription: 防止工作流无限期运行
tags: workflow, timeout, cancellation, duration
---

## 设置工作流超时

通过向 `DBOS.startWorkflow` 传 `timeoutMS` 来为工作流设置超时。超时到期时，工作流及其所有子工作流都会被取消。

**错误（可能长时间运行的工作流无超时）：**

```typescript
// 无超时 - 可能无限期运行
const handle = await DBOS.startWorkflow(processTask)("data");
```

**正确（带超时）：**

```typescript
async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// 5 分钟后超时（毫秒）
const handle = await DBOS.startWorkflow(processTask, {
  timeoutMS: 5 * 60 * 1000,
})("data");
```

关键超时行为：
- 超时是**从开始到完成**：超时从工作流开始执行时算起，而不是入队时
- 超时是**持久化**的：它们跨重启持续存在，因此工作流可以拥有非常长的超时（小时、天、周）
- 取消发生在**下一步开始时** - 当前步骤先完成
- 取消工作流也会取消所有**子工作流**

参考：[Workflow Timeouts](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-timeouts)
