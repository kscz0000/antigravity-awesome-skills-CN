---
name: expo-brownfield
description: 将 Expo 和 React Native 集成到现有的原生 iOS 或 Android 应用中。在用户提到 brownfield、将 React Native 嵌入原生应用、AAR/XCFramework，或将 Expo 添加到现有的 Kotlin/Swift 项目时使用。同时涵盖隔离方式和集成方式。
risk: unknown
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-brownfield
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# Expo Brownfield（Expo 现存项目集成）
## 何时使用

当你需要将 Expo 和 React Native 集成到现有的原生 iOS 或 Android 应用中时，请使用此技能。在用户提到 brownfield、将 React Native 嵌入原生应用、AAR/XCFramework，或将 Expo 添加到现有的 Kotlin/Swift 项目时使用。同时涵盖隔离方式和集成方式。


**brownfield**（存量项目）应用是指一个已存在的原生 iOS 或 Android 应用，它以渐进方式引入 React Native；与之相对的 **greenfield**（全新项目）应用则是从第一天起就基于 React Native 构建。

Expo 支持两种不同的方式将 React Native 添加到 brownfield 项目中：

| 方式 | 向原生应用交付的内容 | 何时选择 |
| -------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Isolated（隔离式）**   | 预构建的 AAR / XCFramework                                          | 原生团队不需要 Node 或 RN 工具链；RN 代码可以放在独立的仓库中 |
| **Integrated（集成式）** | 将 React Native 源码加入现有的 Gradle / CocoaPods 构建系统 | 单一团队统一所有代码；能接受 RN 工具链；希望使用统一的构建流程 |

完整决策矩阵请参阅 [./references/comparison.md](./references/comparison.md)。

## 选择方式

使用以下快速决策规则——遇到任何不明确的情况请回退到 `comparison.md`。

- **选择 isolated**，如果 iOS/Android 团队必须将 RN 作为常规库依赖（AAR 或 XCFramework）来使用，而无需安装 Node、Yarn 或 React Native 构建工具链。
- **选择 isolated**，如果 RN 代码与原生代码位于不同的仓库，或者按照各自的节奏独立发布。
- **选择 integrated**，如果单一团队同时拥有原生和 RN 代码，并且愿意将 React Native + Expo 加入到原生项目的 Gradle 和 CocoaPods 配置中。
- **选择 integrated**，如果你希望在现有的原生构建流程中无缝使用热重载和 JS 源码映射。

## 参考文档

- ./references/brownfield-isolated.md -- 将 RN 构建为 AAR/XCFramework，并由原生应用消费（BrownfieldActivity、ReactNativeViewController、ReactNativeView）
- ./references/brownfield-integrated.md -- 将 RN 和 Expo 直接加入现有的 Gradle 和 CocoaPods 构建（ReactActivity、RCTRootView、Podfile）
- ./references/comparison.md -- 选择方式时的决策标准、权衡与场景映射
- ./references/troubleshooting.md -- 两种方式常见的 Metro 连接、构建、签名和模块解析问题

更多信息请访问 https://docs.expo.dev/brownfield/overview/

## 共享前置条件

两种方式都需要在负责构建 React Native 一侧的环境中安装：

- **Node.js（LTS）** — 用于运行 Expo CLI 和 JavaScript 代码。
- **Yarn** — 用于管理 JavaScript 依赖。

集成式另外需要在 iOS 上安装 **CocoaPods**（`sudo gem install cocoapods`）。隔离式在消费原生应用中**不**需要 CocoaPods 或任何 RN 工具链。

## 版本说明

**Expo SDK 55 是 brownfield 集成的最低支持版本。** 更早的 SDK 缺少 `expo-brownfield`、所需的 `ExpoReactHostFactory` / `ExpoReactNativeFactory` 入口以及当前的 autolinking 接入面。创建 Expo 项目时，请始终显式指定 SDK 版本：

```sh
npx create-expo-app@latest my-project --template default@sdk-55
```

在 RN 项目和任何被嵌入的依赖之间，请使用相同的 Expo SDK 版本。

## 局限性

- 仅当任务明显匹配其上游产品或 API 范围时才使用此技能。
- 在进行任何变更之前，请根据当前官方文档核对命令、API 行为、定价、配额、凭据及部署影响。
- 不要将生成的示例视为环境专属测试、安全审查或用户对破坏性或高成本操作的批准的替代品。