---
title: "Disclosure controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/disclosure-controls

# 展开控件

展开控件显示和隐藏与控件关联的内容或功能。

![展开控件的样式化呈现，显示展开和折叠状态。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/5e6f7g8h9i0j1k2l3m4n/components-disclosure-controls-intro%402x.png)

展开控件帮助您实现渐进式披露——仅在用户需要时显示相关信息和功能。这种方法可以简化界面并帮助用户专注于当前任务。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Best-practices)

**使用展开控件实现渐进式披露。** 展开控件最适合显示和隐藏与当前任务或选择相关的附加内容。

**提供清晰的视觉指示。** 用户需要能够轻松识别展开控件并理解其当前状态。使用三角形或 V 形图标表示展开状态。

**使用描述性标签。** 展开控件标签应描述隐藏的内容。例如，使用"高级选项"而不是"显示更多"。

**保持隐藏内容相关。** 展开控件隐藏的内容应与控件标签相关。不要使用展开控件隐藏不相关的内容。

**提供平滑的动画。** 当用户展开或折叠控件时，使用平滑的动画过渡。这帮助用户理解内容的变化。

**考虑默认状态。** 决定展开控件默认是展开还是折叠。如果隐藏的内容经常使用，考虑默认展开。

## [展开控件与折叠列表](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-vs-outline)

了解何时使用展开控件与折叠列表：

| 展开控件| 折叠列表
---|---|---
用途| 显示/隐藏单个内容区域| 显示/隐藏层次数据
典型位置| 侧边栏、设置面板| 导航、文件浏览器
内容类型| 设置、选项、详情| 层次数据结构

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#iOS-iPadOS)

在 iOS 和 iPadOS 中，展开控件通常使用列表样式实现。

**使用系统提供的样式。** iOS 和 iPadOS 提供标准的展开控件样式，用户已经熟悉。

**支持动态类型。** 展开控件标签需要支持动态类型，以便用户可以调整文本大小。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#macOS)

在 macOS 中，展开控件是标准控件，出现在设置窗口和侧边栏中。

**使用三角形图标。** macOS 展开控件使用指向右侧（折叠）或向下（展开）的三角形图标。

**支持键盘导航。** 用户应能够使用键盘展开和折叠控件。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#visionOS)

在 visionOS 中，展开控件使用列表样式实现。

**使用适合空间界面的尺寸。** 确保展开控件足够大以便用户轻松交互。

## [资源](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Related)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[侧边栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)

[列表](https://developer.apple.com/design/human-interface-guidelines/lists)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Developer-documentation)

[`DisclosureGroup`](https://developer.apple.com/documentation/SwiftUI/DisclosureGroup) — SwiftUI

[`OutlineGroup`](https://developer.apple.com/documentation/SwiftUI/OutlineGroup) — SwiftUI

[`NSDisclosureViewController`](https://developer.apple.com/documentation/AppKit/NSDisclosureViewController) — AppKit
