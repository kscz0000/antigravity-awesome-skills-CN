---
title: 使用 toSorted() 替代 sort() 保持不可变性
impact: MEDIUM-HIGH
impactDescription: 防止 React state 中的修改 bug
tags: javascript, arrays, immutability, react, state, mutation
---

## 使用 toSorted() 替代 sort() 保持不可变性

`.sort()` 会就地修改数组，这可能导致 React state 和 props 的 bug。使用 `.toSorted()` 创建新的排序数组而不修改原数组。

**错误（修改原数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正确（创建新数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**为什么这在 React 中很重要：**

1. Props/state 的修改破坏了 React 的不可变性模型 - React 要求将 props 和 state 视为只读
2. 导致闭包过期 bug - 在闭包（回调、effect）中修改数组可能导致意外行为

**浏览器支持（旧浏览器的降级方案）：**

`.toSorted()` 在所有现代浏览器中可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。对于旧环境，使用展开运算符：

```typescript
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**其他不可变数组方法：**

- `.toSorted()` - 不可变排序
- `.toReversed()` - 不可变反转
- `.toSpliced()` - 不可变拼接
- `.with()` - 不可变元素替换
