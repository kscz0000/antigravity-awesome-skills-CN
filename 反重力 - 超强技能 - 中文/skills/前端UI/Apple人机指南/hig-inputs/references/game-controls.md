---
title: "Game controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/game-controls

# 游戏控制

精准、直观的游戏控制能提升游戏体验，并增强玩家的沉浸感。

![A sketch of a D-pad control from a game controller, suggesting gameplay. The image is overlaid with rectangular and circular grid lines and is tinted purple to subtly reflect the purple in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/b6c5b8cb6c62c9dd9f5e59ae745d6465/inputs-game-controls-intro%402x.png)

在 Apple 平台上，游戏可以支持实体游戏控制器输入，也可以使用平台默认的交互方式，如触控、遥控器或鼠标键盘。玩家可能更倾向于使用实体游戏控制器，但支持平台默认交互方式同样重要，原因有二：

  * 尽管除 watchOS 外的所有平台都支持实体游戏控制器，但并非每位玩家都能获取到。

  * 玩家更喜欢能使用自己最熟悉的平台交互方式的游戏。




为触达最广泛的用户并在每个平台上提供最佳体验，选择支持的输入方式时请牢记以下因素。

## [触控控制](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls)

对于 iOS 和 iPadOS 游戏，支持触控交互意味着你可以在游戏内容上方提供虚拟控制，同时让玩家通过直接触摸游戏元素来与之交互。你可以使用 [Touch Controller](https://developer.apple.com/documentation/TouchController) 框架为游戏添加这些虚拟控制。请遵循以下指南来打造出色的触控体验。

**判断是否有必要在游戏内容上方显示虚拟控制。** 一般来说，虚拟游戏控制适合提供大量操作或需要玩家控制移动的游戏。但有时，当玩家能直接与游戏内物体交互时，游戏体验会更加沉浸和高效。寻找机会，将操作与游戏内手势关联，从而减少覆盖在游戏内容上的虚拟控制数量。例如，可以考虑让玩家通过点击物体来选中，而不是添加一个虚拟选择按钮。

**将虚拟按钮放在易于触达的位置。** 考虑设备的边界和[安全区域](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas)，同时确保控制位于舒适的位置。确保按钮不与系统功能（如 iPhone 的主屏幕指示器或灵动岛）重叠。将常用按钮放在拇指附近，避开玩家习惯用于移动和视角输入的圆形区域。将菜单等次要控制放在屏幕顶部。

![A graphic that shows ideal placement for touch controls for an iPhone in landscape orientation.](https://docs-assets.developer.apple.com/published/dd0cd40a5b38af26ea97072ecf987b24/game-controls-touch-input-heat-map%402x.png)

将虚拟控制放在拇指可及范围内，能让游戏操作更舒适。

**确保控制足够大。** 常用控制的最小尺寸应为 44×44 pt，菜单等次要控制的最小尺寸应为 28×28 pt，以适应手指操作。

**始终提供可见和触觉按压状态。** 缺少视觉和触觉反馈的虚拟控制会让人感觉迟钝。通过添加视觉按压效果（如发光），帮助玩家确认操作成功——即使手指遮挡了控制也能看到。结合音效和触觉反馈进一步增强体验。相关指南请参阅[触觉反馈](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)。

![A right hand holding an iPhone in landscape orientation. The thumb is pressing down on a virtual button, and the button indicates its press state by increasing its opacity and showing a glow effect around it.](https://docs-assets.developer.apple.com/published/7e633e5b94444a3590ce03fee0d5c3df/game-controls-press-state%402x.png)

**使用能直观表达操作含义的图标。** 选择能视觉化表示按钮功能的图形，例如用武器图标表示攻击。避免使用抽象形状或基于控制器的命名（如 A、X、R1）作为图标，这会让玩家难以理解和记忆控制功能。

![A game controller button with a graphic of a square mapping to a virtual button with a graphic of a hand making a gesture to pick up an object.](https://docs-assets.developer.apple.com/published/d5ba7d4086cc786b24b789e29bfd3507/game-controls-button-to-action%402x.png)

**根据游戏情境显示或隐藏虚拟控制。** 利用触控控制的动态特性，根据玩家当前情境调整屏幕上的控制显示。当某个操作不可用或无关时隐藏控制，减少视觉干扰，帮助玩家专注于重要内容。例如，可以考虑在玩家触摸屏幕之前隐藏移动控制，以减少 UI 对游戏内容的遮挡。

  * 可见控制 
  * 隐藏控制 



![A graphic that shows gameplay with a virtual control to move the character that's more visible while the character is moving.](https://docs-assets.developer.apple.com/published/2c9a0444ff10b37e8e5b54a9036d482e/game-controls-thumbstick-in-motion%402x.png)

摇杆向右移动时，变得更加可见并显示高亮以指示移动方向。

![A graphic that shows gameplay with a virtual control to move the character that's less visible while the character is at rest.](https://docs-assets.developer.apple.com/published/8feb4b819cccdf9a74fa7c3ccd5d6e42/game-controls-thumbstick-at-rest%402x.png)

摇杆静止时，虚拟控制逐渐淡化以表示未使用状态。

**将多个功能合并到单一控制中。** 考虑重新设计那些要求玩家同时或按顺序按下多个按钮的游戏机制。利用双击、长按等手势为同一操作提供不同变体，例如长按可释放特殊强化攻击。对于步行或冲刺等多种操作，考虑将其合并到单一控制中。

![A graphic of a virtual button that supports both single tap and touch and hold gestures.](https://docs-assets.developer.apple.com/published/a92df74768951a55f0f4d406eedb6b4a/game-controls-power-up-action%402x.png)

**将移动和视角控制映射到符合直觉的行为。** 通常，玩家期望在屏幕左侧控制移动，在屏幕右侧控制视角方向。尽可能使用大面积输入区域，最大化玩家对移动和视角方向的控制范围。对于移动控制，建议在玩家手指落点处显示虚拟摇杆，而非固定位置。对于视角控制，建议使用直接触控来平移视角，而非虚拟摇杆。

![A graphic that shows placement for movement controls on the left side of the screen, and placement for camera controls on the right side of the screen.](https://docs-assets.developer.apple.com/published/7bc00774e35dd1839091df6f8c16a830/game-controls-camera-thumbstick-zones%402x.png)

## [实体控制器](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers)

**支持平台的默认交互方式。** 游戏控制器是可选购买的配件，但每台 iPhone 和 iPad 都有触控屏，每台 Mac 都有键盘和触控板或鼠标，每台 Apple TV 都有遥控器，每台 Apple Vision Pro 都能响应用户的手势和眼动。如果你支持游戏控制器，请确保有平台默认交互方式作为备选方案。开发者指南请参阅[为支持游戏控制器的 iOS 游戏添加触控控制](https://developer.apple.com/documentation/GameController/adding-touch-controls-to-games-that-support-game-controllers-in-ios)。

**告知用户游戏控制器的要求。** 在 tvOS 和 visionOS 中，你可以要求使用实体游戏控制器。App Store 会显示"需要游戏控制器"标签，帮助用户识别此类应用。记住，用户可能在任何时候打开你的游戏，即使控制器未连接。如果你的应用需要游戏控制器，请检测其是否存在并友好地提示用户连接。开发者指南请参阅 [`GCRequiresControllerUserInteraction`](https://developer.apple.com/documentation/BundleResources/Information-Property-List/GCRequiresControllerUserInteraction)。

**自动检测控制器是否已配对。** 无需让玩家手动设置实体游戏控制器，你可以自动检测控制器是否已配对并获取其配置。开发者文档请参阅 [Game Controller](https://developer.apple.com/documentation/GameController)。

![An illustration of a game controller with callouts that indicate the locations of the controller's triggers, shoulder buttons, directional pad, and thumbsticks.](https://docs-assets.developer.apple.com/published/40b70c72921efd92b91da0453533baaa/game-controls-controller-anatomy%402x.png)

**根据连接的游戏控制器自定义屏幕内容。** 为简化游戏代码，Game Controller 框架根据控制器元素的位置为其分配标准名称，但实际游戏控制器上的颜色和符号可能不同。在界面中引用控制或显示相关内容时，请使用所连接控制器的标签方案。开发者指南请参阅 [`GCControllerElement`](https://developer.apple.com/documentation/GameController/GCControllerElement)。

**将控制器按钮映射到符合预期的 UI 行为。** 在游戏过程中，玩家期望以符合所用平台习惯的方式导航游戏 UI。非游戏状态下，请在所有 Apple 平台上遵循以下约定：

按钮| 预期 UI 行为  
---|---  
A| 激活控件  
B| 取消操作或返回上一屏  
X| —  
Y| —  
左肩键| 向左导航到不同屏幕或区域  
右肩键| 向右导航到不同屏幕或区域  
左扳机键| —  
右扳机键| —  
左/右摇杆| 移动选择  
方向键| 移动选择  
Home/Logo| 系统控制保留  
菜单键| 打开游戏设置或暂停游戏  
  
**支持多个已连接的控制器。** 如果连接了多个控制器，请使用与玩家当前正在使用的控制器匹配的标签和图标。如果你的游戏支持多人游戏，在引用特定玩家的控制器时请使用相应的标签和符号。如果需要引用多个控制器上的按钮，可以考虑将它们列在一起。

**优先使用符号而非文字来表示游戏控制器元素。** Game Controller 框架为大多数元素提供了 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)，包括各种品牌游戏控制器上的按钮。使用符号而非文字描述对不熟悉控制器的玩家尤其有帮助，因为他们无需在游戏过程中费力寻找特定的按钮标签。

![A screenshot of the SF Symbols app showing symbols in the Gaming category.](https://docs-assets.developer.apple.com/published/c76627e659aa17ab46a638437cc5d33c/game-controls-sf-symbols-gaming-category%402x.png)

## [键盘](https://developer.apple.com/design/human-interface-guidelines/game-controls#Keyboards)

键盘玩家喜欢使用快捷键来加速与应用和游戏的交互。

**优先使用单键命令。** 单键命令通常更易于执行且速度更快，尤其是在同时使用鼠标或触控板时。例如，你可以使用菜单项的首字母作为快捷键，如 I 对应 Inventory（物品栏）或 M 对应 Map（地图）；也可以将游戏的主要操作映射到空格键，利用该键较大的面积优势。

**使用 Apple 键盘测试键位绑定的舒适度。** 例如，如果某个键位绑定在非 Apple 键盘上使用了 Control 键（^），考虑将其重新映射到 Apple 键盘上的 Command 键（⌘）。在 Apple 键盘上，Command 键紧邻空格键，当玩家使用 W、A、S、D 键时特别方便触达。

**考虑按键的邻近关系。** 例如，如果玩家使用 W、A、S、D 键进行导航，可以考虑使用附近的按键定义其他高频操作。同样，如果一组操作密切相关，将它们映射到物理位置相近的按键上效果会很好，例如使用数字键来对应物品栏分类。

**允许玩家自定义键位绑定。** 尽管玩家通常期望有合理的默认设置，但许多人需要根据个人舒适度和游戏风格来自定义键位绑定。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/game-controls#Platform-considerations)

 _iOS、iPadOS、macOS 和 tvOS 无额外考量。watchOS 不支持此功能。_

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/game-controls#visionOS)

**将空间游戏控制器行为与手部输入对齐。** 除了支持多种无线游戏控制器外，你的 visionOS 游戏还可以支持空间游戏控制器，如 PlayStation VR2 Sense 控制器。让玩家以与手部交互类似的方式使用控制器与游戏互动。具体来说，支持注视物体并按下控制器的左或右扳机键进行间接交互，或伸出双手并按下左或右扳机键进行直接交互。更多信息请参阅 [visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)。

## [资源](https://developer.apple.com/design/human-interface-guidelines/game-controls#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/game-controls#Related)

[游戏设计](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)

[手势](https://developer.apple.com/design/human-interface-guidelines/gestures)

[键盘](https://developer.apple.com/design/human-interface-guidelines/keyboards)

[触觉反馈](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/game-controls#Developer-documentation)

[为 Apple 平台创建游戏](https://developer.apple.com/games/)

[Touch Controller](https://developer.apple.com/documentation/TouchController)

[Game Controller](https://developer.apple.com/documentation/GameController)

#### [视频](https://developer.apple.com/design/human-interface-guidelines/game-controls#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/2DB746B8-E0B0-4ED1-B250-902DB7A0F3E7/9196_wide_250x141_1x.jpg) 为 Apple 平台设计高级游戏 ](https://developer.apple.com/videos/play/wwdc2024/10085)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/AD3141F9-6984-4328-9388-551C8677F6A2/4973_wide_250x141_1x.jpg) 深入了解虚拟和实体游戏控制器 ](https://developer.apple.com/videos/play/wwdc2021/10081)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/51863C09-0E96-4230-91A3-B85E950FBF3D/9205_wide_250x141_1x.jpg) 探索 visionOS 中的游戏输入 ](https://developer.apple.com/videos/play/wwdc2024/10094)

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/game-controls#Change-log)

日期| 变更内容  
---|---  
2025 年 6 月 9 日| 更新了触控控制最佳实践，更新了游戏控制器 UI 映射，并新增了 visionOS 中空间游戏控制器支持的指南。  
2024 年 6 月 10 日| 新增了支持触控控制的指南，并将标题从"Game controllers"更改为当前名称。  
