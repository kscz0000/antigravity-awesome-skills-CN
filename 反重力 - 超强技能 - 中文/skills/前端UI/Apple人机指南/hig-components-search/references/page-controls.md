---
title: "Page controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/page-controls

# 页面控件

页面控件显示一行指示器图像，每个代表扁平列表中的一页。

![A stylized representation of a page control with an indicator denoting the active page. The image is tinted red to subtly reflect the red in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/a0dcd33d7bfca7feb019c4743b89c7c0/components-page-dots-intro%402x.png)

滚动的指示器行帮助用户导航列表找到所需页面。页面控件可以处理任意数量的页面，特别适用于用户可以创建自定义列表的场景。

页面控件默认显示为一系列小指示点，代表可用页面。实心点表示当前页面。视觉上，这些点始终等距排列，如果太多无法在窗口中容纳则会被裁剪。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/page-controls#Best-practices)

**使用页面控件表示有序页面列表间的移动。** 页面控件不代表层级或非顺序的页面关系。对于更复杂的导航，考虑使用侧边栏或分栏视图。

**将页面控件居中放置在视图或窗口底部。** 为确保用户始终知道在哪里找到页面控件，将其水平居中并放置在视图底部附近。

**虽然页面控件可以处理任意数量的页面，但不要显示太多。** 超过约 10 个点很难一目了然地计数。如果应用需要显示超过 10 个对等页面，考虑使用不同的排列方式（如网格），让用户可以按任意顺序导航内容。

## [自定义指示器](https://developer.apple.com/design/human-interface-guidelines/page-controls#Customizing-indicators)

默认情况下，页面控件使用系统提供的点图像作为所有指示器，但也可以显示独特的图像来帮助用户识别特定页面。例如，天气应用使用 `location.fill` 符号来区分当前位置页面。

