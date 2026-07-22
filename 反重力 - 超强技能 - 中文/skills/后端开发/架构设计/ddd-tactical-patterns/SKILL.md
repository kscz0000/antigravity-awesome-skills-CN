---
name: ddd-tactical-patterns
description: "在代码中应用 DDD 战术模式，使用实体、值对象、聚合、仓储和领域事件，并明确不变量。"
risk: safe
source: self
tags: "[ddd, tactical, aggregates, value-objects, domain-events]"
date_added: "2026-02-27"
---

# DDD 战术模式

## 使用此技能的场景

- 将领域规则转化为代码结构。
- 设计聚合边界和不变量。
- 将贫血模型重构为行为丰富的领域对象。
- 定义仓储契约和领域事件边界。

## 不适用场景

- 你仍在定义战略边界。
- 任务仅涉及 API 文档或 UI 布局。
- 完整的 DDD 复杂性不合理。

## 指导原则

1. 首先识别不变量，并围绕它们设计聚合。
2. 为已验证的概念建模不可变值对象。
3. 将领域行为保留在领域对象中，而非控制器。
4. 为有意义的状态转换发出领域事件。
5. 将仓储保持在聚合根边界。

如需详细检查清单，请打开 `references/tactical-checklist.md`。

## 示例

```typescript
class Order {
  private status: "draft" | "submitted" = "draft";

  submit(itemsCount: number): void {
    if (itemsCount === 0) throw new Error("订单不能为空提交");
    if (this.status !== "draft") throw new Error("订单已提交");
    this.status = "submitted";
  }
}
```

## 局限性

- 本技能不定义部署架构。
- 不选择数据库或传输协议。
- 应与测试模式配合使用以确保不变量覆盖。
