---
title: "Windows | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/windows

# 窗口

窗口在应用或游戏中呈现 UI 视图和组件。

![带有关闭、最小化和全屏按钮的窗口的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/3c5ea22db1d7d414c160c95ed7f62ec9/components-window-intro%402x.png)

在 iPadOS、macOS 和 visionOS 中，窗口帮助定义应用内容的视觉边界并将其与其他系统区域分隔，并在应用内外启用多任务工作流。窗口包含系统提供的界面元素，如框架和窗口控件，让人们打开、关闭、调整大小和重新定位它们。

概念上，应用使用两种类型的窗口显示内容：

  * 主窗口呈现应用的主要导航和内容，以及与之相关的操作。

  * 辅助窗口呈现应用中的特定任务或区域。辅助窗口专用于一种体验，不允许导航到其他应用区域，通常包含一个按钮，人们在完成任务后使用它关闭窗口。




有关在任何平台上布局窗口内内容的指南，请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)；有关在 Apple Vision Pro 空间中布局内容的指南，请参阅[空间布局](https://developer.apple.com/design/human-interface-guidelines/spatial-layout)。开发者指南请参阅 [Windows](https://developer.apple.com/documentation/SwiftUI/Windows)。

## 最佳实践

**确保您的窗口流畅适应不同尺寸以支持多任务和多窗口工作流。** 指南请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)和[多任务](https://developer.apple.com/design/human-interface-guidelines/multitasking)。

**选择合适的时机打开新窗口。** 在单独窗口中打开内容非常适合帮助人们多任务或保留上下文。例如，每当有人选择撰写操作时，邮件会打开新窗口，以便新邮件和现有邮件同时可见。但是，过度打开新窗口会造成混乱，并可能使导航应用更加困惑。除非对您的应用有意义，否则避免将打开新窗口作为默认行为。

**考虑提供在新窗口中查看内容的选项。** 虽然除非对用户体验有益，否则最好避免将打开新窗口作为默认行为，但让人们灵活地以多种方式查看内容也很棒。考虑让人们使用[上下文菜单](https://developer.apple.com/design/human-interface-guidelines/context-menus)或[文件菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)中的命令在新窗口中查看内容。开发者指南请参阅 [`OpenWindowAction`](https://developer.apple.com/documentation/SwiftUI/OpenWindowAction)。

**避免创建自定义窗口 UI。** 系统提供的窗口以人们理解和识别的方式外观和行为。避免制作自定义窗口框架或控件，不要尝试复制系统提供的外观。这样做而不完美匹配系统的外观和行为可能会使您的应用感觉损坏。

**在面向用户的内容中使用术语窗口。** 系统将应用窗口称为窗口，无论类型如何。使用不同的术语——包括场景，它指的是窗口实现——可能会混淆人们。

## 平台注意事项

iOS、tvOS 和 watchOS 不支持。

### iPadOS

窗口根据人们在多任务与手势设置中的选择以两种方式之一呈现。

  * **全屏。** 应用窗口填满整个屏幕，人们使用应用切换器在它们之间切换——或在同一应用的多个窗口之间切换。

  * **窗口化。** 人们可以自由调整应用窗口大小。多个窗口可以同时出现在屏幕上，人们可以重新定位它们并将它们置于最前。即使应用关闭，系统也会记住窗口大小和位置。




  * 全屏
  * 窗口化




![iPad 上全屏笔记应用的截图，打开标题为自然漫步的文档。应用界面填满整个屏幕，窗口没有可见边框。](https://docs-assets.developer.apple.com/published/5daa697ab73d7e08de1e4fa78a56bfcb/windows-ipad-notes-fullscreen%402x.png)

![iPad 上窗口化笔记应用的截图，打开标题为自然漫步的文档。文档窗口占据屏幕中心，主屏幕背景填充其后面的其余屏幕，底部有程序坞。](https://docs-assets.developer.apple.com/published/0d1eca9806c6d60816eb9b6f436c28d3/windows-ipad-notes-windowed%402x.png)

**确保窗口控件不与工具栏项目重叠。** 窗口化时，应用窗口在工具栏前端边缘包含窗口控件。如果您的应用在前端边缘有工具栏按钮，当窗口控件出现时它们可能会被隐藏。为防止这种情况，不要将按钮直接放在前端边缘，而是在窗口控件出现时将它们向内移动。

**考虑让人们使用手势在新窗口中打开内容。** 例如，人们可以使用捏合手势将笔记项展开为新窗口。开发者指南请参阅 [`collectionView(_:sceneActivationConfigurationForItemAt:point:)`](https://developer.apple.com/documentation/UIKit/UICollectionViewDelegate/collectionView\(_:sceneActivationConfigurationForItemAt:point:\))（从集合视图项过渡）或 [`UIWindowScene.ActivationInteraction`](https://developer.apple.com/documentation/UIKit/UIWindowScene/ActivationInteraction)（从任何其他视图中的项过渡）。

提示

如果您只需要让人们查看一个文件，您可以在不创建自己的窗口的情况下呈现它，但您必须在应用中支持多窗口。开发者指南请参阅 [`QLPreviewSceneActivationConfiguration`](https://developer.apple.com/documentation/QuickLook/QLPreviewSceneActivationConfiguration)。

### macOS

在 macOS 中，人们通常同时运行多个应用，经常在一个桌面上查看多个应用的窗口，并在不同窗口之间频繁切换——移动、调整大小、最小化和显示窗口以适应他们的工作风格。

要了解如何在 macOS 中设置窗口以显示游戏，请参阅[在 macOS 中为 Metal 管理游戏窗口](https://developer.apple.com/documentation/Metal/managing-your-game-window-for-metal-in-macos)。

#### macOS 窗口结构

macOS 窗口由框架和主体区域组成。人们可以通过拖动框架移动窗口，通常可以通过拖动其边缘调整窗口大小。

窗口的框架出现在主体区域上方，可以包含窗口控件和[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)。在极少数情况下，窗口也可以显示底部栏，这是出现在主体内容下方的框架的一部分。

#### macOS 窗口状态

macOS 窗口可以有三种状态之一：

  * **主窗口。** 人们查看的最前面的窗口是应用的主窗口。每个应用只能有一个主窗口。

  * **关键窗口。** 也称为活动窗口，关键窗口接受人们的输入。屏幕上一次只能有一个关键窗口。虽然最前面应用的主窗口通常是关键窗口，但另一个窗口——如浮动在主窗口上方的面板——可能代替成为关键窗口。人们通常点击窗口使其成为关键窗口；当人们点击应用的程序坞图标将该应用的所有窗口置于最前时，只有最近访问的窗口成为关键窗口。

  * **非活动窗口。** 不在前台的窗口是非活动窗口。




系统为主窗口、关键窗口和非活动窗口提供不同的外观，帮助人们在视觉上识别它们。例如，关键窗口在关闭、最小化和缩放选项的标题栏中使用颜色；非活动窗口和不是关键窗口的主窗口在这些选项中使用灰色。此外，非活动窗口不使用[活力](https://developer.apple.com/design/human-interface-guidelines/materials)（一种可以从下方内容将颜色拉入窗口的效果），这使它们看起来更柔和，在视觉上似乎比主窗口和关键窗口更远。

![三个窗口堆栈的插图，如下：背景中的非活动窗口、中间的应用主窗口、出现在其他两个窗口上方的关键窗口。](https://docs-assets.developer.apple.com/published/7ecd910726f347fb452d9ecd2b492d22/window-states%402x.png)

注意

某些窗口——通常是颜色或字体等面板——仅在人们点击窗口的标题栏或需要键盘输入的组件（如文本字段）时才成为关键窗口。

**确保自定义窗口使用系统定义的外观。** 人们依赖窗口之间的视觉差异来帮助他们识别前台窗口并知道哪个窗口将接受他们的输入。当您使用系统提供的组件时，窗口的背景和按钮外观会在窗口状态更改时自动更新；如果您使用自定义实现，则需要自己完成此工作。

**避免在底部栏中放置关键信息或操作，因为人们经常以隐藏其底部边缘的方式重新定位窗口。** 如果必须包含底部栏，请仅使用它显示与窗口内容或其中所选项直接相关的小量信息。例如，Finder 使用底部栏（称为状态栏）显示窗口中的项目总数、所选项目数和磁盘上的可用空间。底部栏很小，所以如果您有更多信息要显示，请考虑使用检查器，它通常在分割视图的尾端呈现信息。

### visionOS

visionOS 定义了两种主要窗口样式：默认和体积。默认窗口（称为窗口）和体积窗口（称为体积）都可以显示 2D 和 3D 内容，人们可以在共享空间和全空间中同时查看多个窗口和体积。

![表示 visionOS 中窗口的插图。插图由两个平行的圆角矩形组成，略微分离并以一定角度显示，位于窗口栏上方。](https://docs-assets.developer.apple.com/published/e8dc51484c2e5f3289a5f6a878f4c47d/visionos-window-style-2d-window%402x.png)窗口

![表示 visionOS 中体积的插图。插图由半透明立方体组成。立方体的底部比其他侧面更暗。立方体的正面位于窗口栏上方。](https://docs-assets.developer.apple.com/published/92d953d099f72f9909c47bad408f4c9b/visionos-window-style-3d-volume%402x.png)体积

注意

visionOS 还定义了普通窗口样式，它与默认样式类似，只是直立平面不使用玻璃背景。开发者指南请参阅 [`PlainWindowStyle`](https://developer.apple.com/documentation/SwiftUI/PlainWindowStyle)。

系统定义了人们在您的应用或游戏中打开的第一个窗口或体积的初始位置。在共享空间和全空间中，人们可以将窗口和体积移动到新位置。

#### visionOS 窗口

默认窗口样式由使用不可修改的背景[材质](https://developer.apple.com/design/human-interface-guidelines/materials)（称为玻璃）的直立平面组成，并包含关闭按钮、窗口栏和调整大小控件，让人们关闭、移动和调整窗口大小。窗口还可以包含共享按钮、[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)、[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)和一个或多个[装饰件](https://developer.apple.com/design/human-interface-guidelines/ornaments)。默认情况下，visionOS 使用动态[缩放](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Scale)帮助窗口的尺寸看起来保持一致，无论其与观看者的距离如何。开发者指南请参阅 [`DefaultWindowStyle`](https://developer.apple.com/documentation/SwiftUI/DefaultWindowStyle)。

![visionOS 中名为"Hello World"的应用窗口截图。窗口包含文本和用于进入不同体验的按钮。](https://docs-assets.developer.apple.com/published/95650cb19e1930e6b08ca5aa3b5b06a0/visionos-window-2d%402x.png)窗口

**优先使用窗口呈现熟悉的界面并支持熟悉的任务。** 通过显示人们已经舒适的界面帮助人们在您的应用中感到宾至如归，为您提供的有意义内容和活动保留更多[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)。如果您想展示有界的 3D 内容如游戏棋盘，请考虑使用[体积](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS-volumes)。

**保留窗口的玻璃背景。** 默认玻璃背景帮助您的内容感觉像是人们周围环境的一部分，同时动态适应照明并使用镜面反射和阴影传达窗口的缩放和位置。移除玻璃材质往往会导致 UI 元素和文本变得不太清晰，不再显得彼此相关；使用不透明背景会遮挡人们的周围环境，并可能使窗口感觉受限和沉重。

**选择最小化内部空白区域的初始窗口尺寸。** 默认情况下，窗口尺寸为 1280x720 pt。当窗口首次打开时，系统将其放置在佩戴者前方约两米处，使其表观宽度约为三米。窗口内太多空白空间会使其看起来不必要地大，同时也会遮挡人们空间中的其他内容。

**力求选择适合窗口内容的初始形状。** 例如，默认 Keynote 窗口很宽，因为幻灯片很宽，而默认 Safari 窗口很高，因为大多数网页比宽更长。对于游戏，塔建游戏可能会在比驾驶游戏更高的窗口中打开。

**为每个窗口选择最小和最大尺寸以帮助保持内容美观。** 人们欣赏能够在自定义空间时调整窗口大小，但您需要确保您的布局在所有尺寸下都能良好调整。如果您不为窗口设置最小和最大尺寸，人们可能会将其做得太小以至于 UI 元素重叠，或做得太大以至于您的应用或游戏变得不可用。开发者指南请参阅[定位和调整窗口大小](https://developer.apple.com/documentation/visionOS/positioning-and-sizing-windows)。

![visionOS 中应用窗口的截图。窗口包含讨论轨道物体的文本，并包含用于查看卫星、月球和望远镜的按钮。卫星按钮被选中并显示 3D 卫星。](https://docs-assets.developer.apple.com/published/db1e41fe4000281898003f792ff037c8/visionos-window-2d-with-volume%402x.png)包含 3D 内容的窗口

**最小化您在窗口中显示的 3D 内容的深度。** 系统为窗口内的视图和控件添加高光和阴影，赋予它们[深度](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Depth)的外观，帮助它们感觉更实在，尤其是当人们从某个角度查看窗口时。虽然您可以在窗口中显示 3D 内容，但如果内容延伸离窗口表面太远，系统会将其剪切。要显示具有更大深度的 3D 内容，请使用体积。

#### visionOS 体积

您可以使用体积显示人们可以从任何角度查看的 2D 或 3D 内容。体积包含窗口管理控件，就像窗口一样，但与窗口不同，体积的关闭按钮和窗口栏会随着人们围绕体积移动而移动位置以面向观看者。开发者指南请参阅 [`VolumetricWindowStyle`](https://developer.apple.com/documentation/SwiftUI/VolumetricWindowStyle)。

![visionOS 中包含 3D 地球的体积截图，旁边有一个窗口。](https://docs-assets.developer.apple.com/published/99098a290c36254e48329511216e1d5a/visionos-window-3d%402x.png)体积

**优先使用体积显示丰富的 3D 内容。** 相比之下，如果您想呈现熟悉的、以 UI 为中心的界面，通常最好使用[窗口](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS-windows)。

**放置 2D 内容使其从多个角度看起来良好。** 因为人们的视角随着他们围绕体积移动而改变，其中的 2D 内容位置可能以不合理的方式出现变化。要将 2D 内容固定到体积内 3D 内容的特定区域，您可以使用附件。

**通常，使用动态缩放。** 动态缩放帮助体积的内容保持舒适可读和易于交互，即使它离观看者很远。另一方面，如果您希望体积的内容代表真实世界的物体，如零售应用中的产品，您可以使用固定缩放（这是默认值）。

**利用默认底板外观帮助人们辨别体积的边缘。** 在 visionOS 2 及更高版本中，当人们查看体积时，系统会通过在其边框周围显示柔和发光自动使体积的水平"地板"或底板可见。如果您的内容没有填满体积，系统提供的发光可以帮助人们意识到体积的边缘，这在保持调整大小控件易于查找方面特别有用。另一方面，如果您的内容是全出血或填满体积的边界——或者您显示自定义底板外观——您可能不想要默认发光。

**考虑在装饰件中提供高价值内容。** 在 visionOS 2 及更高版本中，除了工具栏和标签栏外，体积还可以包含装饰件。您可以使用装饰件减少体积中的混乱并提升重要视图或控件。当您使用附件锚点指定装饰件的位置（如 `topBack` 或 `bottomFront`）时，随着人们围绕体积移动，装饰件相对于观看者的视角保持在相同位置。请确保避免在与工具栏或标签栏相同的边缘放置装饰件，并优先只创建一个额外的装饰件以避免遮蔽体积中的重要内容。开发者指南请参阅 [`ornament(visibility:attachmentAnchor:contentAlignment:ornament:)`](https://developer.apple.com/documentation/SwiftUI/View/ornament\(visibility:attachmentAnchor:contentAlignment:ornament:\))。

**选择支持人们与体积交互方式的对齐。** 当人们移动体积时，底板可以保持与人周围环境地板平行，或可以倾斜以匹配人们观看的角度。通常，保持与地板平行的体积适用于人们不太交互的内容，而倾斜以匹配人们观看位置的体积可以保持内容舒适可用，即使观看者正在斜躺。

## 资源

#### 相关

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

[Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)

#### 开发者文档

[Windows](https://developer.apple.com/documentation/SwiftUI/Windows) — SwiftUI

[`WindowGroup`](https://developer.apple.com/documentation/SwiftUI/WindowGroup) — SwiftUI

[`UIWindow`](https://developer.apple.com/documentation/UIKit/UIWindow) — UIKit

[`NSWindow`](https://developer.apple.com/documentation/AppKit/NSWindow) — AppKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/873F40BE-101A-4C0D-99F0-F5C7CE7B47A3/10046_wide_250x141_1x.jpg) Elevate the design of your iPad app ](https://developer.apple.com/videos/play/wwdc2025/208)

## 变更日志

日期| 变更
---|---
2025年6月9日| 添加了最佳实践，并更新了 iPadOS 中可调整大小窗口的指南。
2024年6月10日| 更新以包含在 visionOS 2 中使用体积的指南并添加了游戏特定示例。
2023年6月21日| 更新以包含 visionOS 的指南。
