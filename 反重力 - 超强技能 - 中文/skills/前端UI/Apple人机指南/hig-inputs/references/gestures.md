---
title: "手势 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/gestures

# 手势

人们通过在屏幕上执行手势来与 iOS 和 iPadOS 设备交互。这些手势与内容建立更紧密的个人联系，并增强直接操作的感觉。

![一张手绘的食指在触摸屏上点击的草图，暗示手势交互。图像上叠加了矩形和圆形网格线，并以紫色着色，微妙地反映了原始六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/126393ded1c486236fc7a9feabea30ea/inputs-gestures-intro%402x.png)

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/gestures#Best-practices)

**尽可能使用标准手势。** 人们熟悉标准手势，期望它们在所有应用和游戏中都能工作。当应用重新定义标准手势的含义时，人们会感到困惑。有关标准手势的列表，请参阅[规格说明](https://developer.apple.com/design/human-interface-guidelines/gestures#Specifications)。

**不要阻止系统手势。** 人们依赖系统手势来在系统级别工作。例如，在 iPhone 和 iPad 上，从屏幕底部边缘向上滑动的手势会显示主屏幕；在 iPad 上，从底部角落向上滑动会显示快速备忘录或显示应用库。除了游戏和其他沉浸式体验外，避免将自定义手势与系统保留的边缘滑动冲突。在特定情况下，应用可以通过请求系统推迟其边缘保护手势来处理从屏幕顶部或底部边缘开始的手势（有关开发者指导，请参阅 [`preferredScreenEdgesDeferringSystemGestures`](https://developer.apple.com/documentation/UIKit/UIViewController/preferredScreenEdgesDeferringSystemGestures)）。

**仅在必要时定义自定义手势。** 当你为人们经常执行的、且现有手势未涵盖的专业任务设计自定义手势时（如在游戏或绘图应用中），自定义手势效果最佳。如果你决定实现自定义手势，请确保它：

  * 可发现

  * 易于执行

  * 与其他手势有区别

  * 不是在应用或游戏中执行重要操作的唯一方式




**让自定义手势易于学习。** 在应用中提供帮助人们快速学习和执行自定义手势的时刻，并确保在实际使用场景中测试交互。如果你发现很难用简单的语言和图形来描述一个手势，这可能意味着人们会觉得该手势难以学习和执行。

**使用快捷手势来补充标准手势，而不是替代它们。** 虽然你可以提供自定义手势来快速访问应用的某些部分，但人们也需要简单、熟悉的方式来导航和执行操作，即使这意味着多点击一两次。例如，在支持层级视图导航的应用中，人们期望在顶部工具栏中找到一个返回按钮，让他们只需点击一下就能返回上一个视图。为了帮助加速此操作，许多应用还提供快捷手势——例如从窗口或触摸屏侧面滑动——同时继续提供返回按钮。

**避免与访问系统 UI 的手势冲突。** 多个平台提供用于访问系统行为的手势，如 watchOS 中的边缘滑动或在 visionOS 中翻滚手腕以访问系统覆盖层。避免定义可能与这些交互冲突的自定义手势非常重要，因为人们期望这些控件能一致地工作。在游戏或沉浸式体验的特定情况下，开发者可以通过推迟系统手势来解决此问题。有关更多信息，请参阅 iOS、iPadOS、watchOS 和 visionOS 的平台注意事项。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/gestures#Platform-considerations)

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/gestures#iOS-iPadOS)

除了所有平台支持的[标准手势](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)外，iOS 和 iPadOS 还支持人们期望的其他几种手势。

手势| 常见操作  
---|---  
三指滑动| 启动撤销（左滑）；启动重做（右滑）。  
三指捏合| 复制选中的文本（捏合）；粘贴复制的文本（展开）。  
四指滑动（仅限 iPadOS）| 在应用之间切换。  
摇晃| 启动撤销；启动重做。  
  
**如果同时识别多个手势能增强体验，请考虑允许。** 虽然同时手势在非游戏应用中不太可能有用，但游戏可能包含多个屏幕控件——如操纵杆和发射按钮——人们可以同时操作。有关在 iPadOS 应用中集成触摸屏输入与 Apple Pencil 输入的指导，请参阅 [Apple Pencil 和 Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/gestures#macOS)

人们主要使用[键盘](https://developer.apple.com/design/human-interface-guidelines/keyboards)和鼠标与 macOS 交互。此外，他们可以在 Magic Trackpad、Magic Mouse 或包含触摸表面的[游戏控制器](https://developer.apple.com/design/human-interface-guidelines/game-controls)上执行[标准手势](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/gestures#tvOS)

人们期望使用[标准手势](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)通过兼容的遥控器、Siri Remote 或包含触摸表面的[游戏控制器](https://developer.apple.com/design/human-interface-guidelines/game-controls)来导航 tvOS 应用和游戏。有关指导，请参阅[遥控器](https://developer.apple.com/design/human-interface-guidelines/remotes)。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)

visionOS 支持两类手势：间接手势和直接手势。

人们通过注视对象来定位它，然后从远处——间接地——用手操作该对象来使用_间接_手势。例如，人们可以注视按钮使其获得焦点，然后快速将拇指和食指捏合来选择它。间接手势在任何距离下都能舒适地执行，让人们能够快速在不同对象之间切换焦点并以最小的动作选择项目。

带有自定义控件的视频。

内容描述：一段录制视频，显示 visionOS 中窗口顶部的特写视图。窗口中的按钮被高亮显示。录制右下角可见画中画窗口。它显示一个人的手正在执行间接点击手势。作为对手势的响应，窗口中高亮的按钮被激活。

播放

人们使用_直接_手势来物理触摸交互对象。例如，人们可以通过点击虚拟按键直接在 visionOS 键盘上打字。直接手势在触手可及的范围内效果最佳。因为人们可能会觉得长时间举起手臂很累，所以直接手势最适合偶尔使用。visionOS 还支持所有标准手势的直接版本，让人们可以选择直接或间接地与任何标准组件交互。

带有自定义控件的视频。

内容描述：一段录制视频，显示 visionOS 中一张桌子上垂直堆叠的三个虚拟立方体。一个人的手从右向左移向方块，伸出的手指触摸并推开了中间的方块。中间的方块倒向一边，另一个方块也翻倒在桌面上。

播放

以下是人们在 visionOS 中使用的标准直接手势；有关标准间接手势的列表，请参阅[规格说明](https://developer.apple.com/design/human-interface-guidelines/gestures#Specifications)。

直接手势| 常见用途  
---|---  
触摸| 直接选择或激活对象。  
触摸并按住| 打开上下文菜单。  
触摸并拖动| 将对象移动到新位置。  
双击| 预览对象或文件；在编辑上下文中选择单词。  
滑动| 显示操作和控件；关闭视图；滚动。  
用双手捏合并一起或分开拖动| 放大或缩小。  
用双手捏合并以圆周运动拖动| 旋转对象。  
  
**尽可能支持标准手势。** 例如，一旦有人注视你应用或游戏中的对象，点击很可能是他们想要选择或激活它时首先会做的手势。即使你也支持自定义手势，支持点击等标准手势也能帮助人们快速熟悉你的应用或游戏。

**尽可能同时提供间接和直接交互。** 对于 UI 和按钮等常见组件，优先使用间接手势。将直接手势和自定义手势保留给需要近距离交互的对象或游戏或交互体验中的特定动作。

**避免要求特定的身体动作或姿势作为输入。** 并非所有人都能始终执行特定的身体动作或以特定方式定位自己，无论是由于残疾、空间限制还是其他环境因素。如果你的体验需要运动，请考虑支持替代输入，让人们选择最适合他们的交互方式。

#### [在 visionOS 中设计自定义手势](https://developer.apple.com/design/human-interface-guidelines/gestures#Designing-custom-gestures-in-visionOS)

如果你想为你的体验提供人们无法使用现有系统手势执行的特定交互，请考虑设计自定义手势。要提供此类交互，你的应用需要在 Full Space 中运行，并且必须请求人们许可以访问有关他们手部的信息。有关开发者指导，请参阅 [Setting up access to ARKit data](https://developer.apple.com/documentation/visionOS/setting-up-access-to-arkit-data)。

![一张人在玩 visionOS 游戏时双手执行自定义手势的截图，双手合拢形成心形。](https://docs-assets.developer.apple.com/published/363ecbc8eeb441809f62ae935e13fbdc/visionos-custom-spatial-gesture-happy-beam%402x.png)

**优先考虑舒适度。** 持续测试所有需要自定义手势的交互的人体工程学。即使只需要人们举起手臂一小会儿的自定义交互也会让人身体疲劳，而连续多次重复非常相似的动作会给人们的肌肉和关节带来压力。

**仔细考虑涉及多个手指或双手的复杂自定义手势。** 人们在使用你的应用或游戏时可能并不总是有双手可用。如果你需要更复杂的手势来提供体验，请考虑也提供需要较少动作的替代方案。

**避免需要使用特定手的自定义手势。** 如果人们需要记住使用哪只手来触发自定义手势，这会增加认知负担。这也可能让手部优势明显或肢体差异的人感到你的体验不够友好。

#### [在 visionOS 中处理系统覆盖层](https://developer.apple.com/design/human-interface-guidelines/gestures#Working-with-system-overlays-in-visionOS)

在 visionOS 2 及更高版本中，人们可以注视一只手的手掌并使用手势快速访问主屏幕和控制中心的系统覆盖层。这些交互在系统范围内可用，专门保留用于访问系统覆盖层。

注意

系统覆盖层是 visionOS 2 及更高版本中访问控制中心的默认方法。visionOS 1 的行为（向上看）仍作为辅助功能设置可用。

在设计使用自定义手势或将内容锚定到人们手部的应用和游戏时，考虑与系统覆盖层的交互非常重要。

**为系统覆盖层及其相关手势保留人们手部周围的区域。** 如果可能，不要将内容锚定到人们的手部或手腕。如果你正在设计涉及手部锚定内容的游戏，请将其放置在某人手部直接区域之外，以避免与主屏幕指示器冲突。

![一张人张开手掌向上的插图。手掌上方的虚线圆圈表示为系统覆盖层保留的区域。](https://docs-assets.developer.apple.com/published/de8c04a523a3e225c723c5c09c458e1c/visionos-hand-area-of-focus%402x.png)为与系统覆盖层交互保留的区域。

![一张人张开手掌向上的插图。手掌上方出现一个带有圆形图标的主屏幕指示器按钮。](https://docs-assets.developer.apple.com/published/961d33f07da24b20848f3502d2cea134/visionos-spatial-gesture-home-indicator%402x.png)人注视手掌以显示主屏幕指示器。

![一张人张开手掌向下的插图。手部上方显示带有状态栏的覆盖层。](https://docs-assets.developer.apple.com/published/f1d5a8816f65f35853ccd513355272d8/visionos-spatial-gesture-control-center%402x.png)人转动手以显示状态栏，可以点击打开控制中心。

**在设计沉浸式应用或游戏时考虑推迟系统覆盖层行为。** 在某些情况下，你可能不希望有人注视手掌时出现主屏幕指示器。例如，使用虚拟手或手套的游戏可能希望让人保持在故事世界中，即使他们从不同角度注视手部。在这种情况下，当你的应用在 Full Space 中运行时，你可以选择要求点击来显示主屏幕指示器。有关开发者指导，请参阅 [`persistentSystemOverlays(_:)`](https://developer.apple.com/documentation/SwiftUI/View/persistentSystemOverlays\(_:\))。

![一张人张开手掌向上的图像，从人的视角显示。手掌上方出现一个带有圆形图标的主屏幕指示器按钮。图像背景显示人的周围环境房间。](https://docs-assets.developer.apple.com/published/dc6b4a94633c063ddd432dcc8043cae3/gestures-default-home-indicator%402x.png)共享空间中的默认行为

![一张人张开手掌向上的图像，从人的视角显示。手掌上方出现一个带有圆形图标的主屏幕指示器按钮。图像背景显示完全沉浸空间中的森林。](https://docs-assets.developer.apple.com/published/96cb708d391f1ab78a77d23c7f2e0442/gestures-home-indicator-in-immersive-space%402x.png)Full Space 中的默认行为

![一张人戴着笨重太空服手套张开手掌向上的图像，从人的视角显示。手掌向上，上方没有出现按钮。图像背景显示完全沉浸空间中的星空。](https://docs-assets.developer.apple.com/published/b978fe99b00df892890e1d194f704a83/gestures-fully-immersive-game-with-glove%402x.png)Full Space 中的推迟行为

注意

为 visionOS 1 构建的应用和游戏默认推迟系统覆盖层行为。当有人在你的应用运行于 Full Space 时注视手掌，主屏幕指示器不会出现，除非他们先点击。

**在设计涉及手、手腕和前臂翻滚动作的自定义手势时要小心。** 此特定动作保留用于显示系统覆盖层。由于系统覆盖层始终显示在应用内容之上，且你的应用不知道它们何时可见，因此测试可能与它们冲突的任何自定义手势或内容非常重要。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/gestures#watchOS)

#### [双击](https://developer.apple.com/design/human-interface-guidelines/gestures#Double-tap)

在 watchOS 11 及更高版本中，人们可以使用双击手势滚动列表和滚动视图，以及在垂直标签视图之间前进。此外，你可以将切换或按钮指定为应用中的主要操作，或当系统在智能叠叠中显示你的小组件或实时活动时。在具有主要操作的视图中双击会高亮控件，然后执行操作。系统还支持双击执行你在[通知](https://developer.apple.com/design/human-interface-guidelines/notifications)中提供的自定义操作，它会作用于通知中的第一个非破坏性操作。

**避免在包含列表、滚动视图或垂直标签的视图中设置主要操作。** 这与人们双击时期望的默认导航行为冲突。

**选择人们最常使用的按钮作为视图中的主要操作。** 当双击执行人们最常使用的操作时，在非滚动视图中双击很有帮助。例如，在媒体控制视图中，你可以将主要操作分配给播放/暂停按钮。有关开发者指导，请参阅 [`handGestureShortcut(_:isEnabled:)`](https://developer.apple.com/documentation/SwiftUI/View/handGestureShortcut\(_:isEnabled:\)) 和 [`primaryAction`](https://developer.apple.com/documentation/SwiftUI/HandGestureShortcut/primaryAction)。

## [规格说明](https://developer.apple.com/design/human-interface-guidelines/gestures#Specifications)

### [标准手势](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)

系统提供支持人们在其设备上使用的熟悉手势的 API，无论他们使用触摸屏、visionOS 中的间接手势，还是触控板、鼠标、遥控器或游戏控制器等输入设备。有关开发者指导，请参阅 [Gestures](https://developer.apple.com/documentation/SwiftUI/Gestures)。

手势| 支持平台| 常见操作  
---|---|---  
点击| iOS、iPadOS、macOS、tvOS、visionOS、watchOS| 激活控件；选择项目。  
滑动| iOS、iPadOS、macOS、tvOS、visionOS、watchOS| 显示操作和控件；关闭视图；滚动。  
拖动| iOS、iPadOS、macOS、tvOS、visionOS、watchOS| 移动 UI 元素。  
触摸（或捏合）并按住| iOS、iPadOS、tvOS、visionOS、watchOS| 显示额外的控件或功能。  
双击| iOS、iPadOS、macOS、tvOS、visionOS、watchOS| 放大；如果已放大则缩小；在 Apple Watch Series 9 和 Apple Watch Ultra 2 上执行主要操作。  
缩放| iOS、iPadOS、macOS、tvOS、visionOS| 缩放视图；放大内容。  
旋转| iOS、iPadOS、macOS、tvOS、visionOS| 旋转选中的项目。  
  
有关在特定输入设备上支持其他手势和按钮按下的指导，请参阅[指针设备](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)、[遥控器](https://developer.apple.com/design/human-interface-guidelines/remotes)和[游戏控制](https://developer.apple.com/design/human-interface-guidelines/game-controls)。

## [资源](https://developer.apple.com/design/human-interface-guidelines/gestures#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/gestures#Related)

[反馈](https://developer.apple.com/design/human-interface-guidelines/feedback)

[眼动](https://developer.apple.com/design/human-interface-guidelines/eyes)

[播放触觉反馈](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/gestures#Developer-documentation)

[Gestures](https://developer.apple.com/documentation/SwiftUI/Gestures) — SwiftUI

[`UITouch`](https://developer.apple.com/documentation/UIKit/UITouch) — UIKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/gestures#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/B38CC217-7635-48EF-B8C9-F7954F390CCE/9273_wide_250x141_1x.jpg) 增强你的 UI 动画和过渡 ](https://developer.apple.com/videos/play/wwdc2024/10145)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/C6CDCC79-CCD0-4D2F-A4D1-8FC70DC663DB/8127_wide_250x141_1x.jpg) 为空间输入设计 ](https://developer.apple.com/videos/play/wwdc2023/10073)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/gestures#Change-log)

日期| 变更  
---|---  
2024年9月9日| 添加了在 visionOS 中处理系统覆盖层的指导并进行了组织更新。  
2023年9月15日| 更新规格说明以包含 watchOS 中的双击。  
2023年6月21日| 更改页面标题从触摸屏手势并更新以包含 visionOS 指导。  
