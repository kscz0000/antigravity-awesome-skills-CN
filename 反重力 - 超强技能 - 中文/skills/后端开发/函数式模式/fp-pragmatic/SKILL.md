---
name: fp-pragmatic
description: 实用的函数式编程指南，无学术术语——80/20法则，不讲理论只讲效果。当用户要求'fp-ts入门'、'函数式编程实践'、'TypeScript FP'或相关主题时使用。
risk: unknown
source: community
version: 1.0.0
author: kadu
tags:
  - fp-ts
  - functional-programming
  - typescript
  - pragmatic
  - beginner-friendly
  - best-practices
---

# 实用函数式编程

**先读这个。** 本指南跳过学术术语，只讲真正重要的内容。没有范畴论，没有抽象废话，只有能改善代码的模式。

## 使用场景
- 需要一个实用的 fp-ts 或 TypeScript 函数式编程入门指南。
- 任务是探索性或教育性的，需要了解哪些内容真正值得采用。
- 需要指导何时 FP 有帮助，何时保持简单更好。

## 黄金法则

> **如果函数式编程让你的代码更难读，就别用它。**

FP 是工具，不是信仰。有用就用，没用就跳过。

---

## FP 的 80/20 法则

这五个模式能带来大部分收益。先掌握这些，再探索其他。

### 1. Pipe：清晰链接操作

不要嵌套函数调用或创建中间变量，按阅读顺序链接操作。

```typescript
import { pipe } from 'fp-ts/function'

// 之前：难读（由内向外）
const result = format(validate(parse(input)))

// 之前：变量太多
const parsed = parse(input)
const validated = validate(parsed)
const result = format(validated)

// 之后：清晰的线性流程
const result = pipe(
  input,
  parse,
  validate,
  format
)
```

**何时使用 pipe：**
- 对同一数据进行 3 次以上转换
- 发现自己在给一次性变量命名
- 逻辑从上到下读更顺畅

**何时跳过 pipe：**
- 只有 1-2 个操作（直接调用就行）
- 操作之间不能自然串联

### 2. Option：处理缺失值，无需 null 检查

别再到处写 `if (x !== null && x !== undefined)` 了。

```typescript
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

// 之前：防御性 null 检查
function getUserCity(user: User | null): string {
  if (user === null) return 'Unknown'
  if (user.address === null) return 'Unknown'
  if (user.address.city === null) return 'Unknown'
  return user.address.city
}

// 之后：链式处理可能缺失的值
const getUserCity = (user: User | null): string =>
  pipe(
    O.fromNullable(user),
    O.flatMap(u => O.fromNullable(u.address)),
    O.flatMap(a => O.fromNullable(a.city)),
    O.getOrElse(() => 'Unknown')
  )
```

**大白话翻译：**
- `O.fromNullable(x)` = "包装这个值，把 null/undefined 当作'无'"
- `O.flatMap(fn)` = "如果有值，应用这个函数"
- `O.getOrElse(() => default)` = "解包，如果无则使用这个默认值"

### 3. Either：让错误显式化

别为预期的失败抛异常。把错误作为值返回。

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 之前：隐藏的失败模式
function parseAge(input: string): number {
  const age = parseInt(input, 10)
  if (isNaN(age)) throw new Error('Invalid age')
  if (age < 0) throw new Error('Age cannot be negative')
  return age
}

// 之后：错误在类型中可见
function parseAge(input: string): E.Either<string, number> {
  const age = parseInt(input, 10)
  if (isNaN(age)) return E.left('Invalid age')
  if (age < 0) return E.left('Age cannot be negative')
  return E.right(age)
}

// 使用
const result = parseAge(userInput)
if (E.isRight(result)) {
  console.log(`Age is ${result.right}`)
} else {
  console.log(`Error: ${result.left}`)
}
```

**大白话翻译：**
- `E.right(value)` = "成功，这是值"
- `E.left(error)` = "失败，这是错误"
- `E.isRight(x)` = "成功了吗？"

### 4. Map：不解包直接转换

在容器内转换值，无需先提取。

```typescript
import * as O from 'fp-ts/Option'
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Array'
import { pipe } from 'fp-ts/function'

