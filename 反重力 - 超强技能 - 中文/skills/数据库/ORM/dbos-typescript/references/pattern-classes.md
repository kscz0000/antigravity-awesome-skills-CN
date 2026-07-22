---
title: 在类实例中使用 DBOS
impact: MEDIUM
impactDescription: 支持可配置的工作流实例并提供恢复能力
tags: pattern, class, instance, ConfiguredInstance
---

## 在类实例中使用 DBOS

类实例方法可作为工作流和步骤。具有工作流方法的类必须继承 `ConfiguredInstance` 以启用恢复。

**错误（实例工作流未使用 ConfiguredInstance）：**

```typescript
class MyWorker {
  constructor(private config: any) {}

  @DBOS.workflow()
  async processTask(task: string) {
    // 恢复无效 - DBOS 重启后找不到该实例
  }
}
```

**正确（继承 ConfiguredInstance）：**

```typescript
import { DBOS, ConfiguredInstance } from "@dbos-inc/dbos-sdk";

class MyWorker extends ConfiguredInstance {
  cfg: WorkerConfig;

  constructor(name: string, config: WorkerConfig) {
    super(name); // 需要唯一名称以支持恢复
    this.cfg = config;
  }

  override async initialize(): Promise<void> {
    // 可选：在 DBOS.launch() 时验证配置
  }

  @DBOS.workflow()
  async processTask(task: string): Promise<void> {
    // 可安全使用 this.cfg - 实例可恢复
    const result = await DBOS.runStep(
      () => fetch(this.cfg.apiUrl).then(r => r.text()),
      { name: "callApi" }
    );
  }
}

// 在 DBOS.launch() 之前创建实例
const worker1 = new MyWorker("worker-us", { apiUrl: "https://us.api.com" });
const worker2 = new MyWorker("worker-eu", { apiUrl: "https://eu.api.com" });

// 然后启动
await DBOS.launch();
```

关键要求：
- `ConfiguredInstance` 构造函数要求每个类有唯一的 `name`
- 所有实例必须在 `DBOS.launch()` **之前**创建
- `initialize()` 方法在启动期间被调用以进行验证
- 在实例工作流内部使用 `DBOS.runStep` 执行步骤操作
- 事件注册装饰器（如 `@DBOS.scheduled`）不能应用于实例方法

参考：[Using TypeScript Objects](https://docs.dbos.dev/typescript/tutorials/instantiated-objects)
