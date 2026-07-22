---
title: "Outline views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/outline-views

# 大纲视图

大纲视图在组织成列和行的滚动单元格列表中呈现层级数据。

![文件夹和图像列表的风格化表示，显示在包含四列的大纲视图中：[名称]、[修改日期]、[大小]和[类型]。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/30462b13b59c89c7ba9e142a2fcef05b/components-outline-view-intro%402x.png)

大纲视图至少包含一个包含主要层级数据的列，例如一组父容器及其子项。您可以根据需要添加列来显示补充主要数据的属性；例如，大小和修改日期。父容器具有展开三角形，展开后显示其子项。

Finder 窗口提供用于导航文件系统的大纲视图。

## 最佳实践

大纲视图非常适合显示基于文本的内容，通常出现在[分割视图](https://developer.apple.com/design/human-interface-guidelines/split-views)的前端，相关内容在另一端。

**使用表格而非大纲视图呈现非层级数据。** 指南请参阅[列表和表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)。

**仅在第一列中暴露数据层级。** 其他列可以显示适用于主列层级数据的属性。

**使用描述性列标题提供上下文。** 使用名词或短名词短语，采用[标题式大写](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64)且不加标点；特别是避免添加尾随冒号。始终在多列大纲视图中提供列标题。如果在单列大纲视图中不包含列标题，请使用标签或其他方式确保有足够的上下文。

**考虑让人们点击列标题对大纲视图排序。** 在可排序大纲视图中，人们可以点击列标题基于该列执行升序或降序排序。如有必要，您可以在后台基于辅助列实现额外排序。如果人们点击主列标题，排序在每个层级发生。例如，在 Finder 中，所有顶级文件夹被排序，然后每个文件夹内的项目被排序。如果人们点击已排序列的标题，文件夹及其内容以相反方向再次排序。

**让人们调整列宽。** 大纲视图中显示的数据通常宽度各异。让人们根据需要调整列宽以显示比列更宽的数据很重要。

**使人们易于展开或折叠嵌套容器。** 例如，在 Finder 窗口中点击文件夹的展开三角形仅展开该文件夹。但是，Option 点击展开三角形会展开其所有子文件夹。

**保留人们的展开选择。** 如果人们展开大纲视图的各个级别以到达特定项目，请存储状态以便下次再次显示。这样，人们不需要再次导航到同一位置。

**考虑在多列大纲视图中使用交替行颜色。** 交替颜色可以使人们更容易跨列跟踪行值，尤其是在宽大纲视图中。

**如果在应用中有意义，让人们编辑数据。** 在可编辑大纲视图单元格中，人们期望能够单击单元格编辑其内容。注意单元格对双击可能有不同响应。例如，列出文件的大纲视图可能让人们单击文件名编辑它，但双击文件名打开文件。如果有用，您还可以让人们重新排序、添加和删除行。

**考虑使用居中省略号截断单元格文本而非剪切。** 中间的省略号保留单元格文本的开头和结尾，可以使内容比剪切文本更独特和可识别。

**考虑提供搜索字段帮助人们在冗长的大纲视图中快速找到值。** 以大纲视图为主要功能的窗口通常在工具栏中包含搜索字段。指南请参阅[搜索字段](https://developer.apple.com/design/human-interface-guidelines/search-fields)。

## 平台注意事项

iOS、iPadOS、tvOS、visionOS 和 watchOS 不支持。

## 资源

#### 相关

[Column views](https://developer.apple.com/design/human-interface-guidelines/column-views)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

#### 开发者文档

[`OutlineGroup`](https://developer.apple.com/documentation/SwiftUI/OutlineGroup) — SwiftUI

[`NSOutlineView`](https://developer.apple.com/documentation/AppKit/NSOutlineView) — AppKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/49/1636D358-5C36-4027-B204-81FFE4D05B7D/3455_wide_250x141_1x.jpg) Stacks, Grids, and Outlines in SwiftUI ](https://developer.apple.com/videos/play/wwdc2020/10031)
