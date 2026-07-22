---
title: "Tab views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/tab-views

# 标签视图

标签视图在同一区域呈现多个互斥的内容窗格，人们可以使用标签控件在它们之间切换。

![带有两个带标签标签的视图的风格化表示，第一个被选中。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/4b2dbd07b3c6fe1d349d6db6aad5890b/components-tab-view-intro%402x.png)

## 最佳实践

**使用标签视图呈现密切相关的内容区域。** 标签视图的外观提供强烈的视觉封闭指示。人们期望每个标签显示在某种程度上与其他标签内容相似或相关的内容。

**确保窗格内的控件仅影响同一窗格中的内容。** 窗格是互斥的，因此确保它们完全自包含。

**为每个标签提供描述其窗格内容的标签。** 好的标签帮助人们在点击或点击其标签之前预测窗格内容。通常，为标签标签使用名词或短名词短语。动词或短动词短语在某些上下文中可能有意义。为标签标签使用标题式大写。

**避免使用弹出按钮在标签之间切换。** 标签控件效率高，因为它只需单击或点击即可进行选择，而弹出按钮需要两次。标签控件还同时在屏幕上呈现所有选择，而人们必须点击弹出按钮才能看到其选择。注意，在有太多内容窗格无法合理地用标签显示的情况下，弹出按钮可能是合理的替代方案。

**避免在标签视图中提供超过六个标签。** 超过六个标签可能会令人不知所措并造成布局问题。如果您需要呈现六个或更多标签，请考虑另一种实现界面的方式。例如，您可以改为将每个标签作为弹出按钮菜单中的视图选项呈现。

开发者指南请参阅 [`NSTabView`](https://developer.apple.com/documentation/AppKit/NSTabView)。

## 结构

标签控件出现在内容区域的顶部边缘。您可以选择隐藏控件，这对于以编程方式在窗格之间切换的应用是合适的。

![窗口的插图，其中三标签标签控件在内容视图的顶部边缘居中。](https://docs-assets.developer.apple.com/published/05bb7fbc6365c3bab10db218644756c3/tab-views-top%402x.png)

当您隐藏标签控件时，内容区域可以是无边框的、带边框的或用线条加边框。无边框视图可以是实心的或透明的。

**通常，通过在标签视图的所有侧面留下窗口主体区域的边距来内嵌标签视图。** 此布局看起来整洁，并为与标签视图内容不直接相关的额外控件留出空间。您可以将标签视图延伸到窗口边缘，但此布局不常见。

## 平台注意事项

iOS、iPadOS、tvOS 和 visionOS 不支持。

### iOS、iPadOS

对于类似功能，请考虑改用[分段控件](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)。

### watchOS

watchOS 使用[页面控件](https://developer.apple.com/design/human-interface-guidelines/components/presentation/page-controls)显示标签视图。开发者指南请参阅 [`TabView`](https://developer.apple.com/documentation/SwiftUI/TabView) 和 [`verticalPage`](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/verticalPage)。

![显示 Apple Watch 上数码表冠旁边页面控件的插图。当前点被放大，指示人们可以滚动当前内容以及在页面之间滚动。](https://docs-assets.developer.apple.com/published/10938a94cb663210f148e0fbce431e70/tab-view-watch-vertical%402x.png)

## 资源

#### 相关

[Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

[Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)

#### 开发者文档

[`TabView`](https://developer.apple.com/documentation/SwiftUI/TabView) — SwiftUI

[`NSTabView`](https://developer.apple.com/documentation/AppKit/NSTabView) — AppKit

## 变更日志

日期| 变更
---|---
2023年6月5日| 添加了在 watchOS 中使用标签视图的指南。