如果这能增强您的应用或游戏，您可以提供自定义图像作为所有指示器的默认图像，也可以为特定页面提供不同的图像。开发者指南参见 [`preferredIndicatorImage`](https://developer.apple.com/documentation/UIKit/UIPageControl/preferredIndicatorImage) 和 [`setIndicatorImage(_:forPage:)`](https://developer.apple.com/documentation/UIKit/UIPageControl/setIndicatorImage\(_:forPage:\))。

**确保自定义指示器图像简单清晰。** 避免复杂的形状，不要包含负空间、文本或内部线条，因为这些细节会使图标在极小尺寸下变得模糊难辨。考虑使用简单的 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 作为指示器或设计您自己的图标。指南参见 [Icons](https://developer.apple.com/design/human-interface-guidelines/icons)。

**仅在增强页面控件整体含义时自定义默认指示器图像。** 例如，如果列出的每个页面都包含书签，可以使用 `bookmark.fill` 符号作为默认指示器图像。

**避免在页面控件中使用超过两种不同的指示器图像。** 如果列表包含一个具有特殊含义的页面（如天气应用中的当前位置页面），可以通过为其指定独特的指示器图像使其易于查找。相反，使用多个独特图像标记多个重要页面的页面控件很难使用，因为用户必须记住每个图像的含义。显示超过两种类型指示器图像的页面控件往往看起来杂乱无章，即使每个图像都很清晰。

![An illustration that represents the Weather app highlighted to show a page control at the bottom edge of the screen. The page control displays a mix of icons, such as weak sun, cloud, cloud with sun, and cloud with drizzle.](https://docs-assets.developer.apple.com/published/671a959d0a2a6baf234fcc2255b9abdb/page-indicator-customization-incorrect%402x.png)

![An X in a circle to indicate an incorrect example.](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)使用多种不同指示器会使页面控件看起来繁忙且难以使用。

![An illustration that represents the Weather app highlighted to show a page control at the bottom edge of the screen. The page control displays the location symbol on the leading side followed by a series of dots.](https://docs-assets.developer.apple.com/published/b797a18ec978a588e29113b3a9f522b7/page-indicator-customization-correct%402x.png)

![A checkmark in a circle to indicate a correct example.](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)仅使用两种不同指示器看起来井井有条并提供一致的体验。

**避免为指示器图像着色。** 自定义颜色会降低区分当前页面指示器的对比度，使页面控件在屏幕上可见。为确保页面控件易于使用且在不同上下文中看起来良好，让系统自动为指示器着色。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/page-controls#Platform-considerations)

_macOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/page-controls#iOS-iPadOS)

页面控件可以调整指示器的外观以提供关于列表的更多信息。例如，控件高亮当前页面的指示器，以便用户估计页面在列表中的相对位置。当指示器超出空间容纳范围时，控件可以收缩两侧的指示器以提示还有更多页面。

![An illustration of a page control. The page control displays a total of 9 dots. The center 5 dots use the default size; the second and eighth dots are about half the default size and the first and ninth dots are about one quarter the default size. The center dot is filled, indicating the location of the current page in the list.](https://docs-assets.developer.apple.com/published/6413d2970c5a12e6374d83bed419293c/page-controls-many-indicators%402x.png)

用户通过点击或滑动与页面控件交互（_滑动_ 指用户触摸控件并左右拖动）。点击当前页面指示器的前端或尾端显示下一页或上一页；在 iPadOS 中，用户还可以使用指针定位特定指示器。滑动按顺序打开页面，滑动超过控件的前端或尾端边缘帮助用户快速到达第一页或最后一页。

开发者注意

在 API 中，_点击_ 是_离散交互_，而_滑动_ 是_连续交互_；开发者指南参见 [`UIPageControl.InteractionState`](https://developer.apple.com/documentation/UIKit/UIPageControl/InteractionState-swift.enum)。

**避免在滑动过程中动画化页面过渡。** 用户可以非常快地滑动，为每次过渡使用滚动动画会使应用卡顿并导致分散注意力的视觉闪烁。仅为点击使用动画滚动过渡。

页面控件可以包含半透明的圆角矩形背景外观，为指示器提供视觉对比。可以选择以下背景样式之一：

  * 自动 —— 仅在用户与控件交互时显示背景。当页面控件不是 UI 中的主要导航元素时使用此样式。

  * 突出 —— 始终显示背景。仅当控件是屏幕中的主要导航控件时使用此样式。

  * 最小 —— 从不显示背景。当您只想显示当前页面在列表中的位置且不需要在滑动过程中提供视觉反馈时使用此样式。




开发者指南参见 [`backgroundStyle`](https://developer.apple.com/documentation/UIKit/UIPageControl/backgroundStyle-swift.property)。

**使用最小背景样式时避免支持滑动器。** 最小样式在滑动过程中不提供视觉反馈。如果要让用户在应用中滑动页面列表，请使用自动或突出背景样式。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/page-controls#tvOS)

**在全屏页面集合上使用页面控件。** 页面控件设计用于在全屏环境中运行，其中多个内容丰富的页面在页面层级中是对等的。包含额外控件会使在页面间移动时难以保持焦点。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/page-controls#visionOS)

在 visionOS 中，页面控件表示可用页面并指示当前页面，但用户不与它们交互。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/page-controls#watchOS)

在 watchOS 中，页面控件可以显示在屏幕底部用于水平分页，或在呈现垂直[标签视图](https://developer.apple.com/design/human-interface-guidelines/components/layout-and-organization/tab-views)时显示在数码表冠旁边。使用垂直标签视图时，页面指示器向用户显示他们在导航中的位置，包括在当前页面内和页面集合内。页面控件在滚动页面内容和滚动到其他页面之间过渡。

![An illustration representing a screen that includes a vertical tab view on Apple Watch. A page control next to the Digital Crown shows that the fourth tab is currently selected.](https://docs-assets.developer.apple.com/published/d8ac19e2578c57035e74fe697a15d573/page-controls-watch-vertical%402x.png)

垂直页面控件

![An illustration representing a screen that includes a horizontal tab view on Apple Watch. A page control at the bottom shows that the second tab is currently selected.](https://docs-assets.developer.apple.com/published/0f915ec7b0e8755a2d60845617746f71/page-controls-watch-horizontal%402x.png)

水平页面控件

**使用垂直分页将多个视图分离为独立、有目的的页面。** 为每个页面赋予明确的目的，让用户使用数码表冠滚动浏览页面。在 watchOS 中，这种设计比水平分页或多层级的层级导航更有效。

**考虑将单个页面的内容限制为单个屏幕高度。** 遵循此约束鼓励每个页面服务于明确且独特的目的，并产生更易于扫视的设计。谨慎使用可变高度页面，如果可能，仅在应用设计中将其放在固定高度页面之后。

## [资源](https://developer.apple.com/design/human-interface-guidelines/page-controls#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/page-controls#Related)

[Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/page-controls#Developer-documentation)

[`PageTabViewStyle`](https://developer.apple.com/documentation/SwiftUI/PageTabViewStyle) — SwiftUI

[`UIPageControl`](https://developer.apple.com/documentation/UIKit/UIPageControl) — UIKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/page-controls#Change-log)

日期| 变更
---|---
2023年6月21日| 更新以包含 visionOS 指南。
2023年6月5日| 更新了在 watchOS 中使用页面控件的指南。
