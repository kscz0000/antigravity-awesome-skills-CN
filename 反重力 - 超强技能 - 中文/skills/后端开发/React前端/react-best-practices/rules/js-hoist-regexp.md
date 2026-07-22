---
title: 提升 RegExp 创建位置
impact: LOW-MEDIUM
impactDescription: 避免重复创建
tags: javascript, regexp, optimization, memoization
---

## 提升 RegExp 创建位置

不要在渲染函数内部创建 RegExp。将其提升到模块作用域，或使用 `useMemo()` 进行记忆化。

**错误（每次渲染都创建新的 RegExp）：**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**正确（记忆化或提升）：**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**警告（全局正则具有可变状态）：**

全局正则（`/g`）具有可变的 `lastIndex` 状态：

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```
