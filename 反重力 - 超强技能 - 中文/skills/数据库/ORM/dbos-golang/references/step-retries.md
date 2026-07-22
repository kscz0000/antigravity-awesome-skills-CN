---
title: 为步骤配置重试以应对瞬时故障
impact: HIGH
impactDescription: 自动重试可在不写额外代码的情况下处理瞬时故障
tags: step, retry, exponential-backoff, resilience
---

## 为步骤配置重试以应对瞬时故障

步骤可在失败时按指数退避策略自动重试。这可以处理网络问题等瞬时故障。

**错误示例（手动重试逻辑）：**

```go
func fetchData(ctx context.Context) (string, error) {
	var lastErr error
	for attempt := 0; attempt < 3; attempt++ {
		resp, err := http.Get("https://api.example.com")
		if err == nil {
			defer resp.Body.Close()
			body, _ := io.ReadAll(resp.Body)
			return string(body), nil
		}
		lastErr = err
		time.Sleep(time.Duration(math.Pow(2, float64(attempt))) * time.Second)
	}
	return "", lastErr
}
```

**正确示例（使用 `dbos.RunAsStep` 内置重试）：**

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData,
		dbos.WithStepName("fetchData"),
		dbos.WithStepMaxRetries(10),
		dbos.WithBaseInterval(500*time.Millisecond),
		dbos.WithBackoffFactor(2.0),
		dbos.WithMaxInterval(5*time.Second),
	)
	return data, err
}
```

重试参数：
- `WithStepMaxRetries(n)`：最大重试次数（默认：`0` —— 不重试）
- `WithBaseInterval(d)`：首次重试间隔（默认：`100ms`）
- `WithBackoffFactor(f)`：指数退避倍数（默认：`2.0`）
- `WithMaxInterval(d)`：重试之间的最大间隔（默认：`5s`）

使用默认参数时，重试间隔为：100ms、200ms、400ms、800ms、1.6s、3.2s、5s、5s……

如果重试全部耗尽，将向调用工作流返回 code 为 `MaxStepRetriesExceeded` 的 `DBOSError`。

参考：[Configurable Retries](https://docs.dbos.dev/golang/tutorials/step-tutorial#configurable-retries)
