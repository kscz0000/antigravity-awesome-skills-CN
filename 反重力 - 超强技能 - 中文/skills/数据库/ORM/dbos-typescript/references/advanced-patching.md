---
title: 使用 Patching 安全升级工作流
impact: LOW
impactDescription: 安全部署破坏性工作流变更，不影响进行中的工作流
tags: advanced, patching, upgrade, breaking-change
---

## 使用 Patching 安全升级工作流

使用 `DBOS.patch()` 安全地部署工作流代码的破坏性变更。破坏性变更会改变运行的步骤或其顺序，可能导致恢复失败。

**错误（未使用 patching 的破坏性变更）：**

```typescript
// 之前：原始工作流
async function workflowFn() {
  await foo();
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);

// 之后：破坏性变更 - 进行中的工作流恢复将失败！
async function workflowFn() {
  await baz(); // 变更后的步骤
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

**正确（使用 patch）：**

```typescript
async function workflowFn() {
  if (await DBOS.patch("use-baz")) {
    await baz(); // 新工作流运行此分支
  } else {
    await foo(); // 旧工作流继续运行原代码
  }
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

`DBOS.patch()` 对新工作流返回 `true`，对在补丁之前启动的工作流返回 `false`。

**废弃补丁（所有旧工作流完成后）：**

```typescript
async function workflowFn() {
  if (await DBOS.deprecatePatch("use-baz")) { // 始终返回 true
    await baz();
  }
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

**移除补丁（所有使用 deprecatePatch 的工作流完成后）：**

```typescript
async function workflowFn() {
  await baz();
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

生命周期：`patch()` → 部署 → 等待旧工作流 → `deprecatePatch()` → 部署 → 等待 → 完全移除补丁。

使用 `DBOS.listWorkflows` 检查进行中的旧工作流，然后再废弃或移除补丁。

参考：[Patching](https://docs.dbos.dev/typescript/tutorials/upgrading-workflows#patching)
