---
title: 对工作流进行防抖以避免无效工作
impact: MEDIUM
impactDescription: 在快速触发期间防止冗余的工作流执行
tags: pattern, debounce, delay, efficiency
---

## 对工作流进行防抖以避免无效工作

使用 `Debouncer` 延迟工作流执行，直到自上次触发后经过一段时间。这可以防止在短时间内多次触发同一工作流时的无效工作。

**错误（每次触发都执行）：**

```typescript
async function processInputFn(userInput: string) {
  // 昂贵的处理
}
const processInput = DBOS.registerWorkflow(processInputFn);

// 每次按键都触发新工作流 - 浪费！
async function onInputChange(userInput: string) {
  await processInput(userInput);
}
```

**正确（使用 Debouncer）：**

```typescript
import { DBOS, Debouncer } from "@dbos-inc/dbos-sdk";

async function processInputFn(userInput: string) {
  // 昂贵的处理
}
const processInput = DBOS.registerWorkflow(processInputFn);

const debouncer = new Debouncer({
  workflow: processInput,
  debounceTimeoutMs: 120000, // 最大等待：2 分钟
});

async function onInputChange(userId: string, userInput: string) {
  // 自上次调用起延迟 60 秒执行
  // 最终执行时使用最后一组输入
  await debouncer.debounce(userId, 60000, userInput);
}
```

关键行为：
- `debounceKey` 将被一起防抖的执行分组（例如，每个用户一组）
- `debouncePeriodMs` 自上次调用起延迟执行这么多时间
- `debounceTimeoutMs` 设置自首次触发起的最大等待时间
- 工作流最终执行时使用**最后**一组输入
- 执行开始后，下一次 `debounce` 调用将开启新的周期
- `ConfiguredInstance` 类的工作流不能被防抖

参考：[Debouncing Workflows](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#debouncing-workflows)
