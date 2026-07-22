---
title: "Alerts | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/alerts

# 警告框

警告框向用户提供需要立即关注的关键信息。

![警告框模型的概念图，包含标题、描述、主按钮和次按钮。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/89439ba152693e294fbb3298c00b2b48/components-alert-intro%402x.png)

例如，警告框可以告知用户问题、在操作可能破坏数据时发出警告，并让用户有机会确认购买或其他重要操作。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices)

**谨慎使用警告框。** 警告框提供重要信息，但会中断当前任务。确保每个警告框只提供必要信息和有用操作，以鼓励用户关注。

**避免仅用于提供信息的警告框。** 用户不喜欢被仅提供信息但无操作价值的警告框打断。如果只需提供信息，优先在相关上下文中寻找其他方式传达。例如，当服务器连接不可用时，Mail 显示一个指示器，用户可以选择了解更多。

**避免为常见的可撤销操作显示警告框，即使是破坏性操作。** 例如，用户每次删除邮件或文件时不需要警告数据丢失，因为他们的意图就是丢弃数据，而且可以撤销操作。相比之下，当用户执行不常见且不可撤销的破坏性操作时，显示警告框很重要，以防误操作。

**避免在应用启动时显示警告框。** 如果需要在用户打开应用时立即通知新信息或重要信息，设计一种让信息易于发现的方式。如果应用在启动时检测到问题（如无网络连接），考虑其他方式告知用户。例如，可以显示缓存或占位数据，以及描述问题的非侵入性标签。

## [结构](https://developer.apple.com/design/human-interface-guidelines/alerts#Anatomy)

警告框是一种模态视图，在不同平台和设备上外观可能不同。

  * iOS 
  * macOS 
  * tvOS 
  * visionOS 
  * watchOS 



