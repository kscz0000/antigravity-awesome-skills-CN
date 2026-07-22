# 顶部栏覆盖层（iOS 26+ 及兼容方案）

## 意图

在滚动内容上方放置自定义的顶部选择器或胶囊栏，iOS 26 使用 `safeAreaBar(.top)`，更早版本使用兼容的回退方案。

## iOS 26+ 方案

使用 `safeAreaBar(edge: .top)` 将视图附加到安全区域栏。

```swift
if #available(iOS 26.0, *) {
  content
    .safeAreaBar(edge: .top) {
      TopSelectorView()
        .padding(.horizontal, .layoutPadding)
    }
}
```

## 旧版 iOS 回退方案

使用 `.safeAreaInset(edge: .top)` 并隐藏工具栏背景以避免双层叠加。

```swift
content
  .toolbarBackground(.hidden, for: .navigationBar)
  .safeAreaInset(edge: .top, spacing: 0) {
    VStack(spacing: 0) {
      TopSelectorView()
        .padding(.vertical, 8)
        .padding(.horizontal, .layoutPadding)
        .background(Color.primary.opacity(0.06))
        .background(Material.ultraThin)
      Divider()
    }
  }
```

## 设计要点

- 可用时优先使用 `safeAreaBar`，它与导航栏的集成更好。
- 回退方案中使用微妙的背景 + 分割线来与内容保持分隔。
- 保持选择器高度紧凑，避免将内容推得太低。

## 陷阱

- 不要叠加多个顶部 inset，否则会产生多余的间距。
- 避免使用与导航栏冲突的厚重不透明背景。
