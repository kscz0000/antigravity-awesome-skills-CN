---
name: not-human-search-mcp
description: "搜索 AI 就绪网站、检查已索引站点详情、验证 MCP 端点，并使用 Not Human Search MCP 服务器发现工具和 API。当用户要求搜索 AI 工具、验证 MCP 端点或发现 API 时使用。"
category: mcp
risk: safe
source: "https://nothumansearch.ai"
source_type: community
date_added: "2026-04-16"
author: unitedideas
tags: [mcp, search, ai-discovery, api-discovery, mcp-verification, agent-tools]
tools: [claude, cursor, gemini]
---

# Not Human Search MCP

## 概述

Not Human Search 是一个远程 MCP 服务器，允许 AI 智能体搜索包含 1,750+ 个 AI 就绪网站的精选索引、检查已索引站点详情、提交新站点进行分析，以及通过 JSON-RPC 探测验证活跃的 MCP 端点。它专为需要在运行时发现工具、API 和服务而不依赖硬编码列表的 AI 智能体设计。

## 使用场景

- 当 AI 智能体需要为特定任务发现工具、API 或 MCP 服务器时使用
- 当你想检查网站是否暴露了机器可读端点（llms.txt、OpenAPI、MCP）时使用
- 当验证 MCP 端点是否实际响应 JSON-RPC 时使用
- 当构建需要动态发现和连接外部服务的智能体工作流时使用

## MCP 配置

将 Not Human Search MCP 服务器添加到你的客户端配置中。该端点使用可流式传输的 HTTP，无需认证。

### Claude Desktop / Cursor / Windsurf

```json
{
  "mcpServers": {
    "not-human-search": {
      "url": "https://nothumansearch.ai/mcp"
    }
  }
}
```

无需 API 密钥或认证。

## 可用工具

### `search_agents`

按关键词搜索包含 1,750+ 个 AI 就绪网站的索引。返回带有评分、类别和可用端点的排序结果。

```
search_agents({ query: "code review tools", limit: 10 })
```

### `get_site_details`

检查特定域名的 AI 就绪评分和可用的机器可读端点。

```
get_site_details({ domain: "linear.app" })
```

### `get_stats`

获取聚合索引统计信息，包括已索引站点总数、类别和端点覆盖率。

```
get_stats({})
```

### `submit_site`

提交 URL 进行爬取和 AI 就绪分析。

```
submit_site({ url: "https://example.com" })
```

### `verify_mcp`

通过发送 JSON-RPC 探测并检查有效响应来验证 URL 是否为活跃的 MCP 端点。

```
verify_mcp({ url: "https://example.com/mcp" })
```

### `list_categories`

列出可用的发现类别以缩小搜索范围。

```
list_categories({})
```

### `get_top_sites`

检索排名最高的已索引站点。

```
get_top_sites({ limit: 10 })
```

### `register_monitor`

使用用户提供的电子邮件地址注册域名监控。

```
register_monitor({ domain: "example.com", email: "user@example.com" })
```

## 示例

### 示例 1：发现代码审查工具

```text
Use @not-human-search-mcp to find code review tools that expose MCP or API endpoints.
```

智能体将调用 `search_agents({ query: "code review", limit: 10 })` 并返回带有评分和端点详情的排序结果。

### 示例 2：检查站点是否 AI 就绪

```text
Use @not-human-search-mcp to check the AI-readiness of linear.app.
```

智能体将调用 `get_site_details({ domain: "linear.app" })` 并返回该站点的评分明细。

### 示例 3：验证 MCP 端点

```text
Use @not-human-search-mcp to verify that https://heliumtrades.com/mcp is a working MCP server.
```

智能体将调用 `verify_mcp({ url: "https://heliumtrades.com/mcp" })` 并确认其是否响应 JSON-RPC。

## 最佳实践

- 使用 `search_agents` 进行广泛发现，然后使用 `get_site_details` 对特定索引结果进行详细分析
- 在将 MCP 端点接入智能体工作流之前，使用 `verify_mcp` 确认其处于活跃状态
- 当相关站点未在索引中且用户希望对其进行分析时，使用 `submit_site`
- 仅在用户明确提供电子邮件地址用于监控时使用 `register_monitor`
- 与其他 MCP 技能结合使用，构建动态工具发现管道

## 限制

- 搜索索引覆盖 1,750+ 个站点并定期更新，但可能不包含互联网上的每个站点。
- 评分反映机器可读信号（llms.txt、OpenAPI、MCP、结构化数据）而非内容质量。
- `verify_mcp` 向目标 URL 发送 JSON-RPC 探测；仅在你预期为 MCP 端点的 URL 上使用。
- `register_monitor` 需要用户提供的电子邮件地址并同意接收监控通知。

## 相关技能

- `@mcp-builder` - 用于构建自己的 MCP 服务器
- `@ai-dev-jobs-mcp` - 通过 MCP 搜索 AI/ML 职位列表
