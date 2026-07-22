---
title: "Column views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/column-views

# 分栏视图

分栏视图——也称为浏览器——让人们使用一系列垂直分栏查看和导航数据层级。

![三个分栏的风格化表示，包含文件夹列表、图像和文件信息。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/34ebf07677359428c45cbda0b9c1641e/components-column-view-intro%402x.png)

每个分栏代表层级的一个级别，包含数据项的水平行。在分栏内，任何包含嵌套子项的父项都标有三角形图标。当人们选择父项时，下一分栏显示其子项。人们可以继续以这种方式导航，直到到达没有子项的项，也可以向上导航以探索数据的其他分支。

注意

如果需要在 iPadOS 或 visionOS 应用中管理层级内容的呈现，请考虑使用[分割视图](https://developer.apple.com/design/human-interface-guidelines/split-views)。

## 最佳实践

当您有深层级数据结构，人们倾向于在级别之间频繁来回导航，且不需要[列表或表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)提供的排序功能时，考虑使用分栏视图。例如，Finder 提供分栏视图（除图标、列表和画廊视图外）用于导航目录结构。

**在第一分栏中显示数据层级的根级别。** 人们知道可以快速滚动回第一分栏，从顶部重新开始导航层级。

**当没有嵌套项可显示时，考虑显示有关所选项的信息。** 例如，Finder 显示所选项的预览以及创建日期、修改日期、文件类型和大小等信息。

**让人们调整分栏宽度。** 如果某些数据项的名称太长无法放入默认分栏宽度内，这一点尤为重要。

## 平台注意事项

iOS、iPadOS、tvOS、visionOS 和 watchOS 不支持。

## 资源

#### 相关

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

#### 开发者文档

[`NSBrowser`](https://developer.apple.com/documentation/AppKit/NSBrowser) — AppKit
