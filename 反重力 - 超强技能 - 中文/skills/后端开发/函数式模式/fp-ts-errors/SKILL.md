---
name: fp-ts-errors
description: "使用 fp-ts 的 Either 和 TaskEither 将错误作为值处理，实现更清晰、更可预测的 TypeScript 代码。当用户要求'fp-ts 错误处理'、'Either 模式'、'TaskEither 异步错误'、'类型安全的错误处理'或'函数式错误处理'时使用。"
risk: safe
source: "https://github.com/whatiskadudoing/fp-ts-skills"
date_added: "2026-02-27"
---

# fp-ts 实战错误处理

本技能教你如何避免 try/catch 意大利面代码。没有学术术语——只有解决实际问题的实用模式。

## 何时使用本技能

- 需要 TypeScript 中的类型安全错误处理
- 用 Either 和 TaskEither 模式替代 try/catch
- 构建需要显式错误类型的 API 或服务
- 累积多个验证错误

核心理念：**错误只是数据**。与其抛向虚空期待有人捕获，不如作为值返回，让 TypeScript 追踪。

---

## 1. 停止到处抛异常

### 异常的问题

异常在类型中不可见。它们破坏了函数间的契约。

```typescript
// 函数签名承诺的：
function getUser(id: string): User

// 实际行为：
function getUser(id: string): User {
  if (!id) throw new Error('ID required')
  const user = db.find(id)
  if (!user) throw new Error('User not found')
  return user
}

// 调用者完全不知道这可能失败
const user = getUser(id) // 可能爆炸！
```

你最终会写出这样的代码：

```typescript
// 混乱：到处 try/catch
function processOrder(orderId: string) {
  let order
  try {
    order = getOrder(orderId)
  } catch (e) {
    console.error('Failed to get order')
    return null
  }

  let user
  try {
    user = getUser(order.userId)
  } catch (e) {
    console.error('Failed to get user')
    return null
  }

  let payment
  try {
    payment = chargeCard(user.cardId, order.total)
  } catch (e) {
    console.error('Payment failed')
    return null
  }

  return { order, user, payment }
}
```

### 解决方案：将错误作为值返回

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 现在 TypeScript 知道这可能失败
function getUser(id: string): E.Either<string, User> {
  if (!id) return E.left('ID required')
  const user = db.find(id)
  if (!user) return E.left('User not found')
  return E.right(user)
}

// 调用者被迫处理两种情况
const result = getUser(id)
// result 是 Either<string, User> - 错误或成功，不会同时存在
```

---

## 2. 结果模式（Either）

`Either<E, A>` 很简单：它持有错误（`E`）或值（`A`）。

- `Left` = 错误情况
- `Right` = 成功情况（"right" 意为 "正确"）

```typescript
import * as E from 'fp-ts/Either'

// 创建值
const success = E.right(42)           // Right(42)
const failure = E.left('Oops')        // Left('Oops')

// 检查持有的是什么
if (E.isRight(result)) {
  console.log(result.right) // 成功值
} else {
  console.log(result.left)  // 错误
}

// 更好的方式：用 fold 模式匹配
const message = pipe(
  result,
  E.fold(
    (error) => `失败: ${error}`,
    (value) => `得到: ${value}`
  )
)
```

### 将抛异常代码转换为 Either

```typescript
// 用 tryCatch 包装任何抛异常的函数
const parseJSON = (json: string): E.Either<Error, unknown> =>
  E.tryCatch(
    () => JSON.parse(json),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  )

parseJSON('{"valid": true}')  // Right({ valid: true })
parseJSON('not json')          // Left(SyntaxError: ...)

