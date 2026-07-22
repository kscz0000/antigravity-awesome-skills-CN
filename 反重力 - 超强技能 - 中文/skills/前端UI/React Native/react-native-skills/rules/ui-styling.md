---
title: 现代 React Native 样式模式
impact: MEDIUM
impactDescription: 一致的设计、更平滑的圆角、更简洁的布局
tags: styling, css, layout, shadows, gradients
---

## 现代 React Native 样式模式

遵循以下样式模式，编写更简洁、更一致的 React Native 代码。

**使用 `borderRadius` 时始终搭配 `borderCurve: 'continuous'`：**

```tsx
// Incorrect
{ borderRadius: 12 }

// Correct – smoother iOS-style corners
{ borderRadius: 12, borderCurve: 'continuous' }
```

**使用 `gap` 替代 margin 实现元素间距：**

```tsx
// Incorrect – margin on children
<View>
  <Text style={{ marginBottom: 8 }}>Title</Text>
  <Text style={{ marginBottom: 8 }}>Subtitle</Text>
</View>

// Correct – gap on parent
<View style={{ gap: 8 }}>
  <Text>Title</Text>
  <Text>Subtitle</Text>
</View>
```

**`padding` 用于内部空间，`gap` 用于元素间距：**

```tsx
<View style={{ padding: 16, gap: 12 }}>
  <Text>First</Text>
  <Text>Second</Text>
</View>
```

**使用 `experimental_backgroundImage` 实现线性渐变：**

```tsx
// Incorrect – third-party gradient library
<LinearGradient colors={['#000', '#fff']} />

// Correct – native CSS gradient syntax
<View
  style={{
    experimental_backgroundImage: 'linear-gradient(to bottom, #000, #fff)',
  }}
/>
```

**使用 CSS `boxShadow` 字符串语法实现阴影：**

```tsx
// Incorrect – legacy shadow objects or elevation
{ shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1 }
{ elevation: 4 }

// Correct – CSS box-shadow syntax
{ boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)' }
```

**避免多种字号——使用字重和颜色体现层次：**

```tsx
// Incorrect – varying font sizes for hierarchy
<Text style={{ fontSize: 18 }}>Title</Text>
<Text style={{ fontSize: 14 }}>Subtitle</Text>
<Text style={{ fontSize: 12 }}>Caption</Text>

// Correct – consistent size, vary weight and color
<Text style={{ fontWeight: '600' }}>Title</Text>
<Text style={{ color: '#666' }}>Subtitle</Text>
<Text style={{ color: '#999' }}>Caption</Text>
```

限制字号种类可建立视觉一致性。使用 `fontWeight`（粗体/半粗体）和灰度颜色体现层次。
