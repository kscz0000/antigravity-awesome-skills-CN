---
title: "Pointing devices | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/pointing-devices

# 指点设备

用户可以使用触控板或鼠标等指点设备来导航界面并发起操作。

![A sketch of an arrow-shaped pointer, suggesting use of a mouse or trackpad. The image is overlaid with rectangular and circular grid lines and is tinted purple to subtly reflect the purple in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/d62ce652f0470403da6dfbad1b1ad2b0/inputs-pointing-devices-intro%402x.png)

用户很看重指点设备提供的精确性和灵活性。在 Mac 上，用户通常期望将指点设备与键盘配合使用来操作应用和系统。在 iPad 和 Apple Vision Pro 上，指点设备为用户提供了一种额外的交互方式，但不会取代触控、视线或手势。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Best-practices)

**对鼠标和触控板手势的响应要保持一致。** 用户期望大多数手势在整个系统中的行为方式相同，无论他们使用的是哪款应用或游戏。例如在 Mac 上，用户依赖"在页面间滑动"手势在浏览文档页面、网页或图片时都有一样的表现。

**避免重新定义系统级触控板手势。** 即使是使用自定义手势的游戏，用户也期望系统级手势仍然可用；例如，用户期望使用熟悉的手势来唤出 macOS 中的 Dock 或"调度中心"。记住，Mac 用户可以自定义执行系统级操作的手势。

**在应用中提供一致的体验，无论用户使用的是手势、视线、指点设备还是键盘。** 用户期望在多种输入方式之间流畅切换，不想为每种模式或每款应用学习不同的交互方式。

**允许用户使用指针来显示和隐藏自动最小化或淡出的控件。** 例如在 iPadOS 中，用户可以将指针悬停在最小化的 Safari 工具栏上来显示它（指针移开后工具栏会再次最小化）。用户还可以在全屏观看视频时移动指针来显示或隐藏播放控制。

**在用户按住修饰键并与应用中的对象交互时，提供一致的体验。** 例如，如果用户可以按住 Option 键拖动对象来复制它，那么无论是通过触控还是指针拖动，结果都应该是相同的。

## [平台考量](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Platform-considerations)

 _iOS 无额外考量。tvOS 和 watchOS 不支持此功能。_

### [iPadOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#iPadOS)

iPadOS 在传统指针体验的基础上进行了拓展，自动适配当前上下文并提供丰富的视觉反馈，以精准的交互提升生产力并简化触屏设备上的常见任务。iPadOS 指点系统为用户提供了一种额外的交互方式——它不会取代触控。

