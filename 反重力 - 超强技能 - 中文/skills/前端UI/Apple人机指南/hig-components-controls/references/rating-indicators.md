---
title: "Rating indicators | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/rating-indicators

# 评分指示器

评分指示器使用一系列水平排列的图形符号（默认为星形）来表示评级等级。

![评分指示器的风格化示意图，表示五颗星中的三颗星评级。图像以红色着色，微妙地呼应了原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/aacce03e9d1c173b00080802bc79ff5d/components-rating-indicators-intro%402x.png)

评分指示器不显示不完整的符号；它会将数值四舍五入，仅显示完整的符号。在评分指示器中，符号之间的间距始终保持一致，不会为了适应组件宽度而拉伸或压缩。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Best-practices)

**让排名调整变得简单。** 展示排名列表时，允许用户直接在行内调整单项排名，无需跳转到单独的编辑页面。

**如果用自定义符号替代星形，请确保其含义清晰。** 星形是一种辨识度极高的排名符号，用户可能不会将其他符号与评级量表关联起来。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Platform-considerations)

 _macOS 无额外注意事项。iOS、iPadOS、tvOS、visionOS 和 watchOS 不支持此组件。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Related)

[评分与评论](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Developer-documentation)

[`NSLevelIndicator.Style.rating`](https://developer.apple.com/documentation/AppKit/NSLevelIndicator/Style/rating) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Change-log)

日期| 变更内容  
---|---  
2022 年 9 月 23 日| 新建页面。  
