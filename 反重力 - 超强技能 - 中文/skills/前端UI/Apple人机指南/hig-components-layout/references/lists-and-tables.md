---
title: "Lists and tables | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/lists-and-tables

# 列表和表格

列表和表格在一个或多个列的行中呈现数据。

![三行表格的风格化表示，带有标题和页脚文本。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/c3e26d2515ac05cae7aba2704f8640d6/components-lists-and-tables-intro%402x.png)

表格或列表可以表示按组或层级组织的数据，并支持选择、添加、删除和重新排序等用户交互。所有平台的应用和游戏都可以使用表格来呈现内容和选项；许多应用使用列表来表达整体信息层级并帮助人们导航。例如，iOS 设置使用列表层级帮助人们选择选项，多个应用——如 iPadOS 和 macOS 中的邮件——在[分割视图](https://developer.apple.com/design/human-interface-guidelines/split-views)中使用表格。

有时，人们需要在多列表格或电子表格中处理复杂数据。提供生产力任务的应用通常使用表格在单独的可排序列中表示数据的各种特征或属性。

## 最佳实践

**优先在列表或表格中显示文本。** 表格可以包含任何类型的内容，但基于行的格式特别适合使文本易于扫描和阅读。如果您的项目大小差异很大——或需要显示大量图像——请考虑改用[集合](https://developer.apple.com/design/human-interface-guidelines/collections)。

**适当时让人们编辑表格。** 人们希望能够重新排序列表，即使他们无法添加或删除项目。在 iOS 和 iPadOS 中，人们必须进入编辑模式才能选择表格项目。

**当人们选择列表项时提供适当的反馈。** 反馈可能因选择项目是显示新视图还是切换项目状态而异。通常，帮助人们导航层级的表格会持久高亮所选行以阐明人们采取的路径。相比之下，列出选项的表格通常只短暂高亮一行，然后添加图像——如复选标记——表示该项目已被选中。

## 内容

**保持项目文本简洁，使行内容易于阅读。** 简短、简洁的文本有助于最小化截断和换行，使文本更易于阅读和扫描。如果每个项目包含大量文本，请考虑帮助您避免显示过大表格行的替代方案。例如，您可以只列出项目标题，让人们选择项目以在详情视图中显示其内容。

**考虑保持可能被剪切或截断的文本可读性的方法。** 当表格较窄时——例如，如果人们可以改变其宽度——您希望内容保持可识别和易于阅读。有时，文本中间的省略号可以使项目更易于区分，因为它保留了内容的开头和结尾。

**在多列表格中使用描述性列标题。** 使用名词或短名词短语，采用[标题式大写](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64)，不加结尾标点。如果在单列表格视图中不包含列标题，请使用标签或标题帮助人们理解上下文。

## 样式

**选择与您的数据和平台协调的表格或列表样式。** 某些样式使用视觉细节帮助传达分组和层级或提供特定体验。例如，在 iOS 和 iPadOS 中，分组样式使用标题、页脚和额外空间分隔数据组；watchOS 中可用的椭圆样式使项目在人们滚动时看起来像从圆角表面滚落；macOS 定义了边框样式，使用交替行背景帮助使大型表格更易于使用。开发者指南请参阅 [`ListStyle`](https://developer.apple.com/documentation/SwiftUI/ListStyle)。

**选择适合您需要显示信息的行样式。** 例如，您可能需要在行的前端显示小图像，后跟简短说明标签。某些平台提供内置行样式，您可以使用它们在列表行中排列内容，例如 [`UIListContentConfiguration`](https://developer.apple.com/documentation/UIKit/UIListContentConfiguration-swift.struct) API，您可以使用它在 iOS、iPadOS 和 tvOS 中布局列表行、标题和页脚的内容。

## 平台注意事项

### iOS、iPadOS、visionOS

**仅使用信息按钮显示有关行内容的更多信息。** 信息按钮——当它出现在列表行中时称为详情展示按钮——不支持通过层级表格或列表导航。如果需要让人们深入查看列表或表格行的子视图，请使用展示指示器附件控件。开发者指南请参阅 [`UITableViewCell.AccessoryType.disclosureIndicator`](https://developer.apple.com/documentation/UIKit/UITableViewCell/AccessoryType-swift.enum/disclosureIndicator)。

![分组行列表的插图。每个列表项在行的后端包含一个信息按钮。](https://docs-assets.developer.apple.com/published/fd301d26835e0341b95eaa2027f200f2/info-button-in-list%402x.png)信息按钮显示有关列表项的详情；它不支持导航。

![分组行列表的插图。每个列表项在行的后端包含向右指向的 V 形。](https://docs-assets.developer.apple.com/published/dcb3678fe458846713b03756ab5e1a28/disclosure-indicator-in-list%402x.png)展示指示器显示层级中的下一级别；它不显示有关项目的详情。

**避免向在其行后端显示控件（如展示指示器）的表格添加索引。** 索引通常由字母表中的字母组成，垂直显示在列表的后端。人们可以通过选择映射到特定分区的索引字母跳转到该分区。因为索引和展示指示器等元素都出现在列表的后端，人们可能难以使用一个元素而不激活另一个。

### macOS

**当有价值时，让人们点击列标题以基于该列对表格视图排序。** 如果人们点击已排序列的标题，则以相反方向重新排序数据。

**让人们调整列宽。** 表格视图中显示的数据通常宽度各异。人们希望能够调整列宽以帮助他们专注于不同区域或显示被剪切的数据。

**考虑在多列表格中使用交替行颜色。** 交替颜色可以帮助人们跨列跟踪行值，尤其是在宽表格中。

**使用大纲视图而非表格视图呈现层级数据。** [大纲视图](https://developer.apple.com/design/human-interface-guidelines/outline-views)看起来像表格视图，但包含用于展示嵌套数据级别的展示三角形。例如，大纲视图可能显示文件夹及其包含的项目。

### tvOS

**确认表格附近的图像在每个行获得焦点并略微增大尺寸时仍然看起来良好。** 获得焦点的行的角落也可能变圆，这可能影响其两侧图像的外观。在准备图像时考虑此效果，不要添加自己的遮罩来圆角化角落。

### watchOS

**尽可能限制行数。** 短列表更易于人们扫描，但有时人们期望长项目列表。例如，如果人们订阅了大量播客，如果他们无法查看所有项目，他们可能会认为出了问题。您可以通过列出最相关的项目并提供让人们查看更多的方式来帮助使长列表更易于管理。

**如果您想支持垂直基于页面的导航，请限制详情视图的长度。** 人们使用垂直基于页面的导航在不同列表行的详情项之间垂直滑动。以这种方式导航节省时间，因为人们不需要返回列表来点击新的详情项，但它仅在详情视图较短时有效。如果您的详情视图滚动，人们将无法使用垂直基于页面的导航在其中滑动。

## 资源

#### 相关

[Collections](https://developer.apple.com/design/human-interface-guidelines/collections)

[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### 开发者文档

[`List`](https://developer.apple.com/documentation/SwiftUI/List) — SwiftUI

[Tables](https://developer.apple.com/documentation/SwiftUI/Tables) — SwiftUI

[`UITableView`](https://developer.apple.com/documentation/UIKit/UITableView) — UIKit

[`NSTableView`](https://developer.apple.com/documentation/AppKit/NSTableView) — AppKit

#### 视频

[![](https://devimages-cdn.apple.com/wwdc-services/images/49/1636D358-5C36-4027-B204-81FFE4D05B7D/3455_wide_250x141_1x.jpg) Stacks, Grids, and Outlines in SwiftUI ](https://developer.apple.com/videos/play/wwdc2020/10031)

## 变更日志

日期| 变更
---|---
2023年6月21日| 更新以包含 visionOS 指南。
2023年6月5日| 更新指南以反映 watchOS 10 中的变更。