// 对于要复用的函数，用 tryCatchK
const safeParseJSON = E.tryCatchK(
  JSON.parse,
  (e) => (e instanceof Error ? e : new Error(String(e)))
)
```

### 常用 Either 操作

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 转换成功值
const doubled = pipe(
  E.right(21),
  E.map(n => n * 2)
) // Right(42)

// 转换错误
const betterError = pipe(
  E.left('bad'),
  E.mapLeft(e => `错误: ${e}`)
) // Left('错误: bad')

// 为错误提供默认值
const value = pipe(
  E.left('failed'),
  E.getOrElse(() => 0)
) // 0

// 将可空值转换为 Either
const fromNullable = E.fromNullable('not found')
fromNullable(user)  // 存在时 Right(user)，null/undefined 时 Left('not found')
```

---

## 3. 链式调用可能失败的操作

真正的威力在于链式调用。每一步都可能失败，但你写出的是清晰的管道。

### 之前：嵌套 try/catch 地狱

```typescript
// 混乱：每步都可能失败，到处嵌套 try/catch
function processUserOrder(userId: string, productId: string): Result | null {
  let user
  try {
    user = getUser(userId)
  } catch (e) {
    logError('User fetch failed', e)
    return null
  }

  if (!user.isActive) {
    logError('User not active')
    return null
  }

  let product
  try {
    product = getProduct(productId)
  } catch (e) {
    logError('Product fetch failed', e)
    return null
  }

  if (product.stock < 1) {
    logError('Out of stock')
    return null
  }

  let order
  try {
    order = createOrder(user, product)
  } catch (e) {
    logError('Order creation failed', e)
    return null
  }

  return order
}
```

### 之后：Either 清晰链式调用

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 每个函数返回 Either<Error, T>
const getUser = (id: string): E.Either<string, User> => { ... }
const getProduct = (id: string): E.Either<string, Product> => { ... }
const createOrder = (user: User, product: Product): E.Either<string, Order> => { ... }

// 链式调用 - 第一个错误就会停止链条
const processUserOrder = (userId: string, productId: string): E.Either<string, Order> =>
  pipe(
    getUser(userId),
    E.filterOrElse(
      user => user.isActive,
      () => 'User not active'
    ),
    E.chain(user =>
      pipe(
        getProduct(productId),
        E.filterOrElse(
          product => product.stock >= 1,
          () => 'Out of stock'
        ),
        E.chain(product => createOrder(user, product))
      )
    )
  )

// 或用 Do 语法更清晰地访问中间值
const processUserOrder = (userId: string, productId: string): E.Either<string, Order> =>
  pipe(
    E.Do,
    E.bind('user', () => getUser(userId)),
    E.filterOrElse(
      ({ user }) => user.isActive,
      () => 'User not active'
    ),
    E.bind('product', () => getProduct(productId)),
    E.filterOrElse(
      ({ product }) => product.stock >= 1,
      () => 'Out of stock'
    ),
    E.chain(({ user, product }) => createOrder(user, product))
  )
```

### 不同错误类型？用 chainW

```typescript
type ValidationError = { type: 'validation'; message: string }
type DbError = { type: 'db'; message: string }

const validateInput = (id: string): E.Either<ValidationError, string> => { ... }
const fetchFromDb = (id: string): E.Either<DbError, User> => { ... }

// chainW（W = "wider"）自动合并错误类型
const process = (id: string): E.Either<ValidationError | DbError, User> =>
  pipe(
    validateInput(id),
    E.chainW(validId => fetchFromDb(validId))
  )
```

---

## 4. 收集多个错误

有时你需要所有错误，而不只是第一个。表单验证是经典例子。

### 之前：手动收集错误

```typescript
// 混乱：手动错误累积
function validateForm(form: FormData): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  if (!form.email) {
    errors.push('Email required')
  } else if (!form.email.includes('@')) {
    errors.push('Invalid email')
  }

  if (!form.password) {
    errors.push('Password required')
  } else if (form.password.length < 8) {
    errors.push('Password too short')
  }

  if (!form.age) {
    errors.push('Age required')
  } else if (form.age < 18) {
    errors.push('Must be 18+')
  }

  return { valid: errors.length === 0, errors }
}
```

### 之后：带错误累积的验证

```typescript
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

