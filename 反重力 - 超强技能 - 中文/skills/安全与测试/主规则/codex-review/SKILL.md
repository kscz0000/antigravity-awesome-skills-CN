---
name: codex-review
description: "集成 Codex AI 的专业代码审查，支持自动生成 CHANGELOG。当用户要求'代码审查'、'提交前审查'、'自动生成 CHANGELOG'、'大规模重构审查'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# codex-review

## 概述

集成 Codex AI 的专业代码审查，支持自动生成 CHANGELOG

## 使用场景

- 提交前需要专业代码审查
- 需要自动生成 CHANGELOG
- 审查大规模重构

## 安装

```bash
npx skills add -g BenedictKing/codex-review
```

## 使用步骤

1. 使用上述命令安装技能
2. 确保已安装 Codex CLI
3. 使用 `/codex-review` 或自然语言触发

## 示例

参见 [GitHub 仓库](https://github.com/BenedictKing/codex-review) 获取示例。

## 最佳实践

- 在项目根目录保持 CHANGELOG.md
- 使用约定式提交消息

## 故障排除

参见 GitHub 仓库获取故障排除指南。

## 相关技能

- context7-auto-research, tavily-web, exa-search, firecrawl-scraper

## 限制

- 仅在任务明确符合上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清
