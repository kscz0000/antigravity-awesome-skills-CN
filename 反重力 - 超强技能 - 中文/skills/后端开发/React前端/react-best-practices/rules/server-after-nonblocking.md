---
title: 使用 after() 处理非阻塞操作
impact: MEDIUM
impactDescription: 更快的响应时间
tags: server, async, logging, analytics, side-effects
---

## 使用 after() 处理非阻塞操作

使用 Next.js 的 `after()` 来调度应在响应发送后执行的工作。这可以防止日志记录、分析和其他副作用阻塞响应。

**错误写法（阻塞响应）：**

```tsx
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // 执行变更
  await updateDatabase(request)
  
  // 日志记录阻塞了响应
  const userAgent = request.headers.get('user-agent') || 'unknown'
  await logUserAction({ userAgent })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**正确写法（非阻塞）：**

```tsx
import { after } from 'next/server'
import { headers, cookies } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // 执行变更
  await updateDatabase(request)
  
  // 响应发送后再记录日志
  after(async () => {
    const userAgent = (await headers()).get('user-agent') || 'unknown'
    const sessionCookie = (await cookies()).get('session-id')?.value || 'anonymous'
    
    logUserAction({ sessionCookie, userAgent })
  })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

响应会立即发送，而日志记录在后台执行。

**常见用例：**

- 分析追踪
- 审计日志
- 发送通知
- 缓存失效
- 清理任务

**重要说明：**

- `after()` 即使在响应失败或重定向时也会运行
- 可在 Server Actions、Route Handlers 和 Server Components 中使用

参考：[https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)
