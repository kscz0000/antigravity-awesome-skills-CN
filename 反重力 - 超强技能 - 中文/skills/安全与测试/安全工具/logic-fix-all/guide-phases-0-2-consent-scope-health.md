# Logic-Lens — 逻辑全修 — 阶段 0-2（确认 · 范围 · 健康检查）

---

## 阶段 0 — 预检通知与确认门控

0a. 估算文件数量（git 仓库使用 `git ls-files | wc -l`；否则使用 `find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/target/*' -not -path '*/.venv/*' -not -path '*/build/*' -not -path '*/dist/*' -not -path '*/vendor/*' | wc -l`）。逐字显示以下通知并填入估算值——不得改写：

```
⚠️  /logic-fix-all — Full Repository Logic Audit & Fix

Scope:    ENTIRE repository, not just recent commits or staged changes.
          Includes runtime-affecting files: source code, runtime
          config (.json/.yaml/.toml/.ini), constraint files
          (CLAUDE.md, .logic-lens.yaml, AGENTS.md, etc.), and
          behavioral documentation (README, ARCHITECTURE, ADRs).
          Auto-excludes .git, build artifacts, dependency caches,
          binary assets; respects .gitignore and .logic-lens.yaml
          `ignore:` patterns.
Estimated files to scan: ~N

Method:   Semi-formal execution tracing — Premises → Trace →
          Divergence → Remedy. This is a LOGIC review, not a
          syntax/style/lint pass.

Skills:   logic-health → logic-review → logic-locate → logic-explain
          → logic-diff, iterated until clean.

Token cost: HIGH. The pipeline uses ranked passes and scope caps, but
deep tracing still costs roughly 5k–15k tokens per reviewed file
(more for deeply interprocedural code, less for stateless utilities),
times ~1.3 for iteration rounds.
Your estimate: min(N, 100) reviewed files × ~10k tokens × 1.3 ≈
(compute and show here, e.g. "~1M tokens").

Git impact: The pipeline edits source files. It does NOT commit,
push, or amend. If you have uncommitted work, commit or stash first.

Iteration: Critical findings loop until resolved (no cap). Warnings
and Suggestions default to 3 rounds, configurable via
`.logic-lens.yaml` `fix_all.max_iterations:`.

Proceed with full autonomous run? [Y/n]
```

0b. 解析用户回复。维护两个阶段局部计数器（阶段 0 退出时重置）：`consecutive_pauses`、`consecutive_questions`。

信号集（不区分大小写）：
- **确认：** `Y`、`yes`、`ok`、`sure`、`proceed`、`go`、`continue`、`继续`、`好`、`好的`、`行`、`可以`
- **硬否定：** `no`、`n`、`abort`、`cancel`、`取消`、`don't`、`不要`
- **软暂停：** `wait`、`hold on`、`not yet`、`一下`、`先别`、`等一下`、`等我`、`let me`

决策规则（首次匹配生效）：
1. 硬否定 → 中止："Aborted by user before scan — no files modified"。
2. 确认 + 软暂停 → 递增 `consecutive_pauses`，一行确认后等待下一条消息。若 `consecutive_pauses` 将达到 3，重新显示完整阶段 0 通知并重置为 0。
3. 确认（无否定）→ 继续。在一行确认中遵循任何范围/语言指令。
4. 提问 → 递增 `consecutive_questions`，回答一次，重新提示。若 `consecutive_questions` 将达到 2，降级至规则 5。
5. 未匹配（或从规则 4 降级）→ 重新显示通知一次；若下一条回复仍未匹配，视为中止。

0c. 确认后，在阶段 8 上限升级之前不再提问。

---

## 阶段 1 — 范围枚举

1a. 读取 `.logic-lens.yaml`（如存在）：仅加载 `ignore`、`focus`、`disable`、`custom_risks`、`severity:`、`trace.*` 和 `fix_all.max_iterations`。立即应用 `ignore`。

