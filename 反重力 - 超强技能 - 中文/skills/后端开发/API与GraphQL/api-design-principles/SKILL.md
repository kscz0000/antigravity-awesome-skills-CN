---
name: api-design-principles
description: "掌握 REST 和 GraphQL API 设计原则，构建直观、可扩展、可维护的 API。触发词：API设计、REST API、GraphQL、接口设计、API规范、API命名、HTTP状态码、分页、API版本、速率限制、接口分页、错误响应格式、API过滤、API排序。"
risk: safe
source: community
date_added: "2026-02-27"
---

# API 设计原则

掌握 REST 和 GraphQL API 设计原则，构建直观、可扩展、可维护的 API，让开发者愉悦使用并经受时间考验。

## 使用此技能的时机

- 设计新的 REST 或 GraphQL API
- 重构现有 API 以提升可用性
- 为团队建立 API 设计标准
- 在实现前审查 API 规范
- 在 API 范式之间迁移（REST 到 GraphQL 等）
- 创建开发者友好的 API 文档
- 针对特定用例优化 API（移动端、第三方集成）

## 不使用此技能的时机

- 仅需要特定框架的实现指导
- 正在进行仅涉及基础设施的工作，无需 API 契约
- 无法更改或版本化公共接口

## 操作说明

1. 定义消费者、用例和约束条件。
2. 选择 API 风格并建模资源或类型。
3. 指定错误处理、版本控制、分页和认证策略。
4. 用示例验证并审查一致性。

详细模式、检查清单和模板请参考 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 包含详细的模式、检查清单和模板。

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代特定环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