// 错误作为 NonEmptyArray（至少有一个）
type Errors = NEA.NonEmptyArray<string>

// 创建累积错误的 applicative
const validation = E.getApplicativeValidation(NEA.getSemigroup<string>())

// 返回 Either<Errors, T> 的验证器
const validateEmail = (email: string): E.Either<Errors, string> =>
  !email ? E.left(NEA.of('Email required'))
  : !email.includes('@') ? E.left(NEA.of('Invalid email'))
  : E.right(email)

const validatePassword = (password: string): E.Either<Errors, string> =>
  !password ? E.left(NEA.of('Password required'))
  : password.length < 8 ? E.left(NEA.of('Password too short'))
  : E.right(password)

const validateAge = (age: number | undefined): E.Either<Errors, number> =>
  age === undefined ? E.left(NEA.of('Age required'))
  : age < 18 ? E.left(NEA.of('Must be 18+'))
  : E.right(age)

// 组合所有验证 - 收集所有错误
const validateForm = (form: FormData) =>
  sequenceS(validation)({
    email: validateEmail(form.email),
    password: validatePassword(form.password),
    age: validateAge(form.age)
  })

// 使用
validateForm({ email: '', password: '123', age: 15 })
// Left(['Email required', 'Password too short', 'Must be 18+'])

validateForm({ email: 'a@b.com', password: 'longpassword', age: 25 })
// Right({ email: 'a@b.com', password: 'longpassword', age: 25 })
```

### 表单字段级错误

```typescript
interface FieldError {
  field: string
  message: string
}

type FormErrors = NEA.NonEmptyArray<FieldError>

const fieldError = (field: string, message: string): FormErrors =>
  NEA.of({ field, message })

const formValidation = E.getApplicativeValidation(NEA.getSemigroup<FieldError>())

// 现在错误知道自己属于哪个字段
const validateEmail = (email: string): E.Either<FormErrors, string> =>
  !email ? E.left(fieldError('email', 'Required'))
  : !email.includes('@') ? E.left(fieldError('email', 'Invalid format'))
  : E.right(email)

// 容易在 UI 中显示
const getFieldError = (errors: FormErrors, field: string): string | undefined =>
  errors.find(e => e.field === field)?.message
```

---

## 5. 异步操作（TaskEither）

对于可能失败的异步操作，使用 `TaskEither`。它就像 `Either`，但用于 Promise。

- `TaskEither<E, A>` = 返回 `Promise<Either<E, A>>` 的函数
- 惰性：执行前什么都不运行

```typescript
import * as TE from 'fp-ts/TaskEither'
import { pipe } from 'fp-ts/function'

// 包装任何异步操作
const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(r => r.json()),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  )

// 链式异步操作 - 就像 Either
const getUserPosts = (userId: string): TE.TaskEither<Error, Post[]> =>
  pipe(
    fetchUser(userId),
    TE.chain(user => fetchPosts(user.id))
  )

// 准备好后执行
const result = await getUserPosts('123')() // 返回 Either<Error, Post[]>
```

### 之前：带错误处理的 Promise 链

```typescript
// 混乱：try/catch 混合 Promise 链
async function loadDashboard(userId: string) {
  try {
    const user = await fetchUser(userId)
    if (!user) throw new Error('User not found')

    let posts, notifications, settings
    try {
      [posts, notifications, settings] = await Promise.all([
        fetchPosts(user.id),
        fetchNotifications(user.id),
        fetchSettings(user.id)
      ])
    } catch (e) {
      // 哪个失败了？谁知道！
      console.error('Failed to load data', e)
      return null
    }

    return { user, posts, notifications, settings }
  } catch (e) {
    console.error('Failed to load user', e)
    return null
  }
}
```

### 之后：清晰的 TaskEither 管道

```typescript
import * as TE from 'fp-ts/TaskEither'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

