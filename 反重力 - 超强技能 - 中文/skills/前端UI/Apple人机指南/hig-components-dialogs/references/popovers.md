---
title: "Popovers | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/popovers

# 弹出框

弹出框是一种临时视图，当用户点击或轻触控件或交互区域时，在其他内容上方显示。

![弹出框视图的概念图。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/90068cb259f3c3d15e6adf38766dd706/components-popover-intro%402x.png)

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices)

**使用弹出框展示少量信息或功能。** 由于弹出框在用户与之交互后会消失，将弹出框中的功能限制为几个相关任务。例如，日历事件弹出框让用户可以轻松更改事件的日期或时间，或将其移动到另一个日历。更改后弹出框消失，让用户继续查看日历上的事件。

**当需要更多内容空间时考虑使用弹出框。** 侧边栏和面板等视图占用大量空间。如果只需临时显示内容，在弹出框中显示可以简化界面。

**正确定位弹出框。** 确保弹出框的箭头尽可能直接指向触发它的元素。理想情况下，弹出框不应覆盖触发它的元素或用户在使用时可能需要查看的重要内容。

**仅在需要确认和指导时使用关闭按钮。** 如果关闭按钮（包括取消或完成）能提供清晰性（如带或不带保存更改退出），则值得包含。否则，弹出框通常在用户点击或轻触其边界外部或选择弹出框中的项目时关闭。如果可能进行多项选择，确保弹出框保持打开，直到用户明确关闭或点击或轻触其边界外部。

**自动关闭非模态弹出框时始终保存工作。** 用户可能因点击或轻触边界外部而意外关闭非模态弹出框。仅在用户点击或轻触明确的取消按钮时丢弃用户的工作。

**一次只显示一个弹出框。** 显示多个弹出框会使界面混乱并造成困惑。切勿显示级联或层级弹出框，即一个弹出框从另一个弹出框中弹出。如需显示新弹出框，先关闭已打开的弹出框。

**不要在弹出框上显示其他视图。** 确保没有任何内容显示在弹出框上方，警告框除外。

**尽可能让用户通过单次点击或轻触关闭一个弹出框并打开另一个。** 避免额外手势尤其适用于多个不同栏按钮各自打开弹出框的情况。

**避免让弹出框过大。** 弹出框只需大到足以显示其内容并指向来源位置。如有必要，系统可以调整弹出框大小以确保其在界面中适配良好。

**更改弹出框大小时提供平滑过渡。** 某些弹出框提供相同信息的精简和扩展视图。如果调整弹出框大小，请动画化更改以避免给人新弹出框替换旧弹出框的印象。

**避免在帮助文档中使用"弹出框"一词。** 相反，引用具体任务或选择。例如，不要写"选择弹出框底部的显示按钮"，可以写"选择显示按钮"。

**避免使用弹出框显示警告。** 用户可能错过弹出框或意外关闭它。如需警告用户，改用[警告框](https://developer.apple.com/design/human-interface-guidelines/alerts)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/popovers#Platform-considerations)

 _visionOS 无其他注意事项。tvOS 或 watchOS 不支持。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/popovers#iOS-iPadOS)

**避免在紧凑视图中显示弹出框。** 让应用或游戏根据内容区域的大小类动态调整布局。弹出框保留给宽视图；对于紧凑视图，通过在表单等全屏模态视图中展示信息来使用所有可用屏幕空间。相关指导参见[模态](https://developer.apple.com/design/human-interface-guidelines/modality)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/popovers#macOS)

在 macOS 中，可以让弹出框可分离，当用户拖动它时变成独立面板。面板在用户与其他内容交互时保持可见。

  * 附加弹出框 
  * 分离弹出框 



![日历中事件的示意图，事件的附加版本弹出框在旁边并指向它。](https://docs-assets.developer.apple.com/published/ef05d3cb071e4c11209cce39b596ca99/attached-popover%402x.png)

![日历中事件的示意图，事件的分离版本弹出框在旁边。](https://docs-assets.developer.apple.com/published/d0b16d14a582a887f385896669394ee4/detached-popover%402x.png)

**考虑让用户分离弹出框。** 如果用户希望在弹出框保持可见时查看其他信息，他们可能会欣赏能够将弹出框转换为面板的功能。

**对分离的弹出框做最少的外观更改。** 看起来与原始弹出框相似的面板有助于用户保持上下文。

## [资源](https://developer.apple.com/design/human-interface-guidelines/popovers#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/popovers#Related)

[表单](https://developer.apple.com/design/human-interface-guidelines/sheets)

[操作表](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

[警告框](https://developer.apple.com/design/human-interface-guidelines/alerts)

[模态](https://developer.apple.com/design/human-interface-guidelines/modality)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/popovers#Developer-documentation)

[`popover(isPresented:attachmentAnchor:arrowEdge:content:)`](https://developer.apple.com/documentation/SwiftUI/View/popover\(isPresented:attachmentAnchor:arrowEdge:content:\)) — SwiftUI

[`UIPopoverPresentationController`](https://developer.apple.com/documentation/UIKit/UIPopoverPresentationController) — UIKit

[`NSPopover`](https://developer.apple.com/documentation/AppKit/NSPopover) — AppKit
