# macOS 设置

## 意图

当使用 SwiftUI 的 `Settings` 场景构建 macOS 设置窗口时使用。

## 核心模式

- 在 `App` 中声明 Settings 场景，仅在 macOS 上编译。
- 将设置内容放在专门的根视图（`SettingsView`）中，使用 `@AppStorage` 驱动值。
- 超过一个分类时使用 `TabView` 对设置进行分组。
- 在每个标签页中使用 `Form` 保持控件对齐和可访问性。
- 使用 `OpenSettingsAction` 或 `SettingsLink` 作为应用内进入设置窗口的入口。

## 示例：设置场景

```swift
@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    #if os(macOS)
    Settings {
      SettingsView()
    }
    #endif
  }
}
```

## 示例：标签式设置视图

```swift
@MainActor
struct SettingsView: View {
  @AppStorage("showPreviews") private var showPreviews = true
  @AppStorage("fontSize") private var fontSize = 12.0

  var body: some View {
    TabView {
      Form {
        Toggle("Show Previews", isOn: $showPreviews)
        Slider(value: $fontSize, in: 9...96) {
          Text("Font Size (\(fontSize, specifier: "%.0f") pts)")
        }
      }
      .tabItem { Label("General", systemImage: "gear") }

      Form {
        Toggle("Enable Advanced Mode", isOn: .constant(false))
      }
      .tabItem { Label("Advanced", systemImage: "star") }
    }
    .scenePadding()
    .frame(maxWidth: 420, minHeight: 240)
  }
}
```

## 跳过导航

- 除非确实需要深层推送导航，否则避免将 `SettingsView` 包装在 `NavigationStack` 中。
- 优先使用标签页或分区，Settings 已作为独立窗口呈现，应该感觉是扁平的。
- 如果必须展示层级设置，使用单一的 `NavigationSplitView` 配合分类侧边栏列表。

## 陷阱

- 不要复用仅限 iOS 的设置布局（全屏堆栈、重工具栏流程）。
- 避免在 `Form` 内使用大型自定义视图层级，保持行聚焦且可访问。
