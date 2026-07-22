# CI 与团队策略

当用户希望在 pull request、受保护分支或 GitHub 合并队列中防止 Drizzle 迁移冲突时，参考本文档。

## 推荐层级

1. **本地开发者习惯**
   - 在生成迁移前先拉取或合并父分支。
   - 在 schema 源码冲突解决后再生成迁移。
   - 在确认 `drizzle-kit check` 的配置/环境不指向生产环境后，再运行 `drizzle-kit check`。
2. **Pull request 检查**
   - 运行项目常规的静态检查。
   - 用显式的非生产配置运行 `drizzle-kit check`，或运行 `package.json` 中封装该命令的脚本。
   - 运行只读辅助脚本，捕捉旧式迁移日志/快照不匹配问题。
3. **合并队列检查**
   - 如果启用了 GitHub 合并队列，在 `merge_group` 事件上运行同样的检查。
   - 不要假设 PR 检查通过就意味着队列中的合并结果仍无冲突。

## GitHub Actions 模板

请根据目标仓库调整包管理器、配置路径、迁移目录和脚本位置。辅助脚本必须先内置（vendored）或复制进仓库，CI 才能运行它。任何情况下都不要让 CI 的迁移检查指向生产凭据。

```yaml
name: drizzle-migration-check

on:
  pull_request:
  merge_group:

jobs:
  drizzle-migration-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - run: pnpm install --frozen-lockfile
      # Run only with a non-production or disposable DATABASE_URL if the config requires one.
      - run: pnpm exec drizzle-kit check --config drizzle.config.ts
      # Example assumes the helper was copied to scripts/check_drizzle_migrations.py.
      - run: python3 scripts/check_drizzle_migrations.py --root . --config drizzle.config.ts --migrations-dir drizzle
```

如果仓库没有内置本技能，请将辅助脚本复制进仓库，或在 CI 工具仓库中运行等效的只读检查。在多配置仓库中，为 Drizzle Kit 和辅助脚本传入相同的配置和匹配的迁移目录。

辅助脚本退出码为：`0` 表示所有检查目录均正常；`1` 表示发现错误或警告项；`2` 表示未发现任何迁移目录。运行该脚本的 CI 步骤在非零退出时应判定为失败，但仅当仓库本就不应包含 Drizzle 迁移时，才可将退出码 `2` 视为"无需检查"；否则退出码 `2` 通常意味着检测未找到迁移目录，应显式传入配置。

## 合并队列能解决与不能解决的问题

合并队列可以串行化最终的合并顺序并对临时合并结果进行测试。它不会重写 Drizzle 迁移、不会重新运行 `drizzle-kit generate`，也不会判断哪个分支的快照是正确的。当生成的迁移历史不一致时，检查应判定失败，再由开发者更新分支并重新生成迁移。

## 策略建议

- 要求每个 PR 在 schema 冲突解决后只生成一次迁移。
- 将迁移产物视为"已生成但可审查"的文件：不要在 CI 中静默重写它们。
- 在合并前要求运行 `drizzle-kit check` 或等效的冲突检查。
- 在旧式项目中，拒绝重复的迁移编号以及迁移日志/快照漂移。
- 在目录式项目中，拒绝不完整的迁移目录以及失败的可交换性检查。
- 将生产迁移执行与 PR 校验分开。

## 何时应让 CI 失败

当以下任一情况为真时让任务失败：

- `_journal.json` 包含重复的 `idx` 或 `tag` 值。
- 迁移日志条目引用了缺失的 SQL 文件或快照。
- 旧式输出中存在根目录的 SQL 或快照文件，但未被迁移日志引用。
- 迁移文件包含 Git 冲突标记。
- 目录式迁移目录缺少 `migration.sql` 或 `snapshot.json`。
- `drizzle-kit check` 报告非可交换迁移冲突。
