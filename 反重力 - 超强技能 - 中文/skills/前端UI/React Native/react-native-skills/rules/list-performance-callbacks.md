---
title: Hoist callbacks to the root of lists
impact: MEDIUM
impactDescription: 减少重渲染，加速列表
tags: tag1, tag2
---

## 列表性能：回调提升

**影响: HIGH（减少重渲染，加速列表）**

向列表项传递回调函数时，在列表根层级创建回调的单个实例。列表项随后通过唯一标识符调用它。

**错误示例（每次渲染创建新回调）：**

```typescript
return (
  <LegendList
    renderItem={({ item }) => {
      // bad: creates a new callback on each render
      const onPress = () => handlePress(item.id)
      return <Item key={item.id} item={item} onPress={onPress} />
    }}
  />
)
```

**正确示例（单个函数实例传递给每个列表项）：**

```typescript
const onPress = useCallback(() => handlePress(item.id), [handlePress, item.id])

return (
  <LegendList
    renderItem={({ item }) => (
      <Item key={item.id} item={item} onPress={onPress} />
    )}
  />
)
```

参考: [文档或资源链接](https://example.com)
