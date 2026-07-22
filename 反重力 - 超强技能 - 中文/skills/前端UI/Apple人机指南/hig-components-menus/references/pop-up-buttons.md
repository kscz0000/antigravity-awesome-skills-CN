---
title: "Pop-up buttons | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons

# 弹出按钮

弹出按钮显示一个菜单，用户从中选择一个项目，所选项目始终可见。

![弹出按钮的样式化呈现，显示展开的选项菜单。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/3c4d5e6f7g8h9i0j1k2l/components-pop-up-buttons-intro%402x.png)

弹出按钮是让用户从一组互斥选项中进行选择的紧凑方式。与[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)不同，弹出按钮始终显示当前选择。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Best-practices)

**使用弹出按钮进行互斥选择。** 弹出按钮最适合让用户从一组选项中选择一个项目。如果用户需要选择多个项目，使用复选框或其他控件代替。

**显示当前选择。** 弹出按钮始终显示当前选择，帮助用户了解当前状态。

**保持菜单简洁。** 弹出按钮菜单应包含合理数量的项目。如果选项太多，考虑使用其他方式呈现，如表格或列表。

**使用清晰的标签。** 弹出按钮标签需要清晰描述选项。使用简短、描述性的文本。

**在 macOS 中，提供默认选择。** 弹出按钮应始终有一个选中的项目，不要显示空白状态。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#iOS-iPadOS)

在 iOS 和 iPadOS 中，弹出按钮通常使用菜单组件实现。

**使用熟悉的样式。** iOS 和 iPadOS 用户期望弹出按钮使用系统提供的样式。

**考虑使用选择器。** 对于某些选择场景，选择器可能是更好的选择，特别是当选项是日期、时间或大量项目时。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#macOS)

在 macOS 中，弹出按钮是标准控件，出现在许多应用中。

**提供足够的宽度。** 确保弹出按钮足够宽以显示最长的选项。

**支持键盘导航。** 用户应能够使用键盘在弹出按钮选项之间导航。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#visionOS)

在 visionOS 中，弹出按钮使用菜单组件实现。

**使用适合空间界面的尺寸。** 确保弹出按钮足够大以便用户轻松交互。

## [资源](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Related)

[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons#Developer-documentation)

[`Menu`](https://developer.apple.com/documentation/SwiftUI/Menu) — SwiftUI

[`UIButton`](https://developer.apple.com/documentation/UIKit/UIButton) — UIKit

[`NSPopUpButton`](https://developer.apple.com/documentation/AppKit/NSPopUpButton) — AppKit
