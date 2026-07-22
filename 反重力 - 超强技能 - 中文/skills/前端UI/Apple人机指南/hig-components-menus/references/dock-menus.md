---
title: "Dock menus | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/dock-menus

# Dock 菜单

在 Mac 上，用户可以辅助点击 Dock 中应用或游戏的图标以显示 Dock 菜单，该菜单同时呈现系统提供的和自定义的项目。

![从 Dock 中的图标延伸出的菜单的样式化呈现。图像染成红色以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/b09af2b90f697b3e25f1985cce93f4ab/components-dock-menu-intro%402x.png)

系统提供的 Dock 菜单项可能因应用是否打开而异。例如，Safari 的 Dock 菜单包含查看当前窗口或创建新窗口等操作的菜单项。

注意

虽然 iOS 和 iPadOS 不支持 Dock 菜单，但当用户在主屏幕或 Dock 中长按应用图标时，可以显示类似的系统提供和自定义项目菜单——称为主屏幕快捷操作。有关指导，请参阅[主屏幕快捷操作](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Best-practices)

与所有菜单一样，您需要简洁地标记 Dock 菜单项并对其进行逻辑组织。有关指导，请参阅[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

**在其他地方也提供自定义 Dock 菜单项。** 并非每个人都使用 Dock 菜单，因此在其他地方提供相同的命令很重要，如在菜单栏菜单中或在界面内。

**为 Dock 菜单优先提供高价值的自定义项目。** 例如，Dock 菜单可以列出所有当前或最近打开的窗口，使其成为跳转到用户想要的窗口的便捷方式。还可以考虑列出一些在应用不是最前面或没有打开窗口时最有用的操作。例如，邮件除了列出所有打开的窗口外，还包括获取新邮件和撰写新邮件的项目。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Platform-considerations)

_iOS、iPadOS、tvOS、visionOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Related)

[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)

[主屏幕快捷操作](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Developer-documentation)

[`applicationDockMenu(_:)`](https://developer.apple.com/documentation/AppKit/NSApplicationDelegate/applicationDockMenu\(_:\)) — AppKit
