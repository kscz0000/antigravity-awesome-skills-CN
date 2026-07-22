---
title: 数组比较前先做长度检查
impact: MEDIUM-HIGH
impactDescription: 长度不同时避免昂贵操作
tags: javascript, arrays, performance, optimization, comparison
---

## 数组比较前先做长度检查

当使用昂贵操作（排序、深度相等、序列化）比较数组时，应先检查长度。如果长度不同，数组不可能相等。

在实际应用中，当比较运行在热路径（事件处理器、渲染循环）中时，这种优化尤其有价值。

**错误（总是运行昂贵的比较）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

即使 `current.length` 为 5 而 `original.length` 为 100，两次 O(n log n) 的排序仍会执行。此外还有数组拼接和字符串比较的开销。

**正确（先做 O(1) 长度检查）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true
  }
  // Only sort/join when lengths match
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

这种新方法更高效，因为：
- 长度不同时避免了排序和拼接数组的开销
- 避免了为拼接后的字符串分配内存（对大数组尤其重要）
- 避免了修改原数组
- 发现差异时立即提前返回
