---
title: "键盘 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/keyboards

# 键盘

实体键盘是用于输入文本、玩游戏、控制应用等场景的重要输入设备。

![键盘示意图，暗示键盘输入。图片覆盖了矩形和圆形网格线，色调为紫色，微妙地呼应了 Apple 原始六色 Logo 中的紫色。](https://docs-assets.developer.apple.com/published/041dcf36a378d11a3727a6ff04989365/inputs-keyboard-intro%402x.png)

用户可以将实体键盘连接到 Apple Watch 以外的任何设备。Mac 用户通常一直使用实体键盘，iPad 用户也经常使用。许多游戏能很好地配合实体键盘，用户在输入大量文本时也可能更倾向于使用实体键盘而非[虚拟键盘](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)。

键盘用户通常喜欢使用键盘快捷键来加速与应用和游戏的交互。_键盘快捷键_是一个主键与一个或多个修饰键（Control、Option、Shift 和 Command）的组合，映射到特定命令。游戏中的键盘快捷键——称为_按键绑定_——通常由单个按键组成。

Apple 定义了标准键盘快捷键，在系统和大多数应用中保持一致，帮助用户将已有经验迁移到新体验中。一些应用为用户最常用的应用专属命令定义自定义键盘快捷键；大多数游戏定义自定义按键绑定，让用户能快速高效地用键盘控制游戏。相关指引请参阅[游戏控制](https://developer.apple.com/design/human-interface-guidelines/game-controls#Keyboards)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices)

**尽可能支持全键盘控制。** 全键盘控制适用于 iOS、iPadOS、macOS 和 visionOS，让用户能够仅使用键盘来导航和激活窗口、菜单、控件和系统功能。要在你的应用或游戏中测试全键盘控制，请在系统"设置"应用的"辅助功能"区域中将其开启。开发者指引请参阅[在 iOS 应用中支持全键盘控制](https://developer.apple.com/videos/play/wwdc2021/10120/)和 [`isFullKeyboardAccessEnabled`](https://developer.apple.com/documentation/AppKit/NSApplication/isFullKeyboardAccessEnabled)。

重要

虽然 iPadOS 支持在文本栏、文本视图和侧边栏中进行键盘导航，并提供 API 供你在集合视图和其他自定义视图中支持键盘导航，但应避免为按钮、分段控件和开关等控件支持键盘导航。应让用户使用全键盘控制来激活控件、导航到所有屏幕组件，以及执行拖放等基于手势的交互。相关指引请参阅 [iPadOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#iPadOS)；开发者指引请参阅[基于焦点的导航](https://developer.apple.com/documentation/uikit/focus-based_navigation)。

**遵循标准键盘快捷键。** 使用大多数应用时，用户通常期望依赖在其他应用和整个系统中通用的标准键盘快捷键。如果你的应用提供了用户经常执行的独特操作，应优先为其创建[自定义](https://developer.apple.com/design/human-interface-guidelines/keyboards#Custom-keyboard-shortcuts)快捷键，而不是重新定义用户已与其他操作关联的标准快捷键。玩游戏时，用户可能期望使用某些标准键盘快捷键——如 Command–Q 退出游戏——但他们也期望能够修改每个游戏的按键绑定以适应个人操作习惯。相关指引请参阅[游戏控制](https://developer.apple.com/design/human-interface-guidelines/game-controls#Keyboards)。

## [标准键盘快捷键](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

**通常情况下，不要将标准键盘快捷键重新定义为自定义操作。** 当用户熟悉的快捷键在你的应用或游戏中表现不同时，他们会感到困惑。仅在标准快捷键的操作在你的使用场景中没有意义时，才考虑重新定义。例如，如果你的应用不支持文本编辑，就不需要斜体等文本样式命令，因此可以将 Command–I 重新定义为更有意义的操作，如"显示简介"。

用户期望以下每个标准键盘快捷键执行下表中列出的操作。

**主键**| 快捷键| 操作  
---|---|---  
空格键| Command-空格键| 显示或隐藏 Spotlight 搜索栏。  
| Shift-Command-空格键| 因系统而异。  
| Option-Command-空格键| 显示 Spotlight 搜索结果窗口。  
| Control-Command-空格键| 显示特殊字符窗口。  
Tab| Shift-Tab| 反向导航控件。  
| Command-Tab| 在已打开应用列表中切换到最近使用的下一个应用。  
| Shift-Command-Tab| 在已打开应用列表中反向切换（按最近使用排序）。  
| Control-Tab| 将焦点移至对话框中的下一组控件或下一个表格（当 Tab 移至下一个单元格时）。  
| Control-Shift-Tab| 将焦点移至上一组控件。  
Esc| Esc| 取消当前操作或进程。  
Esc| Option-Command-Esc| 打开"强制退出"对话框。  
弹出键| Control-Command-弹出键| 退出所有应用（在更改已保存到已打开文档后）并重新启动电脑。  
| Control-Option-Command-弹出键| 退出所有应用（在更改已保存到已打开文档后）并关闭电脑。  
F1| Control-F1| 切换全键盘控制开或关。  
F2| Control-F2| 将焦点移至菜单栏。  
F3| Control-F3| 将焦点移至 Dock。  
F4| Control-F4| 将焦点移至活动（或下一个）窗口。  
| Control-Shift-F4| 将焦点移至上一个活动窗口。  
F5| Control-F5| 将焦点移至工具栏。  
| Command-F5| 开启或关闭 VoiceOver。  
F6| Control-F6| 将焦点移至第一个（或下一个）面板。  
| Control-Shift-F6| 将焦点移至上一个面板。  
F7| Control-F7| 临时覆盖窗口和对话框中的当前键盘访问模式。  
F8| | 因系统而异。  
F9| | 因系统而异。  
F10| | 因系统而异。  
F11| | 显示桌面。  
F12| | 隐藏或显示 Dashboard。  
重音符 (`)| Command-重音符| 激活最前面应用中的下一个打开窗口。  
| Shift-Command-重音符| 激活最前面应用中的上一个打开窗口。  
| Option-Command-重音符| 将焦点移至窗口抽屉。  
连字符 (-)| Command-连字符| 缩小选区。  
| Option-Command-连字符| 在屏幕缩放开启时缩小。  
左方括号 ([)| Command-左方括号| 左对齐选区。  
右方括号 (])| Command-右方括号| 右对齐选区。  
竖线 (\|)| Command-竖线| 居中对齐选区。  
冒号 (:)| Command-冒号| 显示"拼写"窗口。  
分号 (;)| Command-分号| 查找文档中的拼写错误。  
逗号 (,)| Command-逗号| 打开应用的设置窗口。  
| Control-Option-Command-逗号| 降低屏幕对比度。  
句号 (.)| Command-句号| 取消操作。  
| Control-Option-Command-句号| 提高屏幕对比度。  
问号 (?)| Command-问号| 打开应用的"帮助"菜单。  
正斜杠 (/)| Option-Command-正斜杠| 开启或关闭字体平滑。  
等号 (=)| Shift-Command-等号| 增大选区。  
| Option-Command-等号| 在屏幕缩放开启时放大。  
3| Shift-Command-3| 将屏幕截图捕获为文件。  
| Control-Shift-Command-3| 将屏幕截图捕获到剪贴板。  
4| Shift-Command-4| 将选区截图捕获为文件。  
| Control-Shift-Command-4| 将选区截图捕获到剪贴板。  
8| Option-Command-8| 开启或关闭屏幕缩放。  
| Control-Option-Command-8| 反转屏幕颜色。  
A| Command-A| 选择文档或窗口中的所有项目，或文本栏中的所有字符。  
| Shift-Command-A| 取消选择所有选区或字符。  
B| Command-B| 将所选文本加粗或切换粗体开和关。  
C| Command-C| 将选区复制到剪贴板。  
| Shift-Command-C| 显示"颜色"窗口。  
| Option-Command-C| 复制所选文本的样式。  
| Control-Command-C| 复制选区的格式设置并存储到剪贴板。  
D| Option-Command-D| 显示或隐藏 Dock。  
| Control-Command-D| 在词典应用中显示所选单词的定义。  
E| Command-E| 将选区用于查找操作。  
F| Command-F| 打开"查找"窗口。  
| Option-Command-F| 跳转到搜索栏控件。  
| Control-Command-F| 进入全屏模式。  
G| Command-G| 查找选区的下一个匹配项。  
| Shift-Command-G| 查找选区的上一个匹配项。  
H| Command-H| 隐藏当前运行应用的窗口。  
| Option-Command-H| 隐藏所有其他运行应用的窗口。  
I| Command-I| 将所选文本设为斜体或切换斜体开或关。  
| Command-I| 显示"显示简介"窗口。  
| Option-Command-I| 显示检查器窗口。  
J| Command-J| 滚动到选区。  
M| Command-M| 将活动窗口最小化到 Dock。  
| Option-Command-M| 将活动应用的所有窗口最小化到 Dock。  
N| Command-N| 打开新文档。  
O| Command-O| 显示选择要打开的文档的对话框。  
P| Command-P| 显示"打印"对话框。  
| Shift-Command-P| 显示"页面设置"对话框。  
Q| Command-Q| 退出应用。  
| Shift-Command-Q| 注销当前登录的用户。  
| Option-Shift-Command-Q| 立即注销当前登录的用户（不确认）。  
S| Command-S| 保存新文档或保存文档版本。  
| Shift-Command-S| 复制活动文档或启动"另存为"。  
T| Command-T| 显示"字体"窗口。  
| Option-Command-T| 显示或隐藏工具栏。  
U| Command-U| 给所选文本加下划线或切换下划线开或关。  
V| Command-V| 在插入点粘贴剪贴板内容。  
| Shift-Command-V| 选择性粘贴（如"粘贴为引用"）。  
| Option-Command-V| 将一个对象的样式应用到选区。  
| Option-Shift-Command-V| 在插入点粘贴剪贴板内容，并将周围文本的样式应用到插入的对象。  
| Control-Command-V| 将格式设置应用到选区。  
W| Command-W| 关闭活动窗口。  
| Shift-Command-W| 关闭文件及其关联窗口。  
| Option-Command-W| 关闭应用中的所有窗口。  
X| Command-X| 移除选区并存储到剪贴板。  
Z| Command-Z| 撤销上一个操作。  
| Shift-Command-Z| 重做（当撤销和重做是独立命令而非通过 Command-Z 切换时）。  
右箭头| Command-右箭头| 将键盘布局切换为当前罗马字母布局。  
| Shift-Command-右箭头| 将选区扩展到下一个语义单元，通常是当前行的末尾。  
| Shift-右箭头| 将选区向右扩展一个字符。  
| Option-Shift-右箭头| 将选区扩展到当前单词末尾，再到下一个单词末尾。  
| Control-右箭头| 将焦点移至视图（如表格）中的另一个值或单元格。  
左箭头| Command-左箭头| 将键盘布局切换为当前系统文字布局。  
| Shift-Command-左箭头| 将选区扩展到上一个语义单元，通常是当前行的开头。  
| Shift-左箭头| 将选区向左扩展一个字符。  
| Option-Shift-左箭头| 将选区扩展到当前单词开头，再到上一个单词开头。  
| Control-左箭头| 将焦点移至视图（如表格）中的另一个值或单元格。  
上箭头| Shift-Command-上箭头| 将选区向上扩展到下一个语义单元，通常是文档的开头。  
| Shift-上箭头| 将选区扩展到上一行，到相同水平位置最近的字符边界。  
| Option-Shift-上箭头| 将选区扩展到当前段落开头，再到上一段落开头。  
| Control-上箭头| 将焦点移至视图（如表格）中的另一个值或单元格。  
下箭头| Shift-Command-下箭头| 将选区向下扩展到下一个语义单元，通常是文档的末尾。  
| Shift-下箭头| 将选区扩展到下一行，到相同水平位置最近的字符边界。  
| Option-Shift-下箭头| 将选区扩展到当前段落末尾，再到下一段落末尾（在剪切、复制和粘贴操作中包含段落终止符，如回车键）。  
| Control-下箭头| 将焦点移至视图（如表格）中的另一个值或单元格。  
  
系统还定义了若干键盘快捷键，用于系统的本地化版本、本地化键盘、键盘布局和输入方法。这些快捷键不直接对应菜单命令。

快捷键| 操作  
---|---  
Control-空格键| 在当前和上一个输入源之间切换。  
Control-Option-空格键| 切换到列表中的下一个输入源。  
[修饰键]-Command-空格键| 因系统而异。  
Command-右箭头| 将键盘布局切换为当前罗马字母布局。  
Command-左箭头| 将键盘布局切换为当前系统文字布局。  
  
## [自定义键盘快捷键](https://developer.apple.com/design/human-interface-guidelines/keyboards#Custom-keyboard-shortcuts)

**仅为最常用的应用专属命令定义自定义键盘快捷键。** 用户喜欢对频繁执行的操作使用键盘快捷键，但定义过多新快捷键会让你的应用看起来难以学习。

**以用户期望的方式使用修饰键。** 例如，拖动时按住 Command 键可将多个项目作为一组移动，拖动调整大小时按住 Shift 键可约束为项目的宽高比。此外，按住箭头键可将所选项目以应用定义的最小距离单位移动，直到用户松开按键。

以下是修饰键及其对应符号。

修饰键| 符号| 推荐用法  
---|---|---  
Command| ![风格化三叶草形状轮廓。](https://docs-assets.developer.apple.com/published/43dd468e7f303fbaa3abbf3935292ae2/Keyboard_Command.svg)| 优先将 Command 键用作自定义键盘快捷键的主修饰键。  
Shift| ![向上箭头轮廓。](https://docs-assets.developer.apple.com/published/3a7e5aed7275031a8c41a7fb7789e41f/Keyboard_Shift.svg)| 优先将 Shift 键用作补充相关快捷键的辅助修饰键。  
Option| ![暗示水平翻转的 Z 形线段，顶部对齐一条短横线。](https://docs-assets.developer.apple.com/published/8b064ad029d2012128a6aaeb1322b290/Keyboard_Option.svg)| 谨慎使用 Option 修饰键，仅用于不常用的命令或高级功能。  
Control| ![浅 V 形倒置形状。](https://docs-assets.developer.apple.com/published/5c92c8350588d52ff786bf763b18e9e7/Keyboard_Control.svg)| 避免使用 Control 键作为修饰键。系统在许多系统级功能和快捷键中使用了 Control 键，如移动焦点或截屏。  
  
提示

某些语言需要修饰键来输入特定字符。例如，在法语键盘上，Option-5 生成"{"字符。使用 Command 键作为修饰键通常是安全的，但应避免将额外修饰键与并非所有键盘上都有的字符一起使用。如果必须使用 Command 以外的修饰键，建议仅与字母字符搭配使用。

**按正确顺序列出修饰键。** 如果在自定义快捷键中使用多个修饰键，务必按以下顺序列出：Control、Option、Shift、Command。

**避免将 Shift 添加到使用双字符键上方字符的快捷键中。** 用户已经知道必须按住 Shift 键才能输入双字符键的上方字符，因此直接在快捷键中列出上方字符更为清晰。例如，"隐藏状态栏"的快捷键是 Command-斜杠，而"帮助"的快捷键是 Command-问号，而非 Shift-Command-斜杠。

**让系统根据需要本地化和镜像你的键盘快捷键。** 系统会自动本地化快捷键的主键和修饰键，以支持当前连接的键盘；如果你的应用或游戏切换到从右到左的布局，系统会自动镜像快捷键。相关指引请参阅[从右到左](https://developer.apple.com/design/human-interface-guidelines/right-to-left)。

**避免通过在不相关命令的现有快捷键上添加修饰键来创建新快捷键。** 例如，由于用户习惯使用 Command-Z 撤销操作，将 Shift-Command-Z 用作与撤销和重做无关的命令的快捷键会令人困惑。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/keyboards#Platform-considerations)

 _iOS、iPadOS、macOS 或 tvOS 无额外考量。watchOS 不支持此功能。_

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/keyboards#visionOS)

在 visionOS 中，当用户按住已连接键盘上的 Command 键时，应用的键盘快捷键会显示在快捷键界面中。与 iPad 或 Mac 上应用的[菜单栏菜单](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)组织方式类似，Apple Vision Pro 上的快捷键界面将应用命令显示在用户熟悉的系统定义菜单类别中，如"文件"、"编辑"和"显示"。与菜单栏菜单不同的是，快捷键界面在一个视图中显示所有相关类别，在每个类别中仅列出具有快捷键的可用命令。

**编写描述性的快捷键标题。** 由于快捷键界面以扁平列表显示每个类别中的所有项目，子菜单标题无法为其子项提供上下文。确保每个快捷键标题具有足够的描述性，能够在没有子菜单标题提供额外上下文的情况下传达其操作。开发者指引请参阅 [`discoverabilityTitle`](https://developer.apple.com/documentation/UIKit/UIKeyCommand/discoverabilityTitle)。

**了解用户在 visionOS 应用或游戏中使用实体键盘时会看到叠加层。** 当用户在使用你的 visionOS 应用或游戏时连接实体键盘，系统会显示一个虚拟键盘叠加层，提供输入补全和其他控件。

带有自定义控件的视频。

内容描述：一段录制视频，显示一双手在实体键盘上打字，同时用户在 visionOS 中运行应用。实体键盘上方可见一个虚拟窗口，显示输入的文本和建议。

播放

## [资源](https://developer.apple.com/design/human-interface-guidelines/keyboards#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/keyboards#Related)

[虚拟键盘](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)

[输入数据](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[指向设备](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/keyboards#Developer-documentation)

[`KeyboardShortcut`](https://developer.apple.com/documentation/SwiftUI/KeyboardShortcut) — SwiftUI

[输入事件](https://developer.apple.com/documentation/SwiftUI/Input-events) — SwiftUI

[处理实体键盘上的按键](https://developer.apple.com/documentation/UIKit/handling-key-presses-made-on-a-physical-keyboard) — UIKit

[鼠标、键盘和触控板](https://developer.apple.com/documentation/AppKit/mouse-keyboard-and-trackpad) — AppKit

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/keyboards#Change-log)

日期| 变更  
---|---  
2025 年 6 月 9 日| 将游戏专属按键绑定指引移至"游戏控制"页面。  
2024 年 6 月 10 日| 新增游戏专属指引并进行了结构更新。  
2023 年 6 月 21 日| 更新以包含 visionOS 指引。  
