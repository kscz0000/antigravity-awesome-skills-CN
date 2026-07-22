---
title: 使用 SWR 实现自动去重
impact: MEDIUM-HIGH
impactDescription: 自动去重
tags: client, swr, deduplication, data-fetching
---

## 使用 SWR 实现自动去重

SWR 可在组件实例之间实现请求去重、缓存和重新验证。

**错误做法（无去重，每个实例各自请求）：**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**正确做法（多个实例共享一个请求）：**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**对于不可变数据：**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**对于变更操作：**

```tsx
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

参考：[https://swr.vercel.app](https://swr.vercel.app)
