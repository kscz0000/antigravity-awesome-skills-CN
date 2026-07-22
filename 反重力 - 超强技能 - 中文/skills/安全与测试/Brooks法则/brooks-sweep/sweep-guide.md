# Brooks-Lint — 全量扫描指南

顺序自治流水线：**review → test → debt → audit**。就地修复发现的问题，
迭代直到干净或达到上限，报告残留项。仅有一个交互点：
步骤 0（预飞同意）—— 批准后流水线将自动运行直到步骤 8。

每个发现项遵循铁律：**症状 → 来源 → 后果 → 修复**。

---

### 步骤 0 — 预飞同意门

**目标：** 一开始就声明作用域、成本和不可逆性；获得一次性明确同意，
以便后续步骤不再询问。

0a. 在 git 仓库中使用 `git ls-files | wc -l` 估算文件数，否则使用
   `find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/build/*' -not -path '*/dist/*' -not -path '*/vendor/*' -not -path '*/target/*' | wc -l`。量级即可。

0b. 逐字显示此通知，并填入估算值。不要意译——
   用户同意的就是这个确切的作用域。

   ```
   ⚠️  /brooks-sweep — Full Repository Sweep & Auto-Fix

   Scope:    Four analysis dimensions run in sequence — PR code decay (R1–R6),
             test quality (T1–T6), tech debt, architecture. Edits are made in
             place inside the detected project scope.
   Estimated files in scope: ~N

   Order:    brooks-review → brooks-test → brooks-debt → brooks-audit.
             Each dimension scans, queues, and fixes before the next starts.

   Autonomy: Fully autonomous. Safe single-file fixes apply directly. Multi-file
             fixes that have test coverage AND do not break a public interface
             also apply directly. High-risk fixes (public API break, cross-module
             structural change, or no test coverage) are NOT applied — they are
             recorded in the residual report for human review.

   Iteration: After each dimension pass, modified files + same-module + static
             consumers are re-scanned. A finding that fails to fix 3 times is
             retired to the unresolvable set and never re-queued. Non-critical
             rounds cap at 3 iterations; critical findings iterate until
             resolved or retired.

   Git impact: The pipeline edits files. It does NOT commit, push, or amend.
             If you have uncommitted work you want to preserve, commit or stash
             first.

   Proceed with full autonomous sweep? [Y/n]
   ```

0c. 解析回复（首次匹配获胜，按顺序评估规则）：
   1. **硬否定**（`no`、`n`、`abort`、`cancel`、`取消`、`不要`）：中止并显示 "Aborted before scan — no files modified."
   2. **同意**（`Y`、`yes`、`ok`、`sure`、`proceed`、`go`、`continue`、`好`、`好的`、`行`、`可以`）：继续到步骤 1。
   3. **软暂停**（`wait`、`hold on`、`等一下`、`等我`、`let me`）：用一行回复确认（"Understood, waiting"），然后等待用户的下一条消息，并从规则 1 重新评估。
   4. **提问**：先回答问题，再重新显示一次通知并等待下一条回复。如果下一条回复不是同意（规则 2）—— 无论是第二个问题、另一次暂停还是其他内容 —— 则中止并显示 "Aborted — did not receive consent after clarification."

0d. 同意后，在步骤 8 之前不再提出进一步问题。

---

### 步骤 1 — 作用域枚举和状态初始化

1a. 如果用户未指定文件或目录，则应用 `../_shared/common.md` 中的自动作用域检测。
   否则尊重用户明确指定的作用域。

1b. 如果项目根目录存在 `.brooks-lint.yaml`，则读取它。按照 common.md 应用
   `disable`、`severity`、`ignore`、`focus` 和 `custom_risks`。记录已应用的
   配置值，并在所有迭代轮次中复用它们 —— 即使文件被修改，也不在步骤 6 中重新读取该文件。

1c. 初始化流水线状态（在所有轮次中持续存在）：

   - **`unresolvable`**（集合）：3 次尝试失败后退役的发现项 —— 以 `(file, line_range, risk_code)` 为键；`signature` 用于打破平局。永不重新入队。
   - **`non_critical_rounds`**（整数，0）：每产生 Warning/Suggestion 的轮次递增；在干净的轮次上重置。
   - **`fix_log`**（列表）：每项修复包含文件、行范围、风险代码、描述和结果（`applied` / `reverted` / `retired`）。

1d. 将最终的作用域文件列表记录在步骤 8 的修复报告输出缓冲区中。

