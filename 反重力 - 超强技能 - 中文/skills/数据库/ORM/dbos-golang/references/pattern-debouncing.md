---
title: 防抖工作流以避免无效执行
impact: MEDIUM
impactDescription: 在快速连续触发时避免冗余的工作流执行
tags: pattern, debounce, delay, efficiency
---

## 防抖工作流以避免无效执行

使用 `dbos.NewDebouncer` 延迟工作流执行，直至距上次触发经过一段时间。这可以避免在工作流短时间内被多次触发时产生的无效工作。

**错误示例（每次触发都执行）：**

```go
// 每次按键都触发新工作流 - 浪费资源！
func onInputChange(ctx dbos.DBOSContext, userInput string) {
	dbos.RunWorkflow(ctx, processInput, userInput)
}
```

**正确示例（使用 Debouncer）：**

```go
// 在 Launch() 之前创建 debouncer
debouncer := dbos.NewDebouncer(ctx, processInput,
	dbos.WithDebouncerTimeout(120*time.Second), // 最长等待：2 分钟
)

func onInputChange(ctx dbos.DBOSContext, userID, userInput string) error {
	// 从最后一次调用起延迟 60 秒执行
	// 最终执行时使用最后一组输入
	_, err := debouncer.Debounce(ctx, userID, 60*time.Second, userInput)
	return err
}
```

关键行为：
- `Debounce` 的第一个参数是防抖 key，用于将执行分组（例如按用户）
- 第二个参数是自上次调用起的延迟时长
- `WithDebouncerTimeout` 设置自首次触发起的最长等待时间
- 工作流最终执行时使用**最后**一组输入
- 执行开始后，下一次 `Debounce` 调用将开启新的周期
- Debouncer 必须在 `Launch()` **之前**创建

类型签名：`Debouncer[P any, R any]` —— 类型参数与目标工作流一致。

参考：[Debouncing Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#debouncing)
