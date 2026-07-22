# 媒体（图片、视频、查看器）

## 意图

使用一致的模式加载图片、预览媒体和展示全屏查看器。

## 核心模式

- 使用 `LazyImage`（或 `AsyncImage`）加载远程图片并展示加载状态。
- 内联媒体优先使用轻量级预览组件。
- 使用共享的查看器状态（如 `QuickLook`）展示全屏媒体查看器。
- 桌面/visionOS 使用 `openWindow`，iOS 使用 sheet。

## 示例：内联媒体预览

```swift
struct MediaPreviewRow: View {
  @Environment(QuickLook.self) private var quickLook

  let attachments: [MediaAttachment]

  var body: some View {
    ScrollView(.horizontal, showsIndicators: false) {
      HStack {
        ForEach(attachments) { attachment in
          LazyImage(url: attachment.previewURL) { state in
            if let image = state.image {
              image.resizable().aspectRatio(contentMode: .fill)
            } else {
              ProgressView()
            }
          }
          .frame(width: 120, height: 120)
          .clipped()
          .onTapGesture {
            quickLook.prepareFor(
              selectedMediaAttachment: attachment,
              mediaAttachments: attachments
            )
          }
        }
      }
    }
  }
}
```

## 示例：全局媒体查看器 Sheet

```swift
struct AppRoot: View {
  @State private var quickLook = QuickLook.shared

  var body: some View {
    content
      .environment(quickLook)
      .sheet(item: $quickLook.selectedMediaAttachment) { selected in
        MediaUIView(selectedAttachment: selected, attachments: quickLook.mediaAttachments)
      }
  }
}
```

## 设计要点

- 预览保持轻量，在查看器中加载完整媒体。
- 使用共享查看器状态，让任何视图都能打开媒体而无需逐层传递属性。
- 使用单一入口点（sheet/window）展示查看器，避免重复。

## 陷阱

- 避免在列表行中加载全尺寸图片，使用缩放后的预览。
- 不要同时展示多个查看器 Sheet，保持单一数据源。
