---
title: "Boxes | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/boxes

# 分组框

分组框为逻辑相关的信息和组件创建视觉上明显的分组。

![圆角矩形内一组界面元素的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/6e253271e9888e8d596d1d5b601d90f3/components-box-intro%402x.png)

默认情况下，分组框使用可见边框或背景色将其内容与界面其余部分分隔。分组框也可以包含标题。

## 最佳实践

**保持分组框相对于其包含视图较小。** 当分组框尺寸接近包含窗口或屏幕的尺寸时，它传达分组内容分隔的效果会减弱，并会挤压其他内容。

**考虑使用内边距和对齐来传达分组框内的额外分组。** 分组框的边框是明显的视觉元素——添加嵌套分组框来定义子组会使界面显得拥挤和受限。

## 内容

**如果有助澄清分组框内容，提供简洁的介绍性标题。** 分组框的外观帮助人们理解其内容是相关的，但提供更多关于关系的细节可能有意义。此外，标题可以帮助 VoiceOver 用户预测在分组框中遇到的内容。

**如果需要标题，编写描述内容的简短短语。** 使用句子式大写。避免结尾标点，除非在设置面板中使用分组框，此时在标题后加冒号。

## 平台注意事项

visionOS 无额外注意事项。tvOS 和 watchOS 不支持。

### iOS、iPadOS

默认情况下，iOS 和 iPadOS 在分组框中使用次要和三级背景[颜色](https://developer.apple.com/design/human-interface-guidelines/color)。

### macOS

默认情况下，macOS 在分组框上方显示其标题。

## 资源

#### 相关

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### 开发者文档

[`GroupBox`](https://developer.apple.com/documentation/SwiftUI/GroupBox) — SwiftUI

[`NSBox`](https://developer.apple.com/documentation/AppKit/NSBox) — AppKit
