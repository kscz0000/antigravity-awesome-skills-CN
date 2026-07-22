# 搭建 SwiftPM macOS 应用（无需 Xcode）

## 步骤
1) 创建仓库并初始化 SwiftPM：
```
mkdir MyApp
cd MyApp
swift package init --type executable
```

2) 更新 `Package.swift`，将目标设为 macOS 并为应用定义可执行目标。

3) 在 `Sources/MyApp/` 下创建应用入口点。
- 如需带窗口的应用且只需最少的 AppKit 粘合代码，请使用 SwiftUI。
- 如需菜单栏或附属样式应用，请使用 AppKit。

4) 如需应用资源，添加：
```
resources: [.process("Resources")]
```
并创建 `Sources/MyApp/Resources/`。

5) 添加 `version.env` 文件（供打包模板使用）：
```
MARKETING_VERSION=0.1.0
BUILD_NUMBER=1
```

6) 将 `assets/templates/` 中的脚本模板复制到你的仓库（例如 `Scripts/`）。

## 最小 Package.swift（示例）
```
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.macOS(.v14)],
    targets: [
        .executableTarget(
            name: "MyApp",
            path: "Sources/MyApp",
            resources: [
                .process("Resources")
            ])
    ]
)
```

## 最小 SwiftUI 入口点（示例）
```
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            Text("Hello")
        }
    }
}
```

## 最小 AppKit 入口点（示例）
```
import AppKit

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Initialize app state here.
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
```
