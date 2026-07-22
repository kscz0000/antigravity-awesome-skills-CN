---
title: 使用 React.cache() 进行单请求去重
impact: MEDIUM
impactDescription: 请求内去重
tags: server, cache, react-cache, deduplication
---

## 使用 React.cache() 进行单请求去重

使用 `React.cache()` 进行服务端请求去重。认证和数据库查询受益最大。

**用法：**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

在单个请求内，对 `getCurrentUser()` 的多次调用只会执行一次查询。
