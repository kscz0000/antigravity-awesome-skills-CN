---
title: 去重全局事件监听器
impact: LOW
impactDescription: N 个组件共用单个监听器
tags: client, swr, event-listeners, subscription
---

## 去重全局事件监听器

使用 `useSWRSubscription()` 在多个组件实例之间共享全局事件监听器。

**错误做法（N 个实例 = N 个监听器）：**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

多次使用 `useKeyboardShortcut` hook 时，每个实例都会注册一个新的监听器。

**正确做法（N 个实例 = 1 个监听器）：**

```tsx
import useSWRSubscription from 'swr/subscription'

// 模块级 Map，用于按按键追踪回调
const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  // 将此回调注册到 Map 中
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set())
    }
    keyCallbacks.get(key)!.add(callback)

    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) {
          keyCallbacks.delete(key)
        }
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}

function Profile() {
  // 多个快捷键将共享同一个监听器
  useKeyboardShortcut('p', () => { /* ... */ }) 
  useKeyboardShortcut('k', () => { /* ... */ })
  // ...
}
```
