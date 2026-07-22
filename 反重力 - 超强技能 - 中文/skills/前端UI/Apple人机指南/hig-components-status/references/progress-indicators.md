---
title: "Progress indicators | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/progress-indicators

# 进度指示器

进度指示器让用户知道应用在加载内容或执行耗时操作时没有卡住。

![一个旋转的不确定性活动指示器和进度条的示意性表示。图片带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/983ffd361839ffc1360b1542a8205a45/components-progress-indicators-intro%402x.png)

某些进度指示器还让用户能够估算需要等待多久才能完成某事。所有进度指示器都是临时的，仅在操作进行时出现，完成后消失。

由于操作的时长要么已知要么未知，因此有两种类型的进度指示器：

  * _确定性_，用于有明确定义时长的任务，如文件转换

  * _不确定性_，用于无法量化的任务，如加载或同步复杂数据




确定性和不确定性进度指示器根据平台可以有不同的外观。确定性进度指示器通过填充线性或圆形轨道来显示任务进度。_进度条_包含从起始侧向结束侧填充的轨道。_圆形进度指示器_具有顺时针填充的轨道。

![macOS 中水平进度条的图像，几乎填充到中点，填充为实色。](https://docs-assets.developer.apple.com/published/ec2a80ba694138d5ac65555f5e3b0734/progress-indicator-determinate-bar%402x.png)进度条

![macOS 中圆形进度指示器的图像，几乎填充到八点钟位置，填充为实色。](https://docs-assets.developer.apple.com/published/8288f9d55f529f513e7c3bd33bc3e17a/progress-indicator-determinate-circle%402x.png)圆形进度指示器

不确定性进度指示器——也称为_活动指示器_——使用动画图像指示进度。所有平台都支持看起来在旋转的圆形图像；但 macOS 还支持不确定性进度条。

![macOS 中旋转的圆形活动指示器图像。](https://docs-assets.developer.apple.com/published/6c1e23fcc6e04603423dacd5df6c48a3/progress-indicator-intermediate-spinner%402x.png)macOS

![watchOS 中旋转的活动指示器图像。](https://docs-assets.developer.apple.com/published/02a8427a04f946d9b80d2907f84ab365/activity-indicators-watch%402x.png)watchOS

开发者指南见 [`ProgressView`](https://developer.apple.com/documentation/SwiftUI/ProgressView)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices)

**尽可能使用确定性进度指示器。** 不确定性进度指示器显示正在发生处理，但不帮助用户估算任务需要多长时间。确定性进度指示器可以帮助用户决定是等待任务完成时做其他事情、在另一个时间重启任务，还是放弃任务。

**报告确定性进度指示器的进度时尽可能准确。** 考虑平滑进度速度，帮助用户对任务完成所需时间建立信心。在五秒内显示 90% 完成，然后最后 10% 需要 5 分钟，会让用户怀疑应用是否还在工作，甚至感觉被欺骗。

**保持进度指示器移动，让用户知道事情在继续发生。** 用户倾向于将静止的指示器与停滞的进程或冻结的应用联系起来。如果进程因某种原因停滞，提供反馈帮助用户理解问题以及他们可以做什么。

**尽可能将进度条从不确定性切换为确定性。** 如果不确定性进程达到可以确定其时长的点，切换到确定性进度条。用户通常更喜欢确定性进度指示器，因为它帮助他们判断正在发生什么以及需要多长时间。

**不要从圆形样式切换到条形样式。** 活动指示器（也称为_旋转指示器_）和进度条形状和大小不同，在它们之间过渡可能破坏界面并让用户困惑。

**如果有帮助，显示为任务提供额外上下文的描述。** 准确且简洁。避免使用"加载中"或"验证中"等模糊术语，因为它们很少增加价值。

**在一致的位置显示进度指示器。** 为进度指示器选择一致的位置有助于用户可靠地在平台间或应用内或应用间找到操作状态。

**可行时让用户能够停止处理。** 如果用户可以中断进程而不会造成负面副作用，包含取消按钮。如果中断进程可能导致负面副作用——例如丢失已下载的文件部分——除了取消按钮外，提供暂停按钮可能有用。

**让用户知道停止进程有负面后果。** 当取消进程导致进度丢失时，提供包含确认取消或恢复进程选项的[警告](https://developer.apple.com/design/human-interface-guidelines/alerts)会有帮助。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Platform-considerations)

_tvOS 或 visionOS 无额外注意事项。_

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#iOS-iPadOS)

#### [刷新内容控件](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Refresh-content-controls)

刷新控件让用户立即重新加载内容，通常在表格视图中，无需等待下一次自动内容更新。刷新控件是一种特殊类型的活动指示器，默认隐藏，当用户下拉要重新加载的视图时变为可见。例如，在"邮件"中，用户可以下拉收件箱列表来检查新邮件。

![邮件检查新邮件时旋转的刷新内容控件截图。](https://docs-assets.developer.apple.com/published/861acc5c0d9d6821e3dd4fd7fb42606f/refresh-controls%402x.png)

**执行自动内容更新。** 虽然用户欣赏能够立即刷新内容，他们也期望定期发生自动刷新。不要让用户负责发起每次更新。通过定期更新保持数据新鲜。

**仅在增加价值时提供简短标题。** 刷新控件可以选择包含标题。在大多数情况下，这是不必要的，因为控件的动画表明内容正在加载。如果确实包含标题，不要用它解释如何执行刷新。相反，提供有关正在刷新内容的有价值信息。例如，"播客"中的刷新控件使用标题告诉用户上次播客更新是什么时候。

开发者指南见 [`UIRefreshControl`](https://developer.apple.com/documentation/UIKit/UIRefreshControl)。

### [macOS](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#macOS)

在 macOS 中，不确定性进度指示器可以有条形或圆形外观。两个版本都使用动画图像指示应用正在执行任务。

![macOS 中完全填充的水平进度条图像。填充动画在进度继续时循环显示各种色调变化。](https://docs-assets.developer.apple.com/published/53c298b42043574cfe1d304c01bfc967/progress-indicator-intermediate-bar%402x.png)不确定性进度条

![macOS 中旋转的圆形活动指示器图像。](https://docs-assets.developer.apple.com/published/6c1e23fcc6e04603423dacd5df6c48a3/progress-indicator-intermediate-spinner%402x.png)不确定性圆形进度指示器

**首选活动指示器（旋转指示器）来传达后台操作状态或空间受限时。** 旋转指示器小而不显眼，因此对于异步后台任务（如从服务器检索消息）很有用。旋转指示器也适合在小区域内传达进度，例如在文本字段内或特定控件（如按钮）旁边。

**避免为旋转进度指示器添加标签。** 由于旋转指示器通常在用户发起进程时出现，标签通常是不必要的。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#watchOS)

默认情况下，系统在场景背景色上以白色显示进度指示器。你可以通过设置其色调颜色来更改进度指示器的颜色。

![watchOS 中从左到右填充的进度条图像。](https://docs-assets.developer.apple.com/published/33bbf8ea9d047a5933e60cb120d3556e/progress-bar-watch%402x.png)进度条

![watchOS 中顺时针填充的圆形进度指示器图像。](https://docs-assets.developer.apple.com/published/9327014cf549f926741534698be7d5ee/progress-ring-watch%402x.png)圆形进度指示器

![watchOS 中旋转的活动指示器图像。](https://docs-assets.developer.apple.com/published/02a8427a04f946d9b80d2907f84ab365/activity-indicators-watch%402x.png)活动指示器

## [资源](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Resources)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Developer-documentation)

[`ProgressView`](https://developer.apple.com/documentation/SwiftUI/ProgressView) — SwiftUI

[`UIProgressView`](https://developer.apple.com/documentation/UIKit/UIProgressView) — UIKit

[`UIActivityIndicatorView`](https://developer.apple.com/documentation/UIKit/UIActivityIndicatorView) — UIKit

[`UIRefreshControl`](https://developer.apple.com/documentation/UIKit/UIRefreshControl) — UIKit

[`NSProgressIndicator`](https://developer.apple.com/documentation/AppKit/NSProgressIndicator) — AppKit

## [更新日志](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Change-log)

日期| 变更  
---|---  
2023年9月12日| 合并了所有平台通用的指导。  
2023年6月5日| 更新指导以反映 watchOS 10 的变化。  
