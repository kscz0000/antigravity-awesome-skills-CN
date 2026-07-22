---
title: "Scroll views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/scroll-views

# 滚动视图

滚动视图让人们通过垂直或水平移动内容来查看大于视图边界的内容。

![可滚动图像视图的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/395072e6a9ec2890d242c1d967a7cbe4/components-scroll-view-intro%402x.png)

滚动视图本身没有外观，但它可以显示半透明的滚动指示器，通常在人们开始滚动视图内容后出现。尽管滚动指示器的外观和行为可能因平台而异，但所有指示器都提供有关滚动操作的视觉反馈。例如，在 iOS、iPadOS、macOS、visionOS 和 watchOS 中，指示器显示当前可见内容是否靠近视图的开头、中间或结尾。

## 最佳实践

**支持默认滚动手势和键盘快捷键。** 人们习惯了系统范围的滚动行为，并期望它在任何地方都能工作。如果您为视图构建自定义滚动，请确保您的滚动指示器使用人们期望的弹性行为。

**使内容可滚动时显而易见。** 因为滚动指示器并不总是可见，使内容延伸超出视图时明显是有帮助的。例如，在视图边缘显示部分内容表示该方向有更多内容。尽管大多数人会立即尝试滚动视图以发现是否有额外内容，但引起他们注意是体贴的。

**避免将滚动视图放在具有相同方向的另一个滚动视图内。** 嵌套具有相同方向的滚动视图可能会创建难以控制的不可预测界面。但是，将水平滚动视图放在垂直滚动视图内（或反之亦然）是可以的。

