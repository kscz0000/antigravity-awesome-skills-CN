---
title: "Lockups | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/lockups

# Lockup

Lockup 将多个独立的视图组合成一个可交互的单元。

![人物图标位于标题文本行和脚注文本行之上的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/0d5e4d64c6d09fdf802bfebd9ffb5b0e/components-lockups-intro%402x.png)

每个 lockup 由内容视图、页眉和页脚组成。页眉出现在 lockup 的主要内容上方，页脚出现在主要内容下方。当 lockup 获得焦点时，所有三个视图一起扩展和收缩。

根据你的 App 需求，你可以组合四种类型的 lockup：卡片、标题按钮、字母组合和海报。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/lockups#Best-practices)

**在 lockup 之间留出足够的空间。** 获得焦点的 lockup 会扩展尺寸，因此在 lockup 之间留出足够的间距以避免重叠或移动其他 lockup。有关指导，请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

![显示三行五个等距 lockup 的插图。在每行中，中间的 lockup 处于焦点状态，比其他略大。](https://docs-assets.developer.apple.com/published/67a6f9b8d570939f21cd6af73ce21032/lockups-generic%402x.png)

**在一行或一组中使用一致的 lockup 尺寸。** 当所有元素的宽度和高度匹配时，一组按钮或一行内容图像在视觉上更具吸引力。

有关开发者指导，请参阅 [`TVLockupView`](https://developer.apple.com/documentation/TVUIKit/TVLockupView) 和 [`TVLockupHeaderFooterView`](https://developer.apple.com/documentation/TVUIKit/TVLockupHeaderFooterView)。

## [卡片](https://developer.apple.com/design/human-interface-guidelines/lockups#Cards)

卡片结合页眉、页脚和内容视图，呈现媒体项目的评分和评论。

![Apple TV 屏幕的插图，包含多张卡片，其中一张高亮显示。在高亮的卡片中，从顶部开始，占位内容显示评分位置和多行文本。](https://docs-assets.developer.apple.com/published/697a2d112e491e9cf51cf654c70af8e4/lockups-background%402x.png)

有关开发者指导，请参阅 [`TVCardView`](https://developer.apple.com/documentation/TVUIKit/TVCardView)。

## [标题按钮](https://developer.apple.com/design/human-interface-guidelines/lockups#Caption-buttons)

标题按钮可以在按钮下方包含标题和副标题。标题按钮可以包含图像或文本。

确保当用户聚焦时，标题按钮随其滑动的动作倾斜。垂直对齐时，标题按钮上下倾斜。水平对齐时，标题按钮左右倾斜。在网格中显示时，标题按钮同时垂直和水平倾斜。

![Apple TV 屏幕的插图，高亮显示一行中的四个标题按钮。最左边的按钮处于焦点状态，使其略微扩展并似乎漂浮在背景上方。](https://docs-assets.developer.apple.com/published/338475f68a07a861939e2809a0211fbf/lockups-caption-button%402x.png)

有关开发者指导，请参阅 [`TVCaptionButtonView`](https://developer.apple.com/documentation/TVUIKit/TVCaptionButtonView)。

## [字母组合](https://developer.apple.com/design/human-interface-guidelines/lockups#Monograms)

字母组合用于识别人物，通常是媒体项目的演员和工作人员。每个字母组合由人物的圆形图片及其姓名组成。如果图像不可用，则人物的首字母缩写出现在图像位置。

**优先使用图像而非首字母缩写。** 人物的图像比文本创建更亲密的联系。

![Apple TV 屏幕的插图，包含一行多个字母组合，其中最左边的一个高亮显示。每个字母组合包含人物符号。每个字母组合下方是代表两行文本的占位内容。](https://docs-assets.developer.apple.com/published/906c0b8ed8e54f03b24792a684b3b449/lockups-monogram%402x.png)

有关开发者指导，请参阅 [`TVMonogramContentView`](https://developer.apple.com/documentation/TVUIKit/TVMonogramContentView)。

## [海报](https://developer.apple.com/design/human-interface-guidelines/lockups#Posters)

海报由图像和可选的标题及副标题组成，这些文本在海报获得焦点之前隐藏。海报可以是任何尺寸，但尺寸需要适合其内容。有关相关指导，请参阅[图像视图](https://developer.apple.com/design/human-interface-guidelines/image-views)。

![Apple TV 屏幕的插图，显示靠近底部边缘的一行多张海报。一张海报处于焦点状态，其下方是代表一行文本的占位内容。](https://docs-assets.developer.apple.com/published/b37a0a55b2f3902282bd7464422ee054/lockups-poster%402x.png)

有关开发者指导，请参阅 [`TVPosterView`](https://developer.apple.com/documentation/TVUIKit/TVPosterView)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/lockups#Platform-considerations)

_iOS、iPadOS、macOS、visionOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/lockups#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/lockups#Related)

[tvOS 设计](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)

[布局](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/lockups#Developer-documentation)

[`TVLockupView`](https://developer.apple.com/documentation/TVUIKit/TVLockupView) — TVUIKit

[`TVLockupHeaderFooterView`](https://developer.apple.com/documentation/TVUIKit/TVLockupHeaderFooterView) — TVUIKit
