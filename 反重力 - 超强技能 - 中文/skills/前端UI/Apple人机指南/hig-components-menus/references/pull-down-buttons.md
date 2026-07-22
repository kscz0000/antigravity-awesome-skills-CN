---
title: "Pull-down buttons | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons

# 下拉按钮

下拉按钮显示一个包含操作或选项列表的菜单，不显示当前选择。

![下拉按钮的样式化呈现，显示展开的操作菜单。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/4d5e6f7g8h9i0j1k2l3m/components-pull-down-buttons-intro%402x.png)

下拉按钮提供对相关操作的访问，类似于[操作按钮](https://developer.apple.com/design/human-interface-guidelines/action-button)。与[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)不同，下拉按钮不显示当前选择。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Best-practices)

**使用下拉按钮提供操作列表。** 下拉按钮最适合让用户从一组相关操作中选择。如果需要让用户选择一个选项（而非操作），使用弹出按钮代替。

**使用清晰的图标或标签。** 下拉按钮应使用清晰传达其用途的图标或标签。例如，使用共享图标表示共享操作。

**保持菜单简洁。** 下拉按钮菜单应包含合理数量的项目。如果需要提供大量操作，考虑使用子菜单进行组织。

**将破坏性操作放在菜单末尾。** 如果下拉按钮菜单包含破坏性操作（如"删除"），将它们列在菜单末尾并使用红色文本标识。

**在菜单栏中也提供操作。** 下拉按钮提供快捷方式，但菜单栏是所有命令的主位置。

## [下拉按钮与弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Pull-down-vs-pop-up-buttons)

了解何时使用下拉按钮与弹出按钮：

| 下拉按钮| 弹出按钮
---|---|---
用途| 操作列表| 选项选择
当前选择| 不显示| 始终显示
标签| 描述按钮功能| 显示当前选择
典型用途| 共享、导出、工具| 字体选择、视图选项

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#iOS-iPadOS)

在 iOS 和 iPadOS 中，下拉按钮使用菜单组件实现。

**使用熟悉的样式。** iOS 和 iPadOS 用户期望下拉按钮使用系统提供的样式。

**考虑使用操作按钮。** 在工具栏中，操作按钮可能是分组次要操作的更好选择。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#macOS)

在 macOS 中，下拉按钮是标准控件，出现在工具栏和其他位置。

**使用描边样式。** macOS 下拉按钮通常使用描边边框样式。

**支持键盘快捷键。** 为下拉按钮菜单中的常用操作分配键盘快捷键。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#visionOS)

在 visionOS 中，下拉按钮使用菜单组件实现。

**使用适合空间界面的尺寸。** 确保下拉按钮足够大以便用户轻松交互。

## [资源](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Related)

[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)

[操作按钮](https://developer.apple.com/design/human-interface-guidelines/action-button)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons#Developer-documentation)

[`Menu`](https://developer.apple.com/documentation/SwiftUI/Menu) — SwiftUI

[`UIMenu`](https://developer.apple.com/documentation/UIKit/UIMenu) — UIKit

[`NSPullDownButton`](https://developer.apple.com/documentation/AppKit/NSPullDownButton) — AppKit
