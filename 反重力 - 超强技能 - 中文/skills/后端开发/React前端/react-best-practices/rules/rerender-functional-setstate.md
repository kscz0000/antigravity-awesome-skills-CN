---
title: 使用函数式 setState 更新
impact: MEDIUM
impactDescription: 防止过时闭包和不必要的回调重建
tags: react, hooks, useState, useCallback, callbacks, closures
---

## 使用函数式 setState 更新

当基于当前状态值更新状态时，使用 setState 的函数式更新形式，而非直接引用状态变量。这可以防止过时闭包、消除不必要的依赖，并创建稳定的回调引用。

**错误写法（需要状态作为依赖）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 回调必须依赖 items，每次 items 变化都会重建
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ items 依赖导致重建
  
  // 如果忘记依赖会有过时闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ 缺少 items 依赖 - 会使用过时的 items！
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

第一个回调每次 `items` 变化都会重建，可能导致子组件不必要地重渲染。第二个回调有过时闭包 bug——它总是引用初始的 `items` 值。

**正确写法（稳定的回调，无过时闭包）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 稳定的回调，永不重建
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ 无需依赖
  
  // 总是使用最新状态，无过时闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ 安全且稳定
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**优势：**

1. **稳定的回调引用** - 状态变化时无需重建回调
2. **无过时闭包** - 始终操作最新状态值
3. **更少的依赖** - 简化依赖数组并减少内存泄漏
4. **防止 bug** - 消除最常见的 React 闭包 bug 来源

**何时使用函数式更新：**

- 任何依赖当前状态值的 setState
- 在 useCallback/useMemo 中需要状态时
- 引用状态的事件处理器
- 更新状态的异步操作

**何时直接更新没问题：**

- 将状态设为静态值：`setCount(0)`
- 仅从 props/参数设置状态：`setName(newName)`
- 状态不依赖先前值

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，编译器可以自动优化某些情况，但仍建议使用函数式更新以确保正确性并防止过时闭包 bug。