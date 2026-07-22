---
name: rich-elicitation
description: "在开始模糊任务前进行多轮澄清提问。当2个以上任务维度各有3种以上可行答案时触发。触发词：澄清提问、多轮追问、消歧、需求澄清、模糊任务、elicitation、clarifying questions、ambiguity resolution"
category: productivity
risk: none
source: self
source_type: self
date_added: "2026-05-07"
author: abubakar
tags: [elicitation, clarifying-questions, ambiguity, multi-round, prompt-engineering]
tools: [antigravity]
---

# 深度澄清技能

## 概述

本技能规定 Antigravity 在开始工作之前如何解决任务模糊性。当用户请求中有太多未回答的维度——每个维度都有多种合理答案时——Antigravity 会通过多轮有针对性的澄清提问来消除歧义，而非静默选择默认值。

目标是产出正确的初稿，而非需要三轮修订的泛泛回答。轮次上限为三轮；第三轮后仍不清晰的内容会标注为假定前提，然后 Antigravity 继续执行。

---

## 何时使用本技能

- 当请求有 2 个或以上模糊维度，且每个维度有 3 种以上可行选项时使用
- 当用户可能在范围、受众、语气、格式或策略上的意图不清晰时使用
- 当早期回答会显著改变输出的结构或方向时使用
- 当从事范围开放的写作、规划、设计、推荐或创意任务时使用
- 当第一轮回答解锁了一组新的有意义选择、需要在继续前解决时使用

以下情况**不**触发：
- 简单的事实查询或数学计算
- 范围明确、只有单一明显解读的请求
- 存在安全默认值的次要未知项

---

## 工作原理

### 步骤 1：运行触发检查清单

在开始任何任务之前，心理上检查以下各项有多少适用：

| 信号 | 行动 |
|---|---|
| 存在多种有效输出格式 | 询问格式 |
| 受众未知 | 询问受众 |
| 语气模糊 | 询问语气 |
| 范围可能窄也可能广 | 询问深度/篇幅 |
| 技术性 vs 简明性处理不明确 | 询问技术级别 |
| 存在多种策略方向 | 询问方向 |
| 用户约束未知 | 询问约束 |

**如果 2 行以上适用 → 触发本技能。**

### 步骤 2：提出第一轮问题

使用 `ask_user_input_v0` 最多提出 3 个问题。将相关问题归入同一次调用。以 1-2 句话开头解释为什么提问。为每个问题标记一个选项为**(推荐)**。

### 步骤 3：重新运行检查清单

第一轮回答后，对仍未解决的部分重新运行检查清单。如果仍有 2 行以上适用，运行第二轮。否则继续执行。

### 步骤 4：运行后续轮次（如需要）

| 轮次 | 目的 | 最多问题数 |
|---|---|---|
| 第一轮 | 阻塞性问题 — 塑造整个输出 | 3 |
| 第二轮 | 由第一轮回答解锁的追问 | 3 |
| 第三轮 | 最终细节 — 谨慎使用 | 2 |

轮次之间自然过渡。不要机械地宣布"第二轮"。使用如下措辞：
> "明白了——很有帮助。开始前还有一件事："

### 步骤 5：继续执行

第三轮之后（或更早，如果已有足够上下文），简要陈述任何剩余假定前提，然后开始任务。

---

## 示例

### 示例 1：多轮 — 投资人路演文稿

**用户：** "帮我为我的项目做一个演示文稿。"

**第一轮** — 三个阻塞性问题：

```
Framing: "This could go a lot of different ways. Quick questions before I start:"

Q1: Who is the audience?
  - Internal team / colleagues
  - External clients or partners
  - Investors or stakeholders (Recommended)
  - General / public audience

Q2: What's the primary goal?
  - Inform and update
  - Persuade and drive a decision (Recommended)
  - Teach or explain a concept
  - Pitch and raise funding

Q3: How much content do you already have?
  - Starting from scratch
  - Rough notes or an outline (Recommended)
  - Full draft — just needs polish
  - Previous version to update
```

