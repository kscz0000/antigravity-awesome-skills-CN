# Config Plugin 参考

Config plugin 用于自定义通过 `npx expo prebuild` 生成的原生 Android 和 iOS 项目。它们是同步函数，接收一个 `ExpoConfig` 并返回修改后的版本。

## 插件结构

```
my-module/
  plugin/
    tsconfig.json
    src/
      index.ts
  app.plugin.js         # 入口：module.exports = require('./plugin/build');
```

## 编写插件

插件函数遵循 `with` 前缀的命名约定。

```typescript
import {
  ConfigPlugin,
  withInfoPlist,
  withAndroidManifest,
  AndroidConfig,
} from "expo/config-plugins";

const withMyConfig: ConfigPlugin<{ apiKey: string }> = (config, { apiKey }) => {
  // iOS: 修改 Info.plist
  config = withInfoPlist(config, (config) => {
    config.modResults["MY_API_KEY"] = apiKey;
    return config;
  });

  // Android: 修改 AndroidManifest.xml
  config = withAndroidManifest(config, (config) => {
    const mainApp =
      AndroidConfig.Manifest.getMainApplicationOrThrow(config.modResults);
    AndroidConfig.Manifest.addMetaDataItemToMainApplication(
      mainApp,
      "MY_API_KEY",
      apiKey
    );
    return config;
  });

  return config;
};

export default withMyConfig;
```

## 在 app.json 中使用

```json
{
  "expo": {
    "plugins": [["my-module", { "apiKey": "secret_key" }]]
  }
}
```

## 在原生代码中读取配置值

**Swift:**

```swift
Function("getApiKey") {
  return Bundle.main.object(forInfoDictionaryKey: "MY_API_KEY") as? String
}
```

**Kotlin:**

```kotlin
Function("getApiKey") {
  val appInfo = appContext?.reactContext?.packageManager?.getApplicationInfo(
    appContext?.reactContext?.packageName.toString(),
    PackageManager.GET_META_DATA
  )
  return@Function appInfo?.metaData?.getString("MY_API_KEY")
}
```

## 关键规则

- 插件必须是同步的；返回值必须可序列化（`mods` 除外）
- `Mods` 是在 prebuild "syncing" 阶段调用的异步函数
- 使用 `npm run build plugin` 编译 TypeScript 插件
- 使用 `npx expo prebuild --clean` 进行测试