# 冲突解决操作手册

在收集仓库事实后使用本手册。目标是在保留 schema 意图的同时，用基于合并后 schema 重新生成的迁移，替换过期的已生成迁移产物。

## 决策树

1. 仓库当前是否处于合并或变基状态？
   - 运行 `git status --short` 和 `git ls-files -u`。
   - 如果是，需识别：用户是将父分支合入功能分支、对功能分支变基，还是将功能分支合入父分支。
2. 当前存在哪种迁移结构？
   - 旧式：`meta/_journal.json`、`meta/*_snapshot.json`、根目录 SQL 文件。
   - 目录式：每个迁移是一个目录，其中包含 `migration.sql` 和 `snapshot.json`。
   - 混合或未知：停止并询问预期的迁移输出路径。
   - 过渡期（旧式产物 + 部分目录式迁移）：在用户确认目标结构前不要修复。仅在明确最终目标结构后，才将旧式产物与目录式产物视为同一逻辑历史；否则修复可能丢弃错误的一侧。
3. schema 源文件是否已解决？
   - 如未解决，先解决再继续，否则告知用户尚不能安全地重新生成迁移。
4. 用户要求的是诊断还是修复？
   - 诊断保持只读。
   - 修复只有在明确要丢弃的生成文件后才能包含文件变更。

## 只读检查命令

```bash
git status --short
git ls-files -u
rg --files -g 'drizzle.config.*' -g 'package.json'
rg -n "drizzle-kit|drizzle-orm|db:generate|db:check|migrate" package.json pnpm-lock.yaml yarn.lock package-lock.json 2>/dev/null
python3 <skill-dir>/scripts/check_drizzle_migrations.py --root .
```

如果 `rg` 不可用，使用等效的 `find` 和 `grep`。在运行辅助脚本前，将 `<skill-dir>` 解析为已安装的技能目录。按顺序检查并使用第一个包含 `scripts/check_drizzle_migrations.py` 的目录：目标仓库内置的 `skills/drizzle-migration-conflict`，然后是 `~/.claude/skills/drizzle-migration-conflict`，再然后是用户报告的安装位置。如果都不存在，回退到上面的 `git`/`rg` 检查命令，并告知用户未找到辅助脚本。

## 旧式结构修复

旧式 Drizzle 输出的典型结构如下：

```text
drizzle/
  0000_initial.sql
  0001_add_user.sql
  meta/
    _journal.json
    0000_snapshot.json
    0001_snapshot.json
```

针对从父分支更新后的功能分支的安全流程：

1. 先解决 schema 源码冲突。
2. 以父分支的迁移历史作为基线。
3. 丢弃从功能分支自分支分歧以来创建的已生成迁移文件。
4. 从 `package.json` 重新运行项目认可的 `drizzle-kit generate` 脚本。
5. 校验重新生成的历史。

除非用户明确要求紧急手工修复并接受风险，否则不要手工编辑 `_journal.json` 或快照 JSON。下一条生成的迁移依赖这些快照。

### Ours/theirs 警告

`ours` 和 `theirs` 的含义会随合并方向而变化：

| 场景 | `ours` 通常指 | `theirs` 通常指 | 安全建议 |
| --- | --- | --- | --- |
| 在功能分支上，将父分支合入其中 | 当前功能分支 | 正被合入的父分支 | 父分支通常为 `theirs`，但 checkout 前请核对。 |
| 在父分支上，将功能分支合入其中 | 当前父分支 | 功能分支 | 父分支通常为 `ours`，但 checkout 前请核对。 |
| 变基 | 含义可能不直观 | 含义可能不直观 | 避免使用简写；尽量用显式的分支/路径恢复。 |

存疑时，询问哪个分支应作为迁移历史的真源。不要猜测。

## 目录式结构修复

目录式 Drizzle 输出的典型结构如下：

```text
drizzle/
  20260618120000_add_user/
    migration.sql
    snapshot.json
```

安全流程：

1. 先审查 Drizzle 配置和环境，再在仅使用非生产目标的前提下运行 `drizzle-kit check` 或封装它的项目脚本。
2. 如果它报告非可交换迁移冲突，识别冲突的迁移以及依赖它的所有后续迁移。
3. 仅在用户确认后，移除或重新生成位于该冲突下游的已生成迁移产物。
4. 基于合并后的 schema 重新运行 `drizzle-kit generate`。
5. 再次运行辅助脚本，并仅在确认配置/环境目标仍为非生产后再次运行 `drizzle-kit check`。

仅在确认属于已知误报（迁移实际可交换，或检查本身有误）时使用 `--ignore-conflicts`，并将该决策写入报告。

## 重新生成后的校验

按层级校验，避免智能体意外触及生产数据库或运行任意项目脚本。

### 无数据库的检查

```bash
python3 <skill-dir>/scripts/check_drizzle_migrations.py --root . --migrations-dir <migration-dir>
```

### 会加载项目配置或环境的检查

在审查 `drizzle.config.*`、包脚本和相关环境变量后，再运行 `drizzle-kit check`。在执行前确认任何数据库 URL 或凭据指向的是非生产或可丢弃目标。运行该命令前，请按以下清单逐项确认：

1. 阅读 `drizzle.config.*`，注意其中的 `url`、`dbCredentials`、`credentials` 或连接字段。判断它们是字面量、从 `process.env` 读取，还是通过 `dotenv` 加载。
2. 识别为这些字段提供值的环境变量（常见名称：`DATABASE_URL`、`DB_URL`、`POSTGRES_URL`、`DRIZZLE_DATABASE_URL`）。在不回显密钥的前提下，检查 `.env`、`.env.local` 和包脚本环境中的对应值。
3. 如果某值指向生产主机（命名为 `prod`/`production`、托管集群端点，或用户指明为在线的主机），停下来并请求可丢弃目标，不要运行检查。
4. 如果 `drizzle-kit check` 因所配置 dialect 而需要真实连接，优先用可丢弃/本地数据库内联覆盖该 URL，或使用禁用连接的配置（部分 dialect 允许仅做 schema 检查）。如果两者都不可行，则回退到无数据库的辅助脚本，并报告 `drizzle-kit check` 无法安全运行。
5. 仅在确认目标为非生产环境后，才运行项目认可的检查命令。

```bash
# Project script names vary; inspect package.json first.
# Override with a disposable DATABASE_URL only if the config requires a connection.
DATABASE_URL=postgres://localhost/disposable pnpm exec drizzle-kit check --config <drizzle-config>
```

### 项目测试

只有在审查脚本定义后才运行类型检查或测试。测试可能执行迁移、连接数据库、修改 fixture 或启动服务。

```bash
pnpm typecheck
pnpm test
```

除非用户指明可丢弃数据库或明确要求执行迁移，否则避免对生产数据库执行任何命令。

## 反模式

- 在生产环境中运行 `drizzle-kit push` 来绕过迁移历史。
- 同时保留两侧已生成的迁移并手工重新编号文件，而不基于合并后的 schema 重新生成。
- 在未核对 SQL 与快照配对的情况下，通过接受两侧来"解决" `_journal.json`。
- 在未理解合并方向的情况下使用 `git checkout --theirs drizzle/`。
- 将 `drizzle-kit check --ignore-conflicts` 作为团队默认工作流。
