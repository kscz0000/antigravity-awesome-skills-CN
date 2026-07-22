---
name: drizzle-migration-conflict
description: "诊断、修复并预防 Drizzle Kit 迁移冲突，涵盖生成的 SQL、快照、迁移日志、合并队列及团队工作流。涉及迁移冲突、drizzle-kit 冲突、schema 合并、迁移修复、合并队列策略等场景时使用此技能。"
category: databases
risk: critical
source: community
source_repo: chaunsin/agent-skills
source_type: community
date_added: "2026-06-29"
author: chaunsin
tags: [drizzle, migrations, database, ci, merge-conflicts]
tools: [git, python, rg]
license: "Apache-2.0"
license_source: "https://github.com/chaunsin/agent-skills/blob/master/LICENSE"
---

# Drizzle 迁移冲突

使用本技能帮助用户在多人协作仓库中诊断、修复并预防 Drizzle Kit 迁移冲突。由于 Drizzle 迁移同时编码了 SQL 和迁移快照，安全方案取决于当前的迁移目录结构、Drizzle Kit 版本以及 git 状态。

## 适用场景

- 在拉取、合并、变基或更新 PR 后，Drizzle 迁移文件、`_journal.json` 或 `snapshot.json` 发生冲突时使用。
- 当 `drizzle-kit check` 报告非可交换（non-commutative）迁移或迁移目录冲突时使用。
- 当团队希望在 schema 变更合并后，为生成的 Drizzle 迁移提供安全的修复流程时使用。
- 当设计 CI 或合并队列策略以防止反复出现 Drizzle 迁移冲突时使用。

## 安全规则

- 除非用户明确要求修复文件，否则以只读诊断模式开始。
- 除非用户明确请求且目标清晰，否则不要运行 `drizzle-kit migrate`、`drizzle-kit push`、数据库 seed 脚本或任何连接到生产数据库的命令。
- 将 `drizzle-kit check`、项目的类型检查和测试视为可能加载项目配置、环境变量或脚本的命令执行。先审查脚本和配置，再要求显式的非生产或可丢弃目标，方可进行任何依赖数据库的校验。
- 除非用户已确认要修改的具体侧（side）和文件，否则不要删除迁移文件、重写 `_journal.json`，也不要运行 `git checkout --ours`、`git checkout --theirs`、`git restore` 或 `rm`。
- 不要将 `drizzle-kit push` 推荐为迁移冲突的生产解决方案；它会跳过团队所需的可审计迁移历史。
- 将 `--ignore-conflicts` 视为针对已知误报的特例，而非常规修复手段。
- 保留 schema 源代码改动，除非用户明确要求丢弃。冲突修复通常会丢弃已生成的迁移，并基于合并后的 schema 重新生成。
- 如果 `ours` 和 `theirs` 会因合并方向不同而指代不同分支，请在建议 checkout 命令前请用户指明父分支。

## 必读参考资料

- 当答案依赖当前 Drizzle 行为、官方指引或某个保留的外部链接时，请阅读 `references/sources.md`。
- 在推荐修复流程前，请阅读 `references/conflict-resolution.md`。
- 在提出 CI、合并队列或团队工作流变更建议前，请阅读 `references/ci-policy.md`。
- 在编写诊断报告前，请阅读 `references/report-template.md`。

## 来源参考

官方文档、Drizzle GitHub 讨论、社区脚本和合并队列参考的完整列表位于 `references/sources.md`，并附有可信度等级和注意事项。只要答案依赖当前 Drizzle 行为，就应阅读该文件。当项目 `drizzle-kit` 主版本变更时，请重新核对官方文档和最相关的讨论，因为迁移内部实现（快照格式、迁移日志结构、`drizzle-kit check` 语义）在各版本之间已有变动。

## 模式选择

先对任务分类：

1. **诊断（Diagnose）** — 用户遇到冲突或 `drizzle-kit check` 失败，希望理解原因。
2. **修复（Repair）** — 用户明确要求修复或重新生成迁移文件。
3. **CI 加固（CI hardening）** — 用户希望防止 PR 或合并队列中未来再出现冲突。
4. **解释（Explain）** — 用户希望获得概念性解答或团队操作手册。

当模式未明确时，默认选择诊断。

每个模式解锁一组特定操作。未经显式升级，请勿跨模式越界：

- **诊断** — 仅只读。运行 `git status`、`git ls-files -u`、辅助脚本和文件检查。不要运行 `drizzle-kit check`、类型检查、测试或任何写命令。报告发现和拟定的修复路径，但不要执行。
- **修复** — 增加文件写入和 `drizzle-kit generate`/`check` 执行；每一步都要受安全规则约束，并需显式确认要修改的具体文件和分支侧（`ours`/`theirs`）。
- **CI 加固** — 增加提出或编辑 CI/工作流文件。不要针对用户的数据库运行迁移命令以校验工作流；只校验工作流的语法和逻辑。
- **解释** — 仅概念性。除可选的只读检查外，不对仓库执行任何命令。

