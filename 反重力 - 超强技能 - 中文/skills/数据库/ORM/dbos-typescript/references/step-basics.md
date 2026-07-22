---
title: 对外部操作使用步骤
impact: HIGH
impactDescription: 步骤通过检查点结果来支持恢复
tags: step, external, api, checkpoint
---

## 对外部操作使用步骤

任何执行复杂操作、访问外部 API 或具有副作用的函数都应该是步骤。步骤结果被检查点化，支持工作流恢复。

**错误（工作流中直接调用外部 API）：**

```typescript
async function myWorkflowFn() {
  // 工作流中直接调用外部 API - 未被检查点化！
  const response = await fetch("https://api.example.com/data");
  return await response.json();
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

**正确（使用 `DBOS.runStep` 在步骤中调用外部 API）：**

```typescript
async function fetchData() {
  return await fetch("https://api.example.com/data").then(r => r.json());
}

async function myWorkflowFn() {
  const data = await DBOS.runStep(fetchData, { name: "fetchData" });
  return data;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

`DBOS.runStep` 也接受内联箭头函数：

```typescript
async function myWorkflowFn() {
  const data = await DBOS.runStep(
    () => fetch("https://api.example.com/data").then(r => r.json()),
    { name: "fetchData" }
  );
  return data;
}
```

也可以使用 `DBOS.registerStep` 预注册步骤，或使用 `@DBOS.step()` 作为类装饰器，但大多数场景推荐使用 `DBOS.runStep`。

步骤要求：
- 输入和输出必须可序列化为 JSON
- 不能从步骤内部调用、启动或入队工作流
- 从一个步骤调用另一个步骤会使被调用的步骤成为调用步骤执行的一部分

何时使用步骤：
- 对外部服务的 API 调用
- 文件系统操作
- 随机数生成
- 获取当前时间
- 任何非确定性操作

参考：[DBOS Steps](https://docs.dbos.dev/typescript/tutorials/step-tutorial)
