---
name: ask-matt
description: 询问哪种技能或流程适合你的情况。本仓库用户调用技能的路由器。触发词：ask-matt、路由、技能选择、流程选择、ask-matt 路由器
disable-model-invocation: true
category: "productivity"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - productivity
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 询问 Matt

## 使用时机

当本工作流匹配用户请求时使用：询问哪种技能或流程适合你的情况。本仓库用户调用技能的路由器。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

你无法记住每项技能，所以请询问。

**流程（flow）** 是贯穿技能的一条路径。大多数路径沿一条**主流（main flow）**运行，并有两条**引道（on-ramps）**汇入其中。其余皆为独立项。

## 主流：创意 → 上线

大部分工作所走的路线。你有一个想法，并希望将其落地。

1. **`/grill-with-docs`** —— 通过问答打磨创意。当你**已有代码库**时从此处开始：它是有状态的，会把所学内容保存在 `CONTEXT.md` 与 ADR 中。（没有代码库？请用 `/grill-me` —— 见"独立项"。）
2. **分支 —— 能否在对话中敲定所有问题？** 若某问题需要可运行的答案（状态、业务逻辑、需要看到的 UI），通过原型绕道走，并由 **`/handoff`** 在两个方向衔接（见"跨会话"）：
   - **`/handoff`** 出栈，然后针对该文件开启一个新会话，
   - **`/prototype`** 用一次性代码回答该问题，
   - **`/handoff`** 把所学内容回传，并在原始创意讨论中引用它。
3. **分支 —— 这是多会话构建吗？**
   - **是** → **`/to-prd`**（将讨论转化为 PRD）→ **`/to-issues`**（将 PRD 拆分为可独立领取的工单）。由于工单相互独立，**请在每个工单之间清理上下文**：每个工单都开启一个新会话，并通过把 PRD 与单个工单一起传给 **`/implement`** 来启动它。
   - **否** → 在此处直接 **`/implement`**，保持在同一上下文窗口中。

### 上下文卫生

将步骤 1–3 保持在**一个不间断的上下文窗口中** —— 在 `/to-issues` 之前不要压缩或清理 —— 这样问答、PRD 与工单都能建立在同一思路之上。之后的每个 `/implement` 都从工单出发重新开始。

此做法的限制是 **[智能区（smart zone）](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**：模型仍能清晰推理的窗口（在最先进的模型上约 12 万 token）。若某个会话在到达 `/to-issues` 之前就已逼近该上限，不要在退化状态下硬撑 —— 请使用 `/handoff` 并在新线程中继续。

## 引道

产生工作并最终汇入主流的起始情形。

- **问题与需求堆积** → **`/triage`**。它将工单在分诊角色中流转，并产出可直接交给智能体的工单，随后由 **`/implement`** 接手。

  分诊仅适用于**非你创建的**工单 —— bug 报告、新收到的功能需求，任何以原始形态到来的东西。`/to-issues` 所产出的工单已经具备可直接交给智能体的形态，因此**不要对它们进行分诊**。

## 代码库健康

非特性工作 —— 是日常维护。

- **`/improve-codebase-architecture`** —— 在你有空时随时运行，让代码库始终适合智能体在其中工作。它会浮现可深化的机会；挑一个就能_生成一个创意_，然后带入主流的 `/grill-with-docs`。

## 跨会话

- **`/handoff`** —— 当线程已满或需要分叉（例如进入 `/prototype` 会话）时，它会把对话压缩为 Markdown 文件。你不在原地继续 —— 而是**开启一个新会话并引用该文件**来跨上下文衔接。它是上下文窗口之间的桥梁，方向任意。当你想要**新会话**但需要**保留当前对话**时使用。
- **`/compact`**（内置） —— 留在**同一对话**中，让前序轮次被总结。在**阶段之间的刻意停顿点**使用，且你能接受丢失逐字历史时。不要在阶段进行中压缩 —— 智能体可能迷失方向。`/handoff` 是分叉；`/compact` 是延续。

## 独立项

完全脱离主流。

- **`/grill-me`** —— 与 `/grill-with-docs` 相同的不留情面的问答，但适用于**没有代码库**的情形。无状态：不保存任何本地内容，不生成 `CONTEXT.md`。当你需要打磨任何不在仓库中的计划或设计时使用它。
- **`/teach`** —— 在多个会话中学习某个概念，使用当前目录作为有状态工作区。
- **`/writing-great-skills`** —— 编写与编辑技能时的参考资料。

## 前置条件

**`/setup-matt-pocock-skills`** —— 在你首次工程流之前运行，用于配置其他技能所假定的问题跟踪器、分诊标签与文档布局。自定义问题跟踪器亦可。


## 局限性

- 当工作流指定上游工具、账号、API 密钥或本地设置时，依赖这些前提。
- 未经用户明确同意，不会授权执行破坏性、生产级、付费或对外发送消息的操作。
- 在将生成的产物或建议视为最终结论之前，请结合用户的真实来源进行核验。