---
title: "Activity views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/activity-views

# 活动视图

活动视图（通常称为分享面板）展示一系列可在当前上下文中执行的任务。

![活动视图或分享面板的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/74899abd7c2a017fc05523d112743616/components-activity-view-intro%402x.png)

活动视图展示分享活动（如发消息）和操作（如复制和打印），并提供对常用 App 的快速访问。用户通常在查看页面或文档时选择操作按钮，或在选择项目后打开分享面板。活动视图可以显示为面板或弹出窗口，具体取决于设备和方向。

你可以提供 App 特定的活动，当用户在你的 App 或游戏中打开分享面板时显示。例如，照片提供复制照片、添加到相册、调整位置等 App 特定操作。默认情况下，系统将 App 特定操作列在多 App 或系统范围内可用的操作（如添加到文件或 AirPlay）之前。用户可以编辑操作列表，确保显示最常用的操作并添加新操作。

你还可以创建 App 扩展，提供用户可在其他 App 中使用的自定义分享和操作活动。（App 扩展是你提供的代码，用户可以在 App 外部安装和使用。）例如，你可以创建自定义分享活动，帮助用户将网页分享到特定社交媒体服务。虽然 macOS 不提供活动视图，但你可以创建用户可在 Mac 上使用的分享和操作 App 扩展。有关指导，请参阅[分享和操作扩展](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices)

**避免创建活动视图中已有的常见操作的重复版本。** 例如，提供重复的打印操作是不必要且令人困惑的，因为用户不知道如何区分你的操作和系统提供的操作。如果你需要提供与现有操作类似的 App 特定功能，请为其指定自定义标题。例如，如果你让用户使用自定义格式打印银行交易，请使用帮助用户理解打印活动用途的标题，如"打印交易"。

**考虑使用符号来表示自定义活动。** [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 提供了一套全面的可配置符号，你可以在活动视图中用来传达项目和概念。如果需要创建自定义界面图标，请将其居中放置在约 70x70 像素的区域中。有关指导，请参阅[图标](https://developer.apple.com/design/human-interface-guidelines/icons)。

**为每个自定义操作编写简洁、描述性的标题。** 如果标题太长，系统会换行并可能截断。优先使用单个动词或简短的动词短语，清楚地传达操作的作用。避免在操作标题中包含公司或产品名称。相比之下，分享面板在表示分享活动的图标下方显示其标题（通常是公司名称）。

**确保活动适合当前上下文。** 虽然你无法重新排序活动视图中的系统提供任务，但可以排除不适用于你的 App 的任务。例如，如果你的 App 不适合打印，可以排除打印活动。你还可以确定在任何给定时间显示哪些自定义任务。

**使用分享按钮显示活动视图。** 用户习惯于在选择分享按钮时访问系统提供的活动。避免通过提供替代方式来做同样的事情而使用户困惑。

![iPhone 上备忘录 App 的截图，显示一个打开的备忘录文档，标题为 Nature Walks。顶部工具栏包含一个分享按钮，与其后方的更多按钮组合在一起。](https://docs-assets.developer.apple.com/published/5cdc980290422f59da0f79ab5f5efd13/activity-views-share-button%402x.png)

![iPhone 上备忘录 App 的截图，显示一个打开的备忘录文档，标题为 Nature Walks。从分享按钮打开了一个活动视图，包含与联系人或其他 App 分享文档的控件，以及复制、导出或标记文档的控件。](https://docs-assets.developer.apple.com/published/68a789fa9a70048fcef600615af180fd/activity-views-share-sheet%402x.png)

## [分享和操作扩展](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions)

分享扩展让用户可以方便地将当前上下文中的信息分享给 App、社交媒体账户和其他服务。操作扩展让用户可以启动特定内容的任务（如添加书签、复制链接、编辑内嵌图像或以另一种语言显示选定的文本），而无需离开当前上下文。

系统根据平台以不同方式呈现分享和操作扩展：

* 在 iOS 和 iPadOS 中，分享和操作扩展显示在用户选择操作按钮时出现的分享面板中。

* 在 macOS 中，用户通过点击工具栏中的分享按钮或在上下文菜单中选择分享来访问分享扩展。用户可以通过将指针悬停在某些类型的嵌入内容（如添加到邮件撰写窗口的图像）上、点击工具栏按钮或在 Finder 窗口中选择快速操作来访问操作扩展。

**如有必要，创建用户感觉熟悉的自定义界面。** 对于分享扩展，优先使用系统提供的撰写视图，因为它提供了用户已经熟悉的一致分享体验。对于操作扩展，包含你的 App 名称。如果需要呈现界面，请包含 App 界面的元素，帮助用户理解你的扩展和 App 是相关的。

**简化和限制交互。** 用户欣赏只需几步就能完成任务的扩展。例如，分享扩展可能只需轻点或点击就能立即将图像发布到社交媒体账户。

**避免在扩展上方放置模态视图。** 默认情况下，系统在模态视图中显示扩展。虽然可能需要在扩展上方显示警告，但避免显示额外的模态视图。

**如有必要，提供传达扩展用途的图像。** 分享扩展自动使用你的 App 图标，帮助用户确信你的 App 提供了该扩展。对于操作扩展，优先使用[符号](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)或创建清楚标识任务的界面[图标](https://developer.apple.com/design/human-interface-guidelines/icons)。

**使用主 App 表示长时间操作的进度。** 用户在你的分享或操作扩展中完成任务后，活动视图会立即关闭。如果任务耗时，请在后台继续执行，并为用户提供在主 App 中检查状态的方式。虽然你可以使用通知告知用户问题，但不要仅因为任务完成就通知他们。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/activity-views#Platform-considerations)

_iOS、iPadOS 或 visionOS 无其他注意事项。macOS、tvOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/activity-views#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/activity-views#Related)

[面板](https://developer.apple.com/design/human-interface-guidelines/sheets)

[弹出窗口](https://developer.apple.com/design/human-interface-guidelines/popovers)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/activity-views#Developer-documentation)

[`UIActivityViewController`](https://developer.apple.com/documentation/UIKit/UIActivityViewController) — UIKit

[`UIActivity`](https://developer.apple.com/documentation/UIKit/UIActivity) — UIKit

[App Extension Support](https://developer.apple.com/documentation/Foundation/app-extension-support) — Foundation

#### [视频](https://developer.apple.com/design/human-interface-guidelines/activity-views#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/124/74342B30-92E9-48F3-B0F2-6E42C8FD9391/6506_wide_250x141_1x.jpg) Design for Collaboration with Messages ](https://developer.apple.com/videos/play/wwdc2022/10015)
