---
title: 使用过渡处理非紧急更新
impact: MEDIUM
impactDescription: 维持 UI 响应性
tags: rerender, transitions, startTransition, performance
---

## 使用过渡处理非紧急更新

将频繁、非紧急的状态更新标记为过渡，以维持 UI 响应性。

**错误写法（每次滚动都阻塞 UI）：**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**正确写法（非阻塞更新）：**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```