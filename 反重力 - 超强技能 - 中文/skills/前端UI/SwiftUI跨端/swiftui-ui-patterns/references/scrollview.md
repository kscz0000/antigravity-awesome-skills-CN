# ScrollView 与 Lazy 堆栈

## 意图

当需要自定义布局、混合内容或水平/网格滚动时，使用 `ScrollView` 配合 `LazyVStack`、`LazyHStack` 或 `LazyVGrid`。

## 核心模式

- 聊天类或自定义信息流布局优先使用 `ScrollView` + `LazyVStack`。
- 芯片、标签、头像和媒体条使用 `ScrollView(.horizontal)` + `LazyHStack`。
- 图标/媒体网格使用 `LazyVGrid`，尽可能使用自适应列。
- 滚动到顶部/底部和基于锚点的跳转使用 `ScrollViewReader`。
- 应固定在键盘上方的输入栏使用 `safeAreaInset(edge:)`。

## 示例：垂直自定义信息流

```swift
@MainActor
struct ConversationView: View {
  private enum Constants { static let bottomAnchor = "bottom" }
  @State private var scrollProxy: ScrollViewProxy?

  var body: some View {
    ScrollViewReader { proxy in
      ScrollView {
        LazyVStack {
          ForEach(messages) { message in
            MessageRow(message: message)
              .id(message.id)
          }
          Color.clear.frame(height: 1).id(Constants.bottomAnchor)
        }
        .padding(.horizontal, .layoutPadding)
      }
      .safeAreaInset(edge: .bottom) {
        MessageInputBar()
      }
      .onAppear {
        scrollProxy = proxy
        withAnimation {
          proxy.scrollTo(Constants.bottomAnchor, anchor: .bottom)
        }
      }
    }
  }
}
```

## 示例：水平芯片

```swift
ScrollView(.horizontal, showsIndicators: false) {
  LazyHStack(spacing: 8) {
    ForEach(chips) { chip in
      ChipView(chip: chip)
    }
  }
}
```

## 示例：自适应网格

```swift
let columns = [GridItem(.adaptive(minimum: 120))]

ScrollView {
  LazyVGrid(columns: columns, spacing: 8) {
    ForEach(items) { item in
      GridItemView(item: item)
    }
  }
  .padding(8)
}
```

## 设计要点

- 当项目数量大或未知时使用 `Lazy*` 堆栈。
- 对于小型固定内容使用非惰性堆栈，避免惰性加载的开销。
- 使用 `ScrollViewReader` 时保持 ID 稳定。
- 滚动到指定 ID 时优先使用显式动画（`withAnimation`）。

## 陷阱

- 避免嵌套同轴的滚动视图，会导致手势冲突。
- 没有明确理由不要在同层级混用 `List` 和 `ScrollView`。
- 对少量内容过度使用 `LazyVStack` 会增加不必要的复杂度。
