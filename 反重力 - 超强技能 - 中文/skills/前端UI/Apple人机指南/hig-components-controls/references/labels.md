---
title: "Labels | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/labels

# 标签

标签是一段静态文本，用户可以阅读并经常复制，但不能编辑。

![文本标签的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/b428963465f223dd1fdd01779043810c/components-label-intro%402x.png)

标签在整个界面的按钮、菜单项和视图中显示文本，帮助用户了解当前上下文和接下来可以做什么。

术语_标签_指可以出现在各种位置的可编辑文本。例如：

* 在按钮中，标签通常传达按钮的作用，如编辑、取消或发送。

* 在许多列表中，标签可以描述每个项目，通常伴有符号或图像。

* 在视图中，标签可能通过介绍控件或描述用户可以在视图中执行的常见操作或任务来提供额外的上下文。




开发者说明

要显示可编辑文本，SwiftUI 定义了两个组件：[`Label`](https://developer.apple.com/documentation/SwiftUI/Label) 和 [`Text`](https://developer.apple.com/documentation/SwiftUI/Text)。

以下指导可以帮助您使用标签显示文本。在某些情况下，特定组件的指导——如[操作按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)、[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)和[列表和表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)——包含使用文本的额外建议。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/labels#Best-practices)

**使用标签显示用户不需要编辑的少量文本。** 如果需要让用户编辑少量文本，请使用[文本字段](https://developer.apple.com/design/human-interface-guidelines/text-fields)。如果需要显示大量文本，并可选择让用户编辑，请使用[文本视图](https://developer.apple.com/design/human-interface-guidelines/text-views)。

**优先使用系统字体。** 标签可以显示纯文本或样式化文本，默认支持动态类型（如果可用）。如果调整标签的样式或使用自定义字体，请确保文本保持可读。

**使用系统提供的标签颜色传达相对重要性。** 系统定义了四种标签颜色，外观各异，帮助您给文本不同的视觉重要性级别。有关额外指导，请参阅[颜色](https://developer.apple.com/design/human-interface-guidelines/color)。

系统颜色| 示例用法| iOS、iPadOS、tvOS、visionOS| macOS  
---|---|---|---  
标签| 主要信息| [`label`](https://developer.apple.com/documentation/UIKit/UIColor/label)| [`labelColor`](https://developer.apple.com/documentation/AppKit/NSColor/labelColor)  
次要标签| 副标题或补充文本| [`secondaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/secondaryLabel)| [`secondaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/secondaryLabelColor)  
第三标签| 描述不可用项目或行为的文本| [`tertiaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/tertiaryLabel)| [`tertiaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/tertiaryLabelColor)  
第四标签| 水印文本| [`quaternaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/quaternaryLabel)| [`quaternaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/quaternaryLabelColor)  
  
**让有用的标签文本可选择。** 如果标签包含有用的信息——如错误消息、位置或 IP 地址——请考虑让用户选择并复制它以粘贴到其他地方。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/labels#Platform-considerations)

_iOS、iPadOS、tvOS 或 visionOS 无额外注意事项。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/labels#macOS)

开发者说明

要在标签中显示可编辑文本，请使用 [`NSTextField`](https://developer.apple.com/documentation/AppKit/NSTextField) 的 [`isEditable`](https://developer.apple.com/documentation/AppKit/NSTextField/isEditable) 属性。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/labels#watchOS)

日期和时间文本组件（如下左所示）显示当前日期、当前时间或两者的组合。您可以将日期文本组件配置为使用各种格式、日历和时区。倒计时计时器文本组件（如下右所示）显示精确的倒计时或正计时计时器。您可以将计时器文本组件配置为以各种格式显示其计数值。

![Apple Watch 上日期和时间文本组件的插图，日期与前边缘对齐，时间与后边缘对齐。](https://docs-assets.developer.apple.com/published/3cedf27f398b6683c78d37a325f26c33/labels-date-time-text-component%402x.png)日期和时间标签

![Apple Watch 上倒计时计时器文本组件的插图，时间值居中。](https://docs-assets.developer.apple.com/published/bc3014364c7bc508ff68d21d79c15441/labels-countdown-timer-text-component%402x.png)计时器标签

当您使用系统提供的日期和计时器文本组件时，watchOS 会自动调整标签的呈现以适应可用空间。系统还会更新内容，无需您的应用进一步输入。

考虑在复杂功能中使用日期和计时器组件。有关设计指导，请参阅[复杂功能](https://developer.apple.com/design/human-interface-guidelines/components/system-experiences/complications)；有关开发者指导，请参阅 [`Text`](https://developer.apple.com/documentation/SwiftUI/Text)。

## [资源](https://developer.apple.com/design/human-interface-guidelines/labels#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/labels#Related)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/labels#Developer-documentation)

[`Label`](https://developer.apple.com/documentation/SwiftUI/Label) — SwiftUI

[`Text`](https://developer.apple.com/documentation/SwiftUI/Text) — SwiftUI

[`UILabel`](https://developer.apple.com/documentation/UIKit/UILabel) — UIKit

[`NSTextField`](https://developer.apple.com/documentation/AppKit/NSTextField) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/labels#Change-log)

日期| 变更  
---|---  
2023年6月5日| 更新指导以反映 watchOS 10 的变化。  
