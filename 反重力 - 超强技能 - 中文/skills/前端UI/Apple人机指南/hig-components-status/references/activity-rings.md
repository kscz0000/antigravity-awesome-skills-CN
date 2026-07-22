---
title: "Activity rings | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/activity-rings

# 活动圆环

活动圆环显示个人每日"移动"、"锻炼"和"站立"目标的完成进度。

![一组移动、锻炼和站立活动圆环的示意性表示，表示进度。图片带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/715b90d471efa2d8c388287bc5fe1700/components-activity-ring-intro%402x.png)

在 watchOS 中，活动圆环元素始终包含三个圆环，其颜色和含义与"健身"应用提供的一致。在 iOS 中，活动圆环元素包含单个"移动"圆环（表示活动量的近似值），或在配对 Apple Watch 时显示全部三个圆环。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Best-practices)

**当活动圆环与应用目的相关时显示它们。** 如果你的应用与健康或健身相关，尤其是向 HealthKit 贡献信息的应用，用户通常期望在界面中找到活动圆环。例如，如果你围绕活动圆环的完成来构建锻炼或健康课程，考虑在锻炼指标屏幕上显示该元素，以便用户在课程期间追踪进度。同样，如果你在锻炼结束时提供摘要屏幕，可以显示活动圆环帮助用户查看每日目标的完成进度。

![一张进行中锻炼屏幕的截图，显示当前计时器值，后跟当前移动、锻炼和站立值的列表。屏幕还显示活动圆环图像，每个圆环的状态表示当前值。](https://docs-assets.developer.apple.com/published/868194b00a492b5d029cb3737ee7c7b9/activity-rings-summary%402x.png)

**仅使用活动圆环显示移动、锻炼和站立信息。** 活动圆环旨在一致地表示这些特定领域的进度。不要复制或修改活动圆环用于其他目的。绝不要使用活动圆环显示其他类型的数据。绝不要在其他类似圆环的元素中显示移动、锻炼和站立进度。

**使用活动圆环显示单人的进度。** 绝不要使用活动圆环表示多人的数据，并确保通过标签、照片或头像明确显示这是谁的进度。

**无论在哪里显示，始终保持活动圆环的视觉外观一致。** 遵循以下准则以提供一致的体验：

  * 绝不要更改圆环的颜色；例如，不要使用滤镜或修改不透明度。

  * 始终在黑色背景上显示活动圆环。

  * 首选将圆环和背景包含在圆形内。为此，调整包围视图的圆角半径，而不是应用圆形遮罩。

  * 确保黑色背景在最外层圆环周围保持可见。如有必要，在圆环外边缘添加细黑色描边，避免包含渐变、阴影或任何其他视觉效果。

  * 始终适当缩放圆环，使其看起来不脱节或不协调。

  * 必要时设计周围界面与圆环融合；绝不要更改圆环以与周围界面融合。




**显示与活动圆环直接关联的标签或数值时，使用匹配的颜色。** 要显示圆环特定的标签"移动"、"锻炼"和"站立"，或显示每个人每个圆环的当前值和目标值，使用以下颜色，指定为 RGB 值。

移动| 锻炼| 站立  
---|---|---  
![R-250,G-17,B-79](https://docs-assets.developer.apple.com/published/f347174d08cc485cd465646660bce083/activity-rings-color-swatch-red%402x.png)| ![R-166,G-255,B-0](https://docs-assets.developer.apple.com/published/462bfbf466935f89dcc63b1c79aa0a7a/activity-rings-color-swatch-green%402x.png)| ![R-0,G-255,B-246](https://docs-assets.developer.apple.com/published/a766fb1cbeeacd0434ca05b581168f1a/activity-rings-color-swatch-blue%402x.png)  
  
**保持活动圆环边距。** 活动圆环元素必须包含不小于圆环间距的最小外边距。绝不允许其他元素裁剪、遮挡或侵入此边距或圆环本身。

**将其他类似圆环的元素与活动圆环区分开。** 混合不同圆环样式可能导致视觉混乱的界面。如果必须包含其他圆环，使用内边距、线条或标签将它们与活动圆环分隔开。颜色和比例也有助于提供视觉分隔。

**不要发送重复"健身"应用信息的通知。** 系统已经传递移动、锻炼和站立进度更新，因此用户从你的应用收到冗余信息会感到困惑。此外，不要在应用通知中显示活动圆环元素。在通知中引用活动进度是可以的，但要以应用独特的方式进行，不要复制系统提供的相同信息。

**不要将活动圆环用于装饰。** 活动圆环向用户提供信息；它们不只是美化应用设计。绝不要在标签或背景图形中显示活动圆环。

**不要将活动圆环用于品牌标识。** 严格在应用中使用活动圆环显示活动进度。绝不要在应用图标或营销材料中使用活动圆环。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Platform-considerations)

_iPadOS 或 watchOS 无额外注意事项。macOS、tvOS 或 visionOS 不支持。_

### [iOS](https://developer.apple.com/design/human-interface-guidelines/activity-rings#iOS)

活动圆环在 iOS 中通过 [`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView) 提供。活动圆环元素的外观根据是否配对 Apple Watch 自动变化：

  * 配对 Apple Watch 时，iOS 显示全部三个活动圆环。

  * 未配对 Apple Watch 时，iOS 仅显示移动圆环，表示基于用户步数和其他应用锻炼信息的活动量近似值。




![配对 Apple Watch 时 iOS"健身"应用中活动摘要的截图。显示全部三个活动圆环。](https://docs-assets.developer.apple.com/published/eab44acde68216f8cbace4a59594b7b6/activity-rings-watch-paired%402x.png)

已配对 Apple Watch

![未配对 Apple Watch 时 iOS"健身"应用中活动摘要的截图。仅显示移动圆环。](https://docs-assets.developer.apple.com/published/ef6b2bf87ac8e2917dae8283236c2965/activity-rings-no-watch-paired%402x.png)

未配对 Apple Watch

由于 iOS 无论是否配对 Apple Watch 都显示活动圆环，活动历史可能包含两种样式的组合。例如，"健身"中的活动圆环在用户配对 Apple Watch 锻炼时显示三个圆环，在未配对 Apple Watch 锻炼时仅显示移动圆环。

## [资源](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Related)

[Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Developer-documentation)

[`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView) — HealthKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/12499BF9-8217-4A56-81CA-5E7CB66904DD/9856_wide_250x141_1x.jpg) Track workouts with HealthKit on iOS and iPadOS ](https://developer.apple.com/videos/play/wwdc2025/322)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/30D3C2CB-B24D-467A-9B20-A369641E966F/4850_wide_250x141_1x.jpg) Build a workout app for Apple Watch ](https://developer.apple.com/videos/play/wwdc2021/10009)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/50551741-78CD-4E8A-9550-7D0EC29D7882/8035_wide_250x141_1x.jpg) Build custom workouts with WorkoutKit ](https://developer.apple.com/videos/play/wwdc2023/10016)

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Change-log)

日期| 变更  
---|---  
2024年3月29日| 增强了显示活动圆环的指导，并列出了显示相关内容的具体颜色。  
2023年12月5日| 添加了 iOS 中活动圆环的图示。  
