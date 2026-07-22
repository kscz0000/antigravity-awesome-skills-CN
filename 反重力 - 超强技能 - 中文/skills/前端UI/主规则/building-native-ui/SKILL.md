---
name: building-native-ui
description: 使用 Expo Router 构建精美应用的完整指南。涵盖基础、样式、组件、导航、动画、模式和原生标签页。当用户要求'构建原生UI'、'Expo Router应用'、'Expo导航'、'原生标签页'、'Expo动画'或'Expo样式'时使用。
risk: unknown
source: community
version: 1.0.1
license: MIT
---

# Expo UI 指南

## 适用场景
- 你正在构建原生体验的 Expo Router 应用，需要导航、控件、效果或平台特定 UI 方面的指导。
- 你需要判断 Expo Go 是否够用，还是确实需要自定义原生构建。
- 任务涉及动画、标签页、头部、存储、媒体或视觉效果等现代 Expo UI 模式。

## 参考资料

根据需要查阅以下资源：

```
references/
  animations.md          Reanimated：进入、退出、布局、滚动驱动、手势
  controls.md            原生 iOS：Switch、Slider、SegmentedControl、DateTimePicker、Picker
  form-sheet.md          expo-router 中的表单 Sheet：配置、底部栏和背景交互
  gradients.md           通过 experimental_backgroundImage 实现 CSS 渐变（仅新架构）
  icons.md               通过 expo-image 使用 SF Symbols（sf: source）、名称、动画、字重
  media.md               相机、音频、视频和文件保存
  route-structure.md     路由约定、动态路由、分组、文件夹组织
  search.md              带头部的搜索栏、useSearch hook、过滤模式
  storage.md             SQLite、AsyncStorage、SecureStore
  tabs.md                NativeTabs、从 JS 标签页迁移、iOS 26 特性
  toolbar-and-headers.md Stack 头部和工具栏按钮、菜单、搜索（仅 iOS）
  visual-effects.md      模糊（expo-blur）和液态玻璃（expo-glass-effect）
  webgpu-three.md        使用 WebGPU 和 Three.js 实现 3D 图形、游戏、GPU 可视化
  zoom-transitions.md    Apple Zoom：通过 Link.AppleZoom 实现流畅缩放转场（iOS 18+）
```

## 运行应用

**关键：创建自定义构建之前，务必先尝试 Expo Go。**

大多数 Expo 应用无需任何自定义原生代码即可在 Expo Go 中运行。在运行 `npx expo run:ios` 或 `npx expo run:android` 之前：

1. **从 Expo Go 开始**：运行 `npx expo start` 并用 Expo Go 扫描二维码
2. **检查功能是否正常**：在 Expo Go 中充分测试你的应用
3. **仅在必要时创建自定义构建** — 见下文

### 何时需要自定义构建

仅在以下情况才需要 `npx expo run:ios/android` 或 `eas build`：

- **本地 Expo 模块**（`modules/` 中的自定义原生代码）
- **Apple targets**（通过 `@bacons/apple-targets` 实现的小组件、App Clips、扩展）
- **Expo Go 未包含的第三方原生模块**
- **无法在 `app.json` 中表达的自定义原生配置**

### Expo Go 可用的场景

Expo Go 开箱即支持大量功能：

- 所有 `expo-*` 包（相机、定位、通知等）
- Expo Router 导航
- 大多数 UI 库（reanimated、gesture handler 等）
- 推送通知、深度链接等

**如果不确定，先试 Expo Go。** 创建自定义构建会增加复杂度、降低迭代速度，还需要配置 Xcode/Android Studio。

## 代码风格

- 注意未闭合的字符串。确保嵌套的反引号已转义；切勿忘记正确转义引号。
- 始终在文件顶部使用 import 语句。
- 文件名始终使用 kebab-case，例如 `comment-card.tsx`
- 移动或重构导航时，始终删除旧的路由文件
- 文件名中不要使用特殊字符
- 在 tsconfig.json 中配置路径别名，重构时优先使用别名而非相对导入。

## 路由

详细路由约定见 `./references/route-structure.md`。

- 路由放在 `app` 目录中。
- 不要在 app 目录中混放组件、类型或工具函数。这是反模式。
- 确保应用始终有匹配 "/" 的路由，它可以在分组路由内。

## 库偏好

- 不要使用已从 React Native 中移除的模块，如 Picker、WebView、SafeAreaView 或 AsyncStorage
- 不要使用旧版 expo-permissions
- 用 `expo-audio` 而非 `expo-av`
- 用 `expo-video` 而非 `expo-av`
- 用 `expo-image` 配合 `source="sf:name"` 来使用 SF Symbols，而非 `expo-symbols` 或 `@expo/vector-icons`
- 用 `react-native-safe-area-context` 而非 react-native 的 SafeAreaView
- 用 `process.env.EXPO_OS` 而非 `Platform.OS`
- 用 `React.use` 而非 `React.useContext`
- 用 `expo-image` 的 Image 组件而非内置元素 `img`
- 用 `expo-glass-effect` 实现液态玻璃背景

## 响应式

- 始终将根组件包裹在 ScrollView 中以实现响应式
- 使用 `<ScrollView contentInsetAdjustmentBehavior="automatic" />` 而非 `<SafeAreaView>`，以获得更智能的安全区域适配
- `contentInsetAdjustmentBehavior="automatic"` 也应应用于 FlatList 和 SectionList
- 使用 flexbox 而非 Dimensions API
- 始终优先使用 `useWindowDimensions` 而非 `Dimensions.get()` 来测量屏幕尺寸

## 行为

