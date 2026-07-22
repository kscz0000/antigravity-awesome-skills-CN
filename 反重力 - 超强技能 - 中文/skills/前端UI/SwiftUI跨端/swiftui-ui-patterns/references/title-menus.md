# 标题菜单

## 意图

在导航栏的标题上添加菜单，提供上下文相关的筛选或快捷操作，无需额外的 UI 元素。

## 核心模式

- 使用 `ToolbarTitleMenu` 将菜单附加到导航标题。
- 保持菜单内容紧凑并用分隔线分组。

## 示例：筛选标题菜单

```swift
@ToolbarContentBuilder
private var toolbarView: some ToolbarContent {
  ToolbarTitleMenu {
    Button("Latest") { timeline = .latest }
    Button("Resume") { timeline = .resume }
    Divider()
    Button("Local") { timeline = .local }
    Button("Federated") { timeline = .federated }
  }
}
```

## 示例：附加到视图

```swift
NavigationStack {
  TimelineView()
    .toolbar {
      toolbarView
    }
}
```

## 示例：标题 + 菜单组合

```swift
struct TimelineScreen: View {
  @State private var timeline: TimelineFilter = .home

  var body: some View {
    NavigationStack {
      TimelineView()
        .toolbar {
          ToolbarItem(placement: .principal) {
            VStack(spacing: 2) {
              Text(timeline.title)
                .font(.headline)
              Text(timeline.subtitle)
                .font(.caption)
                .foregroundStyle(.secondary)
            }
          }

          ToolbarTitleMenu {
            Button("Home") { timeline = .home }
            Button("Local") { timeline = .local }
            Button("Federated") { timeline = .federated }
          }
        }
        .navigationBarTitleDisplayMode(.inline)
    }
  }
}
```

## 示例：带菜单的标题 + 副标题

```swift
ToolbarItem(placement: .principal) {
  VStack(spacing: 2) {
    Text(title)
      .font(.headline)
    Text(subtitle)
      .font(.caption)
      .foregroundStyle(.secondary)
  }
}
```

## 设计要点

- 仅在需要筛选或上下文切换时显示标题菜单。
- 保持标题可读，避免过长的标签被截断。
- 需要额外上下文时在标题下方使用次要文本。

## 陷阱

- 不要在菜单中堆砌太多选项。
- 避免将标题菜单用于破坏性操作。
