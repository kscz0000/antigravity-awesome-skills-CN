---
title: 正确配置和启动 DBOS
impact: CRITICAL
impactDescription: 没有正确设置应用将无法运行
tags: configuration, launch, setup, initialization
---

## 正确配置和启动 DBOS

每个 DBOS 应用必须在运行任何工作流之前配置并启动 DBOS。所有工作流和步骤必须在调用 `DBOS.launch()` 之前注册。

**错误（缺少配置或启动）：**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

// 没有配置或启动！
async function myWorkflowFn() {
  // 这将失败 - DBOS 未启动
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
await myWorkflow();
```

**正确（在 main 中配置并启动）：**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function myWorkflowFn() {
  // 工作流逻辑
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  await myWorkflow();
}

main().catch(console.log);
```

参考：[DBOS Lifecycle](https://docs.dbos.dev/typescript/reference/dbos-class)
