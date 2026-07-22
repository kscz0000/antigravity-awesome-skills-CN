---
name: git-hooks-automation
description: "掌握 Git hooks 配置，涵盖 Husky、lint-staged、pre-commit 框架和 commitlint。在代码进入 CI 前自动执行代码质量门控、格式化、lint 检查和提交信息规范。适用于设置 git hooks、配置 Husky、强制提交信息规范等场景。"
risk: safe
source: community
date_added: "2026-03-07"
---

# Git Hooks 自动化

在 Git 层面自动执行代码质量检查。设置钩子，在提交和推送到达 CI 流水线之前进行 lint、格式化、测试和验证——秒级发现问题，而非分钟级。

## 适用场景

- 需要设置 git hooks 或添加 pre-commit hooks
- 配置 Husky、lint-staged 或 pre-commit 框架
- 强制执行提交信息规范（Conventional Commits、commitlint）
- 在提交前自动执行 lint、格式化或类型检查
- 为测试运行器设置 pre-push hooks
- 从 Husky v4 迁移到 v9+ 或从零开始采用 hooks
- 用户提到"pre-commit"、"commit-msg"、"pre-push"、"lint-staged"或"githooks"

## Git Hooks 基础

Git hooks 是在 Git 工作流的特定节点自动运行的脚本。它们存放在 `.git/hooks/` 中，默认不受版本控制——这就是 Husky 等工具存在的原因。

### Hook 类型与触发时机

| Hook | 触发时机 | 常见用途 |
|---|---|---|
| `pre-commit` | 提交创建前 | 对暂存文件执行 lint、格式化、类型检查 |
| `prepare-commit-msg` | 默认信息生成后、编辑器打开前 | 自动填充提交模板 |
| `commit-msg` | 用户编写提交信息后 | 强制提交信息格式 |
| `post-commit` | 提交创建后 | 通知、日志记录 |
| `pre-push` | 推送到远程前 | 运行测试、检查分支策略 |
| `pre-rebase` | rebase 开始前 | 防止在受保护分支上 rebase |
| `post-merge` | 合并完成后 | 安装依赖、运行迁移 |
| `post-checkout` | 切换分支后 | 安装依赖、重建资源 |

### 原生 Git Hooks（无框架）

```bash
# Create a pre-commit hook manually
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
set -e

# Run linter on staged files only
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|jsx|tsx)$' || true)

if [ -n "$STAGED_FILES" ]; then
  echo "🔍 Linting staged files..."
  echo "$STAGED_FILES" | xargs npx eslint --fix
  echo "$STAGED_FILES" | xargs git add  # Re-stage after fixes
fi
EOF
chmod +x .git/hooks/pre-commit
```

**问题**：`.git/hooks/` 仅存在于本地，无法与团队共享。应使用框架。

## Husky + lint-staged（Node.js 项目）

JavaScript/TypeScript 项目的现代标准。Husky 管理 Git hooks；lint-staged 仅对暂存文件执行命令以提升速度。

### 快速配置（Husky v9+）

```bash
# Install
npm install --save-dev husky lint-staged

# Initialize Husky (creates .husky/ directory)
npx husky init

# The init command creates a pre-commit hook — edit it:
echo "npx lint-staged" > .husky/pre-commit
```

