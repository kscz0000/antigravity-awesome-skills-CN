---
name: recallmax
description: "免费 — AI 智能体的神级长上下文记忆。注入 50 万至 100 万纯净 token，自动摘要并保留语气/意图，将 14 轮对话历史压缩为 800 token。当用户提到长上下文记忆、agent记忆、RAG注入、对话压缩、上下文窗口扩展、记忆增强、长对话处理时使用。"
category: memory
risk: safe
source: community
date_added: "2026-03-13"
author: christopherlhammer11-ai
tags: [memory, context, rag, summarization, compression, long-context, agent-infrastructure]
tools: [claude, cursor, codex, gemini, copilot, windsurf, antigravity, grok]
---

# RecallMax — 神级长上下文记忆

## 概述

RecallMax 大幅增强 AI 智能体的记忆能力。可注入 50 万至 100 万纯净 token 的外部上下文，且不会产生幻觉漂移。自动摘要对话内容，同时保留语气、讽刺意味和意图。将多轮对话历史压缩为高密度 token 序列。

永久免费。由 Genesis Agent Marketplace 构建。

## 安装

```bash
npx skills add christopherlhammer11-ai/recallmax
```

## 何时使用此技能

- 当你的智能体在长对话（50 轮以上）中丢失上下文时使用
- 当需要向智能体上下文注入大型 RAG/外部文档时使用
- 当需要压缩对话历史且不丢失语义时使用
- 当需要核查长对话中的论断时使用
- 适用于任何需要记住一切的智能体

## 工作原理

### 第一步：上下文注入

RecallMax 将外部上下文（文档、RAG 结果、历史对话）干净地注入智能体的工作记忆。与简单的拼接不同，它会：
- 对重叠内容去重
- 保留来源归属
- 防止上下文污染导致的幻觉漂移

### 第二步：自适应摘要

随着对话增长，RecallMax 自动摘要较早的对话轮次，同时保留：
- **语气** — 讽刺、正式、紧迫感
- **意图** — 用户真正想要的 vs 用户所说的
- **关键事实** — 数字、名称、决策、承诺
- **情绪基调** — 挫败、兴奋、困惑

### 第三步：历史压缩

将 14 轮对话历史压缩为约 800 个高密度 token，保留完整语义。压缩后的输出可在需要时重新展开。

### 第四步：事实核查

内置交叉引用检查，针对对话上下文中有争议或模糊的论断。标记矛盾之处和缺乏依据的断言。

## 最佳实践

- ✅ 在长时间运行的智能体会话开始时使用 RecallMax
- ✅ 对超过 20 轮的对话启用自动摘要
- ✅ 在触及上下文窗口限制前使用压缩
- ✅ 对高风险输出运行事实核查器
- ❌ 不要在未去重的情况下注入未审查的外部内容
- ❌ 不要跳过摘要而依赖原始截断

## 相关技能

- `@tool-use-guardian` - 工具调用可靠性包装器（同样来自 Genesis Marketplace，免费）

## 链接

- **仓库：** https://github.com/christopherlhammer11-ai/recallmax
- **市场：** https://genesis-node-api.vercel.app
- **浏览技能：** https://genesis-marketplace.vercel.app

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
