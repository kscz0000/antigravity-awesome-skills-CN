---
title: 使用 Promise.all() 处理独立操作
impact: CRITICAL
impactDescription: 2-10 倍性能提升
tags: async, parallelization, promises, waterfalls
---

## 使用 Promise.all() 处理独立操作

当 async 操作之间没有相互依赖时，使用 `Promise.all()` 并发执行它们。

**错误写法（顺序执行，3 次往返）：**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**正确写法（并行执行，1 次往返）：**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```