### 在 `package.json` 中配置 lint-staged

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix --max-warnings=0",
      "prettier --write"
    ],
    "*.{css,scss}": [
      "prettier --write",
      "stylelint --fix"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

### 添加提交信息 Lint 检查

```bash
# Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Create commitlint config
cat > commitlint.config.js << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100]
  }
};
EOF

# Add commit-msg hook
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

### 添加 Pre-Push Hook

```bash
# Run tests before pushing
echo "npm test" > .husky/pre-push
```

### 完整的 Husky 目录结构

```
project/
├── .husky/
│   ├── pre-commit        # npx lint-staged
│   ├── commit-msg        # npx --no -- commitlint --edit $1
│   └── pre-push          # npm test
├── commitlint.config.js
├── package.json          # lint-staged config here
└── ...
```

## pre-commit 框架（Python / 多语言项目）

语言无关的框架，适用于任何项目。Hooks 在 YAML 中定义，在隔离环境中运行。

### 配置

```bash
# Install (Python required)
pip install pre-commit

# Create config
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # Built-in checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: detect-private-key

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  # Python linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: ['--fix']
      - id: ruff-format

  # Shell script linting
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.10.0.1
    hooks:
      - id: shellcheck

  # Commit message format
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.2.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
EOF

# Install hooks into .git/hooks/
pre-commit install
pre-commit install --hook-type commit-msg

# Run against all files (first time)
pre-commit run --all-files
```

### 常用命令

```bash
pre-commit install              # Install hooks
pre-commit run --all-files      # Run on everything (CI or first setup)
pre-commit autoupdate           # Update hook versions
pre-commit run <hook-id>        # Run a specific hook
pre-commit clean                # Clear cached environments
```

## 自定义 Hook 脚本（任意语言）

对于不使用 Node 或 Python 的项目，直接用 shell 编写 hooks。

### 可移植的 Pre-Commit Hook

```bash
#!/bin/sh
# .githooks/pre-commit — Team-shared hooks directory
set -e

echo "=== Pre-Commit Checks ==="

# 1. Prevent commits to main/master
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "❌ Direct commits to $BRANCH are not allowed. Use a feature branch."
  exit 1
fi

# 2. Check for debugging artifacts
if git diff --cached --diff-filter=ACM | grep -nE '(console\.log|debugger|binding\.pry|import pdb)' > /dev/null 2>&1; then
  echo "⚠️  Debug statements found in staged files:"
  git diff --cached --diff-filter=ACM | grep -nE '(console\.log|debugger|binding\.pry|import pdb)'
  echo "Remove them or use git commit --no-verify to bypass."
  exit 1
fi

# 3. Check for large files (>1MB)
LARGE_FILES=$(git diff --cached --name-only --diff-filter=ACM | while read f; do
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  if [ "$size" -gt 1048576 ]; then echo "$f ($((size/1024))KB)"; fi
done)
if [ -n "$LARGE_FILES" ]; then
  echo "❌ Large files detected:"
  echo "$LARGE_FILES"
  exit 1
fi

# 4. Check for secrets patterns
if git diff --cached --diff-filter=ACM | grep -nEi '(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{48}|ghp_[a-zA-Z0-9]{36}|password\s*=\s*["\x27][^"\x27]+["\x27])' > /dev/null 2>&1; then
  echo "🚨 Potential secrets detected in staged changes! Review before committing."
  exit 1
fi

echo "✅ All pre-commit checks passed"
```

### 通过 `core.hooksPath` 共享自定义 Hooks

```bash
# In your repo, set a shared hooks directory
git config core.hooksPath .githooks

# Add to project setup docs or Makefile
# Makefile
setup:
	git config core.hooksPath .githooks
	chmod +x .githooks/*
```

## CI 集成

Hooks 是第一道防线，但 CI 才是最终保障。

### 在 CI 中运行 pre-commit（GitHub Actions）

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]
jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - uses: pre-commit/action@v3.0.1
```

### 在 CI 中运行 lint-staged（仅验证）

```yaml
# Validate that lint-staged would pass (catch bypassed hooks)
name: Lint Check
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx eslint . --max-warnings=0
      - run: npx prettier --check .
```

## 常见问题与修复

### Hooks 未运行

| 症状 | 原因 | 解决方案 |
|---|---|---|
| Hooks 静默跳过 | 未安装到 `.git/hooks/` | 运行 `npx husky init` 或 `pre-commit install` |
| "Permission denied" | Hook 文件不可执行 | `chmod +x .husky/pre-commit` |
| Hooks 运行但不是预期的 | 旧配置残留 | 删除 `.git/hooks/` 内容后重新安装 |
| 本地正常，CI 失败 | Node/Python 版本不一致 | 在 CI 配置中固定版本 |

### 性能问题

```json
// ❌ Slow: runs on ALL files every commit
{
  "scripts": {
    "precommit": "eslint src/ && prettier --write src/"
  }
}

// ✅ Fast: lint-staged runs ONLY on staged files
{
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix", "prettier --write"]
  }
}
```

### 绕过 Hooks（必要时）

```bash
# Skip all hooks for a single commit
git commit --no-verify -m "wip: quick save"

# Skip pre-push only
git push --no-verify

# Skip specific pre-commit hooks
SKIP=eslint git commit -m "fix: update config"
```

> **警告**：绕过 hooks 应该是罕见情况。如果团队频繁绕过，说明 hooks 太慢或太严格——修复它们。

## 迁移指南

### Husky v4 → v9 迁移

```bash
# 1. Remove old Husky
npm uninstall husky
rm -rf .husky

# 2. Remove old config from package.json
# Delete "husky": { "hooks": { ... } } section

# 3. Install fresh
npm install --save-dev husky
npx husky init

# 4. Recreate hooks
echo "npx lint-staged" > .husky/pre-commit
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg

# 5. Clean up — old Husky used package.json config,
#    new Husky uses .husky/ directory with plain scripts
```

### 在现有项目中采用 Hooks

```bash
# Step 1: Start with formatting only (low friction)
# lint-staged config:
{ "*.{js,ts}": ["prettier --write"] }

# Step 2: Add linting after team adjusts (1-2 weeks later)
{ "*.{js,ts}": ["eslint --fix", "prettier --write"] }

# Step 3: Add commit message linting
# Step 4: Add pre-push test runner

# Gradual adoption prevents team resistance
```

## 核心原则

- **仅处理暂存文件**——永远不要在每次提交时 lint 整个代码库
- **尽可能自动修复**——`--fix` 标志减少开发者摩擦
- **快速 hooks**——pre-commit 应在 5 秒内完成
- **明确报错**——清晰的错误信息，提供可执行的修复建议
- **团队共享**——使用 Husky 或 `core.hooksPath` 使 hooks 受版本控制
- **CI 作为备份**——hooks 是便利；CI 才是强制执行者
- **渐进式采用**——从格式化开始，再添加 lint，最后是测试

## 相关技能

- `@codebase-audit-pre-push` - GitHub 推送前深度审计
- `@verification-before-completion` - 声称完成前的验证
- `@bash-pro` - 用于自定义 hooks 的高级 shell 脚本
- `@github-actions-templates` - CI/CD 工作流模板

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
