# 平台专属 Android UI：`@expo/ui/jetpack-compose`

> **仅适用于 Android。** 从 `@expo/ui/jetpack-compose` 导入的代码在 iOS 上会崩溃，并抛出 "Unable to get view config" 错误。请始终将此类代码放在 `.android.tsx` 组件文件中，或用 `Platform.OS === 'android'` 做守卫。`Host` 必须从 `@expo/ui`（通用包根目录）导入，而不是从 `@expo/ui/jetpack-compose`。

仅当通用 `@expo/ui` 组件无法覆盖你在 Android 上的需求时（请先参阅 `./universal.md`），再使用本层。这需要一份平台专属的组件树。

### Expo Router 中的文件放置

**不要把 `.android.tsx` 文件放在 `app/` 或 `src/app/` 内。** Expo Router 不支持路由文件使用平台扩展名后缀，会抛出 "no fallback sibling" 渲染错误。

将平台专属组件文件放在 `components/`（或路由树之外的任何目录）中，然后在常规路由文件中导入：

```
src/components/ProductList.android.tsx   ← Compose 组件树放在这里
src/app/product-list.tsx                 ← 常规 Expo Router 路由，导入组件
```

`src/app/product-list.tsx`：
```tsx
import ProductList from '../components/ProductList';
export default ProductList;
```

另一种方式是全部放在一个常规路由文件中，通过 `Platform.OS` 进行分支：

```tsx
// src/app/product-list.tsx
import { Platform } from 'react-native';
const ComposeList = Platform.OS === 'android' ? require('../components/ProductList.android').default : null;
```

## 指引

- Expo UI 的 API 与 Jetpack Compose 的 API 一致。利用 Jetpack Compose 与 Material Design 3 的知识来决定使用哪些组件或修饰符。如果你需要更深入的 Jetpack Compose 或 Material 3 指引（例如该选用哪个组件、布局模式、主题化），请派生子代理研究 [Jetpack Compose](https://developer.android.com/develop/ui/compose/components) 和 [Material Design 3](https://m3.material.io/) 的最佳实践。
- 组件从 `@expo/ui/jetpack-compose` 导入，修饰符从 `@expo/ui/jetpack-compose/modifiers` 导入。
- **在编写任何代码之前，请先运行 list-components 脚本**，获取已安装版本中可用的精确组件和修饰符：
  ```bash
  node <skill-root>/scripts/list-components.js <project-path>          # 仅名称（紧凑）
  node <skill-root>/scripts/list-components.js <project-path> --docs   # 附一行说明
  ```
  （`<skill-root>` 是包含 `references/` 目录的文件夹路径。）
- **请始终阅读 `.d.ts` 类型文件**来确认属性形状与签名——从已安装的 `@expo/ui/jetpack-compose` 包的 `node_modules` 中读取相应的 `{ComponentName}/index.d.ts`。这是最可靠的真相来源。
- 使用某个组件前，请查阅其文档确认 API — https://docs.expo.dev/versions/latest/sdk/ui/jetpack-compose/{component-name}/index.md
- 对修饰符的 API 有疑问时，请参考文档 — https://docs.expo.dev/versions/latest/sdk/ui/jetpack-compose/modifiers/index.md
- 每个 Jetpack Compose 组件树都必须用 `Host` 包裹。需要按内容尺寸自适应时使用 `<Host matchContents>`；当需要显式尺寸时（例如作为 `LazyColumn` 的父组件）使用 `<Host style={{ flex: 1 }}>`。示例：

```jsx
import { Host } from "@expo/ui";                              // Host 始终从通用包根目录导入
import { Column, Button, Text } from "@expo/ui/jetpack-compose";
import { fillMaxWidth, paddingAll } from "@expo/ui/jetpack-compose/modifiers";

<Host matchContents>
  <Column verticalArrangement={{ spacedBy: 8 }} modifiers={[fillMaxWidth(), paddingAll(16)]}>
    <Text style={{ typography: "titleLarge" }}>Hello</Text>
    <Button onPress={() => alert("Pressed!")}>Press me</Button>
  </Column>
</Host>;
```

- `RNHostView` 用于在 Jetpack Compose 组件树中嵌入 React Native 组件（与 `@expo/ui/swift-ui` 中的概念相同）——将任何 RN 子组件包裹在 `<RNHostView>` 中。
- 如果 Expo UI 中缺少必需的 composable 或修饰符，可以通过本地 Expo 模块扩展。参见：https://docs.expo.dev/guides/expo-ui-jetpack-compose/extending/index.md。扩展前请与用户确认。

## 关键组件

- **LazyColumn** — 用于替代 react-native 的 `ScrollView`/`FlatList` 来实现可滚动列表。需用 `<Host style={{ flex: 1 }}>` 包裹。不适用于大型列表——每个 item 都是一个在 JS 线程上处理的 JSX 节点，规模一大就会出现明显的卡顿。
- **Icon** — 使用 `<Icon source={require('./icon.xml')} size={24} />` 配合 Android XML 矢量图。获取图标的方法：前往 [Material Symbols](https://fonts.google.com/icons)，选择一个图标，选择 Android 平台，下载 XML 矢量图。将其保存为项目 `assets/` 目录下的 `.xml` 文件（例如 `assets/icons/wifi.xml`）。Metro 会自动打包 `.xml` 资源——无需修改 metro 配置。

## useNativeState

`useNativeState` 创建通过 worklet 在 UI 线程上同步更新的可观察状态，能够在不等待 React 渲染周期的情况下即时改变原生状态。需要 `react-native-worklets`——没有它，更新仍会经过 React，闪烁问题仍然存在。最适合那些同步更新至关重要的实时交互场景，例如在用户输入时进行掩码或格式化处理的文本框。

- `ObservableState.value` 可以在 worklet 中读写；`onChange` 在状态变更时触发 worklet 监听器。
- 文档 — https://docs.expo.dev/versions/latest/sdk/ui/jetpack-compose/usenativestate/index.md