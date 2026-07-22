# Brownfield：集成方式

将 React Native 和 Expo 直接添加到现有原生项目的构建系统中——Android 上使用 Gradle，iOS 上使用 CocoaPods——就像添加任何其他库一样。原生项目将获得 React Native 能力，同时保持单一、统一的构建流程。

## 何时使用

- 单一团队同时拥有原生代码和 React Native 代码。
- 团队能接受将 React Native 和 Expo 加入到原生构建中（Gradle 插件、CocoaPods pods）。
- 你希望在现有构建中原生支持热重载、JS 源码映射以及单一 Metro 实例。
- 你倾向于使用单一仓库和单一构建流水线，而不是交付预构建产物。

如果原生团队不应该依赖 Node、Yarn 或 React Native 工具链，请改用 [./brownfield-isolated.md](./brownfield-isolated.md)。

## 前置条件

- **Expo SDK 54 或更高版本** — 下面使用的 `ExpoReactHostFactory`、`ExpoReactNativeFactory` 和 `ApplicationLifecycleDispatcher` 入口需要 SDK 54+。更早的 SDK 不支持此配置。
- **Node.js（LTS）** — 运行 JavaScript 和 Expo CLI。
- **Yarn** — 管理 JavaScript 依赖。
- **CocoaPods**（iOS）— `sudo gem install cocoapods`。

---

## 1) 创建一个 Expo 项目

在现有原生项目内部（或旁边）创建 Expo 项目。**请锁定到 SDK 55 或更高版本——更早的 SDK 不支持 brownfield 集成：**

```sh
npx create-expo-app@latest my-project --template default@sdk-55
```

新项目自带一个 TypeScript 示例应用。JS 入口在名为 `"main"` 的根组件下注册——这个名字必须与后面原生侧引用的 `moduleName` 匹配。

## 2) 将原生项目放入 Expo 项目下

标准的 React Native 项目将原生代码放在 `android/` 和 `ios/` 下。把现有的原生项目移入其中：

```sh
mkdir my-project/android
mv /path/to/your/android-project my-project/android/
# 对 ios/ 重复上述步骤
```

### Monorepo（单仓库多包）替代方案

如果原生项目无法移动，可以使用 Expo 项目作为工作区搭建一个 monorepo。在根目录创建 `package.json`：

```json
{
  "version": "1.0.0",
  "private": true,
  "workspaces": ["my-project"]
}
```

在根目录运行 `yarn install`。这会在工作区根目录安装 `node_modules`，以便 Gradle 和 CocoaPods 脚本能够解析 React Native 和 Expo 依赖。

> **Monorepo 提示：** 在 monorepo 中，Expo 项目相对原生项目并不在 `../../`。你必须在 Gradle 中显式设置 `projectRoot`，并把项目根目录传给 CocoaPods，以便 autolinking 能够找到 Expo 项目。

---

## 3) 配置 Android

### `settings.gradle`

