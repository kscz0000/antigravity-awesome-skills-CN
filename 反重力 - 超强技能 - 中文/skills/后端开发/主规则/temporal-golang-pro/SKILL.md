---
name: temporal-golang-pro
description: "用于基于 Temporal Go SDK 构建持久化分布式系统的场景。涵盖确定性工作流规则、mTLS Worker 配置和高级模式。触发词：Temporal、Go SDK、分布式系统、持久化工作流、确定性工作流、mTLS"
risk: safe
source: self
date_added: "2026-02-27"
---

# Temporal Go SDK (temporal-golang-pro)

## 概述

使用 Temporal Go SDK 构建高弹性、可扩展、确定性分布式系统的专家级指南。将模糊的编排需求转化为生产级 Go 实现，聚焦持久化执行、严格确定性和企业级 Worker 配置。

## 适用场景

- **设计分布式系统**：构建需要持久化状态和可靠编排的微服务时。
- **实现复杂工作流**：使用 Go SDK 处理长时间运行的流程（天/月级别）或复杂 Saga 模式。
- **优化性能**：Worker 需要精细并发控制、mTLS 安全或自定义拦截器时。
- **确保可靠性**：实现幂等活动、优雅错误处理和精细化重试策略时。
- **维护与演进**：对运行中的工作流进行版本管理或执行零停机 Worker 更新时。

## 不适用场景

- 使用 Temporal 的其他 SDK（Python、Java、TypeScript）——请参考对应的 `-pro` 技能。
- 简单的请求/响应任务，不需要持久化或协调能力。
- 仅做高层设计不涉及实现（使用 `workflow-orchestration-patterns`）。

## 操作步骤

1.  **收集上下文**：主动询问：
    - 目标 **Temporal 集群**（Cloud 还是自托管）和 **Namespace**。
    - **Task Queue** 名称和预期吞吐量。
    - **安全要求**（mTLS 路径、认证方式）。
    - **故障模式**和期望的重试/超时策略。
2.  **验证确定性**：在建议工作流代码前，对照以下 **5 条规则**验证：
    - 禁止使用原生 Go 并发（goroutines）。
    - 禁止使用原生时间函数（`time.Now`、`time.Sleep`）。
    - 禁止使用非确定性 map 遍历（必须排序键）。
    - 禁止直接进行外部 I/O 或网络调用。
    - 禁止使用非确定性随机数。
3.  **增量实现**：从共享 Protobuf/Data 类开始，然后是 Activities，接着是 Workflows，最后是 Workers。
4.  **善用资源**：实现需要高级模式（Sagas、拦截器、重放测试）时，明确参考实现手册和测试策略。

## 能力范围

### Go SDK 实现

- **Worker 管理**：深入掌握 `worker.Options`，包括 `MaxConcurrentActivityTaskPollers`、`WorkerStopTimeout` 和 `StickyScheduleToStartTimeout`。
- **拦截器**：实现 Client、Worker 和 Workflow 拦截器处理横切关注点（日志、追踪、认证）。
- **自定义数据转换器**：集成 Protobuf、加密载荷或自定义 JSON 序列化。

### 高级工作流模式

- **持久化并发**：使用 `workflow.Go`、`workflow.Channel` 和 `workflow.Selector` 替代原生并发原语。
- **版本管理**：使用 `workflow.GetVersion` 和 `workflow.GetReplaySafeLogger` 实现安全的代码演进。
- **大规模处理**：使用 `ContinueAsNew` 模式管理历史大小限制（默认：50MB 或 50K 事件）。
- **子工作流**：管理生命周期、取消和父子信号传播。

### 测试与可观测性

- **测试套件精通**：使用 `WorkflowTestSuite` 进行单元测试和功能测试，支持确定性时间控制。
- **Mock 策略**：精细化的 Activity 和子工作流 Mock 策略。
- **重放测试**：使用生产事件历史验证代码变更。
- **指标监控**：配置 Prometheus/OpenTelemetry 导出器追踪 Worker 性能。

## 示例

### 示例 1：带版本管理的工作流（确定性）

```go
// Note: imports omitted. Requires 'go.temporal.io/sdk/workflow', 'go.temporal.io/sdk/temporal', and 'time'.
func SubscriptionWorkflow(ctx workflow.Context, userID string) error {
    // 1. Versioning for logic evolution (v1 = DefaultVersion)
    v := workflow.GetVersion(ctx, "billing_logic", workflow.DefaultVersion, 2)

    for i := 0; i < 12; i++ {
        ao := workflow.ActivityOptions{
            StartToCloseTimeout: 5 * time.Minute,
            RetryPolicy: &temporal.RetryPolicy{MaximumAttempts: 3},
        }
        ctx = workflow.WithActivityOptions(ctx, ao)

        // 2. Activity Execution (Always handle errors)
        err := workflow.ExecuteActivity(ctx, ChargePaymentActivity, userID).Get(ctx, nil)
        if err != nil {
            workflow.GetLogger(ctx).Error("Payment failed", "Error", err)
            return err
        }

        // 3. Durable Sleep (Time-skipping safe)
        sleepDuration := 30 * 24 * time.Hour
        if v >= 2 {
            sleepDuration = 28 * 24 * time.Hour
        }

        if err := workflow.Sleep(ctx, sleepDuration); err != nil {
            return err
        }
    }
    return nil
}
```

