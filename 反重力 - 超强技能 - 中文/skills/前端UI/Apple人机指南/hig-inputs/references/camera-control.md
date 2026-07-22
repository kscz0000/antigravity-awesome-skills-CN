---
title: "相机控制 | Apple 开发者文档"
source: https://developer.apple.com/design/human-interface-guidelines/camera-control

# 相机控制

相机控制提供对应用相机体验的直接访问。

![相机控制的风格化表示。](https://docs-assets.developer.apple.com/published/73774a69a0e7738c02ffdaeccfe03830/inputs-camera-control-intro%402x.png)

在 iPhone 16 和 iPhone 16 Pro 机型上，相机控制可以快速打开应用的相机体验，在瞬间发生时捕捉时刻。当人轻按相机控制时，系统会显示从设备边框延伸的覆盖层。

![一张显示 iPhone 横向方向上相机控制和覆盖层标注的截图。](https://docs-assets.developer.apple.com/published/3d9efd41aaf5eb91e9d51fdf57a26472/camera-control-button-callout%402x.png)

覆盖层允许人们快速调整控件。人可以通过轻按两次相机控制来查看可用控件。选择控件后，他们可以在相机控制上滑动手指来调整值，以按自己的意愿捕捉内容。

![相机控制覆盖层显示其控件的部分截图。](https://docs-assets.developer.apple.com/published/59fe90435020556bfc9b5ed3f003b651/camera-control-picker%402x.png)覆盖层中的控件

## [结构](https://developer.apple.com/design/human-interface-guidelines/camera-control#Anatomy)

相机控制提供两种类型的控件来调整值或在选项之间切换：

  * _滑块_提供一系列可选值，例如要对内容应用多少对比度。

  * _选择器_提供离散选项，例如在取景器中打开和关闭网格。




![相机控制覆盖层显示滑块控件的部分截图。](https://docs-assets.developer.apple.com/published/3bb2ecfcd292742f087c064e5dfd1ec5/camera-control-slider-control%402x.png)滑块控件

![相机控制覆盖层显示选择器控件的部分截图。](https://docs-assets.developer.apple.com/published/27e6bc8836d9265133dd150098c3865d/camera-control-picker-control%402x.png)选择器控件

除了你创建的自定义控件外，系统还提供一组标准控件，你可以选择在覆盖层中包含这些控件，允许某人调整相机的缩放和曝光。

![相机控制覆盖层显示系统缩放倍数控件的部分截图。](https://docs-assets.developer.apple.com/published/3bb2ecfcd292742f087c064e5dfd1ec5/system-control-type-zoom-factor%402x.png)缩放倍数控件

![相机控制覆盖层显示系统曝光偏移控件的部分截图。](https://docs-assets.developer.apple.com/published/47568cc559bb20a5cea03ded2199916b/system-control-type-exposure-bias%402x.png)曝光偏移控件

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/camera-control#Best-practices)

**使用 SF Symbols 来表示控件功能。** 系统不支持自定义符号；相反，从 SF Symbols 中选择一个能清楚表示控件行为的符号。iOS 提供数千个符号，你可以用来表示应用在覆盖层中显示的控件。控件的符号不表示其当前状态。要查看可用符号，请参阅 [SF Symbols 应用](https://developer.apple.com/sf-symbols/)中的相机与照片部分。

![相机控制覆盖层显示使用 bolt.fill 符号的相机闪光灯控件的部分截图。](https://docs-assets.developer.apple.com/published/29e9dac71ac35e1d3d9510a545fce3c3/camera-control-picker-sf-symbols-flash%402x.png)表示相机闪光灯控件的 `bolt.fill` 符号

![相机控制覆盖层显示使用 camera.filters 符号的相机滤镜控件的部分截图。](https://docs-assets.developer.apple.com/published/17466338143a202a0241d26725f23048/camera-control-picker-sf-symbols-filters%402x.png)表示滤镜控件的 `camera.filters` 符号

**保持控件名称简短。** 控件标签遵循动态类型大小，较长的名称可能会遮挡相机的取景器。

**在滑块控件值中包含单位或符号以提供上下文。** 在覆盖层中提供描述性信息（如 EV、% 或自定义字符串）可帮助人们理解滑块控制的内容。有关开发者指导，请参阅 [`localizedValueFormat`](https://developer.apple.com/documentation/AVFoundation/AVCaptureSlider/localizedValueFormat)。

![显示相机控制覆盖层中滑块控件显示值和值类型上下文示例的部分截图。](https://docs-assets.developer.apple.com/published/00f466e6926811164965fdb40483a34c/system-control-with-label%402x.png)

![圆圈中的勾号表示正确用法。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)带上下文的值

![显示相机控制覆盖层中滑块控件显示值但没有表示什么值信息的示例的部分截图。](https://docs-assets.developer.apple.com/published/b965fe40e836dfce1361f8653c3d2abb/system-control-no-label%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)不带上下文的值

**为滑块控件定义突出值。** 突出值是人们最常选择的值，或均匀分布的值，如缩放倍数的主要增量。当人在相机控制上滑动以调整滑块控件时，系统更容易落在你定义的突出值上。有关开发者指导，请参阅 [`prominentValues`](https://developer.apple.com/documentation/AVFoundation/AVCaptureSlider/prominentValues-199dz)。

**在取景器中为覆盖层留出空间。** 覆盖层和控件标签在纵向和横向方向上都占据与相机控制相邻的屏幕区域。为避免与相机捕捉体验的界面元素重叠，请将 UI 放置在覆盖层区域之外。最大化取景器的高度和宽度，允许覆盖层在其上方显示和消失。

![在 iPhone 纵向和横向方向上显示相机控制覆盖层及其控件标签在视口中的部分截图。](https://docs-assets.developer.apple.com/published/efa0584ce5fa07cd540174b71ef59d6d/camera-control-portrait-landscape-orientation%402x.png)

**尽量减少取景器中的干扰。** 在捕捉照片或视频时，人们喜欢大型预览图像，视觉干扰尽可能少。避免在系统显示覆盖层时在 UI 和覆盖层中重复控件（如滑块和切换）。

![显示相机控制覆盖层中捕捉视口中移除 UI 元素示例的部分截图。](https://docs-assets.developer.apple.com/published/9cd4da3793671dd837c50d855ab265df/camera-control-screen-ui-good-example%402x.png)

![圆圈中的勾号表示正确用法。](https://docs-assets.developer.apple.com/published/88662da92338267bb64cd2275c84e484/checkmark%402x.png)保持 UI 简洁。

![显示相机控制覆盖层中捕捉视口中重复 UI 元素示例的部分截图。](https://docs-assets.developer.apple.com/published/eb4a1bc88b0f16c3074d57f8ff3afb9f/camera-control-screen-ui-bad-example%402x.png)

![圆圈中的 X 表示错误用法。](https://docs-assets.developer.apple.com/published/209f6f0fc8ad99d9bf59e12d82d06584/crossout%402x.png)避免在取景器中显示人们可以在覆盖层中访问的控件。

**根据相机模式启用或禁用控件。** 例如，在拍照时禁用视频控件。覆盖层支持多个控件，但你无法在运行时移除或添加控件。

**考虑如何排列控件。** 将常用控件排列在中间以便快速访问，并在两侧包含较少使用的控件。当人轻按相机控制再次打开覆盖层时，系统会记住他们在你的应用中上次使用的控件。

**允许人们使用相机控制从任何地方启动你的体验。** 创建锁定的相机捕捉扩展，让人们配置相机控制从锁定的设备、主屏幕或其他应用内启动应用的相机体验。有关指导，请参阅[锁定设备上的相机体验](https://developer.apple.com/design/human-interface-guidelines/controls#Camera-experiences-on-a-locked-device)。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/camera-control#Platform-considerations)

_iPadOS、macOS、watchOS、tvOS 或 visionOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/camera-control#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/camera-control#Related)

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

[控件](https://developer.apple.com/design/human-interface-guidelines/controls)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/camera-control#Developer-documentation)

[Enhancing your app experience with the Camera Control](https://developer.apple.com/documentation/AVFoundation/enhancing-your-app-experience-with-the-camera-control) — AVFoundation

[`AVCaptureControl`](https://developer.apple.com/documentation/AVFoundation/AVCaptureControl) — AVFoundation

[LockedCameraCapture](https://developer.apple.com/documentation/LockedCameraCapture)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/camera-control#Change-log)

日期| 变更  
---|---  
2024年9月9日| 新页面。  
