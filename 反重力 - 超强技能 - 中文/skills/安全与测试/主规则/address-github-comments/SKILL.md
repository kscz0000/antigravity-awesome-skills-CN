---
name: address-github-comments
description: "使用 gh CLI 处理 GitHub 开放 Pull Request 上的审查评论或 issue 反馈。触发词：处理 PR 评论、回复审查意见、解决 PR 反馈、GitHub 评论处理、address comments、PR review comments、gh pr comment"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 处理 GitHub 评论

## 概述

使用 GitHub CLI (`gh`) 高效处理 PR 审查评论或 issue 反馈。本技能确保系统性地处理所有反馈。

## 前置条件

确保 `gh` 已通过身份验证。

```bash
gh auth status
```

如果未登录，运行 `gh auth login`。

## 工作流程

### 1. 检查评论

获取当前分支 PR 的评论。

```bash
gh pr view --comments
```

或者使用自定义脚本列出讨论线程（如有）。

### 2. 分类与规划

- 列出评论和审查线程。
- 为每条评论提出修复方案。
- **如果评论较多，等待用户确认优先处理顺序。**

### 3. 应用修复

为选定的评论应用代码更改。

### 4. 回复评论

修复完成后，回复线程标记为已解决。

```bash
gh pr comment <PR_NUMBER> --body "Addressed in latest commit."
```

## 常见错误

- **在不理解上下文的情况下应用修复**：始终阅读评论周围的代码。
- **未验证身份**：开始前检查 `gh auth status`。

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
