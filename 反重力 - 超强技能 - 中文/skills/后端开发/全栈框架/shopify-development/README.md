# Shopify 开发技能

用于在 Shopify 平台上构建的综合技能：应用、扩展、主题和 API 集成。

## 功能特性

- **应用开发** - OAuth 认证、GraphQL Admin API、webhook、计费集成
- **UI 扩展** - 使用 Polaris 组件自定义结账、管理后台、POS
- **主题开发** - Liquid 模板、sections、snippets
- **Shopify Functions** - 自定义折扣、支付、配送规则

## 目录结构

```
shopify-development/
├── SKILL.md              # 主技能文件（AI 优化）
├── README.md             # 本文件
├── references/
│   ├── app-development.md    # OAuth、API、webhook、计费
│   ├── extensions.md         # UI 扩展、Functions
│   └── themes.md             # Liquid、主题架构
└── scripts/
    ├── shopify_init.py       # 交互式项目脚手架
    ├── shopify_graphql.py    # GraphQL 工具和模板
    └── tests/                # 单元测试
```

## 已验证的 GraphQL

本技能中的所有 GraphQL 查询和变更均已使用官方 Shopify MCP 针对 Shopify Admin API 2026-01 schema 进行验证。

## 快速开始

```bash
# 安装 Shopify CLI
npm install -g @shopify/cli@latest

# 创建新应用
shopify app init

# 启动开发
shopify app dev
```

## 使用触发词

当用户提及以下内容时激活此技能：

- "shopify app"、"shopify extension"、"shopify theme"
- "checkout extension"、"admin extension"、"POS extension"
- "liquid template"、"polaris"、"shopify graphql"
- "shopify webhook"、"shopify billing"、"metafields"

## API 版本

当前版本：**2026-01**（季度发布，12 个月支持期）

## 许可证

MIT
