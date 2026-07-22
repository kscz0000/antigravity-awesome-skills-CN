---
title: "Collections | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/collections

# 集合

集合管理一组有序的内容，并以可定制且高度视觉化的布局呈现。

![八个图像图标的风格化呈现，分为两行，每行四个。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/8769a85042888c4d649fd21c992b593f/components-collection-view-intro%402x.png)

一般来说，集合非常适合显示基于图像的内容。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices)

**尽可能使用标准的行或网格布局。** 集合默认以水平行或网格显示内容，这是用户期望的简单、有效的外观。避免创建可能使用户困惑或过度吸引注意力的自定义布局。

**对于文本，考虑使用表格而不是集合。** 在可滚动列表中显示文本信息通常更简单、更高效，便于查看和消化。

**使选择项目变得容易。** 如果在集合中访问项目太困难，用户会在到达想要的内容之前感到沮丧并失去兴趣。在图像周围使用足够的内边距，使焦点或悬停效果易于查看，并防止内容重叠。

**必要时添加自定义交互。** 默认情况下，用户可以轻点选择、触摸并按住编辑，以及滑动滚动。如果你的 App 需要，你可以添加更多手势来执行自定义操作。

**考虑使用动画在用户插入、删除或重新排序项目时提供反馈。** 集合支持这些操作的标准动画，你也可以使用自定义动画。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/collections#Platform-considerations)

_macOS、tvOS 或 visionOS 无其他注意事项。watchOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/collections#iOS-iPadOS)

**在进行动态布局更改时要谨慎。** 集合的布局可以动态更改。确保任何更改都有意义且易于跟踪。如果可能，尽量避免在用户查看和交互时更改布局，除非是响应明确的操作。

## [资源](https://developer.apple.com/design/human-interface-guidelines/collections#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/collections#Related)

[列表和表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[图像视图](https://developer.apple.com/design/human-interface-guidelines/image-views)

[布局](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/collections#Developer-documentation)

[`UICollectionView`](https://developer.apple.com/documentation/UIKit/UICollectionView) — UIKit

[`NSCollectionView`](https://developer.apple.com/documentation/AppKit/NSCollectionView) — AppKit
