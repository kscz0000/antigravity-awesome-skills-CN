---
name: git-advanced-workflows
description: "掌握高级 Git 技术以维护干净的历史记录、高效协作，并自信地从任何情况中恢复。当用户要求'清理提交历史'、'cherry-pick提交'、'查找引入bug的提交'、'使用worktree'、'恢复丢失的提交'、'交互式rebase'、'git bisect'或'高级Git工作流'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Git 高级工作流

掌握高级 Git 技术以维护干净的历史记录、高效协作，并自信地从任何情况中恢复。

## 不适用场景

- 任务与 Git 高级工作流无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 合并前清理提交历史
- 跨分支应用特定提交
- 查找引入 bug 的提交
- 同时处理多个功能
- 从 Git 错误或丢失的提交中恢复
- 管理复杂的分支工作流
- 准备干净的 PR 以供审查
- 同步已分叉的分支

## 核心概念

### 1. 交互式 Rebase

交互式 rebase 是编辑 Git 历史的多功能工具。

**常用操作：**
- `pick`：保持提交原样
- `reword`：修改提交信息
- `edit`：修改提交内容
- `squash`：与前一个提交合并
- `fixup`：类似 squash 但丢弃提交信息
- `drop`：完全删除提交

**基本用法：**
```bash
# Rebase 最近 5 个提交
git rebase -i HEAD~5

# Rebase 当前分支的所有提交
git rebase -i $(git merge-base HEAD main)

# Rebase 到特定提交
git rebase -i abc123
```

### 2. Cherry-Picking

将特定提交从一个分支应用到另一个分支，而无需合并整个分支。

```bash
# Cherry-pick 单个提交
git cherry-pick abc123

# Cherry-pick 提交范围（不包含起始提交）
git cherry-pick abc123..def456

# Cherry-pick 但不提交（仅暂存更改）
git cherry-pick -n abc123

# Cherry-pick 并编辑提交信息
git cherry-pick -e abc123
```

### 3. Git Bisect

通过二分查找遍历提交历史，找出引入 bug 的提交。

```bash
# 启动 bisect
git bisect start

# 标记当前提交为 bad
git bisect bad

# 标记已知的好提交
git bisect good v1.0.0

# Git 会检出中间提交 - 测试它
# 然后标记为 good 或 bad
git bisect good  # 或：git bisect bad

# 继续直到找到 bug
# 完成后
git bisect reset
```

**自动化 Bisect：**
```bash
# 使用脚本自动测试
git bisect start HEAD v1.0.0
git bisect run ./test.sh

# test.sh 应返回 0 表示 good，1-127（除 125 外）表示 bad
```

### 4. Worktrees

同时处理多个分支，无需 stash 或切换分支。

```bash
# 列出现有 worktree
git worktree list

# 为功能分支添加新 worktree
git worktree add ../project-feature feature/new-feature

# 添加 worktree 并创建新分支
git worktree add -b bugfix/urgent ../project-hotfix main

# 删除 worktree
git worktree remove ../project-feature

# 清理过期的 worktree
git worktree prune
```

### 5. Reflog

你的安全网 - 跟踪所有 ref 移动，甚至包括已删除的提交。

```bash
# 查看 reflog
git reflog

# 查看特定分支的 reflog
git reflog show feature/branch

# 恢复已删除的提交
git reflog
# 找到提交哈希
git checkout abc123
git branch recovered-branch

# 恢复已删除的分支
git reflog
git branch deleted-branch abc123
```

## 实战工作流

### 工作流 1：PR 前清理功能分支

```bash
# 从功能分支开始
git checkout feature/user-auth

# 交互式 rebase 清理历史
git rebase -i main

# 示例 rebase 操作：
# - Squash "fix typo" 提交
# - Reword 提交信息使其更清晰
# - 逻辑上重新排序提交
# - Drop 不必要的提交

# 强制推送清理后的分支（如果无其他人使用则安全）
git push --force-with-lease origin feature/user-auth
```

### 工作流 2：将 Hotfix 应用到多个发布版本

```bash
# 在 main 上创建修复
git checkout main
git commit -m "fix: critical security patch"

# 应用到发布分支
git checkout release/2.0
git cherry-pick abc123

git checkout release/1.9
git cherry-pick abc123

# 如有冲突则处理
git cherry-pick --continue
# 或
git cherry-pick --abort
```

### 工作流 3：查找 Bug 引入点

```bash
# 启动 bisect
git bisect start
git bisect bad HEAD
git bisect good v2.1.0

# Git 检出中间提交 - 运行测试
npm test

# 如果测试失败
git bisect bad

# 如果测试通过
git bisect good

# Git 会自动检出下一个待测试的提交
# 重复直到找到 bug

# 自动化版本
git bisect start HEAD v2.1.0
git bisect run npm test
```

### 工作流 4：多分支开发

