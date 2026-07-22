---
title: "Action sheets | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/action-sheets

# 操作表

操作表是一种模态视图，展示与用户发起的操作相关的选择。

![iPhone 底部一组操作表按钮的概念图。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/6102d0ab9e98aa9149e6a929f0576d75/components-action-sheet-intro%402x.png)

开发者说明

使用 SwiftUI 时，可以通过为确认对话框指定[展示修饰符](https://developer.apple.com/documentation/swiftui/view-presentation)在所有平台提供操作表功能。使用 UIKit 时，使用 [`UIAlertController.Style.actionSheet`](https://developer.apple.com/documentation/UIKit/UIAlertController/Style/actionSheet) 在 iOS、iPadOS 和 tvOS 中显示操作表。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Best-practices)

**使用操作表——而非警告框——提供与有意操作相关的选择。** 例如，当用户在 iPhone 的 Mail 中取消正在编辑的邮件时，操作表提供两个选择：删除草稿或保存草稿。虽然警告框也可以帮助用户确认或取消有破坏性后果的操作，但它不提供与操作相关的其他选择。更重要的是，警告框通常是意外的，一般告知用户问题或当前情况的变化，可能需要他们采取行动。参见[警告框](https://developer.apple.com/design/human-interface-guidelines/alerts)。

![iPhone 上 Mail 正在撰写新邮件的部分截图。](https://docs-assets.developer.apple.com/published/d78e3a39898532655eb9155586cdc1e7/action-sheet-iphone-mail%402x.png)

![iPhone 上 Mail 正在撰写新邮件的部分截图，选择取消邮件后操作表打开。操作表展示删除草稿或保存草稿的选择。](https://docs-assets.developer.apple.com/published/fedd171df9ff41645c885d3a428bc190/action-sheet-iphone-mail-delete-action%402x.png)

**谨慎使用操作表。** 操作表提供重要信息和选择，但会中断当前任务。为鼓励用户关注操作表，避免过度使用。

**标题尽量简短，确保单行显示。** 过长的标题难以快速阅读，可能会被截断或需要用户滚动。

**仅在必要时提供消息。** 通常，标题结合当前操作的上下文已足够帮助用户理解选择。

**如有必要，提供取消按钮让用户拒绝可能破坏数据的操作。** 将取消按钮放在操作表底部（watchOS 中放在左上角）。SwiftUI 确认对话框默认包含取消按钮。

**使破坏性选择在视觉上突出。** 对执行破坏性操作的按钮使用破坏性样式，并将这些按钮放在操作表顶部，那里最引人注目。开发者指南参见 [`destructive`](https://developer.apple.com/documentation/SwiftUI/ButtonRole/destructive)（SwiftUI）或 [`UIAlertAction.Style.destructive`](https://developer.apple.com/documentation/UIKit/UIAlertAction/Style-swift.enum/destructive)（UIKit）。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Platform-considerations)

 _macOS 或 tvOS 无其他注意事项。visionOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/action-sheets#iOS-iPadOS)

**使用操作表——而非菜单——提供与操作相关的选择。** 用户习惯在执行可能需要明确选择的操作时看到操作表。相比之下，用户期望在选择显示菜单时看到菜单。

**避免让操作表滚动。** 操作表按钮越多，用户做选择所需的时间和精力就越多。此外，滚动操作表时容易误触按钮。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/action-sheets#watchOS)

操作表的系统定义样式包括标题、可选消息、取消按钮和一个或多个其他按钮。此界面的外观因设备而异。

![Apple Watch 上操作表的示意图，显示手表屏幕上半部分代表文本的内容和下半部分两个堆叠按钮。](https://docs-assets.developer.apple.com/published/4ec6a46689c0ec4550d6fe48d4aa27a8/action-sheet-watch-system-defined%402x.png)

每个按钮都有相关样式，传达有关按钮效果的信息。有三种系统定义的按钮样式：

样式| 含义  
---|---  
默认| 按钮无特殊含义。  
破坏性| 按钮销毁用户数据或在应用中执行破坏性操作。  
取消| 按钮关闭视图而不执行任何操作。  
  
**避免在操作表中显示超过四个按钮，包括取消按钮。** 屏幕上按钮较少时，用户更容易一次查看所有选项。由于取消按钮是必需的，目标是最多提供三个其他选择。

## [资源](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Related)

[模态](https://developer.apple.com/design/human-interface-guidelines/modality)

[表单](https://developer.apple.com/design/human-interface-guidelines/sheets)

[警告框](https://developer.apple.com/design/human-interface-guidelines/alerts)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Developer-documentation)

[`confirmationDialog(_:isPresented:titleVisibility:actions:)`](https://developer.apple.com/documentation/SwiftUI/View/confirmationDialog\(_:isPresented:titleVisibility:actions:\)-46zbb) — SwiftUI

[`UIAlertController.Style.actionSheet`](https://developer.apple.com/documentation/UIKit/UIAlertController/Style/actionSheet) — UIKit
