---
title: 创建定时工作流
impact: MEDIUM
impactDescription: 支持周期性任务，且每个周期保证精确执行一次
tags: pattern, scheduled, cron, recurring
---

## 创建定时工作流

使用 `DBOS.registerScheduled` 按 cron 计划运行工作流。每次定时调用在每个周期精确执行一次。

**错误（使用 setInterval 手动调度）：**

```typescript
// 手动调度不持久，宕机期间会错过周期
setInterval(async () => {
  await generateReport();
}, 60000);
```

**正确（使用 DBOS.registerScheduled）：**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function everyThirtySecondsFn(scheduledTime: Date, actualTime: Date) {
  DBOS.logger.info("Running scheduled task");
}
const everyThirtySeconds = DBOS.registerWorkflow(everyThirtySecondsFn);
DBOS.registerScheduled(everyThirtySeconds, { crontab: "*/30 * * * * *" });

async function dailyReportFn(scheduledTime: Date, actualTime: Date) {
  await DBOS.runStep(generateReport, { name: "generateReport" });
}
const dailyReport = DBOS.registerWorkflow(dailyReportFn);
DBOS.registerScheduled(dailyReport, { crontab: "0 9 * * *" });
```

定时工作流必须接受恰好两个参数：`scheduledTime`（Date）和 `actualTime`（Date）。

DBOS crontab 支持 5 或 6 个字段（秒可选）：
```text
┌────────────── 秒（可选）
│ ┌──────────── 分钟
│ │ ┌────────── 小时
│ │ │ ┌──────── 日
│ │ │ │ ┌────── 月
│ │ │ │ │ ┌──── 星期
* * * * * *
```

追溯执行（针对错过的周期）：

```typescript
import { DBOS, SchedulerMode } from "@dbos-inc/dbos-sdk";

async function fridayNightJobFn(scheduledTime: Date, actualTime: Date) {
  // 即使应用在计划时间处于离线状态也会运行
}
const fridayNightJob = DBOS.registerWorkflow(fridayNightJobFn);
DBOS.registerScheduled(fridayNightJob, {
  crontab: "0 21 * * 5",
  mode: SchedulerMode.ExactlyOncePerInterval,
});
```

定时工作流不能应用于实例方法。

参考：[Scheduled Workflows](https://docs.dbos.dev/typescript/tutorials/scheduled-workflows)
