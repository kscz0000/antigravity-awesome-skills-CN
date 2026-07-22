---
title: 使用持久化 Sleep 实现延迟执行
impact: MEDIUM
impactDescription: 在重启后仍能可靠调度
tags: pattern, sleep, delay, durable, schedule
---

## 使用持久化 Sleep 实现延迟执行

在工作流内部使用 `dbos.Sleep` 实现持久化延迟。唤醒时间存储在数据库中，因此 sleep 可以跨重启存活。

**错误示例（非持久化 sleep）：**

```go
func delayedTask(ctx dbos.DBOSContext, input string) (string, error) {
	// time.Sleep 不具备持久性 - 重启后丢失！
	time.Sleep(60 * time.Second)
	result, err := dbos.RunAsStep(ctx, doWork, dbos.WithStepName("doWork"))
	return result, err
}
```

**正确示例（持久化 sleep）：**

```go
func delayedTask(ctx dbos.DBOSContext, input string) (string, error) {
	// 持久化 sleep - 跨重启存活
	_, err := dbos.Sleep(ctx, 60*time.Second)
	if err != nil {
		return "", err
	}
	result, err := dbos.RunAsStep(ctx, doWork, dbos.WithStepName("doWork"))
	return result, err
}
```

`dbos.Sleep` 接受一个 `time.Duration`。返回剩余的 sleep 时长（正常完成时为零）。

使用场景：
- 调度任务在未来某个时间运行
- 实现重试延迟
- 跨越小时、天或周的延迟

```go
func scheduledTask(ctx dbos.DBOSContext, task string) (string, error) {
	// Sleep 一周
	dbos.Sleep(ctx, 7*24*time.Hour)
	return processTask(task)
}
```

参考：[Durable Sleep](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#durable-sleep)
