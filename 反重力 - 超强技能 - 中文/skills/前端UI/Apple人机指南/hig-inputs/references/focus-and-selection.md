---
title: "Focus and selection | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection

# 焦点与选择

焦点帮助用户直观确认其交互所指向的目标对象。

![A sketch of a frame around a circular interface element, suggesting locking focus on an object. The image is overlaid with rectangular and circular grid lines and is tinted purple to subtly reflect the purple in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/13b5befef4936f31ce74db6aa05b7a0e/inputs-focus-and-selection-intro%402x.png)

焦点支持简化的、基于组件的导航。用户通过遥控器、游戏手柄或键盘等输入设备，将焦点移至想要交互的组件上。

在许多情况下，聚焦某个项目即表示选中它。但当自动选择可能导致令人分心的上下文切换（如打开新视图）时，则属于例外。例如在 tvOS 中，用户使用遥控器将焦点逐项移动以寻找目标，但由于选中聚焦的项目会打开或激活它，因此需要单独的手势来完成选择。

不同平台以不同方式呈现焦点。例如，iPadOS 和 macOS 通过在项目周围绘制轮廓或高亮来显示焦点；tvOS 通常使用[视差效果](https://developer.apple.com/design/human-interface-guidelines/images#Parallax-effect)赋予聚焦项目立体感和生动感。焦点效果与交互的组合有时被称为_焦点系统_或_焦点模型_。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices)

**使用系统提供的焦点效果。** 系统定义的焦点效果经过精确调校，与 Apple 设备的交互相辅相成，带来灵敏、流畅且逼真的体验。采用系统提供的焦点行为可确保应用的一致性和可预测性，帮助用户快速理解。仅在绝对必要时才考虑创建自定义焦点效果。

**避免在用户未操作时改变焦点。** 用户依赖焦点系统来了解自己在应用中的位置。如果在用户未操作时改变焦点，用户需要花费时间找到新聚焦的项目，从而中断当前任务。例外情况是：当用户使用支持离散方向移动的输入设备（如键盘、遥控器或游戏手柄）移动焦点，且之前聚焦的项目消失时。在此场景中，之前聚焦项目的一个离散步幅范围内只有少量项目，将焦点移至其中一个剩余项目可确保焦点指示器位于用户容易找到的位置。当用户未使用此类输入设备移动焦点时，你无法预测其下一个目标，因此通常最好在聚焦对象消失时直接隐藏焦点指示器。

**在帮助用户将焦点引导至应用中的项目时，保持与平台的一致性。** 例如，在 iPadOS 和 macOS 中，完整键盘访问模式帮助用户使用键盘到达每个控件，因此你只需为内容元素（如列表项、文本字段和搜索字段）支持焦点，而无需为按钮、滑块和开关等控件支持焦点。相比之下，tvOS 用户依赖遥控器或游戏手柄的方向手势（或连接键盘上的方向键）来访问每个屏幕元素，因此你需要确保用户能够将焦点引导至应用中的每个元素。

**使用与平台一致的视觉外观来指示焦点。** 例如，考虑一个包含项目列表的窗口。在 iPadOS 和 macOS 中，系统使用白色文本和与应用强调色匹配的背景高亮来绘制聚焦的列表项，使用标准文本颜色和灰色背景高亮绘制未聚焦的项目（开发者指南请参阅 [`UICollectionView`](https://developer.apple.com/documentation/UIKit/UICollectionView) 和 [`NSTableView`](https://developer.apple.com/documentation/AppKit/NSTableView)）。

**通常，文本或搜索字段使用焦点环，列表或集合使用高亮。** 虽然可以使用焦点环来突出填充整个单元格的项目（如照片），但在列表和集合中高亮整行通常更容易浏览。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Platform-considerations)

 _iOS 和 watchOS 不支持。_

### [iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#iPadOS)

iPadOS 15 及更高版本定义了一套焦点系统，支持使用键盘在文本字段、文本视图、侧边栏以及应用中的各类集合视图和其他自定义视图之间导航。

iPadOS 和 tvOS 的焦点系统相似。用户通过将焦点指示器移至项目上来执行操作，然后选中它（指南请参阅 [tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS)）。虽然底层系统相同，但用户体验略有不同。tvOS 使用_方向焦点_，意味着用户可以使用相同的交互方式——即滑动 Siri Remote 或仅使用连接键盘上的方向键——来导航到每个屏幕组件。而 iPadOS 定义了_焦点组_，代表应用中的特定区域，如侧边栏、网格或列表。通过焦点组，iPadOS 可支持两种不同的键盘交互方式：

  * 按下 Tab 键在焦点组之间移动焦点，让用户导航到侧边栏、网格和其他应用区域。

  * 按下方向键支持类似于 tvOS 的方向焦点交互，但仅限于同一焦点组内项目之间的导航。例如，用户可以使用方向键在列表或侧边栏中的项目之间移动。




屏幕组件可以使用光晕效果或高亮外观来指示焦点。

_光晕_焦点效果——也称为_焦点环_——在组件周围显示可自定义的轮廓。你可以将光晕效果应用于自定义视图以及集合或列表单元格中完全不透明的内容（如图片）。

![An illustration of a collection view of photos showing the standard halo effect that outlines the focused photo.](https://docs-assets.developer.apple.com/published/2bfe6fedc5a6a8ecf6d7e74e9492a096/focus-and-selection-halo-focus-effect%402x.png)

**必要时自定义光晕焦点效果。** 默认情况下，系统使用项目的形状来推断其光晕的形状。如果系统提供的光晕未能达到预期效果，你可以对其进行调整以匹配圆角或贝塞尔路径定义的轮廓。如果其他组件遮挡或裁剪了光晕，你还可以调整其位置。例如，你可能需要确保徽章显示在光晕上方，或确保父视图不会裁剪它。开发者指南请参阅 [`UIFocusHaloEffect`](https://developer.apple.com/documentation/UIKit/UIFocusHaloEffect)。

![An illustration of a collection view of photos showing a rounded-rectangle halo effect that outlines the focused photo.](https://docs-assets.developer.apple.com/published/1a84f872d0624355e89fa03b357ddd13/focus-and-selection-customized-halo%402x.png)

_高亮_外观——即组件文本使用应用强调色——也可指示焦点，但它不是焦点效果。当用户选中你设置了内容配置的集合视图单元格时，高亮外观会自动出现（开发者指南请参阅 [`UICollectionViewCell`](https://developer.apple.com/documentation/UIKit/UICollectionViewCell)）。

![An illustration of a list of menu items with the second item highlighted. The item's title and icon are tinted with a red accent color.](https://docs-assets.developer.apple.com/published/01261865c38379fa118f16057a54f23e/focus-and-selection-highlighted-appearance%402x.png)

**确保焦点在自定义视图之间的移动方式合理。** 当用户持续按下 Tab 键时，焦点按阅读顺序在焦点组之间移动：从左到右，从上到下。虽然焦点在系统提供的视图中的移动方式符合用户预期，但你可能需要调整焦点系统访问自定义视图的顺序。例如，如果你希望焦点先在垂直堆叠的自定义视图中向下移动，然后再向右移动到下一个视图，你需要将堆叠容器标识为单个焦点组。开发者指南请参阅 [`focusGroupIdentifier`](https://developer.apple.com/documentation/UIKit/UIFocusEnvironment/focusGroupIdentifier)。

**调整项目的优先级以反映其在焦点组中的重要性。** 当一个焦点组获得焦点时，其_主要项目_也会自动获得焦点，使用户能够轻松选择最可能想要的项目。你可以通过提高优先级来将某个项目设为主要项目。开发者指南请参阅 [`UIFocusGroupPriority`](https://developer.apple.com/documentation/UIKit/UIFocusGroupPriority)。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS)

**在全屏体验中，让用户使用手势与内容交互，而非移动焦点。** 当项目以全屏显示时，不会显示焦点，因此用户自然会认为其手势作用于对象本身，而非其焦点状态。

**避免显示指针。** 用户期望通过改变焦点来在固定数量的项目之间导航，而不是在巨大的屏幕上拖动微小的指针。虽然自由移动在游戏过程中可能有意义（如寻找隐藏物品或驾驶飞机），但在用户导航菜单和其他界面元素时应使用焦点模型。如果你的应用确实需要指针，请确保其高度可见且与体验融为一体。

**设计界面以适配各种焦点状态下的组件。** 在 tvOS 中，可聚焦项目最多可有五种不同的视觉状态。由于聚焦项目通常会放大，你需要为更大的聚焦尺寸提供素材以确保其始终清晰，同时确保放大的项目不会挤压周围的界面。

状态| 描述  
---|---  
![An image of an unfocused button on top of a photograph. A small drop shadow makes it appear very close to the content behind it, with a translucent background infused by the colors of the content, and a high-contrast text color.](https://docs-assets.developer.apple.com/published/bfc53c88dc7a84a9ca45d43d8f7fb550/focus-and-selection-state-unfocused%402x.png)| 用户尚未将焦点移至该项目。未聚焦的项目看起来不如聚焦项目突出。  
![An image of a focused button on top of a photograph. It's larger than an unfocused button, and a drop shadow makes it appear farther away from the content behind it, with an opaque white background and a black text label.](https://docs-assets.developer.apple.com/published/882b1286aa16b7a8d4a6367778a984b9/focus-and-selection-state-focused%402x.png)| 用户将焦点移至该项目。聚焦项目通过提升到前景、照明和动画，在视觉上与其他屏幕内容区分开来。  
![An image of a highlighted button on top of a photograph. It's the same size as an unfocused button, and a drop shadow makes it appear a little farther away from the surface of the content behind it, with an opaque white background and a black text label.](https://docs-assets.developer.apple.com/published/d5388fe044717ba970895f33bdbebe3c/focus-and-selection-state-highlighted%402x.png)| 用户选中了聚焦项目。聚焦项目在用户选择时会提供即时视觉反馈。例如，按钮可能会短暂反转颜色并播放动画，然后过渡到选中外观。  
![An image of a selected button on top of a photograph. It's the same size as an unfocused button, and a small drop shadow makes it appear very close to the content behind it, with an opaque white background and a black text label.](https://docs-assets.developer.apple.com/published/ea6520ec5576b19ad7952c35a28c2dfc/focus-and-selection-state-selected%402x.png)| 用户已通过某种方式选择或激活了该项目。例如，用于收藏照片的心形按钮在选中状态可能显示为实心，在取消选中状态显示为空心。  
![An image of an unavailable button on top of a photograph. It's the same size as an unfocused button. It lacks a drop shadow and appears to rest directly on the content behind it, with a translucent background tinted by the the colors of nearby content, and a low-contrast text color.](https://docs-assets.developer.apple.com/published/c1d9c327cbefe45ef0aeef12b93b956c/focus-and-selection-state-unavailable%402x.png)| 用户无法将焦点移至该项目或选择它。不可用项目显示为非活动状态。  
  
开发者指南请参阅 [Adding user-focusable elements to a tvOS app](https://developer.apple.com/documentation/UIKit/adding-user-focusable-elements-to-a-tvos-app)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS)

visionOS 支持与 iPadOS 和 tvOS 相同的焦点系统，让用户可以使用连接的输入设备（如键盘或游戏手柄）与应用和系统交互。

注意

当用户注视虚拟对象以将其识别为想要交互的对象时，系统使用_悬停效果_（而非焦点效果）来提供视觉反馈（指南请参阅 [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)）。悬停效果与焦点系统无关。

## [资源](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Related)

[Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)

[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Developer-documentation)

[Focus Attributes](https://developer.apple.com/documentation/TVML/focus-attributes) — TVML

[Focus-based navigation](https://developer.apple.com/documentation/UIKit/focus-based-navigation) — UIKit

[About focus interactions for Apple TV](https://developer.apple.com/documentation/UIKit/about-focus-interactions-for-apple-tv) — UIKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/C6CDCC79-CCD0-4D2F-A4D1-8FC70DC663DB/8127_wide_250x141_1x.jpg) Design for spatial input ](https://developer.apple.com/videos/play/wwdc2023/10073)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/38E4EE32-29B5-4478-B8B6-35B8ACA67B16/8130_wide_250x141_1x.jpg) Design for spatial user interfaces ](https://developer.apple.com/videos/play/wwdc2023/10076)

[![](https://devimages-cdn.apple.com/wwdc-services/images/49/F9A980A7-B00A-4856-9172-FDB610A419E5/3509_wide_250x141_1x.jpg) Design for the iPadOS pointer ](https://developer.apple.com/videos/play/wwdc2020/10640)

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Change-log)

日期| 变更内容  
---|---  
2023 年 10 月 24 日| 说明了焦点效果与 visionOS 悬停效果的区别。  
2023 年 6 月 21 日| 更新以包含 visionOS 相关指导。  
  