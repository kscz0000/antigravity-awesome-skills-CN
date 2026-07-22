---
title: 使用版本管理实现蓝绿部署
impact: LOW
impactDescription: 在新代码版本与旧版本并存时实现安全部署
tags: advanced, versioning, blue-green, deployment
---

## 使用版本管理实现蓝绿部署

在配置中设置 `ApplicationVersion` 以给工作流打版本标签。DBOS 仅恢复与当前应用版本匹配的工作流，避免恢复期间出现代码不匹配。

**错误示例（部署新代码破坏进行中的工作流）：**

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:     "my-app",
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	// 未设置版本 - 版本根据二进制哈希自动计算
	// 旧工作流将用新代码恢复，可能导致故障
})
```

**正确示例（带版本的部署）：**

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:            "my-app",
	DatabaseURL:        os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	ApplicationVersion: "2.0.0",
})
```

默认情况下，应用版本通过可执行二进制文件的 SHA-256 哈希自动计算。显式设置可以获得更多控制权。

**蓝绿部署策略：**

1. 与旧版本（v1）并行部署新版本（v2）
2. 将新流量导向 v2 进程
3. 让 v1 进程"排空"（完成进行中的工作流）
4. 检查剩余的 v1 工作流：

```go
oldWorkflows, _ := dbos.ListWorkflows(ctx,
	dbos.WithAppVersion("1.0.0"),
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusPending}),
)
```

5. 一旦所有 v1 工作流完成，退役 v1 进程

**分叉到新版本（用于卡住的工作流）：**

```go
// 将工作流从失败的步骤分叉到新版本运行
handle, _ := dbos.ForkWorkflowstring
```

参考：[Versioning](https://docs.dbos.dev/golang/tutorials/upgrading-workflows#versioning)
