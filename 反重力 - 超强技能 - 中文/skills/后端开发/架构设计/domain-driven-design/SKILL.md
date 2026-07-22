---
name: domain-driven-design
description: "从战略建模到战术实现和事件驱动架构模式，规划并路由领域驱动设计工作。"
risk: safe
source: self
tags: "[ddd, domain, bounded-context, architecture]"
date_added: "2026-02-27"
---

# 领域驱动设计

## 使用此技能的场景

- 需要为复杂业务领域建模，并明确边界。
- 想要判断完整的 DDD 是否值得增加的复杂度。
- 需要将战略设计决策与实现模式关联起来。
- 正在基于领域需求规划 CQRS、事件溯源、Saga 或投影。

## 不使用此技能的场景

- 问题只是简单的 CRUD，业务复杂度低。
- 只需要局部的 bug 修复。
- 无法获取领域知识，也没有代理产品专家。

## 指令

1. 在投入完整 DDD 之前，先运行可行性检查。
2. 优先产出战略产物：子领域、Bounded Context、语言术语表。
3. 根据当前任务路由到专门技能。
4. 为每个阶段定义成功标准和证据。

### 可行性检查

仅当以下条件至少满足两条时，才使用完整 DDD：

- 业务规则复杂或变化频繁。
- 多个团队导致模型冲突。
- 集成契约不稳定。
- 可审计性和显式不变量至关重要。

### 路由映射

- 战略模型和边界：`@ddd-strategic-design`
- 跨上下文集成和转换：`@ddd-context-mapping`
- 战术代码建模：`@ddd-tactical-patterns`
- 读写分离：`@cqrs-implementation`
- 事件历史作为事实来源：`@event-sourcing-architect` 和 `@event-store-design`
- 长时间运行的工作流：`@saga-orchestration`
- 读模型：`@projection-patterns`
- 决策日志：`@architecture-decision-records`

如需模板，打开 `references/ddd-deliverables.md`。

## 输出要求

始终返回：

- 范围和假设
- 当前阶段（战略、战术或事件驱动）
- 已产出的显式产物
- 未解决风险和下一步建议

## 示例

```text
使用 @domain-driven-design 评估这个计费平台是否应该采用完整 DDD。
然后路由到正确的下一步技能，并列出本周必须产出的产物。
```

## 局限性

- 此技能不能替代与领域专家的直接工作坊。
- 它不提供框架特定的代码生成。
- 不应将其作为过度工程化简单系统的理由。
