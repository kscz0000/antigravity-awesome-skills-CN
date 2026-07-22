---
title: 将 DBOS 与 Express 集成
impact: CRITICAL
impactDescription: 正确集成确保工作流在服务器重启后存活
tags: express, http, integration, server
---

## 将 DBOS 与 Express 集成

在启动 Express 服务器之前配置并启动 DBOS。所有工作流和步骤必须在调用 `DBOS.launch()` 之前注册。

**错误（服务器启动前未启动 DBOS）：**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// 服务器未启动 DBOS 就启动了！
app.listen(3000);
```

**正确（先启动 DBOS，再启动 Express）：**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

app.post("/process", async (req, res) => {
  const handle = await DBOS.startWorkflow(processTask)(req.body.data);
  res.json({ workflowID: handle.workflowID });
});

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  app.listen(3000, () => {
    console.log("Server running on port 3000");
  });
}

main().catch(console.log);
```

参考：[Integrating DBOS](https://docs.dbos.dev/typescript/integrating-dbos)
