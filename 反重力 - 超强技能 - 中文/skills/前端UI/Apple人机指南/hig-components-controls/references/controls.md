---
title: "Controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/controls

# 控件

在 iOS 和 iPadOS 中，控件可从控制中心、锁定屏幕或操作按钮快速访问应用功能。

![控制中心中控件的部分截图，如飞行模式开关、Wi-Fi 开关和 AirPlay 按钮。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/0cea7197d96a9a3bfadc6aed2942b027/components-controls-intro%402x.png)

控件是按钮或开关，可从系统的其他区域快速访问应用功能。控件按钮执行操作、链接到应用的特定区域，或在锁定设备上启动[相机体验](https://developer.apple.com/design/human-interface-guidelines/controls#Camera-experiences-on-a-locked-device)。控件开关在两种状态之间切换，如开和关。

用户可以通过在控制中心的空白区域长按来添加控件到控制中心，通过自定义锁定屏幕添加到锁定屏幕，通过在设置应用中配置操作按钮添加到操作按钮。

## [结构](https://developer.apple.com/design/human-interface-guidelines/controls#Anatomy)

控件包含符号图像、标题和可选的值。符号直观地表示控件的功能，可以是 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 中的符号或自定义符号。标题描述控件关联的内容，值表示控件的状态。例如，标题可以显示房间中灯的名称，而值可以显示它是开还是关。

![显示控件开关的符号图像、标题和值位置的示意图。](https://docs-assets.developer.apple.com/published/df1b5eb2796a6452c640b746948df228/control-medium-anatomy%402x.png)

控件根据出现位置以不同方式显示信息：

* 在控制中心，控件显示其符号，在较大尺寸下还显示标题和值。

* 在锁定屏幕，控件显示其符号。

* 在分配了控件的操作按钮的 iPhone 设备上，长按会在灵动岛中显示控件的符号及其值（如果有）。




![iPhone 上控制中心的部分截图，高亮显示静音模式控件处于活动状态，带有划线的铃铛符号和红色色调。](https://docs-assets.developer.apple.com/published/01a84972ab485b0b33d4342bd1b1a42a/control-control-center%402x.png)

控制中心中的控件开关

![iPhone 锁定屏幕底部的部分截图，高亮显示右侧静音模式控件处于活动状态，带有划线的铃铛符号和红色色调。](https://docs-assets.developer.apple.com/published/912ae3e318cf61d7146965079dc682cb/control-lock-screen%402x.png)

锁定屏幕上的控件开关

![iPhone 主屏幕顶部显示灵动岛的部分截图，显示静音模式控件处于活动状态，灵动岛前部区域显示带红色调的划线铃铛符号，后部区域显示红色文字"静音"。](https://docs-assets.developer.apple.com/published/e336ce21634c50e782cfab47988eb576/control-dynamic-island%402x.png)

从操作按钮执行时的灵动岛中的控件开关

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/controls#Best-practices)

**为无需启动应用即可带来最大收益的操作提供控件。** 例如，从控件启动实时活动可创造轻松无缝的体验，让用户了解进度而无需导航到应用保持更新。有关指导，请参阅 [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities)。

**在用户交互、操作完成或通过推送通知远程更新控件。** 更新控件内容以准确反映状态，并显示操作是否仍在进行中。

**选择描述性的符号来暗示控件的行为。** 根据用户添加控件的位置，它可能不显示标题和值，因此符号需要传达足够的控件操作信息。对于控件开关，为开和关状态都提供符号。例如，使用 SF Symbols `door.garage.open` 和 `door.garage.closed` 来表示打开和关闭车库门的控件。有关指导，请参阅 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)。

**使用符号动画来突出状态变化。** 对于控件开关，在开和关状态之间设置过渡动画。对于执行有持续时间操作的控件按钮，在操作执行期间无限动画，操作完成时停止动画。有关开发者指导，请参阅 [Symbols](https://developer.apple.com/documentation/Symbols) 和 [`SymbolEffect`](https://developer.apple.com/documentation/Symbols/SymbolEffect)。

**选择与应用品牌配合的色调颜色。** 系统将此色调颜色应用于控件开关开启状态下的符号。当用户从操作按钮执行控件操作时，系统还使用此色调颜色在灵动岛中显示值和符号。有关指导，请参阅 [Branding](https://developer.apple.com/design/human-interface-guidelines/branding)。

![带有灯泡符号的非活动控件开关，未着色。](https://docs-assets.developer.apple.com/published/858a6c878e81223350b2c6175e7edc8d/control-lightbulb-not-tinted%402x.png)关闭状态下未着色的控件开关

![带有灯泡符号的活动控件开关，着黄色。](https://docs-assets.developer.apple.com/published/6beab4a3187d3a10493645eaf5447811/control-lightbulb-tinted%402x.png)开启状态下着色的控件开关

**帮助用户提供系统执行操作所需的额外信息。** 用户可能需要配置控件以执行所需操作——例如，选择房屋中的特定灯来开关。如果控件需要配置，在用户首次添加时提示完成此步骤。用户可以随时重新配置控件。有关开发者指导，请参阅 [`promptsForUserConfiguration()`](https://developer.apple.com/documentation/SwiftUI/ControlWidgetConfiguration/promptsForUserConfiguration\(\))。

![表示具有将选项设置为用户选择值能力的控件。](https://docs-assets.developer.apple.com/published/2862099d2344c5c6576a3c4503b0c0b4/control-configuration-options%402x.png)

**为操作按钮提供提示文本。** 当用户按下操作按钮时，系统显示提示文本帮助他们理解长按时会发生什么。当用户长按操作按钮时，系统执行配置给它的操作。使用动词构建提示文本。有关开发者指导，请参阅 [`controlWidgetActionHint(_:)`](https://developer.apple.com/documentation/SwiftUI/View/controlWidgetActionHint\(_:\)-5yoyh)。

![iPhone 主屏幕的部分截图，显示操作按钮的提示文本。提示文本是"长按静音"。](https://docs-assets.developer.apple.com/published/530aa049e2d419ed4af0e3e4a0fb812e/controls-action-button-coaching-text-on%402x.png)

![iPhone 主屏幕的部分截图，显示操作按钮的提示文本。提示文本是"长按响铃"。](https://docs-assets.developer.apple.com/published/8058fe453e9c21c3654f7917f533a70a/controls-action-button-coaching-text-off%402x.png)

**如果控件标题或值可变，请包含占位符。** 占位符信息告诉用户当标题和值是情境性的时控件做什么。当用户在控制中心或锁定屏幕调出控件库并选择控件时，或在将其分配给操作按钮之前，系统显示此信息。

**设备锁定时隐藏敏感信息。** 设备锁定时，考虑让系统遮盖标题和值以隐藏个人或安全相关信息。指定系统是否也需要遮盖符号状态。如果指定，系统遮盖标题和值，并以关闭状态显示符号。

![中等大小的控件开关，显示灯泡符号、标题和值文本。](https://docs-assets.developer.apple.com/published/3239b45e3faff12f7e0c8faad57ac4da/control-regular-text%402x.png)未隐藏信息的控件开关

![带有遮盖文本的中等大小控件开关。](https://docs-assets.developer.apple.com/published/60fdc68e4ffd056e2ced9b7c49ed6730/control-redacted-text%402x.png)锁定设备上隐藏信息的控件开关

**对影响安全的操作要求认证。** 例如，要求用户解锁设备才能访问锁定或解锁房屋门或启动汽车的控件。有关开发者指导，请参阅 [`IntentAuthenticationPolicy`](https://developer.apple.com/documentation/AppIntents/IntentAuthenticationPolicy)。

## [锁定设备上的相机体验](https://developer.apple.com/design/human-interface-guidelines/controls#Camera-experiences-on-a-locked-device)

如果您的应用支持相机拍摄，从 iOS 18 开始，您可以创建一个控件，在设备锁定时直接启动应用的相机体验。对于拍摄以外的任何任务，用户必须认证并解锁设备才能在应用中完成任务。有关开发者指导，请参阅 [LockedCameraCapture](https://developer.apple.com/documentation/LockedCameraCapture)。

**在应用和相机体验中使用相同的相机 UI。** 共享 UI 利用用户对应用的熟悉度。通过使用相同的 UI，当用户拍摄内容并点击按钮执行其他任务（如发布到社交网络或编辑照片）时，过渡到应用是无缝的。

**提供添加控件的说明。** 帮助用户了解如何添加启动此相机体验的控件。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/controls#Platform-considerations)

_iOS 或 iPadOS 无额外注意事项。macOS、watchOS、tvOS 或 visionOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/controls#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/controls#Related)

[Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)

[Action button](https://developer.apple.com/design/human-interface-guidelines/action-button)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/controls#Developer-documentation)

[LockedCameraCapture](https://developer.apple.com/documentation/LockedCameraCapture)

[WidgetKit](https://developer.apple.com/documentation/WidgetKit)

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/controls#Change-log)

日期| 变更  
---|---  
2024年6月10日| 新页面。  
