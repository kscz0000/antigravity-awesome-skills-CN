---
title: "Context menus | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/context-menus

# 上下文菜单

上下文菜单提供对与项目直接相关的功能的访问，而不会使界面杂乱。

![点击指针下方的上下文菜单的样式化呈现。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/6145c402544704012a48978cf5ceb87a/components-context-menu-intro%402x.png)

虽然上下文菜单提供对常用项目的便捷访问，但默认情况下是隐藏的，因此用户可能不知道它的存在。要显示上下文菜单，用户通常选择视图或选择某些内容，然后使用其当前配置支持的输入模式执行操作。例如：

* visionOS、iOS 和 iPadOS 中的系统定义触摸或捏合并保持手势
* 在 macOS 和 iPadOS 中按住 Control 键的同时单击定点设备
* 在 macOS 或 iPadOS 中使用 Magic Trackpad 上的辅助点击

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/context-menus#Best-practices)

**在选择要包含在上下文菜单中的项目时优先考虑相关性。** 上下文菜单不是用于提供高级或很少使用的项目；相反，它帮助用户快速访问他们在当前上下文中最可能需要的命令。例如，收件箱中邮件的上下文菜单包含回复和移动邮件的命令，但不包含编辑邮件内容、管理邮箱或过滤邮件的命令。

**以少量菜单项为目标。** 过长的上下文菜单可能难以扫描和滚动。

**在整个应用中一致地支持上下文菜单。** 如果您在某些地方为项目提供上下文菜单而在其他地方不提供，用户将不知道在哪里可以使用该功能，可能会认为存在问题。

**始终在主界面中也提供上下文菜单项。** 例如，在 iOS 和 iPadOS 的邮件中，收件箱中邮件可用的上下文菜单项也可以在邮件视图的工具栏中使用。在 macOS 中，应用的菜单栏菜单列出所有应用的命令，包括各种上下文菜单中的命令。

