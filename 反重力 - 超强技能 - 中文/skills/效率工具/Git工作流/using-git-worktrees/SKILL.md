---
name: using-git-worktrees
description: "Git worktrees 创建共享同一仓库的隔离工作区，可在多个分支上同时工作而无需切换。触发词：git worktree、隔离工作区、创建 worktree、分支隔离、功能分支、工作树、独立工作区、worktree 隔离"
risk: critical
source: community
date_added: "2026-02-27"
---

# 使用 Git Worktrees

## 概述

Git worktrees 创建共享同一仓库的隔离工作区，可在多个分支上同时工作而无需切换。

**核心原则：** 系统化的目录选择 + 安全验证 = 可靠的隔离。

**启动时宣告：**「我正在使用 using-git-worktrees 技能来设置一个隔离的工作区。」

## 目录选择流程

按以下优先级顺序执行：

### 1. 检查已有目录

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**如果找到：** 使用该目录。如果两者都存在，`.worktrees` 优先。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果指定了偏好：** 直接使用，无需询问。

### 3. 询问用户

如果没有目录存在且 CLAUDE.md 中没有偏好设置：

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全验证

### 项目本地目录（.worktrees 或 worktrees）

**创建 worktree 之前必须验证目录已被忽略：**

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果未被忽略：**

依据 Jesse 的规则「立即修复损坏的东西」：
1. 向 .gitignore 添加相应行
2. 提交该变更
3. 继续创建 worktree

**为何关键：** 防止意外将 worktree 内容提交到仓库。

### 全局目录（~/.config/superpowers/worktrees）

无需 .gitignore 验证——完全位于项目之外。

## 创建步骤

### 1. 检测项目名称

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目初始化

自动检测并运行相应的初始化命令：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证干净的基线

运行测试以确保 worktree 起始状态干净：

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**如果测试失败：** 报告失败，询问是继续还是排查。

**如果测试通过：** 报告就绪。

### 5. 报告位置

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考

| 场景 | 操作 |
|------|------|
| `.worktrees/` 已存在 | 使用它（验证已被忽略） |
| `worktrees/` 已存在 | 使用它（验证已被忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 两者都不存在 | 检查 CLAUDE.md → 询问用户 |
| 目录未被忽略 | 添加到 .gitignore + 提交 |
| 基线测试失败 | 报告失败 + 询问 |
| 没有 package.json/Cargo.toml | 跳过依赖安装 |

## 常见错误

### 跳过忽略验证

- **问题：** worktree 内容被跟踪，污染 git status
- **修复：** 创建项目本地 worktree 之前务必使用 `git check-ignore`

### 假设目录位置

- **问题：** 造成不一致，违反项目约定
- **修复：** 遵循优先级：已有目录 > CLAUDE.md > 询问

### 测试失败仍继续

- **问题：** 无法区分新 bug 与既有故障
- **修复：** 报告失败，获得明确许可后再继续

### 硬编码初始化命令

- **问题：** 在使用不同工具的项目上会失败
- **修复：** 从项目文件自动检测（package.json 等）

## 示例工作流

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## 危险信号

**绝不：**
- 未验证目录已被忽略就创建 worktree（项目本地）
- 跳过基线测试验证
- 测试失败时不询问就继续
- 在不明确时假设目录位置
- 跳过 CLAUDE.md 检查

**始终：**
- 遵循目录优先级：已有目录 > CLAUDE.md > 询问用户
- 项目本地目录务必验证是否被忽略
- 自动检测并运行项目初始化
- 验证干净的测试基线

## 集成关系

**被调用方：**
- **brainstorming**（第 4 阶段）— 设计获批且进入实现时必须使用
- 任何需要隔离工作区的技能

**配合使用：**
- **finishing-a-development-branch** — 工作完成后必须用于清理
- **executing-plans** 或 **subagent-driven-development** — 工作在此 worktree 中进行

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 若缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
