---
title: Use Item Types for Heterogeneous Lists
impact: HIGH
impactDescription: 高效回收，减少布局抖动
tags: list, performance, recycling, heterogeneous, LegendList
---

## 异构列表使用 Item Types

当列表包含不同布局的项（消息、图片、标题等）时，在每个项上使用 `type` 字段并向列表提供 `getItemType`。这会将项放入不同的回收池，消息组件不会被回收到图片组件的位置。

**错误示例（单一组件使用条件判断）：**

```tsx
type Item = { id: string; text?: string; imageUrl?: string; isHeader?: boolean }

function ListItem({ item }: { item: Item }) {
  if (item.isHeader) {
    return <HeaderItem title={item.text} />
  }
  if (item.imageUrl) {
    return <ImageItem url={item.imageUrl} />
  }
  return <MessageItem text={item.text} />
}

function Feed({ items }: { items: Item[] }) {
  return (
    <LegendList
      data={items}
      renderItem={({ item }) => <ListItem item={item} />}
      recycleItems
    />
  )
}
```

**正确示例（类型化项使用独立组件）：**

```tsx
type HeaderItem = { id: string; type: 'header'; title: string }
type MessageItem = { id: string; type: 'message'; text: string }
type ImageItem = { id: string; type: 'image'; url: string }
type FeedItem = HeaderItem | MessageItem | ImageItem

function Feed({ items }: { items: FeedItem[] }) {
  return (
    <LegendList
      data={items}
      keyExtractor={(item) => item.id}
      getItemType={(item) => item.type}
      renderItem={({ item }) => {
        switch (item.type) {
          case 'header':
            return <SectionHeader title={item.title} />
          case 'message':
            return <MessageRow text={item.text} />
          case 'image':
            return <ImageRow url={item.url} />
        }
      }}
      recycleItems
    />
  )
}
```

**为什么这很重要：**

- **回收效率**：相同类型的项共享回收池
- **无布局抖动**：标题不会被回收到图片单元格
- **类型安全**：TypeScript 可以在每个分支中缩窄项类型
- **更精确的尺寸估算**：结合 `itemType` 使用 `getEstimatedItemSize` 可按类型精确估算

```tsx
<LegendList
  data={items}
  keyExtractor={(item) => item.id}
  getItemType={(item) => item.type}
  getEstimatedItemSize={(index, item, itemType) => {
    switch (itemType) {
      case 'header':
        return 48
      case 'message':
        return 72
      case 'image':
        return 300
      default:
        return 72
    }
  }}
  renderItem={({ item }) => {
    /* ... */
  }}
  recycleItems
/>
```

参考:
[LegendList getItemType](https://legendapp.com/open-source/list/api/props/#getitemtype-v2)
