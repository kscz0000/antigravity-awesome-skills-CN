# 深度链接与导航

## 意图

将外部 URL 路由到应用内目的地，必要时回退到系统处理。

## 核心模式

- 将 URL 处理集中在路由器中（`handle(url:)`、`handleDeepLink(url:)`）。
- 注入 `OpenURLAction` 处理器并委托给路由器。
- 应用 scheme 链接使用 `.onOpenURL`，需要时转换为 web URL。
- 让路由器决定是内部导航还是外部打开。

## 示例：路由器入口

```swift
@MainActor
final class RouterPath {
  var path: [Route] = []
  var urlHandler: ((URL) -> OpenURLAction.Result)?

  func handle(url: URL) -> OpenURLAction.Result {
    if isInternal(url) {
      navigate(to: .status(id: url.lastPathComponent))
      return .handled
    }
    return urlHandler?(url) ?? .systemAction
  }

  func handleDeepLink(url: URL) -> OpenURLAction.Result {
    // Resolve federated URLs, then navigate.
    navigate(to: .status(id: url.lastPathComponent))
    return .handled
  }
}
```

## 示例：附加到根视图

```swift
extension View {
  func withLinkRouter(_ router: RouterPath) -> some View {
    self
      .environment(
        \.openURL,
        OpenURLAction { url in
          router.handle(url: url)
        }
      )
      .onOpenURL { url in
        router.handleDeepLink(url: url)
      }
  }
}
```

## 设计要点

- URL 解析和决策逻辑放在路由器内部。
- 避免在多个地方处理深度链接，一个入口就够了。
- 始终提供回退到 `OpenURLAction` 或 `UIApplication.shared.open`。

## 陷阱

- 不要假设 URL 是内部的，先验证。
- 解析远程链接时避免阻塞 UI，使用 `Task`。
