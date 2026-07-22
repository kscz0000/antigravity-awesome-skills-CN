---
title: 保持工作流确定性
impact: CRITICAL
impactDescription: 非确定性工作流无法正确恢复
tags: workflow, determinism, recovery, reliability
---

## 保持工作流确定性

工作流函数必须是确定性的：在相同输入和步骤返回值的情况下，必须以相同顺序调用相同步骤。非确定性操作必须移到步骤中。

**错误（非确定性工作流）：**

```typescript
async function exampleWorkflowFn() {
  // 工作流中的随机值会破坏恢复！
  // 重放时，Math.random() 返回不同的值，
  // 所以工作流可能走不同的分支。
  const choice = Math.random() > 0.5 ? 1 : 0;
  if (choice === 0) {
    await stepOne();
  } else {
    await stepTwo();
  }
}
const exampleWorkflow = DBOS.registerWorkflow(exampleWorkflowFn);
```

**正确（非确定性操作放在步骤中）：**

```typescript
async function exampleWorkflowFn() {
  // 步骤结果被检查点化 - 重放时使用保存的值
  const choice = await DBOS.runStep(
    () => Promise.resolve(Math.random() > 0.5 ? 1 : 0),
    { name: "generateChoice" }
  );
  if (choice === 0) {
    await stepOne();
  } else {
    await stepTwo();
  }
}
const exampleWorkflow = DBOS.registerWorkflow(exampleWorkflowFn);
```

必须放在步骤中的非确定性操作：
- 随机数生成（UUID 使用 `DBOS.randomUUID()`）
- 获取当前时间（时间戳使用 `DBOS.now()`）
- 访问外部 API
- 读取文件
- 数据库查询（使用事务或步骤）

参考：[Workflow Determinism](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#determinism)
