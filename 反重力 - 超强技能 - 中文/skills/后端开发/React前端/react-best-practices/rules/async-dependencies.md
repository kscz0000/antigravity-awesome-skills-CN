---
title: 基于依赖的并行化
impact: CRITICAL
impactDescription: 2-10 倍性能提升
tags: async, parallelization, dependencies, better-all
---

## 基于依赖的并行化

对于具有部分依赖的操作，使用 `better-all` 来最大化并行度。它会在最早的可能时刻自动启动每个任务。

**错误写法（profile 不必要地等待 config）：**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**正确写法（config 和 profile 并行运行）：**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

参考：[https://github.com/shuding/better-all](https://github.com/shuding/better-all)
