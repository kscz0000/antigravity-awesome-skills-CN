---
title: 禁止在 useState 中跟踪滚动位置
impact: HIGH
impactDescription: 防止滚动时的渲染抖动
tags: scroll, performance, reanimated, useRef
---

## 禁止在 useState 中跟踪滚动位置

绝不要将滚动位置存储在 `useState` 中。滚动事件触发非常频繁——状态更新会导致渲染抖动和掉帧。动画应使用 Reanimated 共享值，非响应式追踪应使用 ref。

**错误（useState 导致卡顿）：**

```tsx
import { useState } from 'react'
import {
  ScrollView,
  NativeSyntheticEvent,
  NativeScrollEvent,
} from 'react-native'

function Feed() {
  const [scrollY, setScrollY] = useState(0)

  const onScroll = (e: NativeSyntheticEvent<NativeScrollEvent>) => {
    setScrollY(e.nativeEvent.contentOffset.y) // re-renders on every frame
  }

  return <ScrollView onScroll={onScroll} scrollEventThrottle={16} />
}
```

**正确（Reanimated 用于动画）：**

```tsx
import Animated, {
  useSharedValue,
  useAnimatedScrollHandler,
} from 'react-native-reanimated'

function Feed() {
  const scrollY = useSharedValue(0)

  const onScroll = useAnimatedScrollHandler({
    onScroll: (e) => {
      scrollY.value = e.contentOffset.y // runs on UI thread, no re-render
    },
  })

  return (
    <Animated.ScrollView
      onScroll={onScroll}
      // higher number has better performance, but it fires less often.
      // unset this if you need higher precision over performance.
      scrollEventThrottle={16}
    />
  )
}
```

**正确（ref 用于非响应式追踪）：**

```tsx
import { useRef } from 'react'
import {
  ScrollView,
  NativeSyntheticEvent,
  NativeScrollEvent,
} from 'react-native'

function Feed() {
  const scrollY = useRef(0)

  const onScroll = (e: NativeSyntheticEvent<NativeScrollEvent>) => {
    scrollY.current = e.nativeEvent.contentOffset.y // no re-render
  }

  return <ScrollView onScroll={onScroll} scrollEventThrottle={16} />
}
```