```bash
# 主项目目录
cd ~/projects/myapp

# 为紧急修复创建 worktree
git worktree add ../myapp-hotfix hotfix/critical-bug

# 在单独目录中处理 hotfix
cd ../myapp-hotfix
# 进行更改，提交
git commit -m "fix: resolve critical bug"
git push origin hotfix/critical-bug

# 返回主工作区，不受干扰
cd ~/projects/myapp
git fetch origin
git cherry-pick hotfix/critical-bug

# 完成后清理
git worktree remove ../myapp-hotfix
```

### 工作流 5：从错误中恢复

```bash
# 不小心重置到错误的提交
git reset --hard HEAD~5  # 糟糕！

# 使用 reflog 找到丢失的提交
git reflog
# 输出显示：
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: my important changes

# 恢复丢失的提交
git reset --hard def456

# 或从丢失的提交创建分支
git branch recovery def456
```

## 高级技巧

### Rebase vs Merge 策略

**何时使用 Rebase：**
- 推送前清理本地提交
- 使功能分支与 main 保持同步
- 创建线性历史以便于审查

**何时使用 Merge：**
- 将完成的功能集成到 main
- 保留协作的完整历史
- 他人使用的公共分支

```bash
# 用 rebase 更新功能分支（包含 main 的更改）
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# 处理冲突
git status
# 在文件中解决冲突
git add .
git rebase --continue

# 或改用 merge
git merge origin/main
```

### Autosquash 工作流

在 rebase 期间自动 squash fixup 提交。

```bash
# 创建初始提交
git commit -m "feat: add user authentication"

# 稍后，修复该提交中的某些内容
# 暂存更改
git commit --fixup HEAD  # 或指定提交哈希

# 进行更多更改
git commit --fixup abc123

# 带 autosquash 的 rebase
git rebase -i --autosquash main

# Git 自动标记 fixup 提交
```

### 拆分提交

将一个提交拆分为多个逻辑提交。

```bash
# 启动交互式 rebase
git rebase -i HEAD~3

# 用 'edit' 标记要拆分的提交
# Git 会在该提交处停止

# 重置提交但保留更改
git reset HEAD^

# 按逻辑块暂存和提交
git add file1.py
git commit -m "feat: add validation"

git add file2.py
git commit -m "feat: add error handling"

# 继续 rebase
git rebase --continue
```

### 部分 Cherry-Pick

仅 cherry-pick 提交中的特定文件。

```bash
# 显示提交中的文件
git show --name-only abc123

# 从提交中检出特定文件
git checkout abc123 -- path/to/file1.py path/to/file2.py

# 暂存并提交
git commit -m "cherry-pick: apply specific changes from abc123"
```

## 最佳实践

1. **始终使用 --force-with-lease**：比 --force 更安全，防止覆盖他人的工作
2. **仅 Rebase 本地提交**：不要 rebase 已推送且共享的提交
3. **描述性的提交信息**：未来的你会感谢现在的你
4. **原子提交**：每个提交应该是单个逻辑更改
5. **强制推送前测试**：确保历史重写没有破坏任何内容
6. **保持 Reflog 意识**：记住 reflog 是你的安全网，保留 90 天
7. **风险操作前创建分支**：在复杂 rebase 前创建备份分支

```bash
# 安全的强制推送
git push --force-with-lease origin feature/branch

# 风险操作前创建备份
git branch backup-branch
git rebase -i main
# 如果出现问题
git reset --hard backup-branch
```

## 常见陷阱

- **Rebase 公共分支**：会导致协作者的历史冲突
- **不带 Lease 的强制推送**：可能覆盖队友的工作
- **在 Rebase 中丢失工作**：仔细解决冲突，rebase 后测试
- **忘记清理 Worktree**：孤立的 worktree 占用磁盘空间
- **实验前不备份**：始终创建安全分支
- **在脏工作目录上 Bisect**：bisect 前提交或 stash

## 恢复命令

```bash
# 中止进行中的操作
git rebase --abort
git merge --abort
git cherry-pick --abort
git bisect reset

# 将文件恢复到特定提交的版本
git restore --source=abc123 path/to/file

# 撤销最后一个提交但保留更改
git reset --soft HEAD^

# 撤销最后一个提交并丢弃更改
git reset --hard HEAD^

# 恢复已删除的分支（90 天内）
git reflog
git branch recovered-branch abc123
```

## 资源

- **references/git-rebase-guide.md**：交互式 rebase 深入指南
- **references/git-conflict-resolution.md**：高级冲突解决策略
- **references/git-history-rewriting.md**：安全重写 Git 历史
- **assets/git-workflow-checklist.md**：PR 前清理检查清单
- **assets/git-aliases.md**：高级工作流的实用 Git 别名
- **scripts/git-clean-branches.sh**：清理已合并和过期的分支

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
