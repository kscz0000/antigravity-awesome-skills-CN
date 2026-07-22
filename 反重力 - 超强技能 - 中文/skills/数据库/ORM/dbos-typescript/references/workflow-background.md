---
title: 在后台启动工作流
impact: CRITICAL
impactDescription: 后台工作流支持可靠的异步处理
tags: workflow, background, handle, async
---

## 在后台启动工作流

使用 `DBOS.startWorkflow` 在后台启动工作流，并获取用于跟踪的句柄。即使应用被中断，工作流也保证运行至完成。

**错误（无法跟踪后台工作）：**

```typescript
async function processDataFn(data: string) {
  // ...
}
const processData = DBOS.registerWorkflow(processDataFn);

// 启动后不管 - 无法跟踪或获取结果
processData(data);
```

**正确（使用 startWorkflow）：**

```typescript
async function processDataFn(data: string) {
  return "processed: " + data;
}
const processData = DBOS.registerWorkflow(processDataFn);

async function main() {
  // 在后台启动工作流，获取句柄
  const handle = await DBOS.startWorkflow(processData)("input");

  // 获取工作流 ID
  console.log(handle.workflowID);

  // 等待结果
  const result = await handle.getResult();

  // 检查状态
  const status = await handle.getStatus();
}
```

稍后通过工作流 ID 检索句柄：

```typescript
const handle = DBOS.retrieveWorkflow<string>(workflowID);
const result = await handle.getResult();
```

参考：[Starting Workflows in Background](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#starting-workflows-in-the-background)
