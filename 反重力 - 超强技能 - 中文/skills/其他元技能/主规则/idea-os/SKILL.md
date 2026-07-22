---
name: idea-os
description: "五阶段流水线（分流 → 澄清 → 研究 → PRD → 计划），将原始创意转化为四个关联文件：澄清问题、深度研究、包含非目标和指标的 PRD，以及带有 mermaid 用户旅程和终止标准的分阶段执行计划。触发词：创意验证、产品规划、PRD生成、想法落地、从创意到计划、产品操作系统、idea validation、product planning、turn idea into plan、build-ready plan、raw idea to PRD。"
category: product-management
risk: safe
source: community
source_repo: Slashworks-biz/idea-os
source_type: community
date_added: "2026-04-18"
author: Slashworks-biz
tags: [product-management, prd, market-research, mvp, idea-validation, jtbd, swot, competitor-analysis, founder, non-technical]
tools: [claude, cursor, gemini]
license: "MIT"
license_source: "https://github.com/Slashworks-biz/idea-os/blob/main/LICENSE"
---

# idea-os

将原始创意转化为可执行构建计划的操作系统。接收一个粗略的问题陈述，产出四个文件：澄清问题、深度研究、PRD，以及包含平台/技术栈选择、用户旅程图和终止标准的分阶段执行计划。

## 概述

idea-os 是一个 5 阶段顺序流水线，每个阶段的输出都作为下一阶段的输入——研究塑造 PRD，PRD 塑造计划，计划的终止标准回溯到研究洞察。与单命令 PRD 生成器不同，idea-os 在研究完成前拒绝编写 PRD，在 PRD 稳定前拒绝编写计划。深度和词汇量根据双轴分类（复杂度 × 构建者成熟度）自适应调整，确保首次构建者不会淹没在术语中，而创始人获得完整严谨性。

来源：https://github.com/Slashworks-biz/idea-os — 完整技能、11 个参考文件、4 个资产模板，以及 590 行完整示例。

## 何时使用

- 当用户分享原始产品创意或问题陈述，需要从澄清问题到深度研究、PRD 和分阶段执行计划的结构化流水线时使用。
- 当用户说"我有个想法……"、"帮我构建 X"、"验证并规划这个概念"或"我该构建什么？"——并且需要可推进的文件，而非一次性答案时使用。
- 当非技术创始人、产品经理或爱好者需要结构化方法来弥合"创意"与"周一早上的构建队列"之间的鸿沟时使用。
- **不要**用于对半成型创意的快速合理性检查反馈（改用 `idea-refine`）或编辑现有 PRD（改用 `product-management`）。

## 工作原理

### 阶段 1 — 分流

在任何操作之前，先在两个轴上对创意进行分类。研究/PRD/计划的深度和问题数量随复杂度缩放；词汇量随成熟度缩放。

- **创意层级 (T1/T2/T3)** — T1 = 周末工具，T2 = SaaS MVP 或 AI 封装器，T3 = 市场 / B2B SaaS / 受监管行业。
- **成熟度 (S1/S2/S3)** — S1 = 非技术，不使用框架名称；S2 = 爱好者，引入框架并附带定义；S3 = 创始人/资深 PM，完整词汇。

在继续之前，用一行陈述分类（例如"T2 · S2 — 中等复杂度 SaaS，构建者有发布经验"）。

### 阶段 2 — 澄清

编写 `questions.md`，包含 4–18 个问题（数量随复杂度缩放），分组为：谁和痛点 · 范围和切入点 · 约束和目标。每个问题必须可执行——答案必须能改变你构建的内容。拒绝通用问题。

编写后，停止并等待回答。在回答或声明自主模式假设之前，不要进入研究阶段。

### 阶段 3 — 研究

使用 WebSearch + WebFetch 编写 `research.md`。最低要求：5 次 WebSearch，2 次对命名竞争对手的 WebFetch，每个 TAM 数字 1 个来源，每个来源标注日期。未标注来源的内容标记 `[assumption]`。

必需章节：问题验证、JTBD、市场（TAM/SAM/SOM 自上而下 + 自下而上）、竞争对手（直接/间接/替代品 + 定位图）、SWOT、分销（前 100 用户渠道匹配）、风险，以及 3–7 个非显而易见的洞察。

### 阶段 4 — PRD

编写 `PRD.md`，包含：可证伪的问题陈述、命名用户画像、排序的 JTBD、非目标（强制——这是糟糕 PRD 的死因）、领先和滞后指标。

### 阶段 5 — 计划

编写 `plan.md`，包含：用户旅程（文本 + mermaid）、与研究发现关联的平台推荐、保守/现代/前沿矩阵中的技术栈、分阶段构建（MVP → v1 → 目标）及每阶段终止标准和前 100 用户分销策略、每阶段指标，以及 3–5 个立即行动项。

## 局限性

- 为获得最佳结果，阶段之间需要用户输入；如果答案缺失，输出依赖于显式假设。
- 产出规划产物（`questions.md`、`research.md`、`PRD.md`、`plan.md`），但不执行构建或部署工作。
- 来源质量决定输出质量；薄弱或过时的参考会降低推荐准确性。
- 更适合新创意验证和早期规划，而非已发布产品的后期优化。

## 示例

### 示例 1：非技术创始人的消费者应用创意

用户："我想为 ADHD 人群构建一个习惯追踪器。"

idea-os 分类为 T2 · S1，编写 8 个通俗易懂的澄清问题，运行包含竞品定价和 ADHD 子版块社区信号的研究，产出包含 ADHD 特定非目标（无连续打卡、无惩罚机制）的 PRD，以及包含单屏 MVP 和关联 14 天留存的终止标准的计划。

### 示例 2：创始人的 B2B SaaS 创意

用户："我在考虑为中型制造商开发采购软件。"

idea-os 分类为 T3 · S3，编写 18 个包含采购周期细节的问题，运行包含 Wardley 图选项和波特五力的研究，产出包含分层用户画像（购买者/审批者/IT）的 PRD，以及包含关联付费试点成交率的阶段 1 终止标准的计划。

## 完整源码

完整 11 参考技能、4 资产模板、完整示例和 MIT 许可证位于 https://github.com/Slashworks-biz/idea-os。本 antigravity 条目为参考副本——上游仓库是持续开发所在地。
