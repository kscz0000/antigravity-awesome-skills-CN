---
title: 使用 Pressable 替代 Touchable 组件
impact: LOW
impactDescription: 现代 API，更灵活
tags: ui, pressable, touchable, gestures
---

## 使用 Pressable 替代 Touchable 组件

绝不要使用 `TouchableOpacity` 或 `TouchableHighlight`。使用 `react-native` 或 `react-native-gesture-handler` 的 `Pressable` 替代。`Pressable` 是更现代的触摸反馈 API，提供了更细粒度的按压状态控制和更好的性能。

**核心区别**：`Pressable` 可以检测 `pressed`、`hovered`、`focused` 等多种交互状态，而旧版 Touchable 组件只支持简单的按压反馈。

**错误（过时的 Touchable 组件）：**

`TouchableOpacity` 和 `TouchableHighlight` 是旧版 API，功能有限且不支持细粒度的按压状态检测，已被官方标记为不推荐使用：

```tsx
import { TouchableOpacity } from 'react-native'

function MyButton({ onPress }: { onPress: () => void }) {
  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      <Text>Press me</Text>
    </TouchableOpacity>
  )
}
```

**正确（Pressable）：**

`Pressable` 提供了 `onPressIn`、`onPressOut`、`onLongPress` 等更丰富的事件回调：

```tsx
import { Pressable } from 'react-native'

function MyButton({ onPress }: { onPress: () => void }) {
  return (
    <Pressable onPress={onPress}>
      <Text>Press me</Text>
    </Pressable>
  )
}
```

**正确（列表中使用 gesture-handler 的 Pressable）：**

在可滚动列表中，应使用 `react-native-gesture-handler` 版本的 Pressable 以避免手势冲突：

```tsx
import { Pressable } from 'react-native-gesture-handler'

function ListItem({ onPress }: { onPress: () => void }) {
  return (
    <Pressable onPress={onPress}>
      <Text>Item</Text>
    </Pressable>
  )
}
```

在可滚动列表中使用 `react-native-gesture-handler` 的 Pressable 以获得更好的手势协调，前提是你也使用了 `react-native-gesture-handler` 的 ScrollView。否则滚动和按压手势可能产生冲突。

**对于带动画的按压状态（缩放、透明度变化）：** 使用 `GestureDetector` 配合 Reanimated 共享值，而非 Pressable 的样式回调。参见 `animation-gesture-detector-press` 规则。

**总结**：始终使用 `Pressable` 替代旧的 Touchable 组件。在列表中使用 gesture-handler 版本以避免手势冲突。需要动画反馈时，配合 Reanimated 而非 style 回调。这是 React Native 团队推荐的现代做法。
