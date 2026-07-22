---
name: ax-extract-workflow
description: "基于本地 ax 的会话/提交/技能/工具追踪，重构某个历史编码智能体产物背后的工作流。当被问及'X 是怎么构建出来的'时使用。触发词：工作流重构、会话溯源、产物还原、ax 重放"
category: development
risk: safe
source: community
source_repo: Necmttn/ax
source_type: community
date_added: "2026-06-21"
author: Necmttn
tags: [ai-coding, workflow-reconstruction, session-analysis, observability]
tools: [claude, cursor, gemini, codex-cli]
license: "AGPL-3.0-only"
license_source: "https://github.com/Necmttn/ax/blob/main/LICENSE"
---

# ax 工作流提取

## 概述

使用本技能可以还原某个历史编码智能体产物背后的工作流：已发布的功能、PR、演示、重构、报告或其他具体成果。它借助本地的 `ax` 图谱，把提交、会话、轮次、技能和工具追踪串联成一段简短的"它是怎么做出来的"叙述。

`ax` 必须安装、可在 `PATH` 中找到，并且能访问其本地数据库。若 ax 连不上数据库，请如实上报连接失败并停止，不要凭记忆猜测。

## 何时使用本技能

- 当用户问出"我们是怎么把 X 做出来的？"、"X 为何能跑通？"或"把这份产物背后的工作流提取出来"时使用。
- 当锚点是提交 SHA、日期、功能名、PR、会话或仓库本地产物时使用。
- 当用户想要梳理导致最终结果的智能体技能、提示词、命令、决策与校验的先后顺序时使用。
- 不要用于笼统的活动回顾；那种情况请用常规的会话列表。

## 工作机制

### 步骤一：定位锚点

从用户的请求中找出最合适的锚点：

- 提交 SHA：直接使用。
- 日期或日期区间：检查该日期前后的会话。
- 主题、功能或产物名称：用 recall 搜索相关的轮次、提交和技能。
- "这个仓库最近"：列出当前仓库最近的会话。

```bash
ax recall "live ingest dashboard" --sources=turn,commit,skill --scope=here
ax sessions near abc1234 --json
ax sessions around 2026-06-15 --days=3 --json
ax sessions here --days=14
```

这些命令都是只读检视命令。

### 步骤二：挑选相关会话

挑出最有可能解释该产物的少数会话。优先选择那些：提到该产物、触碰过相关文件、包含相关提交，或其中出现的技能和工具调用与该项工作的动作吻合。

若多个候选都讲得通，把这些候选展示给用户，请他指定要看哪一个。

### 步骤三：检视会话轨迹

打开每个选定的会话，留意以下要点：

- 用到了哪些技能，以及调用顺序
- 用户的引导点与被明确下来的约束
- 改变了工作走向的文件、测试与命令
- 产生关键证据的子智能体或工具追踪
- 在判定完成之前所做的校验步骤

```bash
ax sessions show <session-id> --json
ax sessions show <session-id> --by-role
ax recall "specific keyword from the artifact" --sources=turn,commit --scope=here
```

### 步骤四：撰写重构文档

除非用户明确要求落盘，否则把结果以行内方式返回。叙述要简短、立足证据：

1. 锚点：你最终定到的日期、提交、功能或产物。
2. 有序工作流：4-8 步，列出每一步所用技能或动作，以及产生的产物。
3. 关键决策：那些改变路径的用户或智能体选择。
4. 校验环节：测试、评审、检查或人工证据。
5. 复现简报：用于再次完成类似工作的浓缩配方。

如果有条件，尽量用会话 ID、提交 SHA、文件路径作为引用。

## 示例

### 从一次提交重构功能

```bash
ax sessions near 8f31c2a --json
ax sessions show <session-id> --by-role
ax sessions show <session-id> --json
```

输出形态：

```text
Anchor: 8f31c2a, live ingest dashboard

Workflow:
1. Problem framing -> narrowed the failure to stale dashboard polling.
2. Session recall -> found the earlier ingest-stream design and constraints.
3. Implementation -> wired the server event bus and browser subscription.
4. Verification -> ran typecheck and refreshed the dashboard locally.

Reproducer brief:
Start from the failing artifact, find nearby sessions, inspect role-grouped
skills, then summarize the smallest ordered path from framing to verification.
```

### 围绕某个日期重构工作

```bash
ax sessions around 2026-06-15 --days=2 --json
ax recall "otel receiver" --sources=turn,commit,skill --scope=here
```

适用于用户记得工作发生的时间、但不记得提交号的场景。

## 最佳实践

- 优先选用最具体的锚点：SHA 优于日期，日期优于模糊主题。
- 把 ax 视为唯一信源，不得编造缺失的技能、花费、命令或决策。
- 引用要克制；只有在用户决策或命令对重构至关重要时才引用。
- 私密对话细节保持私密，使用概括而非整段日志。
- 把"实际发生了什么"与"下次要复现什么"分开陈述。

## 局限性

- 需要本机已正确安装 ax 且能访问其本地数据库。
- 只能看到 ax 已摄入的会话、提交、技能和工具追踪。
- 当智能体服务方省略工具输出、花费或推理数据时，会话数据可能不完整。
- 它重构的是工作流，而不是正确性；做工程决策时仍需检查代码并运行项目校验。

## 安全与注意事项

- 不得上传私有对话、会话日志、提示词、工具输出或本地数据库导出。
- 撰写概要时要脱敏：密钥、令牌、客户数据、文件内容以及私有对话文本。
- 除非用户明确要求执行单独的维护动作，否则一律使用只读的 ax 检视命令。
- 不要在重构过程中执行改写 `.ax/`、重建索引、发布报告或改动仓库的命令。

## 相关技能

- `@agenttrace-session-audit` - 用于本地智能体会话的健康度、花费、延迟与工具失败审计。
- `@domain-modeling` - 当重构暴露了应当沉淀下来的术语或架构决策时使用。
- `@planning-with-files` - 当用户希望把重构得到的配方转成一份带追踪笔记的新计划时使用。
