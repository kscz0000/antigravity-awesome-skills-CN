---
name: ai-dev-jobs-mcp
description: "搜索 8,400+ 个 AI 和 ML 职位，覆盖 489 家公司，查看招聘详情和雇主信息，匹配职位，查看薪资和市场统计数据。触发词：AI职位搜索、机器学习工作、AI招聘、ML工程师职位、远程AI工作、AI就业市场、薪资数据、职位匹配"
category: mcp
risk: safe
source: "https://aidevboard.com"
source_type: community
date_added: "2026-04-16"
author: unitedideas
tags: [mcp, jobs, ai-jobs, ml-jobs, recruiting, job-search, career]
tools: [claude, cursor, gemini]
---

# AI Dev Jobs MCP

## 概述

AI Dev Jobs 是一个远程 MCP 服务器，为 AI 智能体提供 AI 和 ML 职位列表的实时索引访问。截至 2026 年 4 月 17 日，实时 MCP 统计数据显示有 8,405 个活跃职位，覆盖 489 家公司，中位数薪资为 $213,500，本周新增 600 个职位。智能体可以按职位、地点或公司搜索工作，获取完整职位详情，列出招聘公司，将职位与个人资料匹配，以及获取薪资或汇总市场统计数据。该服务专为协助求职搜索、招聘或劳动力市场分析的 AI 智能体而设计。

## 何时使用此技能

- 帮助用户搜索 AI 或 ML 工程职位时使用
- 智能体需要查询哪些公司正在招聘特定 AI 职位时使用
- 构建招聘或人才匹配工作流时使用
- 分析 AI 就业市场（开放职位、头部公司、职位分布）时使用

## MCP 配置

将 AI Dev Jobs MCP 服务器添加到您的客户端配置中。该端点使用可流式 HTTP，无需身份验证。

### Claude Desktop / Cursor / Windsurf

```json
{
  "mcpServers": {
    "ai-dev-jobs": {
      "url": "https://aidevboard.com/mcp"
    }
  }
}
```

无需 API 密钥或身份验证。

## 可用工具

### `search_jobs`

按关键词、地点、公司或工作安排搜索职位索引。返回匹配的职位列表，包含职位名称、公司、地点和薪资信息。

```
search_jobs({ query: "machine learning engineer", location: "remote" })
```

### `get_job`

根据 ID 获取特定职位的完整详情，包括职位描述、要求、薪资范围和申请链接。

```
get_job({ id: "abc123" })
```

### `list_companies`

列出索引中的所有公司及其开放职位数量。用于发现哪些公司正在积极招聘。

```
list_companies({})
```

### `get_company`

获取特定公司的详情，包括端点暴露的可用 AI 职位。

```
get_company({ id: "openai" })
```

### `get_stats`

获取就业市场的汇总统计数据：总职位数、按开放职位排名的头部公司、职位分布和地点分布。

```
get_stats({})
```

### `match_jobs`

根据候选人资料、技能列表或偏好匹配职位。

```
match_jobs({ skills: ["python", "llm", "pytorch"], workplace: "remote" })
```

### `get_salary_data`

获取职位、标签、级别或地点的薪资统计数据（如有）。

```
get_salary_data({ tag: "llm", level: "senior" })
```

### `list_tags`

列出可用于过滤搜索或薪资分析的索引标签。

```
list_tags({})
```

## 示例

### 示例 1：查找远程 ML 职位

```text
Use @ai-dev-jobs-mcp to find remote machine learning engineer positions.
```

智能体将调用 `search_jobs({ query: "machine learning engineer", location: "remote" })` 并返回匹配的职位列表。

### 示例 2：查看哪些公司正在招聘

```text
Use @ai-dev-jobs-mcp to list all companies currently hiring for AI roles.
```

智能体将调用 `list_companies({})` 并返回按开放职位数量排序的公司列表。

### 示例 3：获取就业市场概览

```text
Use @ai-dev-jobs-mcp to show current AI job market statistics.
```

智能体将调用 `get_stats({})` 并返回职位数、头部雇主和职位分布的汇总数据。

### 示例 4：获取完整职位详情

```text
Use @ai-dev-jobs-mcp to get the full details for job ID abc123.
```

智能体将调用 `get_job({ id: "abc123" })` 并返回完整的职位信息，包括要求和申请链接。

### 示例 5：将职位与候选人资料匹配

```text
Use @ai-dev-jobs-mcp to match remote LLM roles to a senior Python and PyTorch profile.
```

智能体将调用 `match_jobs({ skills: ["python", "llm", "pytorch"], workplace: "remote" })` 并返回合适的职位列表。

### 示例 6：比较薪资数据

```text
Use @ai-dev-jobs-mcp to compare senior LLM salary data.
```

智能体将调用 `get_salary_data({ tag: "llm", level: "senior" })` 并汇总可用的薪资范围。

## 最佳实践

- 使用 `search_jobs` 配合特定关键词进行精准搜索，而非宽泛查询
- 使用 `list_companies` 发现公司，然后使用 `search_jobs` 按公司名称过滤进行聚焦搜索
- 使用 `get_stats` 在深入具体职位列表前为用户提供市场背景
- 当用户提供技能、资历、地点或工作安排偏好时，使用 `match_jobs`
- 仅将 `get_salary_data` 作为市场背景；提醒用户职位列表和薪资变化很快
- 结合简历或求职信技能，创建端到端的求职申请工作流

## 限制

- 索引专门覆盖 AI 和 ML 职位；AI 领域之外的通用软件工程职位可能不在收录范围内
- 职位列表定期更新，但新发布的职位可能有短暂延迟才会出现
- 薪资数据仅在公司提供时可用；并非所有职位都包含薪资信息
- 计数和薪资中位数是实时市场数据，在向用户展示前应使用 `get_stats` 刷新

## 相关技能

- `@not-human-search-mcp` - 通过 MCP 发现 AI 就绪的工具和 API
- `@mcp-builder` - 用于构建您自己的 MCP 服务器
