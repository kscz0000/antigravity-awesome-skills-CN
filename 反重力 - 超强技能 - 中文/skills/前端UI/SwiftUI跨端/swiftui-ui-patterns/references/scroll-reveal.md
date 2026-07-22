# 滚动展示详情页面

## 意图

当详情页面先展示主表面、背后有次级内容，且希望用户通过滚动或滑动而非点击单独按钮来展示次级层时，使用此模式。

典型适用场景：

- 展示操作或元数据的媒体详情页
- 过渡到结构化详情的地图、卡片或画布
- 带有第二页"操作"或"洞察"的全屏查看器

## 核心模式

将交互构建为分页式垂直 `ScrollView`，包含两个区域：

1. 与视口等大的主区域
2. 主区域下方的次级区域

从垂直内容偏移量派生标准化的 `progress` 值，并以此单一值驱动所有视觉变化。

除非仅靠滚动无法表达，否则避免将展示视为独立的手势系统。

## 最小结构

```swift
private enum DetailSection: Hashable {
  case primary
  case secondary
}

struct DetailSurface: View {
  @State private var revealProgress: CGFloat = 0
  @State private var secondaryHeight: CGFloat = 1

  var body: some View {
    GeometryReader { geometry in
      ScrollViewReader { proxy in
        ScrollView(.vertical, showsIndicators: false) {
          VStack(spacing: 0) {
            PrimaryContent(progress: revealProgress)
              .frame(height: geometry.size.height)
              .id(DetailSection.primary)

            SecondaryContent(progress: revealProgress)
              .id(DetailSection.secondary)
              .onGeometryChange(for: CGFloat.self) { geo in
                geo.size.height
              } action: { newHeight in
                secondaryHeight = max(newHeight, 1)
              }
          }
          .scrollTargetLayout()
        }
        .scrollTargetBehavior(.paging)
        .onScrollGeometryChange(for: CGFloat.self, of: { scroll in
          scroll.contentOffset.y + scroll.contentInsets.top
        }) { _, offset in
          revealProgress = (offset / secondaryHeight).clamped(to: 0...1)
        }
        .safeAreaInset(edge: .bottom) {
          ChevronAffordance(progress: revealProgress) {
            withAnimation(.smooth) {
              let target: DetailSection = revealProgress < 0.5 ? .secondary : .primary
              proxy.scrollTo(target, anchor: .top)
            }
          }
        }
      }
    }
  }
}
```

## 设计要点

- 当交互应感觉像在状态间分页时，让主区域与视口等大。
- 从真实滚动偏移量计算 `progress`，而非使用重复的布尔值如 `isExpanded`、`isShowingSecondary` 和 `isSnapped`。
- 使用 `progress` 驱动 `offset`、`opacity`、`blur`、`scaleEffect` 和工具栏状态，使整个页面保持同步。
- 当需要点击主内容或箭头指示器进行程序化吸附时，使用 `ScrollViewReader`。
- 当需要确定的区域状态用于触觉反馈、提示消除、分析或无障碍通知时，使用 `onScrollTargetVisibilityChange`。

## 共享控件变形

如果一个控件看起来从主表面移动到了次级内容中，不要渲染两个完全可见的副本。

而是：

- 在主区域暴露源锚点
- 在次级区域暴露目标锚点
- 渲染一个使用 `progress` 插值位置和大小的覆盖层

```swift
Color.clear
  .anchorPreference(key: ControlAnchorKey.self, value: .bounds) { anchor in
    ["source": anchor]
  }

Color.clear
  .anchorPreference(key: ControlAnchorKey.self, value: .bounds) { anchor in
    ["destination": anchor]
  }

.overlayPreferenceValue(ControlAnchorKey.self) { anchors in
  MorphingControlOverlay(anchors: anchors, progress: revealProgress)
}
```

这样可以保持运动连贯，避免重复点击目标的 bug。

## 触觉反馈与指示器

- 在展示开始时使用轻阈值触觉反馈，在接近确认状态时使用更强的触觉反馈。
- 当 `progress` 接近零时保持可见的指示器（如箭头或胶囊）。
- 在次级区域激活时翻转、淡出或模糊指示器。

## 交互保护

- 当冲突模式激活时（如捏合缩放、裁剪或全屏媒体操作），禁用垂直滚动。
- 在次级内容展示后应消失的覆盖层上禁用命中测试。
- 避免同轴嵌套滚动视图，除非内层视图在展示期间实际上是静态或禁用的。

## 陷阱

- 不要硬编码 progress 除数。测量次级区域高度或其他真实的展示距离。
- 不要为同一属性混合多个动画源。如果 `progress` 驱动它，就不要为该属性设置其他动画。
- 除非其他 API 需要，否则不要存储派生状态如 `isSecondaryVisible`。优先从 `progress` 或可见滚动目标派生。
- 测量高度时注意布局反馈循环。钳制零值，仅在测量高度实际变化时更新。

## 具体示例

- Pool iOS 瓷砖详情展示：`/Users/dimillian/Documents/Dev/Pool/pool-ios/Pool/Sources/Features/Tile/Detail/TileDetailView.swift`
- 次级内容锚点示例：`/Users/dimillian/Documents/Dev/Pool/pool-ios/Pool/Sources/Features/Tile/Detail/TileDetailIntentListView.swift`
