---
name: mcp-tool-developer
description: "构建模型上下文协议(MCP)服务器和工具。涵盖TypeScript/Python全栈MCP开发、测试、部署与注册发布。"
category: developer-tools
risk: safe
source: community
source_repo: demo112/yunqu-ai-skills
source_type: community
date_added: "2026-05-13"
author: yundu-ai
tags: [mcp, ai-agent, tool-development, typescript, python, llm, model-context-protocol]
tools: [claude, cursor, gemini]
---

# MCP 工具开发

## 概述

专注于构建模型上下文协议(MCP)服务器，为 AI 智能体赋予新能力。覆盖完整的 MCP 开发生命周期：规格定义、实现、测试、部署与注册发布。支持 TypeScript 和 Python 两种语言，提供生产级可用模式。

本技能掌握 MCP 规范原语（tools、resources、prompts、sampling）、传输方式（stdio、SSE、Streamable HTTP），以及让 MCP 服务器可靠且可组合的工具设计模式。

## 适用场景

- 从零构建新的 MCP 服务器时使用
- 将现有 API 封装为 MCP 工具时使用
- 调试 MCP 服务器问题时使用
- 设计 MCP 服务器的工具 Schema 时使用
- 将 MCP 服务器发布到注册中心时使用

## 工作流程

### 第 1 步：定义 MCP 服务器范围

确定服务器应暴露哪些能力：
- **Tools（工具）** - LLM 可调用的函数（主要用途）
- **Resources（资源）** - LLM 可读取的数据（文件、API、数据库）
- **Prompts（提示词）** - 可复用的提示词模板

选择传输方式：
- **stdio** - 用于本地 CLI 工具（Claude Code、Cursor）
- **SSE（Server-Sent Events）** - 用于远程/托管工具
- **Streamable HTTP** - MCP 规范新增，适用于现代部署

### 第 2 步：设计工具 Schema

在编写实现之前，先定义输入/输出 Schema：

```typescript
{
  name: "tool_name",
  description: "What this tool does (visible to the LLM)",
  inputSchema: {
    type: "object",
    properties: { ... },
    required: [ ... ]
  }
}
```

### 第 3 步：实现服务器

创建带有正确错误处理、输入校验和日志记录的服务器。使用官方 MCP SDK：TypeScript（@modelcontextprotocol/sdk）或 Python（mcp）。

### 第 4 步：测试与部署

使用 MCP Inspector 测试，校验工具 Schema，处理边界情况，然后进行本地或远程部署。

## 示例

### 示例 1：TypeScript MCP 服务器

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-tools", version: "1.0.0" });

server.tool("greet", "Greet someone by name",
  { name: z.string().describe("Person's name") },
  async ({ name }) => ({ content: [{ type: "text", text: `Hello, ${name}!` }] })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 示例 2：API 封装模式

将外部 API 封装为 MCP 工具，包含认证、速率限制和错误处理：
- 将 API 端点映射为工具
- 通过环境变量处理认证
- 将 API 响应转换为 LLM 友好格式
- 添加指数退避重试逻辑

## 最佳实践

- 构建小而专注的工具，支持链式调用，而非构建庞大的一体化工具
- 返回结构化错误而非崩溃——工具应优雅地失败
- 先定义 Schema，再实现功能
- 在描述中包含帮助 LLM 理解何时及如何使用每个工具的说明
- 根据 Schema 校验所有输入
- 对外部 API 调用添加速率限制
- 使用环境变量存储密钥，绝不硬编码凭证

## 局限性

- 本技能提供指导和代码生成；实际运行测试需要开发环境
- MCP 规范仍在演进；务必检查最新的规范版本
- 部署处理敏感数据的工具前，安全审查必不可少

## 安全注意事项

- 绝不在工具实现中硬编码 API 密钥或凭证
- 所有认证均使用环境变量或密钥管理器
- 校验并清理所有输入，防止注入攻击
- 对外部 API 调用进行速率限制，防止滥用
- 仔细审查工具权限——工具可能访问文件、网络和执行代码

## 常见问题

- **问题：** LLM 使用错误参数调用工具
  **解决方案：** 改进工具描述并在描述字段中添加示例。LLM 依据描述来决定如何调用工具。

- **问题：** 大输入导致工具超时
  **解决方案：** 添加输入大小校验和分页。对大响应使用流式传输而非缓冲。

## 相关技能

- `api-integration-architect` - 用于 MCP 工具中的 API 设计模式
- `security-audit-code-reviewer` - 用于审查 MCP 服务器代码安全性
