---
name: before-you-build
description: "在编码前审查产品风险，检查需求、替代方案、渠道、迁移成本和失败信号。触发词：构建前、需求验证、产品风险、迁移成本、发布前检查、可行性评估。"
category: product
risk: safe
source: community
source_repo: bin1874/before-you-build-skill
source_type: community
date_added: "2026-07-02"
author: bin1874
tags: [product-validation, planning, ai-coding, risk-review]
tools: [claude, cursor, codex, gemini, antigravity]
license: "MIT"
license_source: "https://github.com/bin1874/before-you-build-skill/blob/main/LICENSE"
---

# 构建之前

## 概述

构建之前帮助 AI 编码工作流在实施之前暂停一下，检查这个功能、产品或工具是否值得构建。它聚焦于产品风险而非代码结构：谁需要这个东西、他们现在用什么、为什么会切换、分发机制如何运作、以及什么样的证据会让项目启动更安全。

上游项目发布了一个独立的技能仓库，并提供了适用于多个编码助手的 `npx` 安装器。

## 何时使用此技能

- 当用户要求 AI 编码助手构建新应用、功能、内部工具、SaaS 或副业项目时使用。
- 当想法听起来合理，但买家、工作流、分发路径或切换原因仍模糊不清时使用。
- 在编写代码之前使用，以便助手能将请求转化为更清晰的假设、风险检查和验证步骤。

## 工作机制

### 步骤 1：识别关键押注

用一句具体的话复述这个产品或功能。指出目标用户、他们要完成的任务、以及当前的替代方案或竞争对手。

### 步骤 2：检查主要风险

从需求、工作流适配度、切换意愿、分发、定价、数据访问和运营负担等维度审查想法。优先提出具体的疑问，而不是泛泛的头脑风暴。

### 步骤 3：决定下一步最小测试

在实施之前建议最小且有用的验证步骤。这可能是买家对话、着陆页测试、手动代运营工作流、原型、候补名单、付费试点或小范围内部试验。

### 步骤 4：继续或停止

如果风险可接受，将假设写下来后进入实施。如果风险较高或证据薄弱，则推荐一个更小的实验，而不是构建完整版本。

## 示例

### 示例 1：SaaS 功能请求

```text
User: Build a dashboard for AI trend monitoring.

Before coding, check:
- Which role needs this dashboard every week?
- What source do they use today?
- What decision changes because of the dashboard?
- Would they pay for alerts, reports, or workflow integration?
- What is the smallest manual report that proves repeat use?
```

### 示例 2：内部工具

```text
User: Build an internal CRM for our small team.

Before coding, check:
- What breaks in the current spreadsheet or existing CRM?
- How many people will use it daily?
- What data must be imported or kept in sync?
- What process change is required after launch?
- Can a no-code workflow prove the need first?
```

## 最佳实践

- ✅ 在实施之前询问用户、任务、当前替代方案和切换原因。
- ✅ 将产品风险与工程风险分开，避免团队很好地解决了错误的问题。
- ✅ 当想法的需求证据薄弱时，推荐小规模的验证步骤。
- ✅ 让产品名称、数字和声明都基于用户提供的内容。
- ❌ 不要用通用清单来证明一个想法已经过验证。
- ❌ 不要编造市场规模、收入、竞争对手吸引力或买家引语。

## 局限性

- 本技能不能替代客户调研、法律审查、财务建议或领域专家审查。
- 它本身无法证明需求；但能帮助助手暴露假设并选择更小的验证步骤。
- 如果用户已经拥有强证据和明确规格，则保持审查简短并进入实施。

## 安全注意事项

- 本技能作为规划层运行是安全的，因为它不需要凭证、外部网络访问或文件变更。
- 如果与安装器或仓库拉取配合使用，请只从你信任的上游仓库或 npm 包安装。

## 常见陷阱

- **问题：** 助手重复产品宣传话术，而不是挑战假设。
  **解决方案：** 在编写代码之前询问当前替代方案、切换触发因素和验证步骤。

- **问题：** 审查过于宽泛，阻碍进展。
  **解决方案：** 挑出风险最大的假设，只先测试这一个。

- **问题：** 即使只是一个小型内部工作流，也被当作创业项目对待。
  **解决方案：** 让风险审查与项目规模相匹配，只问会改变构建决策的问题。

## 相关技能

- `@saas-mvp-launcher` - 当从验证阶段进入 MVP 规划和发布执行时使用。
- `@ux-research-methodology` - 当下一步需要结构化的用户研究时使用。