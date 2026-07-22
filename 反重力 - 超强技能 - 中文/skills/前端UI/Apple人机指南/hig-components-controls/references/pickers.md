---
title: "Pickers | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/pickers

# 选择器

选择器显示一个或多个可滚动的不同值列表供用户选择。

![可滚动列表中选中项目的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/56b152d613ef1fc1424549eaa95a23d6/components-pickers-intro%402x.png)

系统提供多种样式的选择器，每种都提供不同类型的可选值并具有不同的外观。选择器中显示的确切值及其顺序取决于设备语言。

选择器帮助用户通过选择单一或多部分值输入信息。日期选择器特别提供其他选择值的方式，如在日历视图中选择一天或使用数字键盘输入日期和时间。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/pickers#Best-practices)

**考虑使用选择器提供中到长项目列表。** 如果需要显示相当短的选择列表，请考虑使用[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)而非选择器。虽然选择器使快速滚动浏览许多项目变得容易，但它可能为短项目列表增加太多视觉重量。另一方面，如果需要呈现非常大的项目集合，请考虑使用[列表或表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)。列表和表格可以调整高度，表格可以包含索引，这使得定位列表的某个部分更快。

**使用可预测且逻辑排序的值。** 在用户与选择器交互之前，其许多值可能被隐藏。最好让用户能够预测隐藏值是什么，例如按字母顺序排列的国家列表，以便他们可以快速浏览项目。

**避免切换视图来显示选择器。** 选择器在上下文中、用户正在编辑的字段下方或附近显示时效果很好。选择器通常出现在窗口底部或弹出框中。

**考虑在日期选择器中指定分钟时提供较少的粒度。** 默认情况下，分钟列表包含 60 个值（0 到 59）。您可以选择增加分钟间隔，只要它能被 60 整除。例如，您可能想要 15 分钟间隔（0、15、30 和 45）。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/pickers#Platform-considerations)

_visionOS 无额外注意事项。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/pickers#iOS-iPadOS)

日期选择器是使用触摸、键盘或指针设备选择特定日期、时间或两者的高效界面。您可以用以下样式之一显示日期选择器：

* 紧凑 — 一个按钮，在模态视图中显示可编辑的日期和时间内容。

* 内联 — 仅时间时，显示值滚轮的按钮；对于日期和时间，显示内联日历视图。

* 滚轮 — 一组滚动滚轮，也支持通过内置或外部键盘进行数据输入。

* 自动 — 基于当前平台和日期选择器模式的系统确定样式。




日期选择器有四种模式，每种呈现不同的可选值集合。

* 日期 — 显示月份、日期和年份。

* 时间 — 显示小时、分钟和（可选）AM/PM 标识。

* 日期和时间 — 显示日期、小时、分钟和（可选）AM/PM 标识。

* 倒计时计时器 — 显示小时和分钟，最多 23 小时 59 分钟。此模式在内联或紧凑样式中不可用。




日期选择器中显示的确切值及其顺序取决于设备位置。

以下是显示样式和模式不同组合的几个日期选择器示例。

* 紧凑 
* 内联 
* 滚轮 




