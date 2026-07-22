---
title: 保持工作流确定性
impact: CRITICAL
impactDescription: 非确定性工作流无法正确恢复
tags: workflow, determinism, recovery, reliability
---

## 保持工作流确定性

工作流函数必须具有确定性：给定相同的输入和步骤返回值，必须以相同的顺序调用相同的步骤。非确定性操作必须移至步骤中。

**错误示例（非确定性工作流）：**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 工作流中的随机值会破坏恢复！
	// 重放时，rand.Intn 返回不同值，
	// 工作流可能走上不同分支。
	if rand.Intn(2) == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

**正确示例（非确定性操作放入步骤）：**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 步骤结果被 checkpoint - 重放时使用保存的值
	choice, err := dbos.RunAsStep(ctx, func(ctx context.Context) (int, error) {
		return rand.Intn(2), nil
	}, dbos.WithStepName("generateChoice"))
	if err != nil {
		return "", err
	}
	if choice == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

必须放入步骤的非确定性操作：
- 随机数生成
- 获取当前时间（`time.Now()`）
- 访问外部 API（`http.Get` 等）
- 读取文件
- 数据库查询

参考：[Workflow Determinism](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#determinism)
