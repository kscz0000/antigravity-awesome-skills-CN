---
name: hig-components-controls
description: "提问前检查 .claude/apple-design-context.md。使用现有上下文，仅询问未覆盖的信息。当用户需要选择和输入控件设计指导时使用。"
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 选择与输入控件

提问前检查 `.claude/apple-design-context.md`。使用现有上下文，仅询问未覆盖的信息。

## 核心原则

1. **清晰显示当前状态。** 用户必须始终能看到已选择的内容。开关显示开/关，分段控件高亮当前分段，选择器显示当前选项。

2. **优先使用系统标准控件。** 内置控件提供一致性和无障碍支持。自定义控件增加学习成本，可能破坏辅助功能。

3. **开关用于二元状态。** 开或关。在设置类界面中，更改立即生效。在模态表单中，更改在确认时提交。

4. **分段控件用于互斥选项。** 2-5个项目，重要性大致相等，标签简短。

5. **滑块用于连续值。** 当精确数值输入不是关键时使用。提供最小/最大标签或图标标识范围端点。

6. **选择器用于长选项列表。** 选项过多不适合分段控件时使用。适用于日期、时间、结构化数据。

7. **步进器用于小幅精确调整。** 固定步长递增/递减。在步进器旁显示当前值，设置合理的最小/最大边界。

8. **文本字段用于简短单行输入。** 文本视图用于多行。配置键盘类型以匹配预期输入（邮箱、URL、数字）。

9. **组合框：文本输入 + 选择列表。** macOS 专属。当自定义值有效时，可输入值或从预定义列表中选择。

10. **令牌字段：离散值显示为可视化令牌。** macOS 专属。用于邮件收件人、标签或离散项集合。

11. **仪表和评分指示器显示数值。** 仪表显示范围内的值。评分指示器显示评分（通常是星级）。仅显示用；如需输入请使用交互式变体。

## 参考索引

| 参考 | 主题 | 核心内容 |
|---|---|---|
| [controls.md](references/controls.md) | 通用控件 | 状态、示能性、系统控件 |
| [toggles.md](references/toggles.md) | 开关 | 开/关、即时生效 |
| [segmented-controls.md](references/segmented-controls.md) | 分段控件 | 2-5选项、等权重 |
| [sliders.md](references/sliders.md) | 滑块 | 连续范围、最小/最大标签 |
| [steppers.md](references/steppers.md) | 步进器 | 固定步长、有界值 |
| [pickers.md](references/pickers.md) | 选择器 | 日期、时间、长选项集 |
| [combo-boxes.md](references/combo-boxes.md) | 组合框 | macOS、输入或选择、自定义值 |
| [text-fields.md](references/text-fields.md) | 文本字段 | 简短输入、键盘类型、验证 |
| [text-views.md](references/text-views.md) | 文本视图 | 多行、评论、描述 |
| [labels.md](references/labels.md) | 标签 | 位置、VoiceOver 支持 |
| [token-fields.md](references/token-fields.md) | 令牌字段 | macOS、芯片、标签、收件人 |
| [virtual-keyboards.md](references/virtual-keyboards.md) | 虚拟键盘 | 邮箱、URL、数字键盘类型 |
| [rating-indicators.md](references/rating-indicators.md) | 评分指示器 | 星级评分、仅显示 |
| [gauges.md](references/gauges.md) | 仪表 | 水平指示器、范围显示 |

## 输出格式

1. **控件推荐及理由**，说明为何替代方案不太适合。
2. **状态管理**——控件如何传达当前状态，更改是立即生效还是确认时提交。
3. **验证方式**——何时显示错误，如何传达规则。
4. **无障碍**——VoiceOver 的标签、特征、提示。

## 需要询问的问题

1. 数据类型是什么？（布尔值、固定集合选择、数值、自由文本？）
2. 有多少选项？
3. 目标平台？（组合框和令牌字段仅限 macOS）
4. 设置界面还是内联表单？

## 相关技能

- **hig-components-menus** —— 按钮和弹出按钮，补充选择控件
- **hig-components-dialogs** —— 包含表单的表单页和弹出框
- **hig-components-search** —— 共享文本输入模式的搜索字段
- **hig-inputs** —— 与控件的键盘、指针、手势交互
- **hig-foundations** —— 控件样式的排版、颜色、布局

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
