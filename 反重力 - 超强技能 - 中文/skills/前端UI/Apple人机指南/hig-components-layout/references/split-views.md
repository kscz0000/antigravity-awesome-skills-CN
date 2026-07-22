---
title: "Split views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/split-views

# 分割视图

分割视图管理多个相邻内容窗格的呈现，每个窗格可以包含各种组件，包括表格、集合、图像和自定义视图。

![由三个区域组成的窗口的风格化表示：侧边栏、画布和检查器。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/68c529d6dd40b4b46f1862f1cdbadec4/components-split-view-intro%402x.png)

通常，您使用分割视图同时显示应用的多个层级并支持它们之间的导航。在此场景中，选择视图主窗格中的项目会在辅助窗格中显示该项目的内容。同样，如果辅助窗格中的项目包含额外内容，分割视图可以显示第三窗格。

使用分割视图显示用于导航的[侧边栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)很常见，其中前端窗格列出应用中的顶级项目或集合，辅助窗格和可选的第三窗格可以呈现子集合和项目详情。很少情况下，您可能还使用分割视图提供补充主视图的功能组——例如，macOS 中的 Keynote 使用分割视图窗格在环绕主幻灯片画布的区域中呈现幻灯片导航器、演讲者备注和检查器窗格。

## 最佳实践

**为支持导航，在每个通向详情视图的窗格中持久高亮当前选择。** 所选外观阐明各窗格内容之间的关系并帮助人们保持方向。

**考虑让人们在不同窗格之间拖放内容。** 因为分割视图提供对多个层级级别的访问，人们可以通过将项目拖到不同窗格方便地将内容从应用的一个部分移动到另一个部分。指南请参阅[拖放](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop)。

## 平台注意事项

### iOS

**优先在常规——而非紧凑——环境中使用分割视图。** 分割视图需要水平空间来显示多个窗格。在紧凑环境中，如竖屏方向的 iPhone，难以在不换行或截断内容的情况下显示多个窗格，使其可读性和交互性降低。

### iPadOS

在 iPadOS 中，分割视图可以包含两个垂直窗格（如邮件）或三个垂直窗格（如 Keynote）。

