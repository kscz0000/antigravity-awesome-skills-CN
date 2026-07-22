---
name: uxui-principles
description: "依据 168 条经过研究验证的 UX/UI 原则评估界面，检测反模式，并在 AI 编码会话中注入 UX 上下文。触发词：UX 评估、UI 原则、反模式检测、AI 界面审查、用户体验审计、界面气味。"
category: design
risk: safe
source: community
date_added: "2026-04-03"
author: uxuiprinciples
tags: [ux, ui, design, evaluation, principles, antipatterns, accessibility]
tools: [claude, cursor, windsurf]
---

# UX/UI 原则

包含 5 个智能体技能，用于依据 168 条经过研究验证的 UX/UI 原则评估界面、检测反模式，并在 AI 辅助设计与编码会话中注入 UX 上下文。

**来源：** https://github.com/uxuiprinciples/agent-skills

## 技能列表

| 技能 | 用途 |
|-------|---------|
| `uxui-evaluator` | 依据 168 条经过研究验证的原则评估界面描述 |
| `interface-auditor` | 使用 uxuiprinciples 气味分类法检测 UX 反模式 |
| `ai-interface-reviewer` | 依据 44 条 AI 时代 UX 原则审计 AI 驱动的界面 |
| `flow-checker` | 依据决策、错误与反馈原则检查用户流程 |
| `vibe-coding-advisor` | 在 vibe coding 会话的实施前注入 UX 上下文 |

## 适用场景
- 审计现有界面以发现 UX 问题
- 检查 UI 是否遵循经过研究验证的最佳实践
- 在设计中检测反模式与 UX 气味
- 审查 AI 驱动界面的信任度、透明度与安全性
- 在实施前或实施过程中获取 UX 指导

## 工作原理

1. 从集合中安装任意技能
2. 描述你希望评估的界面、屏幕或流程
3. 该技能依据相关原则进行评估，并返回包含严重程度级别与修复步骤的结构化发现
4. 可选择连接 uxuiprinciples.com API，以获取包含完整引用的富化输出

## 安装

```
npx skills add uxuiprinciples/agent-skills
```

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为针对特定环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
