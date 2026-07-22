---
name: hig-components-search
description: Apple HIG 导航相关组件指南，包括搜索字段、页面控件和路径控件。当用户要求"搜索字段"、"页面控件"、"路径控件"、"HIG导航组件"、"Apple搜索设计"时使用。
risk: safe
source: community
date_added: '2026-02-27'
---

# Apple HIG: 导航组件

提问前检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未覆盖的信息。

## 核心原则

1. **搜索：可发现且即时反馈。** 将搜索字段放在用户期望的位置（列表顶部、工具栏/导航栏）。用户输入时即时显示结果。

2. **页面控件：扁平页面序列定位。** 适用于离散、等权重的页面（引导流程、照片画廊）。显示当前页和总页数。

3. **路径控件：文件层级导航。** macOS 路径控件显示目录结构中的位置，允许跳转到任意祖先目录。

4. **搜索范围缩小大型结果集。** 提供范围按钮，让用户无需复杂查询即可过滤。

5. **搜索空状态要清晰。** 提供有用的提示信息，建议修正或替代方案，而非空白屏幕。

6. **页面控件不用于层级导航。** 仅用于扁平、线性序列。层级导航使用导航控制器、标签栏或侧边栏。

7. **保持路径控件简洁。** 仅显示有意义的段落。用户可点击任意段落直接导航。

8. **搜索支持键盘。** Command-F 和系统搜索快捷键应能激活搜索。

## 参考索引

| 参考 | 主题 | 核心内容 |
|---|---|---|
| [search-fields.md](references/search-fields.md) | 搜索字段 | 范围、令牌、即时结果、位置 |
| [page-controls.md](references/page-controls.md) | 页面控件 | 点指示器、扁平页面序列 |
| [path-controls.md](references/path-controls.md) | 路径控件 | 面包屑、祖先导航 |

## 输出格式

1. **组件推荐** —— 搜索字段、页面控件或路径控件，及原因。
2. **行为规范** —— 交互模型（边输入边搜索、滑动翻页、路径点击导航）。
3. **平台差异** —— iOS、iPadOS、macOS、visionOS 的区别。

## 需要询问的问题

1. 搜索或导航的内容类型是什么？
2. 目标平台有哪些？
3. 数据集有多大？
4. 搜索是否为主要交互？

## 相关技能

- **hig-components-menus** —— 托管搜索和导航控件的工具栏和菜单栏
- **hig-components-controls** —— 搜索界面中的文本字段、选择器、分段控件
- **hig-components-dialogs** —— 用于扩展搜索或过滤的弹出框和表单
- **hig-patterns** —— 导航模式和信息架构
- **hig-foundations** —— 导航组件的排版和布局

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