// 在 Option 内转换
const maybeUser: O.Option<User> = O.some({ name: 'Alice', age: 30 })
const maybeName: O.Option<string> = pipe(
  maybeUser,
  O.map(user => user.name)
)

// 在 Either 内转换
const result: E.Either<Error, number> = E.right(5)
const doubled: E.Either<Error, number> = pipe(
  result,
  E.map(n => n * 2)
)

// 转换数组（同一个概念！）
const numbers = [1, 2, 3]
const doubled = pipe(
  numbers,
  A.map(n => n * 2)
)
```

### 5. FlatMap：链接可能失败的操作

当每一步都可能失败时，把它们串联起来。

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

const parseJSON = (s: string): E.Either<string, unknown> =>
  E.tryCatch(() => JSON.parse(s), () => 'Invalid JSON')

const extractEmail = (data: unknown): E.Either<string, string> => {
  if (typeof data === 'object' && data !== null && 'email' in data) {
    return E.right((data as { email: string }).email)
  }
  return E.left('No email field')
}

const validateEmail = (email: string): E.Either<string, string> =>
  email.includes('@') ? E.right(email) : E.left('Invalid email format')

// 链接所有步骤——任何一步失败，整体失败
const getValidEmail = (input: string): E.Either<string, string> =>
  pipe(
    parseJSON(input),
    E.flatMap(extractEmail),
    E.flatMap(validateEmail)
  )

// 成功路径：Right('user@example.com')
// 任何失败：Left('具体错误信息')
```

**大白话：** `flatMap` 意思是"如果这步成功了，尝试下一步"

---

## 何时不用 FP

函数式编程不总是答案。以下情况保持简单。

### 简单的 null 检查

```typescript
// 直接用可选链——语言内置的
const city = user?.address?.city ?? 'Unknown'

// 别过度复杂化
const city = pipe(
  O.fromNullable(user),
  O.flatMap(u => O.fromNullable(u.address)),
  O.flatMap(a => O.fromNullable(a.city)),
  O.getOrElse(() => 'Unknown')
)
```

### 简单的循环

```typescript
// 需要提前退出或复杂逻辑时，for 循环挺好
function findFirst(items: Item[], predicate: (i: Item) => boolean): Item | null {
  for (const item of items) {
    if (predicate(item)) return item
  }
  return null
}

// 别强行用 FP
const result = pipe(
  items,
  A.findFirst(predicate),
  O.toNullable
)
```

### 性能关键代码

```typescript
// 热路径用命令式更快（无中间数组）
function sumLarge(numbers: number[]): number {
  let sum = 0
  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i]
  }
  return sum
}

// fp-ts 会创建中间结构
const sum = pipe(numbers, A.reduce(0, (acc, n) => acc + n))
```

### 团队不懂 FP 时

如果只有你能读懂代码，那不是好代码。

```typescript
// 如果你的团队熟悉这个模式
async function getUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) return null
    return await response.json()
  } catch {
    return null
  }
}

// 别强推这个给他们
const getUser = (id: string): TE.TaskEither<Error, User> =>
  pipe(
    TE.tryCatch(() => fetch(`/api/users/${id}`), E.toError),
    TE.flatMap(r => r.ok ? TE.right(r) : TE.left(new Error('Not found'))),
    TE.flatMap(r => TE.tryCatch(() => r.json(), E.toError))
  )
```

---

## 快速见效：今天就能改善代码的简单改动

### 1. 用 pipe + fold 替换嵌套三元

```typescript
// 之前：嵌套三元噩梦
const message = user === null
  ? 'No user'
  : user.isAdmin
    ? `Admin: ${user.name}`
    : `User: ${user.name}`

// 之后：清晰的情况处理
const message = pipe(
  O.fromNullable(user),
  O.fold(
    () => 'No user',
    (u) => u.isAdmin ? `Admin: ${u.name}` : `User: ${u.name}`
  )
)
```

### 2. 用 tryCatch 替换 try-catch

