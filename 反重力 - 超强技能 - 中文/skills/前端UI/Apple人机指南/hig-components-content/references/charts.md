---
title: "Charts | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/charts

# 图表

在图表中组织数据，以清晰且视觉吸引的方式传达信息。

![柱状图的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/e60ec631128010abf4cf09793552a20a/components-charts-intro%402x.png)

有效的图表突出显示数据集中的几个关键信息片段，帮助用户获得洞察并做出决策。例如，用户可能使用图表来：

* 了解即将到来的天气状况如何影响他们的计划。

* 分析股票价格以了解过去的表现并发现趋势。

* 查看健身数据以监控进度并设定新目标。

要了解如何设计图表以增强你的体验，请参阅[数据图表化](https://developer.apple.com/design/human-interface-guidelines/charting-data)；有关开发者指导，请参阅[使用 Swift Charts 创建图表](https://developer.apple.com/documentation/Charts/Creating-a-chart-using-Swift-Charts)。

## [结构](https://developer.apple.com/design/human-interface-guidelines/charts#Anatomy)

图表由多个图形元素组成，这些元素描绘数据集中的值并传达相关信息。

![带有标注的柱状图，标识图表组件，如坐标轴、网格线、标记、刻度、轴值标签和整体绑图区域。](https://docs-assets.developer.apple.com/published/3435cdf95a0a1c5faeeb347ccd4915d4/charts-anatomy%402x.png)

标记是数据值的视觉表示。你通过提供一个或多个数据值系列并将每个值分配给标记来创建图表。要指定要显示的图表样式（如柱状图、折线图或散点图），你需要选择标记类型，如柱状、线条或点（有关指导，请参阅[标记](https://developer.apple.com/design/human-interface-guidelines/charts#Marks)）。在图表中描绘单个数据值的一般任务称为绑图，包含标记的区域称为绑图区域。

要描绘一个值，每种类型的标记使用由比例确定的视觉属性，该比例将数字、日期或类别等数据值映射到位置、颜色或高度等视觉特征。例如，柱状标记可以使用特定高度来表示值的大小，使用特定位置来表示值发生的时间。

为了让用户获得解释图表视觉特征所需的上下文，你需要提供可以采取几种不同形式的描述性内容。

你可以使用轴来帮助定义一组标记所表示的数据的参考框架。许多图表在绑图区域边缘显示一对坐标轴——一个水平轴和一个垂直轴——每个轴代表一个变量，如时间、数量或类别。

轴可以包含刻度，这是帮助用户在视觉上定位轴上重要值位置的参考点，如 0、50% 和 100%。许多图表显示网格线，每条网格线从刻度延伸穿过绑图区域，帮助用户在标记不在轴附近时在视觉上估计数据值。

你还有多种方式来描述图表元素，帮助用户解释数据并突出你想传达的关键信息。例如，你可以提供命名轴、网格线、刻度或标记等项目的标签，以及为使用辅助技术的用户描述图表元素的无障碍标签。要提供上下文和额外细节，你可以创建描述性标题、副标题和注释。需要时，你还可以创建图例，描述与标记位置无关的图表属性，如使用颜色或形状来表示不同的值类别。

清晰、准确的描述可以帮助使图表更易接近和无障碍；要了解改善图表无障碍性的其他方法，请参阅[增强图表的无障碍性](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart)。

## [标记](https://developer.apple.com/design/human-interface-guidelines/charts#Marks)

**根据你想传达的数据信息选择标记类型。** 一些最熟悉的标记类型是柱状、线条和点；有关这些和其他标记类型的开发者指导，请参阅 [Swift Charts](https://developer.apple.com/documentation/Charts)。

柱状标记适用于帮助用户比较不同类别中的值或查看整体中各部分的相对比例的图表。当用于帮助用户理解随时间变化的数据时，柱状图特别适用于每个值可以表示总和的情况，如一天中的总步数。

![描绘一个月中每天步数的柱状图。](https://docs-assets.developer.apple.com/published/69afb0247060876d7c148529bb6770ef/charts-bar-marks%402x.png)

线条标记也可以显示值如何随时间变化。在折线图中，一条线连接一个数据系列中的所有数据值。线的斜率揭示了数据值之间变化的大小，可以帮助用户可视化整体趋势。

![描绘五年期间股票表现的折线图。](https://docs-assets.developer.apple.com/published/a242ab0dd33e91b2928163ac76839aae/charts-line-marks%402x.png)

点标记帮助你将单个数据值描绘为视觉上不同的标记。一组点标记可以显示数据的两个不同属性如何相互关联，帮助用户检查单个数据值并识别异常值和聚类。

![描绘 5 个半月期间每分钟心跳次数的每日读数的点标记图表。](https://docs-assets.developer.apple.com/published/e425cf9c73689456ffe358c15a2db34c/charts-point-marks%402x.png)

**考虑在增加图表清晰度时组合标记类型。** 例如，如果你使用折线图显示随时间的变化，你可能想在折线上方添加点标记以突出单个数据点。通过将点与线组合，你可以帮助用户理解整体趋势，同时吸引他们注意单个值。

## [坐标轴](https://developer.apple.com/design/human-interface-guidelines/charts#Axes)

**根据图表的含义使用固定或动态轴范围。** 在固定范围中，轴的上下限从不改变；而在动态范围中，上下限可以随当前数据变化。当特定的最小值和最大值对所有可能的数据值都有意义时，考虑使用固定范围。例如，用户期望显示电池当前电量的图表的最小值为 0%（完全空），最大值为 100%（完全满）。

![电池设置的插图，使用图表描绘电池电量随时间的变化，其中电量可以在 0% 到 100% 的固定范围内变化。](https://docs-assets.developer.apple.com/published/77814deac13d3c51e09eb47c57e690fa/charts-fixed-range-axis%402x.png)

相比之下，当可能的数据值变化很大并且你希望标记填充可用的绑图区域时，考虑使用动态范围。例如，健康 App 中步数图表的 Y 轴范围上限会变化，以便特定时间段内的最大步数接近图表顶部。

![健康 App 中步数图表的插图，显示一周内每天的平均步数。](https://docs-assets.developer.apple.com/published/ba6263f9c8e9b9afef93349f20cbdde7/charts-dynamic-range-axis-small%402x.png)周范围

![健康 App 中步数图表的插图，显示一个月期间每天的平均步数。](https://docs-assets.developer.apple.com/published/de535d589204fce38a55acfb5c869c3e/charts-dynamic-range-axis-large%402x.png)月范围

**根据标记类型和图表用途定义下限值。** 例如，当 Y 轴下限使用零时，柱状图效果很好，因为这样用户可以在视觉上比较单个柱的相对高度，以合理估计其值。相比之下，将下限定义为零有时会使值之间的有意义差异更难辨别。例如，始终使用零作为下限的心率图表可能会掩盖静息和活动读数之间的重要差异，因为差异发生在远离零的范围内。

**在轴的刻度和网格线标签中使用熟悉的数值序列。** 例如，如果你使用常见的数字序列如 0、5、10 等，用户很可能一眼就知道每个刻度值等于前一个值加五。即使像 1、6、11 等序列遵循相同的规则，它也不常见，所以大多数用户可能会花额外时间思考值之间的间隔。

**根据图表的使用场景调整网格线和标签的外观。** 太多网格线可能在视觉上过于拥挤，分散用户对数据的注意力；太少网格线可能使估计标记值变得困难。要帮助你确定这些元素的适当密度和视觉权重，请考虑图表在界面中的上下文、你支持的交互以及用户可以在图表中执行的任务。例如，如果用户可以通过与图表交互来检查单个数据点，你可能使用较少的网格线和浅色标签颜色，以确保数据在视觉上保持突出。

## [描述性内容](https://developer.apple.com/design/human-interface-guidelines/charts#Descriptive-content)

**编写帮助用户在查看图表之前了解其作用的描述。** 当你提供描述图表目的和功能的信息丰富的标题和标签时，你在用户深入查看细节之前就提供了他们所需的上下文。以这种方式提供上下文对于 VoiceOver 用户和某些类型的认知障碍用户特别重要，因为他们依赖你的描述来理解图表的目的和主要信息，然后再决定进一步研究。

**总结图表的主要信息，使其对所有人都易于理解且有用。** 虽然使用图表的一个主要原因是显示支持主要信息的数据，但总结关键信息至关重要，这样用户可以快速掌握。例如，天气提供了简洁描述下一小时预期降水量的标题和副标题，为用户提供最重要的信息，而无需他们检查图表细节。

![天气 App 中下一小时降雨预报的插图，使用简洁的平实语言描述预期降水量。](https://docs-assets.developer.apple.com/published/28ee38d191d2f9816ded3e735bfee4a7/charts-descriptive-content%402x.png)

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/charts#Best-practices)

**建立一致的视觉层级，帮助传达各种图表元素的相对重要性。** 通常，你希望数据本身最突出，同时让描述和轴提供额外的上下文而不与数据竞争。

**在紧凑环境中，最大化绑图区域的宽度，为用户提供足够的空间舒适地检查图表。** 要帮助重要数据在给定宽度内良好适配，请确保垂直轴上的标签在不失清晰度的情况下尽可能短。你可能还需要考虑在图表的其他区域（如标题中）描述单位，并在不会遮挡重要信息时将较长的轴标签（如类别名称）放在绑图区域内。

**使 App 中的每个图表都可访问。** 图表——像所有信息图一样——需要对所有人都完全可访问，无论他们如何感知内容。例如，支持 VoiceOver 至关重要，它描述屏幕内容，帮助用户获取信息并在不需要看到屏幕的情况下导航（要了解更多关于 VoiceOver 的信息，请参阅[视觉](https://www.apple.com/accessibility/vision/)）。除了提供描述图表组件的无障碍标签外，你还可以通过使用音频图表来增强 VoiceOver 体验。[音频图表](https://developer.apple.com/documentation/Accessibility/audio-graphs)向 VoiceOver 提供图表信息，VoiceOver 构建一组在听觉上表示图表数据值及其趋势的音调；它还让你呈现提供额外上下文的高级文本摘要。有关指导，请参阅[增强图表的无障碍性](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart)。

**在有意义时让用户与数据交互，但不要要求交互来揭示关键信息。** 例如，在股票中，用户通常最感兴趣的是股票随时间的表现，所以 App 显示描绘用户选择的时间段（如一天、三个月或五年）内表现的折线图。如果用户想探索更多细节，他们可以在折线图中拖动垂直指示器，显示所选时间的值。

**让每个人都容易与图表交互。** 有时，图表标记太小而无法用手指或指针定位，使你的图表对运动控制能力降低的用户难以使用，对所有人都不舒适。在这种情况下，考虑将点击目标扩展到包括整个绑图区域，让用户在区域上滑动以显示各种值。

**使交互式图表在使用键盘命令（包括完全键盘访问）或 Switch Control 时易于导航。** 默认情况下，这些输入类型倾向于按线性顺序访问单个屏幕元素，如数据文件中的值序列。如果你想在图表中提供自定义导航体验，有两种主要方法。第一种方法是使用无障碍 API（如 [`accessibilityRespondsToUserInteraction(_:)`](https://developer.apple.com/documentation/SwiftUI/View/accessibilityRespondsToUserInteraction\(_:\))）指定通过图表信息的逻辑和可预测的路径。例如，你可能想让用户沿 X 轴导航而不是来回跳跃。第二种方法——如果你需要呈现非常大的数据集特别有用——是让用户在值的子集之间移动焦点，而不是导航所有单个数据点。请注意，这两种自定义也可以增强 VoiceOver 体验，即使你的图表不是交互式的。有关指导，请参阅[无障碍](https://developer.apple.com/design/human-interface-guidelines/accessibility)。

**帮助用户注意图表中的重要变化。** 例如，如果用户没有注意到标记或轴的变化，他们可能会误读图表。动画化这些变化可以帮助用户注意到它们，但你还需要以其他方式突出这些变化，以确保 VoiceOver 用户和关闭动画的用户知道它们。有关开发者指导，请参阅 [`UIAccessibility.Notification`](https://developer.apple.com/documentation/UIKit/UIAccessibility/Notification)（UIKit）或 [`NSAccessibility.Notification`](https://developer.apple.com/documentation/AppKit/NSAccessibility-swift.struct/Notification)（AppKit）。

**将图表与周围的界面元素对齐。** 例如，将图表的前沿与屏幕中其他视图的前沿对齐通常效果很好。在图表中保持清晰前沿的一种方法是在每条垂直网格线的后侧显示其标签。你可能还需要考虑将 Y 轴移到图表的后侧，以便其刻度标签不会突出超过图表的前沿。如果最终出现一个似乎与任何内容都不关联的标签，你可以使用刻度将其锚定到网格线。

## [颜色](https://developer.apple.com/design/human-interface-guidelines/charts#Color)

与界面的所有其他部分一样，在图表中使用颜色可以帮助你阐明信息、唤起品牌并提供视觉连续性。有关以所有人都能欣赏的方式使用颜色的一般指导，请参阅[包容性颜色](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color)。

**避免仅依赖颜色来区分不同的数据片段或在图表中传达基本信息。** 在图表中使用有意义的颜色来突出差异和提升关键细节效果很好，但至关重要的是包含传达此信息的替代方式，以便用户无论是否能辨别颜色都可以使用你的图表。补充颜色的一种方法是使用不同的形状或图案来描绘数据的不同部分。例如，除了使用红色和黑色或红色和白色外，健康还在表示血压两个组成部分的点标记中使用两种不同的形状。

![健康 App 中血压图表的插图，使用红色圆圈表示收缩压值，使用黑色或白色菱形表示舒张压值。](https://docs-assets.developer.apple.com/published/47d2a6b70d030b1aa595826248cb1186/charts-colors%402x.png)

**通过在相邻的颜色区域之间添加视觉分隔来帮助理解。** 例如，在单个行或列中堆叠标记的柱状图中，通常为每个标记分配不同的颜色。在这种设计中，在标记之间添加分隔符可以帮助用户区分单个标记。

![iPhone 存储设置的插图，使用包含几种不同颜色段的单个柱状标记来显示音乐、App 和照片等项目占用的相对空间。柱状标记在每对段之间包含一条狭窄的空白带。](https://docs-assets.developer.apple.com/published/86da90aecee27935b14e2b48388d08a6/charts-colors-stacked%402x.png)

## [增强图表的无障碍性](https://developer.apple.com/design/human-interface-guidelines/charts#Enhancing-the-accessibility-of-a-chart)

当你使用 Swift Charts 创建图表时，除了每个标记（或标记组）描述其值的默认无障碍元素外，你还可以获得[音频图表](https://developer.apple.com/documentation/Accessibility/audio-graphs)的默认实现。

**考虑使用音频图表为 VoiceOver 用户提供有关图表的更多信息。** 你可以通过提供图表标题和描述性摘要来自定义 Swift Charts 提供的默认音频图表实现，VoiceOver 会朗读这些内容以帮助用户理解图表的目的和主要特征。如果你不使用音频图表，你需要提供图表结构和用途的概述。例如，你需要识别图表的类型（如柱状或线条）、解释每个轴代表什么，并描述上下轴边界等细节。

重要

与图像（需要一个描述性无障碍标签）不同，图表通常需要为每个重要或交互元素提供无障碍标签。根据图表的目的及其标记的范围和密度，你需要决定是否有必要描述每个标记，或者描述标记组是否能改善无障碍体验。在某些情况下，使用提供图表简洁、高级描述的单个无障碍标签可能有意义，例如当你在按钮中使用图表的小版本以显示更详细的版本时。

**编写支持图表目的的无障碍标签。** 例如，地图使用图表显示骑行路线的海拔，该图表表示路线全程的海拔变化。图表的目的是让用户了解整个路线的地形，而不是提供单个海拔。因此，地图提供总结路线部分海拔变化的无障碍标签，而不是为每个单独时刻提供标签。相比之下，健康为步数图表中的每个柱提供无障碍标签，因为图表的目的是为用户提供每个跟踪期间的实际步数。

![地图中图表的插图，显示行程总距离范围内的海拔范围。图表顶部可见 VoiceOver 焦点指示器，包含约五分之一的总距离和海拔。](https://docs-assets.developer.apple.com/published/b85d8add4c38b6bedd65caf24fdbe03a/charts-bar-chart-with-voiceover-focus%402x.png)对于此骑行海拔图表的聚焦部分，VoiceOver 提供有关该路线部分的信息，包括距离和海拔变化。

以下指南可以帮助你为图表元素编写有用的无障碍标签。

* **优先考虑清晰性和全面性。** 通常，除非你还包含帮助用户理解的上下文（如与之关联的日期或位置），否则仅报告数据值很少足够。旨在简洁描述值的上下文，而不重复用户可以通过其他方式获取的信息，如音频图表或你的概述提供的轴名称。在设置上下文的信息之后，提供元素细节的简洁描述。

* **避免使用主观术语。** 主观词汇——如快速、逐渐和几乎——传达你对数据的解释。为了帮助用户形成自己的解释，请在描述中使用实际值。

* **通过避免潜在歧义的格式和缩写来最大化数据描述的清晰度。** 例如，使用"6月6日"比使用"6/6"更清晰；同样，拼写"60分钟"或"60米"比使用缩写"60m"更清晰。

* **描述图表细节代表什么，而不是它们看起来像什么。** 考虑一个使用红色和蓝色帮助用户在视觉上区分两个不同数据系列的图表。创建识别每个系列代表什么的无障碍标签至关重要，但描述在视觉上表示它们的颜色可能会添加不必要的信息并造成干扰。

* **在引用特定轴时在整个 App 中保持一致。** 例如，如果你总是先提到 X 轴，用户可以花更少时间弄清楚描述中相关的是哪个轴。

**从辅助技术中隐藏轴和刻度的可见文本标签。** 轴和刻度标签帮助用户在视觉上评估图表中的趋势并估计标记值。VoiceOver 用户可以通过无障碍标签和音频图表获取标记值和趋势信息，因此他们通常不需要可见标签中的内容。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/charts#Platform-considerations)

_iOS、iPadOS、macOS、tvOS、visionOS 无其他注意事项。_

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/charts#watchOS)

**通常，避免在 watchOS App 中要求复杂的图表交互。** 尽可能优先显示用户可以一目了然获取的有用信息，并在增加价值时支持简单交互。如果你还在其他平台提供 App 版本，考虑使用它来显示更多细节并支持与图表的额外交互。例如，watchOS 中的心率显示佩戴者当天的心率数据图表，而 iPhone 上的健康 App 显示几个不同时间段的心率数据，并让用户检查单个标记。

## [资源](https://developer.apple.com/design/human-interface-guidelines/charts#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/charts#Related)

[数据图表化](https://developer.apple.com/design/human-interface-guidelines/charting-data)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/charts#Developer-documentation)

[Swift Charts](https://developer.apple.com/documentation/Charts)

#### [视频](https://developer.apple.com/design/human-interface-guidelines/charts#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/89D5888B-58DA-4F47-8E3C-998253F6BA98/9954_wide_250x141_1x.jpg) Bring Swift Charts to the third dimension ](https://developer.apple.com/videos/play/wwdc2025/313)

[![](https://devimages-cdn.apple.com/wwdc-services/images/124/FA764D2D-4E15-4E91-91BA-BDAC80FB901B/6694_wide_250x141_1x.jpg) Design app experiences with charts ](https://developer.apple.com/videos/play/wwdc2022/110342)

[![](https://devimages-cdn.apple.com/wwdc-services/images/124/4BBCB61E-65ED-43FE-8F7B-81524E0C96BE/6692_wide_250x141_1x.jpg) Design an effective chart ](https://developer.apple.com/videos/play/wwdc2022/110340)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/charts#Change-log)

日期| 变更
---|---
2022年9月23日| 新页面。
