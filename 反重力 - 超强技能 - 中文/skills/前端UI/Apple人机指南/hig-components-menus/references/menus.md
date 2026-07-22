---
title: "Menus | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/menus

# 菜单

菜单在用户与其交互时显示选项，是在应用或游戏中呈现命令的空间高效方式。

![菜单的样式化呈现，包含选中项并显示子菜单。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/a64b5649dc039710622ba211979e116b/components-menus-intro%402x.png)

菜单在应用和游戏中无处不在，因此大多数人已经知道如何使用它们。无论您使用系统提供的组件还是自定义组件，用户都期望菜单以熟悉的方式运作。例如，用户理解打开菜单会显示一个或多个_菜单项_，每个菜单项代表影响当前选择或上下文的命令、选项或状态。标签和组织菜单项的指导适用于所有体验中的所有类型的菜单。

注意

多个系统提供的组件也包含支持特定用例的菜单。例如，[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)或[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)可以直接显示与其操作直接相关的选项菜单；[上下文菜单](https://developer.apple.com/design/human-interface-guidelines/context-menus)让用户访问与其当前视图或任务相关的少量常用操作；在 macOS 和 iPadOS 中，[菜单栏](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)菜单包含用户可以在应用或游戏中执行的所有命令。

## [标签](https://developer.apple.com/design/human-interface-guidelines/menus#Labels)

菜单项的标签描述其功能，如果有助于阐明含义，可以包含符号。在应用中，菜单项还可以显示关联的键盘命令（如果有）；在游戏中，菜单项很少显示键盘命令，因为游戏通常需要处理来自更广泛设备的输入，并可能为各种按键提供游戏特定的映射。

注意

根据菜单布局，iOS、iPadOS 或 visionOS 应用可以显示一些仅使用符号或图标来标识的无标签菜单项。有关指导，请参阅 [visionOS](https://developer.apple.com/design/human-interface-guidelines/menus#visionOS) 和 [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/menus#iOS-iPadOS)。

**为每个菜单项编写清晰简洁的标签。** 通常，使用描述操作的动词或动词短语标记启动操作的菜单项，如"查看"、"关闭"或"选择"。有关标记显示和隐藏界面内容或显示某事物当前选择状态的菜单项的指导，请参阅[切换项](https://developer.apple.com/design/human-interface-guidelines/menus#Toggled-items)。与您编写的所有文案一样，让您的应用或游戏的沟通风格指导您创建的菜单项标签的语气。

**为与平台体验保持一致，使用标题式大写。** 虽然游戏可能有不同的写作风格，但通常首选使用标题式大写，即将除冠词、并列连词和短介词外的每个单词大写，并大写标签中的最后一个单词，无论词性如何。有关英语中此大写样式的完整指导，请参阅[标题式大写](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64)。

**从菜单项标签中删除冠词（如 a、an 和 the）以节省空间。** 在英语中，冠词总是使标签变长，但很少增强理解。例如，将菜单项标签从"View Settings"更改为"View the Settings"不会提供额外的说明。

**在菜单项不可用时向用户显示。** 不可用的菜单项通常显示为变暗且不响应交互。如果菜单的所有项目都不可用，菜单本身需要保持可用，以便用户可以打开它并了解其包含的命令。

**当操作在完成前需要更多信息时，在菜单项标签后附加省略号。** 省略号字符（…）表示用户需要输入信息或做出额外选择，通常在另一个视图中。

## [图标](https://developer.apple.com/design/human-interface-guidelines/menus#Icons)

**用熟悉的图标表示菜单项操作。** 图标帮助用户在整个应用中识别常见操作。使用与系统相同的图标来表示"复制"、"共享"和"删除"等操作，无论它们出现在哪里。有关表示常见操作的图标列表，请参阅[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。

**如果找不到清晰表示菜单项的图标，则不要显示图标。** 并非所有菜单项都需要图标。为自定义菜单项添加图标时要小心，以避免与其他现有操作混淆，不要仅为了装饰而添加图标。

![包含星期几的菜单图示。每个菜单项由不同的符号表示，与对应的日期无关。](https://docs-assets.developer.apple.com/published/e612c40d780feb72382a1d387aa556f6/menus-days-of-the-week-incorrect-icons%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![包含星期几的菜单图示，没有伴随符号。](https://docs-assets.developer.apple.com/published/72bddfbe313d096cac7f09d136d2a601/menus-days-of-the-week-correct-no-icons%402x.png)

![圆圈中的勾号表示正确用法。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**使用单个图标引入一组相似项目。** 与其为每个操作添加单独的图标，或为所有操作重用相同的图标，不如用第一个项目的符号建立共同主题，并依靠菜单项文本来区分其余项目。

![包含几个相似复制操作的编辑菜单图示，每个由不同的符号表示。](https://docs-assets.developer.apple.com/published/7deb98def27f19a33794b9ec6cee02b4/menus-copy-actions-different-icons-incorrect%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![包含几个相似复制操作的编辑菜单图示，每个由相同的复制符号表示。](https://docs-assets.developer.apple.com/published/60241bb399a7e5faa06e9e53de4d858b/menus-copy-actions-repeated-icons-incorrect%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![包含几个相似复制操作的编辑菜单图示。第一个由复制符号表示，其他没有符号。](https://docs-assets.developer.apple.com/published/ee3e63278a8b0b023e35e963077f2596/menus-copy-actions-single-icon-correct%402x.png)

![圆圈中的勾号表示正确用法。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

## [组织](https://developer.apple.com/design/human-interface-guidelines/menus#Organization)

以反映用户如何使用您的应用或游戏的方式组织菜单项，可以使您的体验感觉直观且易于使用。

**优先列出重要或常用的菜单项。** 用户倾向于从顶部开始扫描菜单，因此首先列出高优先级项目通常意味着用户可以在不阅读整个菜单的情况下找到他们想要的内容。

**考虑对逻辑相关的项目进行分组。** 例如，将"复制"、"剪切"和"粘贴"等编辑命令或"向上看"、"向下看"和"向左看"等相机命令分组可以帮助用户记住在哪里找到它们。为帮助用户在视觉上区分此类组，请使用分隔符。根据平台 and 菜单类型，_分隔符_在项目组之间显示为水平线或菜单背景外观中的短间隙。

**优先将所有逻辑相关的命令保持在同一组中，即使这些命令并非都具有相同的重要性。** 例如，用户使用"粘贴并匹配样式"的频率通常远低于"粘贴"，但他们期望在包含更常用的编辑命令（如"复制"和"剪切"）的同一组中找到这两个命令。

**注意菜单长度。** 用户需要更多的时间和注意力来阅读长菜单，这意味着他们可能会错过想要的命令。如果菜单太长，考虑将其分成单独的菜单。或者，您可以使用子菜单来缩短列表，例如在"新游戏"菜单项的子菜单中列出难度级别。例外是当菜单包含用户定义或动态生成的内容时，如 Safari 中的"历史记录"和"书签"菜单。用户期望这样的菜单容纳他们添加的所有项目，因此长菜单是可以的，滚动也是可接受的。

## [子菜单](https://developer.apple.com/design/human-interface-guidelines/menus#Submenus)

有时，菜单项可以在称为_子菜单_的从属列表中显示一组密切相关的项目。菜单项通过在其标签后显示符号（如 V 形）来指示子菜单的存在。除了层次位置外，子菜单在功能上与菜单相同。

**谨慎使用子菜单。** 每个子菜单都会增加界面的复杂性并隐藏其包含的项目。当同一组中有两个以上菜单项中出现某个术语时，您可以考虑创建子菜单。例如，与其为"按日期排序"、"按分数排序"和"按时间排序"提供单独的菜单项，游戏可以呈现一个使用子菜单列出排序选项"日期"、"分数"和"时间"的菜单项。在菜单项标签中使用重复术语（在本例中为"排序方式"）通常效果很好，可以帮助用户预测子菜单的内容。

**限制子菜单的深度和长度。** 用户可能难以显示多级层次子菜单，因此通常最好将其限制为单级。此外，如果子菜单包含超过约五个项目，请考虑创建新菜单。

**确保子菜单即使在其嵌套菜单项不可用时也保持可用。** 子菜单项（如所有菜单项）需要让用户打开它并了解其包含的命令。

**优先使用子菜单而不是缩进菜单项。** 使用缩进与系统不一致，并且不能清晰地表达菜单项之间的关系。

## [切换项](https://developer.apple.com/design/human-interface-guidelines/menus#Toggled-items)

菜单项通常表示用户可以打开或关闭的属性或对象。如果您想避免为每个状态列出单独的菜单项，创建一个传达当前状态并让用户更改它的单一切换菜单项可能更高效。

**考虑使用描述项目当前状态的可变标签。** 例如，与其列出"显示地图"和"隐藏地图"两个菜单项，您可以包含一个标签根据地图是否可见而从"显示地图"变为"隐藏地图"的菜单项。

**如果可变标签不够清晰，则包含动词。** 例如，用户可能不知道可变标签"HDR 开"和"HDR 关"描述的是操作还是状态。如果您需要阐明这些项目代表操作，可以在标签中添加动词，如"打开 HDR"和"关闭 HDR"。

**如有必要，显示两个菜单项而不是一个切换项。** 有时，让用户同时查看两个操作或状态会有所帮助。例如，游戏可以同时列出"将账户上线"和"将账户下线"项目，因此当某人的账户在线时，只有"将账户下线"菜单项显示为可用。

**考虑使用勾号显示当前生效的属性。** 用户可以轻松地在属性列表中扫描勾号以找到选中的属性。例如，在标准的"格式 > 字体"菜单中，勾号可以让用户轻松注意到应用于所选文本的样式。

**考虑提供一个菜单项，便于移除多个切换属性。** 例如，如果您让用户对所选文本应用多种样式，提供一个菜单项（如"纯文本"）可以一次性移除所有应用的格式属性。

## [游戏内菜单](https://developer.apple.com/design/human-interface-guidelines/menus#In-game-menus)

游戏内菜单为玩家提供控制游戏玩法以及确定整个游戏[设置](https://developer.apple.com/design/human-interface-guidelines/settings)的方式。

**让玩家使用平台的默认交互方法导航游戏内菜单。** 用户期望使用与导航设备上其他菜单相同的交互来导航您的菜单。例如，玩家期望在 iOS 和 iPadOS 中使用触摸导航您的游戏菜单，在 visionOS 中使用直接和间接手势。

**确保您的菜单在您支持的所有平台上都易于打开和阅读。** 每个平台都定义了最适合字体和交互目标的特定尺寸。有时，缩放游戏内容以在不同屏幕上显示——尤其是移动设备屏幕——可能会使游戏内菜单太小，用户无法阅读或交互。如果发生这种情况，请修改点击目标的尺寸并考虑替代方式来传达菜单内容。有关指导，请参阅[排版](https://developer.apple.com/design/human-interface-guidelines/typography)和[触摸控件](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/menus#Platform-considerations)

_macOS、tvOS 或 watchOS 无额外注意事项。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/menus#iOS-iPadOS)

在 iOS 和 iPadOS 中，菜单可以以下三种布局之一显示项目。

![显示小、中、大菜单布局的图表，每个包含相同的菜单项集。](https://docs-assets.developer.apple.com/published/d04cabb2d7b38602590cd6d59d79a0a0/small-medium-large-menu-layouts%402x.png)

* **小。** 四个项目的一行出现在菜单顶部，在包含其余项目的列表上方。对于顶行中的每个项目，菜单显示符号或图标，但不显示标签。

* **中。** 三个项目的一行出现在菜单顶部，在包含其余项目的列表上方。对于顶行中的每个项目，菜单在短标签上方显示符号或图标。

* **大（默认）。** 菜单在列表中显示所有项目。

开发者指导见 [`preferredElementSize`](https://developer.apple.com/documentation/UIKit/UIMenu/preferredElementSize)。

**当有助于简化用户选择时，选择小或中菜单布局。** 如果您的应用有三个用户经常想要执行的重要操作，请考虑使用中布局。例如，备忘录使用中布局为用户提供执行"扫描"、"锁定"和"固定"操作的快速方式。仅对通常作为一组出现的密切相关的操作使用小布局，如"粗体"、"斜体"、"下划线"和"删除线"。对于每个操作，使用可识别的符号，帮助用户在没有标签的情况下识别操作。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/menus#visionOS)

在 visionOS 中，菜单可以使用 iOS 和 iPadOS 定义的小或大布局样式显示项目（有关指导，请参阅 [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/menus#iOS-iPadOS)）。您可以使用 SwiftUI 视图从 3D 内容在应用或游戏中呈现菜单。为确保您的菜单始终对用户可见，即使其他内容遮挡它，您可以应用[穿透效果](https://developer.apple.com/documentation/swiftui/view/presentationbreakthrougheffect\(_:\))。与 macOS 一样，visionOS 窗口中打开的菜单可以出现在窗口边界之外。

**优先在菜单控制的内容附近显示菜单。** 由于用户需要在点击菜单项之前查看它，如果菜单控制的内容太远，他们可能会错过项目的效果。

![visionOS 中应用窗口的部分截图。窗口包含几个按钮，包括一个选中的"更多"按钮。包含操作列表的菜单显示在按钮下方。](https://docs-assets.developer.apple.com/published/b424693063f332d9edd65d555fec417e/visionos-notes-menu-popover-style%402x.png)

**在大多数情况下优先使用微妙的穿透效果。** 此效果将呈现与其周围内容混合，在保持可读性和可用性的同时保留场景的深度和上下文。当您为与 3D 内容重叠的菜单选择 [`automatic`](https://developer.apple.com/documentation/SwiftUI/BreakthroughEffect/automatic) 穿透效果时，系统默认应用 [`subtle`](https://developer.apple.com/documentation/SwiftUI/BreakthroughEffect/subtle)。如果您需要在应用或游戏的整个场景上突出显示菜单，可以使用 [`prominent`](https://developer.apple.com/documentation/SwiftUI/BreakthroughEffect/prominent)，但这可能会干扰用户体验并可能导致不适。或者，您可以使用 [`none`](https://developer.apple.com/documentation/SwiftUI/BreakthroughEffect/none) 将菜单完全遮挡在其他 3D 内容后面——例如，在需要用户绕过障碍物的益智游戏中——但这可能会使用户难以查看和访问菜单。

## [资源](https://developer.apple.com/design/human-interface-guidelines/menus#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/menus#Related)

[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)

[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

[上下文菜单](https://developer.apple.com/design/human-interface-guidelines/context-menus)

[菜单栏](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/menus#Developer-documentation)

[`Menu`](https://developer.apple.com/documentation/SwiftUI/Menu) — SwiftUI

[菜单和快捷键](https://developer.apple.com/documentation/UIKit/menus-and-shortcuts) — UIKit

[菜单](https://developer.apple.com/documentation/AppKit/menus) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/menus#Change-log)

日期| 变更
---|---
2025年12月16日| 添加了在 visionOS 中使用穿透效果呈现菜单的指导。
2025年7月28日| 添加了用图标表示菜单项的指导。
2024年6月10日| 添加了游戏内菜单的指导并包含游戏特定示例。
2023年6月21日| 更新以包含 visionOS 的指导。
2022年9月14日| 添加了在 iPadOS 中使用小、中、大菜单布局的指南。
