---
name: expo-ui-swift-ui
description: >
  使用 `@expo/ui/swift-ui` 包在 Expo 中构建 iOS 原生 SwiftUI 界面。当用户要求"用 SwiftUI 写 Expo 应用"、"在 Expo 中嵌入 SwiftUI"、"@expo/ui/swift-ui 用法"时使用。触发词：expo-ui、swift-ui、SwiftUI、Expo SDK 55、iOS 原生 UI、RNHostView。
risk: unknown
source: community
---

---
name: expo-ui-swift-ui
description: `@expo/ui/swift-ui` 包允许你在应用中使用 SwiftUI 视图和修饰符。
---

> 本技能中的说明仅适用于 SDK 55。其他 SDK 版本请参考对应版本的 Expo UI SwiftUI 文档获取最准确信息。

## 何时使用

- 你需要在 Expo 中使用 `@expo/ui/swift-ui` 构建 iOS 原生界面。
- 任务涉及选择 SwiftUI 视图或修饰符、将组件树包裹在 `Host` 中，或在 SwiftUI 树中嵌入 React Native 组件（`RNHostView`）。
- 你针对的是 Expo SDK 55 的 SwiftUI 集成行为和扩展指南。

## 安装

```bash
npx expo install @expo/ui
```

安装后需进行原生重建（`npx expo run:ios`）。

## 使用说明

- Expo UI 的 API 与 SwiftUI 的 API 对应。使用 SwiftUI 的知识来决定使用哪些组件或修饰符。
- 组件从 `@expo/ui/swift-ui` 导入，修饰符从 `@expo/ui/swift-ui/modifiers` 导入。
- 准备使用某个组件时，先拉取其文档确认 API —— https://docs.expo.dev/versions/v55.0.0/sdk/ui/swift-ui/{component-name}/index.md
- 不确定修饰符的 API 时，查阅文档 —— https://docs.expo.dev/versions/v55.0.0/sdk/ui/swift-ui/modifiers/index.md
- 每个 SwiftUI 树都必须包裹在 `Host` 中。
- `RNHostView` 专门用于在 SwiftUI 树中嵌入 RN 组件。示例：

```jsx
import { Host, VStack, RNHostView } from "@expo-ui/swift-ui";
import { Pressable } from "react-native";

<Host matchContents>
  <VStack>
    <RNHostView matchContents>
      // 此处的 `Pressable` 是 RN 组件，所以包裹在 `RNHostView` 中。
      <Pressable />
    </RNHostView>
  </VStack>
</Host>;
```

- 如果 Expo UI 中缺少必需的修饰符或视图，可以通过本地 Expo 模块扩展。参见：https://docs.expo.dev/guides/expo-ui-swift-ui/extending/index.md。扩展前请与用户确认。

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
