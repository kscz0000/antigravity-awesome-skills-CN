---
title: 缓存 Storage API 调用
impact: LOW-MEDIUM
impactDescription: 减少昂贵的 I/O 操作
tags: javascript, localStorage, storage, caching, performance
---

## 缓存 Storage API 调用

`localStorage`、`sessionStorage` 和 `document.cookie` 是同步的且开销较大。将读取结果缓存在内存中。

**错误做法（每次调用都读取存储）：**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// 调用 10 次 = 10 次存储读取
```

**正确做法（Map 缓存）：**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // 保持缓存同步
}
```

使用 Map（而非 hook），这样它可以在任何地方使用：工具函数、事件处理器，而不仅限于 React 组件。

**Cookie 缓存：**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**重要（外部变更时失效）：**

如果存储可能被外部修改（另一个标签页、服务器端设置的 cookie），需要使缓存失效：

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```
