---
title: 状态必须代表基本事实
impact: HIGH
impactDescription: 更清晰的逻辑，更容易调试，单一数据源
tags: state, derived-state, reanimated, hooks
---

## 状态必须代表基本事实

状态变量——无论是 React `useState` 还是 Reanimated 共享值——都应代表某事物的实际状态（如 `pressed`、`progress`、`isOpen`），而非派生的视觉值（如 `scale`、`opacity`、`translateY`）。应通过计算或插值从状态派生视觉值。

**错误（存储视觉输出）：**

```tsx
const scale = useSharedValue(1)

const tap = Gesture.Tap()
  .onBegin(() => {
    scale.set(withTiming(0.95))
  })
  .onFinalize(() => {
    scale.set(withTiming(1))
  })

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ scale: scale.get() }],
}))
```

**正确（存储状态，派生视觉值）：**

```tsx
const pressed = useSharedValue(0) // 0 = not pressed, 1 = pressed

const tap = Gesture.Tap()
  .onBegin(() => {
    pressed.set(withTiming(1))
  })
  .onFinalize(() => {
    pressed.set(withTiming(0))
  })

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ scale: interpolate(pressed.get(), [0, 1], [1, 0.95]) }],
}))
```

**为什么这很重要：**

状态变量应代表真正的"状态"，而不一定是期望的最终结果。

1. **单一数据源** — 状态（`pressed`）描述正在发生的事情；视觉效果是派生的
2. **易于扩展** — 添加透明度、旋转或其他效果只需从同一状态增加更多插值
3. **调试** — 检查 `pressed = 1` 比检查 `scale = 0.95` 更清晰
4. **可复用逻辑** — 同一个 `pressed` 值可以驱动多个视觉属性

**React 状态同样适用此原则：**

```tsx
// Incorrect: storing derived values
const [isExpanded, setIsExpanded] = useState(false)
const [height, setHeight] = useState(0)

useEffect(() => {
  setHeight(isExpanded ? 200 : 0)
}, [isExpanded])

// Correct: derive from state
const [isExpanded, setIsExpanded] = useState(false)
const height = isExpanded ? 200 : 0
```

状态是最小的真实来源，其余一切皆应派生。
