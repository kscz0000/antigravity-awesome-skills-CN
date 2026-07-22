---
title: 为步骤配置重试以应对瞬态故障
impact: HIGH
impactDescription: 自动重试无需手动代码即可处理瞬态故障
tags: step, retry, exponential-backoff, resilience
---

## 为步骤配置重试以应对瞬态故障

步骤可在失败时按指数退避自动重试。这可处理网络问题等瞬态故障。

**错误（手动重试逻辑）：**

```typescript
async function fetchData() {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await fetch("https://api.example.com").then(r => r.json());
    } catch (e) {
      if (attempt === 2) throw e;
      await new Promise(r => setTimeout(r, 2 ** attempt * 1000));
    }
  }
}
```

**正确（使用 `DBOS.runStep` 内置重试）：**

```typescript
async function fetchData() {
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  const data = await DBOS.runStep(fetchData, {
    name: "fetchData",
    retriesAllowed: true,
    maxAttempts: 10,
    intervalSeconds: 1,
    backoffRate: 2,
  });
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

使用内联箭头函数：

```typescript
async function myWorkflowFn() {
  const data = await DBOS.runStep(
    () => fetch("https://api.example.com").then(r => r.json()),
    { name: "fetchData", retriesAllowed: true, maxAttempts: 10 }
  );
}
```

重试参数：
- `retriesAllowed`：启用自动重试（默认：`false`）
- `maxAttempts`：最大重试次数（默认：`3`）
- `intervalSeconds`：重试之间的初始延迟（秒）（默认：`1`）
- `backoffRate`：指数退避乘数（默认：`2`）

使用默认值时，重试延迟为：1s, 2s, 4s, 8s, 16s...

如果所有重试都耗尽，则向调用工作流抛出 `DBOSMaxStepRetriesError`。

参考：[Configurable Retries](https://docs.dbos.dev/typescript/tutorials/step-tutorial#configurable-retries)
