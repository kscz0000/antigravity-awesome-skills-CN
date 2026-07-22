# NavigationStack

## 意图

使用此模式实现编程式导航和深度链接，尤其当每个标签页需要独立的导航历史时。核心理念是每个标签页一个 `NavigationStack`，各自拥有独立的路径绑定和路由器对象。

## 核心架构

- 定义一个 `Hashable` 的路由枚举，表示所有目的地。
- 创建轻量级路由器（或使用库如 `https://github.com/Dimillian/AppRouter`），持有 `path` 和 sheet 状态。
- 每个标签页拥有自己的路由器实例，将 `NavigationStack(path:)` 绑定到它。
- 将路由器注入环境，让子视图可以编程式导航。
- 用单一的 `navigationDestination(for:)` 块（或 `withAppRouter()` 修饰符）集中目的地映射。

## 示例：每标签页独立堆栈的自定义路由器

```swift
@MainActor
@Observable
final class RouterPath {
  var path: [Route] = []
  var presentedSheet: SheetDestination?

  func navigate(to route: Route) {
    path.append(route)
  }

  func reset() {
    path = []
  }
}

enum Route: Hashable {
  case account(id: String)
  case status(id: String)
}

@MainActor
struct TimelineTab: View {
  @State private var routerPath = RouterPath()

  var body: some View {
    NavigationStack(path: $routerPath.path) {
      TimelineView()
        .navigationDestination(for: Route.self) { route in
          switch route {
          case .account(let id): AccountView(id: id)
          case .status(let id): StatusView(id: id)
          }
        }
    }
    .environment(routerPath)
  }
}
```

## 示例：集中式目的地映射

使用共享的视图修饰符避免在各页面重复路由 switch。

```swift
extension View {
  func withAppRouter() -> some View {
    navigationDestination(for: Route.self) { route in
      switch route {
      case .account(let id):
        AccountView(id: id)
      case .status(let id):
        StatusView(id: id)
      }
    }
  }
}
```

然后在每个堆栈中应用一次：

```swift
NavigationStack(path: $routerPath.path) {
  TimelineView()
    .withAppRouter()
}
```

## 示例：每标签页绑定（独立历史的标签页）

```swift
@MainActor
struct TabsView: View {
  @State private var timelineRouter = RouterPath()
  @State private var notificationsRouter = RouterPath()

  var body: some View {
    TabView {
      TimelineTab(router: timelineRouter)
      NotificationsTab(router: notificationsRouter)
    }
  }
}
```

## 示例：泛型标签页 + 每标签页 NavigationStack

当标签页由数据构建且每个都需要独立路径、无需硬编码名称时使用。

```swift
@MainActor
struct TabsView: View {
  @State private var selectedTab: AppTab = .timeline
  @State private var tabRouter = TabRouter()

  var body: some View {
    TabView(selection: $selectedTab) {
      ForEach(AppTab.allCases) { tab in
        NavigationStack(path: tabRouter.binding(for: tab)) {
          tab.makeContentView()
        }
        .environment(tabRouter.router(for: tab))
        .tabItem { tab.label }
        .tag(tab)
      }
    }
  }
}

@MainActor
@Observable
final class TabRouter {
  private var routers: [AppTab: RouterPath] = [:]

  func router(for tab: AppTab) -> RouterPath {
    if let router = routers[tab] { return router }
    let router = RouterPath()
    routers[tab] = router
    return router
  }

  func binding(for tab: AppTab) -> Binding<[Route]> {
    let router = router(for: tab)
    return Binding(get: { router.path }, set: { router.path = $0 })
  }
}
```

## 设计要点

- 每个标签页一个 `NavigationStack`，保持独立历史。
- 导航状态的单一数据源（`RouterPath` 或库路由器）。
- 使用 `navigationDestination(for:)` 将路由映射到视图。
- 应用上下文变化时（账号切换、登出等）重置路径。
- 将路由器注入环境，让子视图可以导航和展示 Sheet 而无需逐层传递属性。
- 如果希望在一个地方管理模态窗口，将 Sheet 展示状态放在路由器上。

## 陷阱

- 不要在所有标签页间共享同一路径，除非你需要全局历史。
- 确保路由标识稳定且 `Hashable`。
- 不要在路径中存储视图实例，存储轻量级路由数据。
- 如果使用路由器对象，将其放在其他 `@Observable` 对象之外，避免嵌套观察。