**考虑窄、紧凑和中间窗口宽度。** 由于 iPad 窗口可以流畅调整大小，考虑分割视图布局在多个宽度下的设计很重要。特别是，确保可以以逻辑方式在各种窗格之间导航。指南请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)。开发者指南请参阅 [`NavigationSplitView`](https://developer.apple.com/documentation/SwiftUI/NavigationSplitView) 和 [`UISplitViewController`](https://developer.apple.com/documentation/UIKit/UISplitViewController)。

### macOS

在 macOS 中，您可以垂直、水平或两者兼有地排列分割视图的窗格。分割视图在窗格之间包含分隔符，可以支持拖动调整大小。开发者指南请参阅 [`VSplitView`](https://developer.apple.com/documentation/SwiftUI/VSplitView) 和 [`HSplitView`](https://developer.apple.com/documentation/SwiftUI/HSplitView)。

  * 垂直
  * 水平
  * 多个




![显示两个垂直堆叠窗格的笔记本电脑屏幕插图。](https://docs-assets.developer.apple.com/published/8c23f101a012db47a8e2350e50432617/vertical-split-view%402x.png)

![显示两个并排窗格的笔记本电脑屏幕插图，左侧窗格较窄，右侧窗格较宽。](https://docs-assets.developer.apple.com/published/713be8f9e61a9578b26087ad71ca6b23/horizontal-split-view%402x.png)

![显示分为三个窗格的笔记本电脑屏幕插图，垂直和水平分割。](https://docs-assets.developer.apple.com/published/3e315fbb8f8ade8b2d3d4f105f8c4482/multiple-split-view%402x.png)

**为窗格的最小和最大尺寸设置合理的默认值。** 如果人们可以调整应用分割视图中窗格的大小，请确保使用保持分隔符可见的尺寸。如果窗格变得太小，分隔符可能看起来消失，变得难以使用。

**适当时考虑让人们隐藏窗格。** 如果您的应用包含编辑区域，例如，考虑让人们隐藏其他窗格以减少干扰或为编辑腾出更多空间——在 Keynote 中，人们可以在想要编辑幻灯片内容时隐藏导航器和演讲者备注窗格。

**提供多种方式显示隐藏的窗格。** 例如，您可以提供工具栏按钮或菜单命令——包括键盘快捷键——人们可以使用它来恢复隐藏的窗格。

**优先使用细分隔符样式。** 细分隔符宽度为一个点，为您提供最大的内容空间，同时对人们来说仍然易于使用。除非有特定需要，否则避免使用较粗的分隔符样式。例如，如果分隔符两侧都呈现使用强线性元素的表格行，这可能使细分隔符难以区分，使用较粗的分隔符可能有效。开发者指南请参阅 [`NSSplitView.DividerStyle`](https://developer.apple.com/documentation/AppKit/NSSplitView/DividerStyle-swift.enum)。

### tvOS

在 tvOS 中，分割视图可以很好地帮助人们过滤内容。当人们在主窗格中选择过滤类别时，您的应用可以在辅助窗格中显示结果。

**选择保持窗格看起来平衡的分割视图布局。** 默认情况下，分割视图将屏幕宽度的三分之一用于主窗格，三分之二用于辅助窗格，但您也可以指定一半一半的布局。

**在分割视图上方显示单个标题，帮助人们将内容作为一个整体理解。** 人们已经知道如何使用分割视图导航和过滤内容；他们不需要描述每个窗格包含什么的标题。

**根据辅助窗格包含的内容类型选择标题的对齐方式。** 具体来说，当辅助窗格包含内容集合时，考虑将标题在窗口中居中。相比之下，如果辅助窗格包含重要内容的单个主视图，考虑将标题放在主视图上方以给内容更多空间。

### visionOS

**为显示补充信息，优先使用分割视图而非新窗口。** 分割视图让人们方便地访问更多信息而无需离开当前上下文，而新窗口可能会混淆正在尝试导航或重新定位内容的人们。打开更多窗口还需要您仔细管理应用或游戏中视图之间的关系。如果您需要请求少量信息或呈现人们在返回主任务之前必须完成的简单任务，请使用[表单](https://developer.apple.com/design/human-interface-guidelines/sheets)。

### watchOS

在 watchOS 中，分割视图将列表视图或详情视图显示为全屏视图。

**自动显示最相关的详情视图。** 当您的应用启动时，向人们显示最相关的信息。例如，显示与他们的位置、时间或最近操作相关的信息。

**如果您的应用显示多个详情页面，将详情视图放在垂直[标签视图](https://developer.apple.com/design/human-interface-guidelines/tab-views)中。** 人们随后可以使用数码表冠在详情视图的标签之间滚动。watchOS 还在数码表冠旁边显示页面指示器，指示标签数量和当前选中的标签。

![显示 Apple Watch 上带有垂直标签的详情视图的截图。数码表冠旁边的页面指示器显示当前选中第五个标签。](https://docs-assets.developer.apple.com/published/3f36258648d54880e800568e88b5076b/split-view-watch-vertical-tab%402x.png)

## 资源

#### 相关

[Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)

[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### 开发者文档

[`NavigationSplitView`](https://developer.apple.com/documentation/SwiftUI/NavigationSplitView) — SwiftUI

[`UISplitViewController`](https://developer.apple.com/documentation/UIKit/UISplitViewController) — UIKit

[`NSSplitViewController`](https://developer.apple.com/documentation/AppKit/NSSplitViewController) — AppKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/A8CAF870-197F-4982-83D8-56513E5D7D0B/10000_wide_250x141_1x.jpg) Make your UIKit app more flexible ](https://developer.apple.com/videos/play/wwdc2025/282)

## 变更日志

日期| 变更
---|---
2025年6月9日| 添加了 iOS 和 iPadOS 平台注意事项。
2023年12月5日| 添加了 visionOS 中分割视图的指南。
2023年6月5日| 添加了 watchOS 中分割视图的指南。
