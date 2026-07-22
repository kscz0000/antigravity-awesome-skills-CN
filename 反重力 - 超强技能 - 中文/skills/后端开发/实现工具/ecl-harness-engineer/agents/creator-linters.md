# Linter 创建智能体

你正在为智能体 harness 基础设施创建或更新 linter 脚本。

## 输入

你将收到：
- 完整层级层次结构的架构分析（来自 `harness/.analysis/architecture.json`）
- 现有 linter 状态（来自 `harness/.analysis/audit.json`）
- 要创建/更新的差异列表

## 你创建/更新的文件

### scripts/lint-deps.{ext}

**目的**：强制层级边界 —— 防止禁止的导入。

**必须包括**：
- 包含架构分析中**每个**包的完整层级映射
- 没有盲点 —— 如果包存在，它必须在层级映射中
- 层级规则：第 N 层只能从层数 < N 的层导入

**错误消息格式**（智能体可操作的）：

```
{file}:{line} imports {forbidden_package} (layer {N} → layer {M}).
Layer {N} packages can only import from layers < {N}.

Fix options:
1. Move {logic description} to a higher layer (e.g., {suggestion})
2. Pass the value as a parameter instead of importing directly
3. Define an interface in layer {N} and implement in layer {M}
```

这是最重要的质量要求。仅说 "Forbidden import" 的错误消息对智能体毫无用处。消息必须告诉 WHAT 错了、WHY 重要和 HOW 修复。

### scripts/lint-quality.{ext}

**目的**：强制代码质量模式。

**通用规则**（根据代码库模式自定义）：
- 文件大小限制（例如 > 500 行 → 警告）
- 结构化日志强制
- 错误包装约定
- 命名约定
- 测试文件存在

**相同的错误消息质量**：WHAT + WHY + HOW。

### scripts/lint-ecl.{ps1|sh|mjs|py}

**目的**：强制 ECL 变更生命周期完整性。

**必须检查**：
- 当存在激活变更时，`harness/changes/active/` 具有 `summary.md`、`spec.md`、`plan.md`、`tasks.md` 和 `reviews/`。
- Markdown front matter 状态在内部一致。
- 处于 `implement`、`validate` 或 `done` 阶段的激活变更在 `spec.md` 中没有高影响力
  `[NEEDS CLARIFICATION: ...]` 标记。
- 激活变更在 `summary.md` 中 `plan_review` 被批准或
  `reviews/review.md` 中存在等效的已批准计划审查之前不能进入实施。
- `tasks.md` 中的可执行任务行使用 `T###` id，且实施任务包括目标路径
  和验证备注。
- `completed` 变更具有验证结果。
- 具有未解释的待办项的 `tasks.md` 不能被完成。
- ECL 启用的项目存在 `docs/STATUS.md` 并清楚说明激活变更文件覆盖它。
- 临时重新生成的索引与 `harness/changes/INDEX.json` 匹配；否则失败并告诉用户运行生成的 `scripts/harness-change.* reindex` 等效命令。
- `scripts/harness-evolve.*` 和 `harness/evolution/state.json` 存在以用于核心自动演化阈值检查。
- 如果 `harness/evolution/pending.md` 存在，lint 可以将其报告为 pending 上下文，但不得自动应用或删除它。

### scripts/lint-encoding.{ps1|sh|mjs|py}

**目的**：强制 UTF-8 并防止将乱码写入源或文档。

**必须检查**：
- 扫描文本文件中的 `references/ecl-harness.md` 中列出的已知乱码标记。
- 排除 generated/vendor/cache 目录。
- 返回可操作的文件和行消息。

## 语言特定模板

使用 `references/linter-templates.md` 中的模板作为起点，然后自定义：

- **Go**：解析导入的 Go 脚本，针对层级映射进行检查
- **TypeScript/Node.js**：首先读取 `references/adapters/typescript.md`；生成 Node/TS 原生脚本，例如 `scripts/lint-deps.mjs` 和 `scripts/lint-quality.mjs`，并通过 npm/包管理器脚本连接它们
- **Python**：解析 from/import 语句的 Python 脚本
- **ECL/Encoding**：使用 `references/ecl-harness.md` 中所选的命令界面 profile（`.ps1`、`.sh`、`.mjs` 或 `.py`）

## 关键规则

1. **需要首日通过**：linter **必须**在当前代码库上无错误地通过。如果代码库存在现有违规，请在 `docs/exec-plans/tech-debt-tracker.md` 中记录它们，而不是让 linter 失败。

2. **完整覆盖**：代码库中的每个包都必须出现在层级映射中。缺失的包 = 盲点 = 未检测到的违规。

3. **可执行**：脚本必须从项目根目录运行。Bash/Node/Python 脚本在环境支持文件模式时应可执行；仅限 Windows 的 profiles 可以使用显式的解释器命令。

4. **Makefile 集成**：确保 `make lint-arch` 目标运行这些脚本。

5. **生成的索引、演化和交接规范**：`lint-ecl` 验证 `INDEX.json` 新鲜度、自动演化状态存在性和 `docs/STATUS.md` 存在性，但从不重写这些文件。重写属于生成的 `harness-change reindex`、`harness-evolve check/mark-complete` 和显式的智能体/人工交接更新。

6. **命令界面一致性**：根据项目证据自动选择脚本 profile。如果项目拒绝 `.ps1`，则不要将 PowerShell 作为唯一的入口点。对于使用 Bash 的 Windows 项目，记录 Git Bash、WSL、MSYS2 或 CI Linux shell 作为先决条件。如果选择了 PowerShell profile，脚本必须在 Windows PowerShell 5.1 和 PowerShell 7 上运行。

7. **严格的业务闸门**：不要删除或削弱现有项目的 `lint`、`typecheck`、`test`、
   或 `build` 检查以使 CI 通过。如果那些检查在 harness 创建之前失败，将其报告为预先存在的项目债；除非用户明确要求分阶段发布，否则保持生成的 CI 严格。

## 验证

创建 linter 后，验证：

```bash
# Linters are executable
chmod +x scripts/lint-deps* scripts/lint-quality*

# Linters pass on current codebase
make lint-arch

# ECL and encoding checks pass
{ecl_lint_command}
{encoding_lint_command}

# Count covered packages vs total packages
# (should be 100%)
```