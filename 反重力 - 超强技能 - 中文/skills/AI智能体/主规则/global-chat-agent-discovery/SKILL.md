---
name: global-chat-agent-discovery
description: "通过 Global Chat 的跨协议目录和 MCP 服务器，搜索 6+ 个注册中心的 18K+ 个 MCP 服务器和 AI 智能体。当用户要求'查找 MCP 服务器'、'搜索 AI 智能体'、'发现可用工具'、'跨协议搜索'时使用。"
category: development
risk: safe
source: community
source_repo: pumanitro/global-chat
source_type: community
date_added: "2026-04-06"
author: pumanitro
tags: [mcp, ai-agents, agent-discovery, agents-txt, a2a, developer-tools]
tools: [claude, cursor, gemini, codex]
---

# Global Chat 智能体发现

## 概述

Global Chat 是一个跨协议 AI 智能体发现平台，将 6+ 个注册中心的 MCP 服务器和 AI 智能体聚合到一个可搜索的目录中。本技能帮助你在 18,000+ 个索引条目中找到适合任何任务的 MCP 服务器、A2A 智能体或 agents.txt 端点。它还提供 MCP 服务器（`@global-chat/mcp-server`），可从任何兼容 MCP 的客户端程序化访问该目录。

## 何时使用

- 需要为特定能力查找 MCP 服务器（如数据库访问、文件转换、API 集成）
- 评估哪些智能体注册中心提供适合你用例的工具
- 想要同时跨多个协议（MCP、A2A、agents.txt）搜索
- 设置智能体间通信时需要发现可用端点

## 工作方式

### 方式一：使用 MCP 服务器（推荐用于智能体）

安装 Global Chat MCP 服务器，从 Claude Code、Cursor 或任何 MCP 客户端程序化搜索目录。

```bash
npm install -g @global-chat/mcp-server
```

添加到你的 MCP 客户端配置：

```json
{
  "mcpServers": {
    "global-chat": {
      "command": "npx",
      "args": ["-y", "@global-chat/mcp-server"]
    }
  }
}
```

然后让智能体搜索工具：

```
Search Global Chat for MCP servers that handle PostgreSQL database queries.
```

### 方式二：使用网页目录

在 [https://global-chat.io](https://global-chat.io) 浏览完整目录：

1. 访问搜索页面并输入查询
2. 按协议筛选（MCP、A2A、agents.txt）
3. 按注册来源筛选
4. 查看服务器详情、能力和安装说明

### 方式三：验证你的 agents.txt

如果你维护 `agents.txt` 文件，使用免费验证器：

1. 访问 [https://global-chat.io/validate](https://global-chat.io/validate)
2. 输入你的域名或粘贴 agents.txt 内容
3. 获得格式合规性和可发现性的即时反馈

## 示例

### 示例 1：为任务查找 MCP 服务器

```
You: "Find MCP servers that can convert PDF files to text"
Agent (via Global Chat MCP): Searching across 6 registries...
  - @anthropic/pdf-tools (mcpservers.org) — PDF parsing and text extraction
  - pdf-converter-mcp (mcp.so) — Convert PDF to text, markdown, or HTML
  - ...
```

### 示例 2：发现 A2A 智能体

```
You: "What A2A agents are available for code review?"
Agent (via Global Chat MCP): Found 12 A2A agents for code review across 3 registries...
```

### 示例 3：检查智能体协议覆盖

```
You: "How many registries list tools for Kubernetes management?"
Agent (via Global Chat MCP): 4 registries carry Kubernetes-related agents (23 total entries)...
```

## 最佳实践

- 自动化工作流和智能体间发现使用 MCP 服务器
- 手动探索和比较使用网页目录
- 发布前验证 agents.txt 以确保最大可发现性
- 检查多个注册中心——不同领域的覆盖差异很大

## 常见问题

- **问题：** 搜索返回结果过多
  **解决：** 添加协议或注册中心筛选以缩小范围

- **问题：** MCP 服务器无法连接
  **解决：** 确保 `npx` 可用，先手动运行 `npx -y @global-chat/mcp-server` 验证

## 相关技能

- `@mcp-client` - 用于通用 MCP 客户端设置和配置
- `@agent-orchestration-multi-agent-optimize` - 用于编排多个已发现的智能体
- `@agent-memory-mcp` - 用于跨会话持久化已发现的智能体信息

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
