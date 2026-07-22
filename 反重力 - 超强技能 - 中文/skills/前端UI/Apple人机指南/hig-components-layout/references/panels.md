---
title: "Panels | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/panels

# 面板

在 macOS 应用中，面板通常浮动在其他打开的窗口上方，提供与活动窗口或当前选择相关的补充控件、选项或信息。

![浮动在窗口上方的面板的风格化表示。图像带有红色调以微妙反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/37f7c9e6dd4c635ccbae68b50200a74c/components-panel-intro%402x.png)

通常，面板的外观比应用的[主窗口](https://developer.apple.com/design/human-interface-guidelines/windows#macOS-window-states)更不显眼。当情况需要时，面板也可以使用深色半透明样式来支持平视显示器（或 HUD）体验。

当您的应用在其他平台上运行时，考虑使用模态视图呈现与当前任务或选择相关的补充内容。指南请参阅[模态](https://developer.apple.com/design/human-interface-guidelines/modality)。

## 最佳实践

**使用面板让人们快速访问与他们正在处理的内容相关的重要控件或信息。** 例如，您可能使用面板提供影响活动文档或窗口中所选项的控件或设置。

**考虑使用面板呈现检查器功能。** 检查器显示当前所选项的详情，当项目更改或人们选择新项目时自动更新其内容。相比之下，如果您需要呈现信息窗口——即使所选项目更改也始终保持相同内容——请使用常规窗口而非面板。根据应用的布局，您还可以考虑使用[分割视图](https://developer.apple.com/design/human-interface-guidelines/split-views)窗格呈现检查器。

**在面板中优先使用简单调整控件。** 尽可能避免包含需要输入文本或选择要操作的项目控件，因为这些操作可能需要多个步骤。相反，考虑使用滑块和步进器等控件，因为这些组件可以给人们更直接的控制。

**编写描述面板用途的简短标题。** 因为面板通常浮动在应用中其他打开的窗口上方，它需要标题栏以便人们将其定位到想要的位置。使用名词创建简短标题——或使用[标题式大写](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64)的名词短语——可以帮助人们在屏幕上识别面板。例如，macOS 提供熟悉的标题为"字体"和"颜色"的面板，许多应用使用标题"检查器"。

**适当地显示和隐藏面板。** 当您的应用变为活动时，将其所有打开的面板置于最前，无论面板打开时哪个窗口是活动的。当您的应用不活动时，隐藏其所有面板。

**避免在窗口菜单的文档列表中包含面板。** 在[窗口菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu)中包含显示或隐藏面板的命令是可以的，但面板不是文档或标准应用窗口，它们不属于窗口菜单的列表。

**通常，避免使面板的最小化按钮可用。** 人们通常不需要最小化面板，因为它仅在需要时显示，并在应用不活动时消失。

**在界面和帮助文档中通过标题引用面板。** 在菜单中，使用面板的标题而不包含术语面板：例如，"显示字体"、"显示颜色"和"显示检查器"。在帮助文档中，将"面板"作为不同类型的窗口引入可能会令人困惑，因此通常最好通过标题引用面板——或在增加清晰度时——在标题后附加窗口。例如，标题"检查器"通常提供足够的上下文独立存在，而使用"字体窗口"和"颜色窗口"而非仅"字体"和"颜色"可能更清晰。

## HUD 样式面板

HUD 样式面板的功能与标准面板相同，但其外观更暗且半透明。HUD 适用于呈现高度视觉内容或提供沉浸式体验的应用，如媒体编辑或全屏幻灯片。例如，QuickTime Player 使用 HUD 显示检查器信息而不遮挡太多内容。

![半透明 HUD 面板的截图，用于显示电影文件的检查器信息，包括文件名、格式、帧率、数据率和电影内容的帧大小。](https://docs-assets.developer.apple.com/published/f3fccb3f4ad6963af1310c8f98c5a0f7/hud-style-panel%402x.png)

**优先使用标准面板。** 当没有逻辑理由存在 HUD 时，人们可能会被 HUD 分散注意力或困惑。此外，HUD 可能与当前外观设置不匹配。通常，仅在以下情况使用 HUD：

  * 在呈现电影、照片或幻灯片的媒体导向应用中

  * 当标准面板会遮挡必要内容时

  * 当您不需要包含控件时——除了展示三角形，大多数系统提供的控件与 HUD 的外观不匹配。




**当应用切换模式时保持一种面板样式。** 例如，如果您在应用处于全屏模式时使用 HUD，当人们将应用退出全屏模式时，优先保持 HUD 样式。

**在 HUD 中节制使用颜色。** HUD 的深色外观中过多的颜色可能会分散注意力。通常，您只需要少量高对比度颜色来突出 HUD 中的重要信息。

**保持 HUD 较小。** HUD 设计为不引人注目地有用，因此让它们变得太大会违背其主要目的。不要让 HUD 遮挡它调整的内容，并确保它不会与内容争夺人们的注意力。

开发者指南请参阅 [`hudWindow`](https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow)。

## 平台注意事项

iOS、iPadOS、tvOS、visionOS 和 watchOS 不支持。

## 资源

#### 相关

[Windows](https://developer.apple.com/design/human-interface-guidelines/windows)

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

#### 开发者文档

[`NSPanel`](https://developer.apple.com/documentation/AppKit/NSPanel) — AppKit

[`hudWindow`](https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow) — AppKit
