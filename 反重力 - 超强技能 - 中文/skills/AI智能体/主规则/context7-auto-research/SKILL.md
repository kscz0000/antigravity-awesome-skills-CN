---
name: context7-auto-research
description: "通过 Context7 API 自动获取 Claude Code 的最新库/框架文档。当需要库和框架的最新文档，或询问 React、Next.js、Prisma 或其他热门库时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# context7-auto-research

## 概述
通过 Context7 API 自动获取 Claude Code 的最新库/框架文档

## 使用场景
- 需要库和框架的最新文档时
- 询问 React、Next.js、Prisma 或其他热门库时

## 安装
```bash
npx skills add -g BenedictKing/context7-auto-research
```

## 分步指南
1. 使用上述命令安装技能
2. 配置 API 密钥（可选，详见 GitHub 仓库）
3. 在 Claude Code 对话中自然使用

## 示例
示例详见 [GitHub 仓库](https://github.com/BenedictKing/context7-auto-research)。

## 最佳实践
- 通过环境变量配置 API 密钥以获得更高的速率限制
- 使用技能的自动触发功能实现无缝集成

## 故障排除
故障排除指南详见 GitHub 仓库。

## 相关技能
- tavily-web, exa-search, firecrawl-scraper, codex-review

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