*用户回答：投资人 | 融资 | 粗略笔记 → 需要第二轮。*

**第二轮** — 由第一轮解锁：

```
Framing: "Perfect — investor pitch it is. A couple more things:"

Q1: What stage is this raise?
  - Pre-seed / idea stage
  - Seed round (Recommended)
  - Series A or later
  - Strategic partnership / grant

Q2: How long should the deck be?
  - Short and punchy, 8–10 slides (Recommended)
  - Standard, 12–15 slides
  - Comprehensive, 20+ slides
```

*无需第三轮 — 继续执行。*

---

### 示例 2：单轮 — 商务邮件

**用户：** "写一封商务邮件跟进提案。"

**仅第一轮：**

```
Framing: "Two quick questions to nail the tone:"

Q1: What tone should this email strike?
  - Formal and professional (Recommended)
  - Friendly but direct
  - Urgent and firm
  - Warm and relationship-focused

Q2: What's the primary goal?
  - Request action / get a response (Recommended)
  - Share information only
  - Repair or maintain the relationship
  - Negotiate or push back
```

*上下文已足够。无需第二轮。*

---

## 最佳实践

- ✅ 始终为每个问题标记一个选项为**(推荐)**
- ✅ 在问题组件之前用 1-2 句话做铺垫说明
- ✅ 将最多 3 个相关问题归入同一次 `ask_user_input_v0` 调用
- ✅ 每轮后重新评估 — 一旦有足够上下文就停止
- ✅ 互斥选择使用 `single_select`，组合有效时使用 `multi_select`
- ✅ 第三轮结束后，在继续执行前明确陈述剩余假定前提
- ❌ 不要用 6 次独立问题调用，而 2 次分组调用就能解决
- ❌ 不要在同一个问题中标记两个选项为推荐
- ❌ 不要使用"其他"或"看情况"等模糊选项标签而不加说明
- ❌ 不要在 UI 中机械地标注轮次（"第一轮："、"第二轮："）
- ❌ 不要为有安全默认值的次要细节运行后续轮次

---

## 局限性

- 本技能不验证用户答案是否内部一致 — 它按原样信任用户回答。
- 轮次结构是指导原则，而非刚性契约；何时停止需要判断。
- 与 `ask_user_input_v0` 配合效果最佳 — 在没有该工具的环境中，问题质量可能下降。
- 不处理模糊性只能通过获取外部信息来解决的场景（例如读取用户未上传的文件）。
- 不适用于任何提问开销都不可接受的实时或高延迟敏感工作流。

---

## 安全说明

本技能纯属推理 — 不发出 shell 命令、不读取文件、不发起网络请求、不修改任何状态。风险等级为 `none`。

本技能无需 `npm run security:docs` 审查。

---

## 常见陷阱

- **问题：** Antigravity 问了一个好问题，得到回答后就继续了，没有检查是否出现了新的未知项。
  **解决方案：** 每轮之后始终在心理上重新运行触发检查清单，再决定是否继续。

- **问题：** 问题中的所有选项看起来同样有效，所以 Antigravity 没有标记任何推荐。
  **解决方案：** 选择对大多数用户有效或风险最低的选项并标记。"无偏好"极少成立。

- **问题：** Antigravity 运行了 4 轮以上，试图消除每一个未知项。
  **解决方案：** 硬性上限 3 轮。第三轮后陈述假定前提并继续。

- **问题：** 第二轮问题覆盖了与第一轮相同的类别（例如再次问语气）。
  **解决方案：** 每轮应解锁新维度，而非重新询问已解决的维度。

---

## 相关技能

- `@ask-user-questions` — 带推荐选项的单轮澄清。简单任务使用该技能；当早期回答会打开新的有意义选择时使用深度澄清。
