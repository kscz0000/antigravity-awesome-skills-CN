---
title: "Action button | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/action-button

# 操作按钮

操作按钮将相关操作整合在工具栏或标题栏中的单个图标后。

![操作按钮的样式化呈现，显示展开的操作列表。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/2b3c4d5e6f7g8h9i0j1k/components-action-button-intro%402x.png)

操作按钮帮助您在提供对多个操作的访问的同时保持界面整洁。当用户点击操作按钮时，系统显示包含可用操作的菜单。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/action-button#Best-practices)

**使用操作按钮分组次要操作。** 将最常用的操作放在工具栏中作为单独项目，使用操作按钮分组次要操作。

**将相关操作放在一起。** 在操作按钮菜单中，将逻辑相关的操作分组在一起。使用分隔符分隔不同类型的操作。

**使用清晰的图标。** 操作按钮通常使用省略号图标（•••）或共享图标表示。选择能够传达按钮包含多个操作的图标。

**保持菜单简洁。** 操作按钮菜单应包含合理数量的项目。如果需要提供大量操作，考虑使用子菜单进行组织。

**在菜单栏中也提供操作。** 操作按钮提供快捷方式，但菜单栏是所有命令的主位置。确保操作按钮中的每个操作也可以从菜单栏访问。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/action-button#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/action-button#iOS-iPadOS)

在 iOS 和 iPadOS 中，操作按钮通常出现在导航栏或工具栏中。

**使用系统提供的操作图标。** 系统提供标准的操作图标（方框中的向上箭头），用户已经熟悉。

**将破坏性操作放在菜单末尾。** 如果操作按钮菜单包含破坏性操作（如"删除"），将它们列在菜单末尾并使用红色文本标识。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/action-button#macOS)

在 macOS 中，操作按钮可以出现在工具栏中。

**让用户自定义操作按钮。** 如果您的应用支持工具栏自定义，允许用户将操作按钮添加到或从工具栏中移除。

**支持键盘快捷键。** 为操作按钮菜单中的常用操作分配键盘快捷键。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/action-button#visionOS)

在 visionOS 中，操作按钮出现在窗口的工具栏中。

**使用适合空间界面的图标尺寸。** 确保操作按钮图标足够大以便用户轻松注视和点击。

## [资源](https://developer.apple.com/design/human-interface-guidelines/action-button#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/action-button#Related)

[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/action-button#Developer-documentation)

[`Menu`](https://developer.apple.com/documentation/SwiftUI/Menu) — SwiftUI

[`UIMenu`](https://developer.apple.com/documentation/UIKit/UIMenu) — UIKit
