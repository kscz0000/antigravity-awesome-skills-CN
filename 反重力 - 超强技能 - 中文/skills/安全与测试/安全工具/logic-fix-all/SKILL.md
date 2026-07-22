---
name: logic-fix-all
description: '自主仓库级审计-修复流水线：健康检查 → 审查 → 定位/解释 → 修复 → 差异验证 → 迭代直至干净。启动时强制弹出确认提示（token消耗大）；确认后自动运行。当用户需要查找并修复所有逻辑问题时触发——"修复所有逻辑问题"、"全量修复"、"逻辑全修"、"fix all logic"、"logic fix all"'
risk: unknown
source: https://github.com/hyhmrright/logic-lens/tree/main/skills/logic-fix-all
source_repo: hyhmrright/logic-lens
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/logic-lens/blob/main/LICENSE
---

# Logic-Lens — 逻辑全修
## 使用时机

当需要自主仓库级审计-修复流水线时使用：健康检查 → 审查 → 定位/解释 → 修复 → 差异验证 → 迭代直至干净。启动时强制弹出确认提示（token消耗大）；确认后自动运行。当用户需要查找并修复所有逻辑问题时触发——"修复所有逻辑问题"、"全量修复"、"逻辑全修"、"fix all logic"、"logic fix all"


## 设置

按 `../_shared/common.md` §13 采用阶段门控懒加载：
1. 确认前，仅读取 `../_shared/common.md` 获取语言、范围路由、fix-all 头部字段、配置字段和加载预算；然后读取 `logic-fix-all-guide.md` 至阶段地图，读取 `guide-phases-0-2-consent-scope-health.md` 至 Phase 0。
2. 确认后，仅在进入对应阶段时读取该阶段文件。
3. 当某阶段调用其方法时，按需加载 `../_shared/logic-risks.md`、`../_shared/semiformal-guide.md`、`../_shared/semiformal-checklist.md`、`../_shared/report-template.md` 及其他技能指南。

## 流程

**步骤 0. 语言 + 范围路由。** 按 `common.md` §1 检测语言。默认范围为仓库根目录；遵循用户指定的子路径或粘贴的代码片段。对于粘贴的代码片段，跳过确认提示直接运行修复流水线。读取 `.logic-lens.yaml` 获取 `ignore:`、`custom_risks`、`severity:`、`focus:` 和 `fix_all.max_iterations`。

**步骤 1. 确认 + 范围枚举**（指南 Phase 0–1）—— 仓库/目录范围：强制显示确认提示，展示范围/方法/成本/迭代上限；确认后，枚举影响运行时的文件（源码/配置/约束/文档），排除 `.git` 和构建产物，按风险层级分类。粘贴的代码片段：跳过确认，直接枚举代码片段的函数。

**步骤 2. 健康检查**（指南 Phase 2）—— 应用 logic-health 方法论，映射每个模块的 Logic Score 和 L-code 模式。

**步骤 3. 深度审查**（指南 Phase 3）—— 逐文件应用 logic-review，收集完整的 Premises → Trace → Divergence 发现。

**步骤 4. 条件性澄清**（指南 Phase 4–5）—— 对存在具体故障的位置应用 logic-locate；当发现的路径不清晰时（调用深度 > 3、跨模块或异步）应用 logic-explain。

**步骤 5. 修复队列 + 补救**（指南 Phase 6）—— 按严重程度排序；为每个发现编写可直接粘贴的 Remedy；将跨文件矛盾路由到正确的编辑目标（代码/约束/配置/文档）。

**步骤 6. 应用 + 验证**（指南 Phase 7）—— 应用每个修复，然后对原始代码与修复后代码应用 logic-diff 方法论。期望判定为 `⚠️ Conditionally Equivalent`，其中差异条件恰好是 bug 场景。若判定为 `✅ Semantically Equivalent`（修复无效果）或在 bug 场景之外出现新的分歧（回归），则回退。最多重试 3 次。

**步骤 7. 迭代 + 报告**（指南 Phase 8–9）—— 对已修改文件及其消费者重新运行健康检查 + 审查；Critical 无上限循环；Warning/Suggestion 轮次受 `fix_all.max_iterations` 上限约束，达到上限时弹出用户升级提示。输出修复报告。

**报告中的模式行：** `Logic Fix All`（中文：`逻辑全修`）。

**修复报告附加内容**（追加在标准摘要之后；本地化所有标签）：

```
## Scope

| Role (source/config/constraint/doc) | Files scanned | Tier H/M/L | Truncated? |
|-------------------------------------|---------------|------------|------------|

## Skill Invocations
logic-health: N · logic-review: N · logic-locate: N · logic-explain: N · logic-diff: N

## Iteration History

| Round | Severity class | New findings | Action |

## Fix Log

| # | File | Lines | Finding | Risk | Severity | Fix Applied (one-line edit or diff summary) | Status (resolved/unresolved/reverted) |

## Resolved by Clarification
[Findings the Phase-5 logic-explain pass revealed as false positives. Empty if none.]

## Unresolved Findings
[Include reason per entry: "conflicting constraints", "user stopped iteration at round N",
"hard iteration ceiling reached", "ambiguous spec", "unclear whether spec or consumer is wrong".
Empty if all resolved.]
```

**报告头部字段**（按 `common.md` §5 替换标准单行头部）：

```
**Logic Score (before):** XX/100
**Logic Score (after):**  YY/100
**Findings fixed:** N  (Critical: n1 · Warning: n2 · Suggestion: n3)
**Findings unresolved:** M
```

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性/高成本操作的审批。
