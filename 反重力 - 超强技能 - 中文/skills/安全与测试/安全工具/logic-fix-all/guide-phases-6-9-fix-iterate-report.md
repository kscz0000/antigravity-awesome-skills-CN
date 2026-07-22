# Logic-Lens — 逻辑全修 — 阶段 6-9（修复 · 验证 · 迭代 · 报告）

---

## 阶段 6 — 修复队列组装

6a. 合并阶段 3–5 的所有发现（阶段 3 审查 + 阶段 4 定位，经阶段 5 澄清更新/过滤）。阶段 2 健康检查观察不直接纳入——它们必须先从阶段 3 获得完整的 Premises→Trace→Divergence 三元组才能进入队列（铁律）。

6b. 按严重程度排序。每个层级内的二级排序：(1) "confirmed by test/error" 优先；(2) 系统性模式根因优先于症状；(3) 根因优先于调用点。

| 优先级 | 标准 |
|----------|----------|
| 1 | 🔴 Critical |
| 2 | 🟡 Warning |
| 3 | 🟢 Suggestion |

6c. 为每个发现编写补救：**最小化**（仅修改追踪显示有误的部分）、**针对性**（不附带副作用重构）、**有理据**（一句话说明为何此修复正确）。

6d. 跨文件矛盾的补救目标：
- **代码 vs 约束文件**（CLAUDE.md/AGENTS.md/GEMINI.md/README）：编辑代码。例外：若约束文本明显过时（引用了已移除的函数/模块）且代码内部一致，编辑约束文件并在修复日志中注明规格漂移。
- **代码 vs 运行时配置**：编辑配置。例外：若配置值对其键内部一致且代码看似笔误，编辑代码。当双方都合理时，记录为 "Unresolved — unclear whether spec or consumer is wrong"。
- **文档 vs 文档**：(1) git mtime 更近者胜出；(2) 路径更深者胜过根级路径；(3) 仍平局 → "Unresolved — ambiguous spec" 并附双方引用。
- **配置内部不一致**：编辑被引用较少的键。

---

## 阶段 7 — 应用 + 验证（logic-diff）

7a. 首次修复前，捕获基线：

```bash
PRE_FIX_REF=$(git rev-parse HEAD)
```

若非 git 仓库，在首次编辑前将每个文件复制到 `.logic-fix-all-backup/<path>`。

逐条发现应用修复。每次修复后：记录文件路径、变更行范围、一行描述 → 修复日志行。同一文件中行范围重叠时，先修复优先级较高的，然后重新读取文件再应用第二个。

7b. 当补救需要选择方案时，匹配周围代码的现有约定（读取最近的调用方和同级函数）。无法发现约定时，默认选择更防御性的选项（raise/reject/fail fast）。

7c. 对修复前和修复后版本应用 `../logic-diff/logic-diff-guide.md`。独立文件可并行验证；同文件或跨依赖修复需逐一验证。

声明修复"通过"前的**硬验证门控**：
```bash
git diff -- <file>
git diff "$PRE_FIX_REF" -- <file>
```
diff 必须：(a) 匹配计划的补救，(b) 不触碰发现范围之外的行，(c) 使文件语法有效。任何一项失败则跳转至 7d。

解读 logic-diff 判定：

| 判定 | 条件 | 含义 | 操作 |
|---------|-----------|---------|--------|
| Conditionally Equivalent | 恰好覆盖失败场景 | 修复移除了 bug | **通过** |
| Conditionally Equivalent | 比失败场景更窄或更宽 | 部分修复/过度修复 | 7d |
| Conditionally Equivalent | 与失败场景正交（原始 Divergence 不再触发） | 修复成功；新条件是已存在的独立 bug | **通过** + 以 "discovered during verification" 标签记录新发现 |
| Semantically Equivalent | — | 修复未改变任何内容 | 7d |
| Semantically Divergent | — | 修复破坏了之前正确的路径 | 7d |

额外验证：修复后特定 Divergence 字段条件不再触发。

7d. 发生回归时，回退并重试：
```bash
git checkout "$PRE_FIX_REF" -- <file>
# or: cp .logic-fix-all-backup/<path> <path>
```
禁止使用 `git reset --hard` 或 `git clean -f`。3 次失败尝试后，记录为 "Unresolved — conflicting constraints" 并继续。

