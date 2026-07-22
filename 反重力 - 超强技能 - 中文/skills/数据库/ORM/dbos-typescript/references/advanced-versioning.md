---
title: 使用 Versioning 进行蓝绿部署
impact: LOW
impactDescription: 支持新旧代码版本安全并行部署
tags: advanced, versioning, blue-green, deployment
---

## 使用 Versioning 进行蓝绿部署

在配置中设置 `applicationVersion` 以给工作流打上版本标签。DBOS 只恢复与当前应用版本匹配的工作流，防止恢复期间的代码不匹配。

**错误（部署破坏进行中工作流的新代码）：**

```typescript
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  // 未设置版本 - 无论代码版本如何都恢复所有工作流
});
```

**正确（版本化部署）：**

```typescript
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  applicationVersion: "2.0.0",
});
```

默认情况下，应用版本从工作流源代码的哈希自动计算。显式设置可获得更多控制。

**蓝绿部署策略：**

1. 并行部署新版本（v2）和旧版本（v1）
2. 将新流量引导到 v2 进程
3. 让 v1 进程"排空"（完成进行中的工作流）
4. 检查剩余的 v1 工作流：

```typescript
const oldWorkflows = await DBOS.listWorkflows({
  applicationVersion: "1.0.0",
  status: "PENDING",
});
```

5. 一旦所有 v1 工作流完成，停用 v1 进程

**分叉到新版本（针对卡住的工作流）：**

```typescript
// 将工作流从失败步骤分叉到新版本运行
const handle = await DBOS.forkWorkflow<string>(
  workflowID,
  failedStepID,
  { applicationVersion: "2.0.0" }
);
```

参考：[Versioning](https://docs.dbos.dev/typescript/tutorials/upgrading-workflows#versioning)
