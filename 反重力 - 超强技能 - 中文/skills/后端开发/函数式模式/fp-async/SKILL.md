---
name: fp-async
description: 使用 TaskEither 的实用异步模式——用干净的管道替代 try/catch 地狱，包含真实 API 示例。触发词：TaskEither、fp-ts 异步、异步错误处理、Promise 包装、API 管道、try/catch 替代、异步组合、函数式异步、TypeScript 异步模式、错误恢复模式、并行异步、顺序异步、fp-ts TaskEither
risk: unknown
source: community
version: 1.0.0
author: kadu
tags:
  - fp-ts
  - typescript
  - async
  - error-handling
  - practical
  - promises
  - api
  - fetch
---

# fp-ts 实用异步模式

停止编写嵌套的 try/catch 块。停止丢失错误上下文。开始构建能正确处理错误的干净异步管道。

**TaskEither 就是一个跟踪成功或失败的异步操作。** 就这么简单。不需要花哨的术语。

## 何时使用

- 你需要在 TypeScript 中使用 `TaskEither` 进行异步错误处理。
- 任务涉及包装 Promise、组合 API 调用，或替换嵌套的 `try/catch` 流程。
- 你想要实用的 fp-ts 异步模式，而不是学术性的解释。

```typescript
// TaskEither<Error, User> 意思是：
// "一个异步操作，要么以 Error 失败，要么以 User 成功"
```

---

## 1. 安全地包装 Promise

### 问题：到处都是 Try/Catch

```typescript
// 之前：try/catch 地狱
async function getUserData(userId: string) {
  try {
    const response = await fetch(`/api/users/${userId}`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    const user = await response.json()

    try {
      const posts = await fetch(`/api/users/${userId}/posts`)
      if (!posts.ok) {
        throw new Error(`HTTP ${posts.status}`)
      }
      const postsData = await posts.json()
      return { user, posts: postsData }
    } catch (postsError) {
      // 现在怎么办？返回部分数据？重新抛出？记录日志？
      console.error('Failed to fetch posts:', postsError)
      return { user, posts: [] }
    }
  } catch (error) {
    // 丢失了所有关于什么失败的上下文
    console.error('Something failed:', error)
    throw error
  }
}
```

### 解决方案：包装一次，干净处理

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 一个包装函数 - 到处复用
const fetchJson = <T>(url: string): TE.TaskEither<Error, T> =>
  TE.tryCatch(
    async () => {
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      return response.json()
    },
    (error) => error instanceof Error ? error : new Error(String(error))
  )

// 之后：干净且可组合
const getUser = (userId: string) => fetchJson<User>(`/api/users/${userId}`)
const getPosts = (userId: string) => fetchJson<Post[]>(`/api/users/${userId}/posts`)
```

### tryCatch 详解

`TE.tryCatch` 接受两个参数：
1. 一个可能抛出异常的异步函数
2. 一个将抛出的值转换为你的错误类型的函数

```typescript
TE.tryCatch(
  () => somePromise,           // 异步工作
  (thrown) => toError(thrown)  // 将失败转换为你指定的错误类型
)
```

### 创建成功和失败值

```typescript
// 将值包装为成功
const success = TE.right<Error, number>(42)

// 将值包装为失败
const failure = TE.left<Error, number>(new Error('Nope'))

// 从可空值创建（null/undefined 变为错误）
const fromNullable = TE.fromNullable(new Error('Value was null'))
const result = fromNullable(maybeUser) // TaskEither<Error, User>

