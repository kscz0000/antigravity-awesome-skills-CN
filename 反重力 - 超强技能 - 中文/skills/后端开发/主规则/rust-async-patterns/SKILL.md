---
name: rust-async-patterns
description: "掌握 Rust 异步编程，包括 Tokio、async trait、错误处理和并发模式。适用于构建异步 Rust 应用、实现并发系统或调试异步代码。触发词：Rust async、Tokio、异步编程、async trait、并发模式、异步错误处理、异步调试"
risk: safe
source: community
date_added: "2026-02-27"
---

# Rust 异步编程模式

基于 Tokio 运行时的 Rust 异步编程生产级模式，涵盖任务、通道、流和错误处理。

## 适用场景

- 构建异步 Rust 应用
- 实现并发网络服务
- 使用 Tokio 进行异步 I/O
- 正确处理异步错误
- 调试异步代码问题
- 优化异步性能

## 不适用场景

- 任务与 Rust 异步模式无关
- 需要超出此范围的其他领域或工具

## 使用说明

- 明确目标、约束和必要的输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，请查阅 `resources/implementation-playbook.md`

## 资源

- `resources/implementation-playbook.md` 包含详细模式和示例

## 局限性

- 仅在任务明确匹配上述范围时使用此技能
- 输出不能替代针对特定环境的验证、测试或专家评审
- 缺少必要输入、权限、安全边界或成功标准时，应停止并请求澄清