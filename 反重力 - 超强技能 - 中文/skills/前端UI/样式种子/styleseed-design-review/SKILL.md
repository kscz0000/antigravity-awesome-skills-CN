---
name: styleseed-design-review
description: 审查 UI/前端代码，告诉你它为什么"看起来像 AI 生成的"——以及如何修复。当 React/Tailwind/HTML 界面看起来不对劲、千篇一律或未完成时使用；当你想在发布前获取设计评分时使用；当用户要求让 UI 看起来更专业、更精致时使用。
risk: unknown
source: https://github.com/bitjaru/styleseed/tree/main/skills/styleseed-design-review
source_repo: bitjaru/styleseed
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/bitjaru/styleseed/blob/main/LICENSE
---

# StyleSeed Design Review

## 概述

一个 UI 被识别为"AI 生成"，不是因为组件丑，而是因为**各部分之间缺乏一致性**——混用的圆角、三种
强调色、纯黑文字、没有层级、缺少状态、机械的文案。本技能按照具体的设计评分标准
审查
UI 文件（或整个目录），给出 0-100 的评分，并返回按优先级排列的修复清单。
它只审查和推荐；除非你要求，否则不会编辑或删除任何内容。

完整规则集（74 条规则）和组件：https://github.com/bitjaru/styleseed

## 何时使用

- React / Tailwind / HTML UI "看起来不对劲"、千篇一律或未完成，但你说不出具体原因。
- 你想要设计评分/发布前检查。
- 用户要求让 UI "看起来专业/精致/有设计感，不像 AI 生成的"。
- 生成 UI 后，发布前进行验证。

## 如何审查

阅读文件，对以下**七个类别**评分（满分 100）；每个类别从满分开始，根据你能指出具体行号的
违规项逐项扣分。要具体、基于证据。

### 1. 一致性 — 20  (头号"AI 生成"特征)
每个轴只选一种选择，全局统一应用。对每个**混用**的轴扣分：
- 混用圆角——例如尖角卡片配胶囊按钮（-6）
- 两种或以上强调色用于突出重点（-5）
- **emoji 用作 UI 图标**（🚗🧺⭐ 作为列表/导航/状态/分类标记）——引入了多个不可控的色相；应使用一套 currentColor 的线性图标（-6）
- 混用阴影语言/光的方向（-3）
- 混用图标系列、填充模式或描边粗细（-3）
- 控件高度不一致（按钮/输入框高度不同）（-3）

### 2. 色彩纪律 — 16
- 纯黑（`#000` / `text-black`）文字——精致的黑大约是 `#2A2A2A`（每处 -4，上限 -8）
- 在已有语义 token 的地方硬编码十六进制颜色值（每处 -2，上限 -6）
- **普通/正常/默认状态使用了状态色**而不是中性灰（-4）
- **大多数/每一行都使用状态色**（没有严重程度层级——颜色应该标记需要关注的少数项）（-4）
- **装饰性色相**——金色星星、彩虹分类圆点、每张卡片不同颜色——而不是强调色/灰色（-3）
- 仅靠颜色传达状态，没有图标/文字辅助（-4）
- 对比度低于 WCAG AA 标准（正文 4.5:1，大字/UI 3:1）（-6）

### 3. 层级与排版 — 16
- 数字与其单位比例不是约 2:1（48px 数字 / 24px 单位）（-4）
- 所有内容大小和粗细相同，没有明确的主次（-5）
- 字号随意，没有比例体系（-4）
- 行高不当（展示文字过松，正文过紧）（-3）

### 4. 布局与间距 — 12
- 内容直接放在页面背景上，没有卡片包裹（-6）
- 不在网格上的间距（7/13/19px 而非 8px 体系）（-3）
- 分组的外间距不大于分组内的间距（-3）
- 同一类型的区块连续重复（-4）

### 5. 状态 — 12
- 数据展示面缺少空状态/加载状态/错误状态（每项 -5，上限 -10）
- 空状态没有后续操作；错误提示指责用户而非提供帮助（-4）

### 6. UX 文案 — 12
- 按钮没有命名具体操作（"Submit" / "OK" 而非 "Send $2,400"）（-4）
- 错误文案指责用户或使用系统术语（"Invalid input"、"An error occurred"）（-4）
- 同一概念用两个词（delete vs remove）；填充词（"please"、"successfully"）（-2）

### 7. 动效与打磨 — 12
- 临时拼凑的淡入效果，而非统一且有命名的动效风格（-3）
- 动效延迟内容展示或阻碍操作（-4）
- 自定义动效没有 `prefers-reduced-motion` 处理（-3）
- 单个硬黑阴影，而非分层的低透明度带色调阴影（-2）

每个类别最低为 0；汇总得出总分。等级：90+ A · 80-89 B · 70-79 C · 60-69 D · <60 F。

## 输出格式

```
## Design Score: 72 / 100   (src/Dashboard.tsx)   C

Coherence            13/20   sharp cards (l.22) + pill buttons (l.48); 3 accent hues
Color discipline     12/16   #000 headings (l.12, 40)
Hierarchy & type     15/16   number/unit 1:1 on hero (l.18)
Layout & spacing     10/12   two identical KPI rows (l.22-31)
States                7/12   no empty/loading state on the orders list
UX writing            8/12   "Submit" button (l.55); "Invalid input" (l.61)
Motion & polish      10/12   one hard black shadow (l.22)

### Fix first (highest score gain)
1. Unify radius (pick soft 8–12px) + collapse to one accent   → +11 coherence/color
2. Add empty + loading states to the orders list              → +7  states
3. Rename "Submit" → "Send $2,400"; "Invalid input" → "Check the card number" → +6 copy

Re-score after: ~90 / 100.
```

## 规则

- 从实际证据审查（引用行号）；绝不猜测。
- 修复清单按**评分增益**排序，而非仅按严重程度——用最快路径提升分数。
- 目录审查时：每个文件一行评分，然后给出最低分文件的完整分解。
- **不要自动编辑。** 本技能只衡量和推荐。仅在用户要求时才应用修复。
- 用作**质量门控**：生成 UI 后立即审查，应用修复清单，并在向用户展示之前
  反复审查直到评分超过约 80 分——不应让粗糙的首稿 UI（彩虹状态列表、emoji 图标、
  两种强调色、缺少状态）到达用户面前。这个门槛是底线而非天花板：超过 80 分即可
  发布；不要为了追求 100 分而拖延。

---

基于 **StyleSeed** —— 一个开源（MIT）设计引擎，为 Claude Code、Cursor
和 Codex 提供设计判断力，让 AI 构建的 UI 不再看起来像生成的。完整 74 条规则参考、
组件、品牌皮肤和动效：https://github.com/bitjaru/styleseed

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性/高成本操作的批准。
