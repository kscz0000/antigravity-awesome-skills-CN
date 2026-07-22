---
title: 缓存循环中的属性访问
impact: LOW-MEDIUM
impactDescription: 减少查找次数
tags: javascript, loops, optimization, caching
---

## 缓存循环中的属性访问

在热路径中缓存对象属性查找。

**错误做法（3 次查找 × N 次迭代）：**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**正确做法（总共 1 次查找）：**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```
