---
title: 使用持久化睡眠实现延迟执行
impact: MEDIUM
impactDescription: 支持跨重启的可靠调度
tags: pattern, sleep, delay, durable, schedule
---

## 使用持久化睡眠实现延迟执行

在工作流内部使用 `DBOS.sleep()` 实现持久化延迟。唤醒时间存储在数据库中，因此睡眠可跨重启存活。

**错误（非持久化睡眠）：**

```typescript
async function delayedTaskFn() {
  // setTimeout 不持久 - 重启后丢失！
  await new Promise(r => setTimeout(r, 60000));
  await DBOS.runStep(doWork, { name: "doWork" });
}
const delayedTask = DBOS.registerWorkflow(delayedTaskFn);
```

**正确（持久化睡眠）：**

```typescript
async function delayedTaskFn() {
  // 持久化睡眠 - 跨重启存活
  await DBOS.sleep(60000); // 60 秒（毫秒）
  await DBOS.runStep(doWork, { name: "doWork" });
}
const delayedTask = DBOS.registerWorkflow(delayedTaskFn);
```

`DBOS.sleep()` 接受毫秒（不同于 Python 接受秒）。

使用场景：
- 调度将来运行的任务
- 实现重试延迟
- 跨越小时、天或周的延迟

```typescript
async function scheduledTaskFn(task: string) {
  // 睡眠一周
  await DBOS.sleep(7 * 24 * 60 * 60 * 1000);
  await processTask(task);
}
```

要以持久化方式获取当前时间，使用 `DBOS.now()`：

```typescript
async function myWorkflowFn() {
  const now = await DBOS.now(); // 作为步骤检查点
  // 生成随机 UUID：
  const id = await DBOS.randomUUID(); // 作为步骤检查点
}
```

参考：[Durable Sleep](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#durable-sleep)
