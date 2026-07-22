---
title: "Tab bars | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/tab-bars

# 标签栏

标签栏让人们导航应用的顶级分区。

![包含四个带名称占位图标的标签栏的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/8737d6baf5cdb223521eb4dbe3cb45e5/components-tab-bar-intro%402x.png)

标签栏帮助人们理解应用提供的不同类型信息或功能。它们还让人们快速切换视图分区，同时保留每个分区内的当前导航状态。

## 最佳实践

**使用标签栏支持导航，而非提供操作。** 标签栏让人们导航应用的不同分区，如时钟应用中的闹钟、秒表和计时器标签。如果您需要提供对当前视图中元素执行操作的控件，请改用[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)。

**确保人们导航到应用不同分区时标签栏可见。** 如果您隐藏标签栏，人们可能会忘记他们在应用的哪个区域。例外是模态视图覆盖标签栏时，因为模态是临时的且自包含的。

**使用适当数量的标签帮助人们导航您的应用。** 作为应用层级的表示，权衡额外标签的复杂性与人们频繁访问每个分区的需求很重要；请记住，在较少标签之间导航通常更容易。如果可用，考虑使用侧边栏或可适配为侧边栏的标签栏作为具有复杂信息结构应用的替代方案。

**避免溢出标签。** 根据设备尺寸和方向，可见标签数量可能小于标签总数。如果水平空间限制可见标签数量，尾随标签在 iOS 和 iPadOS 中会变为更多标签，在单独列表中显示其余项目。更多标签使人们更难到达和注意到隐藏标签上的内容，因此限制应用中可能发生这种情况的场景。

**不要禁用或隐藏标签栏按钮，即使其内容不可用。** 标签栏按钮在某些情况下可用而在其他情况下不可用会使应用界面显得不稳定和不可预测。如果分区为空，请解释为什么其内容不可用。

**包含标签标签以帮助导航。** 标签标签出现在标签栏图标下方或旁边，可以通过清晰描述标签包含的内容或功能类型来辅助导航。尽可能使用单个词。

**考虑使用 SF Symbols 提供熟悉的、可缩放的标签栏图标。** 当您使用 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 时，标签栏图标会自动适应不同上下文。例如，标签栏可以是常规或紧凑的，具体取决于设备和方向。标签栏图标在紧凑视图中出现在标签标签上方，而在常规视图中，图标和标签并排出现。优先使用填充符号或图标以与平台保持一致。

