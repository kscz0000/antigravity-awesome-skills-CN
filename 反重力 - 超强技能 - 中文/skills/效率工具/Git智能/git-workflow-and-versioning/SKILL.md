---
name: git-workflow-and-versioning
description: 规范化 Git 工作流实践。任何代码变更、提交、分支、解决冲突或需要组织多条并行工作时使用。涉及 git 工作流、提交规范、分支策略、worktree、trunk-based 开发、版本控制时使用。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/git-workflow-and-versioning
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# Git 工作流与版本控制

## 概述

Git 是你的安全网。把 commit 当作存档点，把 branch 当作沙盒，把 history 当作文档。在 AI 智能体高速生成代码的时代,严谨的版本控制是让变更保持可管理、可审查、可回滚的机制。

## 何时使用

任何时候。每次代码变更都要经过 git。

## 核心原则

### Trunk-Based 开发（推荐）

保持 `main` 随时可部署。在短生命周期特性分支中工作,1-3 天内合并回主干。长生命周期的开发分支是隐性成本——它们会分叉、产生合并冲突、延迟集成。DORA 研究持续表明 trunk-based 开发与高绩效工程团队正相关。

```
main ──●──●──●──●──●──●──●──●──●──  (always deployable)
        ╲      ╱  ╲    ╱
         ●──●─╱    ●──╱    ← short-lived feature branches (1-3 days)
```

这是推荐默认做法。使用 gitflow 或长生命周期分支的团队可以将这些原则（原子提交、小改动、清晰的描述信息）适配到自己的分支模型——commit 的纪律性比具体的分支策略更重要。

- **开发分支是成本。** 分支每多存活一天,就累积一天的合并风险。
- **发布分支可以接受。** 当你需要在 main 向前推进的同时稳定某个发布版本时。
- **特性开关优于长分支。** 优先用开关部署未完成的工作,而不是让它在分支上停留数周。

### 1. 尽早提交,频繁提交

每个成功的小增量都单独提交。不要累积大量未提交的更改。

```
Work pattern:
  Implement slice → Test → Verify → Commit → Next slice

Not this:
  Implement everything → Hope it works → Giant commit
```

Commit 就是存档点。如果下一次改动破坏了什么,你可以立刻回退到上一个已知良好的状态。

### 2. 原子提交

每个 commit 只做一件逻辑上的事:

```
# Good: Each commit is self-contained
git log --oneline
a1b2c3d Add task creation endpoint with validation
d4e5f6g Add task creation form component
h7i8j9k Connect form to API and add loading state
m1n2o3p Add task creation tests (unit + integration)

# Bad: Everything mixed together
git log --oneline
x1y2z3a Add task feature, fix sidebar, update deps, refactor utils
```

### 3. 清晰的提交说明

Commit 信息解释的是*为什么*,而不仅仅是*做了什么*:

```
# Good: Explains intent
feat: add email validation to registration endpoint

Prevents invalid email formats from reaching the database.
Uses Zod schema validation at the route handler level,
consistent with existing validation patterns in auth.ts.

# Bad: Describes what's obvious from the diff
update auth.ts
```

**格式:**
```
<type>: <short description>

<optional body explaining why, not what>
```

**类型:**
- `feat` — 新特性
- `fix` — Bug 修复
- `refactor` — 既不修 bug 也不加新功能的代码变更
- `test` — 新增或更新测试
- `docs` — 仅文档变更
- `chore` — 工具、依赖、配置

### 4. 关注点分离

不要把格式变更和功能变更混在一起。不要把重构和新特性混在一起。每种类型的变更应该是独立的 commit——理想情况下也是独立的 PR:

```
# Good: Separate concerns
git commit -m "refactor: extract validation logic to shared utility"
git commit -m "feat: add phone number validation to registration"

# Bad: Mixed concerns
git commit -m "refactor validation and add phone number field"
```

**把重构和功能工作分开。** 重构变更和功能变更是两种不同的变更——分开提交。这样每种变更都更容易审查、回退,在历史中更易理解。小清理（如重命名变量）可以由审查者酌情纳入功能 commit。

### 5. 控制变更规模

每个 commit/PR 目标约 100 行。超过 1000 行的变更应该拆分。大型变更的拆分策略参见 `code-review-and-quality`。

```
~100 lines  → Easy to review, easy to revert
~300 lines  → Acceptable for a single logical change
~1000 lines → Split into smaller changes
```

## 分支策略

### 特性分支

```
main (always deployable)
  │
  ├── feature/task-creation    ← One feature per branch
  ├── feature/user-settings    ← Parallel work
  └── fix/duplicate-tasks      ← Bug fixes
```

- 从 `main`（或团队默认分支）拉出
- 保持分支短生命周期（1-3 天内合并）——长生命周期分支是隐性成本
- 合并后删除分支
- 对未完成的特性,优先用特性开关,而不是长生命周期分支

### 分支命名

```
feature/<short-description>   → feature/task-creation
fix/<short-description>       → fix/duplicate-tasks
chore/<short-description>     → chore/update-deps
refactor/<short-description>  → refactor/auth-module
```

