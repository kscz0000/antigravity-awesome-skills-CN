---
title: Use GestureDetector for Animated Press States
impact: MEDIUM
impactDescription: UI 线程动画，更流畅的按压反馈
tags: animation, gestures, press, reanimated
---

## 使用 GestureDetector 实现动画按压状态

对于动画按压状态（如缩放、按下时的透明度变化），应使用 `GestureDetector` 配合
`Gesture.Tap()` 和共享值，而非 Pressable 的
`onPressIn`/`onPressOut`。手势回调作为 worklet 在 UI 线程运行——按压动画无需经过
JS 线程往返，因此响应更即时、更流畅。这是因为在 Pressable 中，回调首先经过 JS 线程，再触发共享值更新，造成了不可避免的延迟。而 GestureDetector 直接在 UI 线程处理手势，动画零延迟。

**错误示例（Pressable 使用 JS 线程回调，按压反馈存在延迟）：**

```tsx
import { Pressable } from 'react-native'
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
} from 'react-native-reanimated'

function AnimatedButton({ onPress }: { onPress: () => void }) {
  const scale = useSharedValue(1)

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }))

  return (
    <Pressable
      onPress={onPress}
      onPressIn={() => (scale.value = withTiming(0.95))}
      onPressOut={() => (scale.value = withTiming(1))}
    >
      <Animated.View style={animatedStyle}>
        <Text>Press me</Text>
      </Animated.View>
    </Pressable>
  )
}
```

**正确示例（GestureDetector 使用 UI 线程 worklet，按压反馈即时响应）：**

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler'
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  interpolate,
  runOnJS,
} from 'react-native-reanimated'

function AnimatedButton({ onPress }: { onPress: () => void }) {
  // Store the press STATE (0 = not pressed, 1 = pressed)
  const pressed = useSharedValue(0)

  const tap = Gesture.Tap()
    .onBegin(() => {
      pressed.set(withTiming(1))
    })
    .onFinalize(() => {
      pressed.set(withTiming(0))
    })
    .onEnd(() => {
      runOnJS(onPress)()
    })

  // Derive visual values from the state
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: interpolate(withTiming(pressed.get()), [0, 1], [1, 0.95]) },
    ],
  }))

  return (
    <GestureDetector gesture={tap}>
      <Animated.View style={animatedStyle}>
        <Text>Press me</Text>
      </Animated.View>
    </GestureDetector>
  )
}
```

存储按压**状态**（0 或 1），然后通过 `interpolate` 派生缩放值。
这样使共享值作为唯一事实来源，状态与视觉表现分离。使用 `runOnJS` 从 worklet 中调用 JS 函数。使用 `.set()` 和 `.get()` 方法以兼容 React Compiler。这种模式将状态存储与视觉派生解耦，使代码更易于理解和维护。

参考:
[Gesture Handler Tap Gesture](https://docs.swmansion.com/react-native-gesture-handler/docs/gestures/tap-gesture)
