# 菜单栏

## 意图

当使用 SwiftUI commands 添加或自定义 macOS/iPadOS 菜单栏时使用。

## 核心模式

- 在 `Scene` 层级通过 `.commands { ... }` 添加命令。
- 当 UI 包含导航侧边栏时使用 `SidebarCommands()`。
- 使用 `CommandMenu` 添加应用专属菜单，并对相关操作进行分组。
- 使用 `CommandGroup` 在系统分组前/后插入项目或替换它们。
- 使用 `FocusedValue` 实现依赖活动场景的上下文敏感菜单项。

## 示例：基本命令菜单

```swift
@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    .commands {
      CommandMenu("Actions") {
        Button("Run", action: run)
          .keyboardShortcut("R")
        Button("Stop", action: stop)
          .keyboardShortcut(".")
      }
    }
  }

  private func run() {}
  private func stop() {}
}
```

## 示例：插入和替换分组

```swift
WindowGroup {
  ContentView()
}
.commands {
  CommandGroup(before: .systemServices) {
    Button("Check for Updates") { /* open updater */ }
  }

  CommandGroup(after: .newItem) {
    Button("New from Clipboard") { /* create item */ }
  }

  CommandGroup(replacing: .help) {
    Button("User Manual") { /* open docs */ }
  }
}
```

## 示例：聚焦菜单状态

```swift
@Observable
final class DataModel {
  var items: [String] = []
}

struct ContentView: View {
  @State private var model = DataModel()

  var body: some View {
    List(model.items, id: \.self) { item in
      Text(item)
    }
    .focusedSceneValue(model)
  }
}

struct ItemCommands: Commands {
  @FocusedValue(DataModel.self) private var model: DataModel?

  var body: some Commands {
    CommandGroup(after: .newItem) {
      Button("New Item") {
        model?.items.append("Untitled")
      }
      .disabled(model == nil)
    }
  }
}
```

## 菜单栏与设置

- 定义 `Settings` 场景会自动在 macOS 上添加设置菜单项。
- 如果需要在应用内部自定义入口点，使用 `OpenSettingsAction` 或 `SettingsLink`。

## 陷阱

- 避免在多个命令分组中注册相同的键盘快捷键。
- 不要将菜单项作为关键功能的唯一可发现入口。
