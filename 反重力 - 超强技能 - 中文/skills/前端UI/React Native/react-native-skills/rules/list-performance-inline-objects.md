---
title: Avoid Inline Objects in renderItem
impact: HIGH
impactDescription: 防止已记忆化的列表项不必要重渲染
tags: lists, performance, flatlist, virtualization, memo
---

## 避免 renderItem 中使用内联对象

不要在 `renderItem` 内创建新对象作为 props 传递。内联对象每次渲染都创建新引用，破坏记忆化。应直接从 `item` 传递原始值。

**错误示例（内联对象破坏记忆化）：**

```tsx
function UserList({ users }: { users: User[] }) {
  return (
    <LegendList
      data={users}
      renderItem={({ item }) => (
        <UserRow
          // Bad: new object on every render
          user={{ id: item.id, name: item.name, avatar: item.avatar }}
        />
      )}
    />
  )
}
```

**错误示例（内联样式对象）：**

```tsx
renderItem={({ item }) => (
  <UserRow
    name={item.name}
    // Bad: new style object on every render
    style={{ backgroundColor: item.isActive ? 'green' : 'gray' }}
  />
)}
```

**正确示例（直接传递 item 或原始值）：**

```tsx
function UserList({ users }: { users: User[] }) {
  return (
    <LegendList
      data={users}
      renderItem={({ item }) => (
        // Good: pass the item directly
        <UserRow user={item} />
      )}
    />
  )
}
```

**正确示例（传递原始值，在子组件内派生）：**

```tsx
renderItem={({ item }) => (
  <UserRow
    id={item.id}
    name={item.name}
    isActive={item.isActive}
  />
)}

const UserRow = memo(function UserRow({ id, name, isActive }: Props) {
  // Good: derive style inside memoized component
  const backgroundColor = isActive ? 'green' : 'gray'
  return <View style={[styles.row, { backgroundColor }]}>{/* ... */}</View>
})
```

**正确示例（将静态样式提升到模块作用域）：**

```tsx
const activeStyle = { backgroundColor: 'green' }
const inactiveStyle = { backgroundColor: 'gray' }

renderItem={({ item }) => (
  <UserRow
    name={item.name}
    // Good: stable references
    style={item.isActive ? activeStyle : inactiveStyle}
  />
)}
```

传递原始值或稳定引用可让 `memo()` 在实际值未变化时跳过重渲染。

**注意：** 如果启用了 React Compiler，它会自动处理记忆化，这些手动优化变得不那么关键。