1b. 从标记文件检测项目类型并推导排除规则：
- `package.json` → 排除 `node_modules/`、`dist/`、`build/`、`.next/`、`.nuxt/`、`coverage/`
- `Cargo.toml` → 排除 `target/`
- `go.mod` → 排除 `vendor/`（除非项目自有——检查 `modules.txt`）
- `pyproject.toml`/`requirements.txt`/`Pipfile` → 排除 `.venv/`、`venv/`、`__pycache__/`、`*.egg-info/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/`
- `Gemfile` → 排除 `vendor/bundle/`
- `pom.xml` → 排除 `target/`
- `build.gradle`/`build.gradle.kts` → 排除 `build/`、`.gradle/`
- `build.sbt` → 排除 `target/`、`project/target/`
- `mix.exs` → 排除 `_build/`、`deps/`
- `composer.json` → 排除 `vendor/`
- `*.csproj`/`*.sln` → 排除 `bin/`、`obj/`
- `pubspec.yaml` → 排除 `.dart_tool/`、`build/`
- 始终排除：`.git/`、`.DS_Store`、锁文件（`*.lock`、`package-lock.json`、`yarn.lock`、`Pipfile.lock`、`poetry.lock`、`Cargo.lock`、`go.sum`）、日志文件、二进制文件（`.png/.jpg/.gif/.pdf/.wasm/.zip/.tar/.gz/.woff*/.ttf`）
- 将 `.gitignore` 作为提示而非绝对规则——某些被忽略的路径可能仍然相关。

1c. 将每个未排除的文件归入恰好一个类别：
- **源码：** 扩展名匹配项目所用语言的文件（从 1b 中的标记推断）。
- **运行时配置：** `.json`、`.yaml/.yml`、`.toml`、`.ini`、`.conf`、`*.config.js/ts`——分类前需在代码库中 grep 文件名验证。
- **约束文件：** 每一级的 `CLAUDE.md`、`.logic-lens.yaml`、`AGENTS.md`、`GEMINI.md`、schema 文件（`*.schema.json`、`openapi.yaml`、`*.proto`、`*.graphql`）。
- **行为文档：** `README.md`、`CONTRIBUTING.md`、`ARCHITECTURE.md`、描述运行时行为的 `docs/**/*.md`、`.env.example`。跳过变更日志、许可证、营销文案、`.editorconfig`。

1d. 按风险层级分类每个文件：
- **高：** 公共 API 接口；最近 30 天内变更的文件（`git log --since=30.days --name-only --pretty=format: | sort -u`）；无测试覆盖的核心业务逻辑。
- **中：** 工具模块、辅助函数、非核心配置、稳定的约束文件。
- **低：** 稳定且经过良好测试的代码、稳定的文档。

新增文件默认为高。约束/行为文档文件默认为中，若被最近变更的代码引用则升级为高。当文件匹配多个标准时，分配最高层级。

1e. 排序：高 → 中 → 低；每个层级内按行数降序。

1f. 范围上限：
- **>20 个文件：** 低层级文件以降低深度审查（仅前 3 个非平凡函数）。
- **>100 个文件：** 仅保留按（层级降序、行数降序）排名的前 100 个；丢弃其余。在修复报告中注明截断。

1g. 在修复报告开头陈述最终文件列表：文件名 + 层级 + 角色。

---

## 阶段 2 — 健康检查（logic-health）

2a. 对阶段 1 文件列表应用 `../logic-health/logic-health-guide.md` 方法论，包括其模块/函数预算。输出：每模块 Logic Score、按 L-code 汇总的发现、系统性模式。

2b. 记录阶段 2 输出供参考。暂不编写补救——健康检查提供形态，而非精度。精确发现来自阶段 3。

2c. 若健康检查揭示系统性模式（同一 L-code 出现在 4+ 个模块中），标记代表性文件作为阶段 3 优先审查对象。阶段 3 必须在模式可进入阶段 6 作为修复候选之前，产出完整的 Premises→Trace→Divergence 三元组——没有追踪的系统性观察不能成为补救的依据。
