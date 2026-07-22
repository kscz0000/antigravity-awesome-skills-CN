---
name: swift-concurrency-expert
description: 审查和修复 Swift 并发问题，如 actor 隔离和 Sendable 违规。触发词：Swift并发、actor隔离、Sendable、@MainActor、async迁移、并发安全、数据竞争、Swift Concurrency
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# Swift 并发专家

## 概述

在 Swift 6.2+ 代码库中审查和修复 Swift 并发问题，通过应用 actor 隔离、Sendable 安全和现代并发模式，以最小的行为变更确保数据竞争安全。

## 何时使用
- 当用户要求审查 Swift 并发用法或修复编译器诊断信息时。
- 当你需要关于 actor 隔离、`Sendable`、`@MainActor` 或 async 迁移的指导时。

## 工作流程

### 1. 分诊问题

- 捕获确切的编译器诊断信息和有问题的符号。
- 检查项目并发设置：Swift 语言版本（6.2+）、严格并发级别，以及是否启用了平易近人的并发模式（默认 actor 隔离 / 默认主 actor）。
- 识别当前的 actor 上下文（`@MainActor`、`actor`、`nonisolated`）以及是否启用了默认 actor 隔离模式。
- 确认代码是否绑定 UI 还是预期在主 actor 之外运行。

### 2. 应用最小安全修复

优先选择保留现有行为同时满足数据竞争安全的编辑。

常见修复：
- **绑定 UI 的类型**：用 `@MainActor` 标注类型或相关成员。
- **主 actor 类型上的协议一致性**：使一致性成为隔离一致性（例如 `extension Foo: @MainActor SomeProtocol`）。
- **全局/静态状态**：用 `@MainActor` 保护或移入 actor。
- **后台工作**：将耗时工作移到 `nonisolated` 类型上的 `@concurrent` 异步函数，或使用 `actor` 保护可变状态。
- **Sendable 错误**：优先使用不可变/值类型；仅在正确时添加 `Sendable` 一致性；除非能证明线程安全，否则避免使用 `@unchecked Sendable`。

### 3. 验证修复

- 重新构建并确认所有并发诊断已解决，没有引入新警告。
- 运行测试套件检查回归——并发更改即使在构建干净时也可能引入微妙的运行时问题。
- 如果修复暴露了新警告，将每个警告视为新的分诊（返回步骤 1），迭代解决直到构建干净且测试通过。

### 示例

**绑定 UI 的类型 — 添加 `@MainActor`**

```swift
// 修复前：数据竞争警告，因为 ViewModel 从主线程访问
// 但没有 actor 隔离
class ViewModel: ObservableObject {
    @Published var title: String = ""
    func load() { title = "Loaded" }
}

// 修复后：标注整个类型，使所有存储状态和方法
// 自动隔离到主 actor
@MainActor
class ViewModel: ObservableObject {
    @Published var title: String = ""
    func load() { title = "Loaded" }
}
```

**协议一致性隔离**

```swift
// 修复前：编译器错误 — SomeProtocol 方法是非隔离的，但
// 遵循类型是 @MainActor
@MainActor
class Foo: SomeProtocol {
    func protocolMethod() { /* 访问主 actor 状态 */ }
}

// 修复后：将一致性限定为 @MainActor，使需求
// 在正确的隔离上下文中得到满足
@MainActor
extension Foo: SomeProtocol {
    func protocolMethod() { /* 安全访问主 actor 状态 */ }
}
```

**使用 `@concurrent` 的后台工作**

```swift
// 修复前：耗时计算阻塞主 actor
@MainActor
func processData(_ input: [Int]) -> [Int] {
    input.map { heavyTransform($0) }   // 在主线程运行
}

// 修复后：跳离主 actor 执行耗时工作，然后返回结果
// 调用方 await 结果并留在自己的 actor 上
nonisolated func processData(_ input: [Int]) async -> [Int] {
    await Task.detached(priority: .userInitiated) {
        input.map { heavyTransform($0) }
    }.value
}

// 或者，使用 @concurrent 异步函数（Swift 6.2+）：
@concurrent
func processData(_ input: [Int]) async -> [Int] {
    input.map { heavyTransform($0) }
}
```

## 参考材料

- 参见 `references/swift-6-2-concurrency.md` 了解 Swift 6.2 变更、模式和示例。
- 参见 `references/approachable-concurrency.md` 了解项目启用平易近人的并发模式时的指导。
- 参见 `references/swiftui-concurrency-tour-wwdc.md` 了解 SwiftUI 特定的并发指导。

## 局限性
- 仅当任务明确匹配上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
