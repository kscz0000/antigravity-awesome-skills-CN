---
name: projection-patterns
description: "从事件流构建读模型和投影。适用于实现 CQRS 读侧、构建物化视图或优化事件溯源系统的查询性能。触发词：projection, 投影, CQRS, 读模型, 物化视图, 事件溯源, event sourcing, read model, materialized view"
risk: safe
source: community
date_added: "2026-02-27"
---

# 投影模式

构建事件溯源系统的投影和读模型的完整指南。

## 使用场景

- 构建 CQRS 读模型
- 从事件创建物化视图
- 优化查询性能
- 实现实时仪表板
- 从事件构建搜索索引
- 跨流聚合数据

## 不适用场景

- 任务与投影模式无关
- 需要超出此范围的其他领域或工具

## 指引

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请查看 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 包含详细模式和示例。

## 限制

- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家评审。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。