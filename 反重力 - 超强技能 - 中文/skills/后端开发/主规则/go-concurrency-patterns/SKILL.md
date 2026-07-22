---
name: go-concurrency-patterns
description: "掌握 Go 并发编程，涵盖 goroutine、channel、sync 原语和 context。当用户要求'Go 并发模式'、'goroutine'、'channel 通信'、'worker pool'、'调试竞态条件'或'优雅关闭'时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Go 并发模式

Go 并发的生产级模式，涵盖 goroutine、channel、同步原语和 context 管理。

## 使用场景

- 构建并发 Go 应用
- 实现 worker pool 和管道
- 管理 goroutine 生命周期
- 使用 channel 进行通信
- 调试竞态条件
- 实现优雅关闭

## 不适用场景

- 任务与 Go 并发模式无关
- 需要此范围之外的其他领域或工具

## 指令

- 明确目标、约束和必需的输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 资源

- `resources/implementation-playbook.md` 提供详细模式和示例

## 限制

- 仅在任务明确匹配上述范围时使用此技能
- 输出不能替代环境特定的验证、测试或专家审查
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清
