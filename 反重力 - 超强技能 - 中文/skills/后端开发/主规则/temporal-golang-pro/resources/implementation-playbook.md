# Temporal Go 实现手册

本手册提供使用 Temporal Go SDK 实现持久化编排的生产级模式和深度技术指导。

## 目录

1. [确定性戒律](#确定性戒律)
2. [工作流版本管理](#工作流版本管理)
3. [Activity 设计与幂等性](#activity-设计与幂等性)
4. [规模化 Worker 配置](#规模化-worker-配置)
5. [Context 与心跳](#context-与心跳)
6. [拦截器与可观测性](#拦截器与可观测性)

---

## 1. 确定性戒律

在 Go 中，工作流是必须完全一致重放的状态机。违反这些规则会导致 "Determinism Mismatch" 错误。

### ❌ 禁止使用原生 Go 并发

- **错误**：`go myFunc()`
- **正确**：`workflow.Go(ctx, func(ctx workflow.Context) { ... })`
- **原因**：`workflow.Go` 允许 Temporal 编排器在重放期间追踪和暂停 goroutine。

### ❌ 禁止使用原生时间函数

- **错误**：`time.Now()`、`time.Sleep(d)`、`time.After(d)`
- **正确**：`workflow.Now(ctx)`、`workflow.Sleep(ctx, d)`、`workflow.NewTimer(ctx, d)`

### ❌ 禁止使用非确定性 Map 遍历

- **错误**：`for k, v := range myMap { ... }`
- **正确**：收集键、排序后再遍历。
- ```go
  keys := make([]string, 0, len(myMap))
  for k := range myMap { keys = append(keys, k) }
  sort.Strings(keys)
  for _, k := range keys { v := myMap[k]; ... }
  ```

### ❌ 禁止直接进行外部 I/O

- **错误**：在工作流内使用 `http.Get("https://api.example.com")` 或 `os.ReadFile("data.txt")`。
- **正确**：将所有 I/O 封装为 Activity，通过 `workflow.ExecuteActivity` 调用。
- **原因**：外部调用是非确定性的；重放时结果会变化。

### ❌ 禁止使用非确定性随机数

- **错误**：在工作流内使用 `rand.Int()`、`uuid.New()`。
- **正确**：将随机种子或 UUID 作为工作流输入参数传入，或在 Activity 内生成。
- **原因**：`rand.Int()` 每次重放产生不同值，导致确定性不匹配。

---

## 2. 工作流版本管理

需要变更运行中工作流的逻辑时，必须使用 `workflow.GetVersion`。

### 模式：安全逻辑更新

```go
const VersionV2 = 1

func MyWorkflow(ctx workflow.Context) error {
    v := workflow.GetVersion(ctx, "ChangePaymentStep", workflow.DefaultVersion, VersionV2)

    if v == workflow.DefaultVersion {
        // Old logic: kept alive until all pre-existing workflow runs complete.
        return workflow.ExecuteActivity(ctx, OldActivity).Get(ctx, nil)
    }
    // New logic: all new and resumed workflow runs use this path.
    return workflow.ExecuteActivity(ctx, NewActivity).Get(ctx, nil)
}
```

### 模式：完全迁移后的清理

确认**没有运行中的工作流实例**处于 `DefaultVersion` 后（通过 Temporal Web UI 或 `tctl` 验证），即可安全移除旧分支：

```go
func MyWorkflow(ctx workflow.Context) error {
    // Pin minimum version to V2; histories from before the migration will
    // fail the determinism check (replay error) if they replay against this code.
    // Only remove the old branch after confirming zero running instances on DefaultVersion.
    workflow.GetVersion(ctx, "ChangePaymentStep", VersionV2, VersionV2)
    return workflow.ExecuteActivity(ctx, NewActivity).Get(ctx, nil)
}
```

---

## 3. Activity 设计与幂等性

Activity 可能执行多次。必须保证幂等性。

### 模式：使用 Upsert 替代 Insert

不要简单使用 `INSERT`，改用 `UPSERT` 或带幂等键（如 `WorkflowID` 或 `RunID`）的"先检查再操作"模式。

```go
func (a *Activities) ProcessPayment(ctx context.Context, req PaymentRequest) error {
    info := activity.GetInfo(ctx)
    // Use info.WorkflowExecution.ID as part of your idempotency key in DB
    return a.db.UpsertPayment(req, info.WorkflowExecution.ID)
}
```

---

## 4. 规模化 Worker 配置

### 优化的 Worker 选项

```go
w := worker.New(c, "task-queue", worker.Options{
    MaxConcurrentActivityExecutionSize:      100, // Limit based on resource constraints
    MaxConcurrentWorkflowTaskExecutionSize:  50,
    WorkerActivitiesPerSecond:               200, // Rate limit for this worker cluster
    WorkerStopTimeout:                       time.Minute, // Allow activities to finish
})
```

---

## 5. Context 与心跳

### 传播元数据

使用 `Workflow Interceptor` 或自定义 `Header` 传播，在调用链中传递追踪 ID 或用户身份。

### Activity 心跳

长时间运行的 Activity 必须使用心跳，在 `StartToCloseTimeout` 到期前检测 Worker 崩溃。

```go
func LongRunningActivity(ctx context.Context) error {
    for i := 0; i < 100; i++ {
        activity.RecordHeartbeat(ctx, i) // Report progress

        select {
        case <-ctx.Done():
            return ctx.Err() // Handle cancellation
        default:
            // Do work
        }
    }
    return nil
}
```

---

## 6. 拦截器与可观测性

### 自定义 Workflow 拦截器

使用拦截器注入结构化日志（Zap/Slog）或执行全局错误分类。拦截器必须通过根 `WorkerInterceptor` 接入，Temporal 会为每个工作流任务实例化。

```go
// Step 1: Implement the root WorkerInterceptor (registered on worker.Options)
type MyWorkerInterceptor struct {
    interceptor.WorkerInterceptorBase
}

func (w *MyWorkerInterceptor) InterceptWorkflow(
    ctx workflow.Context,
    next interceptor.WorkflowInboundInterceptor,
) interceptor.WorkflowInboundInterceptor {
    return &myWorkflowInboundInterceptor{next: next}
}

// Step 2: Implement the per-workflow inbound interceptor
type myWorkflowInboundInterceptor struct {
    interceptor.WorkflowInboundInterceptorBase
    next interceptor.WorkflowInboundInterceptor
}

func (i *myWorkflowInboundInterceptor) ExecuteWorkflow(
    ctx workflow.Context,
    input *interceptor.ExecuteWorkflowInput,
) (interface{}, error) {
    workflow.GetLogger(ctx).Info("Workflow started", "type", workflow.GetInfo(ctx).WorkflowType.Name)
    result, err := i.next.ExecuteWorkflow(ctx, input)
    if err != nil {
        workflow.GetLogger(ctx).Error("Workflow failed", "error", err)
    }
    return result, err
}

// Step 3: Register on the worker
w := worker.New(c, "task-queue", worker.Options{
    Interceptors: []interceptor.WorkerInterceptor{&MyWorkerInterceptor{}},
})
```

---

## 需要避免的反模式

1.  **巨型工作流**：单个工作流中保留过多状态。事件历史超过 50K 事件时使用 `ContinueAsNew`。
2.  **臃肿 Activity**：在 Activity 内做编排。Activity 应该是单一工作单元。
3.  **全局变量**：在工作流中使用全局变量。Worker 重启后不会保留。
4.  **工作流中的原生并发**：使用 `go` 协程、`mutexes` 或 `channels` 会导致竞态条件和重放时的确定性错误。

---

## 7. SideEffect 与 MutableSideEffect

需要在工作流中捕获**单次非确定性值**并在重放时一致回放时使用 `workflow.SideEffect`——例如生成 UUID 或读取一次性配置快照。

```go
// SideEffect: called only on first execution; result is recorded in history and
// replayed deterministically on all subsequent replays.
// Requires: "go.temporal.io/sdk/workflow"
encodedID := workflow.SideEffect(ctx, func(ctx workflow.Context) interface{} {
    return uuid.NewString()
})

var requestID string
if err := encodedID.Get(&requestID); err != nil {
    return err
}
```

**何时使用 `MutableSideEffect`**：值可能在工作流任务间变化，但仍需按历史事件确定性回放时（例如工作流运行期间更新的功能标志）。

```go
// MutableSideEffect: re-evaluated on each workflow task, but only recorded in
// history when the value changes from the previous recorded value.
encodedFlag := workflow.MutableSideEffect(ctx, "feature-flag-v2",
    func(ctx workflow.Context) interface{} {
        return featureFlagEnabled // read from workflow-local state, NOT an external call
    },
    func(a, b interface{}) bool { return a.(bool) == b.(bool) },
)
var enabled bool
encodedFlag.Get(&enabled)
```

> **警告**：不要用 `SideEffect` 作为在工作流内调用外部 API（HTTP、DB）的变通方案。所有外部 I/O 仍必须通过 Activity 处理。
