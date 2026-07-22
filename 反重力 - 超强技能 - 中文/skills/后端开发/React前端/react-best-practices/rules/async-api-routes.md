---
title: 防止 API 路由中的瀑布式链式调用
impact: CRITICAL
impactDescription: 2-10 倍性能提升
tags: api-routes, server-actions, waterfalls, parallelization
---

## 防止 API 路由中的瀑布式链式调用

在 API 路由和 Server Actions 中，立即启动独立操作，即使尚未 await 它们。

**错误写法（config 等待 auth，data 等待两者）：**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**正确写法（auth 和 config 同时启动）：**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

对于具有更复杂依赖链的操作，使用 `better-all` 自动最大化并行度（参见基于依赖的并行化）。
