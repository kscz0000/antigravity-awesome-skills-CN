# 覆盖层与 Toast 提示

## 意图

使用覆盖层展示临时 UI（Toast、横幅、加载器），不影响布局。

## 核心模式

- 使用 `.overlay(alignment:)` 放置全局 UI，不改变底层布局。
- 保持覆盖层轻量且可关闭。
- 当多个功能需要触发 Toast 时，使用专门的 `ToastCenter`（或类似机制）管理全局状态。

## 示例：Toast 覆盖层

```swift
struct AppRootView: View {
  @State private var toast: Toast?

  var body: some View {
    content
      .overlay(alignment: .top) {
        if let toast {
          ToastView(toast: toast)
            .transition(.move(edge: .top).combined(with: .opacity))
            .onAppear {
              DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                withAnimation { self.toast = nil }
              }
            }
        }
      }
  }
}
```

## 设计要点

- 临时 UI 优先使用覆盖层，而非嵌入布局堆栈。
- 使用过渡动画和短自动关闭计时器。
- 将覆盖层对齐到明确的边缘（`.top` 或 `.bottom`）。

## 陷阱

- 避免阻塞所有交互的覆盖层，除非确实需要。
- 不要叠加多个覆盖层，使用队列或替换当前 Toast。
