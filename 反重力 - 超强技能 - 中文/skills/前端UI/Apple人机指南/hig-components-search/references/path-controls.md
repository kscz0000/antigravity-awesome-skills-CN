---
title: "Path controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/path-controls

# 路径控件

路径控件显示所选文件或文件夹的文件系统路径。

![A stylized representation of a path control for a HIG Design document showing its root disk, parent folder, and selected item. The image is tinted red to subtly reflect the red in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/1266fc8267f96dc76fb9247aa5f08618/components-path-control-intro%402x.png)

例如，在访达中选择"显示 > 显示路径栏"会在窗口底部显示路径栏。它显示所选项目的路径，如果未选择任何内容则显示窗口文件夹的路径。

路径控件有两种样式。

![A screenshot of a Finder path bar that displays a hierarchy of four locations.](https://docs-assets.developer.apple.com/published/c7347a80a423da7a3886208113258675/path-controls-standard%402x.png)

**标准。** 包含根磁盘、父文件夹和所选项目的线性列表。每个项目显示图标和名称。如果列表太长无法在控件内容纳，它会隐藏第一个和最后一个项目之间的名称。如果将控件设为可编辑，用户可以将项目拖到控件上以选择该项目并在控件中显示其路径。

![A screenshot of a path control showing a folder icon and a pop-up control.](https://docs-assets.developer.apple.com/published/6768a6d2292f05923976b90cd80c931d/path-controls-popup%402x.png)

**弹出。** 类似[弹出按钮](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)的控件，显示所选项目的图标和名称。用户可以点击项目打开包含根磁盘、父文件夹和所选项目的菜单。如果将控件设为可编辑，菜单包含额外的"选择"命令，用户可使用它选择项目并在控件中显示。他们也可以将项目拖到控件上以选择它并显示其路径。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/path-controls#Best-practices)

**在窗口主体中使用路径控件，而非窗口框架。** 路径控件不适用于工具栏或状态栏。注意访达中的路径控件出现在窗口主体底部，而非状态栏。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/path-controls#Platform-considerations)

_iOS、iPadOS、tvOS、visionOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/path-controls#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/path-controls#Related)

[File management](https://developer.apple.com/design/human-interface-guidelines/file-management)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/path-controls#Developer-documentation)

[`NSPathControl`](https://developer.apple.com/documentation/AppKit/NSPathControl) — AppKit
