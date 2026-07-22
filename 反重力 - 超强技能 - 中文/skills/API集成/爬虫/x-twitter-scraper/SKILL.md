---
name: x-twitter-scraper
description: "X (Twitter) 数据平台技能 — 推文搜索、用户查询、粉丝抓取、互动数据、抽奖活动、账号监控、Webhook、19 种抓取工具、MCP 服务器。触发词：X 数据、抓取 Twitter、X 平台、推文搜索、用户资料、粉丝提取、互动指标、抽奖抽取、账号监控、Webhook、MCP。"
category: data
risk: safe
source: community
tags: "[twitter, x-api, scraping, mcp, social-media, data-extraction, giveaway, monitoring, webhooks]"
date_added: "2026-02-28"
---

# X (Twitter) 抓取器 — Xquik

## 概述

通过 Xquik 平台让你的 AI 智能体全面访问 X (Twitter) 数据。涵盖推文搜索、用户资料、粉丝抓取、互动数据、抽奖活动、账号监控、Webhook 以及 19 种批量抓取工具 —— 全部通过 REST API 或 MCP 服务器完成。

## 何时使用此技能

- 用户需要按关键词、话题标签或用户搜索 X/Twitter 上的推文
- 用户想要查询某个用户资料（简介、粉丝数等）
- 用户需要某条推文的互动数据（点赞、转发、阅读量）
- 用户想要检查一个账号是否关注了另一个账号
- 用户需要批量抓取粉丝、回复、转发、引用或社区成员
- 用户想要从推文回复中抽取抽奖活动的中奖者
- 用户需要对 X 账号进行实时监控（新推文、粉丝变化）
- 用户希望通过 Webhook 投递被监控的事件
- 用户询问 X 上的热门话题

## 安装

### 安装技能

```bash
npx skills add Xquik-dev/x-twitter-scraper
```

或者手动克隆到智能体的技能目录：

```bash
# Claude Code
git clone https://github.com/Xquik-dev/x-twitter-scraper.git .claude/skills/x-twitter-scraper

# Cursor / Codex / Gemini CLI / Copilot
git clone https://github.com/Xquik-dev/x-twitter-scraper.git .agents/skills/x-twitter-scraper
```

### 获取 API 密钥

1. 在 [xquik.com](https://xquik.com) 注册账号
2. 在控制台生成一个 API 密钥
3. 设为环境变量或直接传入

```bash
export XQUIK_API_KEY="xq_YOUR_KEY_HERE"
```

## 能力

| 能力 | 说明 |
|---|---|
| 推文搜索 | 按关键词、话题标签、from:用户、"精确短语"查找推文 |
| 用户查询 | 资料信息、简介、粉丝/关注数 |
| 推文查询 | 完整数据 —— 点赞、转发、回复、引用、阅读量、书签 |
| 关注检查 | 检查 A 是否关注 B（双向） |
| 热门话题 | 按地区查看头部趋势（免费，无配额限制） |
| 账号监控 | 跟踪新推文、回复、转发、引用、粉丝变化 |
| Webhook | 通过 HMAC 签名将事件实时投递到你的端点 |
| 抽奖抽取 | 从带过滤条件的推文回复中随机抽取中奖者 |
| 19 种抓取工具 | 粉丝、关注、认证粉丝、提及、帖子、回复、转发、引用、串文、文章、社区、列表、Spaces、人物搜索 |
| MCP 服务器 | 为 AI 原生集成提供 StreamableHTTP 端点 |

## 示例

**搜索推文：**
```
"Search X for tweets about 'claude code' from the last week"
```

**查询用户：**
```
"Who is @elonmusk? Show me their profile and follower count"
```

**查看互动数据：**
```
"How many likes and retweets does this tweet have? https://x.com/..."
```

**运行抽奖：**
```
"Pick 3 random winners from the replies to this tweet"
```

**监控账号：**
```
"Monitor @openai for new tweets and notify me via webhook"
```

**批量抓取：**
```
"Extract all followers of @anthropic"
```

## API 参考

| 端点 | 方法 | 用途 |
|----------|--------|---------|
| `/x/tweets/{id}` | GET | 单条推文及完整数据 |
| `/x/tweets/search` | GET | 搜索推文 |
| `/x/users/{username}` | GET | 用户资料 |
| `/x/followers/check` | GET | 关注关系 |
| `/trends` | GET | 热门话题 |
| `/monitors` | POST | 创建监控 |
| `/events` | GET | 拉取被监控的事件 |
| `/webhooks` | POST | 注册 Webhook |
| `/draws` | POST | 运行抽奖 |
| `/extractions` | POST | 启动批量抓取 |
| `/extractions/estimate` | POST | 估算抓取成本 |
| `/account` | GET | 账号与用量信息 |

**Base URL:** `https://xquik.com/api/v1`
**Auth:** `x-api-key: xq_...` header
**MCP:** `https://xquik.com/mcp` (StreamableHTTP, same API key)

## 仓库

https://github.com/Xquik-dev/x-twitter-scraper

**维护方：** [Xquik](https://xquik.com)

## 限制
- 仅当任务明确符合上述范围时才使用此技能。
- 不要把本技能的输出当作特定环境下的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