const loadDashboard = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.chain(user =>
      pipe(
        // 用 sequenceS 并行获取
        sequenceS(TE.ApplyPar)({
          posts: fetchPosts(user.id),
          notifications: fetchNotifications(user.id),
          settings: fetchSettings(user.id)
        }),
        TE.map(data => ({ user, ...data }))
      )
    )
  )

// 执行并处理两种情况
pipe(
  loadDashboard('123'),
  TE.fold(
    (error) => T.of(renderError(error)),
    (data) => T.of(renderDashboard(data))
  )
)()
```

### 重试失败操作

```typescript
import * as T from 'fp-ts/Task'
import * as TE from 'fp-ts/TaskEither'
import { pipe } from 'fp-ts/function'

const retry = <E, A>(
  task: TE.TaskEither<E, A>,
  attempts: number,
  delayMs: number
): TE.TaskEither<E, A> =>
  pipe(
    task,
    TE.orElse((error) =>
      attempts > 1
        ? pipe(
            T.delay(delayMs)(T.of(undefined)),
            T.chain(() => retry(task, attempts - 1, delayMs * 2))
          )
        : TE.left(error)
    )
  )

// 最多重试 3 次，指数退避
const fetchWithRetry = retry(fetchUser('123'), 3, 1000)
```

### 回退到备选方案

```typescript
// 先尝试缓存，失败则回退到 API
const getUserData = (id: string) =>
  pipe(
    fetchFromCache(id),
    TE.orElse(() => fetchFromApi(id)),
    TE.orElse(() => TE.right(defaultUser)) // 最后手段默认值
  )
```

---

## 6. 模式间转换

真实代码库有抛异常函数、可空值和 Promise。以下是如何与它们协作。

### 从可空值到 Either

```typescript
import * as E from 'fp-ts/Either'
import * as O from 'fp-ts/Option'

// 直接转换
const user = users.find(u => u.id === id) // User | undefined
const result = E.fromNullable('User not found')(user)

// 从 Option
const maybeUser: O.Option<User> = O.fromNullable(user)
const eitherUser = pipe(
  maybeUser,
  E.fromOption(() => 'User not found')
)
```

### 从抛异常函数到 Either

```typescript
// 在边界处包装
const safeParse = <T>(schema: ZodSchema<T>) => (data: unknown): E.Either<ZodError, T> =>
  E.tryCatch(
    () => schema.parse(data),
    (e) => e as ZodError
  )

// 在代码中使用
const parseUser = safeParse(UserSchema)
const result = parseUser(rawData) // Either<ZodError, User>
```

### 从 Promise 到 TaskEither

```typescript
import * as TE from 'fp-ts/TaskEither'

// 包装外部异步函数
const fetchJson = <T>(url: string): TE.TaskEither<Error, T> =>
  TE.tryCatch(
    () => fetch(url).then(r => r.json()),
    (e) => new Error(`Fetch failed: ${e}`)
  )

// 包装 axios、prisma、任何异步库
const getUserFromDb = (id: string): TE.TaskEither<DbError, User> =>
  TE.tryCatch(
    () => prisma.user.findUniqueOrThrow({ where: { id } }),
    (e) => ({ code: 'DB_ERROR', cause: e })
  )
```

### 回到 Promise（逃生舱）

有时你需要纯 Promise 用于外部 API。

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as E from 'fp-ts/Either'

const myTaskEither: TE.TaskEither<Error, User> = fetchUser('123')

// 方式 1：获取 Either（保留两种情况）
const either: E.Either<Error, User> = await myTaskEither()

// 方式 2：错误时抛异常（用于遗留代码）
const toThrowingPromise = <E, A>(te: TE.TaskEither<E, A>): Promise<A> =>
  te().then(E.fold(
    (error) => Promise.reject(error),
    (value) => Promise.resolve(value)
  ))

const user = await toThrowingPromise(fetchUser('123')) // Left 时抛异常

// 方式 3：错误时使用默认值
const user = await pipe(
  fetchUser('123'),
  TE.getOrElse(() => T.of(defaultUser))
)()
```

