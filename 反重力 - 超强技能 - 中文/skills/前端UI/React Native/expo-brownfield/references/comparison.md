# Brownfield：Isolated vs. Integrated

使用此参考文档来选择向现有原生应用添加 React Native + Expo 的两种方式之一。如果你已经清楚团队分工与约束，可以直接跳转到：

- [./brownfield-isolated.md](./brownfield-isolated.md) — 将 RN 作为预构建的 AAR / XCFramework。
- [./brownfield-integrated.md](./brownfield-integrated.md) — 将 RN 直接加入现有的 Gradle / CocoaPods。

## 快速决策规则

- **选择 isolated**，如果原生团队必须将 React Native 作为常规库（AAR 或 XCFramework）来使用，而不安装 Node、Yarn 或 RN 工具链。
- **选择 isolated**，如果 React Native 与原生应用位于**不同的仓库**，或者按**不同的节奏发布**。
- **选择 isolated**，如果现有原生构建被深度定制（Tuist、Bazel、Buck、自定义 Gradle 插件），引入 React Native Gradle 插件或 CocoaPods autolinking 会带来较大改动。
- **选择 integrated**，如果**单一团队**同时拥有原生与 React Native 代码，并且愿意在原生项目内部维护 RN 构建链。
- **选择 integrated**，如果你希望**热重载、JS 源码映射和 devtools** 能在现有原生构建中"开箱即用"，无需额外编排。
- **选择 integrated**，如果你预计会添加很多 Expo 模块，并希望它们通过标准 Expo 工具自动链接，而不是每次都重新构建为一个全新产物。

当你不确定时——尤其是当问题是"原生团队能否避免使用 React Native 工具链？"——选择 **isolated**。

## 对比

| 维度                                            | Isolated                                                                | Integrated                                                            |
| ---------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 向原生应用交付的内容                         | 预构建的 AAR + XCFramework                                              | 将 React Native + Expo 源码自动链接到现有构建中       |
| 原生团队是否需要 Node / Yarn / RN CLI               | **不需要**                                                                  | **需要**                                                               |
| 对构建系统的影响范围                               | 极小——只需一个 Maven 依赖和两个嵌入的 XCFramework               | 全面铺开——React Native Gradle 插件、Podfile、autolinking、codegen |
| RN 开发者的迭代速度                          | 隔离场景下很快；原生侧需要重新构建以获取新产物        | 端到端快速；一次合并构建                                   |
| 开发期热重载                                  | 支持（通过 Metro，在 debug 下运行消费应用时）                 | 支持（原生构建内嵌 Metro 检测）                             |
| 生产环境 JS bundle 的位置                        | 嵌入在 AAR/XCFramework 内部                                         | 由 RN Gradle 插件 / Xcode 构建阶段嵌入到 APK/IPA 中   |
| 维护职责归属                                | RN 团队负责产物流水线；原生团队负责消费侧构建 | 单一团队负责统一构建                                       |
| 是否适合渐进采用                 | 非常适合——可以轻松接入现有应用的单个屏幕                  | 也很适合，但首个屏幕渲染前的配置工作更多             |
| 是否适合多仓库 / 多团队场景       | 非常适合                                                                    | 不太适合——往往需要 monorepo                                     |
| 与现有工具链发生构建系统冲突的风险 | 低                                                                     | 较高（RN Gradle 插件、codegen、Podfile 假设）               |
| RN 变更的重新发布流程                   | `npx expo-brownfield build:*` 然后升级依赖                  | 重新构建原生应用                                                |

## 常见场景

**"React Native 代码在 `xyz-react`，原生应用在 `xyz-ios` 和 `xyz-android`，各自独立发布。"**
→ **Isolated。** 构建带版本的产物（如 `com.xyz:onboarding:1.4.0`、`Onboarding.xcframework`）。原生应用像其他依赖一样固定某个版本。

**"我们的应用使用了深度定制的 Gradle 配置，包含多个 variant 和 flavor。"**
→ **Isolated。** RN Gradle 插件对 variant 命名和 bundle 输出路径有自己的约定，与非标准 variant 干净整合并不简单。

**"我们还不知道 RN 是否会长期保留——希望将来能低成本地移除它。"**
→ **Isolated。** 删除依赖即可移除 framework，原生构建几乎不受影响。

**"我们的 iOS 团队使用 Tuist，并且拒绝在 iOS 构建中加入 Node。"**
→ **Isolated。** 直接交付一个 XCFramework。iOS 团队只需添加两个 `.xcframework` 文件，并在 `AppDelegate` 中调用一次 `ReactNativeHostManager.shared.initialize()`。无需 Node，也无需修改 Expo 的 CocoaPods 配置。

**"我们只有一个仓库、一个团队，希望将 React Native 与现有 Android 应用的 onboarding 流程深度集成。"**
→ **Integrated。** 将现有的 `android-project` 移入 `my-project/android/`，在 `settings.gradle` 中添加 React Native Gradle 插件，注册 `MainApplication`，并在 `ReactActivity` 中承载该流程。一条构建流水线就够了。

**"我们希望在 RN 代码上使用 CNG，不必担心手动升级 RN。"**
→ **Isolated。** AAR/XCFramework 方式将 Expo RN 版本与原生应用的构建解耦，因此你可以独立于原生应用的发布周期升级 Expo 和 React Native。而集成式则需要在 RN 版本与原生应用构建之间做更多协调。

## 两种方式之间完全相同的部分

- React Native + Expo 源码本身 —— 同一个 Expo 项目、同一个 `app.json`、同一套模块 —— 它们只在**交付方式**上有所不同。
- 通过 `AppRegistry.registerComponent("main", () => App)` 注册的 JavaScript 模块是相同的；原生侧在两种流程中传入的都是同一个 `moduleName` 字符串。

## 运行时不同的部分

- **Isolated** 使用 Expo 的 brownfield 运行时包装器 —— `ReactNativeHostManager`、`BrownfieldActivity`、`ReactNativeViewController`、`ReactNativeView`。这些由 `npx expo-brownfield build:*` 生成，并打包到产物中。
- **Integrated** 使用标准的 React Native 运行时 —— `ReactActivity`、`ReactActivityDelegate`、`RCTReactNativeFactory`、`ExpoReactNativeFactory` —— 由 `react-native` 和 `expo` 直接暴露。