// 从条件创建
const mustBePositive = TE.fromPredicate(
  (n: number) => n > 0,
  (n) => new Error(`Expected positive, got ${n}`)
)
```

---

## 2. 链式异步操作

### 问题：回调地狱 / 嵌套的 Await

```typescript
// 之前：深度嵌套，难以追踪
async function processOrder(orderId: string) {
  try {
    const order = await fetchOrder(orderId)
    if (!order) throw new Error('Order not found')

    try {
      const user = await fetchUser(order.userId)
      if (!user) throw new Error('User not found')

      try {
        const inventory = await checkInventory(order.items)
        if (!inventory.available) throw new Error('Out of stock')

        try {
          const payment = await chargePayment(user, order.total)
          if (!payment.success) throw new Error('Payment failed')

          try {
            const shipment = await createShipment(order, user)
            return { order, shipment, payment }
          } catch (e) {
            // 退款？记录日志？现在的状态是什么？
            await refundPayment(payment.id)
            throw e
          }
        } catch (e) {
          throw e
        }
      } catch (e) {
        throw e
      }
    } catch (e) {
      throw e
    }
  } catch (e) {
    console.error('Order processing failed', e)
    throw e
  }
}
```

### 解决方案：使用 chain 构建干净的管道

```typescript
// 之后：扁平、可读的管道
const processOrder = (orderId: string) =>
  pipe(
    fetchOrder(orderId),
    TE.chain(order => fetchUser(order.userId)),
    TE.chain(user =>
      pipe(
        checkInventory(order.items),
        TE.chain(inventory => chargePayment(user, order.total))
      )
    ),
    TE.chain(payment => createShipment(order, user, payment))
  )
```

### chain vs map

当你的转换是同步的且不会失败时使用 `map`：

```typescript
pipe(
  fetchUser(userId),
  TE.map(user => user.name.toUpperCase())  // 只是转换值
)
```

当你的转换是异步的或可能失败时使用 `chain`（或 `flatMap`）：

```typescript
pipe(
  fetchUser(userId),
  TE.chain(user => fetchOrders(user.id))  // 返回另一个 TaskEither
)
```

### 使用 Do 表示法构建上下文

当你需要来自多个步骤的值时：

```typescript
// 之前：必须手动传递值
const processOrderManual = (orderId: string) =>
  pipe(
    fetchOrder(orderId),
    TE.chain(order =>
      pipe(
        fetchUser(order.userId),
        TE.chain(user =>
          pipe(
            chargePayment(user, order.total),
            TE.map(payment => ({ order, user, payment }))
          )
        )
      )
    )
  )

// 之后：Do 表示法让所有内容都可访问
const processOrder = (orderId: string) =>
  pipe(
    TE.Do,
    TE.bind('order', () => fetchOrder(orderId)),
    TE.bind('user', ({ order }) => fetchUser(order.userId)),
    TE.bind('payment', ({ user, order }) => chargePayment(user, order.total)),
    TE.bind('shipment', ({ order, user }) => createShipment(order, user)),
    TE.map(({ order, payment, shipment }) => ({
      orderId: order.id,
      paymentId: payment.id,
      trackingNumber: shipment.tracking
    }))
  )
```

---

## 3. 并行 vs 顺序执行

### 何时使用每种方式

**顺序**（一个接一个）：
- 当每个操作依赖于前一个结果时
- 当你需要遵守速率限制时
- 当顺序很重要时

**并行**（同时进行）：
- 当操作相互独立时
- 当你想要速度时
- 当按 ID 获取多个资源时

### 顺序链式调用

```typescript
// 操作相互依赖 - 必须顺序执行
const getUserWithOrg = (userId: string) =>
  pipe(
    fetchUser(userId),                              // 首先：获取用户
    TE.chain(user => fetchTeam(user.teamId)),      // 然后：获取他们的团队
    TE.chain(team => fetchOrganization(team.orgId)) // 最后：获取组织
  )
```

### 并行执行

```typescript
import { sequenceT } from 'fp-ts/Apply'

// 独立操作 - 并行运行
const getDashboardData = (userId: string) =>
  sequenceT(TE.ApplyPar)(
    fetchUser(userId),
    fetchNotifications(userId),
    fetchRecentActivity(userId)
  ) // 返回 TaskEither<Error, [User, Notification[], Activity[]]>

// 使用解构：
const getDashboard = (userId: string) =>
  pipe(
    sequenceT(TE.ApplyPar)(
      fetchUser(userId),
      fetchNotifications(userId),
      fetchRecentActivity(userId)
    ),
    TE.map(([user, notifications, activities]) => ({
      user,
      notifications,
      activities,
      unreadCount: notifications.filter(n => !n.read).length
    }))
  )
```

### 并行数组操作

```typescript
// 并行获取多个用户
const userIds = ['1', '2', '3', '4', '5']

