---
title: 将外部操作放入步骤
impact: HIGH
impactDescription: 步骤通过 checkpoint 结果实现恢复
tags: step, external, api, checkpoint
---

## 将外部操作放入步骤

任何执行复杂操作、访问外部 API 或具有副作用的函数都应作为步骤执行。步骤结果会被 checkpoint，从而支持工作流恢复。

**错误示例（工作流中直接外部调用）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// 工作流中直接进行外部 API 调用 - 不会被 checkpoint！
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}
```

**正确示例（使用 `dbos.RunAsStep` 将外部调用放入步骤）：**

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	return data, nil
}
```

`dbos.RunAsStep` 也接受内联闭包：

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		resp, err := http.Get("https://api.example.com/data")
		if err != nil {
			return "", err
		}
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		return string(body), nil
	}, dbos.WithStepName("fetchData"))
	return data, err
}
```

步骤类型签名：`type Step[R any] func(ctx context.Context) (R, error)`

步骤要求：
- 函数必须接受一个 `context.Context` 参数 —— 使用提供的那个，而不是工作流的上下文
- 输入和输出必须可以序列化为 JSON
- 不能从步骤内部启动或入队工作流
- 在一个步骤内调用另一个步骤时，内部调用会成为外部步骤执行的一部分

何时使用步骤：
- 访问外部服务的 API 调用
- 文件系统操作
- 随机数生成
- 获取当前时间
- 任何非确定性操作

参考：[DBOS Steps](https://docs.dbos.dev/golang/tutorials/step-tutorial)
