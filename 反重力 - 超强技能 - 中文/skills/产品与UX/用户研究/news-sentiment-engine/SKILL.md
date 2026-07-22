---
name: news-sentiment-engine
description: 多源 RSS 新闻聚合，结合 Claude 驱动的情感分析与结构化简报输出。触发词：新闻情感分析、RSS聚合、新闻简报、情感评分、行业简报
category: research
risk: critical
source: community
source_repo: tellmefrankie/news-engine
source_type: community
date_added: "2026-05-13"
author: tellmefrankie
tags: [news, rss, sentiment-analysis, briefing, research]
tools: [claude, websearch]
plugin:
  targets:
    codex: blocked
    claude: blocked
---
# 新闻情感引擎（免费版）

从多个来源采集并分析 AI/科技新闻，使用 Claude 驱动的情感分析。开源精简版。

## 何时使用

- 从多个 RSS 来源准备简洁的 AI 或科技新闻简报时使用。
- 需要带情感标签、行业标签和影响力评分的排序文章摘要时使用。
- 监控产品发布、政策变动和基础设施变化等行业动态时使用。
- 在撰写每日或每周简报前去重重复报道时使用。

## 功能

- 从 4+ 个 RSS 源采集新闻（TechCrunch、The Verge、Ars Technica、Hacker News）
- 跨源去重文章
- 按重要性排序（行业影响、技术趋势、政策变化）
- 生成带情感标签的结构化简报
- 输出格式化的简报卡片

## 用法

```
Collect latest AI/tech news from RSS feeds.
Rank top 5 by importance to the tech industry.
For each: summary (2-3 sentences), sentiment (positive/negative/neutral),
impact score (1-5), industry tags, one-sentence commentary.
Output as a structured briefing card.
```

## 输出示例

```
AI/Tech News Briefing — 2026-05-13

1. OpenAI announces GPT-5 with 2M context window
   Source: TechCrunch | Impact: 5/5
   Tags: #AI #LLM #OpenAI
   Sentiment: Positive

   Summary: OpenAI unveiled GPT-5 with a 2M token context window and
   improved reasoning. Enterprise pricing starts at $0.03/1k tokens.

   Commentary: Direct competitive pressure on Anthropic Claude 3.5.
   Enterprise deals may shift in H2 2026.

2. EU AI Act enforcement begins for high-risk systems
   Source: The Verge | Impact: 4/5
   Tags: #Regulation #EU #Compliance
   Sentiment: Neutral
```

## 输出格式

每篇文章包含：
- 标题 + 来源 + 发布日期
- 摘要（2-3 句）
- 行业标签：[AI、半导体、云计算等]
- 情感：正面/负面/中性
- 影响力评分：1-5
- 评论：1 句行业视角点评

## 安装

下面的可选安装步骤会克隆并运行来自 `tellmefrankie/news-engine` 的第三方 Node 项目。运行前请自行审查并锁定该仓库版本，不要将 API 密钥暴露给未经审查的代码。

```bash
git clone https://github.com/tellmefrankie/news-engine
cd news-engine
pnpm install
cp .env.example .env
# Requires: ANTHROPIC_API_KEY
pnpm dev -- --collect-only
```

免费版无需付费 API，仅需 Anthropic API 密钥。

## 局限性

- RSS 源可能延迟、失效、限流或重复发布联合内容。
- 情感和影响力评分是简报辅助工具，不构成权威市场或政策分析。
- 示例安装运行的是第三方代码，使用前请审查仓库和环境变量。
- 输出内容在用于发布或投资决策前，应与原始文章来源交叉核实。

## 专业版

免费版覆盖新闻采集和基础分析。

**完整套装 — $29 一次性付费**：投资级分析（投资组合影响评分、期权流关联、财报催化剂检测），Telegram 自动推送。
→ https://jaehyunpark.gumroad.com/l/tcyahy

## 作者

核心模块来自一个自 2026 年起每日处理 50+ 篇文章的生产级新闻分析引擎。