注册 React Native Gradle 插件和 Expo autolinking。参考：[bare-minimum 模板的 `settings.gradle`](https://github.com/expo/expo/blob/main/templates/expo-template-bare-minimum/android/settings.gradle)。

```groovy
pluginManagement {
  def reactNativeGradlePlugin = new File(
    providers.exec {
      workingDir(rootDir)
      commandLine("node", "--print", "require.resolve('@react-native/gradle-plugin/package.json', { paths: [require.resolve('react-native/package.json')] })")
    }.standardOutput.asText.get().trim()
  ).getParentFile().absolutePath
  includeBuild(reactNativeGradlePlugin)

  def expoPluginsPath = new File(
    providers.exec {
      workingDir(rootDir)
      commandLine("node", "--print", "require.resolve('expo-modules-autolinking/package.json', { paths: [require.resolve('expo/package.json')] })")
    }.standardOutput.asText.get().trim(),
    "../android/expo-gradle-plugin"
  ).absolutePath
  includeBuild(expoPluginsPath)
}

plugins {
  id("com.facebook.react.settings")
  id("expo-autolinking-settings")
}

extensions.configure(com.facebook.react.ReactSettingsExtension) { ex ->
  ex.autolinkLibrariesFromCommand(expoAutolinking.rnConfigCommand)
}
expoAutolinking.useExpoModules()
expoAutolinking.useExpoVersionCatalog()
includeBuild(expoAutolinking.reactNativeGradlePlugin)
```

> **Monorepo：** 在 `expoAutolinking.useExpoModules()` 之前添加显式的项目根，以便 autolinking 能够找到你的 Expo 项目的 `node_modules`。

### 顶层 `build.gradle`

添加 React Native Gradle 插件的 classpath 和 Expo 根项目插件：

```groovy
buildscript {
  repositories {
    google()
    mavenCentral()
  }
  dependencies {
    classpath('com.android.tools.build:gradle')
    classpath('com.facebook.react:react-native-gradle-plugin')
    classpath('org.jetbrains.kotlin:kotlin-gradle-plugin')
  }
}

allprojects {
  repositories {
    google()
    mavenCentral()
    maven { url 'https://www.jitpack.io' }
  }
}

apply plugin: "expo-root-project"
apply plugin: "com.facebook.react.rootproject"
```

### `app/build.gradle`

应用 React Native 插件并配置 `react { ... }` 块。完整模板见 [bare-minimum 的 `app/build.gradle`](https://github.com/expo/expo/blob/main/templates/expo-template-bare-minimum/android/app/build.gradle)；你现有模块中至少需要修改的部分：

```groovy
apply plugin: "com.android.application"
apply plugin: "org.jetbrains.kotlin.android"
apply plugin: "com.facebook.react"

def projectRoot = rootDir.getAbsoluteFile().getParentFile().getAbsolutePath()

react {
  entryFile = file(["node", "-e", "require('expo/scripts/resolveAppEntry')", projectRoot, "android", "absolute"].execute(null, rootDir).text.trim())
  reactNativeDir = new File(["node", "--print", "require.resolve('react-native/package.json')"].execute(null, rootDir).text.trim()).getParentFile().getAbsoluteFile()
  codegenDir = new File(["node", "--print", "require.resolve('@react-native/codegen/package.json', { paths: [require.resolve('react-native/package.json')] })"].execute(null, rootDir).text.trim()).getParentFile().getAbsoluteFile()
  cliFile = new File(["node", "--print", "require.resolve('@expo/cli', { paths: [require.resolve('expo/package.json')] })"].execute(null, rootDir).text.trim())
  bundleCommand = "export:embed"
  autolinkLibrariesWithApp()
}
```

> **Monorepo：** 在 `react { ... }` 块内设置 `root = file("../../")`（或你的 Expo 项目所在的路径）。

### `gradle.properties`

```properties
reactNativeArchitectures=armeabi-v7a,arm64-v8a,x86,x86_64
newArchEnabled=true
hermesEnabled=true
```

`newArchEnabled` 和 `hermesEnabled` 必须在构建的所有子模块中保持一致。

### `AndroidManifest.xml`

在位于 `app/src/main/AndroidManifest.xml` 的主清单中添加 `INTERNET` 权限：

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

在 `app/src/debug/AndroidManifest.xml` 的 debug 变体清单中，启用明文流量，以便应用能够通过 HTTP 与本地 Metro bundler 通信：

```xml
<application
  android:usesCleartextTraffic="true"
  tools:targetApi="28"
  tools:ignore="GoogleAppIndexingWarning">
  ...
</application>
```

### `MainApplication.kt`

在你的 `Application` 类中初始化 React Native 和 Expo 生命周期分发：

```kotlin
package com.example.myapp

import android.app.Application
import android.content.res.Configuration

import com.facebook.react.PackageList
import com.facebook.react.ReactApplication
import com.facebook.react.ReactNativeApplicationEntryPoint.loadReactNative
import com.facebook.react.ReactHost
import com.facebook.react.common.ReleaseLevel
import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint

import expo.modules.ApplicationLifecycleDispatcher
import expo.modules.ExpoReactHostFactory

class MainApplication : Application(), ReactApplication {

  override val reactHost: ReactHost by lazy {
    ExpoReactHostFactory.getDefaultReactHost(
      context = applicationContext,
      packageList = PackageList(this).packages
    )
  }

  override fun onCreate() {
    super.onCreate()
    DefaultNewArchitectureEntryPoint.releaseLevel = try {
      ReleaseLevel.valueOf(BuildConfig.REACT_NATIVE_RELEASE_LEVEL.uppercase())
    } catch (_: IllegalArgumentException) {
      ReleaseLevel.STABLE
    }
    loadReactNative(this)
    ApplicationLifecycleDispatcher.onApplicationCreate(this)
  }

  override fun onConfigurationChanged(newConfig: Configuration) {
    super.onConfigurationChanged(newConfig)
    ApplicationLifecycleDispatcher.onConfigurationChanged(this, newConfig)
  }
}
```

### `ReactActivity`

创建一个承载 React Native 屏幕的 `Activity`。`getMainComponentName()` 返回的 `moduleName` 必须与你的 JS 入口（默认模板中为 `"main"`）通过 `AppRegistry.registerComponent(...)` 注册的名字一致。

```kotlin
package com.example.myapp

import com.facebook.react.ReactActivity
import com.facebook.react.ReactActivityDelegate
import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint.fabricEnabled
import com.facebook.react.defaults.DefaultReactActivityDelegate

import expo.modules.ReactActivityDelegateWrapper

class MyReactActivity : ReactActivity() {

  override fun getMainComponentName(): String = "main"

  override fun createReactActivityDelegate(): ReactActivityDelegate {
    return ReactActivityDelegateWrapper(
      this,
      BuildConfig.IS_NEW_ARCHITECTURE_ENABLED,
      object : DefaultReactActivityDelegate(this, mainComponentName, fabricEnabled) {}
    )
  }
}
```

在 `AndroidManifest.xml` 中使用非 ActionBar 主题注册该 Activity：

```xml
<activity
  android:name=".MyReactActivity"
  android:theme="@style/Theme.AppCompat.Light.NoActionBar"
  android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|screenSize|smallestScreenSize|uiMode"
/>
```

从已有的原生代码中启动它：

```kotlin
startActivity(Intent(this, MyReactActivity::class.java))
```

---

## 4) 配置 iOS

集成式 iOS 的驱动方式与全新 Expo 项目完全相同：通过 CocoaPods + Expo 模块 autolinking。关键区别在于，你是在集成到现有的 Xcode 项目中，而不是从模板开始。

### `ios/Podfile`

基于 [bare-minimum Podfile](https://github.com/expo/expo/blob/main/templates/expo-template-bare-minimum/ios/Podfile) 创建（或更新）`ios/Podfile`。核心配置：

```ruby
require File.join(File.dirname(`node --print "require.resolve('expo/package.json')"`), "scripts/autolinking")
require File.join(File.dirname(`node --print "require.resolve('react-native/package.json')"`), "scripts/react_native_pods")

require 'json'
podfile_properties = JSON.parse(File.read(File.join(__dir__, 'Podfile.properties.json'))) rescue {}

platform :ios, podfile_properties['ios.deploymentTarget'] || '16.4'

prepare_react_native_project!

target 'MyApp' do
  use_expo_modules!

  config_command = [
    'node',
    '--no-warnings',
    '--eval',
    'require(\'expo/bin/autolinking\')',
    'expo-modules-autolinking',
    'react-native-config',
    '--json',
    '--platform',
    'ios'
  ]

  config = use_native_modules!(config_command)

  use_frameworks! :linkage => podfile_properties['ios.useFrameworks'].to_sym if podfile_properties['ios.useFrameworks']

  use_react_native!(
    :path => config[:reactNativePath],
    :hermes_enabled => podfile_properties['expo.jsEngine'] == nil || podfile_properties['expo.jsEngine'] == 'hermes',
    :app_path => "#{Pod::Config.instance.installation_root}/..",
    :privacy_file_aggregation_enabled => podfile_properties['apple.privacyManifestAggregationEnabled'] != 'false',
  )

  post_install do |installer|
    react_native_post_install(installer, config[:reactNativePath], :mac_catalyst_enabled => false)
  end
end
```

将 `'MyApp'` 替换为你现有的 Xcode 目标名。`:app_path` 的值告诉 `use_react_native!` JS 应用所在的位置——如果你在 monorepo 中，请设置为 Expo 项目根目录的绝对路径。

在 Podfile 旁边创建 `ios/Podfile.properties.json`（默认值即可）：

```json
{
  "expo.jsEngine": "hermes",
  "EX_DEV_CLIENT_NETWORK_INSPECTOR": "true"
}
```

安装 pods：

```sh
cd ios && pod install
```

之后请打开生成的 `.xcworkspace`（而不是 `.xcodeproj`）。

### Xcode 项目调整

在应用能够构建并运行 React Native 屏幕之前，需要进行三项 Xcode 侧的调整。任何一项缺失都可能导致 CocoaPods 脚本在沙盒下失败、JS 包无法被打入 IPA（发布版本会在查找 `main.jsbundle` 时崩溃），或者状态栏在运行时与 React Native 冲突。

#### 1. 关闭用户脚本沙盒

在 Xcode 中，选择你的项目 → 应用目标 → **Build Settings**，搜索 `ENABLE_USER_SCRIPT_SANDBOXING`，将其设置为 **No**。CocoaPods 的 Hermes 脚本需要在构建时在 debug 与 release 引擎二进制之间切换，而沙盒会阻止这一点。

#### 2. 添加用于嵌入 JS 包的 Run Script 阶段

在应用目标的 **Build Phases** 标签页中，在 `[CP] Embed Pods Frameworks` 之前添加一个新的 **Run Script** 阶段。该阶段在发布构建中打包 JS，debug 模式下会自动跳过（此时由 Metro 提供 bundle）。

```sh
if [[ -f "$PODS_ROOT/../.xcode.env" ]]; then
  source "$PODS_ROOT/../.xcode.env"
fi
if [[ -f "$PODS_ROOT/../.xcode.env.local" ]]; then
  source "$PODS_ROOT/../.xcode.env.local"
fi

export PROJECT_ROOT="$PROJECT_DIR"/..

if [[ "$CONFIGURATION" = *Debug* ]]; then
  export SKIP_BUNDLING=1
fi
if [[ -z "$ENTRY_FILE" ]]; then
  export ENTRY_FILE="$("$NODE_BINARY" -e "require('expo/scripts/resolveAppEntry')" "$PROJECT_ROOT" ios absolute | tail -n 1)"
fi
if [[ -z "$CLI_PATH" ]]; then
  export CLI_PATH="$("$NODE_BINARY" --print "require.resolve('@expo/cli', { paths: [require.resolve('expo/package.json')] })")"
fi
if [[ -z "$BUNDLE_COMMAND" ]]; then
  export BUNDLE_COMMAND="export:embed"
fi

if [[ -f "$PODS_ROOT/../.xcode.env.updates" ]]; then
  source "$PODS_ROOT/../.xcode.env.updates"
fi
if [[ -f "$PODS_ROOT/../.xcode.env.local" ]]; then
  source "$PODS_ROOT/../.xcode.env.local"
fi

`"$NODE_BINARY" --print "require('path').dirname(require.resolve('react-native/package.json')) + '/scripts/react-native-xcode.sh'"`
```

> **Monorepo：** 将 `PROJECT_ROOT` 重写为指向 Expo 项目（例如 `export PROJECT_ROOT="$PROJECT_DIR"/../../my-project`）。否则打包时会在错误的目录中查找 `node_modules`。

该脚本会在 release 配置下将 `main.jsbundle` 写入应用的资源目录。如果没有它，`ReactNativeDelegate` 中的 `bundleURL()` 回退会解析为 `nil`，从而在 Metro 未运行时导致 React Native 屏幕无法加载。

#### 3. 更新 `Info.plist`

将 `UIViewControllerBasedStatusBarAppearance` 设置为 `NO`，以便 React Native 管理状态栏：

```xml
<key>UIViewControllerBasedStatusBarAppearance</key>
<false/>
```

### `AppDelegate.swift`

通过 Expo 的 `ExpoReactNativeFactory` 将 React Native 接入应用委托。委托的 `bundleURL()` 在 `DEBUG` 下选择 Metro 开发服务器，在 release 下选择嵌入的 bundle。

```swift
internal import Expo
import React
import ReactAppDependencyProvider

@main
class AppDelegate: ExpoAppDelegate {
  var window: UIWindow?

  var reactNativeDelegate: ExpoReactNativeFactoryDelegate?
  var reactNativeFactory: RCTReactNativeFactory?

  public override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
  ) -> Bool {
    let delegate = ReactNativeDelegate()
    let factory = ExpoReactNativeFactory(delegate: delegate)
    delegate.dependencyProvider = RCTAppDependencyProvider()

    reactNativeDelegate = delegate
    reactNativeFactory = factory

    window = UIWindow(frame: UIScreen.main.bounds)
    factory.startReactNative(
      withModuleName: "main",
      in: window,
      launchOptions: launchOptions
    )

    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}

class ReactNativeDelegate: ExpoReactNativeFactoryDelegate {
  override func sourceURL(for bridge: RCTBridge) -> URL? {
    bridge.bundleURL ?? bundleURL()
  }

  override func bundleURL() -> URL? {
#if DEBUG
    return RCTBundleURLProvider.sharedSettings().jsBundleURL(forBundleRoot: ".expo/.virtual-metro-entry")
#else
    return Bundle.main.url(forResource: "main", withExtension: "jsbundle")
#endif
  }
}
```

模块名 `"main"` 必须与 JS 端通过 `AppRegistry.registerComponent("main", () => App)` 注册的名字一致。

### 在现有屏幕中嵌入 RN（而非根窗口）

如果你不希望 React Native 接管整个窗口，可以以同样的方式实例化 factory，并将生成的根视图挂载到现有的 `UIViewController` 内：

```swift
import UIKit
import React
import Expo

class ReactNativeScreenViewController: UIViewController {
  private var reactNativeDelegate: ExpoReactNativeFactoryDelegate?
  private var reactNativeFactory: RCTReactNativeFactory?

  override func viewDidLoad() {
    super.viewDidLoad()

    let delegate = ReactNativeDelegate()
    let factory = ExpoReactNativeFactory(delegate: delegate)
    delegate.dependencyProvider = RCTAppDependencyProvider()
    self.reactNativeDelegate = delegate
    self.reactNativeFactory = factory

    let rootView = factory.rootViewFactory.view(
      withModuleName: "main",
      initialProperties: nil,
      launchOptions: nil
    )
    rootView.frame = view.bounds
    rootView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
    view.addSubview(rootView)
  }
}
```

像使用任何其他视图控制器一样呈现它：

```swift
navigationController?.pushViewController(ReactNativeScreenViewController(), animated: true)
```

> **iOS 的 Monorepo：** `pod install` 在 `ios/` 目录中运行，但 Node 模块解析从 Expo 项目根目录开始。如果 autolinking 无法自动找到 Expo 项目，请在 `pod install` 命令前加上 `EXPO_PROJECT_ROOT=/absolute/path/to/expo-project`。

---

## 5) 测试集成

从 Expo 项目（或在 monorepo 根目录执行 `yarn start`）启动 Metro：

```sh
yarn start
```

按常规方式（Android Studio / Xcode）构建并运行原生应用。导航到由 React Native 驱动的 Activity 或屏幕——它会从 Metro 开发服务器加载 JS，并支持热重载。

### 开发与生产

- **开发（Development）** — Metro 通过 HTTP 提供 JS 包，并支持热重载。Debug 构建通过 iOS 的 `RCTBundleURLProvider` 或 Android 的 `ReactActivity` 中的开发服务器检测使用 Metro URL。
- **生产（Production）** — 不使用 Metro。运行 `expo export:embed`（由 React Native Gradle 插件和 iOS 构建阶段自动调用）将 bundle 嵌入到 APK/IPA 中。

有关 Metro 连接、构建失败、模块缺失或架构不匹配的问题，请参阅 [./troubleshooting.md](./troubleshooting.md)。

---

## 相关参考

- [./brownfield-isolated.md](./brownfield-isolated.md) — 替代方案：将 RN 作为预构建的 AAR/XCFramework 交付。
- [./comparison.md](./comparison.md) — 在 isolated 与 integrated 之间进行选择。
- [./troubleshooting.md](./troubleshooting.md) — 常见的 Metro、构建与集成问题。