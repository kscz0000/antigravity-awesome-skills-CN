---
title: "Edit menus | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/edit-menus

# 编辑菜单

编辑菜单让用户对当前视图中选定的内容进行更改，此外还提供"复制"、"选择"、"翻译"和"查找"等相关命令。

![从选定文本延伸出的编辑菜单的样式化呈现。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/2ee5b60d3d9877b65df7633d0321550a/components-edit-menu-intro%402x.png)

除了文本，编辑菜单的命令还可以应用于多种类型的可选内容，如图像、文件和联系人卡片、图表或地图位置等对象。在 iOS、iPadOS 和 visionOS 中，系统自动检测所选项目的数据类型，这可能导致向编辑菜单添加相关操作。例如，选择地址可以向编辑菜单添加"获取路线"等项目。

编辑菜单在不同平台上的外观和行为略有不同。

* 在 iOS 中，编辑菜单以紧凑的水平列表形式显示命令，当用户触摸并保持或双击以选择视图中的内容时出现。用户可以点击后缘的 V 形将其展开为[上下文菜单](https://developer.apple.com/design/human-interface-guidelines/context-menus)。

* 在 iPadOS 中，编辑菜单的外观取决于用户如何显示它。当用户使用触摸交互显示菜单时，它使用紧凑的水平外观。相比之下，当用户使用键盘或定点设备显示它时，编辑菜单直接在上下文菜单中打开。

* 在 macOS 中，用户可以在编辑任务中访问上下文菜单中的编辑命令，以及通过菜单栏中应用的[编辑菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)访问。

* 在 visionOS 中，用户使用标准的[捏合并保持](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)手势将编辑菜单作为水平栏打开，或者可以在上下文菜单中打开它。

在 tvOS 和 watchOS 体验中编辑内容很少见，因此系统在这些平台中不提供编辑菜单。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Best-practices)

**优先使用系统提供的编辑菜单。** 用户熟悉系统提供组件的内容和行为，因此创建呈现相同命令的自定义菜单是多余的，可能会令人困惑。有关标准编辑菜单命令的列表，请参阅 [`UIResponderStandardEditActions`](https://developer.apple.com/documentation/UIKit/UIResponderStandardEditActions)。

**让用户使用他们已经知道的系统定义交互来显示编辑菜单。** 例如，用户期望在触摸屏上触摸并保持，在 visionOS 中捏合并保持，或使用连接的触控板或键盘进行辅助点击。虽然显示编辑菜单的交互可能因平台而异，但用户不希望学习自定义交互来执行标准任务。

**提供在当前上下文中相关的命令，移除或变暗不适用的命令。** 例如，如果未选择任何内容，请避免显示需要选择的选项，如"复制"或"剪切"。同样，当没有内容可粘贴时，避免显示"粘贴"选项。

**将自定义命令列在相关的系统提供命令附近。** 例如，如果您提供自定义格式命令，可以通过在格式部分中系统提供的命令之后列出它们来帮助维护用户期望的顺序。避免用太多自定义命令让用户不知所措。

**在合理的情况下，让用户选择和复制不可编辑的文本。** 用户欣赏能够将静态内容（如图像标题或社交媒体状态）粘贴到消息、备忘录或网络搜索中。通常，让用户复制内容文本，而不是控件标签。

**尽可能支持撤销和重做。** 与所有菜单一样，编辑菜单在执行操作前不需要确认，因此用户可以轻松使用撤销和重做来恢复以前的状态。有关指导，请参阅[撤销和重做](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)。

**通常，避免实现执行与编辑菜单项相同功能的其他控件。** 用户通常期望在编辑菜单中选择熟悉的编辑命令，或使用标准键盘快捷键。提供冗余控件可能会使界面拥挤，留给您更少的空间来呈现用户可能还不知道的操作。

**必要时区分不同类型的删除命令。** 例如，"删除"菜单项的行为与按删除键相同，但"剪切"菜单项在删除所选内容之前将其复制到系统粘贴板。

## [内容](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Content)

**为自定义命令创建短标签。** 使用简洁描述命令执行的操作的动词或短动词短语。有关指导，请参阅[标签](https://developer.apple.com/design/human-interface-guidelines/labels)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Platform-considerations)

_visionOS 无额外注意事项。tvOS 或 watchOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/edit-menus#iOS-iPadOS)

**确保您的编辑菜单在两种样式中都能良好工作。** 当用户使用多点触控手势显示编辑菜单时，系统显示紧凑的水平样式，当用户使用键盘或定点设备显示它时，显示垂直样式。有关使用垂直菜单布局的指导，请参阅[菜单 > iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/menus#iOS-iPadOS)。

**如有必要，调整编辑菜单的位置。** 根据可用空间，默认菜单位置在插入点或选择上方或下方。系统还显示指向目标内容的视觉指示器。虽然您无法更改菜单的形状或其指针，但可以更改菜单的位置。例如，您可能需要移动菜单以防止它覆盖重要内容或界面的部分。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/edit-menus#macOS)

要了解 macOS 应用编辑菜单中项目的顺序，请参阅[编辑菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)。

## [资源](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Related)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[上下文菜单](https://developer.apple.com/design/human-interface-guidelines/context-menus)

[菜单栏](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

[撤销和重做](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Developer-documentation)

[`UIEditMenuInteraction`](https://developer.apple.com/documentation/UIKit/UIEditMenuInteraction) — UIKit

[`NSMenu`](https://developer.apple.com/documentation/AppKit/NSMenu) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/edit-menus#Change-log)

日期| 变更
---|---
2023年6月21日| 更新以包含 visionOS 的指导。
2022年9月14日| 添加了在 iPadOS 中支持两种编辑菜单样式的指导。
