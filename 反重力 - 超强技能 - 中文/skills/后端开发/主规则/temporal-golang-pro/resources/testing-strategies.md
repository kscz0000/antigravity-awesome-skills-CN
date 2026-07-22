# Temporal Go 测试策略

测试 Go 中的工作流和 Activity 需要深入理解 `testsuite` 包，它提供了支持确定性时间跳过的 Mock 环境。

## 测试套件配置

始终使用 `WorkflowTestSuite` 在同一文件的多个测试间保持状态。

```go
// Requires: "github.com/stretchr/testify/suite", "go.temporal.io/sdk/testsuite"
type MyTestSuite struct {
    suite.Suite
    testsuite.WorkflowTestSuite
    env *testsuite.TestWorkflowEnvironment
}

func (s *MyTestSuite) SetupTest() {
    s.env = s.NewTestWorkflowEnvironment()
}

func TestMyTestSuite(t *testing.T) {
    suite.Run(t, new(MyTestSuite))
}
```

## 1. 工作流单元测试

Go SDK 最强大的特性是**时间跳过**。一个休眠 30 天的工作流在测试中几毫秒就能完成。

### Mock Activity

必须在运行工作流前注册 Activity Mock。

```go
func (s *MyTestSuite) Test_SuccessfulWorkflow() {
    // Mock the activity
    s.env.OnActivity(MyActivity, mock.Anything, "input").Return("output", nil)

    s.env.ExecuteWorkflow(MyWorkflow, "input")

    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())

    var result string
    s.env.GetWorkflowResult(&result)
    s.Equal("Completed", result)
}
```

### Mock 子工作流

与 Activity 类似，使用 `OnChildWorkflow`。

```go
s.env.OnChildWorkflow(MyChildWorkflow, mock.Anything, "args").Return("result", nil)
```

## 2. Activity 单元测试

使用 `TestActivityEnvironment` 独立测试 Activity。

```go
// Requires: "go.temporal.io/sdk/testsuite", "github.com/stretchr/testify/assert"
func Test_Activity(t *testing.T) {
    testSuite := &testsuite.WorkflowTestSuite{}
    env := testSuite.NewTestActivityEnvironment()

    env.RegisterActivity(MyActivity)

    val, err := env.ExecuteActivity(MyActivity, "input")
    assert.NoError(t, err)

    var result string
    val.Get(&result)
    assert.Equal(t, "expected", result)
}
```

## 3. 重放测试（确定性检查）

重放测试确保新的代码变更不会破坏正在运行的工作流。

```go
func Test_ReplayStaticHistory(t *testing.T) {
    replayer := worker.NewWorkflowReplayer()

    replayer.RegisterWorkflow(MyWorkflow)

    // Load history from JSON file (exported from Temporal Web UI or CLI).
    // Web UI: Workflow Detail -> Download History (JSON)
    // CLI:    temporal workflow show --workflow-id <id> --namespace <ns> --output json > history.json
    err := replayer.ReplayWorkflowHistoryFromJSONFile(
        worker.ReplayWorkflowHistoryFromJSONFileOptions{},
        "history.json",
    )
    assert.NoError(t, err)
}
```

## 4. 测试 Signal 和 Query

可以在测试中的特定时间点发送 Signal。

```go
func (s *MyTestSuite) Test_WorkflowWithSignal() {
    // Delayed signal
    s.env.RegisterDelayedCallback(func() {
        s.env.SignalWorkflow("my-signal", "data")
    }, time.Hour) // This hour passes instantly!

    s.env.ExecuteWorkflow(MyWorkflow)

    // Query state after signal
    res, err := s.env.QueryWorkflow("get-state")
    s.NoError(err)
    var state string
    res.Get(&state)
    s.Equal("SignalReceived", state)
}
```

## 测试最佳实践

- **>=80% 覆盖率**：工作流逻辑力争高覆盖率，因为 Activity 通常只是 DB/API 调用的封装。
- **断言驱动**：使用 `testify/assert` 或 `testify/suite` 编写清晰的断言。
- **Mock 所有外部依赖**：单元测试中绝不调用真实数据库或 API。
- **测试失败路径**：显式测试 Activity 返回错误或心跳超时的情况。

### 示例：测试 Activity 失败路径

```go
func (s *MyTestSuite) Test_WorkflowHandlesActivityError() {
    // Mock the activity to return a non-retryable error
    s.env.OnActivity(ChargePaymentActivity, mock.Anything, mock.Anything).
        Return("", temporal.NewNonRetryableApplicationError("card declined", "PaymentError", nil))

    s.env.ExecuteWorkflow(SubscriptionWorkflow, "user-123")

    s.True(s.env.IsWorkflowCompleted())
    // Verify the workflow correctly surfaces the error
    err := s.env.GetWorkflowError()
    s.Error(err)
    s.Contains(err.Error(), "card declined")
}
```
