---
title: 缩窄 Effect 依赖
impact: LOW
impactDescription: 最小化 effect 重运行
tags: rerender, useEffect, dependencies, optimization
---

## 缩窄 Effect 依赖

指定原始类型依赖而非对象，以最小化 effect 重运行。

**错误写法（任何 user 字段变化都会重运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确写法（仅 id 变化时重运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外计算：**

```tsx
// 错误写法：width=767、766、765... 时都会运行
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// 正确写法：仅在布尔值转换时运行
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```