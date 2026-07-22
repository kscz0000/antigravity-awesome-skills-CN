---
name: ddd-context-mapping
description: "使用 DDD 上下文映射模式映射限界上下文之间的关系并定义集成契约。"
risk: safe
source: self
tags: "[ddd, context-map, anti-corruption-layer, integration]"
date_added: "2026-02-27"
---

# DDD Context Mapping

## 使用此技能的场景

- 定义限界上下文之间的集成模式
- 防止领域逻辑跨服务边界泄漏
- 在迁移过程中规划防腐层（Anti-Corruption Layer）
- 明确上下游所有权和契约责任

## 不使用此技能的场景

- 单一上下文系统，无集成需求
- 仅需内部类设计
- 正在选择云基础设施工具

## 指导步骤

1. 列出所有上下文对及其依赖方向
2. 为每对上下文选择关系模式
3. 定义转换规则和所有权边界
4. 添加失败模式、降级行为和版本策略

如需详细的映射结构，请参考 `references/context-map-patterns.md`。

## 输出要求

- 所有上下文对的关系映射图
- 契约所有权矩阵
- 转换和防腐层决策
- 已知耦合风险及缓解方案

## 示例

```text
使用 @ddd-context-mapping 定义 Checkout 如何与 Billing、Inventory 和 Fraud 上下文集成，包括 ACL 和契约所有权。
```

## 局限性

- 此技能不替代 API 级别的 Schema 设计
- 无法单独保证组织层面的对齐
- 团队所有权变更时应重新审视
