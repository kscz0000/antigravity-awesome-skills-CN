---
title: "Token fields | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/token-fields

# 令牌字段

令牌字段是一种特定类型的文本字段，包含令牌，令牌是代表离散数据片段（如联系人或日期）的圆角矩形。

![令牌字段的风格化表示，显示两个令牌。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/9e1f4c3f4a2d3b5c7d9e1f4c3f4a2d3b/components-token-field-intro%402x.png)

令牌字段让用户能够高效地选择和修改一组令牌。例如，邮件使用令牌字段让用户将多个收件人添加到邮件中。用户可以在字段中输入文本，或从列表中选择项目。当用户选择项目时，系统将其转换为令牌。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/token-fields#Best-practices)

**使用令牌字段收集离散数据片段。** 令牌字段非常适合收集可以表示为不同项目的数据，如联系人、日期或标签。如果需要收集自由格式文本，请改用[文本字段](https://developer.apple.com/design/human-interface-guidelines/text-fields)或[文本视图](https://developer.apple.com/design/human-interface-guidelines/text-views)。

**提供自动补全建议以帮助用户输入数据。** 当用户在令牌字段中输入文本时，显示匹配建议列表以帮助他们快速找到并选择所需项目。例如，邮件在用户输入时显示匹配联系人列表。

**允许用户删除令牌。** 用户应该能够通过按删除键或点击令牌上的删除按钮来删除单个令牌。

**考虑在令牌字段下方显示已选项目的列表。** 如果令牌字段可以包含许多令牌，考虑在字段下方显示已选项目的列表以帮助用户查看他们选择了什么。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/token-fields#Platform-considerations)

_iOS、iPadOS、tvOS、visionOS 或 watchOS 不支持。_

### [macOS](https://developer.apple.com/design/human-interface-guidelines/token-fields#macOS)

**使用令牌字段收集联系人、收件人或标签。** 令牌字段非常适合这些用例，因为它们让用户能够快速选择多个项目并轻松查看已选择的内容。

**提供自动补全建议。** 当用户在令牌字段中输入文本时，显示匹配建议列表以帮助他们快速找到并选择所需项目。

**允许用户拖放令牌。** 用户应该能够将项目拖到令牌字段中以创建新令牌。

**支持键盘导航。** 用户应该能够使用箭头键在令牌之间导航，并使用删除键删除令牌。

## [资源](https://developer.apple.com/design/human-interface-guidelines/token-fields#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/token-fields#Related)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/token-fields#Developer-documentation)

[`NSTokenField`](https://developer.apple.com/documentation/AppKit/NSTokenField) — AppKit
