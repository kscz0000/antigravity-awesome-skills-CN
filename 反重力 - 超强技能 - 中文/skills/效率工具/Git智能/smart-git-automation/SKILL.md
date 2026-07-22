---
name: smart-git-automation
version: 1.0.0
description: "智能变更检测、自动分支命名与精简的提交/PR 工作流"
risk: critical
source: community
source_type: community
source_repo: mskadu/opencode-agent-skills
license: MIT
license_source: "https://github.com/mskadu/opencode-agent-skills/blob/main/LICENSE"
date_added: "2026-06-05"
---

## 我做什么
- 智能检测并分组相关变更
- 根据变更自动生成描述性分支名
- 精简工作流：扫描 → 分支 → 提交 → 推送 → PR，减少确认交互

## 何时使用
当你想要更快、更智能的 git 工作流——自动按逻辑分组变更、减少手动确认开销时使用。

## 工作流步骤

### 1. 智能检测与分组
并行运行：
- `git status` - 检查变更内容
- `git diff --stat` - 查看文件修改摘要
- `git diff --name-only` - 仅列出变更文件
- `git diff --staged --stat` - 查看已暂存的变更

分析变更并按逻辑分组：
- 同一模块/目录下的文件 → 可能相关
- 近期编辑中一起修改过的文件 → 可能相关
- 互补的新文件 → 可能相关

以清晰格式展示分组变更，例如：
```
📁 Group 1: UI Components
  - src/components/Button.tsx (modified)
  - src/components/Button.test.tsx (modified)

📁 Group 2: API Layer
  - src/api/client.ts (new)
  - src/api/types.ts (modified)
```

### 2. 自动生成分支名
根据主要变更模式生成分支名：
- 格式：`<type>/<short-description>`
- 类型：`feature`、`fix`、`refactor`、`docs`、`test`、`chore`
- 描述从最重要的变更文件/功能推导
- 转为 kebab-case，最长 50 字符
- 示例：
  - `feature/add-user-auth`（来自认证相关文件）
  - `fix/login-validation`（来自验证相关变更）
  - `refactor/api-cleanup`（来自 API 重构）

展示拟定的分支名，要求一个词确认（或输入替代名称）。

### 3. 精简分支与提交
- 若不在 main/master 上：检查当前分支是否与拟定名称匹配
  - 匹配：留在当前分支
  - 不匹配：询问切换还是新建
- 验证分支名后再创建分支，使用 `git checkout -b "$branch_name"`
- 仅暂存显式路径：`git add -- path/to/file ...`
  - 若文件路径是生成的，用 NUL 分隔（`git diff -z --name-only`）并作为路径参数传入。
  - 绝不将不可信文件名拼接到 shell 命令中，也绝不直接执行占位文本。
- 从变更自动生成提交消息：
  - 首行：`<type>: <short description>`（最长 72 字符）
  - 正文：分组的文件变更及简要说明
- 用生成的消息提交，先展示预览
- 要求一个词确认后继续

### 4. 推送与可选 PR
- 提交后询问："推送到远程？(yes/no/abort)"
- 若 yes：`git push -u origin <branch-name>`
- 然后询问："创建 PR？(yes/no)"
- 若 yes：
  - 检查远程：`git remote -v`
  - 若为 fork：使用 fork 的远程（如 `mskadu/repo-name`）
  - 从提交消息自动生成 PR 描述
  - 使用 `gh pr create`，包含：
    - 标题取自分支名
    - 正文：变更摘要 + 文件明细 + 后续事项

## 关键规则
- 自动分组相关文件，但允许用户调整
- 根据实际变更生成分支名，不要让用户命名
- 减少确认：要求一个词回答或单一确认点
- 绝不提交密钥、凭证或大型二进制文件
- 创建 PR 前检查 GitHub 仓库是否存在
- 用户在任一步骤说"no"则跳过后续 PR 步骤
- 若分支已存在且有变更，提供 amend 或新建提交的选项

## 限制

- 不得绕过仓库特定的维护者规则、分支策略或必需的审查门。
- 破坏性或发布类操作必须显式确认；本技能旨在精简日常 Git 流程，而非免除责任。
