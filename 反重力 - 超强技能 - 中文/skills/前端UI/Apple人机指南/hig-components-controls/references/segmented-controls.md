---
title: "Segmented controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/segmented-controls

# 分段控件

分段控件是由两个或更多分段组成的线性集合，每个分段都作为按钮运作。

![分段控件中选中分段的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/89298764551d236435a7057412cf2e06/components-segmented-control-intro%402x.png)

在分段控件中，所有分段通常宽度相等。与[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)一样，分段可以包含文本或图像。分段也可以在其下方（或整个控件下方）有文本标签。

分段控件从一组选项中提供单一选择，或在 macOS 中提供单一选择或多重选择。例如，在 macOS Keynote 中，用户可以在对齐选项控件中仅选择一个分段来对齐选中文本。相比之下，用户可以在字体属性控件中选择多个分段来组合粗体、斜体和下划线等样式。Keynote 窗口的工具栏也使用分段控件让用户在主窗口区域内显示和隐藏各种编辑窗格。

![由四个文本对齐选项组成的分段控件的部分截图。居中对齐选项被选中。](https://docs-assets.developer.apple.com/published/7ed5112804ec078b8ba281e30a30ec85/segmented-control-one-choice%402x.png)单一选择

![由四种字体类型组成的分段控件的部分截图。四个选项中有三个被选中。](https://docs-assets.developer.apple.com/published/0b1d550e9c4fc6e201d45640fad819eb/segmented-control-multiple-choices%402x.png)多重选择

除了表示单一或多重选择状态外，分段控件还可以作为一组不显示选择状态的操作按钮。例如，macOS Mail 中的回复、全部回复和转发按钮。有关开发者指导，请参阅 [`isMomentary`](https://developer.apple.com/documentation/UIKit/UISegmentedControl/isMomentary) 和 [`NSSegmentedControl.SwitchTracking.momentary`](https://developer.apple.com/documentation/AppKit/NSSegmentedControl/SwitchTracking/momentary)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Best-practices)

**使用分段控件提供影响对象、状态或视图的密切相关选择。** 例如，检查器中的分段控件可以让用户选择一个或多个属性应用于选择，或工具栏中的分段控件可以提供一组在当前视图上执行的操作。

![iOS 健康应用活动屏幕上半部分的截图，显示移动和锻炼活动的图表。图表上方的分段控件选择了 D，表示图表显示一天的活动。](https://docs-assets.developer.apple.com/published/f82bafe0f162b0181f6d50661109464b/segmented-controls-activity-charts%402x.png)

在 iOS 健康应用中，分段控件提供活动图表显示的时间范围选择。

**当将功能分组在一起或清楚显示其选择状态很重要时，考虑使用分段控件。** 与其他按钮样式不同，分段控件无论视图大小或出现位置如何都保持其分组。这种分组还可以帮助用户一目了然地了解当前选中哪些控件。

**在单个分段控件内保持控件类型一致。** 不要在表示选择状态的控件中为分段分配操作，也不要在执行操作的控件中为分段显示选择状态。

**限制控件中的分段数量。** 太多分段可能难以解析且导航耗时。在宽界面中目标是不超过约五到七个分段，在 iPhone 上不超过约五个分段。

**通常，保持分段大小一致。** 当所有分段宽度相等时，分段控件感觉平衡。尽可能保持图标和标题宽度一致也是最好的。

## [内容](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Content)

**优先在单个分段控件中使用文本或图像——而非两者混合。** 虽然单个分段可以包含文本标签或图像，但在单个控件中混合两者可能导致界面脱节和混乱。

**尽可能在每个分段中使用大小相似的内容。** 由于所有分段通常宽度相等，如果内容填满某些分段但不填满其他分段，看起来不好。

**为分段标签使用名词或名词短语。** 编写描述每个分段的文本，并使用[标题样式大写](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64)。显示文本标签的分段控件不需要介绍性文本。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Platform-considerations)

_watchOS 不支持。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#iOS-iPadOS)

**考虑使用分段控件在密切相关的子视图之间切换。** 分段控件可以作为快速切换相关子视图的方式很有用。例如，日历的新建事件表单页中的分段控件在创建新事件和新提醒的子视图之间切换。对于在应用完全独立的区域之间切换，请改用[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)。

![iOS 日历应用上半部分的截图，显示新建事件表单页。分段控件提供在添加新事件和新提醒之间切换的能力。](https://docs-assets.developer.apple.com/published/2438acc643ee037a518cad7a15b18709/segmented-controls-calendar-new-event%402x.png)

### [macOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#macOS)

**考虑使用介绍性文本阐明分段控件的用途。** 当控件使用符号或界面图标时，您还可以在每个分段下方添加标签以阐明其含义。如果您的应用包含工具提示，请为分段控件中的每个分段提供一个。

**在主窗口区域使用标签视图——而非分段控件——进行视图切换。** [标签视图](https://developer.apple.com/design/human-interface-guidelines/tab-views)支持高效的视图切换，外观类似于与分段控件组合的[框](https://developer.apple.com/design/human-interface-guidelines/boxes)。考虑使用分段控件帮助用户在工具栏或检查器窗格中切换视图。

![macOS 日历应用的截图。主窗口区域显示包含四个标签的标签视图：日、周、月和年。侧边栏显示包含两个分段的分段控件：新建和已回复。](https://docs-assets.developer.apple.com/published/e0a8dd930dcd6e099b72c643b6077a7b/macos-calendar-tab-view-segmented-control-comparison%402x.png)

**考虑支持弹簧加载。** 在配备 Magic Trackpad 的 Mac 上，弹簧加载让用户可以通过将选中项目拖到分段上并强制点击来激活分段，而无需放下选中的项目。用户还可以在分段激活后继续拖动项目。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#tvOS)

**在执行内容过滤的屏幕上考虑使用分栏视图而非分段控件。** 用户通常发现使用分栏视图在内容和过滤选项之间来回导航很容易。根据其位置，分段控件可能不那么容易访问。

**避免将其他可聚焦元素放在分段控件附近。** 当焦点移动到分段时它们会变为选中状态，而不是当用户点击它们时。仔细考虑相对于其他界面元素放置分段控件的位置。如果其他可聚焦元素太近，用户在尝试在分段之间切换时可能会意外聚焦到它们。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#visionOS)

当用户查看使用图标的分段控件时，系统显示包含您提供的描述性文本的工具提示。

## [资源](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Related)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Developer-documentation)

[`segmented`](https://developer.apple.com/documentation/SwiftUI/PickerStyle/segmented) — SwiftUI

[`UISegmentedControl`](https://developer.apple.com/documentation/UIKit/UISegmentedControl) — UIKit

[`NSSegmentedControl`](https://developer.apple.com/documentation/AppKit/NSSegmentedControl) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/segmented-controls#Change-log)

日期| 变更  
---|---  
2023年6月21日| 更新以包含 visionOS 指导。  
