---
title: "Text fields | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/text-fields

# 文本字段

文本字段是一个矩形区域，用户在其中输入或编辑小段特定文本。

![包含值的文本字段的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/d23fbf0321063ee6b988a1528ad48ef5/components-text-field-intro%402x.png)

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices)

**使用文本字段请求少量信息，如姓名或邮箱地址。** 要让用户输入大量文本，请改用[文本视图](https://developer.apple.com/design/human-interface-guidelines/text-views)。

**在文本字段中显示提示以帮助传达其用途。** 文本字段可以包含占位符文本——如"邮箱"或"密码"——当字段中没有其他文本时。由于占位符文本在用户开始输入时消失，包含单独描述字段的标签以提醒用户其用途也很有用。

**使用安全文本字段隐藏私密数据。** 当应用请求敏感数据（如密码）时，始终使用安全文本字段。有关开发者指导，请参阅 [`SecureField`](https://developer.apple.com/documentation/SwiftUI/SecureField)。

**尽可能将文本字段的大小与预期文本量匹配。** 文本字段的大小帮助用户直观估计要提供的信息量。

**均匀间隔多个文本字段。** 如果布局包含多个文本字段，在它们之间留出足够空间，以便用户可以轻松看到哪个输入字段与每个介绍性标签配对。尽可能垂直堆叠多个文本字段，并使用一致的宽度创建更有组织的布局。例如，地址表单上的名字和姓氏字段可能是一种宽度，而地址和城市字段可能是不同的宽度。

**确保在多个字段之间跳格按用户期望的方式流动。** 在字段之间跳格时，以逻辑顺序移动焦点。系统尝试自动实现此结果，因此您不需要经常自定义此设置。

**在有意义时验证字段。** 例如，如果字段唯一合法的值是一串数字，如果用户输入了数字以外的字符，您的应用需要提醒用户。检查数据的适当时间取决于上下文：输入邮箱地址时，最好在用户切换到另一个字段时验证；创建用户名或密码时，验证需要在用户切换到另一个字段之前发生。

**使用数字格式化器帮助处理数字数据。** 数字格式化器自动配置文本字段仅接受数字值。它还可以以特定方式显示值，如具有特定位数的小数、百分比或货币。但是，不要假设数据的实际呈现，因为格式化可能因用户的区域设置而显著变化。

![两个堆叠文本字段的部分截图。顶部字段包含带有四位小数的数字。底部字段包含货币值。](https://docs-assets.developer.apple.com/published/4c7bdd958dfd5ae5c0eb2103f511c984/text-fields-formatted-text%402x.png)格式化文本

**根据字段的需要调整换行。** 默认情况下，系统裁剪任何超出文本字段边界的文本。或者，您可以将文本字段设置为在字符或单词级别换行到新行，或在开头、中间或结尾截断（用省略号表示）。

![包含在结束前被截断的句子的文本字段的部分截图。](https://docs-assets.developer.apple.com/published/4f5087014620cf61ae6e6cf691766376/text-fields-clipped-text%402x.png)裁剪文本

![包含换行到两行的句子的文本字段的部分截图。](https://docs-assets.developer.apple.com/published/5e7b94570af0f50c9e9a3061a428aa15/text-fields-wrapped-text%402x.png)换行文本

![包含用省略号代替最后几个单词的句子的文本字段的部分截图。](https://docs-assets.developer.apple.com/published/ad0040baa8369af2dbd9ab88a25c3439/text-fields-truncated-text%402x.png)截断文本

**考虑使用扩展工具提示显示裁剪或截断文本的完整版本。** 扩展工具提示的行为类似常规[工具提示](https://developer.apple.com/design/human-interface-guidelines/offering-help#macOS-visionOS)，当用户将指针放在字段上时出现。

**在 iOS、iPadOS、tvOS 和 visionOS 应用中，显示适当的键盘类型。** 有多种不同的键盘类型可用，每种都设计用于促进不同类型的输入，如数字或 URL。为了简化数据输入，显示适合用户正在输入的内容类型的键盘。有关指导，请参阅[虚拟键盘](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)。

**在 tvOS 和 watchOS 应用中最小化文本输入。** 在 Apple TV 和 Apple Watch 上输入长段文本或填写大量文本字段很耗时。最小化文本输入并考虑更高效地收集信息，如使用按钮。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/text-fields#Platform-considerations)

_tvOS 或 visionOS 无额外注意事项。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#iOS-iPadOS)

**在文本字段后端显示清除按钮以帮助用户擦除输入。** 当此元素存在时，用户可以点击它来清除文本字段的内容，而无需持续点击删除键。

**使用图像和按钮在文本字段中提供清晰度和功能。** 您可以在文本字段的两端显示自定义图像，或添加系统提供的按钮，如书签按钮。通常，使用文本字段的前端指示字段的用途，使用后端提供额外功能，如书签。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#macOS)

**如果需要将文本输入与选择列表配对，请考虑使用组合框。** 有关相关指导，请参阅[组合框](https://developer.apple.com/design/human-interface-guidelines/combo-boxes)。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#watchOS)

**仅在必要时显示文本字段。** 尽可能优先显示选项列表而非要求文本输入。

## [资源](https://developer.apple.com/design/human-interface-guidelines/text-fields#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/text-fields#Related)

[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

[Combo boxes](https://developer.apple.com/design/human-interface-guidelines/combo-boxes)

[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/text-fields#Developer-documentation)

[`TextField`](https://developer.apple.com/documentation/SwiftUI/TextField) — SwiftUI

[`SecureField`](https://developer.apple.com/documentation/SwiftUI/SecureField) — SwiftUI

[`UITextField`](https://developer.apple.com/documentation/UIKit/UITextField) — UIKit

[`NSTextField`](https://developer.apple.com/documentation/AppKit/NSTextField) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/text-fields#Change-log)

日期| 变更  
---|---  
2023年6月5日| 更新指导以反映 watchOS 10 的变化。  
