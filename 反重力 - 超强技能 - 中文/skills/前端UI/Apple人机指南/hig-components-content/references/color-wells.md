---
title: "Color wells | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/color-wells

# 颜色井

颜色井让用户可以调整文本、形状、参考线和其他屏幕元素的颜色。

![从展开按钮向下延伸的颜色选择弹出窗口的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/8ed8273449a04a1de75d9f183c19d062/components-color-well-intro%402x.png)

当用户轻点或点击颜色井时，它会显示颜色选择器。这个颜色选择器可以是系统提供的，也可以是你设计的自定义界面。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/color-wells#Best-practices)

**考虑使用系统提供的颜色选择器以获得熟悉的体验。** 使用内置颜色选择器可提供一致的体验，此外还让用户可以保存一组可从任何 App 访问的颜色。系统定义的颜色选择器还可以帮助在 iOS、iPadOS 和 macOS 之间开发 App 时提供熟悉的体验。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/color-wells#Platform-considerations)

_iOS、iPadOS 或 visionOS 无其他注意事项。tvOS 或 watchOS 不支持。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/color-wells#macOS)

当用户点击颜色井时，它会收到高亮以提供视觉确认它处于活动状态。然后它打开颜色选择器，让用户可以选择颜色。在他们做出选择后，颜色井会更新以显示新颜色。

颜色井还支持拖放，因此用户可以将颜色从一个颜色井拖到另一个，以及从颜色选择器拖到颜色井。

## [资源](https://developer.apple.com/design/human-interface-guidelines/color-wells#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/color-wells#Related)

[颜色](https://developer.apple.com/design/human-interface-guidelines/color)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/color-wells#Developer-documentation)

[`UIColorWell`](https://developer.apple.com/documentation/UIKit/UIColorWell) — UIKit

[`UIColorPickerViewController`](https://developer.apple.com/documentation/UIKit/UIColorPickerViewController) — UIKit

[`NSColorWell`](https://developer.apple.com/documentation/AppKit/NSColorWell) — AppKit

[Color Programming Topics](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/DrawColor/DrawColor.html)
