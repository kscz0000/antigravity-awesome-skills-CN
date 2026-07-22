---
title: "Digital Crown | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/digital-crown

# Digital Crown

Digital Crown 是 Apple Vision Pro 和 Apple Watch 的重要硬件输入方式。

![一张 Digital Crown 旁边弯曲箭头的草图，暗示转动 Digital Crown。图像上叠加了矩形和圆形网格线，并以紫色着色，微妙地反映了原始六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/3b12fdaf898877ad12d62535cea6d032/inputs-digital-crown-intro%402x.png)

在 Apple Vision Pro 和 Apple Watch 上，人们可以使用 Digital Crown 与系统交互；在 Apple Watch 上，人们还可以使用 Digital Crown 与应用交互。

![一张人佩戴 Apple Vision Pro 头部特写照片，食指指向 Digital Crown。](https://docs-assets.developer.apple.com/published/b421afd55a6401eeacedaa088b02d909/digital-crown-apple-vision-pro%402x.png)Apple Vision Pro 上的 Digital Crown

![一张 Apple Watch 特写照片，以角度展示，Digital Crown 在图像中心突出显示。](https://docs-assets.developer.apple.com/published/b557ec51bcbcaac70485ca87eda59c40/digital-crown-apple-watch%402x.png)Apple Watch 上的 Digital Crown

## [Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro)

在 Apple Vision Pro 上，人们使用 Digital Crown 来：

  * 调节音量

  * 调节传送门、环境或在 Full Space 中运行的应用或游戏的沉浸程度（有关指导，请参阅[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)）

  * 重新居中内容，使其位于面前

  * 打开辅助功能设置

  * 退出应用并返回主视图




## [Apple Watch](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Watch)

当人们转动 Digital Crown 时，它会生成信息，你可以使用这些信息来增强或促进与应用的交互，如滚动或操作标准或自定义控件。

从 watchOS 10 开始，Digital Crown 作为导航的主要输入方式承担了更重要的角色。在表盘上，人们转动 Digital Crown 查看 Smart Stack 中的小组件；在主屏幕上，人们使用它垂直浏览应用集合。在应用内，人们转动 Digital Crown 在垂直分页标签之间切换，以及滚动列表视图和可变高度页面。

除了用于导航外，转动 Digital Crown 还会生成信息，你可以使用这些信息来增强或促进与应用的交互，如检查数据或操作标准或自定义控件。

注意

应用不响应 Digital Crown 上的按压，因为 watchOS 保留这些交互用于系统提供的功能，如显示主屏幕。

大多数 Apple Watch 型号为 Digital Crown 提供触觉反馈，这让人们在滚动内容时获得更有触感的体验。默认情况下，当人们将 Digital Crown 转动特定距离时，系统会提供线性的触觉_定位点_——即轻击。某些系统控件（如表格视图）会在新项目滚动到屏幕上时提供定位点。

**将应用的导航锚定到 Digital Crown。** 从 watchOS 10 开始，转动 Digital Crown 是人们在应用内和应用间导航的主要方式。列表、标签和滚动视图都是垂直方向的，让人们可以轻松使用 Digital Crown 在应用界面的重要元素之间移动。在将交互锚定到 Digital Crown 时，也要确保用相应的触摸屏交互来支持它们。

**考虑在不需要导航的上下文中使用 Digital Crown 来检查数据。** 在 Digital Crown 不需要在列表或页面之间导航的上下文中，它是检查应用数据的绝佳工具。例如，在世界时钟中，转动 Digital Crown 会推进所选位置的时间，让人们可以比较各种时间与当前时间。

**为 Digital Crown 交互提供视觉反馈。** 例如，选择器会在人们使用 Digital Crown 时更改当前显示的值。如果你直接跟踪转动，请使用这些数据以编程方式更新界面。如果你不提供视觉反馈，人们可能会认为转动 Digital Crown 在你的应用中没有任何效果。

**更新界面以匹配人们转动 Digital Crown 的速度。** 人们期望转动 Digital Crown 能让他们精确控制界面，因此使用这个速度来确定你进行更改的速度效果很好。避免以让人难以选择值的速率更新内容。

**在应用中合理时使用默认触觉反馈。** 如果触觉反馈在你的应用上下文中感觉不对——例如，如果默认定位点与应用的动画不匹配——请关闭定位点。你还可以调整表格的触觉反馈行为，让它们使用线性定位点而不是基于行的定位点。例如，如果你的表格有高度差异很大的行，线性定位点可能会给人们更一致的体验。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Platform-considerations)

_iOS、iPadOS、macOS 或 tvOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Related)

[反馈](https://developer.apple.com/design/human-interface-guidelines/feedback)

[操作按钮](https://developer.apple.com/design/human-interface-guidelines/action-button)

[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Developer-documentation)

[`WKCrownDelegate`](https://developer.apple.com/documentation/WatchKit/WKCrownDelegate) — WatchKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Change-log)

日期| 变更  
---|---  
2023年12月5日| 添加了 Apple Vision Pro 和 Apple Watch 的插图，并澄清了 visionOS 应用不会直接从 Digital Crown 接收信息。  
2023年6月21日| 更新以包含 visionOS 指导。  
2023年6月5日| 添加了强调 Digital Crown 在导航中核心作用的指南。  
