---
title: 动画化 SVG 包裹层而非 SVG 元素本身
impact: LOW
impactDescription: 启用硬件加速
tags: rendering, svg, css, animation, performance
---

## 动画化 SVG 包裹层而非 SVG 元素本身

许多浏览器不支持对 SVG 元素的 CSS3 动画进行硬件加速。将 SVG 包裹在 `<div>` 中，改为动画化包裹层。

**错误（直接动画化 SVG - 无硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**正确（动画化包裹 div - 硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

这适用于所有 CSS 变换和过渡（`transform`、`opacity`、`translate`、`scale`、`rotate`）。包裹 div 允许浏览器使用 GPU 加速以实现更流畅的动画。