```typescript
// 之前：到处 try-catch
let config
try {
  config = JSON.parse(rawConfig)
} catch {
  config = defaultConfig
}

// 之后：一行搞定
const config = pipe(
  E.tryCatch(() => JSON.parse(rawConfig), () => 'parse error'),
  E.getOrElse(() => defaultConfig)
)
```

### 3. 用 Option 替换 undefined 返回值

```typescript
// 之前：调用者可能忘记检查
function findUser(id: string): User | undefined {
  return users.find(u => u.id === id)
}

// 之后：类型强制调用者处理缺失情况
function findUser(id: string): O.Option<User> {
  return O.fromNullable(users.find(u => u.id === id))
}
```

### 4. 用类型化错误替换错误字符串

```typescript
// 之前：只是字符串
function validate(data: unknown): E.Either<string, User> {
  // ...
  return E.left('validation failed')
}

// 之后：结构化错误
type ValidationError = {
  field: string
  message: string
}

function validate(data: unknown): E.Either<ValidationError, User> {
  // ...
  return E.left({ field: 'email', message: 'Invalid format' })
}
```

### 5. 用 const 断言创建错误类型

```typescript
// 不用类也能创建特定错误类型
const NotFound = (id: string) => ({ _tag: 'NotFound' as const, id })
const Unauthorized = { _tag: 'Unauthorized' as const }
const ValidationFailed = (errors: string[]) =>
  ({ _tag: 'ValidationFailed' as const, errors })

type AppError =
  | ReturnType<typeof NotFound>
  | typeof Unauthorized
  | ReturnType<typeof ValidationFailed>

// 现在可以模式匹配
const handleError = (error: AppError): string => {
  switch (error._tag) {
    case 'NotFound': return `Item ${error.id} not found`
    case 'Unauthorized': return 'Please log in'
    case 'ValidationFailed': return error.errors.join(', ')
  }
}
```

---

## 常见重构：前后对比

### 回调地狱变 Pipe

```typescript
// 之前
fetchUser(id, (user) => {
  if (!user) return handleNoUser()
  fetchPosts(user.id, (posts) => {
    if (!posts) return handleNoPosts()
    fetchComments(posts[0].id, (comments) => {
      render(user, posts, comments)
    })
  })
})

// 之后（用 TaskEither 处理异步）
import * as TE from 'fp-ts/TaskEither'

const loadData = (id: string) =>
  pipe(
    fetchUser(id),
    TE.flatMap(user => pipe(
      fetchPosts(user.id),
      TE.map(posts => ({ user, posts }))
    )),
    TE.flatMap(({ user, posts }) => pipe(
      fetchComments(posts[0].id),
      TE.map(comments => ({ user, posts, comments }))
    ))
  )

// 执行
const result = await loadData('123')()
pipe(
  result,
  E.fold(handleError, ({ user, posts, comments }) => render(user, posts, comments))
)
```

### 多重 null 检查变 Option 链

```typescript
// 之前
function getManagerEmail(employee: Employee): string | null {
  if (!employee.department) return null
  if (!employee.department.manager) return null
  if (!employee.department.manager.email) return null
  return employee.department.manager.email
}

// 之后
const getManagerEmail = (employee: Employee): O.Option<string> =>
  pipe(
    O.fromNullable(employee.department),
    O.flatMap(d => O.fromNullable(d.manager)),
    O.flatMap(m => O.fromNullable(m.email))
  )

// 使用
pipe(
  getManagerEmail(employee),
  O.fold(
    () => sendToDefault(),
    (email) => sendTo(email)
  )
)
```

### 多重校验

```typescript
// 之前：遇到第一个错误就抛
function validateUser(data: unknown): User {
  if (!data || typeof data !== 'object') throw new Error('Must be object')
  const obj = data as Record<string, unknown>
  if (typeof obj.email !== 'string') throw new Error('Email required')
  if (!obj.email.includes('@')) throw new Error('Invalid email')
  if (typeof obj.age !== 'number') throw new Error('Age required')
  if (obj.age < 0) throw new Error('Age must be positive')
  return obj as User
}

// 之后：返回第一个错误，类型安全
const validateUser = (data: unknown): E.Either<string, User> =>
  pipe(
    E.Do,
    E.bind('obj', () =>
      typeof data === 'object' && data !== null
        ? E.right(data as Record<string, unknown>)
        : E.left('Must be object')
    ),
    E.bind('email', ({ obj }) =>
      typeof obj.email === 'string' && obj.email.includes('@')
        ? E.right(obj.email)
        : E.left('Valid email required')
    ),
    E.bind('age', ({ obj }) =>
      typeof obj.age === 'number' && obj.age >= 0
        ? E.right(obj.age)
        : E.left('Valid age required')
    ),
    E.map(({ email, age }) => ({ email, age }))
  )
```

