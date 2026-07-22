---
name: accesslint-audit
description: "发现并修复 WCAG 2.2 可访问性问题。两种模式——报告模式（扫描代码库或页面，输出按优先级排序的书面报告，不做改动）和修复模式（针对目标执行审计→修改→验证循环）。优先采用 direct-CDP 实时 DOM 审计；回退到 browser-MCP 组合方案或 HTML 字符串审计。触发词：WCAG、可访问性、无障碍、a11y、accessibility 审计、accessibility 修复、accesslint、无障碍审查。"
risk: safe
source: "https://github.com/AccessLint/skills"
date_added: "2026-06-02"
---

你负责审计可访问性，并按需修复发现的问题。

## 何时使用
- 任务与以下描述匹配时使用此技能：发现并修复 WCAG 2.2 可访问性问题。两种模式——报告模式（扫描代码库或页面，输出按优先级排序的书面报告，不做改动）和修复模式（针对目标执行审计→修改→验证循环）。优先采用 direct-CDP 实时 DOM 审计；回退到 browser-MCP 组合方案或 HTML 字符串审计。

## 根据用户意图选择模式

- **报告模式** ——"审计我的代码库"、"审查 src/components/"、"这个页面有什么问题？"、"给我一份 a11y 报告"。你做审计并产出报告。**不修改任何文件。**
- **修复模式** ——"修复 X 中的 a11y 问题"、"审计并修复"、"让这个变得可访问"、"确认对比度修复已生效"，或交给你一份违规清单让你落地。你执行审计 → 修改 → 验证。

拿不准就问。用户只要审计时，别默认走修复模式。

非常大规模的扫描若涉及主线程上下文成本，可通过 `Task`（通用目的代理）调用以隔离上下文。两种调用方式做法相同。

## 选择流程

三种流程，按偏好顺序。

1. **`audit_live`** ——任何 URL 都优先尝试。连接运行中的 Chrome 调试会话，或自动启动一个最小化的 Chrome —— 无需用户配置。单次调用；IIFE 字节不进入上下文。
2. **`audit-live-page` 提示词** ——当用户需要审计其**现有浏览器会话**（已登录的应用、特定状态）且已连接 browser MCP（chrome-devtools-mcp、playwright-mcp、puppeteer-mcp）时使用。通过 `Skill` 调用，传入 `mode: "fix"` 或 `mode: "plan"`。
3. **`audit_html`** ——用于原始 HTML 字符串、文件（先 `Read`，再 `audit_html`），或已渲染为字符串的 JSX。修复模式验证时配 `audit_diff({ html })` 使用。

非 URL 目标，直接进入流程 3。URL 目标，先试流程 1；自动启动失败时，若已连接 browser MCP 则试流程 2；否则回退到流程 3，并标注实时 DOM 覆盖受限。

## 范围处理（报告模式）

- **目录路径** ——分析其中所有相关文件。
- **多个文件** ——分析所列文件及其可达的 import。
- **URL** ——直接审计。若是开发服务器 URL，走流程 1 或 2。
- **无参数** ——请用户收窄范围。整库扫描几乎都不是正确选择。

报告开头需明确陈述范围。

## 方法（报告模式）

1. **盘点范围。** 用 Glob/Grep 枚举组件、模板、样式。抽样代表性文件，不要盲目全部打开。
2. **尽量做实时审计** ——渲染后的 DOM 能暴露源码看不到的问题。使用上面的流程选择器。
3. **寻找模式。** 一个组件违反某条规则，相似的组件大概率同样违反。规则 ID 与组件族归类，不要把同一条问题列 30 遍。
4. **按用户影响排序。** 严重/重要问题优先。低影响违规大量出现时，往往是同一个根因。
5. **扫描阶段调用使用 `format: "compact"`。** 详细输出留给要在报告中展开的规则。
6. **信任 `Source:` 行。** 针对 React 开发构建的实时 DOM 审计会通过 DevTools fibers 给每条违规附加 `Source: <file>:<line> (Symbol)`。直接以此作为文件指针，不要再 grep 选择器。缺少时回退到稳定 hook → 可见文本 → 树位置。
7. **单次审计返回超过约 50 条违规时停下询问** ——一份 200 条违规的报告无可操作性。

引擎捕获机器可检测的内容。内容清晰度、屏幕阅读器播报质量、键盘流连贯性、复杂场景下的视觉对比需要人工判断，标记出来待人工审核，不要瞎猜。

### 报告格式

```
# Accessibility audit — <scope>

## Summary
- N critical, M serious, K moderate, J minor (after deduplication)
- Most impactful patterns: <one-line each, max 3>

## Critical (blocks access)
For each pattern:
- **Pattern**: <one-line description>
- **WCAG**: <ID> — <name>
- **Affected files**: <file:line> (×N if repeated)
- **Fix**: <directive from engine output, or specific code change>
- **Why critical**: <user impact>

## Serious
[same shape]

## Moderate / Minor
[Bullet list, deduplicated by rule. Skip per-instance detail unless the fix differs.]

## Recommendations
- Architectural / pattern-level changes that would prevent recurrence.
- Tooling or component abstractions worth introducing.
- What to verify manually (screen reader, keyboard, low-vision testing).

## Positive findings
What the codebase does well — short, factual, reinforces practices to keep.
```

每条都要带规则 ID。`mechanical` 类规则的 `Fix:` 指令原样引用。`visual` / `contextual` 类留 `TODO` 并附规则 ID，不要编造内容。

## 步骤（修复模式）

1. **基线。** 用 `name: "before"` 和 `format: "compact"` 审计。
2. **规划并应用。** 对每条违规：
   - 有 `Source:` 行 → 直接打开对应文件对应行。列出多个（用 `←` 分隔）时，第一个是 JSX 字面量，其余是外层组件。用 `Symbol` 消歧。
   - 没有 `Source:` → grep 稳定 hook（`data-testid`、`id`、`aria-label`），再找可见文本，再退到树位置。
   - 违规的 `Fixability:` 与 `Fix:` 字段是权威依据 —— `mechanical` 类修复逐字应用，`contextual` / `visual` 类留 `TODO` 并附规则 ID。绝不编造内容。
   - 同文件的多处编辑合并为一次操作。
   - 涉及明显目标之外的文件，或机械修复超过约 10 处时，与用户确认范围。
3. **验证。** 对基线跑 `audit_diff({ audit_name: "before" })`（或用新名字重新建立基线）。确认 `-fixed` 覆盖目标且 `+new` 为空。

`Source:` 行源自 React DevTools fibers，只在针对 React 开发构建的实时 DOM 审计中出现。静态审计不会有 —— 这时回退到选择器。

对规则有疑问时，调用 `explain_rule({ id: "<rule-id>" })` 获取指引和 `browserHint`。

## 何时停止（修复模式）

- 某条违规没有 `Fix:` 指令 —— 留 `TODO`，不要瞎猜。
- 验证失败（`+new` 里有任意内容，或目标规则未出现在 `-fixed` 中） —— 明确指出并停下。不要静默迭代。

## 输出（修复模式）

每个周期输出：使用的流程、按影响分组的违规、已落地的改动（文件 + 规则）、已延期的内容（`TODO` 及原因）、最终 diff。

## 局限
- 仅在任务明确匹配上述范围时使用此技能。
- 不可将输出视为环境专属验证、测试或专家审查的替代品。
- 所需输入、权限、安全边界或成功标准缺失时，停下询问。
