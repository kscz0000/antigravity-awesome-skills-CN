---
title: "Toggles | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/toggles

# 开关

开关让用户在一对对立状态之间选择，如开和关，使用不同的外观来指示每种状态。

![两个带标签的开关控件的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/f4a1d653777ba4f0b6b4b7d97d704f9f/components-toggles-intro%402x.png)

开关可以有多种样式，如开关和复选框，不同平台可以以不同方式使用这些样式。有关指导，请参阅[平台注意事项](https://developer.apple.com/design/human-interface-guidelines/toggles#Platform-considerations)。

除开关外，所有平台还支持行为类似开关的按钮，通过为每种状态使用不同外观。有关开发者指导，请参阅 [`ToggleStyle`](https://developer.apple.com/documentation/SwiftUI/ToggleStyle)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices)

**使用开关帮助用户在影响内容或视图状态的两个对立值之间选择。** 开关始终让用户管理某物的状态，因此如果您需要支持其他类型的操作——如从项目列表中选择——请使用不同的组件，如[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)。

**清楚标识开关影响的设置、视图或内容。** 通常，周围上下文提供足够信息让用户理解他们正在打开或关闭什么。在某些情况下，通常在 macOS 应用中，您还可以提供标签来描述开关控制的状态。如果您使用行为类似开关的按钮，通常使用传达其用途的界面图标，并根据当前状态更新其外观——通常通过更改背景。

**确保开关状态的视觉差异明显。** 例如，您可以添加或移除颜色填充、显示或隐藏背景形状，或更改显示的内部细节——如勾选标记或圆点——以显示开关是开还是关。避免仅依靠不同颜色来传达状态，因为并非所有人都能感知差异。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/toggles#Platform-considerations)

_tvOS、visionOS 或 watchOS 无额外注意事项。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/toggles#iOS-iPadOS)

**仅在列表行中使用开关样式。** 在这种情况下不需要提供标签，因为行中的内容为开关控制的状态提供了上下文。

**仅在必要时更改开关的默认颜色。** 默认绿色在大多数情况下效果良好，但您可能希望使用应用的强调色代替。确保使用与未着色外观有足够对比度的颜色以便感知。

![两个列表行的插图，一个带有活动开关，一个带有非活动开关。活动开关着有绿色的标准开关颜色。](https://docs-assets.developer.apple.com/published/95dd06ef1de5bf4360caef804af79b15/toggles-ios-default-color%402x.png)标准开关颜色

![两个列表行的插图，一个带有活动开关，一个带有非活动开关。活动开关着有紫色的自定义开关颜色。](https://docs-assets.developer.apple.com/published/8e40963d32263c9319f4b5f3ac3ac721/toggles-ios-custom-color%402x.png)自定义开关颜色

**在列表外，使用行为类似开关的按钮，而非开关。** 例如，电话应用在过滤按钮上使用开关让用户过滤最近通话。应用添加蓝色高亮以指示开关何时活动，并在开关非活动时移除它。

![iPhone 上电话应用上半部分的截图，显示已过滤的最近未接来电列表。右上角的过滤按钮带有蓝色高亮，指示开关处于活动状态。](https://docs-assets.developer.apple.com/published/895b4c8fd67287f587d7c0576c2555a8/toggles-ios-phone-filter-on%402x.png)

电话应用使用开关在所有最近通话和各种过滤选项之间切换。当用户选择过滤时，开关显示在符号后面绘制的自定义背景。

![iPhone 上电话应用上半部分的截图，显示所有最近通话。右上角的过滤按钮没有高亮，指示开关处于非活动状态。](https://docs-assets.developer.apple.com/published/d38180341155877eec2f5b34159ab72f/toggles-ios-phone-filter-off%402x.png)

当用户返回到主最近视图时，开关显示时符号后面没有任何内容。

**避免提供解释按钮用途的标签。** 您创建的界面图标——结合您提供的替代背景外观——帮助用户理解按钮的作用。有关开发者指导，请参阅 [`changesSelectionAsPrimaryAction`](https://developer.apple.com/documentation/UIKit/UIButton/changesSelectionAsPrimaryAction)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/toggles#macOS)

除开关样式外，macOS 还支持复选框样式，并定义了可提供类似行为的单选按钮。

**在窗口主体而非窗口框架中使用开关、复选框和单选按钮。** 特别是避免在工具栏或状态栏中使用这些组件。

#### [开关](https://developer.apple.com/design/human-interface-guidelines/toggles#Switches)

**对要强调的设置优先使用开关。** 开关比复选框有更多视觉重量，因此当它控制比复选框通常控制更多功能时看起来更好。例如，您可能使用开关让用户打开或关闭一组设置，而不仅仅是一个设置。有关开发者指导，请参阅 [`switch`](https://developer.apple.com/documentation/SwiftUI/ToggleStyle/switch)。

**在分组表单中，考虑使用迷你开关控制单行中的设置。** 迷你开关的高度与按钮和其他控件的高度相似，从而产生具有一致高度的行。如果需要在分组表单中呈现设置层次结构，可以对主要设置使用常规开关，对从属设置使用迷你开关。有关开发者指导，请参阅 [`GroupedFormStyle`](https://developer.apple.com/documentation/SwiftUI/GroupedFormStyle) 和 [`ControlSize`](https://developer.apple.com/documentation/SwiftUI/ControlSize)。

**通常，不要用开关替换复选框。** 如果您已在界面中使用复选框，最好继续使用它。

#### [复选框](https://developer.apple.com/design/human-interface-guidelines/toggles#Checkboxes)

复选框是一个小的方形按钮，关闭时为空，打开时包含勾选标记，状态混合时可包含短横线。通常，复选框在其后侧包含标题。在可编辑的检查列表中，复选框可以不带标题或任何其他内容出现。

**如果需要呈现设置层次结构，请使用复选框而非开关。** 复选框的视觉样式有助于它们很好地对齐和传达分组。通过对齐——通常沿复选框的前沿——和缩进，您可以显示依赖关系，例如当复选框的状态控制从属复选框的状态时。

![显示包含两级复选框布局的插图。](https://docs-assets.developer.apple.com/published/ec2755eb8089e275b1ebb3cd294606b0/checkbox-alignment%402x.png)

**如果需要呈现两个以上互斥选项的集合，请考虑使用单选按钮。** 当用户需要从选项中选择而不仅仅是"开"或"关"时，使用多个单选按钮可以帮助您用唯一标签阐明每个选项。

**如果复选框之间的关系不清楚，请考虑使用标签来介绍一组复选框。** 描述选项集，并将标签的基线与组中第一个复选框对齐。

**在复选框的外观中准确反映其状态。** 复选框的状态可以是开、关或混合。如果使用复选框全局打开和关闭多个从属复选框，当从属复选框具有不同状态时显示混合状态。例如，您可能需要呈现一个文本样式设置，可以打开或关闭所有样式，但也让用户选择单个样式设置的子集，如粗体、斜体或下划线。有关开发者指导，请参阅 [`allowsMixedState`](https://developer.apple.com/documentation/AppKit/NSButton/allowsMixedState)。

![显示开启状态的复选框插图，看起来像一个小的圆角方形，带有蓝色填充和白色勾选标记。](https://docs-assets.developer.apple.com/published/67efc6dab34453404f164acef3bac84d/checkbox-selected%402x.png)开

![显示关闭状态的复选框插图，看起来像一个小的圆角方形，没有填充。](https://docs-assets.developer.apple.com/published/ffd72e78175dc69a27016e8454030b71/checkbox-deselected%402x.png)关

![显示混合状态的复选框插图，看起来像一个小的圆角方形，带有蓝色填充和白色连字符。](https://docs-assets.developer.apple.com/published/f60cc3ddbea31509d83e204d963cb1d0/checkbox-mixed%402x.png)混合

#### [单选按钮](https://developer.apple.com/design/human-interface-guidelines/toggles#Radio-buttons)

单选按钮是一个小的圆形按钮，后跟标签。通常以两到五个为一组显示，单选按钮呈现一组互斥选择。

![显示一列中五个项目的插图，每个项目前面有一个单选按钮。第三个项目的单选按钮已填充，指示它被选中。](https://docs-assets.developer.apple.com/published/dee18caa44a87ddcad53b912203b2fea/radio-button-example%402x.png)

单选按钮的状态要么是选中（填充的圆圈），要么是未选中（空圆圈）。虽然单选按钮也可以显示混合状态（由短横线指示），但此状态很少有用，因为您可以使用额外的单选按钮传达多种状态。如果需要显示设置或项目具有混合状态，请考虑改用复选框。

![显示选中单选按钮的插图，看起来像一个白色圆点居中在一个带有深色填充的小圆圈中。](https://docs-assets.developer.apple.com/published/91c45b3934ecd18b42b2bb72e64ca702/radio-button-selected%402x.png)选中

![显示未选中单选按钮的插图，看起来像一个小的空圆圈。](https://docs-assets.developer.apple.com/published/1bec25f63381d81a41f885e1338eb571/radio-button-deselected%402x.png)未选中

**优先使用一组单选按钮来呈现互斥选项。** 如果需要让用户在集合中选择多个选项，请改用复选框。

**避免在一组中列出太多单选按钮。** 一长串单选按钮在界面中占用大量空间，可能令人不知所措。如果需要呈现大约五个以上选项，请考虑使用[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)等组件代替。

**要呈现可以打开或关闭的单个设置，请优先使用复选框。** 虽然单个单选按钮也可以打开或关闭某物，但复选框中勾选标记的存在或缺失可以使当前状态一目了然。在单个复选框无法清楚传达对立状态的罕见情况下，您可以使用一对单选按钮，每个都带有指定其控制状态的标签。

**水平显示单选按钮时使用一致的间距。** 测量容纳最长按钮标签所需的空间，并一致使用该测量值。

![显示一行中三个项目的插图，每个项目前面有一个单选按钮。第一个和第三个项目有长文本标签，而第二个有短标签。每个项目占用的水平空间相等。填充的单选按钮位于第二个项目前面，指示它被选中。](https://docs-assets.developer.apple.com/published/95fc61aefa156d2d78d9eb6589a47f6e/radio-button-equal-spacing%402x.png)

## [资源](https://developer.apple.com/design/human-interface-guidelines/toggles#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/toggles#Related)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/toggles#Developer-documentation)

[`Toggle`](https://developer.apple.com/documentation/SwiftUI/Toggle) — SwiftUI

[`UISwitch`](https://developer.apple.com/documentation/UIKit/UISwitch) — UIKit

[`NSButton.ButtonType.toggle`](https://developer.apple.com/documentation/AppKit/NSButton/ButtonType/toggle) — AppKit

[`NSSwitch`](https://developer.apple.com/documentation/AppKit/NSSwitch) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/toggles#Change-log)

日期| 变更  
---|---  
2024年3月29日| 增强了在 macOS 应用中使用开关的指导，阐明了复选框何时有标题，并为单选按钮添加了插图。  
2023年9月12日| 更新了插图。  
