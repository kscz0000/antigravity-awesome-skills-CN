# Brownfield：隔离方式

将 React Native + Expo 代码构建为预构建的原生库——Android 上为 **AAR**，iOS 上为 **XCFramework**——然后像使用任何其他依赖一样从现有原生应用中消费它。

## 何时使用

- 原生团队和 React Native 团队归属不同，或按不同节奏发布。
- 不强制要求原生团队安装 Node.js、Yarn 或 React Native 工具链。
- React Native 代码与原生应用位于不同的仓库或 monorepo 中。
- 你希望对现有原生构建流水线的影响尽可能小。

如果单一团队同时拥有两层代码、熟悉 React Native 工具链并需要深度集成，请参阅 [./brownfield-integrated.md](./brownfield-integrated.md)。

## 你将产出的产物

| 平台 | 产物                                                                                                                                                                                            | 默认位置                                              |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Android  | `{group}:{libraryName}:{version}` AAR                                                                                                                                                               | 默认发布到本地 Maven（`~/.m2`），也支持远程 Maven |
| iOS      | 一组 `.xcframework` —— 参见下方的 [iOS 部分](#ios)，了解 `ios.buildReactNativeFromSource`（SDK 56+ 默认 `false`）如何控制你将得到 5 个还是 2 个 framework，也可以通过 `--package` 生成单个 Swift Package | `./artifacts`                                                 |

JavaScript bundle 在 release 构建中**嵌入在产物内部**，因此生产环境下的原生应用在运行时无需 Metro。

## 前置条件

- **Expo SDK 55 或更高版本** — brownfield 支持、`expo-brownfield` 及所需的运行时类仅在 SDK 55+ 中可用。更早的 SDK 无法工作。
- **Node.js（LTS）** — 运行 JavaScript 和 Expo CLI。
- **Yarn** — 管理 JavaScript 依赖。

Node 和 Yarn 仅在**构建产物的环境**中需要。消费原生应用不需要它们。

---

## 1) 设置 Expo 项目

### 创建一个新的 Expo 项目

```sh
npx create-expo-app@latest my-project --template default@sdk-55
```

**请锁定到 SDK 55 或更高版本——更早的 SDK 不支持 brownfield。** 项目可以位于单独的仓库中，也可以与原生应用一同放在 monorepo 中；不需要放在原生项目内部。

### 安装 expo-brownfield

```sh
cd my-project
npx expo install expo-brownfield
```

该插件会自动注册到 `app.json` 中，默认值派生自你的应用配置。

### 配置插件（可选）

要覆盖自动生成的名称，请在 `app.json` 中展开插件配置项：

```json
{
  "expo": {
    "plugins": [
      [
        "expo-brownfield",
        {
          "ios": {
            "targetName": "MyBrownfield",
            "bundleIdentifier": "com.example.mybrownfield"
          },
          "android": {
            "libraryName": "mybrownfield",
            "group": "com.example",
            "package": "com.example.mybrownfield",
            "version": "1.0.0"
          }
        }
      ]
    ]
  }
}
```

**iOS 选项** — `targetName`（XCFramework 目标名）、`bundleIdentifier`（framework 的 bundle ID）。

**Android 选项** — `libraryName`（AAR 名）、`group`（Maven group ID）、`package`（Android 包名）、`version`（库版本）、`publishing`（Maven 发布目标 —— 参见 [发布 Android AAR](#发布-android-aar)）。

### 通过预构建的 Expo 模块加速 iOS 构建

启用 `expo-build-properties` 的 `ios.usePrecompiledModules`，使 `pod install` 将每个 Expo 模块作为预构建的 `.xcframework` 下载，而不是从源码编译。`build:ios` 会在 `ios/Pods/` 下检测这些 xcframework，并将它们与 brownfield framework、React、Hermes 以及 `ReactNativeDependencies` 一同打包进 Swift Package 输出。

```json
{
  "expo": {
    "plugins": [
      ["expo-build-properties", { "ios": { "usePrecompiledModules": true } }],
      "expo-brownfield"
    ]
  }
}
```

当检测到预编译模块时，`build:ios` 会为每个包固定为单一 flavor（`--debug` 或 `--release`）—— Swift Package Manager 对 `.binaryTarget(path:)` 没有 per-configuration 重载。每个 flavor 单独构建一次，并将两个包并列分发。

---

## 2) 构建原生库

### Android

```sh
npx expo-brownfield build:android
```

生成一个 AAR 并发布到本地 Maven 仓库 `~/.m2`。Maven 坐标来自插件配置 —— 例如 `com.example:mybrownfield:1.0.0`。

#### 发布 Android AAR

插件的 `publishing` 选项控制 AAR 的发布位置。未设置时，默认为本地 Maven。要推送到其他目标（例如共享的 CI Maven、内部的 Artifactory/Nexus，或被另一个构建拉入的目录），请显式声明发布目标：

```json
{
  "expo": {
    "plugins": [
      [
        "expo-brownfield",
        {
          "android": {
            "libraryName": "mybrownfield",
            "group": "com.example",
            "version": "1.0.0",
            "publishing": [
              { "type": "localMaven" },
              {
                "type": "localDirectory",
                "name": "build",
                "path": "./out/maven"
              },
              {
                "type": "remotePublic",
                "name": "company",
                "url": "https://maven.example.com/releases"
              },
              {
                "type": "remotePrivate",
                "name": "artifactory",
                "url": { "variable": "ARTIFACTORY_URL" },
                "username": { "variable": "ARTIFACTORY_USER" },
                "password": { "variable": "ARTIFACTORY_TOKEN" }
              }
            ]
          }
        }
      ]
    ]
  }
}
```

支持的 `type` 值：`localMaven`、`localDirectory`、`remotePublic`、`remotePrivate`。对于私有仓库，凭证和 URL 既可以接受内联字符串，也可以使用 `{ "variable": "ENV_VAR_NAME" }` 在发布时从环境变量读取。

默认情况下，`build:android` 会运行所有声明的发布任务。要从命令行选择特定的发布任务或仓库，请使用 CLI 标志：

```sh
npx expo-brownfield build:android --task publishReleasePublicationToCompanyRepository
npx expo-brownfield tasks:android   # 列出可用的发布任务和仓库
```

### iOS

```sh
npx expo-brownfield build:ios
```

输出到 `./artifacts`。输出的内容取决于 `ios.buildReactNativeFromSource` 标志（通过 `expo-build-properties` 设置）：

- **`buildReactNativeFromSource: false`**（SDK 56+ 上的默认值）— React Native 作为预构建二进制被消费，因此 `build:ios` 并排输出五个 xcframework：`{TargetName}.xcframework`、`React.xcframework`、`ReactNativeDependencies.xcframework`、`ExpoModulesJSI.xcframework` 和 `hermesvm.xcframework`。
- **`buildReactNativeFromSource: true`**（SDK 55 上的默认值，SDK 56+ 上可选择启用）— React Native 从源码编译并静态链接到 brownfield framework，最终留下两个 xcframework：`{TargetName}.xcframework` 和 `hermesvm.xcframework`。

要在 SDK 56+ 上强制使用源码构建，请在 `app.json` 中添加 `expo-build-properties`：

```json
{
  "expo": {
    "plugins": [
      ["expo-build-properties", { "ios": { "buildReactNativeFromSource": true } }],
      "expo-brownfield"
    ]
  }
}
```

**生成的产物集合中的每个 xcframework 都必须被嵌入消费应用中**（Embed & Sign）。下面的 Swift Package 输出（`--package`）会自动为你完成这一步。

> **iOS 部署目标：** brownfield 产物会继承 Expo 项目的 iOS 部署目标（SDK 56+ 上为 16.4）。消费应用的部署目标必须设置为 16.4 或更高；否则 Xcode 会拒绝链接嵌入的 framework。如果宿主应用使用的是更低的部署目标（例如 iOS 14.0），请在引入产物前先调高其 `IPHONEOS_DEPLOYMENT_TARGET`。

#### 以 Swift Package 形式交付（推荐）

传入 `--package [name]`，将输出打包成自包含的 Swift Package，而不是单独的 `.xcframework` 目录。然后宿主 iOS 应用通过 Xcode 中的 **Add Package Dependencies → Add Local** 引入该包，并自动链接所有打包的 framework —— 无需手动拖拽，也无需为每个 framework 切换 "Embed & Sign"。

```sh
npx expo-brownfield build:ios --release --package MyAppPackage
```

该标志接受一个可选的名称。如果省略，包名为 `{TargetName}Artifacts`。生成的目录是一个完整的 Swift Package：

```
artifacts/MyAppPackage/
├── Package.swift
└── xcframeworks/
    ├── MyAppPackage.xcframework
    ├── hermesvm.xcframework
    ├── React.xcframework
    └── ReactNativeDependencies.xcframework
```

当启用了 `usePrecompiledModules` 时，包目录会带上构建 flavor 后缀（例如 `MyAppPackage-release/`），并包含每个预构建的 Expo 模块 xcframework。请分别运行 `build:ios --debug --package …` 和 `build:ios --release --package …`，并让宿主应用针对每个构建配置指向对应的包。

### 生成用于调试的原生项目

若要查看或调试生成的原生代码，请运行 prebuild：

```sh
npx expo prebuild
```

这会创建包含 brownfield 包装器的 `android/` 和 `ios/` 目录：

**Android（Kotlin）：** `ReactNativeHostManager`、`BrownfieldActivity`、`ReactNativeFragment`、`ReactNativeViewFactory`、`BrownfieldMessaging`。

**iOS（Swift）：** `ReactNativeHostManager`、`ReactNativeViewController`、`ReactNativeView`（SwiftUI）、`BrownfieldMessaging`、`ReactNativeDelegate`。

---

## 3) 在原生应用中消费

### Android

#### 添加 Maven 依赖

在 `app/build.gradle.kts` 中：

```kotlin
dependencies {
  implementation("com.example:mybrownfield:1.0.0")
}
```

如果从本地 Maven 仓库消费，请在 `settings.gradle.kts` 中注册 `mavenLocal()`：

```kotlin
dependencyResolutionManagement {
  repositories {
    google()
    mavenCentral()
    mavenLocal()
  }
}
```

> **注意：** `mavenLocal()` 必须添加到 `dependencyResolutionManagement` 下，而不是已弃用的顶层 `allprojects { repositories { ... } }` 块中。

如果产物发布到了远程 Maven，请改为在同一个 `dependencyResolutionManagement` 块中声明该仓库 —— 凭证遵循 Gradle 的标准形式 `maven { url = uri(...); credentials { username = ...; password = ... } }`。

#### 显示 React Native 屏幕

继承 `BrownfieldActivity` 并调用 `showReactNativeFragment()`：

```kotlin
import android.os.Bundle
import com.example.mybrownfield.BrownfieldActivity
import com.example.mybrownfield.showReactNativeFragment

class ExpoActivity : BrownfieldActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    showReactNativeFragment()
  }
}
```

`BrownfieldActivity` 继承自 `AppCompatActivity` 并转发配置变更。`showReactNativeFragment()` 会注册 React Native 根 Fragment，并自动处理原生返回键。

在 `AndroidManifest.xml` 中注册该 Activity：

```xml
<activity
  android:name=".ExpoActivity"
  android:theme="@style/Theme.AppCompat.Light.NoActionBar"
  android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|screenSize|smallestScreenSize|uiMode"
/>
```

从原生代码中启动它：

```kotlin
startActivity(Intent(this, ExpoActivity::class.java))
```

### iOS

#### 将产物添加到 Xcode 项目

如果你构建的是 **Swift Package**（`build:ios --package …`）：

- 在 Xcode 中选择 **File → Add Package Dependencies… → Add Local…**，然后选择生成的包目录（例如 `artifacts/MyAppPackage/`）。
- 将包的产品添加到你的应用目标。Xcode 会通过聚合库产品链接每个打包的 XCFramework —— 无需手动 "Embed & Sign" 操作。
- 如果你同时生成了 debug 和 release 包（因为启用了 `usePrecompiledModules`），请让宿主应用针对每个构建配置指向对应的包。

如果你构建的是**独立的 XCFramework**（默认输出）：

- 将 `./artifacts` 下生成的**每个** `.xcframework` 拖入 Xcode 项目导航器。
- 在导入对话框中，勾选 **Copy items if needed**，并将它们添加到你的应用目标。
- 在应用目标的 **General** 标签页 → **Frameworks, Libraries, and Embedded Content** 中，将**每个** framework 设置为 **Embed & Sign**。遗漏任何一个（通常是 `hermesvm.xcframework`）是运行时出现 "Library not loaded" 崩溃的主要原因 —— 参见 [./troubleshooting.md](./troubleshooting.md#ios-xcframework-signing-isolated-approach)。

#### 在应用启动时初始化 React Native

在创建任何 React Native 视图之前，从 `AppDelegate` 中调用 `ReactNativeHostManager.shared.initialize()`。该初始化对异步调用友好，但必须在第一个 `ReactNativeViewController` / `ReactNativeView` 实例化之前完成。

```swift
import UIKit
import MyAppBrownfield // 替换为你的目标名

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
  func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    ReactNativeHostManager.shared.initialize()
    return true
  }
}
```

#### 显示 React Native 视图（UIKit）

```swift
import UIKit
import MyAppBrownfield

class ViewController: UIViewController {
  @IBAction func openReactNative(_ sender: Any) {
    let rnViewController = ReactNativeViewController(moduleName: "main")
    navigationController?.pushViewController(rnViewController, animated: true)
  }
}
```

如有需要，可传入 props 和 launch options：

```swift
let rnViewController = ReactNativeViewController(
  moduleName: "main",
  initialProps: ["userId": "123"],
  launchOptions: [:]
)
```

> **注意：** `moduleName` 必须与 Expo 项目 JS 入口中通过 `AppRegistry.registerComponent(...)` 注册的名字一致。默认的 Expo 模板注册的是 `"main"`。

#### 显示 React Native 视图（SwiftUI）

```swift
import SwiftUI
import MyAppBrownfield

struct ContentView: View {
  @State private var showReactNative = false

  var body: some View {
    Button("Open React Native") {
      showReactNative = true
    }
    .fullScreenCover(isPresented: $showReactNative) {
      ReactNativeView(moduleName: "main")
    }
  }
}
```

---

## 开发与生产

### 开发（debug 构建）

在 Expo 项目中启动 Metro：

```sh
npx expo start
```

在 debug 模式下构建并运行原生应用。React Native 屏幕通过 HTTP 从 Metro 开发服务器加载 JS，并支持完整的热重载。设备或模拟器必须能够访问开发机 —— 如果 Metro 连接失败，请参阅 [./troubleshooting.md](./troubleshooting.md)。

### 生产（release 构建）

JS bundle 嵌入在 AAR/XCFramework 内部。不使用 Metro。在 Release 配置下构建原生应用，并确认 React Native 屏幕能正常加载。

---

## 相关参考

- [./brownfield-integrated.md](./brownfield-integrated.md) — 替代方案：直接将 RN 加入原生构建。
- [./comparison.md](./comparison.md) — 在 isolated 与 integrated 之间进行选择。
- [./troubleshooting.md](./troubleshooting.md) — 常见的 Metro、构建与集成问题。