![iPhone 屏幕中央警告框的示意图。](https://docs-assets.developer.apple.com/published/ec9df875e228750105a393c96279bea5/alert-ios%402x.png)

![Mac 屏幕中央警告框的示意图。](https://docs-assets.developer.apple.com/published/0dfc6fd9de495ce3b7201169d829d760/alert-macos%402x.png)

![tvOS 警告框的示意图。](https://docs-assets.developer.apple.com/published/63dde83c2b156231420f095a4d9dfae3/alert-tvos%402x.jpg)

![Apple Vision Pro 警告框的示意图。](https://docs-assets.developer.apple.com/published/1abb6467cc401af501648da039b2b317/alert-visionos%402x.png)

![Apple Watch 警告框的示意图。](https://docs-assets.developer.apple.com/published/a452534204f5ddb4aaa6ba7679946f2e/alert-watchos%402x.png)

## [内容](https://developer.apple.com/design/human-interface-guidelines/alerts#Content)

在所有平台上，警告框显示标题、可选的说明文本和最多三个按钮。某些平台上，警告框可以包含其他元素。

  * 在 iOS、iPadOS、macOS 和 visionOS 中，警告框可以包含文本字段。

  * macOS 和 visionOS 的警告框可以包含图标和附件视图。

  * macOS 警告框可以添加抑制[复选框](https://developer.apple.com/design/human-interface-guidelines/toggles#Checkboxes)和[帮助按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Help-buttons)。





**所有警告框文案应直接、语气中性且亲切。** 警告框通常描述问题和严重情况，避免含糊其辞、指责或掩盖问题严重性。

**编写清晰简洁的标题。** 帮助用户快速理解情况，完整且具体，但不要冗长。尽可能描述发生了什么、在什么上下文中发生以及原因。避免编写不传达有用信息的标题——如"错误"或"发生错误 329347"——但也避免超过两行的过长标题。如果标题是完整句子，使用[句子式大写](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64)和适当的结束标点。如果标题是句子片段，使用标题式大写，不加结束标点。

**仅在有价值时包含说明文本。** 如需添加说明消息，尽可能简短，使用完整句子、句子式大写和适当标点。

**避免解释警告框按钮。** 如果警告框文本和按钮标题清晰，无需解释按钮功能。在极少数需要提供选择按钮指导的情况下，使用"选择"等词语以适应用户当前设备和交互方式，并使用按钮的确切标题引用按钮（不加引号）。参见[按钮](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons)。

**如支持，仅在需要用户输入来解决问题时包含文本字段。** 例如，可能需要显示安全文本字段来接收密码。

## [按钮](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons)

**创建简洁、合乎逻辑的按钮标题。** 力求用一两个词描述选择按钮的结果。优先使用与警告框文本直接相关的动词和动词短语——例如"查看全部"、"回复"或"忽略"。仅在纯信息性警告框中，可以使用"确定"表示接受，避免使用"是"和"否"。始终使用"取消"作为取消警告框操作的按钮标题。与所有按钮标题一样，使用[标题式大写](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64)且不加结束标点。

**避免将"确定"作为默认按钮标题，除非警告框纯属信息性。** 即使在要求用户确认操作的警告框中，"确定"的含义也可能不清楚。例如，"确定"是表示"确定，我想完成操作"还是"确定，我现在理解我的操作会造成的负面后果"？具体的按钮标题如"抹掉"、"转换"、"清除"或"删除"有助于用户理解他们正在采取的操作。

**将按钮放在用户期望的位置。** 通常，将用户最可能选择的按钮放在按钮行的右侧或按钮堆栈的顶部。始终将默认按钮放在行的右侧或堆栈的顶部。取消按钮通常位于行的左侧或堆栈的底部。

**使用破坏性样式标识用户非故意选择的破坏性操作按钮。** 例如，当用户故意选择破坏性操作——如清空废纸篓——生成的警告框不会对"清空废纸篓"按钮应用破坏性样式，因为该按钮执行的是用户的原始意图。在这种情况下，按 Return 键确认故意选择的清空废纸篓操作的便利性，超过了重申按钮具有破坏性的好处。相比之下，用户会感激一个能引起他们注意可能执行非预期破坏性操作的按钮的警告框。

**如果有破坏性操作，包含取消按钮，让用户有明确、安全的方式避免该操作。** 始终使用"取消"作为取消警告框操作的按钮标题。注意不要让取消按钮成为默认按钮。如果想鼓励用户阅读警告框而不是自动按 Return 键关闭，避免让任何按钮成为默认按钮。同样，如果必须显示只有一个按钮且该按钮也是默认按钮的警告框，使用完成按钮，而非取消按钮。

**在合理情况下提供取消警告框的其他方式。** 除了选择取消按钮，用户还喜欢使用键盘快捷键或其他快速方式取消屏幕上的警告框。例如：

操作| 平台  
---|---  
退出到主屏幕| iOS, iPadOS  
在连接的键盘上按 Escape (Esc) 或 Command-句号 (.)| iOS, iPadOS, macOS, visionOS  
在遥控器上按菜单键| tvOS  
  
## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/alerts#Platform-considerations)

 _tvOS 或 watchOS 无其他注意事项。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/alerts#iOS-iPadOS)

**使用操作表——而非警告框——提供与有意操作相关的选择。** 例如，当用户取消正在编辑的 Mail 邮件时，操作表提供三个选择：删除编辑（或整个草稿）、保存草稿或返回编辑。虽然警告框也可以帮助用户确认或取消有破坏性后果的操作，但它不提供与操作相关的其他选择。参见[操作表](https://developer.apple.com/design/human-interface-guidelines/action-sheets)。

**尽可能避免显示需要滚动的警告框。** 虽然如果文本大小足够大，警告框可能会滚动，但务必通过保持警告框标题简短并仅在必要时包含简短消息来最小化滚动的可能性。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS)

macOS 自动在警告框中显示应用图标，但您可以提供替代图标或符号。此外，macOS 允许您：

  * 配置重复警告框，让用户可以抑制相同警告框的后续出现。

  * 在需要提供额外信息时附加自定义视图（开发者指南参见[`accessoryView`](https://developer.apple.com/documentation/AppKit/NSAlert/accessoryView)）。

  * 包含打开帮助文档的帮助按钮（参见[帮助按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Help-buttons)）。





**谨慎使用警告符号。** 在警告框中过于频繁地使用警告符号（如 `exclamationmark.triangle`）会削弱其重要性。仅在确实需要额外注意时使用该符号，如确认可能导致意外数据丢失的操作。不要将该符号用于唯一目的是覆盖或删除数据的任务，如保存或清空废纸篓。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/alerts#visionOS)

当应用在共享空间中运行时，visionOS 在应用窗口前方显示警告框，沿 z 轴略微向前。

带自定义控件的视频。 

内容描述：visionOS 共享空间中 Freeform 应用运行时的警告框视频。视频播放时，有人选择永久删除最近删除的 Freeform 看板。然后警告框出现在 Freeform 窗口前请求确认。 

播放 

如果有人移动窗口而未关闭其警告框，警告框仍锚定在窗口上。如果应用在全空间中运行，系统会在佩戴者的[视野](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Field-of-view)中央显示警告框。

带自定义控件的视频。 

内容描述：visionOS 共享空间中 Freeform 应用运行时的警告框视频。视频播放时，有人选择永久删除最近删除的 Freeform 看板。然后警告框出现在 Freeform 窗口前请求确认。警告框未被关闭，在 Freeform 窗口在共享空间中移动时仍锚定在窗口上。 

播放 

如需在 visionOS 警告框中显示附件视图，请创建最大高度为 154 pt、圆角半径为 16 pt 的视图。

## [资源](https://developer.apple.com/design/human-interface-guidelines/alerts#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/alerts#Related)

[模态](https://developer.apple.com/design/human-interface-guidelines/modality)

[操作表](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

[表单](https://developer.apple.com/design/human-interface-guidelines/sheets)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/alerts#Developer-documentation)

[`alert(_:isPresented:actions:)`](https://developer.apple.com/documentation/SwiftUI/View/alert\(_:isPresented:actions:\)-1bkka) — SwiftUI

[`UIAlertController`](https://developer.apple.com/documentation/UIKit/UIAlertController) — UIKit

[`NSAlert`](https://developer.apple.com/documentation/AppKit/NSAlert) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/alerts#Change-log)

日期| 更改  
---|---  
2024年2月2日| 增强了使用默认按钮和取消按钮的指导。  
2023年9月12日| 添加了 visionOS 的结构图示。  
2023年6月21日| 更新以包含 visionOS 指导。  
  
