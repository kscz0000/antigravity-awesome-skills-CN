---
title: 为 DBOS 搭建合适的测试环境
impact: LOW-MEDIUM
impactDescription: 通过正确的 DBOS 生命周期管理保证测试结果稳定
tags: testing, go-test, setup, integration, mock
---

## 为 DBOS 搭建合适的测试环境

DBOS 应用程序可以通过单元测试（mock DBOSContext）或集成测试（真实 Postgres 数据库）进行测试。

**错误示例（测试之间没有生命周期管理）：**

```go
// 测试之间共享状态 - 结果不稳定！
func TestOne(t *testing.T) {
	myWorkflow(ctx, "input")
}
func TestTwo(t *testing.T) {
	// 上一个测试的状态泄漏到本测试
	myWorkflow(ctx, "input")
}
```

**正确示例（使用 mock 进行单元测试）：**

`DBOSContext` 接口完全可以 mock。使用类似 `testify/mock` 或 `mockery` 的 mock 库：

```go
func TestWorkflow(t *testing.T) {
	mockCtx := mocks.NewMockDBOSContext(t)

	// Mock RunAsStep 以返回预设值
	mockCtx.On("RunAsStep", mockCtx, mock.Anything, mock.Anything).
		Return("mock-result", nil)

	result, err := myWorkflow(mockCtx, "input")
	assert.NoError(t, err)
	assert.Equal(t, "expected", result)

	mockCtx.AssertExpectations(t)
}
```

**正确示例（使用 Postgres 进行集成测试）：**

```go
func setupDBOS(t *testing.T) dbos.DBOSContext {
	t.Helper()
	databaseURL := os.Getenv("DBOS_TEST_DATABASE_URL")
	if databaseURL == "" {
		t.Skip("DBOS_TEST_DATABASE_URL not set")
	}

	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "test-" + t.Name(),
		DatabaseURL: databaseURL,
	})
	require.NoError(t, err)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	err = dbos.Launch(ctx)
	require.NoError(t, err)

	t.Cleanup(func() {
		dbos.Shutdown(ctx, 10*time.Second)
	})
	return ctx
}

func TestWorkflowIntegration(t *testing.T) {
	ctx := setupDBOS(t)

	handle, err := dbos.RunWorkflow(ctx, myWorkflow, "test-input")
	require.NoError(t, err)

	result, err := handle.GetResult()
	require.NoError(t, err)
	assert.Equal(t, "expected-output", result)
}
```

关键要点：
- 使用 `t.Cleanup` 确保每个测试结束后调用 `Shutdown`
- 每个测试使用唯一的 `AppName` 以避免冲突
- Mock `DBOSContext` 实现无 Postgres 的快速单元测试
- 使用真实 Postgres 进行验证持久化行为的集成测试

参考：[Testing DBOS](https://docs.dbos.dev/golang/tutorials/testing)
