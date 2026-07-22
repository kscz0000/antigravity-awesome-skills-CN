---
title: "Status bars | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/status-bars

# 状态栏

状态栏出现在屏幕上边缘，显示设备当前状态的信息，如时间、蜂窝运营商和电量。

![iPhone 状态栏的示意性表示，带有显示时间和蜂窝、Wi-Fi 和电量水平的标签。图片带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/f26343633aeaea4ae5297fae42787bf2/components-status-bar-intro%402x.png)

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/status-bars#Best-practices)

**遮挡状态栏下方的内容。** 默认情况下，状态栏背景是透明的，允许下方内容透出。这种透明度可能使状态栏中呈现的信息难以查看。如果控件在状态栏后方可见，用户可能会尝试与之交互但无法做到。务必保持状态栏可读，不要暗示其后方内容可交互。首选使用滚动边缘效果在状态栏后方放置模糊视图。开发者指南见 [`ScrollEdgeEffectStyle`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle) 和 [`UIScrollEdgeEffect`](https://developer.apple.com/documentation/UIKit/UIScrollEdgeEffect)。

**显示全屏媒体时考虑临时隐藏状态栏。** 当用户专注于媒体时，状态栏可能分散注意力。临时隐藏这些元素以提供更沉浸的体验。例如，"照片"应用在用户浏览全屏照片时隐藏状态栏和其他界面元素。

![iPhone 上"照片"应用上半部分的截图，显示一张照片填满屏幕。状态栏在屏幕顶部可见。](https://docs-assets.developer.apple.com/published/7312261e2309c5707b50e5361375c651/status-bar-visible%402x.png)

状态栏可见时的"照片"应用

![iPhone 上"照片"应用上半部分的截图，显示一张照片填满屏幕。状态栏已隐藏，仅显示照片。](https://docs-assets.developer.apple.com/published/546831607b77b71bf7928e60e9949e9b/status-bar-hidden%402x.png)

状态栏隐藏时的"照片"应用

**避免永久隐藏状态栏。** 没有状态栏，用户必须离开应用才能查看时间或检查是否有 Wi-Fi 连接。让用户通过简单、可发现的手势重新显示隐藏的状态栏。例如，在"照片"应用中浏览全屏照片时，单击即可再次显示状态栏。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/status-bars#Platform-considerations)

_iOS 或 iPadOS 无额外注意事项。macOS、tvOS、visionOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/status-bars#Resources)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/status-bars#Developer-documentation)

[`UIStatusBarStyle`](https://developer.apple.com/documentation/UIKit/UIStatusBarStyle) — UIKit

[`preferredStatusBarStyle`](https://developer.apple.com/documentation/UIKit/UIViewController/preferredStatusBarStyle) — UIKit
