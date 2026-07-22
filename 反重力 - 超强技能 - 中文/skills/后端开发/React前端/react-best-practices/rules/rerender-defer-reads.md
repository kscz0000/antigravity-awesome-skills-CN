---
title: 延迟状态读取到使用点
impact: MEDIUM
impactDescription: 避免不必要的订阅
tags: rerender, searchParams, localStorage, optimization
---

## 延迟状态读取到使用点

如果你只在回调中读取动态状态（searchParams、localStorage），不要订阅它们。

**错误写法（订阅所有 searchParams 变化）：**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()

  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```

**正确写法（按需读取，无订阅）：**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>Share</button>
}
```