---
title: "Sliders | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/sliders

# 滑块

滑块是一个水平轨道，带有一个称为滑块的控件，用户可以在最小值和最大值之间调整。

![亮度滑块的风格化表示。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/ebb02bcf10487e6a03fd081236b35aa0/components-slider-intro%402x.png)

当滑块的值变化时，最小值和滑块之间的轨道部分填充颜色。滑块可以选择性地显示左右图标，说明最小值和最大值的含义。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/sliders#Best-practices)

**如果滑块的外观能增加价值，请自定义它。** 您可以调整滑块的外观——包括轨道颜色、滑块图像和色调颜色以及左右图标——以融入应用的设计并传达意图。例如，调整图像大小的滑块可以在左侧显示小图像图标，在右侧显示大图像图标。

**使用熟悉的滑块方向。** 用户期望所有应用中滑块的最小值和最大值侧一致，水平滑块的最小值在前侧，最大值在后侧，垂直滑块的最小值在底部，最大值在顶部。例如，用户期望能够将表示百分比的滑块从前侧的 0% 移动到后侧的 100%。

**考虑用相应的文本字段和步进器补充滑块。** 特别是当滑块表示大范围值时，用户可能希望看到确切的滑块值并能够在文本字段中输入特定值。添加步进器为用户提供了一种以整数值递增的便捷方式。有关相关指导，请参阅[文本字段](https://developer.apple.com/design/human-interface-guidelines/text-fields)和[步进器](https://developer.apple.com/design/human-interface-guidelines/steppers)。

![没有刻度线的水平线性滑块的插图，后跟文本字段和步进器。滑块位于滑块中心，文本字段显示 50%。](https://docs-assets.developer.apple.com/published/ce79e1e4b3b1faa688862341ed208792/sliders-text-field%402x.png)

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/sliders#Platform-considerations)

_tvOS 不支持。_

### [iOS、iPadOS](https://developer.apple.com/design/human-interface-guidelines/sliders#iOS-iPadOS)

**不要使用滑块调整音量。** 如果需要在应用中提供音量控制，请使用音量视图，它是可自定义的，包含音量级别滑块和用于更改活动音频输出设备的控件。有关指导，请参阅[播放音频](https://developer.apple.com/design/human-interface-guidelines/playing-audio)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/sliders#macOS)

macOS 中的滑块还可以包含刻度线，使用户更容易在范围内精确定位特定值。

在没有或有刻度线的线性滑块中，滑块是一个窄菱形，最小值和滑块之间的轨道部分填充颜色。线性滑块通常包含说明最小值和最大值含义的补充图标。

在圆形滑块中，滑块显示为小圆圈。当存在刻度线时，它们显示为滑块圆周周围均匀间隔的点。

![水平滑块的插图，滑块位于中间。从前侧到滑块的轨道部分填充蓝色高亮颜色。](https://docs-assets.developer.apple.com/published/92445cf683c4dc1b179fb5359a0bdb28/sliders-no-tick-marks%402x.png)没有刻度线的线性滑块

![水平滑块的插图，滑块位于滑块中间两个刻度线之间。从前侧到滑块的轨道部分填充蓝色高亮颜色。](https://docs-assets.developer.apple.com/published/e31ef9e35e8675bd62f695ba6a988a51/sliders-tick-marks%402x.png)有刻度线的线性滑块

![圆形滑块的插图，滑块位于 12 点钟位置。](https://docs-assets.developer.apple.com/published/3f253ed199e7e92b6124e6161dd79152/sliders-circular%402x.png)圆形滑块

**考虑在滑块值变化时提供实时反馈。** 实时反馈向用户实时显示结果。例如，在调整 Dock 设置中的大小滑块时，Dock 图标会动态缩放。

**选择符合用户期望的滑块样式。** 在固定起点和终点之间移动时，水平滑块是理想选择。例如，图形应用可能提供水平滑块来设置对象的透明度级别，范围从 0 到 100%。当值重复或无限延续时使用圆形滑块。例如，图形应用可能使用圆形滑块调整对象的旋转，范围从 0 到 360 度。动画应用可能使用圆形滑块调整对象动画时的旋转次数——四次完整旋转等于四次旋转，或 1440 度旋转。

**考虑使用标签介绍滑块。** 标签通常使用[句子样式大写](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64)并以冒号结尾。有关指导，请参阅[标签](https://developer.apple.com/design/human-interface-guidelines/labels)。

**使用刻度线提高清晰度和准确性。** 刻度线帮助用户理解测量尺度，更容易定位特定值。

![macOS 节能设置窗格的部分截图，裁剪显示控制显示器在非活动后保持开启时间的滑块。](https://docs-assets.developer.apple.com/published/90d44ac8355f4a4e672e5e81633814e6/sliders-labels%402x.png)

**考虑为刻度线添加标签以获得更高的清晰度。** 根据滑块的值，标签可以是数字或单词。除非需要减少混淆，否则不需要标记每个刻度线。在许多情况下，仅标记最小值和最大值就足够了。当滑块的值非线性时（如节能设置窗格中），定期标签提供上下文。当用户将指针悬停在滑块上时，提供显示滑块值的[工具提示](https://developer.apple.com/design/human-interface-guidelines/offering-help#macOS-visionOS)也是一个好主意。

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/sliders#visionOS)

**优先使用水平滑块。** 用户通常发现左右手势比上下手势更容易。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/sliders#watchOS)

滑块是一个水平轨道——显示为一组离散步骤或连续条——表示有限范围的值。用户可以点击滑块两侧的按钮以预定义量增加或减少其值。

![带有离散步骤的 watchOS 音量滑块的插图。三个步骤中的前两个填充绿色高亮颜色，指示音量级别。](https://docs-assets.developer.apple.com/published/3acc4339289d9cf65ec982e73f950f97/sliders-watchos-discrete%402x.png)离散

![带有连续条的 watchOS 音量滑块的插图。条的三分之二填充绿色高亮颜色，指示音量级别。](https://docs-assets.developer.apple.com/published/b356f0616bad32afce9ac9e62763414b/sliders-watchos-continuous%402x.png)连续

**如有必要，创建自定义字形来传达滑块的作用。** 系统默认显示加号和减号。

## [资源](https://developer.apple.com/design/human-interface-guidelines/sliders#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/sliders#Related)

[Steppers](https://developer.apple.com/design/human-interface-guidelines/steppers)

[Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/sliders#Developer-documentation)

[`Slider`](https://developer.apple.com/documentation/SwiftUI/Slider) — SwiftUI

[`UISlider`](https://developer.apple.com/documentation/UIKit/UISlider) — UIKit

[`NSSlider`](https://developer.apple.com/documentation/AppKit/NSSlider) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/sliders#Change-log)

日期| 变更  
---|---  
2023年6月21日| 更新以包含 visionOS 指导。  