---

### 步骤 2 — brooks-review 轮次（R1–R6 代码腐化）

根据 `../_shared/decay-risks.md` 中定义的所有 R 系列风险，扫描范围内的每个文件。

2a. 对于每个 R 风险，应用其症状检查表。将每次命中记录为一条发现项，
   包含：风险代码、文件 + 大致行范围、症状、来源、后果、修复、严重程度
   （Critical / Warning / Suggestion）和 **Fix-Class**（见步骤 2b）。

2b. 为每个发现项分配 Fix-Class：

   | 类别 | 标准 |
   |-------|----------|
   | **Safe** | 单文件且完全本地化：重命名非导出符号、提取常量、删除死代码、在叶子节点添加空值守卫、为未测试的纯函数添加测试脚手架。任何修改或删除已导出符号的变更即使在单个文件中也不算 Safe。 |
   | **Extended-Safe** | 多文件但 (a) 存在项目测试命令且修复前通过，且 (b) 变更不重命名、删除或更改任何公开导出符号的签名，且 (c) 本轮次中触及的文件数 ≤ 5。 |
   | **Residual** | 公开 API 中断、跨服务边界变更、没有测试覆盖作为回退、或修复方案不明确。不应用 —— 带入步骤 8 的残留报告。 |

2c. 跳过与 `unresolvable` 集合中任何条目匹配的发现项。

2d. 应用本维度中的每个 Safe 和 Extended-Safe 修复，在每个严重程度层级内
   优先处理最低风险。对于每个修复：Edit 或 Write，然后在 `fix_log` 中追加一行，
   结果为 `applied`。如果两个修复触及同一文件中的重叠行范围，则优先应用
   严重程度更高的修复，重新读取文件，然后应用下一个。

2e. 在本维度的所有修复完成后，如果存在项目测试/lint 命令则运行它
   （`package.json` 脚本、`pytest`、`cargo test`、`go test ./...` 等）。
   如果测试失败：按相反顺序逐个回滚本维度的修复，每次回滚后重新运行测试命令，
   直到测试通过。在 `fix_log` 中将每个回滚的修复标记为结果 `reverted`，
   并将该发现项提升为 **Residual**。如果找不到测试命令，则在报告中注明一次并继续。

2f. 记录维度摘要：扫描了 N，应用了 Safe M，应用了 Extended-Safe K，
   回滚了 R，Residual P。

---

### 步骤 3 — brooks-test 轮次（T1–T6 测试腐化）

根据 `../_shared/test-decay-risks.md` 中定义的 T 系列风险，扫描测试文件（以及未经测试的生产代码）。

按照与步骤 2 相同的子步骤（分类 → 应用 → 验证 → 摘要），
使用 T 前缀的风险代码。对于完全没有测试覆盖的生产文件，记录为 T5（覆盖幻觉）。
添加纯函数测试的测试脚手架为 **Safe**；添加需要新测试基础设施的测试为 **Residual**。

---

### 步骤 4 — brooks-debt 轮次（技术债累积）

通过债务视角重新分类 R 系列发现项 —— 在累积规模下的相同症状：
重复的重复代码、分层的变通方案、过期的 `TODO`/`FIXME` 集群、无效标志。
使用 **痛苦度 (1–3) × 扩散度 (1–3)** 对每项评分；总分 7–9 = Critical，
4–6 = Warning，1–3 = Suggestion。对于模式级出现的情况应用严重程度提升
（孤立的 Suggestion → 跨 4+ 模块的 Warning）。

按照与步骤 2 相同的子步骤操作。债务发现项通常跨越多个文件，
更可能落入 Extended-Safe 或 Residual 而非 Safe。

---

### 步骤 5 — brooks-audit 轮次（架构完整性）

扫描整个范围内的架构级问题。依赖方向症状（反向依赖、循环导入、跨域耦合）
在 `../_shared/decay-risks.md` 的风险 5 中定义 —— 使用该检查表。步骤 5
还涵盖了 R5 未涵盖的仅限架构的问题：缺失的抽象层、上帝模块、领域代码中泄露的基础设施，
以及接缝边界违规。

大多数架构发现项本质上就是 **Residual** —— 它们需要对模块边界进行人为判断。
少数属于 Extended-Safe（例如将 3+ 模块中使用的共享常量提取到一个尚无任何其他模块
导入的新模块中）。不要自动重构模块布局、重命名包或更改公共导出。

