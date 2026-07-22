---
name: expo-ui
description: "使用 @expo/ui 包构建原生 UI：在 Expo 或 React Native 应用中，从 React 渲染 iOS 上真实的 SwiftUI 以及 Android 上的 Jetpack Compose。涵盖通用跨平台组件（Host、Column、Row、Button、Text、List 等，从 @expo/ui 导入）、即插即用的替代组件……触发词：expo-ui、@expo/ui、SwiftUI、Jetpack Compose、React Native 原生 UI、跨平台原生组件"
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-ui
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# Expo UI（`@expo/ui`）
## 适用场景

当你需要使用 @expo/ui 包构建原生 UI 时使用本技能：在 Expo 或 React Native 应用中，从 React 渲染 iOS 上真实的 SwiftUI 以及 Android 上的 Jetpack Compose。涵盖通用跨平台组件（Host、Column、Row、Button、Text、List 等，从 @expo/ui 导入）、即插即用的替代组件……


`@expo/ui` 从 React 渲染真实的原生 UI：iOS 上是 SwiftUI，Android 上是 Jetpack Compose。建议从通用组件（一份组件树同时适配 iOS、Android 和 Web）入手，只有当通用层不够用时，才下沉到平台专属的 SwiftUI/Jetpack Compose。它还提供即插即用的替代组件，便于从 RN 社区 UI 库迁移。

> 这些说明跟随最新的 Expo SDK 版本。**通用**层要求 **SDK 56+**。即插即用替代组件以及平台专属层在 SDK 55 上也存在。如需了解特定 SDK 上的组件细节，请参阅对应版本的 Expo UI 文档。

## 安装

```bash
npx expo install @expo/ui
```

在 SDK 56 上，`@expo/ui` 可在 Expo Go 中运行，因此 `npx expo start` 即可直接运行——无需自定义构建。在更早的 SDK 上，需要先构建开发客户端（`npx expo run:ios` / `npx expo run:android`）。

每个 `@expo/ui` 组件树——无论是通用层还是平台专属层——都必须用 `Host` 包裹。

## 选择方案（请先阅读本节）

按下面的顺序逐层评估，在第一个能满足需求处停止：

1. **通用组件 — 从这里开始。** 从 `@expo/ui` 根目录导入。一份组件树无需修改即可在 iOS、Android 和 Web 上运行（Android 上是 Compose，iOS 上是 SwiftUI，Web 上是 `react-native-web`/`react-dom`）。无需平台文件拆分。→ `./references/universal.md`

2. **平台专属（SwiftUI / Jetpack Compose）。** 从 `@expo/ui/swift-ui` 或 `@expo/ui/jetpack-compose` 导入。**仅**在通用层缺少你需要的组件或修饰符，或需要平台专属行为与优化时使用。**缺点：**你需要写两份组件树，并拆分到 `.ios.tsx` / `.android.tsx` 文件中（或在 `Platform.OS` 上做分支）——维护成本更高。

   > **`@expo/ui/swift-ui` 仅适用于 iOS。`@expo/ui/jetpack-compose` 仅适用于 Android。** 在运行于另一平台的文件中导入这两个包，会在运行时崩溃并抛出 "Unable to get view config" 错误。请将平台专属组件树隔离到放在 `components/` 下的 `.ios.tsx` / `.android.tsx` 文件中（不要放在 `app/` 内——Expo Router 不支持路由文件的平台扩展名后缀），或在常规路由文件中用 `Platform.OS` 做守卫。`Host` 必须始终从 `@expo/ui`（通用包根目录）导入，而不是从平台专属子包导入。→ `./references/swift-ui.md` 和 `./references/jetpack-compose.md`

**已经在使用某个 RN 社区 UI 库？** `@expo/ui` 还提供了**即插即用的替代组件**——针对主流库（`@gorhom/bottom-sheet`、`@react-native-community/datetimepicker` 等）的 API 兼容替换，从 `@expo/ui/community/<name>` 导入。这是迁移现有依赖的旁路路径，不是上面"通用 vs 平台"决策中的一步。→ `./references/drop-in-replacements.md`

## 参考资料

按需查阅以下资源：

```
references/
  universal.md             通用 @expo/ui 组件及其适用场景（SDK 56+）
  drop-in-replacements.md  RN 社区 UI 库的 API 兼容替代组件
  swift-ui.md              iOS 平台专属 UI：@expo/ui/swift-ui 组件、修饰符、RNHostView、useNativeState
  jetpack-compose.md       Android 平台专属 UI：@expo/ui/jetpack-compose 组件、修饰符、LazyColumn 注意事项、图标、useNativeState
```

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时才使用本技能。
- 在做出改动前，请对照当前官方文档验证命令、API 行为、定价、配额、凭证以及部署影响。
- 不要将生成的示例视为针对特定环境的测试、安全审查或用户对破坏性/高成本操作的审批的替代品。