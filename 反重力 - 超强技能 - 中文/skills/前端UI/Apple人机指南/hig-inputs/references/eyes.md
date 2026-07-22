---
title: "Eyes | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/eyes

# 视线

在 visionOS 中，用户注视虚拟对象来将其选定为可交互的目标。

![一只人眼的草图。画面上叠加了矩形和圆形网格线，并以紫色着色，微妙地呼应了最初六色 Apple 标志中的紫色。](https://docs-assets.developer.apple.com/published/126393ded1c486236fc7a9feabea30ea/inputs-eyes-intro%402x.png)

当用户注视某个交互元素时，visionOS 会高亮显示它，提供视觉反馈帮助用户确认这就是他们想要操作的对象。这种视觉反馈，即_悬停效果_，告知用户可以使用[间接手势](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)（如轻点）与该元素进行交互。

带自定义控件的视频。

内容描述：一段设置应用的录屏，展示当视线从一个设置项移向另一个时，悬停效果依次出现在各个设置项上。

播放

在某些情况下，系统会在用户注视某个组件后自动展开其视图。例如，当用户注视标签栏时，整个标签栏会调整大小，在每个标签旁边显示文字标签。在这种场景下，单个标签也会在标签栏展开前高亮显示，以便用户在显示文字标签之前就选中它。另一个例子是，按钮可以在用户注视时显示工具提示。

重要提示

为保护用户隐私，visionOS 不会在用户轻点之前直接提供其注视位置的信息。当你使用系统提供的组件时，visionOS 会在用户轻点组件时自动通知你。开发者指南请参阅 [Adopting best practices for privacy and user preferences](https://developer.apple.com/documentation/visionOS/adopting-best-practices-for-privacy)。

visionOS 还支持_焦点效果_，帮助用户使用键盘或游戏手柄等连接的输入设备在应用和系统中导航。焦点效果与悬停效果无关；详情请参阅[焦点与选择](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices)

**始终为用户提供多种与应用交互的方式。** 设计应用时应支持辅助功能，让用户能以个性化方式与设备交互。相关指南请参阅[辅助功能](https://developer.apple.com/design/human-interface-guidelines/accessibility)。

**注重视觉舒适度。** 确保用户需要使用的对象在其[视野范围](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Field-of-view)内，帮助用户完成主要任务。当你的应用或游戏在共享空间或全空间中运行时，系统会自动将用户打开的第一个窗口或3D体积放置在他们面前方便查看的位置。在全空间中运行时，应用或游戏还可以请求获取用户头部姿态信息，以便更合理地放置3D内容。在所有情况下，避免要求用户进行大范围或跨多个深度层次的快速视线调整，可以提升体验的视觉舒适度。相关指南请参阅[纵深](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Depth)。

**将内容放置在舒适的观看距离上。** 例如，为了帮助用户在长时间阅读或浏览内容时保持舒适，建议将内容放置在至少一米之外。通常情况下，不要将内容放置得离用户太近，除非他们只是短暂查看或交互。

**优先使用标准 UI 组件。** 系统提供的组件在用户注视时会有一致的响应。如果你的自定义组件使用不同的视觉提示来提供反馈，用户会很难学习和记住这些组件的交互方式。

## [让内容易于注视](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see)

**减少视觉干扰。** 当视觉噪音过多时，用户很难找到想要注视的对象。视觉上的运动干扰更大：当用户感知到运动——尤其是在周边视野中——会本能地看向它，导致难以继续注视原本感兴趣的对象。例如，在用户注视的按钮附近显示内容，可能会导致他们不由自主地看向新内容而非按钮。

**在对象周围留出充足空间，让用户更容易注视。** 因为眼睛即使注视一个位置时也会自然地进行微小快速的方向调整，将 UI 对象挤在一起会导致用户在注视其中一个时容易跳到另一个。你可以通过在每个交互项的边界周围至少保留16点的边距，或将项目中心之间的距离保持在至少60点以上，来确保交互项之间有足够的间距。更多布局指南请参阅[布局](https://developer.apple.com/design/human-interface-guidelines/layout)和[空间布局](https://developer.apple.com/design/human-interface-guidelines/spatial-layout)。

**避免使用填满视野的重复图案或纹理。** 在某些情况下，用户的视线可能会锁定在图案或纹理中的不同元素上，使这些元素看起来具有不同的深度。为避免这种效果，考虑将图案用在较小的区域内。

## [鼓励交互](https://developer.apple.com/design/human-interface-guidelines/eyes#Encouraging-interaction)

**考虑使用微妙的视觉提示引导用户注视他们最可能想要的对象。** 例如，将对象放在视野中心附近，或使用柔和的运动、增强的对比度、颜色或大小的变化等技巧来吸引用户注意力，通常效果很好。通常应优先选择引人注意但不刺眼或突兀的提示方式。

**通常，将交互项设计为圆角形状。** 用户的视线倾向于被形状的角吸引，导致难以持续注视形状的中心。交互项的形状越圆润，用户越容易用视线精准定位。

![一个方形按钮。](https://docs-assets.developer.apple.com/published/d60c5b225c91f041c5ef7e273a9219b6/visionos-eyes-sharp-button-incorrect%402x.png)

![圆圈中的 X，表示用法不正确。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![一个圆形按钮。](https://docs-assets.developer.apple.com/published/61afcfc99cebef8a0feae23fc5803edc/visionos-eyes-rounded-button-correct%402x.png)

![圆圈中的对勾，表示用法正确。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

**如果创建的交互组件包含多个元素，务必提供一个整体的包含形状让 visionOS 可以高亮。** 例如，如果一张图片和下方的文字标签组合成一个交互组件，你需要定义一个包含两个元素的自定义区域，使 visionOS 在用户注视任一元素时能高亮整个区域。

## [自定义悬停效果](https://developer.apple.com/design/human-interface-guidelines/eyes#Custom-hover-effects)

在应用或游戏中有需要时，你可以设计一种悬停效果，在用户注视元素时以自定义方式呈现动画，包括系统提供的或自定义的 UI 元素以及 RealityKit 实体。自定义悬停效果可以替代或增强标准效果。

在开始设计自定义悬停效果之前，了解其工作原理很重要。要为某个元素启用自定义悬停效果，你需要为其创建两种状态或外观：一种显示自定义悬停效果，另一种不显示。当用户在应用或游戏中注视该元素时，系统会在你的软件进程之外的流程中应用预设的悬停效果。这意味着你无法得知系统何时应用了自定义悬停效果，也不知道元素在那一刻处于什么状态。自定义悬停效果的进程外特性还意味着它无法执行需要知道用户何时正在注视该元素的代码。

以一个展示自定义悬停效果能做什么和不能做什么的例子来说，假设有一个照片浏览应用，照片的自定义效果会根据用户是否已将该照片添加到收藏来显示不同符号。应用为照片的自定义悬停效果指定相应的符号，系统会在用户注视照片时显示该效果。但悬停效果无法执行收藏操作，因为系统不会在用户注视照片时通知应用。

**优先使用自定义悬停效果来强调或增强体验中的特殊时刻。** 用户已经习惯提供视觉反馈的标准悬停效果，以及标签栏或工具提示中的附加信息，因此自定义悬停效果会格外引人注目。添加过多的自定义悬停效果——或在标准效果足够时使用自定义效果——会削弱设计的影响力，分散用户的注意力，甚至造成视觉不适。

**选择合适的延迟。** 元素的自定义悬停效果可以即时显示、短延迟后显示或稍长延迟后显示，具体取决于你期望用户如何与该元素交互。

  * **无延迟（默认）。** 无延迟显示的自定义悬停效果在效果本身较微妙或邀请交互时特别有用，例如在滑块上显示旋钮。

  * **短延迟。** 考虑使用短延迟，让用户可以在效果出现之前先注视元素并快速交互；例如，标签栏中标签的展开就采用了这种方式。

  * **长延迟。** 如果自定义悬停效果会显示额外信息，如按钮下方出现的工具提示，稍长的延迟通常效果更好，因为大多数用户不需要每次都查看这些额外信息。

**尽量在自定义悬停效果的两种状态中保持元素的一个或多个主要视图不变。** 当悬停效果动画中至少有一个主要视图保持不变时，它提供的视觉稳定性可以帮助用户跟踪元素的过渡变化。如果元素的所有视图在自定义悬停效果期间都发生移动或变化，可能会让用户感到困惑，难以追踪正在发生的事情。

**充分测试自定义悬停效果。** 测试是判断自定义悬停效果是否美观、响应是否恰当、能否让体验生动又不造成干扰的唯一方法。建议佩戴 Apple Vision Pro 测试自定义悬停效果，以便培养如何运用它们来增强体验的直觉。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/eyes#Platform-considerations)

_iOS、iPadOS、macOS、tvOS 和 watchOS 不支持此功能。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/eyes#Resources)

#### [相关内容](https://developer.apple.com/design/human-interface-guidelines/eyes#Related)

[沉浸式体验](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)

[手势](https://developer.apple.com/design/human-interface-guidelines/gestures)

[空间布局](https://developer.apple.com/design/human-interface-guidelines/spatial-layout)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/eyes#Developer-documentation)

[Adopting best practices for privacy and user preferences](https://developer.apple.com/documentation/visionOS/adopting-best-practices-for-privacy) — visionOS

#### [视频](https://developer.apple.com/design/human-interface-guidelines/eyes#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/CA8CE5A1-B113-403F-BCB7-87871B4BBB52/10053_wide_250x141_1x.jpg) Design hover interactions for visionOS ](https://developer.apple.com/videos/play/wwdc2025/303)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/C6CDCC79-CCD0-4D2F-A4D1-8FC70DC663DB/8127_wide_250x141_1x.jpg) Design for spatial input ](https://developer.apple.com/videos/play/wwdc2023/10073)

[![](https://devimages-cdn.apple.com/wwdc-services/images/D35E0E85-CCB6-41A1-B227-7995ECD83ED5/2C47B638-090D-4CBB-9E9E-EBE8114536D9/8132_wide_250x141_1x.jpg) Design considerations for vision and motion ](https://developer.apple.com/videos/play/wwdc2023/10078)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/eyes#Change-log)

日期| 变更内容
---|---
2024年6月10日| 新增自定义悬停效果指南。
2024年3月29日| 新增展示 visionOS 悬停效果的图示。
2023年10月24日| 说明了焦点效果与 visionOS 悬停效果的区别。
2023年6月21日| 新建页面。
