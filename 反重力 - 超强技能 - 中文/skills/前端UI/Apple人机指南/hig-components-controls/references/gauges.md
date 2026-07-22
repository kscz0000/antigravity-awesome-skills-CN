---
title: "Gauges | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/gauges

# 仪表

仪表显示特定范围内的当前值、数值或状态。

![仪表的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r/components-gauge-intro%402x.png)

仪表可以显示各种类型的数据，如电池电量、音量级别或存储使用量。仪表通常是只读的，但您也可以让用户与之交互以设置值。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/gauges#Best-practices)

**使用仪表显示范围内的数值。** 仪表非常适合显示在特定范围内的值，如电池电量、音量级别或存储使用量。如果需要显示用户评分，请改用[评分指示器](https://developer.apple.com/design/human-interface-guidelines/rating-indicators)。

**选择合适的仪表样式。** 仪表有多种样式，包括线性、圆形和分段。选择最适合您要显示的数据类型和可用空间的样式。

**提供清晰的标签。** 使用标签来标识仪表显示的内容，并在适当情况下显示当前值。例如，电池仪表可能显示"电池"标签和"85%"值。

**考虑使用颜色来传达状态。** 您可以使用颜色来帮助用户快速了解仪表显示的值的状态。例如，电池仪表可能会在电量低时从绿色变为黄色，在电量极低时变为红色。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/gauges#Platform-considerations)

_iOS、iPadOS、tvOS 或 watchOS 无额外注意事项。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/gauges#macOS)

**使用仪表显示范围内的数值。** 仪表非常适合显示在特定范围内的值，如电池电量、音量级别或存储使用量。

**选择合适的仪表样式。** macOS 提供多种仪表样式，包括容量、评分和连续。选择最适合您要显示的数据类型的样式。

**考虑提供可编辑仪表。** 如果需要让用户设置值，可以将仪表设置为可编辑。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/gauges#visionOS)

**使用仪表显示范围内的数值。** 仪表非常适合显示在特定范围内的值，如电池电量、音量级别或存储使用量。

**选择合适的仪表样式。** visionOS 提供多种仪表样式。选择最适合您要显示的数据类型和可用空间的样式。

## [资源](https://developer.apple.com/design/human-interface-guidelines/gauges#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/gauges#Related)

[Rating indicators](https://developer.apple.com/design/human-interface-guidelines/rating-indicators)

[Sliders](https://developer.apple.com/design/human-interface-guidelines/sliders)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/gauges#Developer-documentation)

[`Gauge`](https://developer.apple.com/documentation/SwiftUI/Gauge) — SwiftUI

[`NSLevelIndicator`](https://developer.apple.com/documentation/AppKit/NSLevelIndicator) — AppKit
