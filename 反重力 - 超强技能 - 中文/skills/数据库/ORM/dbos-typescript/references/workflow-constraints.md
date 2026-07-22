---
title: 遵守工作流约束
impact: CRITICAL
impactDescription: 违反约束会破坏恢复和持久化保证
tags: workflow, constraints, rules, best-practices
---

## 遵守工作流约束

工作流具有特定的约束以维持持久化保证。违反它们可能破坏恢复。

**错误（从步骤启动工作流）：**

```typescript
async function myStep() {
  // 不要从步骤启动工作流！
  await DBOS.startWorkflow(otherWorkflow)();
}

async function myOtherStep() {
  // 不要从步骤调用 recv！
  const msg = await DBOS.recv("topic");
}

async function myWorkflowFn() {
  await DBOS.runStep(myStep, { name: "myStep" });
}
```

**正确（工作流操作仅在工作流中执行）：**

```typescript
async function fetchData() {
  // 步骤只执行外部操作
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  await DBOS.runStep(fetchData, { name: "fetchData" });
  // 从父工作流启动子工作流
  await DBOS.startWorkflow(otherWorkflow)();
  // 从工作流接收消息
  const msg = await DBOS.recv("topic");
  // 从工作流设置事件
  await DBOS.setEvent("status", "done");
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

其他约束：
- 不要从工作流或步骤修改全局变量
- 并行步骤必须以确定性顺序启动：

```typescript
// 正确 - 确定性启动顺序
const results = await Promise.allSettled([
  DBOS.runStep(() => step1("arg1"), { name: "step1" }),
  DBOS.runStep(() => step2("arg2"), { name: "step2" }),
  DBOS.runStep(() => step3("arg3"), { name: "step3" }),
]);
```

使用 `Promise.allSettled` 而不是 `Promise.all` 以安全处理错误，避免使 Node.js 进程崩溃。

参考：[Workflow Guarantees](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-guarantees)