**如果需要使用子菜单来管理菜单的复杂性，请将其保持在一个级别。** 子菜单是显示逻辑相关命令的二级菜单的菜单项。虽然子菜单可以缩短上下文菜单并阐明其命令，但超过一级的子菜单会使体验复杂化，用户可能难以导航。如果需要包含子菜单，请给它一个直观的标题，帮助用户在不打开它的情况下预测其内容。有关指导，请参阅[子菜单](https://developer.apple.com/design/human-interface-guidelines/menus#Submenus)。

**隐藏不可用的菜单项，不要使其变暗。** 与帮助用户发现即使不可用也可以执行的操作的常规菜单不同，上下文菜单仅显示与当前选择的视图或内容相关的操作。在 macOS 中，例外是"剪切"、"复制"和"粘贴"菜单项，如果它们不适用于当前上下文，可能会显示为不可用。

**以将最常用的菜单项放在用户可能首先遇到的位置为目标。** 当上下文菜单打开时，用户通常从最接近其手指或指针显示菜单的位置开始阅读。根据所选内容的位置，上下文菜单可能在其上方或下方打开，因此您可能还需要反转项目的顺序以匹配菜单的位置。

**在应用的主菜单中显示键盘快捷键，而不是在上下文菜单中。** 上下文菜单已经提供了对任务特定命令的快捷方式，因此显示键盘快捷键也是多余的。

**遵循使用分隔符的最佳实践。** 与其他类型的菜单一样，您可以使用分隔符对上下文菜单中的项目进行分组，帮助用户更快地扫描菜单。通常，上下文菜单中不要超过约三个组。有关指导，请参阅[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

**在 iOS、iPadOS 和 visionOS 中，警告用户可能破坏数据的上下文菜单项。** 如果需要在上下文菜单中包含潜在破坏性的项目——如"删除"或"移除"——请将它们列在菜单末尾并将其标识为破坏性（开发者指导见 [`destructive`](https://developer.apple.com/documentation/UIKit/UIMenuElement/Attributes/destructive)）。系统可以使用红色文本颜色显示破坏性菜单项。

## [内容](https://developer.apple.com/design/human-interface-guidelines/context-menus#Content)

上下文菜单很少显示标题。相比之下，上下文菜单中的每个项目都需要显示清晰描述其功能的短标签。有关指导，请参阅[菜单 > 标签](https://developer.apple.com/design/human-interface-guidelines/menus#Labels)。

**仅在有助于阐明菜单效果时才在上下文菜单中包含标题。** 例如，当用户选择多封邮件并在 iOS 和 iPadOS 中点击"标记"工具栏按钮时，生成的上下文菜单显示说明所选邮件数量的标题，提醒用户他们选择的命令会影响他们选择的所有邮件。

**用熟悉的图标表示菜单项操作。** 图标帮助用户在整个应用中识别常见操作。使用与系统相同的图标来表示"复制"、"共享"和"删除"等操作，无论它们出现在哪里。有关表示常见操作的图标列表，请参阅[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。有关其他指导，请参阅[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/context-menus#Platform-considerations)

_tvOS 无额外注意事项。watchOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/context-menus#iOS-iPadOS)

**为项目提供上下文菜单或编辑菜单，但不能同时提供两者。** 如果为同一项目同时提供这两个功能，可能会让用户困惑——系统也难以检测他们的意图。请参阅[编辑菜单](https://developer.apple.com/design/human-interface-guidelines/edit-menus)。

**在 iPadOS 中，考虑使用上下文菜单让用户在应用中创建新对象。** iPadOS 允许您在用户在触摸屏上执行长按或使用连接的触控板或键盘进行辅助点击时显示上下文菜单。例如，文件允许用户通过在现有文件和文件夹之间的区域显示上下文菜单来创建新文件夹。

在 iOS 和 iPadOS 中，上下文菜单可以在命令列表附近显示当前内容的预览。用户可以选择菜单中的命令，或者在某些情况下，可以点击预览打开它或将其拖动到另一个区域。

**优先使用图形预览来阐明上下文菜单命令的目标。** 例如，当用户在备忘录或邮件中的列表项上显示上下文菜单时，预览显示实际内容的精简版本，帮助用户确认他们正在使用预期的项目。

**确保预览在动画时看起来良好。** 当用户在屏幕对象上显示上下文菜单时，系统在预览图像从内容中出现时对其进行动画处理，使预览和菜单后面的屏幕变暗。重要的是调整预览的剪切路径以匹配预览图像的形状，以便其轮廓（如圆角）在动画过程中不会显示为变化。开发者指导见 [`UIContextMenuInteractionDelegate`](https://developer.apple.com/documentation/UIKit/UIContextMenuInteractionDelegate)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/context-menus#macOS)

在 Mac 上，上下文菜单有时称为_contextual menu_。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/context-menus#visionOS)

**考虑使用上下文菜单而不是面板或检查器窗口来呈现常用功能。** 最小化应用打开的单独视图或窗口的数量可以帮助用户保持空间整洁。

**通常，避免让上下文菜单的高度超过窗口的高度。** 在 visionOS 中，窗口在其顶部和底部边缘上方和下方包含系统提供的组件，如窗口管理控件和共享菜单，因此过高的上下文菜单可能会遮挡它们。在考虑要包含的项目数量时，以用户可能使用应用的方式为指导。例如，使用应用完成深入、专业任务的用户通常期望花时间学习大量复杂命令，并可能欣赏对它们的上下文访问。另一方面，使用应用执行几个简单操作的用户可能欣赏快速扫描和使用的简短上下文菜单。

## [资源](https://developer.apple.com/design/human-interface-guidelines/context-menus#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/context-menus#Related)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[编辑菜单](https://developer.apple.com/design/human-interface-guidelines/edit-menus)

[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)

[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/context-menus#Developer-documentation)

[`contextMenu(menuItems:)`](https://developer.apple.com/documentation/SwiftUI/View/contextMenu\(menuItems:\)) — SwiftUI

[`UIContextMenuInteraction`](https://developer.apple.com/documentation/UIKit/UIContextMenuInteraction) — UIKit

[`popUpContextMenu(_:with:for:)`](https://developer.apple.com/documentation/AppKit/NSMenu/popUpContextMenu\(_:with:for:\)) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/context-menus#Change-log)

日期| 变更
---|---
2023年12月5日| 添加了隐藏不可用菜单项的指导。
2023年6月21日| 更新以包含 visionOS 的指导。
2022年9月14日| 完善了包含子菜单的指导，并添加了在 iPadOS 应用中使用上下文菜单支持对象创建的指南。
