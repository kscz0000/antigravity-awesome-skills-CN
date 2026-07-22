---
name: socialclaw
description: "智能体优先的社交媒体发布技能 — 通过单一工作区 API 密钥，跨 13 个平台（X、LinkedIn、Instagram、Facebook Pages、TikTok、Discord、Telegram、YouTube、Reddit、WordPress、Pinterest）排期和发布帖子。"
category: marketing
risk: critical
source: community
source_repo: ndesv21/socialclaw
source_type: community
date_added: "2026-05-25"
author: ndesv21
tags: [social-media, publishing, scheduling, marketing, twitter, linkedin, instagram, tiktok, discord, telegram, reddit, wordpress, pinterest]
tools: [claude]
license: "MIT"
license_source: "https://github.com/ndesv21/socialclaw/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# SocialClaw

## 概述

SocialClaw 是一款智能体优先的社交媒体发布技能，让你使用单一工作区 API 密钥即可跨 13 个平台排期和发布帖子。无需逐个平台配置 OAuth — 一个密钥覆盖全部。

## 何时使用

- 当用户想要跨多个平台规划、排期或发布社交媒体活动时使用。
- 当用户拥有 SocialClaw 工作区 API 密钥，并希望用一套工作流同时管理 X、LinkedIn、Instagram、Facebook、TikTok、Discord、Telegram、YouTube、Reddit、WordPress 或 Pinterest 时使用。
- 当用户需要社交媒体发布自动化，能够验证排期、附加媒体并获取帖子表现指标时使用。

## 支持的平台

- X (Twitter)
- LinkedIn（个人主页 + 企业主页）
- Instagram（商业账号 + 独立账号）
- Facebook Pages
- TikTok
- Discord
- Telegram
- YouTube
- Reddit
- WordPress
- Pinterest

## 安装

```bash
npx skills add ndesv21/socialclaw
```

或直接安装 npm 包：

```bash
npm install socialclaw@0.1.12
```

## 配置

设置你的工作区 API 密钥：

```bash
export SOCIALCLAW_API_KEY=your_workspace_api_key
```

在 [getsocialclaw.com](https://getsocialclaw.com) 获取你的 API 密钥。

## 工作流

### 步骤 1：创建活动

定义你的活动，包括目标平台、内容和排期。

### 步骤 2：上传媒体（可选）

上传图片或视频以附加到帖子。

### 步骤 3：验证排期

确认满足各平台特定的时间规则（如频率限制、发布窗口）。

### 步骤 4：发布或排期

立即发布或排期到未来时间，跨所有已选平台同步执行。

### 步骤 5：数据分析

发布后获取帖子表现指标。

## 使用示例

```
/social-publishing

为我们的产品发布创建活动：
- 平台：X、LinkedIn、Instagram
- 内容："Excited to announce our new feature! Check it out at example.com #launch #product"
- 排期：明天上午 9 点 PST
```

## 来源

GitHub: [ndesv21/socialclaw](https://github.com/ndesv21/socialclaw)
网站: [getsocialclaw.com](https://getsocialclaw.com)

## 限制

- 需要有效的 SocialClaw 工作区 API 密钥；在用户提供明确凭据前不得尝试发布。
- 将每次发布、排期、删除或账号变更操作均视为状态变更：先展示目标平台、内容、媒体和时间，然后等待用户明确确认后再调用服务。
- 平台可用性、频率限制、分析字段和排期行为取决于上游 SocialClaw 服务。
- 本技能描述的是发布工作流；不替代发布前各平台所需的合规审核、品牌审查或法律审批。
