---
title: "Toolbars | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/toolbars

# 工具栏

工具栏提供对常用命令、控件、导航和搜索的便捷访问。

![工具栏的风格化展示，前缘带有返回控件，后缘包含撰写、共享和更多菜单。图像以红色着色，微妙地呼应了 Apple 原始六色 logo 中的红色。](https://docs-assets.developer.apple.com/published/c88cf44cf526483c94aa15bd2eb984e1/components-toolbar-intro%402x.png)

工具栏由一组或多组水平排列在视图顶部或底部边缘的控件组成，按逻辑分区归组。

工具栏对视图中的内容进行操作，辅助导航，并帮助用户在应用中定位。工具栏包含三种类型的内容：

  * 当前视图的标题

  * 导航控件，如前进和后退，以及[搜索栏](https://developer.apple.com/design/human-interface-guidelines/search-fields)

  * 操作项（即栏项），如[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)和[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)




与工具栏不同，[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)专门用于在应用的不同区域之间导航。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/toolbars#Best-practices)

**慎重选择项目，避免拥挤。** 用户需要能够区分和激活每个项目，因此不应在工具栏中放置过多项目。为适应不同的视图宽度，应定义当工具栏变窄时哪些项目移入溢出菜单。

注意

当项目不再容纳时，系统会在 macOS 或 iPadOS 中自动添加溢出菜单。请勿手动添加溢出菜单，并避免布局导致工具栏项目默认溢出。

**添加"更多"菜单来收纳额外操作。** 将次要操作优先归入"更多"菜单。尽量将所有操作都放在工具栏中，只在确实需要时才添加此菜单。

  * 标准
  * 紧凑



![Mac 上"备忘录"应用的截图，窗口宽度足以容纳所有可用的工具栏项目。"更多"菜单按钮出现在工具栏后缘，菜单在其下方展开。](https://docs-assets.developer.apple.com/published/38a70b5303c70f442fdf6e60c1caf000/toolbars-notes-app-expanded-icons%402x.png)macOS"备忘录"中的标准工具栏包含一个带有额外命令的"更多"菜单。

![Mac 上"备忘录"应用的截图，窗口较窄时系统将多个项目从工具栏移入溢出菜单，包括"更多"菜单按钮。溢出菜单已展开以显示其包含的项目。](https://docs-assets.developer.apple.com/published/d946d1a2815b1a181b0cd090e536cb21/toolbars-notes-app-collapsed-icons%402x.png)随着窗口变窄，"更多"菜单与其他不再容纳的工具栏项目一起移入溢出菜单。

**在 iPadOS 和 macOS 应用中，考虑允许用户自定义工具栏，添加其最常用的项目。** 工具栏自定义在以下场景特别有用：应用提供大量项目、包含非所有人都需要的高级功能，以及用户倾向于长时间使用的应用。例如，将一系列编辑操作开放给工具栏自定义是一个好做法，因为用户通常会根据工作风格和当前项目使用不同类型的编辑命令。

**减少工具栏背景和着色控件的使用。** 任何自定义背景和外观都可能覆盖或干扰系统提供的背景效果。应通过内容层来决定工具栏的颜色和外观，必要时使用 [`ScrollEdgeEffectStyle`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle) 来区分工具栏区域和内容区域。这种方式有助于应用展现独特风格，同时不分散对内容的注意力。

**避免将相似的颜色同时用于工具栏项目标签和内容层背景。** 如果应用的内容层已有鲜艳丰富的色彩，建议使用工具栏的默认单色外观。更多指导请参阅 [Liquid Glass 颜色](https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color)。

**优先在工具栏中使用标准组件。** 默认情况下，标准按钮、文本字段、页眉和页脚的圆角半径与栏角同心。如果需要创建自定义组件，请确保其圆角半径同样与栏角同心。

**考虑临时隐藏工具栏以获得无干扰体验。** 有时用户希望使用简洁界面来减少干扰或展示更多内容。如果支持此功能，请在最合适的情境下提供，并提供可靠恢复隐藏界面元素的方式。相关指导请参阅[全屏模式](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)。关于 visionOS 的特定指导，请参阅[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)。

## [标题](https://developer.apple.com/design/human-interface-guidelines/toolbars#Titles)

**为每个窗口提供有用的标题。** 标题帮助用户在导航应用时确认当前位置，并区分多个打开窗口的内容。如果工具栏标题显得多余，可以将标题区域留空。例如，"备忘录"在单窗口打开时不为当前备忘录添加标题，因为内容的第一行通常已提供足够的上下文。但在独立窗口中打开备忘录时，系统会以内容的第一行作为标题，以便用户区分。

**不要用应用名称作为窗口标题。** 应用名称不提供有关内容层级或应用中任何窗口或区域的有用信息，因此不适合作为标题。

**撰写简洁的标题。** 目标是用一个词或短语概括窗口或视图的用途，标题控制在 15 个字符以内，为其他控件留出足够空间。

## [导航](https://developer.apple.com/design/human-interface-guidelines/toolbars#Navigation)

带有导航控件的工具栏出现在窗口顶部，帮助用户在内容层级中移动。工具栏通常还包含[搜索栏](https://developer.apple.com/design/human-interface-guidelines/search-fields)，用于在不同区域或内容之间快速导航。在 iOS 中，专用于导航的工具栏有时称为导航栏。

**使用标准的返回和关闭按钮。** 用户知道标准返回按钮可以沿信息层级回溯，标准关闭按钮用于关闭模态视图。优先使用各自的标准符号，不要使用文字标签"_返回_"或"_关闭_"。如果创建自定义版本，请确保外观相同、行为符合预期且与界面其他部分一致，并在整个应用或游戏中保持统一实现。相关指导请参阅[图标](https://developer.apple.com/design/human-interface-guidelines/icons)。

![胶囊形返回按钮的示意图，前缘包含返回符号，后缘附带文字"返回"。](https://docs-assets.developer.apple.com/published/de859b5c4d42c9df2e92c680d48a37b2/toolbars-navigation-action-back-incorrect%402x.png)

![圆圈中的 X 号表示用法错误。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![标准圆形返回按钮的示意图，包含标准返回符号。](https://docs-assets.developer.apple.com/published/bf5f1cf48120b10f031bd9df57124f0f/toolbars-navigation-action-back-correct%402x.png)

![圆圈中的对勾表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

## [操作](https://developer.apple.com/design/human-interface-guidelines/toolbars#Actions)

**提供支持用户主要任务的操作。** 通常应优先放置用户最可能需要的命令。这些命令往往是最常用的，但在某些应用中，优先放置对应最高层级或最重要对象的命令可能更合理。

**确保每个控件的含义清晰。** 不要让用户猜测或尝试才能弄清工具栏项目的用途。优先使用简洁、易识别的符号而非文字，除非是"_编辑_"等难以用符号表达的操作。关于常用操作的符号指导，请参阅[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。

![带有文字按钮标签"筛选"、"删除"和"新建"的项目组示意图。](https://docs-assets.developer.apple.com/published/e39b41732b2b7cf5a40c682f6ec28448/toolbars-prefer-symbols-incorrect%402x.png)

![圆圈中的 X 号表示用法错误。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![带有符号按钮标签"筛选"、"删除"和"新建"的项目组示意图。](https://docs-assets.developer.apple.com/published/a90ab6d6f58aa023f4b830e4045b507b/toolbars-prefer-symbols-correct%402x.png)

![圆圈中的对勾表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**优先使用无边框的系统符号。** 系统符号为用户所熟悉，能自动获得适当的着色和活力效果，并对用户交互做出一致响应。边框（如带轮廓的圆形符号）并非必需，因为分区本身已提供可见的容器，系统会自动定义悬停和选中状态的外观。相关指导请参阅 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)。

![带有"筛选"和"更多"按钮的项目组示意图，按钮标签使用带圆形边框的符号。](https://docs-assets.developer.apple.com/published/90f36d797636e931c39663c146c1cb11/toolbars-icons-circle-outline-incorrect%402x.png)

![圆圈中的 X 号表示用法错误。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![带有"筛选"和"更多"按钮的项目组示意图，按钮标签使用无边框的符号。](https://docs-assets.developer.apple.com/published/e7b2189bb13488aab5e7eacc5eea9b1b/toolbars-icons-no-outline-correct%402x.png)

![圆圈中的对勾表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**对"完成"或"提交"等关键操作使用 `.prominent` 样式。** 这会将操作分离并着色，形成清晰的焦点。仅指定一个主要操作，并将其放置在工具栏后缘。

![两个工具栏项目的示意图，前缘为"筛选"按钮，后缘为"完成"按钮。按钮未分组，"完成"按钮应用了 prominent 样式以表明其为主要操作。](https://docs-assets.developer.apple.com/published/36c552c629c8a980c83501134e53d749/toolbars-prominent-action-tinted%402x.png)

## [项目分组](https://developer.apple.com/design/human-interface-guidelines/toolbars#Item-groupings)

你可以将工具栏项目放置在三个位置：前缘、中心区域和后缘。这些区域为导航控件、窗口或文档标题、常用操作和搜索提供了熟悉的位置。

  * **前缘。** 用于返回上一文档和显示/隐藏侧栏的元素位于最前缘，其后是视图标题。标题旁边可以包含一个文档菜单，其中包含影响整个文档的标准和应用专属命令，如"复制"、"重命名"、"移动"和"导出"。为确保这些项目始终可用，工具栏前缘的项目不可自定义。

  * **中心区域。** 常用且实用的控件出现在中心区域，如果视图标题不在前缘，也可以出现在此处。在 macOS 和 iPadOS 中，如果允许自定义工具栏，用户可以在此添加、删除和重新排列项目，且当窗口缩小到一定程度时，此区域的项目会自动折叠到系统管理的溢出菜单中。

  * **后缘。** 后缘包含需要始终保持可用的重要项目、用于打开附近检查器的按钮、可选的搜索栏，以及包含额外项目并支持工具栏自定义的"更多"菜单。当存在"完成"等主要操作时，也会出现在此区域。后缘的项目在所有窗口尺寸下均保持可见。




![iPad 上 Freeform 应用顶部工具栏的示意图。标注指明了工具栏前缘、中心区域和后缘的项目分组位置。](https://docs-assets.developer.apple.com/published/882504f8e992b3ce0e373f47523adf5e/toolbars-ipad-anatomy%402x.png)

要将项目定位到你想要的分组中，请将它们固定到前缘、中心或后缘，并在按钮或其他项目之间适当插入间距。

**按功能和使用频率对工具栏项目进行逻辑分组。** 例如，Keynote 包含多个基于功能的分区，包括演示文稿级命令、播放命令和对象插入。

**将导航控件和"完成"、"关闭"或"保存"等关键操作放在专门的、熟悉的且视觉上明显的分区中。** 这反映了它们的重要性，帮助用户发现和理解这些操作。

![iPhone 顶部工具栏的示意图，后退、前进、工具选择和"更多"菜单的控件被分在后缘的单一分区中。](https://docs-assets.developer.apple.com/published/9349ac4f406f84c24e98a6b9445b9560/toolbars-layout-grouping-incorrect%402x.png)

![圆圈中的 X 号表示用法错误。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![iPhone 顶部工具栏的示意图，后退和前进控件分组在前缘，工具选择和"更多"菜单控件分组在后缘。](https://docs-assets.developer.apple.com/published/2fede653e14b982c4b2c65f3ca657278/toolbars-layout-grouping-correct%402x.png)

![圆圈中的对勾表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**在各平台保持一致的分组和布局。** 这有助于用户熟悉你的应用，并确信无论在哪个平台使用，应用的行为都是一致的。

**尽量减少分组数量。** 即使在 iPad 和 Mac 上有更多空间，过多的控件分组也会让工具栏显得杂乱和令人困惑。通常建议最多三个分组。

**将带有文字标签的操作保持独立。** 将文字标签操作与符号操作放在一起，可能会让人误以为是一个带有文字和符号组合的单一操作，从而造成困惑和误解。如果工具栏包含多个带文字标签的按钮，按钮的文字可能会连成一片，难以区分。请通过在按钮之间插入固定间距来增加分隔。开发者指导请参阅 [`UIBarButtonItem.SystemItem.fixedSpace`](https://developer.apple.com/documentation/UIKit/UIBarButtonItem/SystemItem/fixedSpace)。

![iPhone 顶部工具栏的示意图，带文字标签的"编辑"控件和带符号的"共享"控件分组在后缘。](https://docs-assets.developer.apple.com/published/de7f7298c70900b9c2f65d5cae7c6d60/toolbars-layout-text-action-grouping-incorrect%402x.png)

![圆圈中的 X 号表示用法错误。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![iPhone 顶部工具栏的示意图，带文字标签的"编辑"控件和带符号的"共享"控件各自独立分区在后缘。](https://docs-assets.developer.apple.com/published/c46f284f584841d7783aa2090426ca9b/toolbars-layout-text-action-grouping-correct%402x.png)

![圆圈中的对勾表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/toolbars#Platform-considerations)

 _tvOS 无额外考量。_

### [iOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#iOS)

**主工具栏区域仅优先放置最重要的项目。** 由于空间非常有限，请仔细考虑哪些操作对应用至关重要，并优先包含。使用"更多"菜单来收纳额外项目。

**使用大标题帮助用户在导航和滚动时保持方向感。** 默认情况下，大标题在用户开始滚动内容时过渡为标准标题，当用户滚动到顶部时恢复为大标题，提醒他们当前所在位置。开发者指导请参阅 [`prefersLargeTitles`](https://developer.apple.com/documentation/UIKit/UINavigationBar/prefersLargeTitles)。

### [iPadOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#iPadOS)

**考虑将工具栏与标签栏结合使用。** 在 iPadOS 中，工具栏和[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)可以共存于视图顶部的同一水平空间中。这对于需要在几个主要应用区域之间导航，同时保持窗口完整宽度用于内容的布局特别有用。相关指导请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)和[窗口](https://developer.apple.com/design/human-interface-guidelines/windows)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS)

在 macOS 应用中，工具栏位于窗口顶部的框架内，位于标题栏下方或与标题栏集成。请注意，窗口标题可以与控件内联显示，且工具栏项目不包含边框。

![macOS 中 Finder 窗口的示意图，标注显示了工具栏和窗口框架的位置。](https://docs-assets.developer.apple.com/published/a595dda6ba3dd30cbd7c9851d941be72/toolbars-mac-window-anatomy%402x.png)

**确保每个工具栏项目在菜单栏中都有对应命令。** 由于用户可以自定义或隐藏工具栏，它不能是呈现命令的唯一位置。反过来，为每个菜单项都提供工具栏项目也不合理，因为并非所有菜单命令都重要或常用到值得在工具栏中占据空间。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#visionOS)

在 visionOS 中，系统提供的工具栏位于窗口底部边缘，位于窗口管理控件上方，处于一个平行平面中，沿 z 轴略微位于窗口前方。

![visionOS 中 Notes 应用窗口底部工具栏的截图。](https://docs-assets.developer.apple.com/published/47985b0aebd160790502368ff9e282a1/visionos-toolbar-notes-app%402x.png)

为确保内容在工具栏后方滚动时工具栏项目的可读性，visionOS 在栏背景中使用可变模糊效果。可变模糊将栏锚定在滚动内容上方，同时保持视图的玻璃材质均匀且不被分割。

在 visionOS 中，你可以为每个工具栏项目提供符号或文字标签。当用户注视包含符号的工具栏项目时，visionOS 会显示文字标签，提供额外信息。

**优先使用系统提供的工具栏。** 标准工具栏具有一致且熟悉的外观，并针对眼部和手势输入进行了优化。此外，系统会自动将标准工具栏放置在相对于其窗口的正确位置。

![visionOS 中工具栏的截图。](https://docs-assets.developer.apple.com/published/449acaaf0268d1fff08e9bf41b7c82d9/visionos-toolbar-standard-layout%402x.png)

**避免创建垂直工具栏。** 在 visionOS 中，[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)是垂直的，因此展示垂直工具栏可能会让用户感到困惑。

**尽量防止窗口缩小到小于工具栏的宽度。** visionOS 不包含用于列出所有应用操作的菜单栏，因此工具栏必须在任何窗口尺寸下都能可靠地提供对必要控件的访问。

**如果你的应用可以进入模态状态，考虑提供与上下文相关的工具栏控件。** 例如，照片编辑应用可能会进入模态状态以帮助用户执行多步骤编辑任务。在这种场景下，模态编辑视图中的控件与主窗口中的控件不同。请确保应用退出模态状态时恢复窗口的标准工具栏控件。

**避免在工具栏中使用下拉菜单。** 下拉菜单可以提供与工具栏项目相关的额外操作，但用户可能难以发现，且可能使界面显得杂乱。由于 visionOS 中工具栏位于窗口底部边缘，下拉菜单可能会遮挡出现在底部边缘下方的标准窗口控件。相关指导请参阅[下拉按钮](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#watchOS)

工具栏按钮可在显示相关内容的视图中提供重要的应用功能。你可以将工具栏按钮放置在顶部角落或底部。如果将按钮放置在滚动内容上方，按钮始终保持可见，内容在其下方滚动。

![显示顶部前缘和后缘角落工具栏按钮的截图。](https://docs-assets.developer.apple.com/published/464c7be02e97dcb7470c9b8202dc2b59/toolbars-watch-top-buttons%402x.png)

顶部工具栏按钮

![显示底部前缘和后缘角落两个工具栏按钮的截图。](https://docs-assets.developer.apple.com/published/53d742601fa4b250207336099587e1d3/toolbars-watch-bottom-buttons%402x.png)

底部工具栏按钮

开发者指导请参阅 [`topBarLeading`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement/topBarLeading)、[`topBarTrailing`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement/topBarTrailing) 或 [`bottomBar`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement/bottomBar)。

你还可以将按钮放置在滚动视图中。默认情况下，滚动工具栏按钮会保持隐藏，直到用户向上滚动时才会显示。用户经常滚动到滚动视图的顶部，因此发现工具栏按钮是自然而然的。

![显示顶部前缘和后缘角落两个工具栏按钮的截图。工具栏在滚动视图中还有一个主要操作按钮，但处于隐藏状态。](https://docs-assets.developer.apple.com/published/027a24ac805a9e7976a1ccd1df68f0d3/toolbars-watch-primary-button-hidden%402x.png)

工具栏按钮隐藏

![显示顶部前缘和后缘角落两个工具栏按钮的截图。工具栏在滚动视图中显示主要操作按钮。](https://docs-assets.developer.apple.com/published/e010a0cdf42f792ebb4715cdd5f65676/toolbars-watch-primary-button-visible%402x.png)

工具栏按钮显示

开发者指导请参阅 [`primaryAction`](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement/primaryAction)。

**对非主要应用功能但同样重要的操作使用滚动工具栏按钮。** 工具栏按钮的灵活性在于，你可以在主要目的与该功能相关但不完全相同的视图中提供重要功能。例如，"邮件"在"收件箱"视图顶部的工具栏按钮中提供了必不可少的"新邮件"操作。收件箱的主要目的是显示可滚动的邮件列表，因此在视图顶部的工具栏按钮中提供与之紧密相关的撰写操作是合理的。

## [资源](https://developer.apple.com/design/human-interface-guidelines/toolbars#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/toolbars#Related)

[侧栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)

[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

[布局](https://developer.apple.com/design/human-interface-guidelines/layout)

[按钮](https://developer.apple.com/design/human-interface-guidelines/buttons)

[搜索栏](https://developer.apple.com/design/human-interface-guidelines/search-fields)

[Apple Design Resources](https://developer.apple.com/design/resources/)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/toolbars#Developer-documentation)

[Toolbars](https://developer.apple.com/documentation/SwiftUI/Toolbars) — SwiftUI

[`UIToolbar`](https://developer.apple.com/documentation/UIKit/UIToolbar) — UIKit

[`NSToolbar`](https://developer.apple.com/documentation/AppKit/NSToolbar) — AppKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/toolbars#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/1AAA030E-2ECA-47D8-AE09-6D7B72A840F6/10044_wide_250x141_1x.jpg) 了解全新的设计系统](https://developer.apple.com/videos/play/wwdc2025/356)

## [变更记录](https://developer.apple.com/design/human-interface-guidelines/toolbars#Change-log)

日期| 变更内容
---|---
2025 年 12 月 16 日| 更新了 Liquid Glass 相关指导。
2025 年 6 月 9 日| 新增了栏项目分组指导，更新了符号使用指导，并整合了导航栏指导。
2023 年 6 月 21 日| 更新以包含 visionOS 相关指导。
2023 年 6 月 5 日| 更新了 watchOS 工具栏使用指导。
