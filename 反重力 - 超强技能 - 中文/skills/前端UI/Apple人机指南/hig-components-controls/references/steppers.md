---
title: "Steppers | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/steppers

# 步进器

步进器是一个双段控件，用户用来递增或递减增量值。

![步进器控件的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/091580d0530042f6685cd17226140173/components-stepper-intro%402x.png)

步进器位于显示其当前值的字段旁边，因为步进器本身不显示值。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/steppers#Best-practices)

**使步进器影响的值显而易见。** 步进器本身不显示任何值，因此确保用户在使用步进器时知道他们正在更改哪个值。

**当可能发生大值变化时，考虑将步进器与文本字段配对。** 步进器本身适用于需要几次点击的小更改。相比之下，用户希望有选项使用字段输入特定值，尤其是当使用的值可能差异很大时。例如，在打印屏幕上，同时有步进器和文本字段来设置副本数可能会有帮助。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/steppers#Platform-considerations)

_iOS、iPadOS 或 visionOS 无额外注意事项。watchOS 或 tvOS 不支持。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/steppers#macOS)

**对于大值范围，考虑支持 Shift 点击以快速更改值。** 如果您的应用受益于步进器值的更大更改，让用户 Shift 点击步进器以超过默认增量的量更改值（例如，默认增量的 10 倍）可能会有用。

## [资源](https://developer.apple.com/design/human-interface-guidelines/steppers#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/steppers#Related)

[Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/steppers#Developer-documentation)

[`UIStepper`](https://developer.apple.com/documentation/UIKit/UIStepper) — UIKit

[`NSStepper`](https://developer.apple.com/documentation/AppKit/NSStepper) — AppKit