---

## 实战场景

### 安全解析用户输入

```typescript
interface ParsedInput {
  id: number
  name: string
  tags: string[]
}

const parseInput = (raw: unknown): E.Either<string, ParsedInput> =>
  pipe(
    E.Do,
    E.bind('obj', () =>
      typeof raw === 'object' && raw !== null
        ? E.right(raw as Record<string, unknown>)
        : E.left('Input must be an object')
    ),
    E.bind('id', ({ obj }) =>
      typeof obj.id === 'number'
        ? E.right(obj.id)
        : E.left('id must be a number')
    ),
    E.bind('name', ({ obj }) =>
      typeof obj.name === 'string' && obj.name.length > 0
        ? E.right(obj.name)
        : E.left('name must be a non-empty string')
    ),
    E.bind('tags', ({ obj }) =>
      Array.isArray(obj.tags) && obj.tags.every(t => typeof t === 'string')
        ? E.right(obj.tags as string[])
        : E.left('tags must be an array of strings')
    ),
    E.map(({ id, name, tags }) => ({ id, name, tags }))
  )

// 使用
parseInput({ id: 1, name: 'test', tags: ['a', 'b'] })
// Right({ id: 1, name: 'test', tags: ['a', 'b'] })

parseInput({ id: 'wrong', name: '', tags: null })
// Left('id must be a number')
```

### 带完整错误处理的 API 调用

```typescript
interface ApiError {
  code: string
  message: string
  status?: number
}

const createApiError = (message: string, code = 'UNKNOWN', status?: number): ApiError =>
  ({ code, message, status })

const fetchWithErrorHandling = <T>(url: string): TE.TaskEither<ApiError, T> =>
  pipe(
    TE.tryCatch(
      () => fetch(url),
      () => createApiError('Network error', 'NETWORK')
    ),
    TE.chain(response =>
      response.ok
        ? TE.tryCatch(
            () => response.json() as Promise<T>,
            () => createApiError('Invalid JSON', 'PARSE')
          )
        : TE.left(createApiError(
            `HTTP ${response.status}`,
            response.status === 404 ? 'NOT_FOUND' : 'HTTP_ERROR',
            response.status
          ))
    )
  )

// 使用：对错误码模式匹配
const handleUserFetch = (userId: string) =>
  pipe(
    fetchWithErrorHandling<User>(`/api/users/${userId}`),
    TE.fold(
      (error) => {
        switch (error.code) {
          case 'NOT_FOUND': return T.of(showNotFoundPage())
          case 'NETWORK': return T.of(showOfflineMessage())
          default: return T.of(showGenericError(error.message))
        }
      },
      (user) => T.of(showUserProfile(user))
    )
  )
```

### 处理部分项可能失败的列表

```typescript
import * as A from 'fp-ts/Array'
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

interface ProcessResult<T> {
  successes: T[]
  failures: Array<{ item: unknown; error: string }>
}

// 处理全部，分别收集成功和失败
const processAllCollectErrors = <T, R>(
  items: T[],
  process: (item: T) => E.Either<string, R>
): ProcessResult<R> => {
  const results = items.map((item, index) =>
    pipe(
      process(item),
      E.mapLeft(error => ({ item, error, index }))
    )
  )

  return {
    successes: pipe(results, A.filterMap(E.toOption)),
    failures: pipe(
      results,
      A.filterMap(r => E.isLeft(r) ? O.some(r.left) : O.none)
    )
  }
}

// 使用
const parseNumbers = (inputs: string[]) =>
  processAllCollectErrors(inputs, input => {
    const n = parseInt(input, 10)
    return isNaN(n) ? E.left(`Invalid number: ${input}`) : E.right(n)
  })

parseNumbers(['1', 'abc', '3', 'def'])
// {
//   successes: [1, 3],
//   failures: [
//     { item: 'abc', error: 'Invalid number: abc', index: 1 },
//     { item: 'def', error: 'Invalid number: def', index: 3 }
//   ]
// }
```

