---
name: hig-components-content
description: Apple 人机界面指南（HIG）内容展示组件。当用户需要设计或开发图表、集合、图像、网页、分享等内容展示组件时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Apple HIG: 内容组件

提问前检查 `.claude/apple-design-context.md`。优先使用已有上下文，仅询问未覆盖的信息。

## 核心原则

1. **适配不同尺寸和场景。** 内容组件必须跨屏幕尺寸、方向和多任务配置正常工作。使用 Auto Layout 和 size classes。

2. **确保内容无障碍。** 图表需要音频图表支持。图像需要替代文本。集合需要正确的 VoiceOver 导航顺序。所有内容组件都需要标签和描述。

3. **保持视觉层级。** 使用间距、尺寸和分组建立清晰的信息层级。主要内容应在视觉上突出。

4. **优先使用系统组件。** 在构建自定义组件前，评估 UICollectionView、SwiftUI Charts、WKWebView。系统组件内置无障碍支持和平台适配。

5. **遵循平台规范。** tvOS 上的集合使用带视差效果的大型 lockup。iOS 上同样的集合使用紧凑的单元格和触摸目标。visionOS 上，内容获得深度和悬停效果。

6. **处理空状态。** 显示有意义的空状态并提供填充指导，而非空白屏幕。

7. **优化性能。** 对大数据集使用懒加载、单元格复用、分页和预取。

## 参考索引

| 参考文档 | 主题 | 关键内容 |
|---|---|---|
| [charts.md](references/charts.md) | 图表 | Swift Charts、柱状/折线/面积/点标记、图表无障碍、音频图表 |
| [collections.md](references/collections.md) | 集合 | 网格/列表布局、组合布局、选择、重排序、可差异数据源 |
| [image-views.md](references/image-views.md) | 图像视图 | 宽高比处理、内容模式、SF Symbol 图像、无障碍 |
| [image-wells.md](references/image-wells.md) | 图像井 | 拖放图像选择、macOS 专用、占位内容 |
| [color-wells.md](references/color-wells.md) | 颜色井 | 颜色选择 UI、系统颜色选择器、自定义色彩空间 |
| [web-views.md](references/web-views.md) | 网页视图 | WKWebView、SFSafariViewController、导航控制、内容限制 |
| [activity-views.md](references/activity-views.md) | 活动视图 | 分享面板、活动项、自定义活动、操作扩展 |
| [lockups.md](references/lockups.md) | Lockup | 图像+文本元素、tvOS 卡片布局、焦点效果、货架布局 |

## 组件选择指南

| 内容需求 | 推荐组件 | 平台说明 |
|---|---|---|
| 可视化定量数据 | Charts (Swift Charts) | iOS 16+、macOS 13+、watchOS 9+ |
| 浏览网格或列表项 | Collection View | 复杂排列使用组合布局 |
| 显示单张图像 | Image View | 支持宽高比适配；提供无障碍描述 |
| 通过拖放或浏览选择图像 | Image Well | 主要用于 macOS；iOS 使用图像选择器 |
| 选择颜色 | Color Well | 触发系统颜色选择器；macOS、iOS 14+ |
| 内嵌显示网页内容 | Web View (WKWebView) | 外部浏览使用 SFSafariViewController |
| 分享内容到其他 App | Activity View | 系统分享面板，可配置活动类型 |
| 内容卡片（图像 + 文本） | Lockup | 主要用于 tvOS；可适配其他平台 |

## 输出格式

1. **组件推荐及理由**，引用相关 HIG 参考文档。
2. **配置指导** — 关键属性和设置。
3. **无障碍要求**，针对推荐组件。
4. **平台特定说明**，针对目标平台。

## 需要询问的问题

1. 内容类型？（定量数据、图像、网页内容、可浏览集合、分享操作？）
2. 目标平台？
3. 静态还是动态内容？
4. 内容量？（少量项目 vs 数百/数千项，影响组件选择和优化。）

## 相关技能

- **hig-foundations** — 颜色、排版、无障碍和图像指南
- **hig-patterns** — 数据可视化、分享和加载模式
- **hig-components-layout** — 托管内容的结构容器（滚动视图、列表、分栏视图）
- **hig-platforms** — 平台特定组件行为（tvOS 上的 lockup、macOS 上的网页视图）

---

*由 [Raintree Technology](https://raintree.technology) 构建 · [更多开发者工具](https://raintree.technology)*

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清。
