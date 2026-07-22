---
title: "Web views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/web-views

# 网页视图

网页视图直接在你的 App 中加载并显示丰富的网页内容，如内嵌 HTML 和网站。

![指南针图标的风格化呈现。图像带有红色色调，以微妙地反映原始六色 Apple 标志中的红色。](https://docs-assets.developer.apple.com/published/ae2c2f04ee2e04730e29b26e7e9bff19/components-web-view-intro%402x.png)

例如，邮件使用网页视图在消息中显示 HTML 内容。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/web-views#Best-practices)

**在适当时支持前进和后退导航。** 网页视图支持前进和后退导航，但此行为默认不可用。如果用户可能使用你的网页视图访问多个页面，请允许前进和后退导航，并提供相应的控件来启动这些功能。

**避免使用网页视图构建网页浏览器。** 使用网页视图让用户在不离开 App 上下文的情况下短暂访问网站是可以的，但 Safari 是用户浏览网页的主要方式。在 App 中尝试复制 Safari 的功能是不必要且不鼓励的。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations)

_iOS、iPadOS、macOS 或 visionOS 无其他注意事项。tvOS 或 watchOS 不支持。_

## [资源](https://developer.apple.com/design/human-interface-guidelines/web-views#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/web-views#Related)

[Webkit.org](https://webkit.org/)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/web-views#Developer-documentation)

[`WKWebView`](https://developer.apple.com/documentation/WebKit/WKWebView) — WebKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/web-views#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/8A0A5E12-9D2C-4629-A13C-8EB702A9DA28/4920_wide_250x141_1x.jpg) Explore WKWebView additions ](https://developer.apple.com/videos/play/wwdc2021/10032)
