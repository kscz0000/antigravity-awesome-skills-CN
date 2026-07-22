# 通用 `@expo/ui` 组件

> 要求 Expo SDK 56+。

通用组件是对各平台原生 UI 工具包的统一 API 层：Android 上是 Jetpack Compose、iOS 上是 SwiftUI、Web 上是 `react-native-web` / `react-dom`。你只需编写一份组件树，即可在三大平台上无需修改地运行，同时保持原生的观感——无需 `.ios.tsx` / `.android.tsx` 拆分。

## 用法

从包根目录（`@expo/ui`）导入所有内容，包括 `Host`。每个组件树都必须用 `Host` 包裹。

```tsx
import { Host, Column, Button, Text } from '@expo/ui';

<Host matchContents>
  <Column>
    <Text>Hello</Text>
    <Button onPress={() => alert('Pressed!')}>Press me</Button>
  </Column>
</Host>;
```

## 组件

| 分类 | 组件 |
|----------|------------|
| 容器 | `Host`（必需的根包裹器） |
| 布局 | `Column`、`Row`、`Spacer`、`ScrollView` |
| 展示 | `Text`、`Icon` |
| 控件 | `Button`、`Switch`、`Checkbox`、`Slider`、`TextInput`、`Picker` |
| 展开与展示 | `BottomSheet`、`Collapsible` |
| 集合与表单 | `List`（配合 `ListItem`）、`FieldGroup` |

> **`List` 不适用于大型列表。** 每个 `ListItem` 都是一个在 JS 线程上处理的 JSX 节点——数据量大时会出现明显的卡顿。

## TextInput 与 useNativeState

`@expo/ui` 中的 `TextInput` **与 React Native 的 TextInput 不同**——它的 `value` 和 `selection` 属性接收的是 `ObservableState` 对象（来自 `useNativeState`），而不是普通字符串。这正是实现同步、无闪烁更新的关键：用户输入时，`onChangeText` 作为 worklet 在 UI 线程上运行，直接写入 `value`，无需经过 React 渲染周期。

需要安装 `react-native-worklets`。如果没有它，worklet 指令不会生效，闪烁问题仍然存在。

```tsx
import { Host, TextInput, useNativeState } from '@expo/ui';
import { useCallback } from 'react';

export default function MyInput() {
  const text = useNativeState('');

  const handleChangeText = useCallback((value: string) => {
    'worklet';
    // 在 UI 线程上同步转换——不触发 React 重渲染
    text.value = value === 'Hello' ? 'World' : value;
  }, [text]);

  return (
    <Host matchContents>
      <TextInput value={text} onChangeText={handleChangeText} placeholder="Type here" />
    </Host>
  );
}
```

文档 — https://docs.expo.dev/versions/latest/sdk/ui/universal/textinput/index.md

## 确认 API

`@expo/ui` 的版本与 Expo SDK 绑定（例如 SDK 56 对应 `56.0.x`），其 API 在不同 SDK 版本之间可能会变化，因此**已安装包的 TypeScript 类型文件（`.d.ts`）是最可靠的真相来源**——它们与你项目中的版本匹配，而文档则跟随最新版本。请从已安装的 `@expo/ui` 包的 `node_modules` 中读取相应组件的 `.d.ts`。将文档作为人类可读的参考：

- 概述 — https://docs.expo.dev/versions/latest/sdk/ui/universal/index.md
- 各组件 — https://docs.expo.dev/versions/latest/sdk/ui/universal/{component-name}/index.md

## 何时下沉到平台专属层

只要通用组件能满足需求，就选择它们。只有在通用 API 没有暴露你需要的组件、修饰符或平台专属行为时，才下沉到 `@expo/ui/swift-ui` 或 `@expo/ui/jetpack-compose`——并接受由此带来的每平台文件拆分要求。详见 `./swift-ui.md` 和 `./jetpack-compose.md`。