// TE.traverseArray 并行运行所有获取操作
const fetchAllUsers = pipe(
  userIds,
  TE.traverseArray(fetchUser)
) // TaskEither<Error, readonly User[]>

// 注意：快速失败 - 如果任何请求失败，整个操作都会失败
// 第一个错误之后的所有错误都会丢失
```

### 带批量控制的并行

当你需要限制并发请求数时：

```typescript
const chunk = <T>(arr: T[], size: number): T[][] => {
  const chunks: T[][] = []
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size))
  }
  return chunks
}

// 以每批 5 个并发请求的方式处理
const fetchUsersWithLimit = (userIds: string[]) => {
  const batches = chunk(userIds, 5)

  return pipe(
    batches,
    // 顺序处理批次
    TE.traverseArray(batch =>
      // 但在每个批次内并行运行
      pipe(batch, TE.traverseArray(fetchUser))
    ),
    TE.map(results => results.flat())
  )
}
```

### 当并行看起来诱人时使用顺序

```typescript
// 错误：这看起来是并行的，但顺序对于数据库操作可能很重要
const createUserAndProfile = (userData: UserData) =>
  sequenceT(TE.ApplyPar)(
    createUser(userData),           // 创建带 ID 的用户
    createProfile(userData.profile) // 需要用户 ID - 竞态条件！
  )

// 正确：当存在依赖关系时使用顺序
const createUserAndProfile = (userData: UserData) =>
  pipe(
    createUser(userData),
    TE.chain(user =>
      pipe(
        createProfile(user.id, userData.profile),
        TE.map(profile => ({ user, profile }))
      )
    )
  )
```

---

## 4. 错误恢复模式

### 回退到替代方案

```typescript
// 尝试主 API，回退到缓存
const getUserWithFallback = (userId: string) =>
  pipe(
    fetchUserFromApi(userId),
    TE.orElse(() => fetchUserFromCache(userId))
  )

// 链式多重回退
const getConfigRobust = () =>
  pipe(
    fetchRemoteConfig(),
    TE.orElse(() => loadLocalConfig()),
    TE.orElse(() => TE.right(defaultConfig))
  )
```

### 条件恢复

```typescript
// 仅从特定错误中恢复
const fetchUserOrCreate = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.orElse(error =>
      error.message.includes('404') || error.message.includes('not found')
        ? createDefaultUser(userId)
        : TE.left(error)  // 重新抛出其他错误
    )
  )
```

### 类型化错误恢复

```typescript
type ApiError =
  | { _tag: 'NotFound'; id: string }
  | { _tag: 'NetworkError'; cause: Error }
  | { _tag: 'Unauthorized' }

const fetchUser = (id: string): TE.TaskEither<ApiError, User> =>
  TE.tryCatch(
    async () => {
      const res = await fetch(`/api/users/${id}`)
      if (res.status === 404) throw { _tag: 'NotFound', id }
      if (res.status === 401) throw { _tag: 'Unauthorized' }
      if (!res.ok) throw { _tag: 'NetworkError', cause: new Error(`HTTP ${res.status}`) }
      return res.json()
    },
    (e): ApiError =>
      typeof e === 'object' && e !== null && '_tag' in e
        ? e as ApiError
        : { _tag: 'NetworkError', cause: e instanceof Error ? e : new Error(String(e)) }
  )

// 以不同方式处理特定错误
const getUserOrGuest = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.orElse(error => {
      switch (error._tag) {
        case 'NotFound':
          return TE.right(createGuestUser())
        case 'Unauthorized':
          return TE.left(error) // 传播认证错误
        case 'NetworkError':
          return fetchUserFromCache(userId) // 网络问题时尝试缓存
      }
    })
  )
```

### 带指数退避的重试

```typescript
import * as T from 'fp-ts/Task'

const wait = (ms: number): T.Task<void> =>
  () => new Promise(resolve => setTimeout(resolve, ms))

const retry = <E, A>(
  operation: TE.TaskEither<E, A>,
  maxAttempts: number,
  baseDelayMs: number = 1000
): TE.TaskEither<E, A> => {
  const attempt = (remaining: number, delay: number): TE.TaskEither<E, A> =>
    pipe(
      operation,
      TE.orElse(error =>
        remaining <= 1
          ? TE.left(error)
          : pipe(
              TE.fromTask(wait(delay)),
              TE.chain(() => attempt(remaining - 1, delay * 2))
            )
      )
    )

  return attempt(maxAttempts, baseDelayMs)
}

