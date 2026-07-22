---
title: "Ornaments | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/ornaments

# 装饰件

在 visionOS 中，装饰件呈现与窗口相关的控件和信息，而不会拥挤或遮挡窗口内容。

![窗口底部装饰件的风格化表示，显示在暗示设计工具画布的网格上方。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/a9012c3e7b1c5d47a4788aefd7a5b48c/components-ornaments-intro%402x.png)

装饰件浮动在与关联窗口平行的平面中，并沿 z 轴略微位于其前方。如果关联窗口移动，装饰件随之移动，保持其相对位置；如果窗口内容滚动，装饰件中的控件或信息保持不变。

装饰件可以出现在窗口的任何边缘，可以包含按钮、分段控件和其他视图等 UI 组件。系统使用装饰件创建和管理[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)、[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)和视频播放控件等组件；您可以使用装饰件创建自定义组件。

## 最佳实践

**考虑使用装饰件在不会使窗口混乱的一致位置呈现经常需要的控件或信息。** 因为装饰件靠近其窗口，人们始终知道在哪里找到它。例如，音乐使用装饰件提供正在播放控件，确保这些控件保持在易于找到的可预测位置。

**通常，保持装饰件可见。** 当人们深入窗口内容时隐藏装饰件可能有意义——例如，当他们观看视频或查看照片时——但在大多数情况下，人们希望能够一致地访问装饰件的控件。

**如果需要显示多个装饰件，请优先考虑窗口的整体视觉平衡。** 装饰件帮助提升重要操作，但有时会分散对内容的注意力。必要时，考虑限制装饰件总数以避免增加窗口的视觉重量并使应用感觉更复杂。如果决定移除装饰件，可以将其元素重新定位到主窗口中。

**力求保持装饰件的宽度与关联窗口的宽度相同或更窄。** 如果装饰件比其窗口宽，它可能会干扰标签栏或窗口侧面的其他垂直内容。

**考虑在装饰件中使用无边框按钮。** 默认情况下，装饰件的背景是[玻璃](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS)，所以如果直接在背景上放置按钮，它可能不需要可见边框。当人们查看装饰件中的无边框按钮时，系统会自动对其应用悬停效果（指南请参阅[眼睛](https://developer.apple.com/design/human-interface-guidelines/eyes)）。

**使用系统提供的工具栏和标签栏，除非需要创建自定义组件。** 在 visionOS 中，工具栏和标签栏自动显示为装饰件，因此您不需要使用装饰件来创建这些组件。开发者指南请参阅 [Toolbars](https://developer.apple.com/documentation/SwiftUI/Toolbars) 和 [`TabView`](https://developer.apple.com/documentation/SwiftUI/TabView)。

## 平台注意事项

iOS、iPadOS、macOS、tvOS 和 watchOS 不支持。

## 资源

#### 相关

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

#### 开发者文档

[`ornament(visibility:attachmentAnchor:contentAlignment:ornament:)`](https://developer.apple.com/documentation/SwiftUI/View/ornament\(visibility:attachmentAnchor:contentAlignment:ornament:\)) — SwiftUI

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/38E4EE32-29B5-4478-B8B6-35B8ACA67B16/8130_wide_250x141_1x.jpg) Design for spatial user interfaces ](https://developer.apple.com/videos/play/wwdc2023/10076)

## 变更日志

日期| 变更
---|---
2024年2月2日| 添加了使用多个装饰件的指南。
2023年12月5日| 删除了关于使用装饰件呈现补充项的声明。
2023年6月21日| 新页面。