**如果对您的内容有意义，考虑支持逐页滚动。** 在某些情况下，人们欣赏每次交互滚动固定数量的内容而非连续滚动。在大多数平台上，您可以定义此类页面的尺寸——通常是视图的当前高度或宽度——并定义一次滚动一页的交互。为了帮助在逐页滚动期间保持上下文，您可以定义重叠单位，如一行文本、一行字形或图片的一部分，并从页面尺寸中减去该单位。开发者指南请参阅 [`PagingScrollTargetBehavior`](https://developer.apple.com/documentation/SwiftUI/PagingScrollTargetBehavior)。

**在某些情况下，自动滚动以帮助人们找到他们的位置。** 尽管人们发起几乎所有滚动，但当相关内容不再可见时，自动滚动可能有帮助，例如当：

  * 您的应用执行选择内容或将插入点放在当前隐藏区域中的操作时。例如，当您的应用定位人们正在搜索的文本时，滚动内容以将新选择带入视图。

  * 人们开始在当前不可见的位置输入信息时。例如，如果插入点在一页上而人们导航到另一页，一旦他们开始输入文本就滚动回插入点。

  * 当人们进行选择时指针移过视图边缘时。在这种情况下，通过向指针移动的方向滚动来跟随指针。

  * 人们选择某物并在执行选择之前滚动到新位置时。在这种情况下，在执行操作之前滚动直到选择在视图中。




在所有情况下，仅自动滚动必要的内容量以帮助人们保持上下文。例如，如果选择的一部分可见，您不需要将整个选择滚动到视图中。

**如果您支持缩放，请设置适当的最大和最小缩放值。** 例如，在大多数情况下，放大文本直到单个字符填满屏幕是没有意义的。

## 滚动边缘效果

在 iOS、iPadOS 和 macOS 中，滚动边缘效果是一种可变模糊，在内容区域和具有 [Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass) 控件（如[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)）的区域之间提供过渡。在大多数情况下，当固定元素与滚动内容重叠时，系统会自动应用滚动边缘效果。如果您使用自定义控件或布局，效果可能不会出现，您可能需要手动添加。开发者指南请参阅 [`ScrollEdgeEffectStyle`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle) 和 [`UIScrollEdgeEffect`](https://developer.apple.com/documentation/UIKit/UIScrollEdgeEffect)。

滚动边缘效果有两种样式：柔和和硬朗。

  * 在大多数情况下使用 [`soft`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle/soft) 边缘效果，特别是在 iOS 和 iPadOS 中，以提供适用于工具栏和按钮等交互元素的微妙过渡。

  * 主要在 macOS 中使用 [`hard`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle/hard) 边缘效果，以获得更强、更不透明的边界，适用于交互文本、无背景控件或需要额外清晰度的固定表格标题。




**仅在滚动视图与浮动界面元素相邻时使用滚动边缘效果。** 滚动边缘效果不是装饰性的。它们不像叠加层那样阻挡或变暗；它们的存在是为了阐明控件和内容相遇的位置。

**每个视图应用一个滚动边缘效果。** 在 iPad 和 Mac 的分割视图布局中，每个窗格可以有自己的滚动边缘效果；在这种情况下，保持它们高度一致以维持对齐。

## 平台注意事项

tvOS 无额外注意事项。watchOS 不支持。

### iOS、iPadOS

**当滚动视图处于逐页模式时考虑显示页面控件。** [页面控件](https://developer.apple.com/design/human-interface-guidelines/page-controls)显示有多少页面、屏幕或其他内容块可用，并指示当前可见的是哪一个。例如，天气使用页面控件指示人们保存位置之间的移动。如果您在滚动视图中显示页面控件，不要在同一轴上显示滚动指示器，以避免用冗余控件混淆人们。

### macOS

在 macOS 中，滚动指示器通常称为滚动条。

**如有必要，在面板中使用小型或迷你滚动条。** 当空间紧张时，您可以在需要与其他窗口共存的面板中使用较小的滚动条。确保在此类面板中所有控件使用相同尺寸。

### tvOS

tvOS 中的视图可以滚动，但它们不被视为具有滚动指示器的独立对象。相反，当内容超过屏幕尺寸时，系统会自动滚动界面以保持聚焦项目可见。

### visionOS

在 visionOS 中，滚动指示器具有较小的固定尺寸，以帮助传达人们可以高效滚动而无需进行大幅移动。为了易于查找，滚动指示器始终出现在相对于窗口的可预测位置：垂直滚动时在尾端边缘垂直居中，水平滚动时在窗口底部边缘水平居中。

当人们开始向他们想要滚动的方向滑动内容时，滚动指示器出现在窗口边缘，在视觉上加强他们手势的效果并提供有关内容当前位置和总长度的反馈。当人们查看滚动指示器并开始拖动手势时，指示器启用微调栏体验，让人们操纵滚动速度而非内容位置。在此体验中，滚动指示器显示刻度标记，随着人们对他们的手势进行小幅调整而加速或减速，提供帮助人们精确控制滚动加速的视觉反馈。

带有自定义控件的视频。

内容描述：显示 Notes 应用中长页面上滚动指示器的录制。当查看者快速拖动页面时，指示器显示与滚动速度匹配的刻度标记。

播放

**如有必要，考虑滚动指示器的尺寸。** 尽管指示器的整体尺寸较小，但它比 iOS 中相同组件稍厚。如果您的内容使用紧凑边距，请考虑增加边距以防止滚动指示器与内容重叠。

### watchOS

**优先使用垂直滚动内容。** 人们习惯使用数码表冠导航到 Apple Watch 上的应用并在其中导航。如果您的应用包含单个列表或内容视图，当应用的内容高于显示器高度时，旋转数码表冠会垂直滚动。

**使用标签视图提供逐页滚动。** watchOS 将标签视图显示为页面。如果您将标签视图放在垂直堆栈中，人们可以旋转数码表冠在全屏内容页面之间垂直移动。在此场景中，系统在数码表冠旁边显示页面指示器，向人们显示他们在内容中的位置，包括当前页面内和页面集合内。指南请参阅[标签视图](https://developer.apple.com/design/human-interface-guidelines/tab-views)。

**显示分页内容时，考虑将单个页面的内容限制为一个屏幕高度。** 采用此约束可阐明每个页面的目的，帮助您创建更一目了然的设计。但是，如果您的应用有长页面，人们仍然可以使用数码表冠在较短页面之间导航并在较长页面中滚动内容，因为页面指示器在必要时会扩展为滚动指示器。明智地使用可变高度页面，并尽可能将它们放在固定高度页面之后。

## 资源

#### 相关

[Page controls](https://developer.apple.com/design/human-interface-guidelines/page-controls)

[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

[Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

#### 开发者文档

[`ScrollView`](https://developer.apple.com/documentation/SwiftUI/ScrollView)

[`UIScrollView`](https://developer.apple.com/documentation/UIKit/UIScrollView)

[`NSScrollView`](https://developer.apple.com/documentation/AppKit/NSScrollView)

[`WKPageOrientation`](https://developer.apple.com/documentation/WatchKit/WKPageOrientation)

## 变更日志

日期| 变更
---|---
2025年7月28日| 添加了滚动边缘效果的指南。
2024年2月2日| 添加了显示 visionOS 滚动指示器行为的插图。
2023年12月5日| 描述了 visionOS 滚动指示器并添加了将其与窗口布局集成的指南。
2023年6月5日| 更新了在 watchOS 中使用滚动视图的指南。