## 仓库探查

在给出命令前先收集仓库事实：

```bash
git status --short
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git ls-files -u
rg --files -g 'drizzle.config.*' -g 'package.json' -g 'pnpm-lock.yaml' -g 'yarn.lock' -g 'package-lock.json'
```

然后审查相关文件：

- `drizzle.config.*` 中的 `out`、`schema`、dialect 及配置结构。
- `package.json` 脚本中项目认可的 `generate`、`check` 和 `migrate` 命令。
- `package.json` 依赖项或锁文件片段中的 `drizzle-kit` 和 `drizzle-orm` 版本。
- 迁移输出目录，可从配置中读取，也可使用常见名称如 `drizzle/`、`migrations/` 或 `src/db/migrations/`。

如果本技能的辅助脚本可用，以只读模式运行：

```bash
python3 <skill-dir>/scripts/check_drizzle_migrations.py --root .
```

在运行前将 `<skill-dir>` 解析为已安装的技能目录。按顺序检查以下位置，使用第一个包含 `scripts/check_drizzle_migrations.py` 的目录：

1. 目标仓库内置副本：`<repo-root>/skills/drizzle-migration-conflict`。
2. Claude Code 技能目录：`~/.claude/skills/drizzle-migration-conflict`。
3. 用户环境报告的其他安装位置。

如果以上都不存在，则回退到上方的 `git`/`rg` 检查命令，并告知用户未找到辅助脚本。当项目有多个 Drizzle 配置或输出目录时，使用 `--config <file>` 和 `--migrations-dir <dir>`。该脚本从不连接数据库，也从不写文件；它只读取迁移目录并报告结构问题。

## 迁移结构判断

在提出修复方案前先确认结构：

- **旧式结构（Legacy）**：`<out>/meta/_journal.json`、`<out>/meta/*_snapshot.json` 以及位于根目录的迁移 SQL 文件，如 `<out>/0003_name.sql`。
- **目录式结构（Folder-based）**：每个迁移是一个目录，其中包含 `migration.sql` 和 `snapshot.json`。
- **未知或混合结构**：停止并报告歧义。不要猜测破坏性修复方案。

## 推荐修复原则

- 优先解决 schema 源码冲突。重新生成的迁移必须反映合并后的 schema，而不是某一侧的过期快照。
- 在从父分支更新后修复功能分支时，将父分支或目标分支的迁移历史视为唯一真源。
- 优先丢弃并重新生成已生成的迁移产物，而非手工编辑迁移日志或快照文件。
- 重新生成后，按层级校验：先做无数据库的结构检查；再在确认配置/环境不会指向生产环境后做 `drizzle-kit check`；最后在审查脚本和任何数据库目标后做项目测试。
- 如用户要求应用变更，请在执行写入前明确说明将修改哪些文件。

## 输出规则

- 在可行时使用用户的语言，但命令片段和文件路径保持原文。
- 说明检测到的迁移结构和所选模式。
- 将已确认的冲突与假设、缺失证据分开。
- 先给出安全默认路径，再提供可选的自动化或 CI 加固方案。
- 对破坏性步骤，标注为"需确认"并说明将丢失什么。
- 绝不回显密钥。在审查 `drizzle.config.*`、`.env` 或环境变量时，报告中不得包含数据库 URL、密码、令牌或连接字符串。引用时用 `<redacted>`，或仅描述其是否指向类生产目标。
- 诊断报告使用 `references/report-template.md` 中的结论值：`NO_CONFLICT_FOUND`、`SAFE_TO_REGENERATE`、`NEEDS_USER_CONFIRMATION` 或 `BLOCKED_BY_AMBIGUITY`。

## 局限性

- 本技能无法保证重新生成的迁移在生产中安全，除非针对目标数据库状态和部署流程进行过审查。
- 除非用户明确确认目标与命令，否则不会运行依赖数据库的迁移命令。
- 聚焦于 Drizzle Kit 迁移冲突，而非通用 schema 设计或应用查询优化。

## 测试提示语

用以下提示语校验技能行为：

- "我的 Drizzle `_journal.json` 和 `0003_snapshot.json` 在合并时冲突。告诉我该怎么办。"
- "我们升级到了迁移目录布局，`drizzle-kit check` 报告非可交换冲突。"
- "设计 CI，让我们的团队不再合并坏掉的 Drizzle 迁移。"
- "我能用 `drizzle-kit push` 解决生产环境中的 Drizzle 迁移冲突吗？"
- "用技能里的链接重新核对当前官方的 Drizzle 迁移冲突指引。"
- "我们正从旧式扁平布局迁移到目录式迁移，迁移到一半时遇到冲突怎么办？"
- "我们的 `drizzle.config.ts` 通过 `process.env.MIGRATIONS_DIR` 设置 `out`，辅助脚本提示找不到 out 目录。现在怎么办？"
- "`drizzle-kit check` 一直对一个我们确认可交换的迁移报错。我们能否始终加 `--ignore-conflicts`？"
