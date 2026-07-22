# 模块配置参考

## expo-module.config.json

使用 `expo-module.config.json` 进行自动链接和模块注册。

文件位置取决于模块类型：

- **standalone 模块**：放在包根目录，紧邻 `package.json`
- **local 模块**：放在 app 的 local 模块目录内的模块根目录（`expo.autolinking.nativeModulesDir`，默认为 `modules/`）

示例：

```json
{
  "platforms": ["android", "apple", "web"],
  "apple": {
    "modules": ["MyModule"],
    "appDelegateSubscribers": ["MyAppDelegateSubscriber"]
  },
  "android": {
    "modules": ["expo.modules.mymodule.MyModule"]
  }
}
```

### 字段

| 字段 | 说明 |
|-------|-------------|
| `platforms` | 支持的平台数组。有效值包括 `android`、`apple`、`web` 和 `devtools`。也可以使用细分的 Apple 平台如 `ios`、`macos` 和 `tvos`，但当一个 Swift 模块支持多个 Apple 目标时，推荐使用 `apple`。 |
| `apple.modules` | Swift 模块类名 |
| `apple.appDelegateSubscribers` | Swift AppDelegate 订阅者类名 |
| `android.modules` | 完全限定的 Kotlin 模块类名（包名 + 类名） |

## 自动链接

Expo 自动链接会自动发现并链接具有 `expo-module.config.json` 的模块。无需手动配置原生项目 —— 通过 npm 安装后运行 `pod install` 即可。

- standalone 模块通过依赖和搜索路径解析。
- local 模块从 `modules` 目录或已定义的 `nativeModulesDir` 中解析。

### 解析顺序

1. `react-native.config.js` 中的显式依赖
2. 自定义 `searchPaths` 目录
3. Local `nativeModulesDir`（默认为 `./modules/`）
4. 递归解析 npm 依赖