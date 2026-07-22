---
title: 字符串必须包裹在 Text 组件中
impact: CRITICAL
impactDescription: 防止运行时崩溃
tags: rendering, text, core
---

## 字符串必须包裹在 Text 组件中

字符串必须在 `<Text>` 内渲染。如果字符串是 `<View>` 的直接子元素，React Native 会崩溃。

**错误（崩溃）：**

```tsx
import { View } from 'react-native'

function Greeting({ name }: { name: string }) {
  return <View>Hello, {name}!</View>
}
// Error: Text strings must be rendered within a <Text> component.
```

**正确：**

```tsx
import { View, Text } from 'react-native'

function Greeting({ name }: { name: string }) {
  return (
    <View>
      <Text>Hello, {name}!</Text>
    </View>
  )
}
```