// 使用示例
const fetchUserWithRetry = (userId: string) =>
  retry(fetchUser(userId), 3, 1000)
  // 尝试：立即、1秒后、2秒后重试
```

### 默认值

```typescript
// 获取值或使用默认值（移除错误通道）
const getUsernameOrDefault = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.map(user => user.name),
    TE.getOrElse(() => T.of('Anonymous'))
  ) // Task<string> - 不再跟踪错误

// 保留错误通道但提供回退值
const getUserWithDefault = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.orElse(() => TE.right(defaultUser))
  ) // TaskEither<Error, User> - 错误通道仍然存在但总是成功
```

---

## 5. 真实 API 示例

### 完整的 Fetch 包装器

```typescript
// types.ts
interface ApiError {
  code: string
  message: string
  status: number
  details?: unknown
}

// api.ts
const createApiError = (
  code: string,
  message: string,
  status: number,
  details?: unknown
): ApiError => ({ code, message, status, details })

const request = <T>(
  url: string,
  options: RequestInit = {}
): TE.TaskEither<ApiError, T> =>
  TE.tryCatch(
    async () => {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        throw createApiError(
          body.code || 'HTTP_ERROR',
          body.message || response.statusText,
          response.status,
          body
        )
      }

      // 处理 204 No Content
      if (response.status === 204) {
        return undefined as T
      }

      return response.json()
    },
    (error): ApiError => {
      if (typeof error === 'object' && error !== null && 'code' in error) {
        return error as ApiError
      }
      return createApiError(
        'NETWORK_ERROR',
        error instanceof Error ? error.message : 'Request failed',
        0
      )
    }
  )

// API 客户端
const api = {
  get: <T>(url: string) => request<T>(url),

  post: <T>(url: string, body: unknown) =>
    request<T>(url, {
      method: 'POST',
      body: JSON.stringify(body)
    }),

  put: <T>(url: string, body: unknown) =>
    request<T>(url, {
      method: 'PUT',
      body: JSON.stringify(body)
    }),

  delete: (url: string) =>
    request<void>(url, { method: 'DELETE' }),
}

// 使用示例
const getUser = (id: string) => api.get<User>(`/api/users/${id}`)
const createUser = (data: CreateUserDto) => api.post<User>('/api/users', data)
const updateUser = (id: string, data: UpdateUserDto) => api.put<User>(`/api/users/${id}`, data)
const deleteUser = (id: string) => api.delete(`/api/users/${id}`)
```

### 数据库操作（Prisma 示例）

```typescript
import { PrismaClient, Prisma } from '@prisma/client'

type DbError =
  | { _tag: 'NotFound'; entity: string; id: string }
  | { _tag: 'UniqueViolation'; field: string }
  | { _tag: 'ConnectionError'; cause: unknown }

const prisma = new PrismaClient()

const wrapPrisma = <T>(
  operation: () => Promise<T>
): TE.TaskEither<DbError, T> =>
  TE.tryCatch(
    operation,
    (error): DbError => {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2002') {
          const field = (error.meta?.target as string[])?.join(', ') || 'unknown'
          return { _tag: 'UniqueViolation', field }
        }
        if (error.code === 'P2025') {
          return { _tag: 'NotFound', entity: 'Record', id: 'unknown' }
        }
      }
      return { _tag: 'ConnectionError', cause: error }
    }
  )

// 仓库模式
const userRepository = {
  findById: (id: string): TE.TaskEither<DbError, User> =>
    pipe(
      wrapPrisma(() => prisma.user.findUnique({ where: { id } })),
      TE.chain(user =>
        user
          ? TE.right(user)
          : TE.left({ _tag: 'NotFound', entity: 'User', id })
      )
    ),

  findByEmail: (email: string): TE.TaskEither<DbError, User | null> =>
    wrapPrisma(() => prisma.user.findUnique({ where: { email } })),

  create: (data: CreateUserInput): TE.TaskEither<DbError, User> =>
    wrapPrisma(() => prisma.user.create({ data })),

  update: (id: string, data: UpdateUserInput): TE.TaskEither<DbError, User> =>
    wrapPrisma(() => prisma.user.update({ where: { id }, data })),

  delete: (id: string): TE.TaskEither<DbError, void> =>
    pipe(
      wrapPrisma(() => prisma.user.delete({ where: { id } })),
      TE.map(() => undefined)
    ),
}