![紧凑日期选择器的插图，单行内联显示当前选中的日期。选择器作为从行向下延伸的弹出框打开，包含完整的日历月用于选择日期。](https://docs-assets.developer.apple.com/published/65d6693bf614da95dde6a82006037c86/pickers-date-picker-compact-expanded%402x.png)在紧凑布局中，选择器作为弹出框在内容上方打开。

![内联日期选择器的插图，标题为"日期"。顶部的开关打开，下方出现用于选择日期的日历月。](https://docs-assets.developer.apple.com/published/053773055a1630d38d3baa6ec6147f5d/pickers-date-picker-inline-expanded%402x.png)在内联布局中，选择器与内容内联打开。

![内联时间选择器的插图，标题为"时间"。当前选中的时间出现在标题行中，标题行下方出现三个垂直滚轮用于选择小时、分钟和 AM 或 PM 值。](https://docs-assets.developer.apple.com/published/4474f286571f0a7b875bbd940f39bb78/pickers-time-picker-inline-wheel%402x.png)另一个使用滚轮选择日期和时间值的内联选择器示例。

**当空间受限时使用紧凑日期选择器。** 紧凑样式显示一个按钮，以应用的强调色显示当前值。当用户点击按钮时，日期选择器打开模态视图，提供对熟悉的日历样式编辑器和时间选择器的访问。在模态视图中，用户可以在点击视图外部确认选择之前对日期和时间进行多次编辑。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/pickers#macOS)

**选择适合应用的日期选择器样式。** macOS 中有两种日期选择器样式：文本和图形。当空间有限且希望用户进行特定日期和时间选择时，文本样式很有用。当您希望让用户浏览日历中的天数或选择日期范围，或时钟表盘的外观适合您的应用时，图形样式很有用。

有关开发者指导，请参阅 [`NSDatePicker`](https://developer.apple.com/documentation/AppKit/NSDatePicker)。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/pickers#tvOS)

选择器在 tvOS 中可通过 SwiftUI 使用。有关开发者指导，请参阅 [`Picker`](https://developer.apple.com/documentation/SwiftUI/Picker)。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/pickers#watchOS)

选择器显示用户使用数码表冠导航的项目列表，帮助用户以精确且引人入胜的方式管理选择。

选择器可以使用滚轮样式显示项目列表。watchOS 还可以使用滚轮样式显示日期和时间选择器。有关开发者指导，请参阅 [`Picker`](https://developer.apple.com/documentation/SwiftUI/Picker) 和 [`DatePicker`](https://developer.apple.com/documentation/SwiftUI/DatePicker)。

![Apple Watch 上包含选择器视图的屏幕表示，显示列表中的三个项目。中间项目高亮显示。](https://docs-assets.developer.apple.com/published/00d1eeb88cc503430767c2318605a71d/pickers-wheel-watch%402x.png)

![Apple Watch 上包含日期选择器的屏幕表示，日期高亮显示。](https://docs-assets.developer.apple.com/published/30053c6f5cb2c0246e5ebecbd8ad70c3/pickers-date-watch%402x.png)

![Apple Watch 上包含时间选择器的屏幕表示，分钟高亮显示。](https://docs-assets.developer.apple.com/published/842ba89f2c3fdb2894949dee31bf8849/pickers-time-watch%402x.png)

您可以将选择器配置为显示轮廓、标题和滚动指示器。

对于较长列表，导航链接将选择器显示为按钮。当用户点击按钮时，系统显示选项列表。用户还可以使用数码表冠浏览选项而无需点击按钮。有关开发者指导，请参阅 [`navigationLink`](https://developer.apple.com/documentation/SwiftUI/PickerStyle/navigationLink)。

![Apple Watch 上包含选择器按钮的屏幕表示。按钮文本表示选中了第二个项目。](https://docs-assets.developer.apple.com/published/657d90a59d600e7eee70effde6784e45/pickers-navigation-button-watch%402x.png)

![Apple Watch 上显示项目列表的屏幕表示。列表中的第二个项目被选中。](https://docs-assets.developer.apple.com/published/1e533809fb6fc291a53fd12ff0ec41f4/pickers-navigation-list-watch%402x.png)

## [资源](https://developer.apple.com/design/human-interface-guidelines/pickers#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/pickers#Related)

[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/pickers#Developer-documentation)

[`Picker`](https://developer.apple.com/documentation/SwiftUI/Picker) — SwiftUI

[`UIDatePicker`](https://developer.apple.com/documentation/UIKit/UIDatePicker) — UIKit

[`UIPickerView`](https://developer.apple.com/documentation/UIKit/UIPickerView) — UIKit

[`NSDatePicker`](https://developer.apple.com/documentation/AppKit/NSDatePicker) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/pickers#Change-log)

日期| 变更  
---|---  
2023年6月5日| 更新了在 watchOS 中使用选择器的指导。  
