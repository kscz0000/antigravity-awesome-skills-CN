---
title: 依赖当前值的状态应使用调度更新器
impact: MEDIUM
impactDescription: 避免闭包过期，防止不必要的重渲染
tags: state, hooks, useState, callbacks
---

## 依赖当前值的状态应使用调度更新器

当新状态依赖当前状态时，使用调度更新器（`setState(prev => ...)`）而非在回调中直接读取状态变量。这可避免闭包过期，确保与最新值进行比较。

**错误（直接读取状态）：**

```tsx
const [size, setSize] = useState<Size | undefined>(undefined)

const onLayout = (e: LayoutChangeEvent) => {
  const { width, height } = e.nativeEvent.layout
  // size may be stale in this closure
  if (size?.width !== width || size?.height !== height) {
    setSize({ width, height })
  }
}
```

**正确（调度更新器）：**

```tsx
const [size, setSize] = useState<Size | undefined>(undefined)

const onLayout = (e: LayoutChangeEvent) => {
  const { width, height } = e.nativeEvent.layout
  setSize((prev) => {
    if (prev?.width === width && prev?.height === height) return prev
    return { width, height }
  })
}
```

从更新器返回前一个值可跳过重渲染。

对于原始类型状态，不需要在触发重渲染前比较值。

**错误（原始类型状态的不必要比较）：**

```tsx
const [size, setSize] = useState<Size | undefined>(undefined)

const onLayout = (e: LayoutChangeEvent) => {
  const { width, height } = e.nativeEvent.layout
  setSize((prev) => (prev === width ? prev : width))
}
```

**正确（直接设置原始类型状态）：**

```tsx
const [size, setSize] = useState<Size | undefined>(undefined)

const onLayout = (e: LayoutChangeEvent) => {
  const { width, height } = e.nativeEvent.layout
  setSize(width)
}
```

然而，如果新状态依赖当前状态，仍应使用调度更新器。

**错误（在回调中直接读取状态）：**

```tsx
const [count, setCount] = useState(0)

const onTap = () => {
  setCount(count + 1)
}
```

**正确（调度更新器）：**

```tsx
const [count, setCount] = useState(0)

const onTap = () => {
  setCount((prev) => prev + 1)
}
```