![两台 iPhone 并排的插图。第一台 iPhone 处于横屏方向，标签栏位于屏幕底部，标签栏图标在每个标签的前端，标签标签在尾端。第二台 iPhone 处于竖屏方向，标签栏位于屏幕底部，标签栏图标在其各自的标签标签上方。](https://docs-assets.developer.apple.com/published/6871e7b24b6da37f753c61deba02c8ab/tab-bar-landscape%402x.png)

如果您正在创建自定义标签栏图标，请参阅 [Apple Design Resources](https://developer.apple.com/design/resources/) 了解标签栏图标尺寸。

![标签栏图解，带有指示标签栏图标和标签标签位置的标注。](https://docs-assets.developer.apple.com/published/eb47e442c964d54ed32f9324c71511d1/tab-bar-anatomy-callouts%402x.png)

**使用徽标指示有重要信息可用。** 您可以在标签上显示徽标——包含白色文本和数字或感叹号的红色椭圆——以指示该分区中有值得人们注意的新信息或更新信息。将徽标保留给重要信息，以免稀释其影响和意义。指南请参阅[通知](https://developer.apple.com/design/human-interface-guidelines/notifications)。

![竖屏方向 iPhone 下半部分的插图，标签栏位于屏幕底部。两个标签附有红色圆形徽标，指示有重要信息。](https://docs-assets.developer.apple.com/published/29a93bc69eaa415e2e3d5440474a8d36/tab-bar-badges-iphone%402x.png)

**避免为标签标签和内容层背景应用相似颜色。** 如果您的应用在内容层中已经有明亮、多彩的内容，优先为标签栏使用单色外观，或选择具有足够视觉差异的强调色。更多指南请参阅 [Liquid Glass 颜色](https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color)。

## 平台注意事项

macOS 无额外注意事项。watchOS 不支持。

### iOS

标签栏浮动在屏幕底部的内容上方。其项目位于 [Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass) 背景上，允许下方内容透出。

对于带有附件的标签栏，如音乐中的 MiniPlayer，您可以选择在人们向下滚动时最小化标签栏并将附件与其内联。人们可以通过点击标签或滚动到视图顶部退出最小化状态。开发者指南请参阅 [`TabBarMinimizeBehavior`](https://developer.apple.com/documentation/SwiftUI/TabBarMinimizeBehavior) 和 [`UITabBarController.MinimizeBehavior`](https://developer.apple.com/documentation/UIKit/UITabBarController/MinimizeBehavior)。

![竖屏方向 iPhone 下半部分的插图，音乐应用打开。MiniPlayer 在屏幕底部的标签栏上方打开。](https://docs-assets.developer.apple.com/published/1b8fb04a802aacd9c9f46ba7b16be080/tab-bar-with-accessory-expanded%402x.png)

带有附件的标签栏，展开

![竖屏方向 iPhone 下半部分的插图，音乐应用打开。标签栏最小化为当前打开的标签，位于屏幕前端底部角落，MiniPlayer 位于底部中心，搜索标签位于尾随角落。](https://docs-assets.developer.apple.com/published/d074ff4013a38155a887ceeecf2417fa/tab-bar-with-accessory-collapsed%402x.png)

带有附件的标签栏，最小化

标签栏可以在尾端包含独特的搜索项。指南请参阅[搜索字段](https://developer.apple.com/design/human-interface-guidelines/search-fields)。

### iPadOS

系统在屏幕顶部附近显示标签栏。您可以选择让标签栏显示为固定元素，或带有可将其转换为侧边栏的按钮。开发者指南请参阅 [`tabBarOnly`](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/tabBarOnly) 和 [`sidebarAdaptable`](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable)。

  * 标签栏
  * 侧边栏




![iPad 上音乐应用的截图，标签栏位于屏幕顶部附近。](https://docs-assets.developer.apple.com/published/66af6b050f67a05a82c5df2acb99913a/ipad-tab-bar-music-app%402x.png)

![iPad 上音乐应用的截图，标签栏转换为屏幕前端边缘的侧边栏。](https://docs-assets.developer.apple.com/published/cb52cc194e4067efff244c3b991a02a4/ipad-sidebar-music-app%402x.png)

注意

要呈现侧边栏而不提供转换为标签栏的选项，请使用[导航分割视图](https://developer.apple.com/documentation/swiftui/navigationsplitview)而非标签视图。指南请参阅[侧边栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)。

**优先使用标签栏进行导航。** 标签栏提供对人们最常使用的应用分区的访问。如果您的应用更复杂，您可以提供将标签栏转换为侧边栏的选项，以便人们可以访问更广泛的导航选项。

**让人们自定义标签栏。** 在人们可能想要访问的分区较多的应用中，让人们选择他们经常使用的项目并将其添加到标签栏，或删除他们较少使用的项目可能很有用。例如，在音乐应用中，人们可以选择喜欢的播放列表显示在标签栏中。如果您让人们选择自己的标签，目标默认列表为五个或更少，以保持紧凑和常规视图尺寸之间的连续性。开发者指南请参阅 [`TabViewCustomization`](https://developer.apple.com/documentation/SwiftUI/TabViewCustomization) 和 [`UITab.Placement`](https://developer.apple.com/documentation/UIKit/UITab/Placement)。

### tvOS

标签栏高度可自定义。例如，您可以：

  * 为标签栏背景指定色调、颜色或图像

  * 为标签项选择字体，包括所选项的不同字体

  * 为选中和未选中项指定色调

  * 添加按钮图标，如设置和搜索




默认情况下，标签栏是半透明的，只有选中的标签是不透明的。当人们使用遥控器聚焦标签栏时，选中的标签包含强调其选中状态的投影。标签栏高度为 68 点，其顶部边缘距屏幕顶部 46 点；您不能更改这两个值。

如果项目过多无法放入标签栏，系统会通过应用从标签栏右侧开始的淡出效果截断最右侧的项目。如果有足够的项目导致滚动，系统还会应用从左侧开始的截断淡出效果。

**注意标签栏滚动行为。** 默认情况下，当当前标签包含单个主视图时，人们可以将标签栏滚动出屏幕。您可以在电视应用的立即观看、电影、电视节目、体育和儿童标签中看到此行为的示例。例外是屏幕包含分割视图时，例如电视应用的资料库标签或应用的设置屏幕。在这种情况下，当人们在分割视图的主窗格和辅助窗格内滚动内容时，标签栏保持固定在视图顶部。无论标签内容如何，当人们在遥控器上按下菜单时，焦点始终返回到页面顶部的标签栏。

**在直播观看应用中，以一致的方式组织标签。** 为获得最佳体验，在直播流应用中使用以下顺序组织带有标签的内容：

  * 直播内容

  * 云 DVR 或其他录制内容

  * 其他内容




更多指南请参阅[直播观看应用](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps)。

### visionOS

在 visionOS 中，标签栏始终是垂直的，浮动在相对于窗口前端侧固定位置。当人们查看标签栏时，它会自动展开；要打开特定标签，人们查看标签并点击。当标签栏展开时，它可以临时遮挡其背后的内容。

带有自定义控件的视频。

内容描述：显示 visionOS 应用窗口侧面标签栏特写的录制。标签栏仅包含符号。当前选中的标签接收悬停效果，显示有人正在查看它，栏展开以显示符号和标签。

播放

**为每个标签提供符号和文本标签。** 标签的符号在标签栏中始终可见。当人们查看标签栏时，系统也会显示标签标签。即使标签栏展开，您也需要保持标签标签简短，以便人们可以一目了然地阅读。

![仅包含符号的折叠标签栏截图。](https://docs-assets.developer.apple.com/published/60282ea47a438f5b2bd84705212b44e4/visionos-tab-bar-collapsed%402x.png)折叠

![包含符号和标签的展开标签栏截图。](https://docs-assets.developer.apple.com/published/df1a14ce3d5e2743bfdfb0fea47fc340/visionos-tab-bar-expanded%402x.png)展开

**如果在应用中有意义，考虑在标签内使用侧边栏。** 如果您的应用层级很深，您可能想使用[侧边栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)支持标签内的辅助导航。如果这样做，请确保防止侧边栏中的选择更改当前打开的标签。

## 资源

#### 相关

[Tab views](https://developer.apple.com/design/human-interface-guidelines/tab-views)

[Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

[Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)

[Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

#### 开发者文档

[`TabView`](https://developer.apple.com/documentation/SwiftUI/TabView) — SwiftUI

[`TabViewBottomAccessoryPlacement`](https://developer.apple.com/documentation/SwiftUI/TabViewBottomAccessoryPlacement) — SwiftUI

[Enhancing your app's content with tab navigation](https://developer.apple.com/documentation/SwiftUI/Enhancing-your-app-content-with-tab-navigation) — SwiftUI

[`UITabBar`](https://developer.apple.com/documentation/UIKit/UITabBar) — UIKit

[Elevating your iPad app with a tab bar and sidebar](https://developer.apple.com/documentation/UIKit/elevating-your-ipad-app-with-a-tab-bar-and-sidebar) — UIKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/1AAA030E-2ECA-47D8-AE09-6D7B72A840F6/10044_wide_250x141_1x.jpg) Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/873F40BE-101A-4C0D-99F0-F5C7CE7B47A3/10046_wide_250x141_1x.jpg) Elevate the design of your iPad app ](https://developer.apple.com/videos/play/wwdc2025/208)

## 变更日志

日期| 变更
---|---
2025年12月16日| 更新了 Liquid Glass 指南。
2025年7月28日| 添加了 Liquid Glass 指南。
2024年9月9日| 添加了代表 iPadOS 18 中标签栏的插图。
2024年8月6日| 更新了 iPadOS 18 中标签栏的指南。
2023年6月21日| 更新以包含 visionOS 的指南。
