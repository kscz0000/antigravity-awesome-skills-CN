---
title: 将事件处理器存储在 Ref 中
impact: LOW
impactDescription: 稳定的订阅
tags: advanced, hooks, refs, event-handlers, optimization
---

## 将事件处理器存储在 Ref 中

当回调用于不应因回调变更而重新订阅的 effect 中时，将其存储在 ref 中。

**错误写法（每次渲染都会重新订阅）：**

```tsx
function useWindowEvent(event: string, handler: () => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**正确写法（稳定的订阅）：**

```tsx
function useWindowEvent(event: string, handler: () => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = () => handlerRef.current()
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**替代方案：如果使用最新版本的 React，可以使用 `useEffectEvent`：**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: () => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` 为相同模式提供了更简洁的 API：它创建一个稳定的函数引用，始终调用最新版本的处理器。
