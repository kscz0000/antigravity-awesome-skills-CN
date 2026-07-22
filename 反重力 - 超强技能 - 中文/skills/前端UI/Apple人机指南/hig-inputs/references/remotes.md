---
title: "遥控器 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/remotes

# 遥控器

Siri Remote 是 Apple TV 的主要输入方式，帮助人们从房间另一端感觉与屏幕内容相连。

![一张 Apple TV 遥控器的草图，暗示与屏幕内容的交互。图像上叠加了矩形和圆形网格线，并以紫色着色，微妙地反映了原始六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/04cb8e9dcd1006a14957bda7627222ad/inputs-remotes-intro%402x.png)

除了几个特定按钮外，Siri Remote 结合了点击板和触摸表面，支持人们用来导航 tvOS 应用、浏览频道和内容、播放和暂停媒体以及进行选择等熟悉手势，如滑动和按压。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices)

**优先使用标准手势执行标准操作。** 除非人们正在积极玩游戏，否则他们期望遥控器在他们使用的每个应用中以标准方式工作。重新定义或重新定义标准遥控器行为会导致混淆并增加体验的复杂性。有关指导，请参阅[手势](https://developer.apple.com/design/human-interface-guidelines/remotes#Gestures)。

**与 tvOS 焦点体验保持一致。** [焦点体验](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection)在人们与他们正在查看的内容之间建立强有力的联系。通过确保以人们熟悉的方式将手势与焦点体验结合使用，在应用中加强这种联系，例如始终沿与手势相同的方向移动焦点。

**提供清晰的反馈，向人们展示在应用中执行手势时会发生什么。** 例如，轻轻将拇指放在遥控器上会向人们展示向下滑动的位置，以便他们可以显示信息区域。

**仅在应用中有意义时定义新手势。** 在游戏过程中，例如，自定义手势可以是体验的有趣部分。在大多数其他情况下，人们期望使用标准手势，可能不喜欢必须发现或记住新手势。

**区分按压和点击，并避免响应意外点击。** 按压是一种有意的操作，非常适合选择按钮、确认选择和在游戏过程中启动操作。点击手势适合导航或显示额外信息，但请记住，当人们将拇指放在遥控器上、拿起它、移动它或递给别人时，可能会导致意外点击，因此在实时视频播放期间避免响应点击通常效果很好。

**考虑使用点击位置来辅助导航或游戏。** 遥控器可以区分触摸表面上的上、下、左、右点击手势。仅当在应用上下文中有意义且这种行为直观且可发现时，才响应位置点击。

**在几乎所有情况下，当人们按下返回按钮时打开当前屏幕的父级。** 在应用或游戏的顶层，父级是 Apple TV 主屏幕；在应用内，父级由应用层次结构定义，不一定是上一个屏幕。此标准行为的例外是当人们正在积极玩游戏时，此时很容易意外重复按下返回按钮。为避免在此场景中中断游戏，通过打开游戏内暂停菜单来响应返回按钮，让人们使用不同的交互导航回游戏的主菜单。当游戏内暂停菜单打开时，通过关闭菜单并恢复游戏来响应返回按钮按下。请注意，人们按住返回按钮可从任何位置前往主屏幕。有关指导，请参阅[按钮](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons)。

**在媒体播放期间正确响应播放/暂停按钮。** 在播放音乐或视频时，人们期望按下播放/暂停按钮来播放、暂停或恢复播放。

## [手势](https://developer.apple.com/design/human-interface-guidelines/remotes#Gestures)

点击板的触摸表面检测滑动和按压。

**滑动。** 滑动让人们可以轻松滚动大量项目，动作开始快然后根据滑动强度减慢。当人们在遥控器边缘向上或向下滑动时，他们可以非常快速地浏览项目。

**按压。** 人们按压以激活控件或选择项目。此外，人们在滑动前按压以激活擦洗模式。

## [按钮](https://developer.apple.com/design/human-interface-guidelines/remotes#Buttons)

确保你的应用或游戏以以下方式响应特定按压。

按钮或区域| 应用中的预期行为| 游戏中的预期行为  
---|---|---  
触摸表面（滑动）| 导航。更改焦点。| 执行方向键行为。  
触摸表面（按压）| 激活控件或项目。深入导航。| 执行主按钮行为。  
返回| 返回上一个屏幕。退出到 Apple TV 主屏幕。| 暂停/恢复游戏。返回上一个屏幕、退出到游戏主菜单或退出到 Apple TV 主屏幕。  
播放/暂停| 激活媒体播放。暂停/恢复媒体播放。| 执行次要按钮行为。跳过介绍视频。  
  
## [兼容遥控器](https://developer.apple.com/design/human-interface-guidelines/remotes#Compatible-remotes)

某些与 Apple TV 兼容的遥控器包含用于浏览直播电视或其他基于频道的内容的按钮。例如，遥控器可能包含人们可以用来打开电子节目指南（EPG）的按钮，以及他们可以用来浏览指南或更换频道的其他按钮。有关开发者指导，请参阅 [Providing Channel Navigation](https://developer.apple.com/documentation/TVServices/providing-channel-navigation)；有关设计指导，请参阅 [EPG 体验](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#EPG-experience)。

**如果你的直播观看应用提供 EPG，以人们期望的方式响应遥控器的 EPG 浏览按钮。** 当人们按下"指南"或"浏览"按钮时，他们期望你的 EPG 打开。当他们查看你的 EPG 时，人们期望通过按下"向上翻页"或"向下翻页"按钮来浏览它。在人们浏览 EPG 时避免以其他方式响应这些按钮。在 Siri Remote 和兼容遥控器上，人们还可以点击触摸表面的上部或下部区域来浏览 EPG。如果你的应用不支持 EPG 体验，系统会将这些按钮按下路由到观众设备上的默认指南应用。

**当你的内容播放时，通过更换频道来响应兼容遥控器的"向上翻页"或"向下翻页"按钮。** 人们期望这些按钮在切换查看内容和浏览 EPG 时表现不同。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/remotes#Platform-considerations)

_iOS、iPadOS、macOS、visionOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/remotes#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/remotes#Related)

[使用 Siri Remote 或 Apple TV Remote 配合 Apple TV](https://support.apple.com/en-us/HT205305)