### 部分成功的批量操作

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as T from 'fp-ts/Task'
import { pipe } from 'fp-ts/function'

interface BulkResult<T> {
  succeeded: T[]
  failed: Array<{ id: string; error: string }>
}

const bulkProcess = <T>(
  ids: string[],
  process: (id: string) => TE.TaskEither<string, T>
): T.Task<BulkResult<T>> =>
  pipe(
    ids,
    A.map(id =>
      pipe(
        process(id),
        TE.fold(
          (error) => T.of({ type: 'failed' as const, id, error }),
          (result) => T.of({ type: 'succeeded' as const, result })
        )
      )
    ),
    T.sequenceArray,
    T.map(results => ({
      succeeded: results
        .filter((r): r is { type: 'succeeded'; result: T } => r.type === 'succeeded')
        .map(r => r.result),
      failed: results
        .filter((r): r is { type: 'failed'; id: string; error: string } => r.type === 'failed')
        .map(({ id, error }) => ({ id, error }))
    }))
  )

// 使用
const deleteUsers = (userIds: string[]) =>
  bulkProcess(userIds, id =>
    pipe(
      deleteUser(id),
      TE.mapLeft(e => e.message)
    )
  )

// 所有操作都运行，你得到成功和失败的报告
```

---

## 快速参考

| 模式 | 使用场景 | 示例 |
|------|----------|------|
| `E.right(value)` | 创建成功 | `E.right(42)` |
| `E.left(error)` | 创建失败 | `E.left('not found')` |
| `E.tryCatch(fn, onError)` | 包装抛异常代码 | `E.tryCatch(() => JSON.parse(s), toError)` |
| `E.fromNullable(error)` | 转换可空值 | `E.fromNullable('missing')(maybeValue)` |
| `E.map(fn)` | 转换成功值 | `pipe(result, E.map(x => x * 2))` |
| `E.mapLeft(fn)` | 转换错误 | `pipe(result, E.mapLeft(addContext))` |
| `E.chain(fn)` | 链式操作 | `pipe(getA(), E.chain(a => getB(a.id)))` |
| `E.chainW(fn)` | 链式不同错误类型 | `pipe(validate(), E.chainW(save))` |
| `E.fold(onError, onSuccess)` | 处理两种情况 | `E.fold(showError, showData)` |
| `E.getOrElse(onError)` | 提取并设默认值 | `E.getOrElse(() => 0)` |
| `E.filterOrElse(pred, onFalse)` | 验证并返回错误 | `E.filterOrElse(x => x > 0, () => 'must be positive')` |
| `sequenceS(validation)({...})` | 收集所有错误 | 表单验证 |

### TaskEither 等价操作

所有 Either 操作都有 TaskEither 等价版本：
- `TE.right`, `TE.left`, `TE.tryCatch`
- `TE.map`, `TE.mapLeft`, `TE.chain`, `TE.chainW`
- `TE.fold`, `TE.getOrElse`, `TE.filterOrElse`
- `TE.orElse` 用于回退

---

## 总结

1. **将错误作为值返回** - 用 Either/TaskEither 替代抛异常
2. **自信地链式调用** - `chain` 自动在第一个错误处停止
3. **需要时收集所有错误** - 用 validation applicative 处理表单
4. **在边界处包装** - 在边缘转换抛异常/Promise 代码
5. **最后再匹配** - 用 `fold` 在准备行动时处理两种情况

收益：TypeScript 追踪你的错误，不再遗忘 try/catch，清晰的控制流，可组合的错误处理。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需输入、权限、安全边界或成功标准，停止并请求澄清。
