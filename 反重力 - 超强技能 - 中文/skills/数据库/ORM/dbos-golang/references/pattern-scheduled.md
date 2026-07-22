---
title: 创建定时工作流
impact: MEDIUM
impactDescription: 为周期性任务提供每个间隔恰好一次的保证
tags: pattern, scheduled, cron, recurring
---

## 创建定时工作流

在注册工作流时使用 `dbos.WithSchedule` 让其按 cron 计划运行。每次定时调用在每个间隔内恰好执行一次。

**错误示例（使用 goroutine 手动调度）：**

```go
// 手动调度不具备持久性，且停机时会错过间隔
go func() {
	for {
		generateReport()
		time.Sleep(60 * time.Second)
	}
}()
```

**正确示例（使用 WithSchedule）：**

```go
// 定时工作流必须接受 time.Time 作为输入
func everyThirtySeconds(ctx dbos.DBOSContext, scheduledTime time.Time) (string, error) {
	fmt.Println("Running scheduled task at:", scheduledTime)
	return "done", nil
}

func dailyReport(ctx dbos.DBOSContext, scheduledTime time.Time) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return generateReport()
	}, dbos.WithStepName("generateReport"))
	return "report generated", err
}

func main() {
	ctx, _ := dbos.NewDBOSContext(context.Background(), config)
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, everyThirtySeconds,
		dbos.WithSchedule("*/30 * * * * *"),
	)
	dbos.RegisterWorkflow(ctx, dailyReport,
		dbos.WithSchedule("0 0 9 * * *"), // 每天上午 9 点
	)

	dbos.Launch(ctx)
	select {} // 永久阻塞
}
```

定时工作流必须接受一个 `time.Time` 类型的参数，表示定时执行的时间。

DBOS crontab 使用 6 个字段，支持秒级精度：
```text
┌────────────── 秒
│ ┌──────────── 分钟
│ │ ┌────────── 小时
│ │ │ ┌──────── 日
│ │ │ │ ┌────── 月
│ │ │ │ │ ┌──── 星期
* * * * * *
```

参考：[Scheduled Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#scheduled-workflows)
