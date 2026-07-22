---
title: "空间交互 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/spatial-interactions

# 空间交互

空间交互支持整合附近环境中人员和物体存在的设备端体验。

![一张弯曲线条旁边包含较小圆形的圆形区域的草图，暗示音频从特定方向接近房间中的人。图像上叠加了矩形和圆形网格线，并以紫色着色，微妙地反映了原始六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/4ee9418314d3a8bbdc8e7586a9e3c787/inputs-nearby-interactions-intro%402x.png)

出色的空间交互让人感觉直观自然，因为它建立在人们对周围世界的内在意识之上。例如，在 iPhone 上播放音乐的人可以在将设备靠近时继续在 HomePod mini 上收听，只需将音频输出从 iPhone 传输到 HomePod mini。

空间交互在支持超宽带技术的设备上可用（要了解更多，请参阅 [Ultra Wideband availability](https://support.apple.com/en-us/HT212274)），并依赖于 [Nearby Interaction](https://developer.apple.com/documentation/NearbyInteraction) 框架。在参与空间交互体验之前，人们授权他们的设备在使用你的应用时进行交互。Nearby Interaction API 通过依赖随机生成的设备标识符来帮助保护人们的隐私，这些标识符仅在你的应用发起的交互会话期间有效。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Best-practices)

**从物理世界的角度考虑任务，为空间交互寻找灵感。** 例如，虽然人们可以轻松使用应用的 UI 将歌曲从 iPhone 传输到 HomePod mini，但通过将设备靠近来启动传输使任务感觉根植于物理世界。发现为任务概念提供信息的物理动作可以帮助你创建引人入胜的体验，使执行任务感觉轻松自然。

**使用距离、方向和上下文来指导交互。** 虽然你的应用可能从各种来源获取信息，但优先考虑附近的、上下文相关的信息可以帮助你提供感觉有机的体验。例如，如果人们想在拥挤的房间里与朋友分享内容，iOS 分享表可以通过使用有关人员最频繁和最近联系人的设备端知识来建议可能的接收者。将此知识与来自包含 U1 芯片的附近设备的信息结合，可以让分享表通过建议人员面对的最近联系人来改善体验。

**考虑物理距离的变化如何指导空间交互。** 在物理世界中，人们通常期望他们对物体的感知随着靠近而变得更清晰。空间交互可以通过提供随物体接近度变化的反馈来反映这种体验。例如，当人们使用 iPhone 查找 AirTag 时，显示屏会随着靠近从方向箭头过渡到脉动圆圈。

**提供连续反馈。** 连续反馈反映物理世界的动态性，并加强空间交互与人们正在执行的任务之间的联系。例如，在"查找"中寻找丢失物品时，人们会获得传达物品方向和接近度的连续更新。通过提供响应人们动作的不间断反馈来保持人们的参与度。

**考虑使用多种反馈类型来创建整体体验。** 在视觉、听觉和触觉反馈之间流畅过渡可以帮助空间交互的任务感觉更引人入胜和真实。使用不止一种类型的反馈还让你可以改变体验以协调任务和当前上下文。例如，当人们与设备屏幕交互时，视觉反馈有意义；当人们与环境交互时，听觉和触觉反馈通常效果更好。

**避免将空间交互作为执行任务的唯一方式。** 你不能假设每个人都能体验空间交互，因此必须提供在应用中完成任务的替代方式。

## [设备使用](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Device-usage)

**鼓励人们以纵向方向握持设备。** 以横向握持设备可能会降低其他设备的距离和相对方向信息的准确性和可用性。如果你的空间交互功能运行时仅支持纵向方向，优先给人们隐含的、视觉反馈，说明如何握持设备以获得最佳体验；尽可能避免明确告诉人们以纵向握持设备。

**为设备的方向视野设计。** 空间交互依赖于具有特定视野的硬件传感器，类似于 iPhone 11 及更高版本中的超广角摄像头。如果参与设备在此视野之外，你的应用可能会收到有关其距离的信息，但不会收到其相对方向的信息。

**帮助人们理解介入物体如何影响应用中的空间交互体验。** 当其他人、动物或足够大的物体位于两个参与设备之间时，距离和方向信息的准确性或可用性可能会降低。考虑在你呈现的入门或教程内容中添加有关避免这种情况的建议。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Platform-considerations)

_iPadOS 无额外注意事项。macOS、tvOS 或 visionOS 不支持。_

### [iOS](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#iOS)

在 iPhone 上，Nearby Interaction API 提供对等设备的距离和方向。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#watchOS)

在 Apple Watch 上，Nearby Interaction API 提供对等设备的距离。此外，所有参与空间交互体验的 watchOS 应用必须在前台运行。

## [资源](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Related)

[反馈](https://developer.apple.com/design/human-interface-guidelines/feedback)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Developer-documentation)

[Nearby Interaction](https://developer.apple.com/documentation/NearbyInteraction)

#### [视频](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/0F487599-C14E-48B0-AEB0-A752DFF26E95/5165_wide_250x141_1x.jpg) 为空间交互设计 ](https://developer.apple.com/videos/play/wwdc2021/10245)

[![](https://devimages-cdn.apple.com/wwdc-services/images/49/E6812719-14BF-4392-84FC-E1CFC1650B71/3558_wide_250x141_1x.jpg) 认识 Nearby Interaction ](https://developer.apple.com/videos/play/wwdc2020/10668)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions#Change-log)

日期| 变更  
---|---  
2023年6月21日| 更改页面标题从空间交互。  
