# 网格

## 意图

使用 `LazyVGrid` 构建图标选择器、媒体画廊和密集的视觉选择布局，其中项目按列对齐。

## 核心模式

- 需要跨设备尺寸自适应的布局使用 `.adaptive` 列。
- 需要固定列数时使用多个 `.flexible` 列。
- 间距保持一致且小，避免不均匀的间隙。
- 需要方形缩略图时在网格单元内使用 `GeometryReader`。

## 示例：自适应图标网格

```swift
let columns = [GridItem(.adaptive(minimum: 120, maximum: 1024))]

LazyVGrid(columns: columns, spacing: 6) {
  ForEach(icons) { icon in
    Button {
      select(icon)
    } label: {
      ZStack(alignment: .bottomTrailing) {
        Image(icon.previewName)
          .resizable()
          .aspectRatio(contentMode: .fit)
          .cornerRadius(6)
        if icon.isSelected {
          Image(systemName: "checkmark.seal.fill")
            .padding(4)
            .tint(.green)
        }
      }
    }
    .buttonStyle(.plain)
  }
}
```

## 示例：固定三列媒体网格

```swift
LazyVGrid(
  columns: [
    .init(.flexible(minimum: 100), spacing: 4),
    .init(.flexible(minimum: 100), spacing: 4),
    .init(.flexible(minimum: 100), spacing: 4),
  ],
  spacing: 4
) {
  ForEach(items) { item in
    GeometryReader { proxy in
      ThumbnailView(item: item)
        .frame(width: proxy.size.width, height: proxy.size.width)
    }
    .aspectRatio(1, contentMode: .fit)
  }
}
```

## 设计要点

- 大型集合使用 `LazyVGrid`，避免对大数据集使用非惰性网格。
- 需要时使用 `.contentShape(Rectangle())` 保持点击目标全区域覆盖。
- 设置选择器和灵活布局优先使用自适应网格。

## 陷阱

- 避免在每个网格单元中使用重量级覆盖层，成本可能很高。
- 没有明确理由不要嵌套网格。
