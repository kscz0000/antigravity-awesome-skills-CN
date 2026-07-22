---
name: ui-lint
description: 快速自动化 lint —— 数秒内检测常见设计系统违规（UI lint、lint、a11y、可访问性、UI 检查、颜色对比）
risk: unknown
source: https://github.com/bitjaru/styleseed/tree/main/engine/.claude/skills/ss-lint
source_repo: bitjaru/styleseed
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/bitjaru/styleseed/blob/main/LICENSE
---

# 设计 Lint（快速检查）
## 何时使用

当你需要快速自动化 lint —— 数秒内检测常见设计系统违规时，使用本技能。


## 何时不要使用

- 需要对设计判断（构图、层级、节奏）进行更深入的审查 → 使用 `/ss-review`
- 专门针对可访问性 → 使用 `/ss-a11y`
- 针对 Nielsen UX 启发式 → 使用 `/ss-audit`
- 用于应用重构 —— 本技能仅标记违规；要修复请使用 `/ss-review`

目标：**$ARGUMENTS**

## 本技能的作用

基于 grep 的快速扫描，用于查找常见的设计违规。运行只需数秒（不同于 `/ss-review` 那种深度的人工审查）。每次文件变更后运行一次。

## 检查项

### 1. 硬编码颜色
在 className 字符串中搜索应为语义令牌的十六进制颜色：
```bash
grep -n '#[0-9a-fA-F]\{3,8\}' [file] | grep -v 'theme.css\|tokens\|\.json'
```
**违规：** `text-[#3C3C3C]`，`bg-[#721FE5]`
**修复：** `text-text-primary`，`bg-brand`

### 2. Tailwind 中使用原始像素值
```bash
grep -n 'p-\[.*px\]\|m-\[.*px\]\|gap-\[.*px\]' [file]
```
**违规：** `p-[24px]`，`gap-[12px]`
**修复：** `p-6`，`gap-3`

### 3. 旧的 width/height 语法
```bash
grep -n 'w-[0-9] h-[0-9]\|w-\[.*\] h-\[' [file]
```
**违规：** `w-4 h-4`
**修复：** `size-4`

### 4. 物理属性（仅适用于 LTR）
```bash
grep -n ' ml-\| mr-\| pl-\| pr-' [file]
```
**违规：** `ml-2`，`mr-4`
**修复：** `ms-2`，`me-4`

### 5. 禁用颜色
```bash
grep -n 'text-black\|bg-black\|#000000\|#000"' [file]
```
**违规：** 任何纯黑
**修复：** 使用皮肤的 text-primary 令牌

### 6. 缺少 data-slot
```bash
grep -n 'function [A-Z]' [file] # find components
grep -n 'data-slot' [file]       # check if present
```
**违规：** 组件缺少 `data-slot`
**修复：** 添加 `data-slot="component-name"`

### 7. 字号 CSS 变量（关键 —— 与 Tailwind v4 冲突）
```bash
grep -n 'text-\[var(--' [file]
grep -n '\-\-text-.*px\|--fs-.*px' [file]
```
**违规：** `text-[var(--text-sm)]` 或在 theme.css 中定义 `--text-sm: 13px`
**修复：** 使用显式写法 `text-[13px]`。CSS 变量形式的字号与 Tailwind v4 的 `--text-*` 命名空间冲突 —— Tailwind 会将其识别为颜色，而非字号。

### 8. className 缺少 cn()
```bash
grep -n 'className={`' [file]
```
**违规：** 使用模板字符串的 className
**修复：** 对所有 className 组合使用 `cn()`

## 输出格式

```
🔴 FAIL  [file:line] Hardcoded hex: text-[#3C3C3C] → use text-text-primary
🔴 FAIL  [file:line] Raw px: p-[24px] → use p-6
🟡 WARN  [file:line] Physical prop: ml-2 → use ms-2
🟡 WARN  [file:line] Missing data-slot on MyComponent
🟢 PASS  No violations found

Total: X errors, Y warnings
```

如果错误数 > 0，请列出每项违规的具体修复方式。

## 局限

- 仅当任务明确匹配其上游来源与本地项目上下文时，才使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例视为环境特定测试、安全审查，或针对破坏性/高成本操作的用户审批的替代品。
