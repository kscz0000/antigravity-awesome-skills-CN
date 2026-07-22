---
title: Prefer useDerivedValue Over useAnimatedReaction
impact: MEDIUM
impactDescription: 更清晰的代码，自动依赖追踪
tags: animation, reanimated, derived-value
---

## 优先使用 useDerivedValue 而非 useAnimatedReaction

当需要从另一个共享值（shared value）派生新值时，应使用 `useDerivedValue` 而非
`useAnimatedReaction`。派生值是声明式的，会自动追踪依赖关系，并返回可直接使用的共享值引用。动画反应（animated reaction）设计用于产生副作用，而非用于值的派生计算。使用 `useDerivedValue` 的代码更简洁、可读性更好，且不需要手动管理依赖数组，是派生共享值的首选方案。

**错误示例（使用 useAnimatedReaction 进行值派生，代码冗余且意图不明确）：**

```tsx
import { useSharedValue, useAnimatedReaction } from 'react-native-reanimated'

function MyComponent() {
  const progress = useSharedValue(0)
  const opacity = useSharedValue(1)

  useAnimatedReaction(
    () => progress.value,
    (current) => {
      opacity.value = 1 - current
    }
  )

  // ...
}
```

**正确示例（使用 useDerivedValue，声明式且自动追踪依赖）：**

```tsx
import { useSharedValue, useDerivedValue } from 'react-native-reanimated'

function MyComponent() {
  const progress = useSharedValue(0)

  const opacity = useDerivedValue(() => 1 - progress.get())

  // ...
}
```

仅在不产生值的副作用场景使用 `useAnimatedReaction`（例如触发触觉反馈、日志记录、调用 `runOnJS`）。当你的逻辑目的是计算并返回一个新值时，`useDerivedValue` 是更合适的选择，它更简洁且不易出错。

参考:
[Reanimated useDerivedValue](https://docs.swmansion.com/react-native-reanimated/docs/core/useDerivedValue)
