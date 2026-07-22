---
title: 导航应使用原生导航器
impact: HIGH
impactDescription: 原生性能，符合平台规范的 UI
tags: navigation, react-navigation, expo-router, native-stack, tabs
---

## 导航应使用原生导航器

始终使用原生导航器而非基于 JS 的导航器。原生导航器利用平台 API（iOS 上的 UINavigationController，Android 上的 Fragment）实现更好的性能和原生行为。JS 导航器在 JavaScript 线程中处理转场动画，容易造成卡顿；原生导航器直接在 UI 线程执行，体验更流畅。

**对于堆栈导航：** 使用 `@react-navigation/native-stack` 或 expo-router 的默认堆栈（它使用 native-stack）。避免使用 `@react-navigation/stack`，因为它基于 JS 实现转场。

**对于标签页导航：** 使用 `react-native-bottom-tabs`（原生）或 expo-router 的原生标签页。当原生体验重要时，避免使用 `@react-navigation/bottom-tabs`，因为它同样基于 JS 渲染。

### 堆栈导航

以下展示 JS 堆栈导航器与原生堆栈导航器的对比。

**错误（JS 堆栈导航器）：**

```tsx
import { createStackNavigator } from '@react-navigation/stack'

const Stack = createStackNavigator()

function App() {
  return (
    <Stack.Navigator>
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='Details' component={DetailsScreen} />
    </Stack.Navigator>
  )
}
```

**正确（react-navigation 原生堆栈）：**

```tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack'

const Stack = createNativeStackNavigator()

function App() {
  return (
    <Stack.Navigator>
      <Stack.Screen name='Home' component={HomeScreen} />
      <Stack.Screen name='Details' component={DetailsScreen} />
    </Stack.Navigator>
  )
}
```

**正确（expo-router 默认使用原生堆栈）：**

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router'

export default function Layout() {
  return <Stack />
}
```

### 标签页导航

标签页导航同样应使用原生实现。原生标签页在 iOS 上自动处理安全区域内边距和半透明效果。

**错误（JS 底部标签页）：**

```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'

const Tab = createBottomTabNavigator()

function App() {
  return (
    <Tab.Navigator>
      <Tab.Screen name='Home' component={HomeScreen} />
      <Tab.Screen name='Settings' component={SettingsScreen} />
    </Tab.Navigator>
  )
}
```

**正确（react-navigation 原生底部标签页）：**

```tsx
import { createNativeBottomTabNavigator } from '@bottom-tabs/react-navigation'

const Tab = createNativeBottomTabNavigator()

function App() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name='Home'
        component={HomeScreen}
        options={{
          tabBarIcon: () => ({ sfSymbol: 'house' }),
        }}
      />
      <Tab.Screen
        name='Settings'
        component={SettingsScreen}
        options={{
          tabBarIcon: () => ({ sfSymbol: 'gear' }),
        }}
      />
    </Tab.Navigator>
  )
}
```

**正确（expo-router 原生标签页）：**

```tsx
// app/(tabs)/_layout.tsx
import { NativeTabs } from 'expo-router/unstable-native-tabs'

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name='index'>
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf='house.fill' md='home' />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name='settings'>
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf='gear' md='settings' />
      </NativeTabs.Trigger>
    </NativeTabs>
  )
}
```

在 iOS 上，原生标签页会自动在每个标签页根部的第一个 `ScrollView` 上启用 `contentInsetAdjustmentBehavior`，使内容能正确地在半透明标签栏后方滚动。如需禁用此行为，在 Trigger 上使用 `disableAutomaticContentInsets`。

### 优先使用原生头部选项而非自定义组件

使用原生头部选项（如 `title`、`headerLargeTitleEnabled`）而非自定义头部组件。原生头部提供了更好的平台一致性和性能。

**错误（自定义头部组件）：**

```tsx
<Stack.Screen
  name='Profile'
  component={ProfileScreen}
  options={{
    header: () => <CustomHeader title='Profile' />,
  }}
/>
```

**正确（原生头部选项）：**

```tsx
<Stack.Screen
  name='Profile'
  component={ProfileScreen}
  options={{
    title: 'Profile',
    headerLargeTitleEnabled: true,
    headerSearchBarOptions: {
      placeholder: 'Search',
    },
  }}
/>
```

原生头部自动支持 iOS 大标题、搜索栏、模糊效果和正确的安全区域处理。

### 为什么使用原生导航器

选择原生导航器的核心原因如下：

- **性能**：原生转场和手势运行在 UI 线程
- **平台行为**：自动支持 iOS 大标题、Android Material Design
- **系统集成**：标签页点击回到顶部、画中画避让、正确的安全区域
- **无障碍**：平台无障碍功能自动生效

参考：

- [React Navigation Native Stack](https://reactnavigation.org/docs/native-stack-navigator)
- [React Native Bottom Tabs with React Navigation](https://oss.callstack.com/react-native-bottom-tabs/docs/guides/usage-with-react-navigation)
- [React Native Bottom Tabs with Expo Router](https://oss.callstack.com/react-native-bottom-tabs/docs/guides/usage-with-expo-router)
- [Expo Router Native Tabs](https://docs.expo.dev/router/advanced/native-tabs)