// 使用仓库的服务
const createUserService = (input: CreateUserInput) =>
  pipe(
    // 检查邮箱不存在
    userRepository.findByEmail(input.email),
    TE.chain(existing =>
      existing
        ? TE.left({ _tag: 'UniqueViolation' as const, field: 'email' })
        : TE.right(undefined)
    ),
    // 创建用户
    TE.chain(() => userRepository.create(input))
  )
```

### 文件操作（Node.js）

```typescript
import * as fs from 'fs/promises'
import * as path from 'path'

type FileError =
  | { _tag: 'NotFound'; path: string }
  | { _tag: 'PermissionDenied'; path: string }
  | { _tag: 'IoError'; cause: unknown }

const toFileError = (error: unknown, filePath: string): FileError => {
  if (error instanceof Error) {
    if ('code' in error) {
      if (error.code === 'ENOENT') return { _tag: 'NotFound', path: filePath }
      if (error.code === 'EACCES') return { _tag: 'PermissionDenied', path: filePath }
    }
  }
  return { _tag: 'IoError', cause: error }
}

const readFile = (filePath: string): TE.TaskEither<FileError, string> =>
  TE.tryCatch(
    () => fs.readFile(filePath, 'utf-8'),
    (e) => toFileError(e, filePath)
  )

const writeFile = (filePath: string, content: string): TE.TaskEither<FileError, void> =>
  TE.tryCatch(
    () => fs.writeFile(filePath, content, 'utf-8'),
    (e) => toFileError(e, filePath)
  )

const readJson = <T>(filePath: string): TE.TaskEither<FileError | { _tag: 'ParseError'; cause: unknown }, T> =>
  pipe(
    readFile(filePath),
    TE.chain(content =>
      TE.tryCatch(
        () => Promise.resolve(JSON.parse(content)),
        (e): { _tag: 'ParseError'; cause: unknown } => ({ _tag: 'ParseError', cause: e })
      )
    )
  )

// 使用示例：加载配置并带回退
const loadConfig = () =>
  pipe(
    readJson<Config>('./config.json'),
    TE.orElse(() => readJson<Config>('./config.default.json')),
    TE.getOrElse(() => T.of(defaultConfig))
  )
```

---

## 6. 处理结果

### 使用 fold/match 进行模式匹配

```typescript
// fold：处理成功和失败，返回一个 Task（不再有错误通道）
const displayResult = pipe(
  fetchUser(userId),
  TE.fold(
    (error) => T.of(`Error: ${error.message}`),
    (user) => T.of(`Welcome, ${user.name}!`)
  )
) // Task<string>

// 执行并获取字符串
const message = await displayResult()
```

### 获取原始 Either

```typescript
// 有时你需要直接使用 Either
const result = await fetchUser(userId)() // Either<Error, User>

if (E.isLeft(result)) {
  console.error('Failed:', result.left)
} else {
  console.log('User:', result.right)
}
```

### 在 Express/Hono 处理器中

```typescript
// Express
app.get('/users/:id', async (req, res) => {
  const result = await pipe(
    fetchUser(req.params.id),
    TE.fold(
      (error) => T.of({ status: 500, body: { error: error.message } }),
      (user) => T.of({ status: 200, body: user })
    )
  )()

  res.status(result.status).json(result.body)
})

// 使用辅助函数更简洁
const sendResult = <E, A>(
  res: Response,
  te: TE.TaskEither<E, A>,
  errorStatus: number = 500
) =>
  pipe(
    te,
    TE.fold(
      (error) => T.of(res.status(errorStatus).json({ error })),
      (data) => T.of(res.json(data))
    )
  )()

app.get('/users/:id', async (req, res) => {
  await sendResult(res, fetchUser(req.params.id), 404)
})
```

---

## 7. 常用模式参考

### 快速转换

```typescript
// 转换成功值
TE.map(user => user.name)

