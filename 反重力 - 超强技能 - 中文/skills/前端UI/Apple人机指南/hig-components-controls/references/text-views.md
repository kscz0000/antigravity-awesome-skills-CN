---
title: "Text views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/text-views

# 文本视图

文本视图显示多行、样式化的文本内容，可以选择可编辑。

![包含文本的字段的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/21cb3b13c0de850f2eef9a9c7ec14754/components-text-view-intro%402x.png)

文本视图可以是任何高度，当内容超出视图时允许滚动。默认情况下，文本视图中的内容与前边缘对齐并使用系统标签颜色。在 iOS、iPadOS 和 visionOS 中，如果文本视图可编辑，当用户选择视图时会出现键盘。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices)

**当需要显示长、可编辑或特殊格式的文本时使用文本视图。** 文本视图与[文本字段](https://developer.apple.com/design/human-interface-guidelines/text-fields)和[标签](https://developer.apple.com/design/human-interface-guidelines/labels)的不同之处在于它们为显示专用文本和接收文本输入提供最多的选项。如果需要显示少量文本，使用标签更简单——如果文本可编辑——使用文本字段。

**保持文本可读。** 虽然您可以以创造性的方式使用多种字体、颜色和对齐方式，但保持内容的可读性至关重要。采用动态类型是个好主意，这样如果用户在设备上更改文本大小，您的文本仍然看起来不错。确保在启用无障碍选项（如粗体文本）的情况下测试内容。有关指导，请参阅[无障碍](https://developer.apple.com/design/human-interface-guidelines/accessibility)和[排版](https://developer.apple.com/design/human-interface-guidelines/typography)。

**让有用的文本可选择。** 如果文本视图包含有用的信息，如错误消息、序列号或 IP 地址，请考虑让用户选择并复制它以粘贴到其他地方。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/text-views#Platform-considerations)

_macOS、visionOS 或 watchOS 无额外注意事项。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/text-views#iOS-iPadOS)

**显示适当的键盘类型。** 有多种不同的键盘类型可用，每种都设计用于促进不同类型的输入。为了简化数据输入，编辑文本视图时显示的键盘需要适合内容类型。有关指导，请参阅[虚拟键盘](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/text-views#tvOS)

您可以在 tvOS 中使用文本视图显示文本。由于 tvOS 中的文本输入设计上是最小的，tvOS 使用[文本字段](https://developer.apple.com/design/human-interface-guidelines/text-fields)来处理可编辑文本。

## [资源](https://developer.apple.com/design/human-interface-guidelines/text-views#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/text-views#Related)

[Labels](https://developer.apple.com/design/human-interface-guidelines/labels)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/text-views#Developer-documentation)

[`Text`](https://developer.apple.com/documentation/SwiftUI/Text) — SwiftUI

[`UITextView`](https://developer.apple.com/documentation/UIKit/UITextView) — UIKit

[`NSTextView`](https://developer.apple.com/documentation/AppKit/NSTextView) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/text-views#Change-log)

日期| 变更  
---|---  
2023年6月5日| 更新指导以反映 watchOS 10 的变化。  