### Promise 链变 TaskEither

```typescript
// 之前
async function processOrder(orderId: string): Promise<Receipt> {
  const order = await fetchOrder(orderId)
  if (!order) throw new Error('Order not found')

  const validated = await validateOrder(order)
  if (!validated.success) throw new Error(validated.error)

  const payment = await processPayment(validated.order)
  if (!payment.success) throw new Error('Payment failed')

  return generateReceipt(payment)
}

// 之后
const processOrder = (orderId: string): TE.TaskEither<string, Receipt> =>
  pipe(
    fetchOrderTE(orderId),
    TE.flatMap(order =>
      order ? TE.right(order) : TE.left('Order not found')
    ),
    TE.flatMap(validateOrderTE),
    TE.flatMap(processPaymentTE),
    TE.map(generateReceipt)
  )
```

---

## 可读性法则

使用任何 FP 模式之前，问：**"初级开发者能看懂吗？"**

### 过于聪明（避免）

```typescript
const result = pipe(
  data,
  A.filter(flow(prop('status'), equals('active'))),
  A.map(flow(prop('value'), multiply(2))),
  A.reduce(monoid.concat, monoid.empty),
  O.fromPredicate(gt(threshold))
)
```

### 刚刚好（推荐）

```typescript
const activeItems = data.filter(item => item.status === 'active')
const doubledValues = activeItems.map(item => item.value * 2)
const total = doubledValues.reduce((sum, val) => sum + val, 0)
const result = total > threshold ? O.some(total) : O.none
```

### 中间路线（通常最佳）

```typescript
const result = pipe(
  data,
  A.filter(item => item.status === 'active'),
  A.map(item => item.value * 2),
  A.reduce(0, (sum, val) => sum + val),
  total => total > threshold ? O.some(total) : O.none
)
```

---

## 速查表

| 你想要什么 | 大白话 | fp-ts |
|--------------|----------------|-------|
| 处理 null/undefined | "包装这个可空值" | `O.fromNullable(x)` |
| 缺失时给默认值 | "没有就用这个" | `O.getOrElse(() => default)` |
| 有值时转换 | "如果有值，改一下" | `O.map(fn)` |
| 链接可空操作 | "如果有值，试试这个" | `O.flatMap(fn)` |
| 返回成功 | "成了，这是值" | `E.right(value)` |
| 返回失败 | "失败了，这是原因" | `E.left(error)` |
| 包装抛异常的函数 | "试试这个，捕获错误" | `E.tryCatch(fn, onError)` |
| 处理两种情况 | "错误做这个，成功做那个" | `E.fold(onLeft, onRight)` |
| 链接操作 | "然后做这个，再做那个" | `pipe(x, fn1, fn2, fn3)` |

---

## 进阶时机

熟悉这些模式后，可以探索：

1. **TaskEither** - 可失败的异步操作（替代 Promise + try/catch）
2. **Validation** - 收集所有错误而非遇到第一个就停
3. **Reader** - 无需类的依赖注入
4. **Do notation** - 更清晰的多绑定语法

但别急。这里的基础能处理 80% 的真实场景。先熟练这些，再添加更多工具。

---

## 总结

1. **使用 pipe** 处理 3 个以上操作
2. **使用 Option** 处理可空链
3. **使用 Either** 处理可能失败的操作
4. **使用 map** 转换包装值
5. **使用 flatMap** 链接可能失败的操作
6. **跳过 FP** 当它损害可读性时
7. **保持简单** - 团队看不懂的代码不是好代码

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