## 使用 Worktree

对于并行 AI 智能体工作,使用 git worktree 同时运行多个分支:

```bash
# Create a worktree for a feature branch
git worktree add ../project-feature-a feature/task-creation
git worktree add ../project-feature-b feature/user-settings

# Each worktree is a separate directory with its own branch
# Agents can work in parallel without interfering
ls ../
  project/              ← main branch
  project-feature-a/    ← task-creation branch
  project-feature-b/    ← user-settings branch

# When done, merge and clean up
git worktree remove ../project-feature-a
```

好处:
- 多个智能体可以同时在不同特性上工作
- 无需切换分支（每个目录都有自己的分支）
- 如果某个实验失败,删除 worktree 即可——没有任何损失
- 变更保持隔离,直到显式合并

## 存档点模式

```
Agent starts work
    │
    ├── Makes a change
    │   ├── Test passes? → Commit → Continue
    │   └── Test fails? → Revert to last commit → Investigate
    │
    ├── Makes another change
    │   ├── Test passes? → Commit → Continue
    │   └── Test fails? → Revert to last commit → Investigate
    │
    └── Feature complete → All commits form a clean history
```

这种模式意味着你最多只会丢失一个增量的工作。如果智能体失控,`git reset --hard HEAD` 让你立刻回到上一次成功状态。

## 变更摘要

任何修改之后,提供结构化的摘要。这让审查更容易,记录了范围纪律,并暴露出非预期的变更:

```
CHANGES MADE:
- src/routes/tasks.ts: Added validation middleware to POST endpoint
- src/lib/validation.ts: Added TaskCreateSchema using Zod

THINGS I DIDN'T TOUCH (intentionally):
- src/routes/auth.ts: Has similar validation gap but out of scope
- src/middleware/error.ts: Error format could be improved (separate task)

POTENTIAL CONCERNS:
- The Zod schema is strict — rejects extra fields. Confirm this is desired.
- Added zod as a dependency (72KB gzipped) — already in package.json
```

这种模式能在早期发现错误假设,并为审查者提供清晰的变更地图。"未触碰"部分尤其重要——它表明你行使了范围纪律,没有进行未经请求的翻新。

## 提交前卫生检查

每次提交前:

```bash
# 1. Check what you're about to commit
git diff --staged

# 2. Ensure no secrets
git diff --staged | grep -i "password\|secret\|api_key\|token"

# 3. Run tests
npm test

# 4. Run linting
npm run lint

# 5. Run type checking
npx tsc --noEmit
```

用 git hooks 自动化:

```json
// package.json (using lint-staged + husky)
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

## 处理生成文件

- **提交生成文件**仅在项目预期这样做时（如 `package-lock.json`、Prisma 迁移）
- **不要提交**构建产物（`dist/`、`.next/`）、环境文件（`.env`）或 IDE 配置（`.vscode/settings.json`,除非是团队共享）
- **维护 `.gitignore`**,涵盖: `node_modules/`、`dist/`、`.env`、`.env.local`、`*.pem`

## 用 Git 调试

```bash
# Find which commit introduced a bug
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Git checkouts midpoints; run your test at each to narrow down

# View what changed recently
git log --oneline -20
git diff HEAD~5..HEAD -- src/

# Find who last changed a specific line
git blame src/services/task.ts

# Search commit messages for a keyword
git log --grep="validation" --oneline
```

## 常见借口

| 借口 | 现实 |
|---|---|
| "等我做完这个特性再提交" | 一个巨大的 commit 无法审查、调试或回退。每完成一个小切片就提交。 |
| "提交信息不重要" | 提交信息就是文档。未来的你（和未来的智能体）需要理解改了什么以及为什么改。 |
| "我之后用 squash 合并" | Squash 会破坏开发叙事。最好从一开始就保持干净的增量提交。 |
| "分支会增加开销" | 短生命周期分支是免费的,可以防止冲突的工作相互碰撞。长生命周期分支才是问题——1-3 天内合并。 |
| "我之后再拆分这个变更" | 大变更更难审查、部署风险更高、回退更难。提交前拆分,而不是提交后。 |
| "我不需要 `.gitignore`" | 等到生产密钥的 `.env` 被提交时就晚了。立刻设置它。 |

## 红旗警告

- 大量未提交的更改不断累积
- 提交信息形如 "fix"、"update"、"misc"
- 格式变更与功能变更混在一起
- 项目中没有 `.gitignore`
- 提交了 `node_modules/`、`.env` 或构建产物
- 长生命周期分支与 main 严重偏离
- 强制推送到共享分支

## 验证

每次 commit:

- [ ] Commit 只做一件逻辑上的事
- [ ] 提交信息解释为什么,遵循类型约定
- [ ] 提交前测试通过
- [ ] diff 中无密钥
- [ ] 没有纯格式变更与功能变更混在一起
- [ ] `.gitignore` 涵盖标准排除项

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时,使用此技能。
- 在应用变更前,验证命令、生成的代码、依赖、凭证和外部服务行为。
- 不要把示例当作特定环境测试、安全审查或用户对破坏性/高代价操作的批准的替代。