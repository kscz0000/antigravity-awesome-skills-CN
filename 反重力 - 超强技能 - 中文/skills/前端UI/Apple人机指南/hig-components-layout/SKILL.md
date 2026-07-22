---
name: hig-components-layout
description: Apple 人机界面指南中关于布局和导航组件的指南。当用户要求设计导航结构、选择布局组件、实现侧边栏/标签栏/分栏视图、或适配多平台布局时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 布局与导航组件

提问前请先检查 `.claude/apple-design-context.md`。使用已有上下文，仅询问未涵盖的信息。

## 核心原则

1. **层级化组织。** 从宽泛类别到具体细节构建信息结构。侧边栏用于顶级分区，列表用于可浏览项，详情视图用于单个内容。

2. **使用标准导航模式。** 标签栏用于平级导航（iPhone）。侧边栏用于深层级导航（iPad、Mac）。根据信息架构和平台匹配模式。

3. **适配屏幕尺寸。** iPad 三栏在 iPhone 上折叠为单栏。使用尺寸类和自适应 API（NavigationSplitView）实现自动适配。

4. **支持 iPad 多任务。** 优雅响应分屏浏览、侧拉和台前调度。在每个分屏比例和尺寸类过渡时测试。

5. **在 visionOS 上保持空间一致性。** 共享空间中的窗口、体积和装饰件。位置可预测。使用装饰件放置工具栏和控件而不遮挡内容。

6. **对溢出内容使用滚动视图。** 为离散内容单元启用分页。适当时支持下拉刷新。尊重安全区域。

7. **保持导航可预测。** 用户应始终知道当前位置、如何到达、如何返回。使用返回按钮、面包屑和清晰的分区标题。

8. **优先使用系统组件。** UINavigationController、UISplitViewController、NavigationSplitView 和 TabView 提供内置自适应性、无障碍支持和状态恢复。

## 参考索引

| 参考 | 主题 | 关键内容 |
|---|---|---|
| [sidebars.md](references/sidebars.md) | 侧边栏 | 源列表、选择状态、可折叠分区、iPad/Mac 模式 |
| [column-views.md](references/column-views.md) | 分栏视图 | Finder 风格浏览、通过分栏渐进展示 |
| [outline-views.md](references/outline-views.md) | 大纲视图 | 可展开层级、展开三角形、树结构 |
| [split-views.md](references/split-views.md) | 分割视图 | 两栏/三栏布局、NavigationSplitView、自适应折叠 |
| [tab-views.md](references/tab-views.md) | 标签视图 | 分段标签、页面式标签、macOS 标签分组 |
| [tab-bars.md](references/tab-bars.md) | 标签栏 | 底部标签栏（iOS）、徽标计数、最大标签数 |
| [scroll-views.md](references/scroll-views.md) | 滚动视图 | 分页、滚动指示器、内容边距、下拉刷新 |
| [windows.md](references/windows.md) | 窗口 | macOS/visionOS 窗口管理、尺寸、全屏、恢复 |
| [panels.md](references/panels.md) | 面板 | 检查器面板、工具面板、浮动面板、macOS 约定 |
| [lists-and-tables.md](references/lists-and-tables.md) | 列表和表格 | Plain/Grouped/InsetGrouped 样式、滑动操作、分区头 |
| [boxes.md](references/boxes.md) | 分组框 | 内容分组容器、带标签分组框、macOS 分组 |
| [ornaments.md](references/ornaments.md) | 装饰件 | visionOS 工具栏附件、定位、可见性 |

## 导航模式选择

| 应用结构 | 推荐模式 | 平台适配 |
|---|---|---|
| 3-5 个平级顶级分区 | 标签栏 | iPhone：底部标签栏。iPad：侧边栏（`.sidebarAdaptable`，iPadOS 18+）。Mac：侧边栏或工具栏标签 |
| 深层级内容 | 侧边栏 + NavigationSplitView | iPhone：单栏堆栈。iPad：两栏/三栏。Mac：完整多栏 |
| 深层文件/文件夹树 | 分栏视图 | Mac：Finder 风格。iPad：可适配。iPhone：推送导航 |
| 带详情的扁平列表 | 分割视图（两栏） | iPhone：推送/弹出堆栈。iPad/Mac：主栏 + 详情栏 |
| 带检查器的文档型应用 | 窗口 + 面板 | Mac：主窗口带检查器。iPad：表单或弹出框 |
| 带工具的空间应用 | 窗口 + 装饰件 | visionOS：窗口上的装饰件。其他平台：工具栏 |

## 布局适配检查清单

- [ ] **紧凑宽度（iPhone 竖屏）：** 导航折叠为单堆栈？标签栏可见？
- [ ] **常规宽度（iPad 横屏、Mac）：** 导航展开为侧边栏 + 详情？空间利用良好？
- [ ] **多任务（iPad）：** 在每个分屏比例下适配？在侧拉中工作？
- [ ] **无障碍：** 所有尺寸支持动态字体？VoiceOver 顺序合理？
- [ ] **方向：** 竖屏和横屏间内容重排？
- [ ] **visionOS：** 窗口位置符合人体工学？装饰件可访问？深度有意义？

## 输出格式

1. **推荐导航模式**及对应用信息架构的理由。
2. **布局层级**从根容器向下（如 TabView > NavigationSplitView > List > Detail）。
3. **平台适配**跨目标平台和尺寸类。
4. **尺寸类行为**在每个过渡点。

## 需要询问的问题

1. 应用的信息架构是什么？（分区、层级深度、顶级类别？）
2. 有多少个顶级分区？
3. 目标平台有哪些？
4. iPad 上需要多任务吗？
5. 使用 SwiftUI 还是 UIKit？

## 相关技能

- **hig-foundations** -- 布局间距、边距、安全区域、对齐
- **hig-platforms** -- 平台特定导航约定
- **hig-patterns** -- 多任务、全屏和启动模式
- **hig-components-content** -- 布局容器内显示的内容

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定验证、测试或专家评审。
- 如果缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清。
