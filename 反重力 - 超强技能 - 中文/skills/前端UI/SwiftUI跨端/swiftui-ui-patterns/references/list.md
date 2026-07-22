# List 与 Section

## 意图

使用 `List` 构建信息流内容和设置行，利用内置的行复用、选择和无障碍功能。

## 核心模式

- 大量垂直滚动的重复行内容优先使用 `List`。
- 使用 `Section` 头部对相关行进行分组。
- 需要滚动到顶部或跳转到指定 ID 时配合 `ScrollViewReader`。
- 现代信息流布局使用 `.listStyle(.plain)`。
- 多分区的发现/搜索页面使用 `.listStyle(.grouped)`，分组有助于信息组织。
- 需要主题化表面时应用 `.scrollContentBackground(.hidden)` + 自定义背景。
- 使用 `.listRowInsets(...)` 和 `.listRowSeparator(.hidden)` 调整行间距和分隔线。
- 使用 `.environment(\.defaultMinListRowHeight, ...)` 控制紧凑列表布局。

## 示例：带滚动到顶部的信息流列表

```swift
@MainActor
struct TimelineListView: View {
  @Environment(\.selectedTabScrollToTop) private var selectedTabScrollToTop
  @State private var scrollToId: String?

  var body: some View {
    ScrollViewReader { proxy in
      List {
        ForEach(items) { item in
          TimelineRow(item: item)
            .id(item.id)
            .listRowInsets(.init(top: 12, leading: 16, bottom: 6, trailing: 16))
            .listRowSeparator(.hidden)
        }
      }
      .listStyle(.plain)
      .environment(\.defaultMinListRowHeight, 1)
      .onChange(of: scrollToId) { _, newValue in
        if let newValue {
          proxy.scrollTo(newValue, anchor: .top)
          scrollToId = nil
        }
      }
      .onChange(of: selectedTabScrollToTop) { _, newValue in
        if newValue == 0 {
          withAnimation {
            proxy.scrollTo(ScrollToView.Constants.scrollToTop, anchor: .top)
          }
        }
      }
    }
  }
}
```

## 示例：设置式列表

```swift
@MainActor
struct SettingsView: View {
  var body: some View {
    List {
      Section("General") {
        NavigationLink("Display") { DisplaySettingsView() }
        NavigationLink("Haptics") { HapticsSettingsView() }
      }
      Section("Account") {
        Button("Sign Out", role: .destructive) {}
      }
    }
    .listStyle(.insetGrouped)
  }
}
```

## 设计要点

- 动态信息流、设置以及任何需要行语义的 UI 使用 `List`。
- 使用稳定 ID 保持动画和滚动定位可靠。
- 应端到端可点击的行优先使用 `.contentShape(Rectangle())`。
- 数据源支持时使用 `.refreshable` 实现下拉刷新。

## 陷阱

- 避免在 `List` 行内使用重量级自定义布局，改用 `ScrollView` + `LazyVStack`。
- 混用 `List` 和嵌套 `ScrollView` 时注意可能的手势冲突。
