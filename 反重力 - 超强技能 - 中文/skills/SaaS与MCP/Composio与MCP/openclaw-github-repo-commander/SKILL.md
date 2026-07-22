---
name: openclaw-github-repo-commander
description: "7 阶段超级工作流，用于 GitHub 仓库审计、清理、PR 审查和竞品分析。当用户要求清理仓库、审计 GitHub 项目或进行竞品对标时使用。"
category: development-and-testing
risk: safe
source: community
date_added: "2026-03-18"
author: wd041216-bit
tags: [github, git, repository, audit, cleanup, workflow, devtools, automation, code-review, security]
tools: [claude, cursor]
---
# OpenClaw GitHub 仓库指挥官

## 概述

一套结构化的 7 阶段超级工作流，用于全面管理 GitHub 仓库。此技能自动化仓库审计、清理、竞品对标和优化——将混乱的仓库转变为干净、文档完善、可投入生产的项目。

## 适用场景

- 需要审计仓库中的密钥、垃圾文件或低质量内容
- 用户说"清理我的仓库""优化我的 GitHub 项目"或"审计这个库"
- 以结构化方式审查或创建 Pull Request
- 将项目与 GitHub 上的竞品进行对比
- 在仓库 URL 上运行 `/super-workflow` 或 `/openclaw-github-repo-commander`

## 工作原理

### 阶段 1：接收
克隆目标仓库，定义成功标准，建立基线指标。

### 阶段 2：执行
运行 `scripts/repo-audit.sh` — 自动检查：
- 硬编码密钥（`ghp_`、`sk-`、`AKIA` 等）
- 被跟踪的 `node_modules/` 或构建产物
- 空目录
- 大文件（>1MB）
- `.gitignore` 覆盖不全
- README 中失效的内部链接

### 阶段 3：反思
超越自动化工具的深度人工审查：内容质量、文档一致性、结构性问题、版本不匹配。

### 阶段 4：竞品分析
在 GitHub 上搜索类似仓库。对比文档标准、功能覆盖、Star 数量和社区采纳度。

### 阶段 5：综合
将所有发现整合为按优先级排列的行动计划（P0 关键 / P1 重要 / P2 锦上添花）。

### 阶段 6：迭代
执行计划：删除低价值文件、修复安全问题、升级文档、添加 CI 工作流、更新变更日志。

### 阶段 7：验证
重新运行审计脚本（目标：7/7 PASS），验证所有变更，推送到 GitHub，交付完整报告。

## 示例

### 示例 1：完整仓库审计

```
/openclaw-github-repo-commander https://github.com/owner/my-repo
```

运行全部 7 个阶段并生成详细的前后对比报告。

### 示例 2：快速清理

```
Clean up my GitHub repo — remove junk files, fix secrets, add .gitignore
```

### 示例 3：竞品对标

```
Compare my skill repo with the top 5 similar repos on GitHub
```

## 最佳实践

- ✅ 推送前务必运行阶段 7 验证
- ✅ 使用语义化提交信息：`chore:`、`fix:`、`docs:`
- ✅ 检查 `pr_todo.json` 文件中的待处理审查请求
- ❌ 不要跳过阶段 4 — 竞品分析能暴露盲点
- ❌ 不要提交 `node_modules/` 或 `.env` 文件

## 安全说明

- 审计脚本扫描常见密钥模式，但排除 `.github/workflows/` 以避免误报
- 所有 `gh` CLI 操作使用用户现有认证 — 此技能不会存储任何凭据
- 在阶段 6 中，未经用户明确确认不会修改任何文件

## 源码仓库

[github.com/wd041216-bit/openclaw-github-repo-commander](https://github.com/wd041216-bit/openclaw-github-repo-commander)

**License**: MIT | **Version**: 4.0.0

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 输出结果不能替代针对特定环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
