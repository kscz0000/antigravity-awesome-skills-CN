---
title: Use Compressed Images in Lists
impact: HIGH
impactDescription: 更快的加载速度，更少的内存占用
tags: lists, images, performance, optimization
---

## 在列表中使用压缩图片

列表中始终加载压缩且尺寸合适的图片。全分辨率图片消耗过多内存并导致滚动卡顿。从服务器请求缩略图或使用带调整大小参数的图片 CDN。

**错误示例（全分辨率图片）：**

```tsx
function ProductItem({ product }: { product: Product }) {
  return (
    <View>
      {/* 4000x3000 image loaded for a 100x100 thumbnail */}
      <Image
        source={{ uri: product.imageUrl }}
        style={{ width: 100, height: 100 }}
      />
      <Text>{product.name}</Text>
    </View>
  )
}
```

**正确示例（请求合适尺寸的图片）：**

```tsx
function ProductItem({ product }: { product: Product }) {
  // Request a 200x200 image (2x for retina)
  const thumbnailUrl = `${product.imageUrl}?w=200&h=200&fit=cover`

  return (
    <View>
      <Image
        source={{ uri: thumbnailUrl }}
        style={{ width: 100, height: 100 }}
        contentFit='cover'
      />
      <Text>{product.name}</Text>
    </View>
  )
}
```

使用内置缓存和占位符支持的优化图片组件，如 `expo-image` 或 `SolitoImage`（底层使用 `expo-image`）。
为视网膜屏幕请求 2 倍显示尺寸的图片。
