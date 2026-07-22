---
title: 使用 Activity 组件实现显示/隐藏
impact: MEDIUM
impactDescription: 保留状态/DOM
tags: rendering, activity, visibility, state-preservation
---

## 使用 Activity 组件实现显示/隐藏

使用 React 的 `<Activity>` 为频繁切换可见性的昂贵组件保留状态/DOM。

**用法：**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

避免昂贵的重新渲染和状态丢失。
