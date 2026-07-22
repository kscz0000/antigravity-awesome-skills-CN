---
title: "陀螺仪和加速度计 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer

# 陀螺仪和加速度计

设备上的陀螺仪和加速度计可以提供有关设备在物理世界中运动的数据。

![一张陀螺仪的草图，暗示运动。图像上叠加了矩形和圆形网格线，并以紫色着色，微妙地反映了原始六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/d095e989767ecf0537fa99b6ea46b50a/inputs-gyroscope-intro%402x.png)

你可以使用加速度计和陀螺仪数据，在 iOS、iPadOS 和 watchOS 上运行的应用和游戏中，基于实时运动信息提供体验。tvOS 应用可以使用 Siri Remote 的陀螺仪数据。有关开发者指导，请参阅 [Core Motion](https://developer.apple.com/documentation/CoreMotion)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Best-practices)

**仅在有实际益处时使用运动数据。** 例如，健身应用可能使用数据来提供有关人们活动和整体健康的反馈，游戏可能使用数据来增强游戏体验。避免仅仅为了拥有数据而收集数据。

重要

如果你的体验需要从设备访问运动数据，你必须提供解释原因的文案。当你的应用或游戏首次尝试访问此类数据时，系统会在权限请求中包含你的文案，人们可以授予或拒绝访问。

**在活跃游戏之外，避免使用加速度计或陀螺仪直接操作界面。** 某些基于运动的手势可能难以精确复制，对某些人来说可能在身体上具有挑战性，并且可能影响电池使用。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Platform-considerations)

_iOS、iPadOS、macOS、tvOS、visionOS 或 watchOS 无额外注意事项。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Related)

[反馈](https://developer.apple.com/design/human-interface-guidelines/feedback)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Developer-documentation)

[Getting processed device-motion data](https://developer.apple.com/documentation/CoreMotion/getting-processed-device-motion-data) — Core Motion

#### [视频](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/5077B5B0-643B-4E31-9C5E-6E766326D3F3/5225_wide_250x141_1x.jpg) 用运动测量健康 ](https://developer.apple.com/videos/play/wwdc2021/10287)
