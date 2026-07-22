# 分栏视图与多列布局

## 意图

为 iPad/macOS 提供轻量、可自定义的多列布局，不依赖 `NavigationSplitView`。

## 自定义分栏模式（手动 HStack）

当你需要完全控制列大小、行为和环境调整时使用。

```swift
@MainActor
struct AppView: View {
  @Environment(\.horizontalSizeClass) private var horizontalSizeClass
  @AppStorage("showSecondaryColumn") private var showSecondaryColumn = true

  var body: some View {
    HStack(spacing: 0) {
      primaryColumn
      if shouldShowSecondaryColumn {
        Divider().edgesIgnoringSafeArea(.all)
        secondaryColumn
      }
    }
  }

  private var shouldShowSecondaryColumn: Bool {
    horizontalSizeClass == .regular
      && showSecondaryColumn
  }

  private var primaryColumn: some View {
    TabView { /* tabs */ }
  }

  private var secondaryColumn: some View {
    NotificationsTab()
      .environment(\.isSecondaryColumn, true)
      .frame(maxWidth: .secondaryColumnWidth)
  }
}
```

## 自定义方案说明

- 使用共享偏好或设置来切换次级列。
- 注入环境标志（如 `isSecondaryColumn`）让子视图可以适配行为。
- 次级列优先使用固定或有上限的宽度，避免布局抖动。

## 替代方案：NavigationSplitView

`NavigationSplitView` 可以自动处理侧边栏 + 详情 + 补充列，但在以下场景更难自定义：
- 独立于选择的专用通知列，
- 自定义尺寸，或
- 每列不同的工具栏行为。

```swift
@MainActor
struct AppView: View {
  var body: some View {
    NavigationSplitView {
      SidebarView()
    } content: {
      MainContentView()
    } detail: {
      NotificationsView()
    }
  }
}
```

## 如何选择

- 当需要完全控制或非标准次级列时，使用手动 HStack 分栏。
- 当希望最少自定义的标准系统布局时，使用 `NavigationSplitView`。
