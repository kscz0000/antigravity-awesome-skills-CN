---
title: 用循环代替排序求最值
impact: LOW
impactDescription: O(n) 替代 O(n log n)
tags: javascript, arrays, performance, sorting, algorithms
---

## 用循环代替排序求最值

查找最小或最大元素只需遍历数组一次。排序是浪费且更慢的。

**错误（O(n log n) - 排序查找最新项）：**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

仅为查找最大值就排序整个数组。

**错误（O(n log n) - 排序查找最旧和最新项）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

只需要最小/最大值时仍然不必要地排序。

**正确（O(n) - 单次循环）：**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

单次遍历数组，无复制，无排序。

**替代方案（小数组使用 Math.min/Math.max）：**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

这对小数组有效，但由于展开运算符的限制，对超大数组可能更慢。为保证可靠性，请使用循环方式。