- 在 iOS 上有条件地使用 expo-haptics 以提升体验
- 使用内置触觉反馈的视图，如 React Native 的 `<Switch />` 和 `@react-native-community/datetimepicker`
- 当路由属于 Stack 时，其第一个子元素几乎总是应设为带有 `contentInsetAdjustmentBehavior="automatic"` 的 ScrollView
- 在页面中添加 `ScrollView` 时，它几乎总是应作为路由组件内的第一个组件
- 优先使用 Stack.Screen options 中的 `headerSearchBarOptions` 来添加搜索栏
- 对可能需要复制的数据文本使用 `<Text selectable />` 属性
- 考虑将大数字格式化为 1.4M 或 38k
- 除非在 webview 或 Expo DOM 组件中，否则不要使用 'img' 或 'div' 等内置元素

# 样式

遵循 Apple 人机界面指南。

## 通用样式规则

- 优先使用 flex gap 而非 margin 和 padding 样式
- 在可能的情况下优先使用 padding 而非 margin
- 始终处理安全区域，可通过 stack 头部、标签页或 ScrollView/FlatList 的 `contentInsetAdjustmentBehavior="automatic"`
- 确保顶部和底部安全区域都已处理
- 使用内联样式而非 StyleSheet.create，除非复用样式更快
- 为状态变化添加进入和退出动画
- 圆角使用 `{ borderCurve: 'continuous' }`，除非创建胶囊形状
- 始终使用导航栈标题而非页面上的自定义文本元素
- 为 ScrollView 添加内边距时，使用 `contentContainerStyle` 的 padding 和 gap 而非 ScrollView 本身的 padding（减少裁剪）
- 不支持 CSS 和 Tailwind — 使用内联样式

## 文本样式

- 为每个显示重要数据或错误信息的 `<Text/>` 元素添加 `selectable` 属性
- 计数器应使用 `{ fontVariant: 'tabular-nums' }` 以实现对齐

## 阴影

使用 CSS `boxShadow` 样式属性。切勿使用旧版 React Native 的 shadow 或 elevation 样式。

```tsx
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

支持 'inset' 阴影。

# 导航

## Link

使用 'expo-router' 的 `<Link href="/path" />` 进行路由间导航。

```tsx
import { Link } from 'expo-router';

// 基本链接
<Link href="/path" />

// 包裹自定义组件
<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

尽可能包含 `<Link.Preview>` 以遵循 iOS 惯例。频繁添加上下文菜单和预览以增强导航。

## Stack

- 始终使用 `_layout.tsx` 文件来定义 stack
- 使用 'expo-router/stack' 的 Stack 来实现原生导航栈

### 页面标题

在 Stack.Screen options 中设置页面标题：

```tsx
<Stack.Screen options={{ title: "Home" }} />
```

## 上下文菜单

为 Link 组件添加长按上下文菜单：

```tsx
import { Link } from "expo-router";

<Link href="/settings" asChild>
  <Link.Trigger>
    <Pressable>
      <Card />
    </Pressable>
  </Link.Trigger>
  <Link.Menu>
    <Link.MenuAction
      title="Share"
      icon="square.and.arrow.up"
      onPress={handleSharePress}
    />
    <Link.MenuAction
      title="Block"
      icon="nosign"
      destructive
      onPress={handleBlockPress}
    />
    <Link.Menu title="More" icon="ellipsis">
      <Link.MenuAction title="Copy" icon="doc.on.doc" onPress={() => {}} />
      <Link.MenuAction
        title="Delete"
        icon="trash"
        destructive
        onPress={() => {}}
      />
    </Link.Menu>
  </Link.Menu>
</Link>;
```

## 链接预览

频繁使用链接预览以增强导航：

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable>
      <Card />
    </Pressable>
  </Link.Trigger>
  <Link.Preview />
</Link>
```

链接预览可与上下文菜单配合使用。

## 模态框

将页面呈现为模态框：

```tsx
<Stack.Screen name="modal" options={{ presentation: "modal" }} />
```

优先使用此方式而非构建自定义模态框组件。

## Sheet

将页面呈现为动态表单 Sheet：

```tsx
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" },
  }}
/>
```

- 使用 `contentStyle: { backgroundColor: "transparent" }` 可在 iOS 26+ 上使背景呈现液态玻璃效果。

## 常见路由结构

标准应用布局：标签页 + 每个标签页内的 stack：

```
app/
  _layout.tsx — <NativeTabs />
  (index,search)/
    _layout.tsx — <Stack />
    index.tsx — 主列表
    search.tsx — 搜索视图
```

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";
import { Theme } from "../components/theme";

export default function Layout() {
  return (
    <Theme>
      <NativeTabs>
        <NativeTabs.Trigger name="(index)">
          <Icon sf="list.dash" />
          <Label>Items</Label>
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="(search)" role="search" />
      </NativeTabs>
    </Theme>
  );
}
```

创建共享分组路由，使两个标签页都能推送公共页面：

```tsx
// app/(index,search)/_layout.tsx
import { Stack } from "expo-router/stack";
import { PlatformColor } from "react-native";

export default function Layout({ segment }) {
  const screen = segment.match(/\((.*)\)/)?.[1]!;
  const titles: Record<string, string> = { index: "Items", search: "Search" };

  return (
    <Stack
      screenOptions={{
        headerTransparent: true,
        headerShadowVisible: false,
        headerLargeTitleShadowVisible: false,
        headerLargeStyle: { backgroundColor: "transparent" },
        headerTitleStyle: { color: PlatformColor("label") },
        headerLargeTitle: true,
        headerBlurEffect: "none",
        headerBackButtonDisplayMode: "minimal",
      }}
    >
      <Stack.Screen name={screen} options={{ title: titles[screen] }} />
      <Stack.Screen name="i/[id]" options={{ headerLargeTitle: false }} />
    </Stack>
  );
}
```

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
