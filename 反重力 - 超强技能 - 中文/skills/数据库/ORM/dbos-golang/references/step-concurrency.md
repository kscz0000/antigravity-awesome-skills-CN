---
title: 使用 Go 和 Select 并发执行步骤
impact: HIGH
impactDescription: 通过持久化 checkpoint 实现步骤的并行执行
tags: step, concurrency, goroutine, select, parallel
---

## 使用 Go 和 Select 并发执行步骤

使用 `dbos.Go` 在 goroutine 中并发执行步骤，使用 `dbos.Select` 持久化地选择最先完成的结果。这两个操作都会被 checkpoint 以支持恢复。

**错误示例（无 checkpoint 的裸 goroutine）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 裸 goroutine 不会被 checkpoint - 恢复时会失败！
	ch := make(chan string, 2)
	go func() { ch <- callAPI1() }()
	go func() { ch <- callAPI2() }()
	return <-ch, nil
}
```

**正确示例（使用 dbos.Go 并发执行步骤）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 并发启动步骤
	ch1, err := dbos.Go(ctx, func(ctx context.Context) (string, error) {
		return callAPI1(ctx)
	}, dbos.WithStepName("api1"))
	if err != nil {
		return "", err
	}

	ch2, err := dbos.Go(ctx, func(ctx context.Context) (string, error) {
		return callAPI2(ctx)
	}, dbos.WithStepName("api2"))
	if err != nil {
		return "", err
	}

	// 等待第一个结果（持久化 select）
	result, err := dbos.Select(ctx, []<-chan dbos.StepOutcome[string]{ch1, ch2})
	if err != nil {
		return "", err
	}
	return result, nil
}
```

**等待所有并发步骤完成：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) ([]string, error) {
	ch1, _ := dbos.Go(ctx, step1, dbos.WithStepName("step1"))
	ch2, _ := dbos.Go(ctx, step2, dbos.WithStepName("step2"))
	ch3, _ := dbos.Go(ctx, step3, dbos.WithStepName("step3"))

	// 收集所有结果
	results := make([]string, 3)
	for i, ch := range []<-chan dbos.StepOutcome[string]{ch1, ch2, ch3} {
		outcome := <-ch
		if outcome.Err != nil {
			return nil, outcome.Err
		}
		results[i] = outcome.Result
	}
	return results, nil
}
```

关键行为：
- `dbos.Go` 在 goroutine 中启动一个步骤并返回 `StepOutcome[R]` 类型的 channel
- `dbos.Select` 持久化地选择最先完成的结果，并 checkpoint 所选的 channel
- 恢复时，`Select` 重放相同的选择，保持确定性
- 使用 `Go` 启动的步骤与 `RunAsStep` 遵循相同的重试和 checkpoint 规则

参考：[Concurrent Steps](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#concurrent-steps)
