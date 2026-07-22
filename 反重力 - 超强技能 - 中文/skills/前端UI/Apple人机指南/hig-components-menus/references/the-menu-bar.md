---
title: "The menu bar | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar

# 菜单栏

在 Mac 或 iPad 上，屏幕顶部的菜单栏显示应用或游戏的顶级菜单。

![显示所选菜单的 macOS 菜单栏的样式化呈现。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/1196662c916a44013329c4c6a1ba03d4/components-the-menu-bar-intro%402x.png)

Mac 用户非常熟悉 macOS 菜单栏，他们依赖它来帮助了解应用的功能并找到所需的命令。为帮助您的应用或游戏在 macOS 中感觉自然，提供一致的菜单栏体验至关重要。

iPad 上的菜单栏菜单与 Mac 上的类似，以相同的顺序出现，并包含熟悉的菜单项集。当您采用用户从 Mac 体验中期望的菜单结构时，这也有助于他们立即理解并利用 iPad 上的菜单栏。

iPadOS 中的键盘快捷键使用与 macOS 相同的模式。有关指导，请参阅[标准键盘快捷键](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)。

![iPad 上应用窗口的图示，其菜单栏出现在屏幕顶部，编辑菜单打开。](https://docs-assets.developer.apple.com/published/7c3a4ae9470f62e0eb41b8ce297032f8/menu-bar-ipad-overview%402x.png)

菜单栏中的菜单共享所有菜单类型具有的大多数外观和行为特征。要了解一般菜单——以及如何组织和标记菜单项——请参阅[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

## [结构](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Anatomy)

当菜单栏中存在以下菜单时，它们按下面列出的顺序出现。

* _您的应用名称_（您为此菜单的标题提供应用的短名称）
* 文件
* 编辑
* 格式
* 显示
* 应用特定菜单（如有）
* 窗口
* 帮助

此外，macOS 菜单栏在前缘包含 Apple 菜单，在后缘包含菜单栏附加项。请参阅 [macOS 平台注意事项](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#macOS)获取指导。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Best-practices)

**支持默认的系统定义菜单及其顺序。** 用户期望以熟悉的顺序找到菜单和菜单项。在许多情况下，系统实现标准菜单项的功能，因此您不必这样做。例如，当用户在标准文本字段中选择文本时，系统使"编辑 > 复制"菜单项可用。

**始终显示相同的菜单项集。** 保持菜单项可见有助于用户了解您的应用支持哪些操作，即使它们在当前上下文中不可用。如果菜单栏项目不可操作，请禁用该操作而不是从菜单中隐藏它。

**用熟悉的图标表示菜单项操作。** 图标帮助用户在整个应用中识别常见操作。使用与系统相同的图标来表示"复制"、"共享"和"删除"等操作，无论它们出现在哪里。有关表示常见操作的图标列表，请参阅[标准图标](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons)。有关其他指导，请参阅[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

**支持您包含的标准菜单项定义的键盘快捷键。** 用户期望对他们已经知道的标准菜单项使用键盘快捷键，如"复制"、"剪切"、"粘贴"、"保存"和"打印"。仅在必要时定义自定义键盘快捷键。有关指导，请参阅[标准键盘快捷键](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)。

**优先使用简短的单字菜单标题。** 各种因素——如不同的显示尺寸和菜单栏附加项的存在——可能会影响菜单的间距和外观。单字菜单标题在菜单栏中效果特别好，因为它们占用很少的空间，用户易于扫描。如果需要在菜单标题中使用多个单词，请使用标题式大写。

## [应用菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#App-menu)

应用菜单列出适用于整个应用或游戏的项目，而不是特定任务、文档或窗口。为帮助用户快速识别活动应用，菜单栏以粗体显示您的应用名称。

应用菜单通常包含以下按以下顺序列出的菜单项。

菜单项| 操作| 指导
---|---|---
关于 _您的应用名称_| 显示应用的关于窗口，其中包括版权和版本信息。| 优先使用 16 个字符或更少的短名称。不要包含版本号。
设置…| 打开您的[设置](https://developer.apple.com/design/human-interface-guidelines/settings)窗口，或您应用在 iPadOS 设置中的页面。| 仅用于应用级设置。如果您还提供文档特定设置，请将它们放在文件菜单中。
可选的应用特定项目| 执行自定义应用级设置或配置操作。| 在设置项目之后的同一组中列出自定义应用配置项目。
服务（仅 macOS）| 显示来自系统和其他应用的适用于当前上下文的服务子菜单。|
隐藏 _您的应用名称_（仅 macOS）| 隐藏您的应用及其所有窗口，然后激活最近使用的应用。| 使用您为关于项目提供的相同短应用名称。
隐藏其他（仅 macOS）| 隐藏所有其他打开的应用及其窗口。|
显示全部（仅 macOS）| 在您的应用窗口后面显示所有其他打开的应用及其窗口。|
退出 _您的应用名称_| 退出您的应用。按 Option 键将"退出 _您的应用名称_"更改为"退出并保留窗口"。| 使用您为关于项目提供的相同短应用名称。

**首先显示关于菜单项。** 在关于菜单项后包含分隔符，使其单独出现在一个组中。

## [文件菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)

文件菜单包含帮助用户管理应用支持的文件或文档的命令。如果您的应用不处理任何类型的文件，您可以重命名或删除此菜单。

文件菜单通常包含以下按以下顺序列出的菜单项。

菜单项| 操作| 指导
---|---|---
新建 _项目_| 创建新文档、文件或窗口。| 对于_项目_，使用命名您的应用创建的项目类型的术语。例如，日历使用_事件_和_日历_。
打开| 可以打开所选项目或呈现一个界面，让用户在其中选择要打开的项目。| 如果用户需要在单独的界面中选择项目，命令后跟省略号以表示需要更多输入。
打开最近| 显示一个子菜单，列出用户可以选择的最近打开的文档和文件，通常包含一个"清除菜单"项目。| 在子菜单中列出用户可识别的文档和文件名；不要显示文件路径。按用户最后打开的顺序列出文档，最近打开的文档排在最前面。
关闭| 关闭当前窗口或文档。按 Option 键将关闭更改为全部关闭。对于基于标签的窗口，关闭标签替换关闭。| 在基于标签的窗口中，考虑添加关闭窗口项目，让用户通过一次点击关闭整个窗口。
保存| 保存当前文档或文件。| 在用户工作时定期自动保存更改，这样他们就不需要一直选择"文件 > 保存"。对于新文档，提示用户输入名称和位置。如果需要让用户以多种格式保存文件，优先使用弹出菜单，让用户在保存表单中选择格式。
复制| 复制当前文档，两个文档都保持打开。按 Option 键将复制更改为另存为。| 优先使用复制而不是"另存为"、"导出"、"复制到"和"保存到"等项目，因为这些项目没有阐明原始文件和新文件之间的关系。
重命名…| 让用户更改当前文档的名称。|
移动到…| 提示用户为文档选择新位置。|
导出为…| 提示用户输入名称、输出位置和导出文件格式。导出文件后，当前文档保持打开；导出的文件不会打开。| 仅在需要让用户以应用通常不处理的格式导出内容时保留导出为项目。
恢复到| 当用户打开自动保存时，显示一个子菜单，列出最近的文档版本和显示版本浏览器的选项。用户选择要恢复的版本后，它替换当前文档。|
页面设置…| 打开一个面板，用于指定打印参数，如纸张大小和打印方向。文档可以保存用户指定的打印参数。| 如果需要支持适用于特定文档的打印参数，请包含页面设置项目。全局性质的参数（如打印机名称）或用户频繁更改的参数（如要打印的份数）属于打印面板。
打印…| 打开标准打印面板，让用户打印到打印机、发送传真或保存为 PDF。|

## [编辑菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)

编辑菜单让用户对当前文档或文本容器中的内容进行更改，并提供与剪贴板交互的命令。由于许多编辑命令适用于任何可编辑内容，即使不是基于文档的应用，编辑菜单也很有用。

**确定查找菜单项是否属于编辑菜单。** 例如，如果您的应用让用户搜索文件或其他类型的对象，查找菜单项可能更适合放在文件菜单中。

编辑菜单通常包含以下按以下顺序列出的顶级菜单项。

菜单项| 操作| 指导
---|---|---
撤销| 撤销上一个用户操作的效果。| 阐明撤销的目标。例如，如果用户刚刚选择了菜单项，您可以附加项目的标题，如"撤销粘贴并匹配样式"。对于文本输入操作，您可能附加单词_输入_以给出"撤销输入"。
重做| 撤销上一个撤销操作的效果。| 阐明重做的目标。例如，如果用户刚刚撤销了菜单项选择，您可以附加项目的标题，如"重做粘贴并匹配样式"。对于文本输入操作，您可能附加单词_输入_以给出"重做输入"。
剪切| 移除所选数据并将其存储在剪贴板上，替换剪贴板以前的内容。|
复制| 复制所选数据并将其存储在剪贴板上。|
粘贴| 在当前插入点插入剪贴板的内容。剪贴板内容保持不变，允许用户多次选择粘贴。|
粘贴并匹配样式| 在当前插入点插入剪贴板的内容，将插入文本的样式与周围文本匹配。|
删除| 移除所选数据，但不将其放在剪贴板上。| 提供删除菜单项而不是擦除或清除菜单项。选择删除等同于按删除键，因此命名保持一致很重要。
全选| 高亮显示当前文档或文本容器中的所有可选内容。|
查找| 显示一个子菜单，包含在当前文档或文本容器中执行搜索操作的菜单项。标准子菜单包括：查找、查找和替换、查找下一个、查找上一个、使用选择进行查找和跳转到选择。|
拼写和语法| 显示一个子菜单，包含在当前文档或文本容器中检查和纠正拼写和语法的菜单项。标准子菜单包括：显示拼写和语法、立即检查文档、输入时检查拼写、随拼写检查语法和自动纠正拼写。|
替换| 显示一个子菜单，包含让用户在文档或文本容器中输入时切换自动替换的项目。标准子菜单包括：显示替换、智能复制/粘贴、智能引号、智能破折号、智能链接、数据检测器和文本替换。|
转换| 显示一个子菜单，包含转换所选文本的项目。标准子菜单包括：全部大写、全部小写和首字母大写。|
语音| 显示一个子菜单，包含开始朗读和停止朗读项目，控制系统何时朗读所选文本。|
开始听写| 打开听写窗口并将口语转换为在当前插入点添加的文本。系统自动在编辑菜单底部添加开始听写菜单项。|
表情与符号| 显示字符查看器，其中包含用户可以在当前插入点插入的表情符号、符号和其他字符。系统自动在编辑菜单底部添加表情与符号菜单项。|

## [格式菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Format-menu)

格式菜单让用户调整当前文档或文本容器中的文本格式属性。如果您的应用不支持格式化文本编辑，您可以排除此菜单。

格式菜单通常包含以下按以下顺序列出的顶级菜单项。

菜单项| 操作
---|---
字体| 显示一个子菜单，包含调整所选文本字体属性的项目。标准子菜单包括：显示字体、粗体、斜体、下划线、放大、缩小、显示颜色、复制样式和粘贴样式。
文本| 显示一个子菜单，包含调整所选文本文本属性的项目。标准子菜单包括：左对齐、居中对齐、两端对齐、右对齐、书写方向、显示标尺、复制标尺和粘贴标尺。

## [显示菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu)

显示菜单让用户自定义应用所有窗口的外观，无论类型如何。

重要

显示菜单不包含在特定窗口之间导航或管理特定窗口的项目；[窗口菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu)提供这些命令。

**即使您的应用仅支持标准显示功能的子集，也要提供显示菜单。** 例如，如果您的应用不包含标签栏、工具栏或侧边栏，但支持全屏模式，请提供仅包含"进入/退出全屏"菜单项的显示菜单。

**确保每个显示/隐藏项目标题反映相应视图的当前状态。** 例如，当工具栏隐藏时，提供"显示工具栏"菜单项；当工具栏可见时，提供"隐藏工具栏"菜单项。

显示菜单通常包含以下按以下顺序列出的顶级菜单项。

菜单项| 操作
---|---
显示/隐藏标签栏| 在基于标签的窗口中切换主体区域上方[标签栏](https://developer.apple.com/design/human-interface-guidelines/tab-bars)的可见性
显示所有标签/退出标签概览| 进入和退出提供基于标签的窗口中所有打开标签概览的视图（类似于任务控制）
显示/隐藏工具栏| 在包含[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)的窗口中，切换工具栏的可见性
自定义工具栏| 在包含工具栏的窗口中，打开一个让用户自定义工具栏项目的视图
显示/隐藏侧边栏| 在包含[侧边栏](https://developer.apple.com/design/human-interface-guidelines/sidebars)的窗口中，切换侧边栏的可见性
进入/退出全屏| 在支持[全屏体验](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)的应用中，以全屏尺寸在新空间中打开窗口

## [应用特定菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#App-specific-menus)

您的应用的自定义菜单出现在菜单栏中显示菜单和窗口菜单之间。例如，Safari 的菜单栏包含应用特定的历史记录和书签菜单。

**为自定义命令提供应用特定菜单。** 用户在搜索应用特定命令时会查看菜单栏，尤其是在首次使用应用时。即使命令在应用的其他地方可用，将它们列在菜单栏中也很重要。将命令放在菜单栏中使它们更容易被用户找到，让您可以为它们分配键盘快捷键，并使它们对使用全键盘访问的用户更易访问。将命令排除在菜单栏之外——即使是很少使用或高级命令——也有让所有人都难以找到的风险。

**尽可能在应用特定菜单中反映应用的层次结构。** 例如，邮件按反映这些项目关系的顺序列出邮箱、邮件和格式菜单：邮箱包含邮件，邮件包含格式。

**以从最通用到最不通用或最常用到最不常用的顺序列出应用特定菜单为目标。** 用户倾向于期望列表前端的菜单比后端的菜单更专业化。

## [窗口菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu)

窗口菜单让用户导航、组织和管理应用的窗口。

重要

窗口菜单不帮助用户自定义窗口外观或关闭窗口。要自定义窗口，用户使用[显示菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu)中的命令；要关闭窗口，用户选择[文件菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)中的关闭。

**即使您的应用只有一个窗口，也要提供窗口菜单。** 包含最小化和缩放菜单项，以便使用全键盘访问的用户可以使用键盘调用这些功能。

**考虑包含显示和隐藏面板的菜单项。** [面板](https://developer.apple.com/design/human-interface-guidelines/panels)提供信息、配置选项或与主窗口中内容交互的工具，通常仅在用户需要时出现。无需提供对字体面板或文本颜色面板的访问，因为格式菜单列出了这些面板。

窗口菜单通常包含以下按以下顺序列出的顶级菜单项。

菜单项| 操作| 指导
---|---|---
最小化| 将活动窗口最小化到 Dock。按 Option 键将此项目更改为全部最小化。|
缩放| 在适合窗口内容的预定义尺寸和用户设置的窗口尺寸之间切换。按 Option 键将此项目更改为全部缩放。| 避免使用缩放进入或退出全屏模式。[显示菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu)支持这些功能。
显示上一个标签| 在基于标签的窗口中显示当前标签之前的标签。|
显示下一个标签| 在基于标签的窗口中显示当前标签之后的标签。|
将标签移动到新窗口| 在新窗口中打开当前标签。|
合并所有窗口| 将所有打开的窗口合并为单个带标签的窗口。|
进入/退出全屏| 在支持[全屏体验](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)的应用中，以全屏尺寸在新空间中打开窗口。| 仅当您的应用没有显示菜单时才在窗口菜单中包含此项目。在这种情况下，继续提供单独的最小化和缩放菜单项。
全部置前| 将应用所有打开的窗口带到前面，保持其在屏幕上的位置、尺寸和层叠顺序。（点击 Dock 中的应用图标具有相同的效果。）按 Option 键将此项目更改为排列在前面，将应用的窗口以整齐平铺的排列方式带到前面。|
_打开的应用特定窗口的名称_| 将所选窗口带到前面。| 按字母顺序列出当前打开的窗口以便于扫描。避免列出面板或其他模态视图。

## [帮助菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Help-menu)

帮助菜单位于菜单栏的后端，提供对应用帮助文档的访问。当您为此文档使用帮助书籍格式时，macOS 自动在帮助菜单顶部包含搜索字段。

菜单项| 操作| 指导
---|---|---
向 Apple 发送 _您的应用名称_ 反馈| 打开反馈助理，用户可以在其中提供反馈。|
_您的应用名称_ 帮助| 当内容使用帮助书籍格式时，在内置帮助查看器中打开内容。|
_附加项目_| | 在主要帮助文档和附加项目之间使用分隔符，附加项目可能包含注册信息或发行说明。保持帮助菜单中列出的项目总数较少，以避免在用户需要帮助时用太多选择让他们不知所措。或者，考虑从帮助文档中链接到附加项目。

有关指导，请参阅[提供帮助](https://developer.apple.com/design/human-interface-guidelines/offering-help)；开发者指导见 [`NSHelpManager`](https://developer.apple.com/documentation/AppKit/NSHelpManager)。

## [动态菜单项](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Dynamic-menu-items)

在极少数情况下，呈现_动态菜单项_可能有意义，动态菜单项是用户在按住修饰键（Control、Option、Shift 或 Command）的同时选择时更改其行为的菜单项。例如，窗口菜单中的_最小化_项目在用户按 Option 键时更改为_全部最小化_。

**避免使动态菜单项成为完成任务的唯一方式。** 动态菜单项默认隐藏，因此它们最适合提供用户可以以其他方式完成的高级操作的快捷方式。例如，如果某人没有发现窗口菜单中的_全部最小化_动态菜单项，他们仍然可以最小化每个打开的窗口。

**主要在菜单栏菜单中使用动态菜单项。** 向上下文或 Dock 菜单添加动态菜单项可能会使项目更难被用户发现。

**仅需单个修饰键即可显示动态菜单项。** 在同时打开菜单并选择菜单项的同时按多个键可能在物理上别扭，此外还会降低动态行为的可发现性。开发者指导见 [`isAlternate`](https://developer.apple.com/documentation/AppKit/NSMenuItem/isAlternate)。

提示

macOS 自动设置菜单的宽度以容纳最宽的项目，包括动态菜单项。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Platform-considerations)

_iOS、tvOS、visionOS 或 watchOS 不支持。_

### [iPadOS](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#iPadOS)

菜单栏显示应用或游戏的顶级菜单，包括系统提供的菜单和您选择添加的任何自定义菜单。用户通过将指针移动到屏幕顶部边缘或从顶部向下滑动来显示菜单栏。可见时，菜单栏占据与屏幕顶部边缘的[状态栏](https://developer.apple.com/design/human-interface-guidelines/status-bars)相同的垂直空间。

与 macOS 菜单栏一样，iPadOS 菜单栏为用户提供了一种熟悉的方式来了解应用的功能、找到所需的命令并发现键盘快捷键。虽然它们在大多数方面相似，但每个平台上的菜单栏之间存在一些关键差异。

| iPadOS| macOS
---|---|---
菜单栏可见性| 隐藏直到显示| 默认可见
水平对齐| 居中| 前缘
菜单栏附加项| 不可用| 系统默认和自定义
窗口控件| 应用全屏时在菜单栏中| 从不在菜单栏中
Apple 菜单| 不可用| 始终可用
应用菜单| 关于、服务和应用可见性相关项目不可用| 始终可用

**由于应用全屏运行时菜单栏通常隐藏，确保用户可以通过其 UI 访问应用的所有功能。** 特别是，始终提供其他方式来完成分配给动态菜单项的任务，因为这些仅在连接硬件键盘时可用。避免使用菜单栏作为不适合其他地方的功能的包罗万象的位置。

**保留"您的应用名称 > 设置"菜单项用于打开您应用在 iPadOS 设置中的页面。** 如果您的应用包含自己的内部首选项区域，请使用同一组中设置下方的单独菜单项链接到它。将任何其他自定义应用范围配置选项也放在此部分中。

**对于具有标签式导航的应用，考虑将每个标签作为显示菜单中的菜单项添加。** 由于每个标签是应用的不同视图，显示菜单是提供在标签之间导航的另一种方式的自然位置。如果这样做，考虑为每个标签分配键绑定以使导航更加方便。

**考虑将菜单项分组到子菜单中以节省垂直空间。** iPad 上的菜单项行比 Mac 上使用更多空间以使其更易于点击。因此，以及某些 iPad 的较小屏幕尺寸，比 Mac 上的菜单栏更频繁地将相关项目分组到子菜单中可能会有所帮助。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#macOS)

macOS 中的菜单栏包含 Apple 菜单，它始终是菜单栏前缘的第一个项目。Apple 菜单包含始终可用的系统定义菜单项，您无法修改或删除它。在空间允许的情况下，系统还可以在菜单栏的后端显示菜单栏附加项。有关指导，请参阅[菜单栏附加项](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Menu-bar-extras)。

当菜单栏空间受限时，系统优先显示菜单和基本菜单栏附加项。为确保菜单保持可读，系统可能会减少标题之间的间距，必要时截断它们。

当用户进入全屏模式时，菜单栏通常隐藏，直到他们通过将指针移动到屏幕顶部来显示它。有关指导，请参阅[进入全屏](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)。

#### [菜单栏附加项](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Menu-bar-extras)

菜单栏附加项使用应用运行时出现在菜单栏中的图标公开应用特定功能，即使它不是最前面的应用。菜单栏附加项位于菜单栏上与应用菜单相反的一侧。开发者指导见 [`MenuBarExtra`](https://developer.apple.com/documentation/SwiftUI/MenuBarExtra)。

必要时，系统隐藏菜单栏附加项以为应用菜单腾出空间。同样，如果菜单栏附加项太多，系统可能会隐藏一些以避免拥挤应用菜单。

![输入法菜单栏附加项及其菜单的截图。](https://docs-assets.developer.apple.com/published/97a8b1969dd941fc8920da157b345fb5/menu-bar-extras%402x.png)

**考虑使用符号来表示您的菜单栏附加项。** 您可以创建[图标](https://developer.apple.com/design/human-interface-guidelines/icons)或选择 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) 之一，按原样使用或自定义以满足您的需求。界面图标和符号都使用黑色和透明颜色来定义其形状；系统可以将其他颜色应用于每个图像中的黑色区域，使其在深色和浅色菜单栏上看起来都不错，并在您的菜单栏附加项被选中时。菜单栏的高度为 24 pt。

**当用户点击您的菜单栏附加项时显示菜单——而不是弹出框。** 除非您想要公开的应用功能对于菜单来说太复杂，否则避免在[弹出框](https://developer.apple.com/design/human-interface-guidelines/popovers)中呈现它。

**让用户——而不是您的应用——决定是否将您的菜单栏附加项放在菜单栏中。** 通常，用户通过在应用的设置窗口中更改设置将菜单栏附加项添加到菜单栏。但是，为确保可发现性，请考虑在设置期间为用户提供这样做的选项。

**避免依赖菜单栏附加项的存在。** 系统定期隐藏和显示菜单栏附加项，您无法确定用户选择显示哪些其他菜单栏附加项或预测您的菜单栏附加项的位置。

**考虑以其他方式公开应用特定功能。** 例如，您可以提供当用户 Control 点击应用的 Dock 图标时出现的 [Dock 菜单](https://developer.apple.com/design/human-interface-guidelines/dock-menus)。用户可以隐藏或选择不使用您的菜单栏附加项，但当您的应用运行时，Dock 菜单始终可用。

## [资源](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Related)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[Dock 菜单](https://developer.apple.com/design/human-interface-guidelines/dock-menus)

[标准键盘快捷键](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Developer-documentation)

[`CommandMenu`](https://developer.apple.com/documentation/SwiftUI/CommandMenu) — SwiftUI

[向菜单栏和用户界面添加菜单和快捷键](https://developer.apple.com/documentation/UIKit/adding-menus-and-shortcuts-to-the-menu-bar-and-user-interface) — UIKit

[`NSStatusBar`](https://developer.apple.com/documentation/AppKit/NSStatusBar) — AppKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/873F40BE-101A-4C0D-99F0-F5C7CE7B47A3/10046_wide_250x141_1x.jpg) 提升 iPad 应用的设计 ](https://developer.apple.com/videos/play/wwdc2025/208)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Change-log)

日期| 变更
---|---
2025年6月9日| 添加了 iPadOS 中菜单栏的指导。
