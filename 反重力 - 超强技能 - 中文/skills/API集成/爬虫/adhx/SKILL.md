---
name: adhx
description: "将任意 X/Twitter 帖子获取为干净的 LLM 友好 JSON 格式。将 x.com、twitter.com 或 adhx.com 链接转换为结构化数据，包含完整文章内容、作者信息和互动指标。无需爬虫或浏览器。触发词：X 帖子、Twitter 帖子、推特帖子、获取推文、分析推文、X 链接、Twitter 链接、推文内容、X 文章、长推文。"
risk: safe
source: community
date_added: "2026-03-25"
---

# ADHX - X/Twitter 帖子读取器

使用 ADHX API 将任意 X/Twitter 帖子获取为结构化 JSON 格式进行分析。

## 概述

ADHX 提供免费 API，可返回任意 X 帖子的干净 JSON 数据，包括完整的长文文章内容。对于 LLM 消费而言，这远优于爬虫或基于浏览器的方法。支持普通推文和完整的 X 文章。

## 何时使用此技能

- 当用户分享 X/Twitter 链接并想要阅读、分析或总结帖子时使用
- 当你需要从 X/Twitter 帖子获取结构化数据（作者、互动、内容）时使用
- 当处理需要提取完整内容的长篇 X 文章时使用

## API 端点

```
https://adhx.com/api/share/tweet/{username}/{statusId}
```

## URL 格式

从以下任意 URL 格式中提取 `username` 和 `statusId`：

| 格式 | 示例 |
|--------|---------|
| `x.com/{user}/status/{id}` | `https://x.com/dgt10011/status/2020167690560647464` |
| `twitter.com/{user}/status/{id}` | `https://twitter.com/dgt10011/status/2020167690560647464` |
| `adhx.com/{user}/status/{id}` | `https://adhx.com/dgt10011/status/2020167690560647464` |

## 工作流程

当用户分享 X/Twitter 链接时：

1. **解析 URL** 从路径段中提取 `username` 和 `statusId`
2. **获取 JSON** 使用 curl：
```bash
curl -s "https://adhx.com/api/share/tweet/{username}/{statusId}"
```
3. **使用结构化响应** 回答用户的问题（总结、分析、提取要点等）

## 响应结构

```json
{
  "id": "statusId",
  "url": "original x.com URL",
  "text": "short-form tweet text (empty if article post)",
  "author": {
    "name": "Display Name",
    "username": "handle",
    "avatarUrl": "profile image URL"
  },
  "createdAt": "timestamp",
  "engagement": {
    "replies": 0,
    "retweets": 0,
    "likes": 0,
    "views": 0
  },
  "article": {
    "title": "Article title (for long-form posts)",
    "previewText": "First ~200 chars",
    "coverImageUrl": "hero image URL",
    "content": "Full markdown content with images"
  }
}
```

## 安装

### 方式 A：Claude Code 插件市场（推荐）
```
/plugin marketplace add itsmemeworks/adhx
```

### 方式 B：手动安装
```bash
curl -sL https://raw.githubusercontent.com/itsmemeworks/adhx/main/skills/adhx/SKILL.md -o ~/.claude/skills/adhx/SKILL.md
```

## 示例

### 示例 1：总结推文

用户："总结这个帖子 https://x.com/dgt10011/status/2020167690560647464"

```bash
curl -s "https://adhx.com/api/share/tweet/dgt10011/2020167690560647464"
```

然后使用返回的 JSON 提供总结。

### 示例 2：分析互动数据

用户："这条推文有多少点赞？https://x.com/handle/status/123"

1. 解析 URL：username = `handle`，statusId = `123`
2. 获取：`curl -s "https://adhx.com/api/share/tweet/handle/123"`
3. 从响应中返回 `engagement.likes` 值

## 最佳实践

- 在调用 API 之前，始终解析完整 URL 以提取 username 和 statusId
- 当用户需要完整内容（不仅仅是推文文本）时，检查 `article` 字段
- 当用户询问点赞、转发或浏览量时，使用 `engagement` 字段
- 不要尝试直接爬取 x.com —— 使用此 API 替代

## 注意事项

- 无需身份验证
- 同时支持短推文和长篇 X 文章
- 对于 X 内容，始终优先使用此方法而非基于浏览器的爬取
- 如果 API 返回错误或空响应，请告知用户该帖子可能不可用

## 其他资源

- [ADHX GitHub 仓库](https://github.com/itsmemeworks/adhx)
- [ADHX 网站](https://adhx.com)

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
