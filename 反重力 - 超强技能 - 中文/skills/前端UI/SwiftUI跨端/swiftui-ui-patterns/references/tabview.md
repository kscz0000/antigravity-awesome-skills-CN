# TabView

## 意图

使用此模式构建可扩展的多平台标签架构，具备：
- 标签标识和内容的单一数据源，
- 平台特定的标签集和侧边栏分区，
- 来自数据的动态标签，
- 特殊标签（如发布）的拦截钩子。

## 核心架构

- `AppTab` 枚举定义标识、标签、图标和内容构建器。
- `SidebarSections` 枚举为侧边栏分区对标签进行分组。
- `AppView` 持有 `TabView` 和选择绑定，通过 `updateTab` 路由标签切换。

## 示例：带副作用的自定义绑定

当标签选择需要副作用时使用，例如拦截特殊标签来执行操作而非切换选中状态。

```swift
@MainActor
struct AppView: View {
  @Binding var selectedTab: AppTab

  var body: some View {
    TabView(selection: .init(
      get: { selectedTab },
      set: { updateTab(with: $0) }
    )) {
      ForEach(availableSections) { section in
        TabSection(section.title) {
          ForEach(section.tabs) { tab in
            Tab(value: tab) {
              tab.makeContentView(
                homeTimeline: $timeline,
                selectedTab: $selectedTab,
                pinnedFilters: $pinnedFilters
              )
            } label: {
              tab.label
            }
            .tabPlacement(tab.tabPlacement)
          }
        }
        .tabPlacement(.sidebarOnly)
      }
    }
  }

  private func updateTab(with newTab: AppTab) {
    if newTab == .post {
      // Intercept special tabs (compose) instead of changing selection.
      presentComposer()
      return
    }
    selectedTab = newTab
  }
}
```

## 示例：无副作用的直接绑定

当选择纯粹由状态驱动时使用。

```swift
@MainActor
struct AppView: View {
  @Binding var selectedTab: AppTab

  var body: some View {
    TabView(selection: $selectedTab) {
      ForEach(availableSections) { section in
        TabSection(section.title) {
          ForEach(section.tabs) { tab in
            Tab(value: tab) {
              tab.makeContentView(
                homeTimeline: $timeline,
                selectedTab: $selectedTab,
                pinnedFilters: $pinnedFilters
              )
            } label: {
              tab.label
            }
            .tabPlacement(tab.tabPlacement)
          }
        }
        .tabPlacement(.sidebarOnly)
      }
    }
  }
}
```

## 设计要点

- 将标签标识和内容集中在 `AppTab` 的 `makeContentView(...)` 中。
- 使用 `Tab(value:)` 配合 `selection` 绑定实现状态驱动的标签选择。
- 通过 `updateTab` 路由选择变更，处理特殊标签和滚动到顶部的行为。
- 使用 `TabSection` + `.tabPlacement(.sidebarOnly)` 构建侧边栏结构。
- 在 `AppTab.tabPlacement` 中使用 `.tabPlacement(.pinned)` 实现单个固定标签；这通常用于 iOS 26 的 `.searchable` 标签内容，但也可用于任何标签。

## 动态标签模式

- `SidebarSections` 处理动态数据标签。
- `AppTab.anyTimelineFilter(filter:)` 将动态标签包装在单个枚举 case 中。
- 枚举通过 filter 类型为动态标签提供 label/icon/title。

## 陷阱

- 避免为标签添加 ViewModel，状态保留在本地或 `@Observable` 服务中。
- 不要将 `@Observable` 对象嵌套在其他 `@Observable` 对象内部。
- 确保 `AppTab.id` 值稳定，动态 case 应基于稳定 ID 进行哈希。
- 特殊标签（如发布）不应改变选择状态。
