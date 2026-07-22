---
title: 使用 Patching 安全升级工作流
impact: LOW
impactDescription: 在不中断进行中工作流的前提下安全部署破坏性变更
tags: advanced, patching, upgrade, breaking-change
---

## 使用 Patching 安全升级工作流

使用 `dbos.Patch` 安全地部署工作流代码的破坏性变更。破坏性变更会改变步骤的执行顺序或具体内容，可能导致恢复失败。

**错误示例（无补丁直接破坏性变更）：**

```go
// 之前：原始工作流
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, foo, dbos.WithStepName("foo"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}

// 之后：破坏性变更 - 进行中的工作流恢复将失败！
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz")) // 步骤已变更
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

**正确示例（使用 patch）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	useBaz, err := dbos.Patch(ctx, "use-baz")
	if err != nil {
		return "", err
	}
	var result string
	if useBaz {
		result, _ = dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz")) // 新工作流
	} else {
		result, _ = dbos.RunAsStep(ctx, foo, dbos.WithStepName("foo")) // 旧工作流
	}
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

`dbos.Patch` 对新工作流返回 `true`，对补丁前已开始的工作流返回 `false`。

**废弃补丁（所有旧工作流完成后）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	dbos.DeprecatePatch(ctx, "use-baz") // 始终走新路径
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

**移除补丁（所有使用 DeprecatePatch 的工作流完成后）：**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

生命周期：`Patch()` → 部署 → 等待旧工作流完成 → `DeprecatePatch()` → 部署 → 等待 → 完全移除补丁。

**必需配置** —— 必须显式启用 patching：

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:        "my-app",
	DatabaseURL:    os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	EnablePatching: true, // dbos.Patch 和 dbos.DeprecatePatch 必需
})
```

若未设置 `EnablePatching: true`，调用 `dbos.Patch` 和 `dbos.DeprecatePatch` 将失败。

参考：[Patching](https://docs.dbos.dev/golang/tutorials/upgrading-workflows#patching)