按照与步骤 2 相同的子步骤操作。

---

### 步骤 6 — 迭代循环

**目标：** 重新扫描修复触及的内容并收敛。在干净的轮次、上限或无进展时停止。

6a. 构建重新扫描作用域：
   - 当前轮次步骤 2–5 中修改的每个文件，加上
   - 与已修改文件相同模块中的每个文件，加上
   - 从已修改文件静态导入的每个文件。

   不要重新扫描其依赖项未被触及的文件。在"模块"可能跨越数百个文件的
   monorepo 中，将同模块的桶范围缩小到从已修改文件导入或被已修改文件导入的文件
   （仅直接依赖图）。

6b. 在重新扫描的作用域上重新运行步骤 2–5。对于本轮中的每条新发现项：
   - 如果匹配 `unresolvable` 中的条目 → 跳过。
   - 否则如果是 🔴 Critical → 入队并修复；Critical 发现项迭代直到
     已解决或已退役（3 次失败尝试 → `unresolvable`）。
   - 否则 🟡 Warning / 🟢 Suggestion → 入队并修复，受以下上限约束。

6c. 在尝试所有修复后对轮次进行分类：
   - **干净的轮次**（在 `unresolvable` 之外没有新发现项）：流水线
     收敛 → 继续到步骤 7。
   - **仅 Critical 的轮次**：不要递增 `non_critical_rounds`；返回到 6a。
   - **混合或非关键轮次**（产生任何 Warning / Suggestion）：
     将 `non_critical_rounds` 递增 1。如果达到上限（默认 3，
     或 `.brooks-lint.yaml` 中的 `sweep.max_iterations`），继续到步骤 7，
     其余未解决的非关键发现项记录为 `"Unresolved — iteration cap reached"`。
     否则返回到 6a。

6d. 修复重试规则：如果单个发现项在任何轮次组合下验证（步骤 2e）失败 3 次，
   则以 `"3-retry budget exhausted"` 为由将其退役到 `unresolvable`，并停止尝试它。

---

### 步骤 7 — 残留项聚合

收集所有未就地修复的内容，进行去重：

- 步骤 2–5 中的所有 Residual 类发现项（首轮 + 重新扫描轮次）
- 所有 `unresolvable` 条目及其退役原因
- 步骤 6c 中的所有迭代上限残留项

按 Critical → Warning → Suggestion 排序。在每个严重程度内，列出文件路径、
风险代码、症状（一行）、修复方案（一行），以及未应用的原因
（`public API break` / `no test coverage` / `3-retry budget` / `iteration cap`）。

---

### 步骤 8 — 扫描报告

输出最终报告。使用 `../_shared/common.md` 中的标准报告模板，并附上以下补充内容：

```
# Brooks-Lint — Full Sweep Report
Mode: Full Sweep | Scope: <files or directory>
Config: .brooks-lint.yaml applied (N risks disabled, M paths ignored)   # omit if no config

## Dimension Summary
| Dimension | Scanned | Safe Applied | Extended Applied | Reverted | Residual |
|-----------|---------|--------------|------------------|----------|----------|
| Review (R1–R6) | ... | ... | ... | ... | ... |
| Test (T1–T6)   | ... | ... | ... | ... | ... |
| Debt           | ... | ... | ... | ... | ... |
| Audit          | ... | ... | ... | ... | ... |

## Iteration History
Round 1: <classification — clean / critical-only / mixed>, <N> new findings
Round 2: ...
Stopped at: clean round | iteration cap | no outstanding criticals

## Fix Log
| # | File | Lines | Risk | Outcome  | Change |
|---|------|-------|------|----------|--------|
| 1 | ...  | ...   | R2   | applied  | Extract repeated constant |
| 2 | ...  | ...   | T4   | reverted | Test regression; promoted to Residual |
...

## Health Score Delta
Before: <estimated score>/100  →  After: <estimated score>/100
(Re-run /brooks-health for an exact recalculation.)

## Residual Items  (<K> not applied)
<Iron Law entries, sorted Critical → Suggestion, with "Not applied because: ..." line>

## Summary
- Total findings detected: <N>
- Fixed this sweep: <M>
- Residual (needs human review): <K>
- Unresolvable (3-retry exhausted): <U>
```

如果没有残留项且没有不可解条目，则以以下内容结束：
**"Sweep complete — codebase is clean."**

**报告中的模式行：** `Full Sweep`