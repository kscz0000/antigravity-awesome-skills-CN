---
title: Use a List Virtualizer for Any List
impact: HIGH
impactDescription: 减少内存，更快挂载
tags: lists, performance, virtualization, scrollview
---

## 任何列表都使用列表虚拟化器

使用 LegendList 或 FlashList 等列表虚拟化器，而非 ScrollView 配合映射子元素——即使是短列表也应如此。虚拟化器仅渲染可见项，减少内存使用和挂载时间。ScrollView 会预先渲染所有子元素，开销增长很快。

**错误示例（ScrollView 一次性渲染所有项）：**

```tsx
function Feed({ items }: { items: Item[] }) {
  return (
    <ScrollView>
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </ScrollView>
  )
}
// 50 items = 50 components mounted, even if only 10 visible
```

**正确示例（虚拟化器仅渲染可见项）：**

```tsx
import { LegendList } from '@legendapp/list'

function Feed({ items }: { items: Item[] }) {
  return (
    <LegendList
      data={items}
      // if you aren't using React Compiler, wrap these with useCallback
      renderItem={({ item }) => <ItemCard item={item} />}
      keyExtractor={(item) => item.id}
      estimatedItemSize={80}
    />
  )
}
// Only ~10-15 visible items mounted at a time
```

**替代方案（FlashList）：**

```tsx
import { FlashList } from '@shopify/flash-list'

function Feed({ items }: { items: Item[] }) {
  return (
    <FlashList
      data={items}
      // if you aren't using React Compiler, wrap these with useCallback
      renderItem={({ item }) => <ItemCard item={item} />}
      keyExtractor={(item) => item.id}
    />
  )
}
```

优势适用于任何有可滚动内容的屏幕——个人资料、设置、信息流、搜索结果。默认使用虚拟化。
