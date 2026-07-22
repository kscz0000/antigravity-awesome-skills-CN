# 平台专属 iOS UI：`@expo/ui/swift-ui`

> **仅适用于 iOS。** 从 `@expo/ui/swift-ui` 导入的代码在 Android 上会崩溃，并抛出 "Unable to get view config" 错误。请始终将此类代码放在 `.ios.tsx` 组件文件中，或用 `Platform.OS === 'ios'` 做守卫。`Host` 必须从 `@expo/ui`（通用包根目录）导入，而不是从 `@expo/ui/swift-ui`。

仅当通用 `@expo/ui` 组件无法覆盖你在 iOS 上的需求时（请先参阅 `./universal.md`），再使用本层。这需要一份平台专属的组件树。

### Expo Router 中的文件放置

**不要把 `.ios.tsx` 文件放在 `app/` 或 `src/app/` 内。** Expo Router 不支持路由文件使用平台扩展名后缀，会抛出 "no fallback sibling" 渲染错误。

将平台专属组件文件放在 `components/`（或路由树之外的任何目录）中，然后在常规路由文件中导入：

```
src/components/ProfileEditor.ios.tsx   ← SwiftUI 组件树放在这里
src/app/profile-editor.tsx             ← 常规 Expo Router 路由，导入组件
```

`src/app/profile-editor.tsx`：
```tsx
import ProfileEditor from '../components/ProfileEditor';
export default ProfileEditor;
```

另一种方式是全部放在一个常规路由文件中，通过 `Platform.OS` 进行分支：

```tsx
// src/app/profile-editor.tsx
import { Platform } from 'react-native';
// 仅在 iOS 时导入 SwiftUI 组件，避免在 Android 上崩溃
const SwiftUIForm = Platform.OS === 'ios' ? require('../components/ProfileEditor.ios').default : null;
```

更简单的方式是，把 `Platform.OS` 守卫和 SwiftUI 导入放在同一个路由文件中（这样是安全的，因为在 `components/` 中使用平台扩展名时，Metro 只在 iOS 构建中打包 `.ios.tsx` 导入）。

## 指引

- Expo UI 的 API 与 SwiftUI 的 API 一致。利用 SwiftUI 的知识来决定使用哪些组件或修饰符。
- 组件从 `@expo/ui/swift-ui` 导入，修饰符从 `@expo/ui/swift-ui/modifiers` 导入。
- **在编写任何代码之前，请先运行 list-components 脚本**，获取已安装版本中可用的精确组件和修饰符：
  ```bash
  node <skill-root>/scripts/list-components.js <project-path>          # 仅名称（紧凑）
  node <skill-root>/scripts/list-components.js <project-path> --docs   # 附一行说明
  ```
  （`<skill-root>` 是包含 `references/` 目录的文件夹路径。）
- **已安装包的 TypeScript 类型文件（`.d.ts`）是最可靠的真相来源**——用于确认属性形状与签名。请从已安装的 `@expo/ui/swift-ui` 包的 `node_modules` 中读取相应 `{Component}/index.d.ts`。将下面的文档作为人类可读的参考。
- 使用某个组件前，请查阅其文档确认 API — https://docs.expo.dev/versions/latest/sdk/ui/swift-ui/{component-name}/index.md
- 对修饰符的 API 有疑问时，请参考文档 — https://docs.expo.dev/versions/latest/sdk/ui/swift-ui/modifiers/index.md
- 每个 SwiftUI 组件树都必须用 `Host` 包裹。
- `RNHostView` 用于在 SwiftUI 组件树中嵌入 RN 组件。示例：

```jsx
import { Host } from "@expo/ui";                       // Host 始终从通用包根目录导入
import { VStack, RNHostView } from "@expo/ui/swift-ui"; // 平台组件从 swift-ui 导入
import { Pressable } from "react-native";

<Host matchContents>
  <VStack>
    <RNHostView matchContents>
      // 此处 `Pressable` 是 RN 组件，因此包裹在 `RNHostView` 中。
      <Pressable />
    </RNHostView>
  </VStack>
</Host>;
```

- 如果 Expo UI 中缺少必需的修饰符或 View，可以通过本地 Expo 模块扩展。参见：https://docs.expo.dev/guides/expo-ui-swift-ui/extending/index.md。扩展前请与用户确认。

## useNativeState

`useNativeState` 创建通过 worklet 在 UI 线程上同步更新的可观察状态，能够在不等待 React 渲染周期的情况下即时改变原生状态。需要 `react-native-worklets`——没有它，更新仍会经过 React，闪烁问题仍然存在。最适合那些同步更新至关重要的实时交互场景，例如在用户输入时进行掩码或格式化处理的文本框。

- `ObservableState.value` 可以在 worklet 中读写；`onChange` 在状态变更时触发 worklet 监听器。
- 文档 — https://docs.expo.dev/versions/latest/sdk/ui/swift-ui/usenativestate/index.md