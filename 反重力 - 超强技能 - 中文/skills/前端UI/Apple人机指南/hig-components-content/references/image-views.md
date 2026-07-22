---
title: "Image views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/image-views

# 图像视图

图像视图在透明或不透明背景上显示单个图像——或在某些情况下显示动画图像序列。

![照片的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/75a4736b08754bbd37dad68ddd0048b9/components-image-view-intro%402x.png)

在图像视图中，你可以拉伸、缩放、尺寸适配或将图像固定到特定位置。图像视图通常不可交互。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/image-views#Best-practices)

**当视图的主要目的仅仅是显示图像时，使用图像视图。** 在极少数情况下，你可能希望图像可交互，请配置系统提供的[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)来显示图像，而不是向图像视图添加按钮行为。

**如果要在界面中显示图标，考虑使用符号或界面图标而不是图像视图。** [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 提供了大量简化的、基于矢量的图像库，你可以用各种颜色和不透明度渲染。[图标](https://developer.apple.com/design/human-interface-guidelines/icons)（也称为字形或模板图像）通常是位图图像，其中非透明像素可以接收颜色。符号和界面图标都可以使用用户选择的强调色。

## [内容](https://developer.apple.com/design/human-interface-guidelines/image-views#Content)

图像视图可以包含各种格式的丰富图像数据，如 PNG、JPEG 和 PDF。有关更多指导，请参阅[图像](https://developer.apple.com/design/human-interface-guidelines/images)。

**在图像上叠加文本时要小心。** 在图像上方合成文本可能会降低图像的清晰度和文本的可读性。为了帮助改善结果，确保文本与图像对比良好，并考虑使文本对象突出的方法，如添加文本阴影或背景层。

**力求在动画序列中的所有图像使用一致的尺寸。** 当你预先缩放图像以适应视图时，系统不必执行任何缩放。在系统必须进行缩放的情况下，当所有图像具有相同的尺寸和形状时，性能通常更好。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/image-views#Platform-considerations)

_iOS 或 iPadOS 无其他注意事项。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/image-views#macOS)

**如果你的 App 需要可编辑的图像视图，请使用图像井。** [图像井](https://developer.apple.com/design/human-interface-guidelines/image-wells)是支持复制、粘贴、拖动和使用 Delete 键清除其内容的图像视图。

**使用图像按钮而不是图像视图来创建可点击的图像。** [图像按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Image-buttons)包含图像或图标，出现在视图中，并启动瞬时的 App 特定操作。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/image-views#tvOS)

许多 tvOS 图像结合多个具有透明度的图层来创造深度感。有关指导，请参阅[分层图像](https://developer.apple.com/design/human-interface-guidelines/images#Layered-images)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/image-views#visionOS)

visionOS App 和游戏中的窗口可以使用图像视图显示 2D 和立体图像以及空间照片。如果你的 App 使用 RealityKit，你还可以在图像视图外部的 3D 内容旁边显示任何类型的图像，或从现有 2D 图像生成空间场景。有关设计指导，请参阅[图像 > visionOS](https://developer.apple.com/design/human-interface-guidelines/images#visionOS)；有关开发者指导，请参阅 [`ImagePresentationComponent`](https://developer.apple.com/documentation/RealityKit/ImagePresentationComponent)。

有关在窗口或体积中呈现其他 3D 内容的指导，请参阅[窗口 > visionOS](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS)。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/image-views#watchOS)

**尽可能使用 SwiftUI 创建动画。** 或者，如果需要，你可以使用 WatchKit 在图像元素内动画化图像序列。有关开发者指导，请参阅 [`WKImageAnimatable`](https://developer.apple.com/documentation/WatchKit/WKImageAnimatable)。

## [资源](https://developer.apple.com/design/human-interface-guidelines/image-views#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/image-views#Related)

[图像](https://developer.apple.com/design/human-interface-guidelines/images)

[图像井](https://developer.apple.com/design/human-interface-guidelines/image-wells)

[图像按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Image-buttons)

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/image-views#Developer-documentation)

[`Image`](https://developer.apple.com/documentation/SwiftUI/Image) — SwiftUI

[`UIImageView`](https://developer.apple.com/documentation/UIKit/UIImageView) — UIKit

[`NSImageView`](https://developer.apple.com/documentation/AppKit/NSImageView) — AppKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/image-views#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/8226C70F-64DC-4FF1-9956-2DC0751A2143/8241_wide_250x141_1x.jpg) Support HDR images in your app ](https://developer.apple.com/videos/play/wwdc2023/10181)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/5A5D0136-1D36-4754-9603-E9C2B459ECB7/4887_wide_250x141_1x.jpg) Add rich graphics to your SwiftUI app ](https://developer.apple.com/videos/play/wwdc2021/10021)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/image-views#Change-log)

日期| 变更
---|---
2023年6月21日| 更新以包含 visionOS 的指导。
