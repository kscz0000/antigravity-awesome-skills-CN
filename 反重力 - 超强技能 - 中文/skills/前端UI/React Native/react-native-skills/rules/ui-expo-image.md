---
title: 使用 expo-image 加载优化图片
impact: HIGH
impactDescription: 内存高效、缓存、blurhash 占位图、渐进式加载
tags: images, performance, expo-image, ui
---

## 使用 expo-image 加载优化图片

使用 `expo-image` 替代 React Native 的 `Image`。它提供内存高效的缓存、blurhash 占位图、渐进式加载，以及在列表中更好的性能表现。React Native 内置的 `Image` 组件缺少缓存控制和占位图支持，在长列表中性能较差。

**错误（React Native Image）：**

React Native 内置的 Image 没有缓存策略和占位图支持：

```tsx
import { Image } from 'react-native'

function Avatar({ url }: { url: string }) {
  return <Image source={{ uri: url }} style={styles.avatar} />
}
```

**正确（expo-image）：**

`expo-image` 的 API 与 React Native Image 几乎相同，但增加了缓存和占位图功能：

```tsx
import { Image } from 'expo-image'

function Avatar({ url }: { url: string }) {
  return <Image source={{ uri: url }} style={styles.avatar} />
}
```

**带 blurhash 占位图：**

在图片加载期间显示模糊占位图，提升用户体验：

```tsx
<Image
  source={{ uri: url }}
  placeholder={{ blurhash: 'LGF5]+Yk^6#M@-5c,1J5@[or[Q6.' }}
  contentFit="cover"
  transition={200}
  style={styles.image}
/>
```

**带优先级和缓存：**

通过优先级和缓存策略控制图片加载行为：

```tsx
<Image
  source={{ uri: url }}
  priority="high"
  cachePolicy="memory-disk"
  style={styles.hero}
/>
```

**关键属性：**

以下是 `expo-image` 提供的关键属性说明：

- `placeholder` — 加载时的 Blurhash 或缩略图
- `contentFit` — `cover`、`contain`、`fill`、`scale-down`
- `transition` — 淡入时长（毫秒）
- `priority` — `low`、`normal`、`high`
- `cachePolicy` — `memory`、`disk`、`memory-disk`、`none`
- `recyclingKey` — 列表回收的唯一键

对于跨平台（web + native），使用 `solito/image` 的 `SolitoImage`，它底层使用 `expo-image`。

**迁移提示**：从 React Native Image 迁移到 expo-image 只需更换 import 语句，API 几乎完全兼容。额外功能（占位图、缓存策略等）通过新增属性启用。

参考：[expo-image](https://docs.expo.dev/versions/latest/sdk/image/)
