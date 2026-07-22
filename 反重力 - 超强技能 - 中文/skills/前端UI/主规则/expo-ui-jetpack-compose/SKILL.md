---
name: expo-ui-jetpack-compose
description: >
  使用 `@expo/ui/jetpack-compose` 包在 Expo 中构建 Android 原生 Jetpack Compose 界面。当用户要求"用 Jetpack Compose 写 Expo 应用"、"在 Expo 中嵌入 Compose"、"@expo/ui/jetpack-compose 用法"时使用。触发词：expo-ui、jetpack-compose、Jetpack Compose、Expo SDK 55、Android 原生 UI、Material Design 3。
risk: unknown
source: community
---

---
name: expo-ui-jetpack-compose
description: `@expo/ui/jetpack-compose` 包允许你在应用中使用 Jetpack Compose 视图和修饰符。
---

> 本技能中的说明仅适用于 SDK 55。其他 SDK 版本请参考对应版本的 Expo UI Jetpack Compose 文档获取最准确信息。

## 何时使用

- 你需要在 Expo 中使用 `@expo/ui/jetpack-compose` 构建 Android 原生界面。
- 任务涉及选择 Compose 视图或修饰符、将它们嵌入 `Host`，或将 Jetpack Compose 模式翻译为 Expo UI 代码。
- 你针对的是 Expo SDK 55 的 Jetpack Compose 集成行为。

## 安装

```bash
npx expo install @expo/ui
```

安装后需进行原生重建（`npx expo run:android`）。

## 使用说明

- Expo UI 的 API 与 Jetpack Compose 的 API 对应。使用 Jetpack Compose 与 Material Design 3 的知识来决定使用哪些组件或修饰符。
- 组件从 `@expo/ui/jetpack-compose` 导入，修饰符从 `@expo/ui/jetpack-compose/modifiers` 导入。
- 准备使用某个组件时，先拉取其文档确认 API —— https://docs.expo.dev/versions/v55.0.0/sdk/ui/jetpack-compose/{component-name}/index.md
- 不确定修饰符的 API 时，查阅文档 —— https://docs.expo.dev/versions/v55.0.0/sdk/ui/jetpack-compose/modifiers/index.md
- 每个 Jetpack Compose 树都必须包裹在 `Host` 中。需要内禀大小时用 `<Host matchContents>`，需要显式大小时（例如作为 `LazyColumn` 的父组件）用 `<Host style={{ flex: 1 }}>`。示例：

```jsx
import { Host, Column, Button, Text } from "@expo/ui/jetpack-compose";
import { fillMaxWidth, paddingAll } from "@expo/ui/jetpack-compose/modifiers";

<Host matchContents>
  <Column verticalArrangement={{ spacedBy: 8 }} modifiers={[fillMaxWidth(), paddingAll(16)]}>
    <Text style={{ typography: "titleLarge" }}>你好</Text>
    <Button onPress={() => alert("已按下")}>按下我</Button>
  </Column>
</Host>;
```

## 关键组件

- **LazyColumn** —— 用于可滚动列表，替代 react-native 的 `ScrollView`/`FlatList`。包裹在 `<Host style={{ flex: 1 }}>` 中。
- **Icon** —— 使用 `<Icon source={require('./icon.xml')} size={24} />`，配合 Android XML 矢量图（来自 [Material Symbols](https://fonts.google.com/icons)）。

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
