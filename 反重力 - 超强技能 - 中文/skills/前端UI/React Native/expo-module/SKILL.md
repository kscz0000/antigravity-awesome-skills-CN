---
name: expo-module
description: 使用 Expo Modules API（Swift、Kotlin、TypeScript）创建和编写 Expo 原生模块与视图的指南。涵盖模块定义 DSL、原生视图、共享对象、配置插件、生命周期钩子、自动链接和类型系统。在构建或修改原生模块时使用。触发词：expo-module、Expo Modules API、原生模块、原生视图、Swift 模块、Kotlin 模块、TypeScript 绑定、config plugin、自动链接、SharedObject。
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-module
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# 编写 Expo 模块

使用 Expo Modules API 构建原生模块和视图的完整参考。涵盖 Swift（iOS）、Kotlin（Android）和 TypeScript。

## 适用场景

- 创建一个新的 Expo 原生模块或原生视图
- 为 Expo 应用添加原生功能（相机、传感器、系统 API）
- 为 React Native 封装平台 SDK
- 构建用于修改原生项目文件的 config plugin
- 为现有的 Expo 模块添加 Android、Apple 或 Web 支持
- 编辑 `expo-module.config.json`、config plugin 或生命周期钩子

## 参考文档

根据需要查阅以下资源：

```
references/
  create-expo-module.md      脚手架与 add-platform-support 工作流、默认值和注意事项
  native-module.md           模块定义 DSL：Name、Function、AsyncFunction、Property、Constant、Events、类型系统、SharedObject
  native-view.md             原生视图组件：View、Prop、EventDispatcher、视图生命周期、基于 ref 的函数
  lifecycle.md               生命周期钩子：模块、iOS app/AppDelegate、Android activity/application 监听器
  config-plugin.md           Config plugin：修改 Info.plist、AndroidManifest.xml，在原生代码中读取值
  module-config.md           expo-module.config.json 字段、文件位置和自动链接行为
```

## 快速开始

推荐使用 `create-expo-module` 而不是手动创建原生模块文件和目录。在实践中，最佳路径通常是先创建脚手架，然后再在其上进行构建。脚手架会设置好预期的目录结构、`expo-module.config.json`、podspec 或 Gradle 文件、TypeScript 绑定以及独立的示例 app 流程。

如果现有 Expo 模块只需要新增另一个平台，请使用 `create-expo-module add-platform-support`，而不是手动复制原生目录。

在脚手架或扩展模块之前，请参阅 [references/create-expo-module.md](references/create-expo-module.md)。它涵盖了：

- local 模块与 standalone 模块
- `--platform`、`--features`、`--barrel`、`--package-manager` 以及非交互模式
- `expo.autolinking.nativeModulesDir`
- `add-platform-support` 的行为和注意事项

## 推荐工作流

1. 首先选择脚手架类型：
   - **Local 模块**：仅用于单个 app
   - **Standalone 模块**：用于复用、monorepo 或发布
2. 确定你将需要的原生 `expo-module` 功能。
   - 根据用户的需求确定哪些功能脚手架会更有用。
   - 可用功能：`Constant`、`Function`、`AsyncFunction`、`Event`、`View`、`ViewEvent`、`SharedObject`
3. 谨慎搭建脚手架：
   - 显式传入 slug 或路径
   - 有意识地选择 `--platform`，不要依赖默认值
   - 使用 `--features` 选择代码样例，然后在下一步中将其修改为匹配实际实现
4. 将生成的示例代码替换为真实实现。
5. 如果之后要添加新平台，优先使用 `add-platform-support` 而非手动复制文件。

## 脚手架实用规则

- 功能示例是 **可选的**。如果未选择任何功能，新搭建的模块可能是最小化的。
- `ViewEvent` 隐含 `View`。
- Local 模块默认 **不会** 生成 `index.ts` barrel。仅当需要时才使用 `--barrel`。
- 在非交互的 local 脚手架中，必须显式传入位置参数 slug 或路径。`--name` 更改原生类名，而非目录名。
- Local 模块位于 `expo.autolinking.nativeModulesDir`（如已配置），否则位于 `modules/`。
- Standalone 模块拥有自己的 package 元数据、脚本，通常还包含一个示例 app。Local 模块则使用宿主 app 的工具链。

## 核心文件形态

Swift 与 Kotlin 的 DSL 共享相同结构。Swift 通常是最清晰的首选示例；具体功能细节请查阅参考文档。

## 模块结构参考

Swift 与 Kotlin 的 DSL 共享相同结构。这里展示两个平台以供参考 —— 在其他参考文件中，除非 Kotlin 模式有显著差异，否则默认以 Swift 作为主语言。

**Swift (iOS):**

```swift
import ExpoModulesCore

public class MyModule: Module {
  public func definition() -> ModuleDefinition {
    Name("MyModule")

    Function("hello") { (name: String) -> String in
      return "Hello \(name)!"
    }
  }
}
```

**Kotlin (Android):**

```kotlin
package expo.modules.mymodule

import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition

class MyModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("MyModule")

    Function("hello") { name: String ->
      "Hello $name!"
    }
  }
}
```

**TypeScript:**

```typescript
import { requireNativeModule } from "expo";

const MyModule = requireNativeModule("MyModule");

export function hello(name: string): string {
  return MyModule.hello(name);
}
```

### expo-module.config.json

```json
{
  "platforms": ["android", "apple"],
  "apple": {
    "modules": ["MyModule"]
  },
  "android": {
    "modules": ["expo.modules.mymodule.MyModule"]
  }
}
```

注意：iOS 仅使用类名；Android 使用完全限定类名（包名 + 类名）。所有字段请参阅 `references/module-config.md`。

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时才使用此技能。
- 在进行更改前，请根据最新的官方文档验证命令、API 行为、价格、配额、凭据和部署效果。
- 不要将生成的示例用作针对特定环境的测试、安全审查或对破坏性/高成本操作的用户授权的替代品。