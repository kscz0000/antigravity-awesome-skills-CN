---
title: 使用 contentInsetAdjustmentBehavior 处理安全区域
impact: MEDIUM
impactDescription: 原生安全区域处理，无布局偏移
tags: safe-area, scrollview, layout
---

## 使用 contentInsetAdjustmentBehavior 处理安全区域

在根 ScrollView 上使用 `contentInsetAdjustmentBehavior="automatic"`，而非用 SafeAreaView 包裹内容或手动添加内边距。这让 iOS 原生处理安全区域内边距，并提供正确的滚动行为。

**错误（SafeAreaView 包裹）：**

```tsx
import { SafeAreaView, ScrollView, View, Text } from 'react-native'

function MyScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ScrollView>
        <View>
          <Text>Content</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}
```

**错误（手动安全区域内边距）：**

```tsx
import { ScrollView, View, Text } from 'react-native'
import { useSafeAreaInsets } from 'react-native-safe-area-context'

function MyScreen() {
  const insets = useSafeAreaInsets()

  return (
    <ScrollView contentContainerStyle={{ paddingTop: insets.top }}>
      <View>
        <Text>Content</Text>
      </View>
    </ScrollView>
  )
}
```

**正确（原生内容内边距调整）：**

```tsx
import { ScrollView, View, Text } from 'react-native'

function MyScreen() {
  return (
    <ScrollView contentInsetAdjustmentBehavior='automatic'>
      <View>
        <Text>Content</Text>
      </View>
    </ScrollView>
  )
}
```

原生方式能处理动态安全区域（键盘、工具栏），并允许内容自然地滚动到状态栏后方。
