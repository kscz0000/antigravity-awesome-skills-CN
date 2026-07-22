---
name: ddd-strategic-design
description: "为复杂业务领域设计 DDD 战略制品，包括子域、限界上下文和通用语言。"
risk: safe
source: self
tags: "[ddd, strategic-design, bounded-context, ubiquitous-language]"
date_added: "2026-02-27"
---

# DDD 战略设计

## 使用此技能的场景

- 定义核心、支撑和通用子域。
- 按领域边界拆分单体或服务版图。
- 将团队和所有权与限界上下文对齐。
- 与领域专家共同构建共享的通用语言。

## 不适用场景

- 领域模型已稳定且边界清晰。
- 仅需要战术代码模式。
- 任务纯粹是基础设施或 UI 导向的。

## 指令

1. 提取领域能力并分类子域。
2. 围绕一致性和所有权定义限界上下文。
3. 建立通用语言术语表和反术语。
4. 在实现前用 ADR 记录上下文边界。

如需详细模板，打开 `references/strategic-design-template.md`。

## 必需制品

- 子域分类表
- 限界上下文目录
- 规范术语表
- 边界决策及其理由

## 示例

```text
使用 @ddd-strategic-design 将我们的电商领域映射到限界上下文，
分类子域，并提议团队所有权。
```

## 局限性

- 此技能不产生可执行代码。
- 没有利益相关者输入时无法推断业务真相。
- 实现前应先进行战术设计。