// 转换错误
TE.mapLeft(error => ({ ...error, timestamp: Date.now() }))

// 同时转换两者
TE.bimap(
  error => enhanceError(error),
  user => user.profile
)
```

### 过滤

```typescript
// 条件不满足时失败
pipe(
  fetchUser(userId),
  TE.filterOrElse(
    user => user.isActive,
    user => new Error(`User ${user.id} is not active`)
  )
)
```

### 不改变值的副作用

```typescript
// 成功时记录日志，保持值不变
pipe(
  fetchUser(userId),
  TE.tap(user => TE.fromIO(() => console.log(`Fetched user: ${user.id}`)))
)

// 错误时记录日志，保持错误不变
pipe(
  fetchUser(userId),
  TE.tapError(error => TE.fromIO(() => console.error(`Failed: ${error.message}`)))
)

// chainFirst 类似于 tap，但用于返回 TaskEither 的操作
pipe(
  createUser(userData),
  TE.chainFirst(user => sendWelcomeEmail(user.email))
) // 返回创建的用户，而不是邮件结果
```

### 从其他类型转换

```typescript
// 从 Either
const fromEither = TE.fromEither(E.right(42))

// 从 Option
import * as O from 'fp-ts/Option'
const fromOption = TE.fromOption(() => new Error('Value was None'))
const result = fromOption(O.some(42))

// 从布尔值
const fromBoolean = TE.fromPredicate(
  (x: number) => x > 0,
  () => new Error('Must be positive')
)
```

---

## 快速参考卡片

| 你想要什么 | 如何实现 |
|---------------|--------------|
| 包装一个 promise | `TE.tryCatch(() => promise, toError)` |
| 创建成功 | `TE.right(value)` |
| 创建失败 | `TE.left(error)` |
| 转换值 | `TE.map(fn)` |
| 转换错误 | `TE.mapLeft(fn)` |
| 链式异步操作 | `TE.chain(fn)` 或 `TE.flatMap(fn)` |
| 并行运行 | `sequenceT(TE.ApplyPar)(te1, te2, te3)` |
| 并行处理数组 | `TE.traverseArray(fn)(items)` |
| 从错误中恢复 | `TE.orElse(fn)` |
| 使用默认值 | `TE.getOrElse(() => T.of(default))` |
| 处理两种情况 | `TE.fold(onError, onSuccess)` |
| 构建上下文 | `TE.Do` + `TE.bind('name', () => te)` |
| 记录日志但不改变值 | `TE.tap(fn)` |
| 带错误过滤 | `TE.filterOrElse(pred, toError)` |

---

## 前后对比总结

### 获取数据

```typescript
// 之前
async function getUser(id: string) {
  try {
    const res = await fetch(`/api/users/${id}`)
    if (!res.ok) throw new Error('Not found')
    return await res.json()
  } catch (e) {
    console.error(e)
    return null
  }
}

// 之后
const getUser = (id: string) =>
  TE.tryCatch(
    async () => {
      const res = await fetch(`/api/users/${id}`)
      if (!res.ok) throw new Error('Not found')
      return res.json()
    },
    E.toError
  )
```

### 链式操作

```typescript
// 之前
async function processOrder(orderId: string) {
  const order = await fetchOrder(orderId)
  if (!order) throw new Error('No order')
  const user = await fetchUser(order.userId)
  if (!user) throw new Error('No user')
  const result = await chargePayment(user, order.total)
  return result
}

// 之后
const processOrder = (orderId: string) =>
  pipe(
    TE.Do,
    TE.bind('order', () => fetchOrder(orderId)),
    TE.bind('user', ({ order }) => fetchUser(order.userId)),
    TE.chain(({ user, order }) => chargePayment(user, order.total))
  )
```

### 错误恢复

```typescript
// 之前
async function getData(id: string) {
  try {
    return await fetchFromApi(id)
  } catch {
    try {
      return await fetchFromCache(id)
    } catch {
      return defaultValue
    }
  }
}

// 之后
const getData = (id: string) =>
  pipe(
    fetchFromApi(id),
    TE.orElse(() => fetchFromCache(id)),
    TE.getOrElse(() => T.of(defaultValue))
  )
```

## 局限性

- 仅当任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
