# 加载与占位符

当视图需要一致的加载状态（骨架屏、脱敏、空状态）而不阻塞交互时使用。

## 推荐模式

- **脱敏占位符**用于列表/详情内容，在加载期间保持布局。
- **ContentUnavailableView**用于加载完成后的空数据或错误状态。
- **ProgressView**仅用于短暂的全局操作（在内容密集的页面中谨慎使用）。

## 推荐方式

1. 保留真实布局，渲染占位数据，然后应用 `.redacted(reason: .placeholder)`。
2. 对于列表，显示固定数量的占位行（避免无限旋转器）。
3. 加载完成但数据为空时切换到 `ContentUnavailableView`。

## 陷阱

- 脱敏期间不要触发布局偏移，保持帧稳定。
- 避免嵌套多个旋转器，每个区域使用一个加载指示器。
- 占位符数量保持少量（3–6），减少低端设备上的卡顿。

## 最小用法

```swift
VStack {
  if isLoading {
    ForEach(0..<3, id: \.self) { _ in
      RowView(model: .placeholder())
    }
    .redacted(reason: .placeholder)
  } else if items.isEmpty {
    ContentUnavailableView("No items", systemImage: "tray")
  } else {
    ForEach(items) { item in RowView(model: item) }
  }
}
```
