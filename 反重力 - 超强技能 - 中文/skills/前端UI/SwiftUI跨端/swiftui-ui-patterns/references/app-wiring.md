# 应用连接与依赖图

## 意图

展示如何连接应用壳（TabView + NavigationStack + sheets）并在一处安装全局依赖图（环境对象、服务、流式客户端、SwiftData ModelContainer）。

## 推荐结构

1) 根视图设置标签页、每标签页路由器和 Sheet。
2) 专门的视图修饰符安装全局依赖和生命周期任务（认证状态、流式监听、推送令牌、数据容器）。
3) 功能视图仅从环境中获取所需内容，功能特定的状态保持在本地。

## 依赖选择

- 应用级服务、共享客户端、主题/配置以及许多后代确实需要的值使用 `@Environment`。
- 功能局部的依赖和模型优先使用初始化注入。不要仅为了避免传递一两个参数就将依赖移入环境。
- 除非是有意跨应用广泛共享，否则不要将可变功能状态放入环境。
- `@EnvironmentObject` 仅作为遗留回退或项目已将其标准化为真正的共享对象时使用。

## 根壳示例（泛型）

```swift
@MainActor
struct AppView: View {
  @State private var selectedTab: AppTab = .home
  @State private var tabRouter = TabRouter()

  var body: some View {
    TabView(selection: $selectedTab) {
      ForEach(AppTab.allCases) { tab in
        let router = tabRouter.router(for: tab)
        NavigationStack(path: tabRouter.binding(for: tab)) {
          tab.makeContentView()
        }
        .withSheetDestinations(sheet: Binding(
          get: { router.presentedSheet },
          set: { router.presentedSheet = $0 }
        ))
        .environment(router)
        .tabItem { tab.label }
        .tag(tab)
      }
    }
    .withAppDependencyGraph()
  }
}
```

最小 `AppTab` 示例：

```swift
@MainActor
enum AppTab: Identifiable, Hashable, CaseIterable {
  case home, notifications, settings
  var id: String { String(describing: self) }

  @ViewBuilder
  func makeContentView() -> some View {
    switch self {
    case .home: HomeView()
    case .notifications: NotificationsView()
    case .settings: SettingsView()
    }
  }

  @ViewBuilder
  var label: some View {
    switch self {
    case .home: Label("Home", systemImage: "house")
    case .notifications: Label("Notifications", systemImage: "bell")
    case .settings: Label("Settings", systemImage: "gear")
    }
  }
}
```

路由器骨架：

```swift
@MainActor
@Observable
final class RouterPath {
  var path: [Route] = []
  var presentedSheet: SheetDestination?
}

enum Route: Hashable {
  case detail(id: String)
}
```

## 依赖图修饰符（泛型）

使用单一修饰符安装环境对象，并在活跃账号/客户端变更时处理生命周期钩子。这保持连接一致性，避免在调用点遗忘依赖。

```swift
extension View {
  func withAppDependencyGraph(
    accountManager: AccountManager = .shared,
    currentAccount: CurrentAccount = .shared,
    currentInstance: CurrentInstance = .shared,
    userPreferences: UserPreferences = .shared,
    theme: Theme = .shared,
    watcher: StreamWatcher = .shared,
    pushNotifications: PushNotificationsService = .shared,
    intentService: AppIntentService = .shared,
    quickLook: QuickLook = .shared,
    toastCenter: ToastCenter = .shared,
    namespace: Namespace.ID? = nil,
    isSupporter: Bool = false
  ) -> some View {
    environment(accountManager)
      .environment(accountManager.currentClient)
      .environment(quickLook)
      .environment(currentAccount)
      .environment(currentInstance)
      .environment(userPreferences)
      .environment(theme)
      .environment(watcher)
      .environment(pushNotifications)
      .environment(intentService)
      .environment(toastCenter)
      .environment(\.isSupporter, isSupporter)
      .task(id: accountManager.currentClient.id) {
        let client = accountManager.currentClient
        if let namespace { quickLook.namespace = namespace }
        currentAccount.setClient(client: client)
        currentInstance.setClient(client: client)
        userPreferences.setClient(client: client)
        await currentInstance.fetchCurrentInstance()
        watcher.setClient(client: client, instanceStreamingURL: currentInstance.instance?.streamingURL)
        if client.isAuth {
          watcher.watch(streams: [.user, .direct])
        } else {
          watcher.stopWatching()
        }
      }
      .task(id: accountManager.pushAccounts.map(\.token)) {
        pushNotifications.tokens = accountManager.pushAccounts.map(\.token)
      }
  }
}
```

说明：
- `.task(id:)` 钩子响应账号/客户端变更，重新设置服务和监听器状态。
- 修饰符聚焦于全局连接，功能特定的状态保留在功能内部。
- 根据项目调整类型（AccountManager、StreamWatcher 等）。

## SwiftData / ModelContainer

在根级安装 `ModelContainer`，让所有功能视图共享同一个 store。保持列表最小化，仅包含需要持久化的模型。

```swift
extension View {
  func withModelContainer() -> some View {
    modelContainer(for: [Draft.self, LocalTimeline.self, TagGroup.self])
  }
}
```

原因：单一容器避免了每个 Sheet 或标签页重复 store，保持数据一致性。

## Sheet 路由（枚举驱动）

用小型枚举和辅助修饰符集中 Sheet。

```swift
enum SheetDestination: Identifiable {
  case composer
  case settings
  var id: String { String(describing: self) }
}

extension View {
  func withSheetDestinations(sheet: Binding<SheetDestination?>) -> some View {
    sheet(item: sheet) { destination in
      switch destination {
      case .composer:
        ComposerView().withEnvironments()
      case .settings:
        SettingsView().withEnvironments()
      }
    }
  }
}
```

原因：枚举驱动的 Sheet 保持展示集中且可测试，添加新 Sheet 只需添加一个枚举 case 和一个 switch 分支。

## 适用场景

- 共享环境对象和服务的多包/多模块应用。
- 需要响应账号/客户端变更并安全地重新连接流式/推送的应用。
- 任何希望一致的 TabView + NavigationStack + Sheet 连接而不重复环境设置的应用。

## 注意事项

- 保持依赖修饰符精简，不要放入功能状态或重量级逻辑。
- 确保 `.task(id:)` 工作轻量或适当取消，长时间运行的工作属于服务。
- 如果存在未认证客户端，对流式/监听调用进行门控，避免重连风暴。
