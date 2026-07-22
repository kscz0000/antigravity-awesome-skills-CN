---
name: hig-components-menus
description: "提问前检查 .claude/apple-design-context.md。使用现有上下文，仅询问未覆盖的信息。当用户要求'设计菜单或按钮'、'Apple HIG 菜单指南'、'macOS/iOS 菜单栏'、'上下文菜单'、'工具栏设计'时使用。"
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG：菜单与按钮

提问前检查 `.claude/apple-design-context.md`。使用现有上下文，仅询问未覆盖的信息。

## 核心原则

1. **菜单应具备上下文相关性和可预测性。** 标准项目位于标准位置。遵循平台约定进行排序和分组。

2. **使用标准按钮样式。** 系统定义的样式传达可操作性并保持视觉一致性。优先使用而非自定义设计。

3. **工具栏用于频繁操作。** 最常用的命令放在工具栏中。很少使用的操作放在菜单中。

4. **菜单栏是 macOS 的主要命令界面。** 每个命令都可从菜单栏访问。工具栏和上下文菜单是补充，而非替代。

5. **上下文菜单用于次要操作。** 右键或长按，与指针下的项目相关。永远不要将命令仅放在上下文菜单中。

6. **弹出按钮用于互斥选项。** 从一组选项中精确选择一个。

7. **下拉按钮用于操作列表。** 无当前选择；它们提供一组命令。

8. **操作按钮将相关操作整合** 在工具栏或标题栏中的单个图标后。

9. **展开控件用于渐进式披露。** 显示或隐藏附加内容。

10. **Dock 菜单：简短且聚焦** 于应用运行时最有用的操作。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [menus.md](references/menus.md) | 通用菜单设计 | 项目排序、分组、快捷键 |
| [context-menus.md](references/context-menus.md) | 上下文菜单 | 右键、长按、次要操作 |
| [dock-menus.md](references/dock-menus.md) | Dock 菜单 | macOS 应用级操作、运行状态 |
| [edit-menus.md](references/edit-menus.md) | 编辑菜单 | 撤销、复制、粘贴、标准项目 |
| [the-menu-bar.md](references/the-menu-bar.md) | 菜单栏 | macOS 主要命令界面、结构 |
| [toolbars.md](references/toolbars.md) | 工具栏 | 频繁操作、自定义、位置 |
| [buttons.md](references/buttons.md) | 按钮 | 系统样式、尺寸、可操作性 |
| [action-button.md](references/action-button.md) | 操作按钮 | 分组次要操作、工具栏使用 |
| [pop-up-buttons.md](references/pop-up-buttons.md) | 弹出按钮 | 互斥选项选择 |
| [pull-down-buttons.md](references/pull-down-buttons.md) | 下拉按钮 | 操作列表、无当前选择 |
| [disclosure-controls.md](references/disclosure-controls.md) | 展开控件 | 渐进式披露、显示/隐藏 |

## 输出格式

1. **组件推荐** —— 使用哪种菜单或按钮类型及原因。
2. **视觉层次** —— 界面内的位置、尺寸、分组。
3. **平台特定行为** —— 跨 iOS、iPadOS、macOS、visionOS。
4. **键盘快捷键** (macOS) —— 菜单项和工具栏操作的标准及自定义快捷键。

## 需要询问的问题

1. 哪些平台？
2. 主要还是次要操作？
3. 需要提供多少个操作？
4. macOS 菜单栏应用？

## 相关技能

- **hig-components-search** —— 搜索字段、页面控件与工具栏和菜单并存
- **hig-components-controls** —— 开关、选择器、分段控件与按钮互补
- **hig-components-dialogs** —— 警告、表单、弹出框由菜单项或按钮触发
- **hig-inputs** —— 键盘快捷键和指针交互与菜单和工具栏

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 何时使用
此技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
