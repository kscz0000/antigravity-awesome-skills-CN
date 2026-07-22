---
title: "Sheets | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/sheets

# 表单

表单帮助用户执行与其当前上下文密切相关的限定任务。

![从窗口顶部向下延伸的表单的概念图。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/357ff0b017e9241da82888bd3aec4372/components-sheet-intro%402x.png)

默认情况下，表单是_模态的_，提供针对性体验，阻止用户与父视图交互，直到关闭表单（有关模态展示的更多信息，参见[模态](https://developer.apple.com/design/human-interface-guidelines/modality)）。模态表单适用于向用户请求特定信息或展示简单任务，用户可以在返回父视图前完成。例如，表单可以让用户提供完成操作所需的信息，如附加文件、选择移动或保存的位置，或指定选择的格式。

在 macOS、visionOS 和 watchOS 中，表单始终是模态的，但在 iOS 和 iPadOS 中，表单也可以是非模态的。当非模态表单在屏幕上时，用户使用其功能直接影响父视图中的当前任务，而无需关闭表单。例如，iPhone 和 iPad 上的 Notes 使用非模态表单帮助用户在编辑笔记时对不同文本选择应用不同格式。

![iPhone 上正在编辑的笔记截图。几个单词被选中并高亮显示。屏幕下半部分，格式表单显示选中的单词使用常规正文字体。](https://docs-assets.developer.apple.com/published/56830eea369c54ce82f6867a0907f3f3/sheets-nonmodal-notes-text-regular%402x.png)

Notes 格式表单让用户对编辑视图中选中的文本应用格式。

![同一 iPhone 上正在编辑的笔记截图。不同的单词被选中并高亮显示。格式表单显示选中的单词使用斜体正文字体。](https://docs-assets.developer.apple.com/published/f7b427fb2d880e16df4ed1025a43b47c/sheets-nonmodal-notes-text-italic%402x.png)

由于表单是非模态的，用户可以进行额外的文本选择而无需关闭表单。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/sheets#Best-practices)

**使用表单展示简单内容或任务。** 表单允许部分父视图保持可见，帮助用户在与表单交互时保持原始上下文。

**对于复杂或长时间的用户流程，考虑表单的替代方案。** 例如，iOS 和 iPadOS 提供全屏样式的模态视图，非常适合显示视频、照片或相机视图等内容，或帮助用户执行文档或照片编辑等多步任务。（开发者指南参见[`UIModalPresentationStyle.fullScreen`](https://developer.apple.com/documentation/UIKit/UIModalPresentationStyle/fullScreen)。）在 macOS 体验中，可能需要打开新窗口或让用户进入全屏模式而不是使用表单。例如，编辑文档等独立任务在单独窗口中效果很好，而[全屏模式](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)可以帮助用户查看媒体。在 visionOS 中，可以让用户将应用转换到全空间，在那里他们可以沉浸于内容或任务；参见[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)。

**一次只从主界面显示一个表单。** 当用户关闭表单时，他们期望返回父视图或窗口。如果关闭表单将用户带回另一个表单，他们可能会迷失在应用中的位置。如果用户在表单内的操作导致出现另一个表单，在显示新表单前关闭第一个表单。如有必要，可以在用户关闭第二个表单后再次显示第一个表单。

**当需要展示影响父视图中主任务的补充项目时，使用非模态视图。** 为让用户在继续与主窗口交互的同时访问所需信息和操作，考虑在 visionOS 中使用[分栏视图](https://developer.apple.com/design/human-interface-guidelines/split-views)或在 macOS 中使用[面板](https://developer.apple.com/design/human-interface-guidelines/panels)；在 iOS 和 iPadOS 中，可以为此工作流程使用非模态表单。参见[iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/sheets#Platform-considerations)

 _tvOS 无其他注意事项。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS)

可调整大小的表单在用户滚动其内容或拖动_抓取器_时展开，抓取器是可能出现在表单顶部边缘的小水平指示器。表单根据其_停靠点_调整大小，停靠点是表单自然停留的特定高度。为 iPhone 设计，停靠点指定表单自然停留的特定高度。系统定义两个停靠点：_大_是完全展开表单的高度，_中_大约是完全展开高度的一半。

![iPhone 纵向屏幕的示意图，包含一个占据几乎整个屏幕的实心圆角矩形，代表全屏表单。表单左上角出现圆角关闭按钮。](https://docs-assets.developer.apple.com/published/c2a600adb5237892585d71d2ae61c9a6/sheets-large-detent%402x.png)

大停靠点

![iPhone 纵向屏幕的示意图，包含一个占据屏幕一半的实心圆角矩形，代表半屏表单。表单左上角出现圆角关闭按钮。](https://docs-assets.developer.apple.com/published/413ac0d4cf462891f2ba9d0cd4bb01f1/sheets-medium-detent%402x.png)

中停靠点

表单自动支持大停靠点。添加中停靠点允许表单在两个高度停留，而仅指定中停靠点则阻止表单展开到全高。开发者指南参见[`detents`](https://developer.apple.com/documentation/UIKit/UISheetPresentationController/detents)。

**在 iPhone 应用中，考虑支持中停靠点以允许表单内容的渐进式展示。** 例如，分享表单在中停靠点内显示最相关的项目，无需调整大小即可看到。要查看更多项目，用户可以滚动或展开表单。相比之下，如果表单内容在全高显示时更有用，可能不想支持中停靠点。例如，Messages 和 Mail 的撰写表单仅在全高显示，为用户提供足够的创作空间。

**在可调整大小的表单中包含抓取器。** 抓取器向用户显示他们可以拖动表单来调整大小；他们也可以点击它来循环切换停靠点。除了提供可调整大小的视觉指示外，抓取器还与 VoiceOver 配合工作，让用户无需看屏幕即可调整表单大小。开发者指南参见[`prefersGrabberVisible`](https://developer.apple.com/documentation/UIKit/UISheetPresentationController/prefersGrabberVisible)。

**支持滑动关闭表单。** 用户期望通过垂直滑动关闭表单，而不是点击关闭按钮。如果用户在开始滑动关闭表单时表单中有未保存的更改，使用操作表让他们确认操作。

**按用户期望的位置放置完成和取消按钮。** 通常，完成或关闭按钮属于表单右上角（从左到右布局中）。取消按钮属于表单左上角。

例外情况是带有附加子视图的表单，取消按钮属于右上角；这为第一页之后页面左上角的后退按钮留出空间。在导航流程结束时，用完成按钮替换取消按钮。

![iPhone 上半部分表单的示意图。取消按钮出现在视图左上角。](https://docs-assets.developer.apple.com/published/4c0ea03add08b05592c51ed58ebb79f1/sheets-close-button-placement-no-back%402x.png)

取消按钮单独出现时的位置

![iPhone 上半部分表单的示意图。后退按钮出现在视图左上角，取消按钮出现在右上角。](https://docs-assets.developer.apple.com/published/4325d8e5db78c585b01a7137e34189c7/sheets-close-button-placement-with-back%402x.png)

取消按钮作为多步流程一部分出现时的位置

**在 iPadOS 应用中优先使用页面或表单展示样式。** 每种样式使用表单的默认大小，在变暗的背景视图上方居中显示内容，提供一致的体验。开发者指南参见[`UIModalPresentationStyle`](https://developer.apple.com/documentation/UIKit/UIModalPresentationStyle)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/sheets#macOS)

在 macOS 中，表单是一种卡片式视图，带有圆角，浮动在其父窗口上方。表单在屏幕上时父窗口变暗，表示用户在关闭表单前无法与之交互。然而，用户期望在关闭表单前与其他应用窗口交互。

![Notes 应用的截图，"What's New in Notes"表单居中显示在变暗的 Notes 文档背景上方。](https://docs-assets.developer.apple.com/published/582e02d0df9b4a07dea002053f9ec6ea/sheets-macos-notes%402x.png)

**以合理的默认大小展示表单。** 用户通常不期望调整表单大小，因此使用适合所显示内容的大小很重要。然而，在某些情况下，用户会欣赏可调整大小的表单——例如当他们需要展开内容以获得更清晰的视图时——所以支持调整大小是个好主意。

**让用户在未先关闭表单的情况下与其他应用窗口交互。** 当表单打开时，将其父窗口带到前面——如果父窗口是文档窗口，也将其非模态文档相关面板带到前面。当用户想要与应用中的其他窗口交互时，确保他们可以将这些窗口带到前面，即使尚未关闭表单。

**按用户期望的位置放置表单的关闭按钮。** 用户期望找到所有关闭表单的按钮——包括完成、确定和取消——在视图底部，后角。

**如果用户需要反复提供输入并观察结果，使用面板而不是表单。** 例如，查找和替换面板可能让用户单独启动替换，以便他们可以观察每次搜索的正确性结果。参见[面板](https://developer.apple.com/design/human-interface-guidelines/panels)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/sheets#visionOS)

当表单在 visionOS 应用中可见时，它浮动在其父窗口前方，使父窗口变暗，并成为用户与应用交互的目标。

带自定义控件的视频。 

内容描述：显示 visionOS 中空白窗口上方打开表单的录制。 

播放 

**避免显示从窗口底部边缘出现的表单。** 为帮助用户查看表单，优先在其[视野](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Field-of-view)中央居中显示。

**以帮助用户保持上下文的默认大小展示表单。** 避免显示覆盖其窗口大部分或全部的表单，但如果用户需要，考虑让他们调整表单大小。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/sheets#watchOS)

在 watchOS 中，表单是滑过应用当前内容的全屏视图。表单是半透明的，以帮助保持当前上下文，但系统对背景应用材质，使被覆盖的内容模糊和去饱和。

![Apple Watch 上带有主要操作按钮和默认取消按钮的表单截图。](https://docs-assets.developer.apple.com/published/fcdad96a098bea9c7b98a114403e46f2/sheets-watch-overlay%402x.png)

**仅在模态任务需要自定义标题或自定义内容展示时使用表单。** 如果需要向用户提供重要信息或展示一组选择，考虑使用[警告框](https://developer.apple.com/design/human-interface-guidelines/alerts)或[操作表](https://developer.apple.com/design/human-interface-guidelines/action-sheets)。

**保持表单交互简短且偶尔。** 仅将表单用作当前工作流程的临时中断，且仅用于促进重要任务。避免使用表单帮助用户导航应用内容。

**仅在应用中有意义时更改关闭控件的默认标签。** 默认情况下，表单在左上角显示圆形取消按钮。当表单让用户对应用行为或数据进行更改时使用此按钮。如果表单仅展示信息而不启用任务，改用标准完成按钮。可以使用[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)显示多个按钮。

![Apple Watch 上显示带有标准勾选完成按钮的表单截图。](https://docs-assets.developer.apple.com/published/bc70ac8a01bd110befa02132e9f53672/sheets-watch-custom%402x.png)

标准完成按钮

**如果更改默认标签，优先使用 SF Symbols 表示操作。** 避免使用可能误导用户认为表单是分层导航界面一部分的标签。此外，如果左上角的文本看起来像页面或应用标题，用户将不知道如何关闭表单。参见[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。

![Apple Watch 上显示屏幕顶部带有默认取消按钮的顶部工具栏截图。](https://docs-assets.developer.apple.com/published/4b2b3901392b3a2101bf98fbee0b7809/modal-sheet-watchos-do%402x.png)

![圆圈中的勾选标记表示正确用法。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

![Apple Watch 上显示屏幕顶部带有自定义后退按钮的顶部工具栏截图。](https://docs-assets.developer.apple.com/published/3342cdf046b51d5b7e22008f4fa36cf8/modal-sheet-watchos-do-not-1%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![Apple Watch 上显示屏幕顶部带有"页面标题"字样按钮的顶部工具栏截图。](https://docs-assets.developer.apple.com/published/7e655a4130904ed5def637dde60325f9/modal-sheet-watchos-do-not-2%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

## [资源](https://developer.apple.com/design/human-interface-guidelines/sheets#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/sheets#Related)

[模态](https://developer.apple.com/design/human-interface-guidelines/modality)

[操作表](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

[弹出框](https://developer.apple.com/design/human-interface-guidelines/popovers)

[面板](https://developer.apple.com/design/human-interface-guidelines/panels)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/sheets#Developer-documentation)

[`sheet(item:onDismiss:content:)`](https://developer.apple.com/documentation/SwiftUI/View/sheet\(item:onDismiss:content:\)) — SwiftUI

[`UISheetPresentationController`](https://developer.apple.com/documentation/UIKit/UISheetPresentationController) — UIKit

[`presentAsSheet(_:)`](https://developer.apple.com/documentation/AppKit/NSViewController/presentAsSheet\(_:\)) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/sheets#Change-log)

日期| 更改  
---|---  
2024年3月29日| 添加了在 iPadOS 应用中使用表单或页面表单样式的指导。  
2023年12月5日| 建议使用分栏视图在 visionOS 应用中提供补充项目。  
2023年6月21日| 更新以包含 visionOS 指导。  
2023年6月5日| 更新了在 watchOS 中使用表单的指导。  
  
