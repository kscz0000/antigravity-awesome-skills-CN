---
title: 最小化状态变量并派生值
impact: MEDIUM
impactDescription: 减少重渲染，避免状态漂移
tags: state, derived-state, hooks, optimization
---

## 最小化状态变量并派生值

使用尽可能少的状态变量。如果一个值可以从已有的状态或 props 计算得出，就在渲染时派生而非存储在状态中。冗余状态会导致不必要的重渲染，且可能失去同步。

**错误（冗余状态）：**

```tsx
function Cart({ items }: { items: Item[] }) {
  const [total, setTotal] = useState(0)
  const [itemCount, setItemCount] = useState(0)

  useEffect(() => {
    setTotal(items.reduce((sum, item) => sum + item.price, 0))
    setItemCount(items.length)
  }, [items])

  return (
    <View>
      <Text>{itemCount} items</Text>
      <Text>Total: ${total}</Text>
    </View>
  )
}
```

**正确（派生值）：**

```tsx
function Cart({ items }: { items: Item[] }) {
  const total = items.reduce((sum, item) => sum + item.price, 0)
  const itemCount = items.length

  return (
    <View>
      <Text>{itemCount} items</Text>
      <Text>Total: ${total}</Text>
    </View>
  )
}
```

**另一个示例：**

```tsx
// Incorrect: storing both firstName, lastName, AND fullName
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const [fullName, setFullName] = useState('')

// Correct: derive fullName
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const fullName = `${firstName} ${lastName}`
```

状态应是最小的真实来源，其余一切皆应派生。

参考：[选择状态结构](https://react.dev/learn/choosing-the-state-structure)
