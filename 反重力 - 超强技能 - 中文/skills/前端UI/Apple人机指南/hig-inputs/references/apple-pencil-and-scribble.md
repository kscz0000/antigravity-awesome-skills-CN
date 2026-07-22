---
title: "Apple Pencil and Scribble | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble

# Apple Pencil 和 Scribble

Apple Pencil 让绘图、书写和标记变得轻松自然，同时也是一款出色的指针和 UI 交互工具。

![A sketch of a scribble mark, suggesting drawing with Apple Pencil. The image is overlaid with rectangular and circular grid lines and is tinted purple to subtly reflect the purple in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/48578c745cec42fe322ab69c99575b38/inputs-apple-pencil-and-scribble-intro%402x.png)

Apple Pencil 是一款功能多样、操作直觉的 iPad 工具，在随手记录、素描、绘画、文档标注等场景中提供像素级精度。Scribble 让用户可以使用 Apple Pencil 在任意文本输入框中书写，通过快速、私密的设备端手写识别完成文字输入。

有关 Apple Pencil 的功能和兼容性信息，请参阅 [Apple Pencil](https://www.apple.com/apple-pencil/)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Best-practices)

**支持用户在使用标记工具时的直觉行为。** 大多数人对现实世界的标记工具已有丰富经验，这些认知会影响他们使用 Apple Pencil 操作你的 app 时的预期。要提供令人愉悦的体验，请思考人们如何与传统铅笔、钢笔等标记工具交互，并主动支持用户可能自然尝试的操作。例如，用户通常会想在文档或书籍的页边空白处书写。

**让用户自行选择何时切换 Apple Pencil 和手指输入。** 例如，如果你的 app 支持使用 Apple Pencil 做标记，还应确保 app 的控件也能响应 Apple Pencil，这样用户就不必切换到手指去点击控件。在这种场景下，不支持 Apple Pencil 输入的控件可能看起来毫无响应，给人一种故障或电量不足的错觉。（Scribble 仅支持 Apple Pencil 输入。）

**让 Apple Pencil 接触屏幕的瞬间就能留下笔迹。** 你要让 Apple Pencil 触屏的体验像传统铅笔落纸一样，因此必须避免要求用户先点击按钮或进入特殊模式才能开始书写。

**通过响应用户使用 Apple Pencil 的方式来帮助他们表达。** Apple Pencil 可以感知倾斜角度（altitude）、按压力度（pressure）、方向（azimuth）和[旋转](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Barrel-roll)。利用这些信息来影响笔触效果，例如改变粗细和深浅。在响应压力时保持简洁直觉。例如，通过改变压力来影响连续属性——如墨水不透明度或笔刷大小——会让人感觉很自然。

![An illustration of Apple Pencil tilted up from a horizontal line by 45 degrees.](https://docs-assets.developer.apple.com/published/71e341540baa3fa3bd5bdf01a55cc8a8/apple-pencil-altitude%402x.png)倾斜角度

![An illustration of Apple Pencil drawing a curved line that increases in thickness as more pressure is applied to the tool.](https://docs-assets.developer.apple.com/published/ce6370f2a90cf23b39ee77f7ba64ff02/apple-pencil-pressure%402x.png)压力

![An illustration of Apple Pencil balancing on its tip at the center of a circle that has degree marks around its circumference. A line from the center of the circle to one of the degree marks indicates the angle at which Apple Pencil is tilted.](https://docs-assets.developer.apple.com/published/e3cd83ae350aac7fe4886903d65ac495/apple-pencil-azimuth%402x.png)方位角

**提供视觉反馈以表明与内容的直接关联。** 确保 Apple Pencil 看起来在直接且即时地操控屏幕上的内容。避免让 Apple Pencil 看起来触发了无关的操作，或影响了屏幕上其他区域的内容。

**为左手和右手用户都提供良好的体验。** 避免将控件放置在可能被任意一只手遮挡的位置。如果控件有可能被遮挡，考虑允许用户重新定位它们。

![An illustration of an iPad app that shows a stack of three circular controls on both side edges. A drawing of a person's left hand holding an Apple Pencil is shown at the bottom-left corner of the screen, partially obscuring the controls on that side. The controls on the left edge are grayed out to indicate the original position they no longer occupy, while the controls on the right edge are bright to indicate their final position.](https://docs-assets.developer.apple.com/published/386201ad5a8d093d8c72fc4db57978aa/apple-pencil-controls-moved-right%402x.png)

![An illustration of an iPad app that shows a stack of three circular controls on both side edges. A drawing of a person's right hand holding an Apple Pencil is shown at the bottom-right corner of the screen, partially obscuring the controls on that side. The controls on the right edge are grayed out to indicate the original position they no longer occupy, while the controls on the left edge are bright to indicate their final position.](https://docs-assets.developer.apple.com/published/6b9182644f4624493d4fbe541186a4dc/apple-pencil-controls-moved-left%402x.png)

## [悬停](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Hover)

**利用悬停帮助用户预判 Apple Pencil 触屏后的效果。** 例如，当用户将 Apple Pencil 悬停在屏幕上方时，悬停预览可以显示当前工具将产生的笔迹尺寸和颜色。尽量避免在用户移动 Apple Pencil 靠近或远离屏幕时持续改变预览。随高度变化的预览不太可能让用户更清楚地了解笔迹效果，频繁的视觉变化反而会让人分心。

**避免使用悬停来触发操作。** 与点击按钮或在屏幕上做标记不同，悬停是一个相对不精确的动作，用户不需要关注 Apple Pencil 与屏幕之间的实际距离。你不希望用户仅仅因为将 Apple Pencil 靠近屏幕就不小心触发了操作——尤其是可能需要撤销的破坏性操作。

**在动态值范围内优先展示中间值的预览。** 不透明度或流量等动态属性在光谱的最高或最低端可能难以呈现。例如，以最大压力预览笔刷标记可能会遮挡用户正在书写的区域；相反，以最小压力呈现的标记可能难以辨认，导致预览无法准确反映实际标记效果，甚至不可见。

![An illustration of Apple Pencil hovering slightly above a gray rectangle that represents the screen. A small blue oval beneath the tip represents a preview.](https://docs-assets.developer.apple.com/published/d18ccebb3a51a66f6c6151bc1414d9a1/apple-pencil-preview-small%402x.png)

![An X in a circle to indicate incorrect usage.](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

![An illustration of Apple Pencil hovering slightly above a gray rectangle that represents the screen. A medium blue oval beneath the tip represents a preview.](https://docs-assets.developer.apple.com/published/4c5b24f4381fc1ed83af48f2a7ae3268/apple-pencil-preview-medium%402x.png)

![A checkmark in a circle to indicate correct usage.](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)

![An illustration of Apple Pencil hovering slightly above a gray rectangle that represents the screen. A large blue oval beneath the tip represents a preview.](https://docs-assets.developer.apple.com/published/50d3aa8162579aced9bd752b856b5f6b/apple-pencil-preview-large%402x.png)

![An X in a circle to indicate incorrect usage.](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)

**考虑使用悬停来支持用户标记区域附近的相关交互。** 例如，当用户执行[挤压](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Squeeze)手势或按下外接键盘上的修饰键时，你可以通过显示工具尺寸的上下文菜单来响应悬停。在用户标记的位置附近显示菜单，让他们无需将 Apple Pencil 或手移到屏幕的其他区域就能做出选择。

**优先为 Apple Pencil 而非指针设备显示悬停预览。** 虽然指针设备也能响应悬停手势，但为两种设备提供相同的视觉反馈可能会造成混淆。如果你的 app 合适，可以将悬停预览限定为仅 Apple Pencil 使用。有关开发者指南，请参阅 [Adopting hover support for Apple Pencil](https://developer.apple.com/documentation/UIKit/adopting-hover-support-for-apple-pencil)。

## [双击](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Double-tap)

**在适用的情况下尊重用户对双击手势的设置。** 默认情况下，支持双击手势的 Apple Pencil 会在当前工具和橡皮擦之间切换，但用户可以将该手势设置为在当前工具和上一个工具之间切换、显示或隐藏颜色选择器，或不做任何操作。如果你的 app 支持这些行为，让用户使用他们偏好的手势来执行。如果系统范围的双击设置不适用于你的 app，你仍然可以使用该手势来切换交互模式。例如，提供网格编辑工具的 3D app 可以使用双击在工具的抬高和降低模式之间切换。

**如有必要，为用户提供指定自定义双击行为的方式。** 如果你除了部分或全部默认行为外还提供自定义双击行为，请提供一个控件让用户选择自定义行为模式。用户需要知道自己处于哪种模式；否则，当你的 app 对他们的交互做出不同响应时，他们可能会感到困惑。在这种场景下，确保用户能轻松发现你的 app 支持的自定义行为，但不要默认启用。

**避免使用双击手势执行修改内容的操作。** 在少数情况下，用户可能会意外双击，这意味着他们甚至可能不知道你的 app 执行了该操作。优先使用双击来执行用户容易撤销的操作。尤其要避免使用双击执行可能导致数据丢失的破坏性操作。

## [挤压](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Squeeze)

使用 Apple Pencil Pro 时，用户可以通过挤压来执行操作。你可以设计响应挤压的自定义行为，但请注意，用户可能会选择将挤压手势配置为运行[App 快捷指令](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)而非 app 特定的操作。

注意

挤压手势仅在配对的 iPad 屏幕亮起且 Apple Pencil Pro 未直接接触屏幕时可用。由于挤压在 Apple Pencil Pro 与 iPad 之间存在距离时才能生效，用户可能不一定能看到手势在屏幕上的结果。

**将挤压视为一个快速的单次手势，执行离散而非连续的操作。** 用户有时会用力挤压，因此持续按压或快速多次挤压会让人疲劳。通过响应单次挤压并及时显示结果来帮助用户保持舒适。

**如果使用挤压来显示 app 界面（如上下文菜单），请将其显示在 Apple Pencil Pro 附近。** 在 Apple Pencil Pro 笔尖附近显示挤压结果，可以加强设备与手势之间的关联感，帮助用户保持对任务的专注。

**定义非破坏性且易于撤销的挤压操作。** 与双击手势类似，用户可能会无意中触发挤压手势，因此必须避免使用挤压执行可能导致数据丢失的操作。

## [旋转](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Barrel-roll)

使用 Apple Pencil Pro 做标记时，用户可以通过旋转手势改变标记类型。例如，在"备忘录"中使用 Apple Pencil Pro 高亮内容时，用户可以旋转来调整标记的角度。

**仅使用旋转来修改标记行为，不要用于导航或显示其他控件。** 与双击和挤压不同，旋转自然与标记相关，用于执行界面操作并不合理。

## [Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Scribble)

借助 Scribble 和 Apple Pencil，用户可以在 app 中任何接受文本输入的地方直接书写——无需先点击或切换模式。由于 Scribble 已完全集成到 iPadOS 中，所有 app 默认都可使用。

**让文字输入感觉流畅而轻松。** 默认情况下，Scribble 在所有标准文本组件中均可工作——如文本字段、文本视图、搜索字段和网页内容中的可编辑字段——密码字段除外。如果你的 app 使用自定义文本字段，避免要求用户先点击或选中它才能开始书写。

**在用户可能想要输入文本的所有地方提供 Scribble。** 与使用键盘不同，使用 Apple Pencil 会让人像对待纸张一样对待屏幕。通过在文字输入看起来自然的地方一致地提供 Scribble 来强化这种感知。例如，在"提醒事项"中，用户很自然地会在最后一个项目下方的空白区域书写来创建新提醒，即使该区域并未包含文本字段。有关开发者指南，请参阅 [`UIIndirectScribbleInteraction`](https://developer.apple.com/documentation/UIKit/UIIndirectScribbleInteraction-1nfjm)。

**避免在用户书写时造成干扰。** 某些文本字段行为适合键盘输入，但会破坏 Apple Pencil 提供的自然书写体验。例如，最好避免在用户书写时显示自动补全文本，因为建议内容会在视觉上干扰书写。同样，建议在用户开始书写的瞬间隐藏字段的占位文本，以免输入内容看起来与占位文本重叠。

**用户在文本字段中书写时，确保字段保持静止。** 在某些情况下，文本字段获得焦点时移动是合理的：例如，搜索字段可能会移动以腾出更多空间显示结果。这种移动在用户使用键盘时没问题，但在书写时会让用户感觉失去了对输入位置的控制。如果你无法阻止文本字段移动或调整大小，考虑将变更延迟到用户暂停书写时再执行。

**防止用户在文本字段中书写和编辑时文本自动滚动。** 当转录的文本自动滚动时，用户可能会试图避免在滚动的文本上方书写。更糟的是，如果用户正在使用 Apple Pencil 选择文本时文本发生滚动，他们可能会选中与预期不同的文本范围。

**为用户提供足够的书写空间。** 较小的文本字段会让人书写时不舒适。当你知道用户可能使用 Apple Pencil 输入时，可以在用户开始书写前或暂停书写时增大文本字段尺寸来改善书写体验；避免在用户书写过程中调整文本字段大小。有关开发者指南，请参阅 [`UIScribbleInteraction`](https://developer.apple.com/documentation/UIKit/UIScribbleInteraction)。

![An illustration showing a stack of two text fields, where the top field is about half the width of the bottom field. Both text fields contain the word Name in the leading end, followed by a person's signature. The top text field is too narrow to fit all of the signature and is marked with an X in a circle to indicate incorrect usage. The bottom text field is wide enough to fit the full signature and is marked with a checkmark in a circle to indicate correct usage.](https://docs-assets.developer.apple.com/published/0e2cd3f5562569097b9f668253dac0f7/apple-pencil-scribble%402x.png)

## [自定义绘图](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Custom-drawing)

使用 [PencilKit](https://developer.apple.com/documentation/PencilKit)，你可以让用户做笔记、标注文档和图片，以及以 iOS 提供的同等低延迟体验进行绘图。PencilKit 还能轻松在你的 app 中创建自定义绘图画布，并提供一流的工具选择器和墨水调色板。

**帮助用户在现有内容上进行绘制。** 默认情况下，PencilKit 画布上的颜色会动态适配深色模式，因此用户在任一模式下创建的内容在两种模式下都能良好呈现。然而，当用户在 PDF 或照片等现有内容上绘制时，你需要阻止颜色的动态调整，以确保标记保持清晰可见。

**考虑在 app 以紧凑环境运行时显示自定义撤销和重做按钮。** 在常规环境中，工具选择器包含撤销和重做按钮，但在紧凑环境中没有。在紧凑环境中，你可以在工具栏中显示撤销和重做按钮。你也可以考虑支持标准的三指撤销/重做手势，这样用户在任何环境中都能使用。有关指南，请参阅[撤销和重做](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)。

![An illustration of an iPad screen in landscape on the left and an iPhone screen in portrait on the right. Both screens show the tool picker at the bottom edge of the screen. The iPad screen shows the standard undo and redo buttons in the left end of the tool picker, and the iPhone screen shows the undo button in the top toolbar.](https://docs-assets.developer.apple.com/published/7587fbeb4272d990e295d093f79e1ef8/apple-pencil-undo-redo-buttons%402x.png)

## [平台说明](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Platform-considerations)

 _不支持 iOS、macOS、tvOS、visionOS 或 watchOS。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Related)

[输入数据](https://developer.apple.com/design/human-interface-guidelines/entering-data)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Developer-documentation)

[PencilKit](https://developer.apple.com/documentation/PencilKit)

[PaperKit](https://developer.apple.com/documentation/PaperKit)

#### [视频](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/BE1C66C1-9D8C-4EF7-BE9A-A36251A00B86/10006_wide_250x141_1x.jpg) Meet PaperKit ](https://developer.apple.com/videos/play/wwdc2025/285)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/2104DC8F-01CE-453F-AF0E-A499CB193E97/9354_wide_250x141_1x.jpg) Squeeze the most out of Apple Pencil ](https://developer.apple.com/videos/play/wwdc2024/10214)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble#Change-log)

日期| 变更
---|---
2024 年 5 月 7 日| 新增 Apple Pencil Pro 挤压和旋转的操作指南。
2023 年 9 月 12 日| 更新插图。
2022 年 11 月 3 日| 新增使用悬停增强 app 体验的指南。