7e. 若 logic-diff 无法确认等价性（函数过于复杂或涉及外部状态），标注为 "unverified — integration test recommended" 并继续。

---

## 阶段 8 — 迭代循环

### 8a. 跨轮次持久状态

- **`unresolvable_findings`**（集合）：阶段 7d 以 "Unresolved — conflicting constraints" 终止的发现。每条为 `(file_path, line_range, L_code, divergence_signature)`。主要按 `(file_path, line_range, L_code)` 匹配——`divergence_signature` 仅作决胜（LLM 生成的 Divergence 文本措辞可能漂移）。
- **`non_critical_round_counter`**（整数，初始 0）：自上次产出 ≥1 条 Warning 或 Suggestion 的提示以来的轮次。在 8d 中递增，仅在用户在 8e 中回答 "continue" 时重置为 0。
- **`consecutive_continues`**（整数，初始 0）：用户在升级提示中回答 "continue" 的次数。永不重置。硬上限为 3。

### 8b. 重新扫描范围

阶段 7 后，对以下内容重新运行阶段 2–3：阶段 7 中所有修改的文件 + 同模块中的文件 + 静态导入修改文件的文件。跳过依赖未被触及的文件。

**静态图边界：** 基于反射的调用、字符串分发、共享全局状态及类似的动态连接可能将回归传播到此扫描范围之外。若仓库有测试套件，阶段 9 摘要应建议运行它。

### 8c. 分类每个新发现

- 匹配 `unresolvable_findings` → 跳过。
- 🔴 Critical → 加入修复后队列（循环直至解决，或直至阶段 7d 在 3 次失败尝试后将其归入 `unresolvable_findings`）。
- 🟡 Warning / 🟢 Suggestion → 加入修复后队列。

对修复后队列运行阶段 6–7。

### 8d. 轮次核算

- **干净轮次**（`unresolvable_findings` 之外无新发现）→ 进入阶段 9。
- **仅 Critical 轮次** → 不递增 `non_critical_round_counter`；返回 8b。
- **混合或非 Critical 轮次** → 递增 `non_critical_round_counter`。若低于上限，返回 8b。若达到上限，进入 8e。

### 8e. 用户升级

```
Logic-Fix-All iteration cap reached.

After {cap} non-critical rounds, N Warning and M Suggestion
findings remain. No outstanding Critical findings
(unresolvable Criticals, if any, are listed in the Fix Log).

Continue for another {cap} rounds?  [Y/n]
```

当 `consecutive_continues` 为 1 或 2 时，追加：
```
(You have continued {consecutive_continues} time(s) so far — hard
cap is 3 continues per run. To run more rounds without repeated
prompts, raise `fix_all.max_iterations` in `.logic-lens.yaml`.)
```

使用与阶段 0b 相同的确认/否定规则解析回复。
- **确认：** 递增 `consecutive_continues`。若现在 ≥ 3，硬停止——将剩余记录为 "Unresolved — hard iteration ceiling reached (user continued 3×)" 并进入阶段 9。否则将 `non_critical_round_counter` 重置为 0 并返回 8b。
- **否定（或未确认）：** 将剩余记录为 "Unresolved — user stopped iteration at round N" 并进入阶段 9。

---

## 阶段 9 — 最终报告

使用 `report-template.md` 的报告模板及 `SKILL.md` 的修复报告附加内容。包含：

- **范围摘要：** 按角色分类的文件数；若应用了阶段 1f 截断则注明。
- **技能调用次数：** health: N、review: N、locate: N、explain: N、diff: N。
- **迭代历史：** 按严重级别的轮次数；每次上限升级及用户响应。
- **按角色分类的发现：** 源码、配置、约束、文档的独立子表。
- **澄清后解决：** 阶段 5 降级为误报的发现。

最终报告中不输出每条发现的 Premises/Trace/Divergence 块——修复日志表是面向用户的记录。按需提供完整追踪。

### Logic Score 计算

- **Logic Score（修复前）：** 从 100 起始，对阶段 3–5 收集的每个发现（修复前）扣分。应用 `common.md` 中的每 L-code 扣分上限。
- **Logic Score（修复后）：** 从 100 起始，仅对阶段 8 后仍标记为未解决的发现扣分。

当修复前后数值相等但实际有修复时（例如 3 个 L1 发现合并为一个 −15 在两处相同），"Findings fixed" 计数是权威的改善信号。