### 示例 2：完整 mTLS Worker 配置

```go
func RunSecureWorker() error {
    // 1. Load Client Certificate and Key
    cert, err := tls.LoadX509KeyPair("client.pem", "client.key")
    if err != nil {
        return fmt.Errorf("failed to load client keys: %w", err)
    }

    // 2. Load CA Certificate for Server verification (Proper mTLS)
    caPem, err := os.ReadFile("ca.pem")
    if err != nil {
        return fmt.Errorf("failed to read CA cert: %w", err)
    }
    certPool := x509.NewCertPool()
    if !certPool.AppendCertsFromPEM(caPem) {
        return fmt.Errorf("failed to parse CA cert")
    }

    // 3. Dial Cluster with full TLS config
    c, err := client.Dial(client.Options{
        HostPort:  "temporal.example.com:7233",
        Namespace: "production",
        ConnectionOptions: client.ConnectionOptions{
            TLS: &tls.Config{
                Certificates: []tls.Certificate{cert},
                RootCAs:      certPool,
            },
        },
    })
    if err != nil {
        return fmt.Errorf("failed to dial temporal: %w", err)
    }
    defer c.Close()

    w := worker.New(c, "payment-queue", worker.Options{})
    w.RegisterWorkflow(SubscriptionWorkflow)

    if err := w.Run(worker.InterruptCh()); err != nil {
        return fmt.Errorf("worker run failed: %w", err)
    }
    return nil
}
```

### 示例 3：Selector 与 Signal 集成

```go
func ApprovalWorkflow(ctx workflow.Context) (string, error) {
    var approved bool
    signalCh := workflow.GetSignalChannel(ctx, "approval-signal")

    // Use Selector to wait for multiple async events
    s := workflow.NewSelector(ctx)
    s.AddReceive(signalCh, func(c workflow.ReceiveChannel, _ bool) {
        c.Receive(ctx, &approved)
    })

    // Add 72-hour timeout timer
    s.AddReceive(workflow.NewTimer(ctx, 72*time.Hour).GetChannel(), func(c workflow.ReceiveChannel, _ bool) {
        approved = false
    })

    s.Select(ctx)

    if !approved {
        return "rejected", nil
    }
    return "approved", nil
}
```

## 最佳实践

- ✅ **推荐**：始终处理 `ExecuteActivity` 和 `client.Dial` 的错误。
- ✅ **推荐**：使用 `workflow.Go` 和 `workflow.Channel` 实现并发。
- ✅ **推荐**：遍历 map 前对键排序，保持确定性。
- ✅ **推荐**：执行时间超过 1 分钟的 Activity 使用 `activity.RecordHeartbeat`。
- ✅ **推荐**：使用 `replayer.ReplayWorkflowHistoryFromJSON` 测试逻辑兼容性。
- ❌ **禁止**：在生产 Worker 中用 `_` 吞掉错误或使用 `log.Fatal`。
- ❌ **禁止**：在 Workflow 函数内直接进行网络/磁盘 I/O。
- ❌ **禁止**：依赖原生 `time.Now()` 或 `rand.Int()`。
- ❌ **禁止**：将此技能应用于不需要持久化的简单定时任务。

## 故障排查

- **Panic: Determinism Mismatch**：通常由逻辑变更未使用 `workflow.GetVersion` 或非确定性代码（如原生 map）引起。
- **Error: History Size Exceeded**：达到历史大小限制（默认 50K 事件）。确保实现了 `ContinueAsNew`。
- **Worker Hang**：检查 `WorkerStopTimeout` 并确保所有 Activity 处理了 context 取消。

## 局限性

- 不涵盖 Temporal Cloud UI 操作或 TLS 证书配置流程。
- 不涵盖 Temporal Java、Python 或 TypeScript SDK；请参考对应的 `-pro` 技能。
- 假设 Temporal Server v1.20+ 和 Go SDK v1.25+；旧版 SDK 可能有不同的 API。
- 不涵盖实验性 Temporal 功能（如 Nexus、多集群复制）。
- 不涉及全局 Namespace 配置或多区域故障转移设置。
- 不涵盖通过 `worker-versioning` 特性标志进行的 Temporal Worker 版本管理（实验性）。

## 资源

- [实现手册](resources/implementation-playbook.md) - Go SDK 模式深入讲解。
- [测试策略](resources/testing-strategies.md) - Go 的单元测试、重放测试和集成测试。
- [Temporal Go SDK 参考](https://pkg.go.dev/go.temporal.io/sdk)
- [Temporal Go 示例](https://github.com/temporalio/samples-go)

## 相关技能

- `grpc-golang` - 内部传输协议和 Protobuf 设计。
- `golang-pro` - 通用 Go 性能调优和高级语法。
- `workflow-orchestration-patterns` - 语言无关的编排策略。
