---
title: Keep List Items Lightweight
impact: HIGH
impactDescription: 减少滚动时可见项的渲染时间
tags: lists, performance, virtualization, hooks
---

## 保持列表项轻量

列表项渲染应尽可能廉价。尽量减少 hooks，避免查询，限制 React Context 访问。虚拟化列表在滚动时渲染大量项——昂贵的项会导致卡顿。

**错误示例（重型列表项）：**

```tsx
function ProductRow({ id }: { id: string }) {
  // Bad: query inside list item
  const { data: product } = useQuery(['product', id], () => fetchProduct(id))
  // Bad: multiple context accesses
  const theme = useContext(ThemeContext)
  const user = useContext(UserContext)
  const cart = useContext(CartContext)
  // Bad: expensive computation
  const recommendations = useMemo(
    () => computeRecommendations(product),
    [product]
  )

  return <View>{/* ... */}</View>
}
```

**正确示例（轻量列表项）：**

```tsx
function ProductRow({ name, price, imageUrl }: Props) {
  // Good: receives only primitives, minimal hooks
  return (
    <View>
      <Image source={{ uri: imageUrl }} />
      <Text>{name}</Text>
      <Text>{price}</Text>
    </View>
  )
}
```

**将数据获取移至父级：**

```tsx
// Parent fetches all data once
function ProductList() {
  const { data: products } = useQuery(['products'], fetchProducts)

  return (
    <LegendList
      data={products}
      renderItem={({ item }) => (
        <ProductRow name={item.name} price={item.price} imageUrl={item.image} />
      )}
    />
  )
}
```

**共享值使用 Zustand 选择器而非 Context：**

```tsx
// Incorrect: Context causes re-render when any cart value changes
function ProductRow({ id, name }: Props) {
  const { items } = useContext(CartContext)
  const inCart = items.includes(id)
  // ...
}

// Correct: Zustand selector only re-renders when this specific value changes
function ProductRow({ id, name }: Props) {
  // use Set.has (created once at the root) instead of Array.includes()
  const inCart = useCartStore((s) => s.items.has(id))
  // ...
}
```

**列表项指南：**

- 不做查询或数据获取
- 不做昂贵计算（移到父级或在父级记忆化）
- 优先使用 Zustand 选择器而非 React Context
- 尽量减少 useState/useEffect hooks
- 传递预计算的值作为 props

目标：列表项应该是简单的渲染函数，接收 props 返回 JSX。
