---
name: buywhere-product-catalog
description: "使用 BuyWhere 的 MCP 和 API 接口，为 AI 购物智能体添加商品搜索、价格比较和优惠发现功能。当用户要求'商品搜索'、'价格比较'、'优惠发现'、'BuyWhere MCP 配置'、'购物智能体接入'时使用。"
category: ecommerce
risk: safe
source: official
source_repo: BuyWhere/buywhere-cursor-plugin
source_type: official
license: "Not declared"
license_source: "https://github.com/BuyWhere/buywhere-cursor-plugin"
date_added: "2026-04-29"
author: BuyWhere
tags: [buywhere, ecommerce, shopping, mcp, api, product-catalog]
tools: [claude, cursor, codex, gemini]
---

# BuyWhere 商品目录

## 概述

BuyWhere 为 AI 智能体提供商品目录接口，支持购物流程、价格比较和优惠发现。当你希望智能体通过 BuyWhere 的 MCP 配置路径或 API 接入流程来连接商品搜索或商家感知的商务操作时，使用此技能。

最安全的公开起点是实时开发者门户、API 密钥注册流程、MCP 指南和官方 Cursor 插件仓库。

## 何时使用此技能

- 当你想为 AI 购物或推荐智能体添加结构化商品搜索时使用。
- 当用户要求在 Cursor、Claude Desktop 或自定义智能体运行时中配置 BuyWhere MCP 时使用。
- 当你需要 BuyWhere API 密钥、MCP 配置或插件发现的具体接入路径时使用。

## 工作原理

### 步骤 1：选择集成接口

从与用户环境匹配的公开 BuyWhere 入口开始：

- 开发者门户：`https://buywhere.ai/developers/`
- API 密钥注册：`https://buywhere.ai/api-keys/`
- MCP 集成指南：`https://api.buywhere.ai/docs/guides/mcp`
- Cursor 插件仓库：`https://github.com/BuyWhere/buywhere-cursor-plugin`

### 步骤 2：确认用户的运行时

在提供配置说明之前，先询问用户使用的是哪个宿主环境：

- Cursor 或其他支持 MCP 的编码助手
- Claude Desktop
- 自定义 MCP 客户端
- 直接 REST API 集成

不要假设同一配置文件或启动命令适用于所有宿主环境。

### 步骤 3：引导首次成功连接

优先采用最小化的首次运行路径：

1. 获取 BuyWhere API 密钥。
2. 按照宿主运行时的 MCP 或插件配置路径进行设置。
3. 在扩展到比价或优惠工作流之前，先运行一个简单的商品搜索请求。

### 步骤 4：扩展到商务工作流

首次查询成功后，帮助用户进入下一层：

- 商品搜索与发现
- 跨商家价格比较
- 优惠发现流程
- 购物智能体编排，将用户引导至商家目标页面

## 示例

### 示例 1：Cursor 插件发现

```text
Use BuyWhere Product Catalog to help me connect BuyWhere inside Cursor and verify one product-search query.
```

### 示例 2：MCP 接入

```text
Use BuyWhere Product Catalog to set up BuyWhere MCP for my shopping agent and keep the first test minimal.
```

## 最佳实践

- ✅ 先从实时开发者门户或 API 密钥流程开始，再提供配置细节。
- ✅ 将首次集成验证保持为一个成功查询。
- ✅ 询问用户使用的是哪个 MCP 宿主或 API 运行时。
- ❌ 除非有当前运行时证据，否则不要声称具体的商品数量或商家数量。
- ❌ 当存在可用的公开页面时，不要将用户引导到已废弃或失效的文档页面。

## 限制

- 此技能不能替代目标 MCP 宿主或 API 客户端内部的环境特定验证。
- 公开 BuyWhere 页面可能变更，因此在精确配置细节重要时，请重新检查实时 URL。

## 安全与注意事项

- 将 API 密钥视为机密。在示例中使用占位符，绝不将真实凭证粘贴到聊天、文档或截图中。
- 在建议文件系统路径、启动命令或本地配置编辑之前，先确认用户的目标宿主环境。

## 常见陷阱

- **问题：** 用户需要 BuyWhere 配置帮助，但尚未创建 API 密钥。
  **解决方案：** 从 `https://buywhere.ai/api-keys/` 开始，完成此步骤后再进行配置。

- **问题：** 文档主机名不可用。
  **解决方案：** 优先使用实时开发者门户、API 密钥流程、`api.buywhere.ai` 上的 MCP 指南和官方 GitHub 插件仓库。

## 相关技能

- `@api-design-principles` - 当用户需要围绕商务集成的 API 设计指导时使用。
- `@mcp-builder` - 当用户正在构建或扩展 MCP 服务器而非消费 MCP 服务时使用。
