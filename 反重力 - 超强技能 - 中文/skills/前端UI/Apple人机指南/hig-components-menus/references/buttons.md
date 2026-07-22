---
title: "Buttons | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/buttons

# 按钮

按钮用于触发即时操作。

![两个水平排列按钮的风格化示意图。图片以红色调呈现，微妙呼应了早期六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/15781cd4e57f0e78b7a388a3fa009fa8/components-buttons-intro%402x.png)

按钮用途广泛且高度可定制，为用户提供了简单、熟悉的方式来完成应用中的操作。通常，按钮通过三个属性来清晰传达其功能：

  * **样式。** 基于尺寸、颜色和形状的视觉样式。

  * **内容。** 按钮为传达其用途而显示的符号（或图标）、文本标签，或两者兼有。

  * **角色。** 系统定义的角色，用于标识按钮的语义含义，并可影响其外观。




还有许多类按钮组件，针对特定场景具有独特的外观和行为，例如[切换开关](https://developer.apple.com/design/human-interface-guidelines/toggles)、[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)和[分段控件](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)

当按钮易于识别且易于理解时，应用往往会让人感觉直观且设计精良。

**确保按钮易于使用。** 按钮周围必须留出足够空间，以便用户在视觉上将其与周围的组件和内容区分开来。足够的空间对于帮助用户选择或激活按钮也至关重要，无论他们使用何种输入方式。一般规则是，按钮至少需要 44x44 pt 的点击区域——在 visionOS 中为 60x60 pt——以确保用户可以轻松选中，无论是用手指、指针、视线还是遥控器。

**始终为自定义按钮提供按下状态。** 没有按下状态的按钮会让人感觉没有响应，使用户怀疑按钮是否正在接受输入。

## [样式](https://developer.apple.com/design/human-interface-guidelines/buttons#Style)

系统按钮提供多种样式，支持自定义的同时内置了交互状态、无障碍支持和外观适配。不同平台定义了不同的样式，帮助你在应用中传达操作的层级关系。

**通常，对视图中最可能的操作使用醒目的按钮样式。** 要将用户注意力引导到特定按钮，请使用醒目按钮样式，以便系统为按钮背景应用强调色。使用颜色的按钮往往在视觉上最为突出，帮助用户快速识别他们最可能使用的操作。每个视图中的醒目按钮应控制在一到两个。过多的醒目按钮会增加认知负担，使用户在做出选择前需要花更多时间评估选项。

**使用样式——而非尺寸——在多个选项中区分首选项。** 当你使用相同尺寸的按钮提供两个或多个选项时，意味着这些选项构成了一组连贯的选择。相反，将两个不同尺寸的按钮放在一起会使界面显得混乱且不一致。如果要突出一组中的首选或最可能的选项，请为该选项使用更醒目的按钮样式，其余选项使用不太醒目的样式。

**避免为按钮标签和内容层背景使用相近的颜色。** 如果应用的内容层已有明亮、多彩的内容，请优先使用按钮标签的默认单色外观。更多指导，请参阅 [Liquid Glass 颜色](https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color)。

## [内容](https://developer.apple.com/design/human-interface-guidelines/buttons#Content)

**确保每个按钮都能清晰传达其用途。** 根据平台不同，按钮可以包含符号（或图标）、文本标签或两者兼有，以帮助用户理解其功能。

注意

在 macOS 和 visionOS 中，当用户将鼠标悬停在按钮上片刻后，系统会显示工具提示。工具提示显示简短的文字说明按钮的功能；相关指导请参阅[提供帮助](https://developer.apple.com/design/human-interface-guidelines/offering-help)。

**尽量将熟悉的操作与熟悉的图标关联。** 例如，用户可以预见包含 `square.and.arrow.up` 符号的按钮将帮助他们执行与分享相关的操作。如果在按钮中使用图标是合理的，可以考虑使用现有或自定义的[符号](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)。代表常见操作的符号列表，请参阅[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。

**当简短标签比图标传达得更清晰时，考虑使用文本。** 使用文本时，用几个词简洁描述按钮的功能。使用[标题式大写](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64)，考虑以动词开头来帮助传达按钮的操作——例如，让用户将商品添加到购物车的按钮可以使用"添加到购物车"标签。

## [角色](https://developer.apple.com/design/human-interface-guidelines/buttons#Role)

系统按钮可以具有以下角色之一：

  * **普通。** 无特定含义。

  * **主要。** 该按钮是默认按钮——用户最可能选择的按钮。

  * **取消。** 该按钮取消当前操作。

  * **破坏性。** 该按钮执行可能导致数据销毁的操作。




按钮的角色可能对其外观产生额外影响。例如，主要按钮使用应用的强调色，而破坏性按钮使用系统红色。

![一个包含三个系统按钮的示例警报，分别标记为主要、破坏性和取消。主要按钮使用蓝色强调色，破坏性按钮使用系统红色文本，取消按钮显示为标准按钮。](https://docs-assets.developer.apple.com/published/ffa011d457181b94f56257d7d59f71aa/buttons-roles-alert%402x.png)

**将主要角色分配给用户最可能选择的按钮。** 当主要按钮响应 Return 键时，用户可以快速确认选择。此外，当按钮位于临时视图中——如[工作表](https://developer.apple.com/design/human-interface-guidelines/sheets)、可编辑视图或[警报](https://developer.apple.com/design/human-interface-guidelines/alerts)——分配主要角色意味着用户按 Return 键时视图可以自动关闭。

**不要将主要角色分配给执行破坏性操作的按钮，即使该操作是最可能的选择。** 由于主要按钮的视觉突出性，用户有时会不加阅读就直接点击。通过将主要角色分配给非破坏性按钮来帮助用户避免丢失内容。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/buttons#Platform-considerations)

 _tvOS 无额外考量。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS)

**配置按钮在需要为非即时完成的操作提供反馈时显示活动指示器。** 在按钮内显示活动指示器可以节省界面空间，同时清晰传达延迟原因。为帮助说明正在发生的情况，还可以配置按钮在活动指示器旁显示不同的标签。例如，"结账"标签可以在活动指示器可见时变为"正在结账…"。当用户点击或轻点你配置的按钮后出现延迟时，系统会在原始或替代标签旁显示活动指示器，隐藏按钮图像（如果有）。

![标记为"结账"的按钮示意图。](https://docs-assets.developer.apple.com/published/f7a2f53cdd4755b1121c34f1df0e94ae/button-activity-indicator-hidden%402x.png)

![标记为"正在结账"的按钮示意图，标签前方有一个活动指示器。](https://docs-assets.developer.apple.com/published/f2d6023f16eed80487f72b630903d220/button-activity-indicator-visible%402x.png)

### [macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#macOS)

macOS 有几种独有的特定按钮类型。

#### [推送按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Push-buttons)

macOS 中的标准按钮类型称为_推送按钮_。你可以配置推送按钮来显示文本、符号、图标或图像，或文本与图像内容的组合。推送按钮可以作为视图中的默认按钮，并且可以着色。

**仅在需要显示较高或可变高度内容时使用弹性高度推送按钮。** 弹性高度按钮支持与普通推送按钮相同的配置——使用相同的圆角半径和内容内边距——因此与界面中的其他按钮保持一致。如果需要展示包含两行文本或高图标的按钮，请使用弹性高度按钮；否则使用标准推送按钮。开发者指南请参阅 [`NSButton.BezelStyle.flexiblePush`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/flexiblePush)。

**当推送按钮打开另一个窗口、视图或应用时，在标题末尾添加省略号。** 在整个系统中，控件标题中的省略号表示用户可以提供额外输入。例如，Safari 设置中自动填充面板的编辑按钮包含省略号，因为它们会打开其他视图让用户修改自动填充值。

**考虑支持弹簧加载。** 在配备妙控板的系统上，_弹簧加载_允许用户通过将选中的项目拖到按钮上并用力按下（即更用力地按压）来激活按钮，而无需放下选中的项目。用力按下后，用户可以继续拖动项目，可能执行额外操作。

#### [方形按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Square-buttons)

_方形按钮_（也称为_渐变按钮_）用于触发与视图相关的操作，如在表格中添加或删除行。

方形按钮包含符号或图标——不含文本——你可以将其配置为推送按钮、切换开关或弹出按钮的行为。方形按钮出现在其关联视图附近——通常在其内部或下方——以便用户知道按钮影响哪个视图。

**在视图中使用方形按钮，而非窗口框架中。** 方形按钮不适用于工具栏或状态栏。如果需要在[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)中放置按钮，请使用工具栏项。

**优先在方形按钮中使用符号。** [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 提供了丰富的符号，这些符号在默认状态下会自动获得适当的颜色，并在响应用户交互时相应变化。

**避免使用标签来介绍方形按钮。** 因为方形按钮与特定视图紧密关联，其用途通常无需描述性文字就已清晰。

开发者指南请参阅 [`NSButton.BezelStyle.smallSquare`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/smallSquare)。

#### [帮助按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Help-buttons)

_帮助按钮_出现在视图内，用于打开应用特定的帮助文档。

帮助按钮是圆形、尺寸统一的按钮，包含一个问号。创建帮助文档的指导，请参阅[提供帮助](https://developer.apple.com/design/human-interface-guidelines/offering-help)。

**使用系统提供的帮助按钮来显示帮助文档。** 用户熟悉标准帮助按钮的外观，知道点击它会打开帮助内容。

**在可能的情况下，打开与当前上下文相关的帮助主题。** 例如，邮件设置中规则面板的帮助按钮会打开邮件用户指南中解释如何更改这些设置的帮助主题。如果没有特定帮助主题直接适用于当前上下文，请在用户选择帮助按钮时打开应用帮助文档的顶层。

**每个窗口中最多包含一个帮助按钮。** 同一上下文中的多个帮助按钮会使用户难以预测点击其中一个的结果。

**将帮助按钮放在用户期望找到的位置。** 以下位置可供参考。

视图样式 | 帮助按钮位置
---|---
带有确认按钮的对话框（如"好"和"取消"） | 底部角落，与确认按钮相对且与其垂直对齐
没有确认按钮的对话框 | 左下角或右下角
设置窗口或面板 | 左下角或右下角

**在视图中使用帮助按钮，而非窗口框架中。** 例如，避免将帮助按钮放在工具栏或状态栏中。

**避免显示介绍帮助按钮的文字。** 用户知道帮助按钮的功能，因此不需要额外的描述性文字。

#### [图像按钮](https://developer.apple.com/design/human-interface-guidelines/buttons#Image-buttons)

_图像按钮_出现在视图中，显示图像、符号或图标。你可以将其配置为推送按钮、切换开关或弹出按钮的行为。

**在视图中使用图像按钮，而非窗口框架中。** 例如，避免将图像按钮放在工具栏或状态栏中。如果需要在工具栏中使用图像作为按钮，请使用工具栏项。参见[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)。

**在图像边缘和按钮边缘之间保留约 10 像素的内边距。** 图像按钮的边缘定义了其可点击区域，即使边缘不可见也是如此。保留内边距可确保即使点击位置不在图像精确范围内也能正确响应。一般情况下，避免在图像按钮中包含系统提供的边框；开发者指南请参阅 [`isBordered`](https://developer.apple.com/documentation/AppKit/NSButton/isBordered)。

**如需包含标签，请将其放在图像按钮下方。** 相关指导请参阅[标签](https://developer.apple.com/design/human-interface-guidelines/labels)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS)

visionOS 按钮通常包含可见的背景以帮助用户发现，并在用户交互时播放声音提供反馈。

视频（含自定义控件）

内容描述：一段 visionOS 窗口顶部区域的录屏。窗口包含多个按钮，其中包括一个"更多"按钮，该按钮接收到悬停效果。按钮被选中，随后出现包含额外选项的菜单。

播放

visionOS 中有三种标准按钮形状。通常，仅图标的按钮使用 [`circle`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/circle) 形状，仅文本的按钮使用 [`roundedRectangle`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/roundedRectangle) 或 [`capsule`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/capsule) 形状，同时包含图标和文本的按钮使用胶囊形状。

visionOS 按钮使用不同的视觉样式来传达四种不同的交互状态。

![一个圆形按钮的图片，包含一个圆角矩形轮廓图标。按钮背景为深色，虚线轮廓为白色。](https://docs-assets.developer.apple.com/published/aed0b1c313448f088dd1ee24663db11e/visionos-button-state-idle%402x.png)空闲

![一个圆形按钮的图片，包含一个圆角矩形轮廓图标。按钮背景为中深色，轮廓为白色。](https://docs-assets.developer.apple.com/published/29d708fd7985184cbee9d90d7684da92/visionos-button-state-hover%402x.png)悬停

![一个圆形按钮的图片，包含一个圆角矩形轮廓图标。按钮背景为白色，轮廓为黑色。](https://docs-assets.developer.apple.com/published/0b94e710605235dfca19ef853499cf26/visionos-button-state-selected%402x.png)已选中

![一个圆形按钮的图片，包含一个圆角矩形轮廓图标。按钮背景非常深，轮廓为浅色。](https://docs-assets.developer.apple.com/published/737120252765e5427161af32bb17e7fb/visionos-button-state-unavailable%402x.png)不可用

注意

在 visionOS 中，按钮不支持自定义悬停效果。

除了上述四种状态外，当用户短暂注视按钮时，按钮还可以显示工具提示。通常，包含文本的按钮不需要显示工具提示，因为按钮的描述性标签已说明了其功能。

视频（含自定义控件）

内容描述：一段展示工具提示出现在 visionOS 按钮下方的动画。

播放

在 visionOS 中，按钮可以有以下尺寸。

形状 | Mini (28 pt) | Small (32 pt) | Regular (44 pt) | Large (52 pt) | Extra large (64 pt)
---|---|---|---|---|---
圆形 | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png)
胶囊（仅文本） | | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | 
胶囊（文本和图标） | | | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | 
圆角矩形 | | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | ![表示可用的勾选标记。](https://docs-assets.developer.apple.com/published/9c1e6292b0ff3ee8f9e10917ad97f3da/table-availability-checkmark%402x.png) | 

**优先使用具有可辨别的背景形状和填充的按钮。** 当按钮被包含在使用对比背景填充的形状中时，用户通常更容易看到它。例外情况是工具栏、上下文菜单、警报或[装饰元素](https://developer.apple.com/design/human-interface-guidelines/ornaments)中的按钮，这些较大组件的形状和材质使按钮已经足够清晰可见。以下指导可帮助你确保按钮在不同场景下都有良好的呈现：

  * 当按钮出现在玻璃材质的[窗口](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS)上方时，使用 [`thin`](https://developer.apple.com/documentation/SwiftUI/Material/thin) 材质作为按钮的背景。

  * 当按钮悬浮在空间中时，使用[玻璃材质](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS)作为其背景。




**避免创建使用白色背景填充和黑色文本或图标的自定义按钮。** 系统保留此视觉样式用于传达切换状态。

**通常，优先使用圆形或胶囊形按钮。** 视线倾向于被形状的角部吸引，使人难以持续注视形状的中心。按钮形状越圆润，用户越容易稳定地注视它。当需要单独显示一个按钮时，优先使用胶囊形按钮。

**在按钮周围留出足够空间，以便用户轻松注视。** 尽量使按钮中心之间的距离始终保持至少 60 pt。如果按钮尺寸为 60 pt 或更大，在其周围添加 4 pt 的内边距以防止悬停效果重叠。此外，通常最好避免在垂直堆叠或水平排列中显示 small 或 mini 按钮。

**如需在堆叠或排列中显示带文本标签的按钮，请选择合适的形状。** 具体而言，在垂直按钮堆叠中优先使用圆角矩形形状，在水平按钮排列中优先使用胶囊形状。

**使用标准控件以利用用户已熟悉的可听反馈声音。** 可听反馈在 visionOS 中尤为重要，因为系统不播放触觉反馈。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS)

watchOS 使用 [`capsule`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/capsule) 按钮形状显示所有内联按钮。当按钮与内容内联放置时，它会获得与背景形成对比的材质效果，以确保可读性。

![一张 Apple Watch 屏幕示意图，包含胶囊形的"主要"和"次要"按钮。](https://docs-assets.developer.apple.com/published/79565402ab107166de9aa0fe6eab4e6d/buttons-watch-full-width%402x.png)

**使用工具栏在角落放置按钮。** 系统会自动移动时间和标题以适应工具栏按钮。系统还会为工具栏按钮应用 [Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass) 外观，与下方内容形成清晰的视觉区分。

![一张示意图，展示了顶部前导和尾随角落的工具栏按钮，以及屏幕底部的三个工具栏按钮。](https://docs-assets.developer.apple.com/published/28835a2c6f34513eb0758beef1f6015d/buttons-watch-toolbar-corners%402x.png)

**对于应用中的主要操作，优先使用跨越屏幕宽度的按钮。** 全宽按钮看起来更好，也更容易点击。如果两个按钮必须共享同一水平空间，请为两者使用相同的高度，并使用图像或简短文本标题作为按钮内容。

**使用工具栏按钮提供对相关区域的导航或对视图内容的上下文操作。** 这些按钮提供对视图内容的额外信息或辅助操作的访问。

**对垂直堆叠的单行和双行文本按钮使用相同的高度。** 尽可能使用相同的按钮高度以保持视觉一致性。

## [资源](https://developer.apple.com/design/human-interface-guidelines/buttons#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/buttons#Related)

[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)

[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

[切换开关](https://developer.apple.com/design/human-interface-guidelines/toggles)

[分段控件](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)

[位置按钮](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/buttons#Developer-documentation)

[`Button`](https://developer.apple.com/documentation/SwiftUI/Button) — SwiftUI

[`UIButton`](https://developer.apple.com/documentation/UIKit/UIButton) — UIKit

[`NSButton`](https://developer.apple.com/documentation/AppKit/NSButton) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/buttons#Change-log)

日期 | 变更
---|---
2025年12月16日 | 更新了 Liquid Glass 相关指导。
2025年6月9日 | 更新了按钮样式和内容相关指导。
2024年2月2日 | 说明了 visionOS 按钮不支持自定义悬停效果。
2023年12月5日 | 澄清了 visionOS 按钮的一些术语和指导。
2023年6月21日 | 更新以包含 visionOS 相关指导。
2023年6月5日 | 更新了 watchOS 中使用按钮的指导。
