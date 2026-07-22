---
name: bats-testing-patterns
description: "掌握 Bash 自动化测试系统（Bats），用于全面的 Shell 脚本测试。当用户要求'编写 Shell 脚本测试'、'Bats 测试'、'Shell 脚本 TDD'、'CI/CD 中的 Shell 自动化测试'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Bats 测试模式

使用 Bats（Bash 自动化测试系统）为 Shell 脚本编写全面单元测试的完整指南，包括测试模式、夹具和生产级 Shell 测试最佳实践。

## 使用此技能的场景

- 为 Shell 脚本编写单元测试
- 为脚本实现 TDD
- 在 CI/CD 流水线中设置自动化测试
- 测试边界情况和错误条件
- 跨 Shell 环境验证行为

## 不使用此技能的场景

- 项目不使用 Shell 脚本
- 需要超出 Shell 行为范围的集成测试
- 目标仅是代码检查或格式化

## 指令

- 确认 Shell 方言和支持的环境。
- 建立包含辅助函数和夹具的测试结构。
- 编写针对退出码、输出和副作用的测试。
- 添加 setup/teardown 并在 CI 中运行测试。
- 如需详细示例，打开 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 提供详细模式和示例。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
