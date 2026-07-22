---
title: 使用 Streams 进行实时数据传输
impact: MEDIUM
impactDescription: 允许从长时间运行的工作流流式输出结果
tags: communication, stream, real-time, channel
---

## 使用 Streams 进行实时数据传输

工作流可以使用 `dbos.WriteStream`、`dbos.CloseStream` 和 `dbos.ReadStream`/`dbos.ReadStreamAsync` 实时向客户端流式传输数据。适用于 LLM 输出流式传输或进度上报。

**错误示例（累积结果后在末尾一次性返回）：**

```go
func processWorkflow(ctx dbos.DBOSContext, items []string) ([]string, error) {
	var results []string
	for _, item := range items {
		result, _ := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return processItem(item)
		}, dbos.WithStepName("process"))
		results = append(results, result)
	}
	return results, nil // 客户端必须等待整个工作流完成
}
```

**正确示例（结果可用时立即流式输出）：**

```go
func processWorkflow(ctx dbos.DBOSContext, items []string) (string, error) {
	for _, item := range items {
		result, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return processItem(item)
		}, dbos.WithStepName("process"))
		if err != nil {
			return "", err
		}
		dbos.WriteStream(ctx, "results", result)
	}
	dbos.CloseStream(ctx, "results") // 标记完成
	return "done", nil
}

// 同步读取流（阻塞至流关闭）
handle, _ := dbos.RunWorkflow(ctx, processWorkflow, items)
values, closed, err := dbos.ReadStreamstring, "results")
```

**使用 channel 进行异步流读取：**

```go
ch, err := dbos.ReadStreamAsyncstring, "results")
if err != nil {
	log.Fatal(err)
}
for sv := range ch {
	if sv.Err != nil {
		log.Fatal(sv.Err)
	}
	if sv.Closed {
		break
	}
	fmt.Println("Received:", sv.Value)
}
```

关键行为：
- 一个工作流可以有任意数量的流，每个流以唯一 key 标识
- 流不可变，仅追加
- 工作流中的写入保证恰好一次
- 工作流终止时流自动关闭
- `ReadStream` 阻塞至工作流不活跃或流关闭
- `ReadStreamAsync` 返回 `StreamValue[R]` 类型的 channel，实现非阻塞读取

参考：[Workflow Streaming](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-streaming)
