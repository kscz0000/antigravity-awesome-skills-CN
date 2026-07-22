---
title: 正确配置并启动 DBOS
impact: CRITICAL
impactDescription: 未正确配置将导致应用程序无法运行
tags: configuration, launch, setup, initialization
---

## 正确配置并启动 DBOS

每个 DBOS 应用程序必须先创建上下文、注册工作流和队列，然后在运行任何工作流之前完成启动。

**错误示例（缺少配置或启动）：**

```go
// 没有上下文或启动！
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	return input, nil
}

func main() {
	// 这将失败 - DBOS 未初始化或未启动
	dbos.RegisterWorkflow(nil, myWorkflow) // panic: ctx cannot be nil
}
```

**正确示例（创建上下文、注册、启动）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	return input, nil
}

func main() {
	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "my-app",
		DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	})
	if err != nil {
		log.Fatal(err)
	}
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	if err := dbos.Launch(ctx); err != nil {
		log.Fatal(err)
	}

	handle, err := dbos.RunWorkflow(ctx, myWorkflow, "hello")
	if err != nil {
		log.Fatal(err)
	}
	result, err := handle.GetResult()
	fmt.Println(result) // "hello"
}
```

配置字段：
- `AppName`（必填）：应用程序标识
- `DatabaseURL`（必填，除非设置了 `SystemDBPool`）：PostgreSQL 连接字符串
- `SystemDBPool`：自定义 `*pgxpool.Pool`（优先级高于 `DatabaseURL`）
- `DatabaseSchema`：Schema 名称（默认：`"dbos"`）
- `Logger`：自定义 `*slog.Logger`（默认输出到 stdout）
- `AdminServer`：启用 HTTP admin server（默认：`false`）
- `AdminServerPort`：admin server 端口（默认：`3001`）
- `ApplicationVersion`：应用版本（未设置时根据二进制哈希自动计算）
- `ExecutorID`：执行器标识（默认：`"local"`）
- `EnablePatching`：启用代码补丁系统（默认：`false`）

参考：[Integrating DBOS](https://docs.dbos.dev/golang/integrating-dbos)
