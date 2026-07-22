---
title: "Sidebars | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/sidebars

# 侧边栏

侧边栏出现在视图的前端，让人们导航应用或游戏中的不同分区。

![窗口顶部显示标题、分区和一些文件夹的侧边栏的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/d8bde769da53e8facee9d89e4362b83c/components-sidebar-intro%402x.png)

侧边栏浮动在内容上方而不锚定到视图边缘。它提供应用信息层级的宽广、扁平视图，让人们同时访问多个对等内容区域或模式。

侧边栏需要大量垂直和水平空间。当空间有限或您想将更多屏幕用于其他信息或功能时，更紧凑的控件如[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)可能提供更好的导航体验。指南请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

## 最佳实践

**将内容延伸到侧边栏下方。** 在 iOS、iPadOS 和 macOS 中，与其他控件如工具栏和标签栏一样，侧边栏浮动在 [Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass) 层中的内容上方。为了加强侧边栏的分隔和浮动外观，通过让其水平滚动或应用背景扩展视图将内容延伸到其下方，背景扩展视图镜像相邻内容以产生将其拉伸到侧边栏下方的印象。开发者指南请参阅 [`backgroundExtensionEffect()`](https://developer.apple.com/documentation/SwiftUI/View/backgroundExtensionEffect\(\))。

![iPad 上应用前端侧面的截图。图像跨越窗口上部，停在侧边栏边缘。](https://docs-assets.developer.apple.com/published/d50ee5db90fbe0cae8f34304aa315053/sidebars-extend-content-beneath-sidebar-incorrect%402x.png)

![圆圈中的 X 表示不正确使用。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![iPad 上应用前端侧面的截图。图像跨越窗口上部，并使用背景扩展效果翻转、模糊并将图像延伸到侧边栏下方直到窗口边缘。](https://docs-assets.developer.apple.com/published/5cdac1170561cddf1930b4d74325c4dd/sidebars-extend-content-beneath-sidebar-correct%402x.png)

![圆圈中的复选标记表示正确使用。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**尽可能让人们自定义侧边栏内容。** 侧边栏让人们导航到应用中的重要区域，因此当人们可以决定哪些区域最重要以及它们出现的顺序时效果很好。

**如果您的应用有大量内容，使用展示控件分组层级。** 使用[展示控件](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls)有助于将侧边栏的垂直空间保持在可管理的水平。

**考虑使用熟悉的符号表示侧边栏中的项目。** [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 提供广泛的可自定义符号，您可以使用它们表示应用中的项目。如果您需要使用自定义图标，考虑创建[自定义符号](https://developer.apple.com/design/human-interface-guidelines/sf-symbols#Custom-symbols)而非使用位图图像。从 [Apple Design Resources](https://developer.apple.com/design/resources/#sf-symbols) 下载 SF Symbols 应用。

**考虑让人们隐藏侧边栏。** 人们有时想隐藏侧边栏以为内容详情创建更多空间或减少干扰。尽可能让人们使用他们已经知道的平台特定交互隐藏和显示侧边栏。例如，在 iPadOS 中，人们期望使用内置边缘滑动手势；在 macOS 中，您可以包含显示/隐藏按钮或在应用的视图菜单中添加显示侧边栏和隐藏侧边栏命令。在 visionOS 中，窗口通常会扩展以容纳侧边栏，因此人们很少需要隐藏它。避免默认隐藏侧边栏以确保它保持可发现。

**通常，在侧边栏中显示不超过两个层级。** 当数据层级深于两个级别时，考虑使用分割视图界面，在侧边栏项目和详情视图之间包含内容列表。

**如果需要在侧边栏中包含两个层级，使用简洁、描述性的标签为每个组命名。** 为了帮助保持标签简短，省略不必要的词。

## 平台注意事项

tvOS 无额外注意事项。watchOS 不支持。

### iOS

**避免使用侧边栏。** 侧边栏在横屏方向占用大量空间，在竖屏方向不可用。相反，考虑使用[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)，它占用更少空间并在两个方向都保持可见。

### iPadOS

当您使用标签视图的 [`sidebarAdaptable`](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable) 样式呈现侧边栏时，您选择应用打开时显示侧边栏还是标签栏。两种变体都包含一个按钮，人们可以使用它在它们之间切换。此样式还自动响应旋转和窗口调整大小，提供适合视图宽度的控件版本。

开发者注意

要仅显示侧边栏，使用 [`NavigationSplitView`](https://developer.apple.com/documentation/SwiftUI/NavigationSplitView) 在分割视图的主窗格中呈现侧边栏，或使用 [`UISplitViewController`](https://developer.apple.com/documentation/UIKit/UISplitViewController)。

**优先考虑使用标签栏。** 标签栏提供更多空间展示内容，并提供足够的灵活性在许多应用的主要区域之间导航。如果您需要暴露比标签栏容纳更多的区域，标签栏的可转换侧边栏样式外观可以提供对人们较少使用的内容的访问。指南请参阅[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)。

**如有必要，为侧边栏应用正确的外观。** 如果您不是使用 SwiftUI 创建侧边栏，可以使用集合视图列表布局的 [`UICollectionLayoutListConfiguration.Appearance.sidebar`](https://developer.apple.com/documentation/UIKit/UICollectionLayoutListConfiguration-swift.struct/Appearance-swift.enum/sidebar) 外观。开发者指南请参阅 [`UICollectionLayoutListConfiguration.Appearance`](https://developer.apple.com/documentation/UIKit/UICollectionLayoutListConfiguration-swift.struct/Appearance-swift.enum)。

### macOS

侧边栏的行高、文本和字形尺寸取决于其整体尺寸，可以是小型、中型或大型。您可以以编程方式设置尺寸，但人们也可以通过在通用设置中选择不同的侧边栏图标尺寸来更改它。

**避免通过为所有侧边栏图标指定固定颜色来风格化您的应用。** 默认情况下，侧边栏图标使用当前[强调色](https://developer.apple.com/design/human-interface-guidelines/color#App-accent-colors)，人们期望在他们使用的所有应用中看到他们选择的强调色。尽管固定颜色可以帮助阐明图标的含义，但您要确保大多数侧边栏图标显示人们选择的颜色。

**考虑在其容器窗口调整大小时自动隐藏和显示侧边栏。** 例如，减小邮件查看器窗口的尺寸可以自动折叠其侧边栏，为邮件内容腾出更多空间。

**避免在侧边栏底部放置关键信息或操作。** 人们经常以隐藏其底部边缘的方式重新定位窗口。

### visionOS

**如果您的应用层级很深，考虑在标签栏的标签内使用侧边栏。** 在这种情况下，侧边栏可以支持标签内的辅助导航。如果这样做，请确保防止侧边栏中的选择更改当前打开的标签。

![visionOS 中音乐应用的部分截图。应用窗口包含用于导航音乐库的侧边栏，辅助窗格包含播放列表网格。](https://docs-assets.developer.apple.com/published/5e381525f4cccac8e9eb979fe4c984c6/visionos-sidebar-music%402x.png)

## 资源

#### 相关

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### 开发者文档

[`sidebarAdaptable`](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable) — SwiftUI

[`NavigationSplitView`](https://developer.apple.com/documentation/SwiftUI/NavigationSplitView) — SwiftUI

[`sidebar`](https://developer.apple.com/documentation/SwiftUI/ListStyle/sidebar) — SwiftUI

[`UICollectionLayoutListConfiguration`](https://developer.apple.com/documentation/UIKit/UICollectionLayoutListConfiguration-swift.struct) — UIKit

[`NSSplitViewController`](https://developer.apple.com/documentation/AppKit/NSSplitViewController) — AppKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/873F40BE-101A-4C0D-99F0-F5C7CE7B47A3/10046_wide_250x141_1x.jpg) Elevate the design of your iPad app ](https://developer.apple.com/videos/play/wwdc2025/208)

## 变更日志

日期| 变更
---|---
2025年6月9日| 添加了将内容延伸到侧边栏下方的指南。
2024年8月6日| 更新指南以包含 SwiftUI 可适配侧边栏样式。
2023年12月5日| 添加了 iPadOS 的插图。
2023年6月21日| 更新以包含 visionOS 的指南。
