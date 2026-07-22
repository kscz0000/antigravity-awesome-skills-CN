---
title: 为重复查找构建索引 Map
impact: LOW-MEDIUM
impactDescription: 从 100 万次操作降到 2000 次操作
tags: javascript, map, indexing, optimization, performance
---

## 为重复查找构建索引 Map

对同一键进行多次 `.find()` 调用时，应使用 Map。

**错误（每次查找 O(n)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**正确（每次查找 O(1)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

构建一次 map（O(n)），之后所有查找均为 O(1)。
对于 1000 个订单 × 1000 个用户：100 万次操作 → 2000 次操作。
