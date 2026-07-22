---
name: clarvia-aeo-check
description: "使用 Clarvia AEO（智能体体验优化）为任何 MCP 服务器、API 或 CLI 评分，评估其智能体就绪度。在将 15,400+ 已索引工具添加到工作流之前进行搜索。当用户要求评估 MCP 服务器、API 或 CLI 工具的智能体就绪度时使用。"
category: tool-quality
risk: safe
source: community
date_added: "2026-03-27"
author: digitamaz
tags: [mcp, aeo, tool-quality, agent-readiness, api-scoring, clarvia]
tools: [claude, cursor, windsurf, cline]
---

# Clarvia AEO Check

## 概述

在将任何 MCP 服务器、API 或 CLI 工具添加到智能体工作流之前，使用 Clarvia 对其智能体就绪度进行评分。Clarvia 从四个 AEO 维度评估 15,400+ AI 工具：API 可访问性、数据结构化、智能体兼容性和信任信号。

## 前置条件

将 Clarvia MCP 服务器添加到配置中：

```json
{
  "mcpServers": {
    "clarvia": {
      "command": "npx",
      "args": ["-y", "clarvia-mcp-server"]
    }
  }
}
```

## 何时使用此技能

- 在评估新的 MCP 服务器后再将其添加到配置中时使用
- 在比较两个功能相似的工具时使用
- 在构建动态选择工具的智能体时使用
- 在查找某类别中质量最高的工具时使用

## 工作原理

### 步骤 1：对特定工具评分

让 Claude 通过 URL 或名称对任何工具进行评分：

```
Score https://github.com/example/my-mcp-server for agent-readiness
```

Clarvia 返回 0-100 的 AEO 分数，并包含四个维度的详细分解。

### 步骤 2：按类别搜索工具

```
Find the top-rated database MCP servers using Clarvia
```

从 15,400+ 已索引工具中返回排名结果。

### 步骤 3：工具对比

```
Compare supabase-mcp vs firebase-mcp using Clarvia
```

返回并排分数对比和推荐建议。

### 步骤 4：查看排行榜

```
Show me the top 10 MCP servers for authentication using Clarvia
```

## 示例

### 示例 1：安装前评估

```
Before I add this MCP server to my config, score it:
https://github.com/example/new-tool

Use the clarvia aeo_score tool and tell me if it's agent-ready.
```

### 示例 2：查找类别中最佳工具

```
I need an MCP server for web scraping. Use Clarvia to find the 
top-rated options and compare the top 3.
```

### 示例 3：CI/CD 质量门控

使用 GitHub Action 添加到 CI 流水线：

```yaml
- uses: clarvia-project/clarvia-action@v1
  with:
    url: https://your-api.com
    fail-under: 70
```

## AEO 分数解读

| 分数 | 评级 | 含义 |
|-------|--------|---------|
| 90-100 | 智能体原生 | 专为智能体使用而构建 |
| 70-89 | 智能体友好 | 运行良好，有轻微缺陷 |
| 50-69 | 智能体兼容 | 可用但需要改进 |
| 30-49 | 部分智能体就绪 | 存在明显局限 |
| 0-29 | 未达智能体就绪 | 不适用于智能体工作流 |

## 最佳实践

- ✅ 在将工具添加到长期运行的智能体工作流之前进行评分
- ✅ 使用 Clarvia 排行榜发现你未曾考虑过的替代方案
- ✅ 定期重新检查分数——工具会随时间改进
- ❌ 不要跳过对"知名"工具的评分——即使是流行工具也可能得分较低
- ❌ 不要在生产环境智能体流水线中使用得分低于 50 的工具，除非你了解其局限性

## 常见问题

- **问题：** Clarvia 对某个工具返回"未找到"
  **解决方案：** 尝试直接使用 `aeo_score` 通过 URL 扫描——Clarvia 会按需评分

- **问题：** 我信任的工具分数看起来偏低
  **解决方案：** 使用 `get_score_breakdown` 查看哪些维度较弱，并判断它们对你的用例是否重要

## 相关技能

- `@mcp-builder` - 构建能在 AEO 上获得高分的新 MCP 服务器
- `@agent-evaluation` - 更广泛的智能体质量评估框架

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
