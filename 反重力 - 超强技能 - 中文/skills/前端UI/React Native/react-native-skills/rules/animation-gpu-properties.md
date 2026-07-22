---
title: Animate Transform and Opacity Instead of Layout Properties
impact: HIGH
impactDescription: GPU 加速动画，无需布局重算
tags: animation, performance, reanimated, transform, opacity
---

## 动画使用 Transform 和 Opacity 而非布局属性

避免动画化 `width`、`height`、`top`、`left`、`margin` 或 `padding`。这些属性每帧都会触发布局重算，导致性能下降和动画卡顿。应使用 `transform`（scale、translate）和 `opacity`，它们在 GPU 上运行而不触发布局重排，动画更流畅。布局属性的变化会强制浏览器或原生渲染引擎重新计算整个组件树的布局，这是非常昂贵的操作。

**错误示例（动画化 height，每帧触发布局）：**

```tsx
import Animated, { useAnimatedStyle, withTiming } from 'react-native-reanimated'

function CollapsiblePanel({ expanded }: { expanded: boolean }) {
  const animatedStyle = useAnimatedStyle(() => ({
    height: withTiming(expanded ? 200 : 0), // triggers layout on every frame
    overflow: 'hidden',
  }))

  return <Animated.View style={animatedStyle}>{children}</Animated.View>
}
```

**正确示例（动画化 scaleY，GPU 加速）：**

```tsx
import Animated, { useAnimatedStyle, withTiming } from 'react-native-reanimated'

function CollapsiblePanel({ expanded }: { expanded: boolean }) {
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { scaleY: withTiming(expanded ? 1 : 0) },
    ],
    opacity: withTiming(expanded ? 1 : 0),
  }))

  return (
    <Animated.View style={[{ height: 200, transformOrigin: 'top' }, animatedStyle]}>
      {children}
    </Animated.View>
  )
}
```

**正确示例（动画化 translateY 实现滑动动画）：**

```tsx
import Animated, { useAnimatedStyle, withTiming } from 'react-native-reanimated'

function SlideIn({ visible }: { visible: boolean }) {
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateY: withTiming(visible ? 0 : 100) },
    ],
    opacity: withTiming(visible ? 1 : 0),
  }))

  return <Animated.View style={animatedStyle}>{children}</Animated.View>
}
```

GPU 加速属性：`transform`（translate、scale、rotate）、`opacity`。其他所有视觉属性的变化都会触发布局重排，应避免在动画中使用。当需要折叠/展开效果时，优先使用 `scaleY` 配合 `transformOrigin`，而非动画化 `height`。
