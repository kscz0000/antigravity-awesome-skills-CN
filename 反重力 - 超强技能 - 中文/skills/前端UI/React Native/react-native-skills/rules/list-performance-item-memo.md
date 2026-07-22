---
title: Pass Primitives to List Items for Memoization
impact: HIGH
impactDescription: 使 memo() 比较更有效
tags: lists, performance, memo, primitives
---

## 传递原始值给列表项以实现记忆化

尽可能只传递原始值（字符串、数字、布尔值）作为列表项组件的 props。原始值使 `memo()` 中的浅比较正确工作，值未变化时跳过重渲染。

**错误示例（对象 prop 需要深比较）：**

```tsx
type User = { id: string; name: string; email: string; avatar: string }

const UserRow = memo(function UserRow({ user }: { user: User }) {
  // memo() compares user by reference, not value
  // If parent creates new user object, this re-renders even if data is same
  return <Text>{user.name}</Text>
})

renderItem={({ item }) => <UserRow user={item} />}
```

这仍然可以优化，但更难正确记忆化。

**正确示例（原始值 props 支持浅比较）：**

```tsx
const UserRow = memo(function UserRow({
  id,
  name,
  email,
}: {
  id: string
  name: string
  email: string
}) {
  // memo() compares each primitive directly
  // Re-renders only if id, name, or email actually changed
  return <Text>{name}</Text>
})

renderItem={({ item }) => (
  <UserRow id={item.id} name={item.name} email={item.email} />
)}
```

**只传递需要的内容：**

```tsx
// Incorrect: passing entire item when you only need name
<UserRow user={item} />

// Correct: pass only the fields the component uses
<UserRow name={item.name} avatarUrl={item.avatar} />
```

**回调函数应提升或使用 item ID：**

```tsx
// Incorrect: inline function creates new reference
<UserRow name={item.name} onPress={() => handlePress(item.id)} />

// Correct: pass ID, handle in child
<UserRow id={item.id} name={item.name} />

const UserRow = memo(function UserRow({ id, name }: Props) {
  const handlePress = useCallback(() => {
    // use id here
  }, [id])
  return <Pressable onPress={handlePress}><Text>{name}</Text></Pressable>
})
```

原始值 props 使记忆化可预测且有效。

**注意：** 如果启用了 React Compiler，无需使用 `memo()` 或 `useCallback()`，但对象引用规则仍然适用。
