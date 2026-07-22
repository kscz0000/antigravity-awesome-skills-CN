## 平易近人的并发（Swift 6.2）- 项目模式快速指南

当项目已启用 Swift 6.2 平易近人的并发设置（默认 actor 隔离 / 默认主 actor）时，使用此参考。

## 检测模式

在 Xcode 构建设置的 "Swift Compiler - Concurrency" 下检查：
- Swift 语言版本（必须为 6.2+）。
- Default actor isolation / Main Actor by default。
- 严格并发检查级别（Complete/Targeted/Minimal）。

对于 SwiftPM，检查 Package.swift swiftSettings 中的相同标志。

## 预期的行为变化

- 异步函数默认留在调用方的 actor 上；除非实现选择，否则不会跳转到全局并发执行器。
- 默认主 actor 减少了绑定 UI 的代码和全局状态的数据竞争错误，因为可变状态被隐式保护。
- 协议一致性可以隔离（例如 `extension Foo: @MainActor Bar`）。

## 在此模式下如何应用修复

- 优先使用最少标注；当代码绑定 UI 时，让默认主 actor 完成工作。
- 使用隔离一致性而非强制 `nonisolated` 变通方案。
- 除非有明确的性能需求需要卸载，否则将全局或共享可变状态保持在主 actor 上。

## 何时退出或卸载工作

- 在必须在并发池上运行的异步函数上使用 `@concurrent`。
- 仅当类型或成员真正线程安全且在主 actor 之外使用时，才设为 `nonisolated`。
- 当值跨越 actor 或任务边界时，继续遵守 Sendable 边界。

## 常见陷阱

- `Task.detached` 忽略继承的 actor 上下文；除非确实需要打破隔离，否则避免使用。
- 默认主 actor 可能隐藏性能问题——如果 CPU 密集型工作留在主 actor 上；将此类工作移到 `@concurrent` 异步函数中。

## 关键字（来自源速查表）

| 关键字 | 作用 |
| --- | --- |
| `async` | 函数可以暂停 |
| `await` | 在此暂停直到完成 |
| `Task { }` | 启动异步工作，继承上下文 |
| `Task.detached { }` | 启动异步工作，不继承上下文 |
| `@MainActor` | 在主线程运行 |
| `actor` | 具有隔离可变状态的类型 |
| `nonisolated` | 退出 actor 隔离 |
| `Sendable` | 可安全跨隔离域传递 |
| `@concurrent` | 始终在后台运行（Swift 6.2+） |
| `async let` | 启动并行工作 |
| `TaskGroup` | 动态并行工作 |

## 来源

https://fuckingapproachableswiftconcurrency.com/en/
