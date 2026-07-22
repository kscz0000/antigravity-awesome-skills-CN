# 主题化与动态字体

## 意图

提供一套简洁、可扩展的主题方案，保持视图代码的语义化和一致性。

## 核心模式

- 使用单一 `Theme` 对象作为数据源（颜色、字体、间距）。
- 在应用根级注入主题，视图中通过 `@Environment(Theme.self)` 读取。
- 优先使用语义化颜色（`primaryBackground`、`secondaryBackground`、`label`、`tint`），而非原始颜色。
- 用户主题控制放在专门的设置页面中。
- 通过自定义字体或 `.font(.scaled...)` 实现 Dynamic Type 缩放。

## 示例：Theme 对象

```swift
@MainActor
@Observable
final class Theme {
  var tintColor: Color = .blue
  var primaryBackground: Color = .white
  var secondaryBackground: Color = .gray.opacity(0.1)
  var labelColor: Color = .primary
  var fontSizeScale: Double = 1.0
}
```

## 示例：在应用根级注入

```swift
@main
struct MyApp: App {
  @State private var theme = Theme()

  var body: some Scene {
    WindowGroup {
      AppView()
        .environment(theme)
    }
  }
}
```

## 示例：视图中使用

```swift
struct ProfileView: View {
  @Environment(Theme.self) private var theme

  var body: some View {
    VStack {
      Text("Profile")
        .foregroundStyle(theme.labelColor)
    }
    .background(theme.primaryBackground)
  }
}
```

## 设计要点

- 主题值保持语义化和最小化，避免重复系统颜色。
- 需要时将用户选择的主题值存储在持久化存储中。
- 确保文本和背景之间的对比度。

## 陷阱

- 避免在视图中散落原始 `Color` 值，这会破坏一致性。
- 不要将主题绑定到单个视图的本地状态。
- 避免仅用 `@Environment(\.colorScheme)` 作为主题控制，它应该作为主题的补充。
