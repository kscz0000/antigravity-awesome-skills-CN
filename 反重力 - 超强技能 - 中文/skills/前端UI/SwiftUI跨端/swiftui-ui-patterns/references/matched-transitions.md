# 匹配过渡

## 意图

使用匹配过渡在源视图（缩略图、头像）和目标视图（Sheet、详情、查看器）之间创建平滑的连续性。

## 核心模式

- 使用共享的 `Namespace` 和稳定的源 ID。
- iOS 26+ 使用 `matchedTransitionSource` + `navigationTransition(.zoom(...))`。
- 视图层级内的原位过渡使用 `matchedGeometryEffect`。
- ID 在视图更新间保持稳定（避免随机 UUID）。

## 示例：媒体预览到全屏查看器（iOS 26+）

```swift
struct MediaPreview: View {
  @Namespace private var namespace
  @State private var selected: MediaAttachment?

  var body: some View {
    ThumbnailView()
      .matchedTransitionSource(id: selected?.id ?? "", in: namespace)
      .sheet(item: $selected) { item in
        MediaViewer(item: item)
          .navigationTransition(.zoom(sourceID: item.id, in: namespace))
      }
  }
}
```

## 示例：视图内的匹配几何

```swift
struct ToggleBadge: View {
  @Namespace private var space
  @State private var isOn = false

  var body: some View {
    Button {
      withAnimation(.spring) { isOn.toggle() }
    } label: {
      Image(systemName: isOn ? "eye" : "eye.slash")
        .matchedGeometryEffect(id: "icon", in: space)
    }
  }
}
```

## 设计要点

- 跨页面过渡优先使用 `matchedTransitionSource`。
- 保持源和目标尺寸合理，避免突兀的缩放变化。
- 状态驱动的过渡使用 `withAnimation`。

## 陷阱

- 不要使用不稳定的 ID，会破坏过渡效果。
- 避免不匹配的形状（如方形到圆形），除非设计预期如此。
