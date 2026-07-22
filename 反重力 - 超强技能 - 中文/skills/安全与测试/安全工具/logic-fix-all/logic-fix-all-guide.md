# Logic-Lens — 逻辑全修 — 指南（导航）

本指南驱动全仓库逻辑级半形式化追踪流水线，编排 **logic-health → logic-review → logic-locate → logic-explain → logic-diff**，直至代码库干净。

唯一的硬交互点是 **阶段 0（确认门控）**。批准后，流水线自动运行，除非阶段 8 触达迭代上限。

这是**逻辑**审查，不是语法/风格/lint 检查。

---

## 流水线概览

```
  Phase 0 — Pre-flight notice & consent gate        ← hard stop, wait for user
  Phase 1 — Scope enumeration (role + risk tier)
  Phase 2 — Health pass (module Logic Score map)
  Phase 3 — Deep review (per-file semi-formal)
  Phase 4 — Fault location (conditional)
  Phase 5 — Path clarification (conditional)
  Phase 6 — Fix queue assembly (sorted, remedied)
  Phase 7 — Apply + verify (logic-diff)
  Phase 8 — Iteration loop (until clean or capped)
  Phase 9 — Final Fix Report
```

## 各阶段文件位置

| 阶段 | 文件 |
|--------|------|
| **0, 1, 2** | `guide-phases-0-2-consent-scope-health.md` — 预检确认；按角色和风险层级的全仓库文件遍历；模块 Logic Score 映射。 |
| **3, 4, 5** | `guide-phases-3-5-review-locate-clarify.md` — 逐文件 Premises→Trace→Divergence（阶段 3）；条件性故障定位（阶段 4）；条件性路径澄清（阶段 5）。 |
| **6, 7, 8, 9** | `guide-phases-6-9-fix-iterate-report.md` — 按严重程度排序的修复队列（阶段 6）；通过 logic-diff 应用 + 验证、回归时回退、重试 ≤3 次（阶段 7）；带状态追踪的迭代循环（阶段 8）；最终修复报告（阶段 9）。 |

## 阶段门控阅读

用户确认前不要阅读整个流水线。

**阶段 0 之前：**
- 仅读取 `../_shared/common.md` 获取语言、范围路由、fix-all 头部字段、配置字段和加载预算。
- 读取本文件至阶段地图。
- 仅读取 `guide-phases-0-2-consent-scope-health.md` 至阶段 0，使确认提示准确。

**确认后：**
- 进入某阶段时读取该阶段的活跃部分。
- 仅当当前阶段调用某方法论时加载共享文件和其他技能指南。
- 保持小型状态记录，包含阶段、已扫描文件、发现、修复和未解决签名，以便后续阶段无需重新读取先前阶段的文本。

## 无 git 环境下运行

阶段 1 默认使用 `git ls-files` 作为枚举器。若 `.git` 不存在，回退到使用相同忽略模式的递归文件遍历。在范围表中报告回退情况。

## 何时将控制权交还用户

1. **阶段 0** — 始终，在任何扫描或编辑之前。
2. **阶段 8 迭代上限** — 当 `fix_all.max_iterations` 的 Warning/Suggestion 轮次已运行且仍有非 Critical 发现时。连续 3 次 "continue" 触及硬上限。
3. **阶段 6 约束与代码平局** — 当发现可通过编辑代码或行为文档/配置来修复，且双方都不是明显权威来源时。

## 输出格式

修复报告布局：头部字段 → 发现 + 摘要 → fix-all 扩展（范围 / 技能调用 / 迭代历史 / 修复日志 / 澄清后解决 / 未解决发现）置于摘要之后。按 `common.md` §1 语言规则渲染。
