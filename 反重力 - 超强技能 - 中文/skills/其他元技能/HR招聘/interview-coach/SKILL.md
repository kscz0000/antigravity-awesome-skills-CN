---
name: interview-coach
description: "全流程求职辅导系统 — JD 解码、简历优化、故事库、模拟面试、面试记录分析、薪资谈判。23 个命令，持久化状态。触发词：面试辅导、求职教练、模拟面试、面试准备、薪资谈判、storybank"
category: productivity
risk: safe
source: community
date_added: "2026-03-11"
author: dbhat93
tags: [interview, job-search, coaching, career, storybank, negotiation]
tools: [claude]
---

# Interview Coach

## 概述

一套持久化、自适应的全流程求职辅导系统。不是题库——而是一套有态度的系统，追踪你的回答模式，给你的答案打分，用得越多越精准。状态通过 `coaching_state.md` 跨会话持久保存，随时从上次中断处继续。

## 安装

```bash
npx skills add dbhat93/job-search-os
```

然后输入 `/coach` → `kickoff`。

## 何时使用此技能

- 开始求职时，需要一套结构化系统
- 为特定面试做准备时（公司调研、模拟、热身）
- 想分析过往面试记录时
- 谈 offer 或应对猎头薪资筛选时
- 构建或维护面试故事库时

## 覆盖范围

- **JD 解码** — 六维分析、匹配判定、向猎头提问的问题清单
- **简历 + LinkedIn** — ATS 审计、要点改写、平台原生优化
- **模拟面试** — 行为面、系统设计、案例面、小组面、技术面等多种形式
- **面试记录分析** — 粘贴 Otter/Zoom/Grain 的原始记录，自动识别格式
- **故事库** — STAR 故事含核心洞察、检索训练、组合优化
- **薪资 + 谈判** — offer 前话术准备、offer 分析、精确谈判脚本
- **共 23 个命令**，覆盖完整求职流程

## 示例

### 示例 1：启动求职

```
/coach
kickoff
```

教练会索要你的简历、目标岗位和时间线——然后构建你的档案，并给出优先级行动计划。

### 示例 2：为特定公司做准备

```
/coach
prep Stripe Senior PM
```

运行公司调研，生成针对该岗位的准备简报，并按 Stripe 的面试流程定制模拟面试题。

### 示例 3：分析面试记录

```
/coach
analyze
```

粘贴来自 Otter、Zoom 或任何工具的原始记录。教练自动识别格式，从五个维度给每个回答打分，并针对你的薄弱环节生成专项训练计划。

### 示例 4：应对薪资问题

```
/coach
salary
```

辅导你应对猎头筛选时"你的薪资期望是多少？"的关键时刻，给出有依据的薪资范围和精确话术。

## 来源

https://github.com/dbhat93/job-search-os

## 限制

- 仅当任务明确匹配上述范围时使用此技能
- 输出不能替代针对具体环境的验证、测试或专家评审
- 若缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
