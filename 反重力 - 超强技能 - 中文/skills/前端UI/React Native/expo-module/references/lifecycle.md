# 生命周期钩子参考

## 模块生命周期（在模块定义中）

```swift
OnCreate {
  // 模块已初始化 - 优先于类构造器使用
}

OnDestroy {
  // 模块已释放 - 清理资源
}

OnAppContextDestroys {
  // App context 正在被释放
}
```

## iOS App 生命周期（在模块定义中）

```swift
OnAppEntersForeground { /* UIApplication.willEnterForegroundNotification */ }
OnAppEntersBackground { /* UIApplication.didEnterBackgroundNotification */ }
OnAppBecomesActive { /* UIApplication.didBecomeActiveNotification */ }
```

## Android Activity 生命周期（在模块定义中）

```kotlin
OnActivityEntersForeground { /* Activity 已恢复 */ }
OnActivityEntersBackground { /* Activity 已暂停 */ }
OnActivityDestroys { /* Activity 已销毁 */ }
OnNewIntent { intent -> /* 接收到 Deep Link */ }
OnActivityResult { activity, result -> /* startActivityForResult 回调 */ }
OnUserLeavesActivity { /* 用户发起的切到后台 */ }
RegisterActivityContracts { /* 现代化的 activity result contracts */ }
```

---

## iOS AppDelegate 订阅者

用于在不直接编辑 AppDelegate 的情况下接入 AppDelegate 事件。要求 app 的 AppDelegate 继承自 `ExpoAppDelegate`。

```swift
import ExpoModulesCore

public class MyAppDelegateSubscriber: ExpoAppDelegateSubscriber {
  public func applicationDidBecomeActive(_ application: UIApplication) {}
  public func applicationWillResignActive(_ application: UIApplication) {}
  public func applicationDidEnterBackground(_ application: UIApplication) {}
  public func applicationWillEnterForeground(_ application: UIApplication) {}
  public func applicationWillTerminate(_ application: UIApplication) {}

  public func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    return false  // 若已处理则返回 true
  }
}
```

在 `expo-module.config.json` 中注册：

```json
{
  "apple": {
    "appDelegateSubscribers": ["MyAppDelegateSubscriber"]
  }
}
```

结果聚合：
- `didFinishLaunchingWithOptions`：只要有 **任一** 订阅者返回 `true`，则整体返回 `true`
- `didReceiveRemoteNotification`：优先级：`failed` > `newData` > `noData`

---

## Android 生命周期监听器

用于在模块定义之外接入 Activity/Application 生命周期。适用于处理 Deep Link、Intent 以及 app 级别的初始化。

### ReactActivityLifecycleListener

支持的回调：`onCreate`、`onResume`、`onPause`、`onDestroy`、`onNewIntent`、`onBackPressed`。

> 注意：**不支持** `onStart` 和 `onStop` —— 该实现挂钩到 `ReactActivityDelegate`，而后者缺少这两个方法。

```kotlin
class MyPackage : Package {
  override fun createReactActivityLifecycleListeners(
    activityContext: Context
  ): List<ReactActivityLifecycleListener> {
    return listOf(MyActivityListener())
  }
}

class MyActivityListener : ReactActivityLifecycleListener {
  override fun onCreate(activity: Activity, savedInstanceState: Bundle?) { }
  override fun onResume(activity: Activity) { }
  override fun onPause(activity: Activity) { }
  override fun onDestroy(activity: Activity) { }
  override fun onNewIntent(intent: Intent?): Boolean { return false }
  override fun onBackPressed(): Boolean { return false }
}
```

### ApplicationLifecycleListener

支持的回调：`onCreate`、`onConfigurationChanged`。

```kotlin
class MyPackage : Package {
  override fun createApplicationLifecycleListeners(
    context: Context
  ): List<ApplicationLifecycleListener> {
    return listOf(MyAppListener())
  }
}

class MyAppListener : ApplicationLifecycleListener {
  override fun onCreate(application: Application) {
    // app 级别的初始化
  }
}
```