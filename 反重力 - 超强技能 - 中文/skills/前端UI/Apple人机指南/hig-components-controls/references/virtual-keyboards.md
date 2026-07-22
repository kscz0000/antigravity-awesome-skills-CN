---
title: "虚拟键盘 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards

# 虚拟键盘

在没有物理键盘的设备上，系统提供多种虚拟键盘供用户输入数据。

![一个风格化的数字键盘示意图，展示在网格上方，暗示设计工具的画布。图片以红色调着色，微妙地呼应了 Apple 经典六色标志中的红色。](https://docs-assets.developer.apple.com/published/d5cea0a3ccb2af2881ade732675a1064/components-virtual-keyboard-intro%402x.png)

虚拟键盘可以提供针对当前任务优化的特定按键集；例如，支持输入电子邮件地址的键盘可以包含 "@" 字符和句号，甚至 ".com"。虚拟键盘不支持键盘快捷键。

在应用中合适的情况下，你可以用自定义视图替换系统键盘，以支持应用特有的数据输入。在 iOS、iPadOS 和 tvOS 上，你还可以创建一个应用扩展，提供用户可安装的自定义键盘来替代标准键盘。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Best-practices)

**选择与用户正在编辑的内容类型匹配的键盘。** 例如，你可以通过提供数字和标点符号键盘来帮助用户输入数字数据。当你为文本输入区域指定语义含义时，系统可以自动提供与预期输入类型匹配的键盘，并可能利用此信息来优化键盘纠错建议。开发者指南请参阅 [`keyboardType(_:)`](https://developer.apple.com/documentation/SwiftUI/View/keyboardType\(_:\))（SwiftUI）、[`textContentType(_:)`](https://developer.apple.com/documentation/SwiftUI/View/textContentType\(_:\))（SwiftUI）、[`UIKeyboardType`](https://developer.apple.com/documentation/UIKit/UIKeyboardType)（UIKit）和 [`UITextContentType`](https://developer.apple.com/documentation/UIKit/UITextContentType)（UIKit）。

  * ASCII capable
  * ASCII capable number pad
  * Decimal pad
  * Default
  * Email address
  * Name phone pad
  * Number pad
  * Numbers and punctuation
  * Phone pad
  * Twitter
  * URL
  * Web search



![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格和回车键。键盘上方显示输入建议，下方显示听写按钮。](https://docs-assets.developer.apple.com/published/1aeba403a2942689ee8efbfed71a7943/virtual-keyboard-ascii-capable%402x.png)

![iPhone 上键盘的部分截图，显示全部 10 个数字键以及 Delete 键。2 到 9 的数字键各包含电话上对应的 3 或 4 个字母。](https://docs-assets.developer.apple.com/published/1da579d09964a9bd81a0823d52fa18e5/virtual-keyboard-ascii-capable-number-pad%402x.png)

![iPhone 上键盘的部分截图，显示全部 10 个数字键以及 Delete 和句号键。2 到 9 的数字键各包含电话上对应的 3 或 4 个字母。](https://docs-assets.developer.apple.com/published/4b43048f8d2f13d8322b95266bc4c4f3/virtual-keyboard-decimal-pad%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格和回车键。键盘上方显示输入建议，下方显示 Emoji 和听写按钮。](https://docs-assets.developer.apple.com/published/34447cdc5d5eb61f1734a046f3d108c6/virtual-keyboard-default%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格、句号、@ 符号和回车键。键盘上方显示输入建议，下方显示 Emoji 按钮。](https://docs-assets.developer.apple.com/published/e7dcd10c36065774ac8cadf76b09d8e4/virtual-keyboard-email-address%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格和回车键。键盘上方显示输入建议，下方显示 Emoji 和听写按钮。](https://docs-assets.developer.apple.com/published/3228cd2d2cd6d36e3db1aff1d50ad903/virtual-keyboard-name-phone-pad%402x.png)

![iPhone 上键盘的部分截图，显示全部 10 个数字键以及 Delete 键。2 到 9 的数字键各包含电话上对应的 3 或 4 个字母。](https://docs-assets.developer.apple.com/published/679c33bdff61bc9e257982b7cffba264/virtual-keyboard-number-pad%402x.png)

![iPhone 上键盘的部分截图，显示 10 个数字键和 15 个标点符号键，以及二级标点符号键和 Delete、字母切换、空格和回车键。键盘上方显示输入建议，下方显示听写按钮。](https://docs-assets.developer.apple.com/published/916933140730b2db67f8004991c558aa/virtual-keyboard-numbers-and-punctuation%402x.png)

![iPhone 上键盘的部分截图，显示全部 10 个数字键以及 Delete 键和一个加号、星号、井号键。2 到 9 的数字键各包含电话上对应的 3 或 4 个字母。](https://docs-assets.developer.apple.com/published/b1b427eb7252b94e7b9d0095ccd04f56/virtual-keyboard-phone-pad%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格、@ 符号和井号键。键盘上方显示输入建议，下方显示 Emoji 和听写按钮。](https://docs-assets.developer.apple.com/published/21b1b12df6335045a6f29efc8cbdb5a1/virtual-keyboard-twitter%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、句号、斜杠、.com 和回车键。键盘上方显示输入建议，下方显示 Emoji 按钮。](https://docs-assets.developer.apple.com/published/daec1d80ab39aff3f52effb615f84425/virtual-keyboard-url%402x.png)

![iPhone 上键盘的部分截图，显示全部 26 个字母键以及 Shift、Delete、数字切换、空格、句号和前往键。键盘上方显示输入建议，下方显示 Emoji 和听写按钮。](https://docs-assets.developer.apple.com/published/0618532f75b91e3f3be2416a363d4a43/virtual-keyboard-web-search%402x.png)

**如果有助于明确文本输入体验，可考虑自定义回车键类型。** 回车键类型基于所选的键盘类型，但在应用中有需要时可以更改。例如，如果你的应用会发起搜索，可以使用搜索类型的回车键而非标准回车键，使体验与其他搜索入口保持一致。开发者指南请参阅 [`submitLabel(_:)`](https://developer.apple.com/documentation/SwiftUI/View/submitLabel\(_:\))（SwiftUI）和 [`UIReturnKeyType`](https://developer.apple.com/documentation/UIKit/UIReturnKeyType)（UIKit）。

## [自定义输入视图](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Custom-input-views)

在某些情况下，你可以创建_输入视图_来提供增强应用数据输入任务的自定义功能。例如，Numbers 在编辑电子表格时提供了用于输入数值的自定义输入视图。自定义输入视图会在用户处于你的应用中时替换系统键盘。开发者指南请参阅 [`ToolbarItemPlacement`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement)（SwiftUI）和 [`inputViewController`](https://developer.apple.com/documentation/UIKit/UIResponder/inputViewController)（UIKit）。

**确保自定义输入视图在应用上下文中合理。** 除了让数据输入简单直观之外，你还应该让用户理解使用自定义输入视图的好处。否则，他们可能会困惑为什么在你的应用中无法恢复系统键盘。

**在用户输入时播放标准键盘音效。** 键盘音效在用户点击系统键盘按键时提供熟悉的反馈，因此他们很可能期望在自定义输入视图中点击按键时也能听到相同的声音。用户可以在"设置 > 声音与触感"中关闭所有键盘交互的键盘音效。开发者指南请参阅 [`playInputClick()`](https://developer.apple.com/documentation/UIKit/UIDevice/playInputClick\(\))（UIKit）。

## [自定义键盘](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Custom-keyboards)

在 iOS、iPadOS 和 tvOS 上，你可以通过创建应用扩展来提供替代系统键盘的自定义键盘。_应用扩展_是用户可安装的代码，用于扩展系统特定区域的功能；详情请参阅[应用扩展](https://developer.apple.com/app-extensions/)。

用户在"设置"中选择你的自定义键盘后，可以在任何应用中使用它进行文本输入，但编辑安全文本字段和电话号码字段时除外。用户可以选择多个自定义键盘并随时切换。开发者指南请参阅[创建自定义键盘](https://developer.apple.com/documentation/UIKit/creating-a-custom-keyboard)。

当你想在系统范围内提供独特的键盘功能时，自定义键盘才有意义，例如新颖的文字输入方式或系统不支持的语言输入能力。如果你只想在用户使用你的应用时提供自定义键盘，请考虑改为创建自定义输入视图。

**提供明显且便捷的键盘切换方式。** 用户知道标准键盘上的 Globe 键——在有多个键盘时会替代专用的 Emoji 键——可以快速切换到其他键盘，他们期望在你的键盘中也有同样直观的体验。

**避免重复系统键盘的功能。** 在某些设备上，Emoji/Globe 键和听写键会自动显示在键盘下方，即使用户正在使用自定义键盘。你的应用无法影响这些按键，如果在你的键盘中重复它们，很可能会造成混淆。

**考虑在应用中提供键盘教程。** 用户习惯了标准键盘，学习使用新键盘可能需要时间。你可以在应用中提供使用说明来帮助简化这个过程——例如，告诉用户如何选择你的键盘、在文本输入时激活它、使用它以及切换回标准键盘。避免在键盘本身内显示帮助内容。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Platform-considerations)

 _macOS 不支持。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#iOS-iPadOS)

**使用键盘布局参考线，让键盘感觉像是界面的有机组成部分。** 使用布局参考线还有助于在虚拟键盘显示在屏幕上时保持界面重要部分的可见性。开发者指南请参阅[使用键盘布局参考线调整布局](https://developer.apple.com/documentation/UIKit/adjusting-your-layout-with-keyboard-layout-guide)。

![iPhone 上的应用布局示意图，显示键盘上方有两个堆叠的文本字段和一个按钮。](https://docs-assets.developer.apple.com/published/2d310619deb1ce3587596b7fee6e5b08/ui-fully-visible%402x.png)

![圆圈中的对勾，表示正确示例。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)键盘布局参考线有助于确保应用界面和键盘协调配合。

![iPhone 上的应用布局示意图，显示两个堆叠的文本字段。键盘遮挡了底部文本字段的一部分。](https://docs-assets.developer.apple.com/published/b2612a1b69632d398d2744caee9ff1e2/text-field-hidden%402x.png)

![圆圈中的叉号，表示错误示例。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)没有布局参考线，键盘可能会使文本输入更加困难。

![iPhone 上的应用布局示意图，显示键盘上方有两个堆叠的文本字段和一个按钮。键盘遮挡了按钮的一部分。](https://docs-assets.developer.apple.com/published/3a2b1c460427926e69f4d3e8d1383aef/button-hidden%402x.png)

![圆圈中的叉号，表示错误示例。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)没有布局参考线，键盘可能会使点击按钮更加困难。

**谨慎地将自定义控件放置在键盘上方。** 一些应用会在键盘上方放置包含自定义控件的输入附件视图，以提供与用户当前数据相关的应用特有功能。例如，Numbers 会显示帮助用户对电子表格数据应用标准或自定义计算的控件。如果你的应用提供了增强键盘功能的自定义控件，请确保它们与当前任务相关。如果你的应用中的其他视图使用了 Liquid Glass，或者你的视图在键盘上方看起来不协调，请对包含控件的视图应用 Liquid Glass 以保持一致性。如果你使用标准工具栏来包含控件，它会自动采用 Liquid Glass。使用键盘布局参考线和标准间距来确保系统按预期在视图中定位你的控件。开发者指南请参阅 [`ToolbarItemPlacement`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement)（SwiftUI）、[`inputAccessoryView`](https://developer.apple.com/documentation/UIKit/UIResponder/inputAccessoryView)（UIKit）和 [`UIKeyboardLayoutGuide`](https://developer.apple.com/documentation/UIKit/UIKeyboardLayoutGuide)（UIKit）。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#tvOS)

当用户使用 Siri 遥控器选择文本字段时，tvOS 会显示一个线性虚拟键盘。

注意

当用户使用 Siri 遥控器以外的设备时，会显示网格键盘界面，内容布局会自动适配键盘。

当用户激活数字输入视图时，tvOS 会显示专用于数字的键盘。详情请参阅[数字输入视图](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#visionOS)

在 visionOS 中，系统提供的虚拟键盘支持直接和间接手势操作，并出现在一个独立的窗口中，用户可以将其移动到任意位置。你无需在布局中考虑键盘的位置。

带自定义控件的视频。

内容描述：一段在 visionOS 中使用虚拟键盘打字的录屏演示。

播放

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#watchOS)

在 Apple Watch 上，如果设备屏幕足够大，文本字段可以显示键盘。否则，系统允许用户使用听写或涂文字输入信息。你无法在 watchOS 中更改键盘类型，但可以设置文本字段的内容类型。系统会利用此信息来简化文本输入，例如提供建议。开发者指南请参阅 [`textContentType(_:)`](https://developer.apple.com/documentation/SwiftUI/View/textContentType\(_:\))（SwiftUI）。

用户还可以使用附近配对的 iPhone 在 Apple Watch 上输入文本。

## [资源](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Related)

[输入数据](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[键盘](https://developer.apple.com/design/human-interface-guidelines/keyboards)

[布局](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Developer-documentation)

[`keyboardType(_:)`](https://developer.apple.com/documentation/SwiftUI/View/keyboardType\(_:\)) — SwiftUI

[`textContentType(_:)`](https://developer.apple.com/documentation/SwiftUI/View/textContentType\(_:\)) — SwiftUI

[`UIKeyboardType`](https://developer.apple.com/documentation/UIKit/UIKeyboardType) — UIKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Change-log)

日期| 变更内容
---|---
2025 年 6 月 9 日| 新增了在键盘上方显示自定义控件的指南，并更新以反映 watchOS 中虚拟键盘的支持情况。
2024 年 2 月 2 日| 明确了 visionOS 中虚拟键盘对直接和间接手势的支持。
2023 年 12 月 5 日| 新增了 visionOS 的美术资源。
2023 年 6 月 21 日| 页面标题从"屏幕键盘"更改为"虚拟键盘"，并更新以包含 visionOS 的指南。
