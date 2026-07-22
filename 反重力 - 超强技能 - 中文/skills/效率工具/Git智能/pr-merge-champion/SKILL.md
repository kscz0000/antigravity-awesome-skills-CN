---
name: pr-merge-champion
description: "优化 Pull Request 以快速获得批准和合并，确保干净的 diff、全面的自审和结构化的文档。触发词：PR合并、合并冠军、PR优化、快速合并、代码审查准备、PR自审、merge champion"
category: workflow
risk: safe
source: self
source_type: self
date_added: "2026-06-16"
author: himanshu-2l
tags: [git, github, pull-request, code-review, workflow]
tools: [claude, cursor, gemini, antigravity]
---

# PR 合并冠军

## 概述

一套系统化的操作手册，用于准备、审查和记录 Pull Request，确保它们高质量、无常见疏漏，并针对即时获得维护者批准和合并进行优化。

## 何时使用此技能

- 在准备于 GitHub 或任何 Git 托管平台提交新的 Pull Request 时使用。
- 在对功能分支或 Bug 修复分支进行自审，检查代码整洁度和一致性时使用。
- 在希望减少审查轮次、加速变更集成时使用。

## 工作原理

### 步骤 1：提交前清理与 Rebase

在将代码展示给审查者之前，清理工作区中的杂乱内容并确保分支是最新的：
1. 将功能分支 rebase 到最新目标分支（如 `main` 或 `master`）之上，尽早解决冲突。
2. 清理仓库中的未跟踪文件、临时文件和交换文件。
3. 在本地运行 linter、格式化工具和编译器，确保不存在风格或语法错误。

### 步骤 2：关键自审

像审查者一样逐行审查自己的 diff。注意以下问题：
1. 遗留的调试语句（如 `console.log`、`print`、断点或自定义调试标志）。
2. 不必要的变更、仅含空白的 diff 或被注释掉的代码块。
3. 未完成的 `TODO` 注释，应该解决或转化为已追踪的 Issue。
4. 错误处理和边界情况的正确性。

### 步骤 3：本地验证与测试套件

验证所有变更按预期工作：
1. 在本地运行项目的自动化测试套件，确认未引入回归。
2. 检查新增代码块的测试覆盖率。
3. 手动测试功能或 Bug 修复的关键路径和边界情况。

### 步骤 4：撰写 Pull Request 描述

编写高信息量、结构化的 PR 描述。优秀的描述讲述变更的故事：
1. **摘要**：变更的简要说明。
2. **背景 / 原因**：为什么需要此变更以及它解决了什么问题。
3. **验证**：你如何测试的具体细节（测试命令、截图或分步复现过程）。
4. **检查清单**：遵循仓库的贡献指南和检查清单要求。

## 示例

### 示例 1：创建干净的 PR 描述

```markdown
# Pull Request: Implement Rate Limiting on Authentication Endpoint

## Summary
Introduces an IP-based rate limiter on the `/api/v1/auth/login` endpoint using Redis to prevent brute-force attacks.

## Why
We identified a high volume of login attempts targeting single accounts. This rate limiting window slows down attackers while keeping the system responsive for genuine users.

## Verification
- Ran unit tests: `npm run test tests/auth.test.js` (all green)
- Manually verified using Postman: sending 15 requests in under 60 seconds returns `429 Too Many Requests`.

## Checklist
- [x] Code follows the style guide
- [x] Unit tests added/updated
- [x] Documentation updated
```

### 示例 2：自审清理命令

在提交前，运行以下命令检查 diff 中的意外添加：

```bash
# Check the names of files changed to ensure no unwanted files are staged
git status --porcelain

# Review the actual diff for any leftover print statements or debuggers
git diff | grep -E "(console\.log|debugger|print\(|var_dump|binding\.pry)"
```

## 最佳实践

- **保持 PR 小而聚焦**：变更少于 200 行的 PR 被审查和合并的速度显著快于大型 PR。
- **先进行自审**：先发现自身的 Bug 和格式问题，能建立与维护者的信任。
- **尊重仓库指南**：检查项目的 `CONTRIBUTING.md` 和 Pull Request 模板，严格遵守。
- **不要捆绑无关变更**：避免在功能 PR 中夹带重构或无关的 Bug 修复。应创建独立的 PR。
- **不要忽视 CI 失败**：在请求审查前，务必修复分支上失败的测试、linter 或安全扫描。

## 局限性

- 此技能不能替代项目特定的 CI/CD 验证、自动化测试或领域专家审查。
- 假设使用标准的 Git 和类似 GitHub 的环境，但核心原则同样适用于 GitLab、Bitbucket 和其他平台。

## 常见陷阱

- **问题**：PR 因格式或风格的细微评论而长时间处于开放状态。
  **解决方案**：在提交前始终运行仓库的本地格式化工具（如 Prettier、ESLint、Black）。
- **问题**：打开 PR 后立即出现合并冲突。
  **解决方案**：每天拉取最新的主分支并 rebase 或合并到你的分支中。

## 相关技能

- `@pr-writer` - Sentry 特定的 PR 撰写指南。
- `@clean-code` - 确保提交前的代码质量。
