---
title: useLatest 用于稳定的回调 Ref
impact: LOW
impactDescription: 防止 effect 重新运行
tags: advanced, hooks, useLatest, refs, optimization
---

## useLatest 用于稳定的回调 Ref

在回调中访问最新值，而无需将其添加到依赖数组中。防止 effect 重新运行，同时避免闭包过期问题。

**实现：**

```typescript
function useLatest<T>(value: T) {
  const ref = useRef(value)
  useEffect(() => {
    ref.current = value
  }, [value])
  return ref
}
```

**错误写法（每次回调变更时 effect 都会重新运行）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**正确写法（稳定的 effect，最新的回调）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchRef = useLatest(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchRef.current(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```
