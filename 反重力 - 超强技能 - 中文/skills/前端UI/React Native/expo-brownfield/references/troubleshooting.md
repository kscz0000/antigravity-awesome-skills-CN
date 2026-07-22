# Brownfield 故障排查

适用于 isolated 和 integrated 两种方式的共性问题。如需了解特定方式的配置步骤，请参阅 [./brownfield-isolated.md](./brownfield-isolated.md) 或 [./brownfield-integrated.md](./brownfield-integrated.md)。

## 构建失败

**症状：** 在修改配置、升级依赖或升级 Expo SDK 后，Gradle 或 Xcode 构建失败。

- **集成方式（Integrated）** — 重新从头生成原生项目：
  ```sh
  npx expo prebuild --clean
  ```
  然后 `cd ios && pod install` 并重新打开 `.xcworkspace`。
- **隔离方式（Isolated）** — 清空本地 Maven 缓存并重新构建产物：
  ```sh
  rm -rf ~/.m2/repository/<group>/<libraryName>
  npx expo-brownfield build:android
  npx expo-brownfield build:ios
  ```
- 对于顽固的 iOS 问题，还需要删除 `ios/build/`、`ios/Pods/` 和 `ios/Podfile.lock`，然后重新运行 `pod install`。
- 对于顽固的 Android 问题，执行 `./gradlew clean` 并删除项目下的 `.gradle/` 和 `build/` 目录。

## 自动链接的 Expo 模块缺失

**症状：** 编译成功，但某个模块在运行时抛出 "Native module cannot be null" / "Cannot find native module 'X'"。

- 使用 `npx expo install <package>` 安装，而不是直接用 `yarn add` —— `expo install` 会选择与当前 SDK 兼容的版本。
- 安装新模块后，需要重新构建原生应用。Autolinking 在原生构建时运行，而不是在 JS 打包阶段运行。
- 对于**隔离方式**，在添加模块后必须重新运行 `npx expo-brownfield build:android|ios`，并重新发布/重新嵌入新的产物。

## Metro 连接

**症状：** 在 debug 启动时出现 "Could not connect to development server" / 红色屏幕。

- 确保设备或模拟器能够访问开发机。Android 模拟器可以通过 `10.0.2.2` 访问宿主机；真机需要一个可达的局域网 IP。
- 对于通过 USB 连接的 Android 真机：`adb reverse tcp:8081 tcp:8081`。
- 确认 Metro 确实在运行：在 Expo 项目中执行 `npx expo start`（或在 monorepo 根目录执行 `yarn start`）。
- 确认 debug 版的 `AndroidManifest.xml` 启用了明文流量 —— Android 9+ 默认会拦截 HTTP。debug 变体应在 `<application>` 上包含 `android:usesCleartextTraffic="true"`，或者提供允许开发服务器的 `network_security_config`。
- iOS 模拟器：Metro 应可通过 `localhost:8081` 访问。如果不可访问，请检查 `Info.plist` 中针对 `localhost` 的 ATS 例外是否仍然存在（Expo 模板默认会带上）。

## iOS XCFramework 签名（隔离方式）

**症状：** 应用启动后立即崩溃，出现 "Library not loaded"，或在归档时出现 codesign 错误。

- `build:ios` 生成的**每个** xcframework 都必须在应用目标的 **Frameworks, Libraries, and Embedded Content** 区域中设置为 **Embed & Sign**。在 SDK 56+ 上有 5 个 framework：`{TargetName}.xcframework`、`React.xcframework`、`ReactNativeDependencies.xcframework`、`ExpoModulesJSI.xcframework` 和 `hermesvm.xcframework`。在 SDK 55 上则是 2 个：`{TargetName}.xcframework` 和 `hermesvm.xcframework`。遗漏任何一个都是运行时崩溃的常见原因。
- 这些 framework 必须添加到**应用目标**，而不是 framework 或 extension 目标。
- 优先使用 Swift Package 输出（`build:ios --package`）—— 它通过一个聚合产品链接每个打包的 xcframework，因此你不会遗漏任何一个。

## iOS 架构 / 模拟器不匹配

**症状：** 出现 "Building for iOS Simulator, but the linked library was built for iOS"，或 "Undefined symbols for architecture arm64"。

- XCFramework 同时包含设备和模拟器切片。如果某个切片缺失，请在缺失的平台上重新构建。`expo-brownfield build:ios` 默认会同时构建两者。
- 在 Apple Silicon 模拟器上，**不要**为模拟器配置设置 `EXCLUDED_ARCHS = arm64` —— Apple Silicon 模拟器需要 `arm64`。过去那种只排除 arm64（仅 Rosetta）的做法已经不再正确。

## Android `mavenLocal()` 找不到（隔离方式）

**症状：** 即使 `expo-brownfield build:android` 成功执行，Gradle 仍然提示 "Could not find com.example:mybrownfield:1.0.0"。

- `mavenLocal()` 必须声明在 `settings.gradle.kts` 的 `dependencyResolutionManagement { repositories { ... } }` 下，而不是已弃用的顶层 `allprojects { repositories { ... } }` 块中。当 `dependencyResolutionManagement` 存在时，弃用形式会被静默忽略。
- 确认产物确实已经发布到 `~/.m2`：
  ```sh
  find ~/.m2/repository -name "mybrownfield*"
  ```
- 核实消费方依赖声明中的 `group` 和 `libraryName` 与插件配置产出的内容一致。

## 模块名不匹配

**症状：** 原生视图已加载，但屏幕是空白的，且 JS 日志中显示 "Application 'X' has not been registered"。

- 传给 `ReactNativeViewController(moduleName: "main")`（iOS）或由 `getMainComponentName()`（Android）返回的 `moduleName` 必须等于 JS 入口中传给 `AppRegistry.registerComponent("main", () => App)` 的名字。
- 默认的 Expo 模板注册的是 `"main"`。如果你修改过注册名，请同步更新每个原生调用点。

## Monorepo：autolinking 找不到 Expo 项目

**症状：** 即使模块已经安装，Gradle 或 CocoaPods 仍然无法解析 Expo 模块。

- **Android（集成）：** 在 `app/build.gradle` 的 `react { ... }` 块内设置 `root = file("../../my-project")`（或正确的相对路径），并在 `settings.gradle` 中 `expoAutolinking.useExpoModules()` 之前显式设置项目根。
- **iOS（集成）：** 将 `use_react_native!` 中的 `:app_path` 设置为 Expo 项目根的绝对路径。也可以在 `pod install` 时传入 `EXPO_PROJECT_ROOT=/abs/path`。
- 确认 `node_modules/` 已经安装在工作区根目录（从 monorepo 根目录运行 `yarn install`，而不是从 Expo 项目的子目录运行）。

## 升级 Expo SDK 之后

如果在 SDK 升级后 brownfield 配置突然无法构建：

- 在 Expo 项目中重新运行 `npx expo install --fix`，对齐原生模块的版本。
- 重新构建产物（隔离方式）或运行 `npx expo prebuild --clean`（集成方式）。
- 将目标 SDK 的新版 `templates/expo-template-bare-minimum` 与你定制过的原生文件进行对比 —— Expo 偶尔会在不同 SDK 之间更改 Gradle 插件名、Podfile 辅助函数或 AppDelegate 入口。