**在需要时允许在自定义视图中进行多选。** 在 iPadOS 15 及更高版本中，用户可以按住指针并拖动来选择多个项目。当用户这样操作时，指针会扩展为一个可见的矩形来选中它所覆盖的项目。标准的非列表集合视图默认支持此交互；如果想在自定义视图中支持多选，需要自行实现。开发者指南请参阅 [`UIBandSelectionInteraction`](https://developer.apple.com/documentation/UIKit/UIBandSelectionInteraction)。

**仅在能带来价值时才区分指针和手指输入。** 例如，当用户使用指针时，播放滑块可以提供一种额外的方式来定位视频中的位置。在此场景下，用户可以使用指针或触控来拖动播放头，但还可以使用指针精确点击跳转位置。

#### [指针形状与内容效果](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Pointer-shape-and-content-effects)

iPadOS 将指针的外观与其下方元素的行为融为一体，将焦点引向指针所指向的项目。你可以使用系统提供的指针效果，也可以根据自己的需求进行调整。

默认情况下，指针的形状是一个圆形，但当用户将其移动到特定元素或区域上方时，它会显示为系统定义或自定义的形状。例如，当用户将指针移动到文本输入区域上方时，它会自动切换为常见的 I 形光标。

Video with custom controls. 

Content description: A video snippet showing the bottom half of a new event popover in Calendar. At the beginning of the video, the pointer is within the URL field and it uses the I-beam shape. As the pointer moves between the URL and Notes fields, it briefly reverts to its default circular shape; when the pointer enters the Notes field, it uses the I-beam shape again. 

Play 

通过_内容效果_，指针下方的 UI 元素或区域在指针悬停时也可以改变外观。根据内容效果的类型，指针可以保持当前形状，也可以变换成与元素新外观融为一体的形状。

iPadOS 定义了三种内容效果，用于将焦点引导到应用中不同类型的交互元素：高亮、浮起和悬停。

_高亮_效果将指针变为一个半透明的圆角矩形，作为控件的背景，并带有轻微的视差效果。这种微妙的高亮和移动将焦点引导到控件上，同时不会分散用户的注意力。iPadOS 默认将高亮效果应用于栏按钮、标签栏、分段控件和编辑菜单。

Video with custom controls. 

Content description: A video snippet showing a small area at the bottom of a Photos window. Nature photos that show purple flowers, rocks in a stream, and grass are visible just above the tab bar, which shows the Photos and For You tabs. At the beginning of the video, the Photos tab is highlighted. Because bar items receive the highlight effect, the pointer becomes the highlighted rounded rectangle that surrounds the tab's glyph and title. The highlighted rounded rectangle slides from one tab to the other as the pointer moves. 

Play 

_浮起_效果将轻微的视差与浮起的外观相结合，使元素看起来像是漂浮在屏幕上方。当指针在元素下方淡出时，iPadOS 通过放大元素、在下方添加阴影并在上方添加柔和的镜面高光来营造浮起的视觉效果。iPadOS 默认将浮起效果应用于应用图标和"控制中心"中的按钮。

Video with custom controls. 

Content description: A video snippet showing the left end of the Dock in front of the Home Screen. From the left, the visible app icons are Messages, Safari, Music, Mail, and Files. As the pointer moves across the first three icons from the left, it disappears beneath each icon in turn, lifting it slightly and letting it return to its original position before moving to the next icon. 

Play 

_悬停_是一种通用效果，允许你在指针移过元素时对其应用自定义的缩放、着色或阴影值。悬停效果将你自定义的值组合起来以聚焦项目，但不会改变默认的指针形状。

Video with custom controls. 

Content description: A video snippet showing an alert floating above the top half of a new event popover in Calendar. The alert contains text that reads Are you sure you want to discard this new event? and a button titled Discard Changes. As the pointer moves into the alert button, the button background darkens. 

Play 

#### [指针附件](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Pointer-accessories)

指针附件是帮助用户理解如何使用指针与当前 UI 元素交互的视觉指示器。例如，当指针接近一个可调整大小的元素时，可能会显示小箭头来表示该元素允许沿某个轴向调整大小。

与指针形状和内容效果不同，附件是辅助项，可以与任何指针组合使用来传达附加信息。开发者指南请参阅 [`UIPointerAccessory`](https://developer.apple.com/documentation/UIKit/UIPointerAccessory)。

**使用清晰、简洁的图片来创建自定义附件。** 指针附件很小，因此必须创建一个在不过多使用细节的情况下就能传达指针交互含义的图像。

**考虑使用附件过渡来表示元素状态或行为的变化。** 除了对指针附件的出现和消失进行动画处理外，系统还会对附件形状和位置的过渡进行动画处理，这些过渡可以伴随内容效果。例如，你可以通过将指针附件从 `plus` 符号过渡到 `circle.slash` 符号来表示添加操作已不可用。

#### [指针磁吸](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Pointer-magnetism)

iPadOS 通过让元素看起来吸引指针来帮助用户使用指针精确定位元素。当用户将指针移近元素或向元素方向快速滑动指针时，会体验到这种磁吸效果。

当用户将指针移近元素时，系统会在指针到达元素的点击区域时就开始改变指针的形状。由于元素的点击区域通常会超出其可见边界，指针会在看起来接触到元素之前就开始变换形状，从而营造出元素将指针"吸"过来的视觉效果。

Video with custom controls. 

Content description: A video snippet showing an area at the bottom of Clock. The World Clock tab is selected and clock images and information for San Francisco, New York, and London are partially visible in the window. As the pointer moves in the tab bar, its highlighted rounded rectangle appearance seems to show a slight resistance as it slides from the World Clock tab to the Alarm tab and back again. 

Play 

当用户向元素方向快速滑动指针时，iPadOS 会分析指针的轨迹来找出最可能的目标元素。当指针路径上有元素时，系统会利用磁吸效果将指针拉向元素中心。

iPadOS 默认将磁吸效果应用于使用浮起效果的元素（如应用图标）和使用高亮效果的元素（如栏按钮），但不应用于使用悬停效果的元素。因为支持悬停的元素不会改变默认指针形状，添加磁吸效果可能会让人感到突兀，甚至让用户觉得失去了对指针的控制。

系统还将磁吸效果应用于文本输入区域，这可以帮助用户在选择文本时避免因意外的垂直移动而跳到另一行。

#### [标准指针和效果](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Standard-pointers-and-effects)

**尽可能支持系统提供的内容效果。** 用户会很快习惯在整个系统中看到的内容效果，并且通常期望这些效果在他们使用的每款应用中都有效。为提供一致的用户体验，你的交互应与每种效果的设计意图保持一致。具体来说：

  * 对透明背景的小型元素使用高亮。

  * 对不透明背景的小型元素使用浮起。

  * 对大型元素使用悬停，并根据需要自定义缩放、着色和阴影属性（指南请参阅[自定义指针](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Customizing-pointers)）。



**对标准按钮和文本输入区域优先使用系统提供的指针外观。** 当指针的行为符合用户的预期时，用户会对你的应用感到更加舒适。

**在交互元素周围添加内边距来创建舒适的点击区域。** 你可能需要通过实验来确定元素点击区域的合适大小。如果点击区域太小，用户会觉得与该元素交互时需要格外精确。反之，如果点击区域太大，用户会觉得要花很大力气才能将指针从元素上移开。一般来说，对于带有边框的元素，在其周围添加约 12 点的内边距效果不错；对于没有边框的元素，在其可见边缘周围添加约 24 点的内边距效果不错。

![An illustration of a button that has a filled, rounded-rectangle bezel. The button is centered on top of a shaded rectangle that extends beyond the button by the same distance on all sides. Centered on each side, a callout indicates that the padding between the button and each edge of the shaded rectangle is 12 points.](https://docs-assets.developer.apple.com/published/3993cfe0b8ec1f79e7c27496d92b240e/padding-for-button-with-bezel%402x.png)

![An illustration of a symbol centered on top of a shaded rectangle that extends beyond the symbol by the same distance on all sides. Centered on each side, a callout indicates that the padding between the symbol and each edge of the shaded rectangle is 24 points.](https://docs-assets.developer.apple.com/published/58bee8289c0508cc5b9e83f030925cb6/padding-for-glyph%402x.png)

![An illustration of a button without a bezel, centered on top of a shaded rectangle that extends beyond the button by the same distance on all sides. Centered on each side, a callout indicates that the padding between the button and each edge of the shaded rectangle is 24 points.](https://docs-assets.developer.apple.com/published/5a79ca3d0a9d4bbd3bf71c23bf8c5da3/padding-for-button-without-bezel%402x.png)

**为自定义栏按钮创建连续的点击区域。** 如果栏中相邻按钮的点击区域之间存在间隙，当指针在按钮之间移动时会短暂恢复默认形状，这会带来令人分心的视觉闪烁。

**为接受浮起效果的非标准元素指定圆角半径。** 使用系统提供的浮起效果时，指针会在淡出时变换为与元素形状匹配的形状。默认情况下，指针使用系统定义的圆角半径变换为圆角矩形。如果你的元素是其他形状——例如圆形——你需要提供半径，以便指针能流畅地动画变换为该元素的形状。开发者指南请参阅 [`UIPointerShape.roundedRect(_:radius:)`](https://developer.apple.com/documentation/UIKit/UIPointerShape-swift.enum/roundedRect\(_:radius:\))。

#### [自定义指针](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Customizing-pointers)

**对行为类似标准元素的自定义元素，优先使用系统提供的指针效果。** 当自定义元素的行为类似标准元素时，用户通常期望使用熟悉的指针交互方式。例如，如果自定义工具栏中的按钮没有使用标准的高亮效果，用户可能会认为它们出了问题。

**在整个应用中以一致的方式使用指针效果。** 例如，如果你的应用帮助用户绘图，那么每个绘图区域都应提供相似的指针体验，这样用户可以将在一个区域获得的经验应用到其他区域。

**避免创建无意义的指针和内容效果。** 用户会注意到指针或其下方 UI 元素外观的变化，并期望这些变化是有用的。纯粹装饰性的指针效果不仅没有实际价值，还会分散甚至惹恼用户。

**保持自定义指针形状简洁。** 理想情况下，指针的形状应该暗示用户在当前上下文中可以执行的操作，同时不过分引人注目。如果用户不能立即理解你的自定义指针形状，他们很可能会浪费时间去琢磨这个形状的含义。

**考虑通过显示提供有用信息的自定义注释来增强指针体验。** 例如，你可以在用户将指针悬停在图表区域上时显示 X 和 Y 值。Keynote 使用注释来显示可调整大小图像的当前宽度和高度。

![An illustration of a custom pointer hovering over a resize handle on the edge of a shaded rectangle. Above the pointer is a small annotation that displays the image's width and height values against a dark background.](https://docs-assets.developer.apple.com/published/291aebad59eee8712e94047fcca4e7cf/useful-pointer-annotation%402x.png)

**避免在指针上显示说明性文字。** 显示说明性文字的指针会让应用显得复杂且难用。与其提供说明，不如在界面中优先考虑清晰和简洁，让用户无论使用指针还是触屏都能快速理解如何使用你的应用。

**在定义自定义悬停效果时，考虑阴影、缩放和元素间距的相互作用。** 一般来说，缩放应保留给那些增大后不会挤占附近空间的元素。例如，缩放不适合用于表格行，因为一行无法在不与相邻行重叠的情况下扩展。对于周围空间有限的元素，考虑使用包含着色但不包含缩放和阴影的悬停效果。请注意，单独使用阴影而不配合缩放效果不佳，因为未缩放的元素即使有阴影暗示它浮在屏幕上方，也不会看起来更接近用户。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#macOS)

macOS 支持广泛的鼠标和触控板标准交互，用户可以自定义这些交互。例如，当点击或手势不是与内容交互的主要方式时，用户通常可以根据当前工作流程将其开启或关闭。用户还可以选择鼠标或触控板的特定区域来触发辅助点击，并为特定手势选择特定的手指组合和动作。

点击或手势| 预期行为| 鼠标| 触控板  
---|---|---|---  
主点击| 选择或激活项目，如文件或按钮。| ●| ●  
辅助点击| 显示上下文菜单。| ●| ●  
滚动| 在视图中上下左右移动内容。| ●| ●  
智能缩放| 放大或缩小内容，如网页或 PDF。| ●| ●  
在页面间滑动| 在单独显示的页面之间前进或后退导航。| ●| ●  
在全屏应用间滑动| 在全屏应用和桌面空间之间前进或后退导航。| ●| ●  
调度中心（双指双击鼠标或三指/四指在触控板上向上滑动）| 激活调度中心。| ●| ●  
查询和数据检测器（单指用力点按或三指点按）| 在所选内容上方显示查询窗口。| | ●  
轻点来点按| 使用轻点而非点击来执行主点击操作。| | ●  
用力点按| 点按后用力按压以在所选内容上方显示"快速查看"窗口或查询窗口。施加不同力度以影响压力感应控件，如变速媒体控制。| | ●  
放大或缩小（双指捏合）| 放大或缩小。| | ●  
旋转（双指做圆弧运动）| 旋转内容，如图像。| | ●  
通知中心（从触控板边缘滑动）| 显示通知中心。| | ●  
App Exposé（三指或四指向下滑动）| 在 Exposé 中显示当前应用的窗口。| | ●  
启动台（拇指和三指捏合）| 显示启动台。| | ●  
显示桌面（拇指和三指张开）| 将所有窗口滑开以显示桌面。| | ●  
  
#### [指针](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Pointers)

macOS 提供多种标准指针样式，你的应用可以使用它们来传达界面元素的交互状态或拖动操作的结果。

指针| 名称| 含义| AppKit API  
---|---|---|---  
![A pointer that resembles a diagonal arrow pointing up and to the left.](https://docs-assets.developer.apple.com/published/5be2c381c17d5d868866b3a5de1013f8/pointers-arrow%402x.png)| 箭头| 用于选择和与内容及界面元素交互的标准指针。| [`arrow`](https://developer.apple.com/documentation/AppKit/NSCursor/arrow)  
![A closed, gloved hand.](https://docs-assets.developer.apple.com/published/6680cdb870edf5364f84a483fd2bead9/pointers-closed-hand%402x.png)| 握拳| 拖动以重新定位视图中的内容显示——例如在"地图"中拖动地图。| [`closedHand`](https://developer.apple.com/documentation/AppKit/NSCursor/closedHand)  
![A pointer arrow with a small menu-like square to the right of the arrow.](https://docs-assets.developer.apple.com/published/0cb033cee3b55bd4be661b28b928fdc1/pointers-contextual-menu%402x.png)| 上下文菜单| 指针下方的内容有可用的上下文菜单。此指针通常仅在按下 Control 键时显示。| [`contextualMenu`](https://developer.apple.com/documentation/AppKit/NSCursor/contextualMenu)  
![A plus symbol.](https://docs-assets.developer.apple.com/published/d55eabe14365af873000aa389e5fad6c/pointers-crosshair%402x.png)| 十字线| 可进行精确的矩形选择，例如在"预览"中查看图像时。| [`crosshair`](https://developer.apple.com/documentation/AppKit/NSCursor/crosshair)  
![A small pointer arrowhead with a circle underneath; the circle contains an Ex.](https://docs-assets.developer.apple.com/published/528819d511869de26beb1fd5008ac773/pointers-disappearing-item%402x.png)| 消失项| 拖动的项目在放下时将消失。如果该项目引用了原始项目，则原始项目不受影响。例如，将邮箱从"邮件"的收藏栏中拖出时，原始邮箱不会被移除。| [`disappearingItem`](https://developer.apple.com/documentation/AppKit/NSCursor/disappearingItem)  
![A small pointer arrowhead with a circle underneath; the circle contains a plus symbol.](https://docs-assets.developer.apple.com/published/ccc7052f9bc6fb302d913633c648adcd/pointers-drag-copy%402x.png)| 拖动复制| 在放下时复制而非移动拖动的项目。在拖动操作期间按住 Option 键时出现。| [`dragCopy`](https://developer.apple.com/documentation/AppKit/NSCursor/dragCopy)  
![A curved arrow, pointing up and to the right.](https://docs-assets.developer.apple.com/published/47dfbfd5f1bf3141dbf875f47446d1fd/pointers-drag-link%402x.png)| 拖动链接| 在拖放操作期间，放下时创建所选文件的替身。替身指向原始文件，原始文件保持不动。在拖动操作期间按住 Option 和 Command 键时出现。| [`dragLink`](https://developer.apple.com/documentation/AppKit/NSCursor/dragLink)  
![Opposing veritcal braces, used to form an insertion marker.](https://docs-assets.developer.apple.com/published/060f443dee8d260a1a1191d7831e36b7/pointers-horizontal-beam%402x.png)| 水平 I 形光标| 可在水平布局中进行文本选择和插入，如 TextEdit 或 Pages 文档。| [`iBeam`](https://developer.apple.com/documentation/AppKit/NSCursor/iBeam)  
![An open, gloved hand.](https://docs-assets.developer.apple.com/published/a5daee642ccc8fb3ac550d176b2d1932/pointers-open-hand%402x.png)| 张开手| 可拖动以重新定位视图中的内容。| [`openHand`](https://developer.apple.com/documentation/AppKit/NSCursor/openHand)  
![A small pointer arrowhead with a do not enter symbol underneath.](https://docs-assets.developer.apple.com/published/2daaf47bef26569f92f30a9016095dde/pointers-operation-not-allowed%402x.png)| 操作不允许| 拖动的项目无法在当前位置放下。| [`operationNotAllowed`](https://developer.apple.com/documentation/AppKit/NSCursor/operationNotAllowed)  
![A gloved hand, with the index finger extended.](https://docs-assets.developer.apple.com/published/25193808b5e72d5983ff26764889718a/pointers-pointing-hand%402x.png)| 指向手| 指针下方的内容是指向网页、文档或其他项目的 URL 链接。| [`pointingHand`](https://developer.apple.com/documentation/AppKit/NSCursor/pointingHand)  
![A horizontal bar with a downward-pointing arrow at its midpoint.](https://docs-assets.developer.apple.com/published/328443ed3b5dd85c84de91a60ed30b43/pointers-resize-down%402x.png)| 向下调整大小| 向下调整窗口、视图或元素的大小或移动它们。| [`resizeDown`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeDown)  
![A vertical bar with a left-pointing arrow at its midpoint.](https://docs-assets.developer.apple.com/published/34113d73f24c003f4b3715e0cef8fbf6/pointers-resize-left%402x.png)| 向左调整大小| 向左调整窗口、视图或元素的大小或移动它们。| [`resizeLeft`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeLeft)  
![A vertical bar with left- and right-pointing arrows extending from its midpoint.](https://docs-assets.developer.apple.com/published/478726bb1a630013de1f77b3bccde9e0/pointers-resize-left-right%402x.png)| 左右调整大小| 向左或向右调整窗口、视图或元素的大小或移动它们。| [`resizeLeftRight`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeLeftRight)  
![A vertical bar with a right-pointing arrow at its midpoint.](https://docs-assets.developer.apple.com/published/6045fce093cc242bf438393155b77992/pointers-resize-right%402x.png)| 向右调整大小| 向右调整窗口、视图或元素的大小或移动它们。| [`resizeRight`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeRight)  
![A horizontal bar with an up-pointing arrow at its midpoint.](https://docs-assets.developer.apple.com/published/34576a4ab42dea114abf11b3ee57a4f8/pointers-resize-up%402x.png)| 向上调整大小| 向上调整窗口、视图或元素的大小或移动它们。| [`resizeUp`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeUp)  
![A horizontal bar with up- and down-pointing arrows extending from its midpoint.](https://docs-assets.developer.apple.com/published/d55d0d01c955105a957231266affb447/pointers-resize-up-down%402x.png)| 上下调整大小| 向上或向下调整窗口、视图或元素的大小或移动它们。| [`resizeUpDown`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeUpDown)  
![Opposing horizontal braces, used to form an insertion marker.](https://docs-assets.developer.apple.com/published/15923a8cac833b5bb1fd69b4a395c4a9/pointers-vertical-beam%402x.png)| 垂直 I 形光标| 可在垂直布局中进行文本选择和插入。| [`iBeamCursorForVerticalLayout`](https://developer.apple.com/documentation/AppKit/NSCursor/iBeamCursorForVerticalLayout)  
  
### [visionOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#visionOS)

在 visionOS 中，用户可以连接外部指点设备或键盘，并在继续使用眼睛和双手的同时使用这两种设备。如果用户注视某个元素然后移动指针，系统会将焦点转移到指针下方的元素。你的应用无需做任何事情来支持此行为。

当连接指点设备时，用户注视的区域决定了指针的上下文。例如，当用户将视线从一个窗口移到另一个窗口时，指针的上下文会无缝切换到新窗口。

Video with custom controls. 

Content description: A recording that shows a pointer moving around, highlighting items, and scrolling content within a Safari window in visionOS. A picture-in-picture window is visible in the bottom left corner of the recording. It shows a person's hand operating a trackpad next to a keyboard outside the field of view. The person's gestures on the trackpad correspond to the pointer movements. 

Play 

当用户使用支持手势的外接指点设备（如触控板或鼠标）时，指针在用户使用手势时会隐藏，以减少视觉干扰。在此场景下，指针会保持隐藏状态，直到用户移动它，此时它会重新出现在用户注视的位置。

## [资源](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Related)

[输入数据](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[键盘](https://developer.apple.com/design/human-interface-guidelines/keyboards)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Developer-documentation)

[Input events](https://developer.apple.com/documentation/SwiftUI/Input-events) — SwiftUI

[Pointer interactions](https://developer.apple.com/documentation/UIKit/pointer-interactions) — UIKit

[Mouse, Keyboard, and Trackpad](https://developer.apple.com/documentation/AppKit/mouse-keyboard-and-trackpad) — AppKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/49/F9A980A7-B00A-4856-9172-FDB610A419E5/3509_wide_250x141_1x.jpg) Design for the iPadOS pointer ](https://developer.apple.com/videos/play/wwdc2020/10640)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Change-log)

日期| 变更内容  
---|---  
2023 年 6 月 21 日| 更新以包含 visionOS 的指南。  
  