---
name: fp-react
description: 在 React 中使用 fp-ts 的实用模式——hooks、状态、表单、数据获取。适用于 React 18/19、Next.js 14/15。触发词：fp-ts React、函数式编程 React、Option Either TaskEither、RemoteData、表单验证、数据获取、React 函数式、fp-ts hooks
risk: unknown
source: community
version: 2.0.0
author: fp-ts-skills
tags: [fp-ts, react, typescript, hooks, state-management, forms, data-fetching, remote-data, react-19, next-js]
---

# React 中的函数式编程

React 应用的实用模式。没有术语堆砌，只有能跑的代码。

---

## 快速参考

| 模式 | 使用场景 |
|---------|----------|
| `Option` | 值可能不存在（用户尚未加载） |
| `Either` | 操作可能失败（表单验证） |
| `TaskEither` | 异步操作可能失败（API 调用） |
| `RemoteData` | 需要显示加载/错误/成功状态 |
| `pipe` | 链式组合多个转换 |

---

## 1. 使用 Option 管理状态（可能有，也可能没有）

用 `Option` 替代 `null | undefined`，意图更清晰。

### 基本模式

```typescript
import { useState } from 'react'
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

interface User {
  id: string
  name: string
  email: string
}

function UserProfile() {
  // Option 表示"这可能还不存在"
  const [user, setUser] = useState<O.Option<User>>(O.none)

  const handleLogin = (userData: User) => {
    setUser(O.some(userData))
  }

  const handleLogout = () => {
    setUser(O.none)
  }

  return pipe(
    user,
    O.match(
      // 没有用户时
      () => <button onClick={() => handleLogin({ id: '1', name: 'Alice', email: 'alice@example.com' })}>
        Log In
      </button>,
      // 有用户时
      (u) => (
        <div>
          <p>Welcome, {u.name}!</p>
          <button onClick={handleLogout}>Log Out</button>
        </div>
      )
    )
  )
}
```

### 链式处理可选值

```typescript
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

interface Profile {
  user: O.Option<{
    name: string
    settings: O.Option<{
      theme: string
    }>
  }>
}

function getTheme(profile: Profile): string {
  return pipe(
    profile.user,
    O.flatMap(u => u.settings),
    O.map(s => s.theme),
    O.getOrElse(() => 'light') // 默认值
  )
}
```

---

## 2. 使用 Either 进行表单验证

Either 非常适合验证：`Left` = 错误，`Right` = 有效数据。

### 简单表单验证

```typescript
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Array'
import { pipe } from 'fp-ts/function'

// 验证函数返回 Either<错误消息, 有效值>
const validateEmail = (email: string): E.Either<string, string> =>
  email.includes('@')
    ? E.right(email)
    : E.left('Invalid email address')

const validatePassword = (password: string): E.Either<string, string> =>
  password.length >= 8
    ? E.right(password)
    : E.left('Password must be at least 8 characters')

const validateName = (name: string): E.Either<string, string> =>
  name.trim().length > 0
    ? E.right(name.trim())
    : E.left('Name is required')
```

### 收集所有错误（不只是第一个）

```typescript
import * as E from 'fp-ts/Either'
import { sequenceS } from 'fp-ts/Apply'
import { getSemigroup } from 'fp-ts/NonEmptyArray'
import { pipe } from 'fp-ts/function'

// 这会收集所有错误，不只是第一个
const validateAll = sequenceS(E.getApplicativeValidation(getSemigroup<string>()))

interface SignupForm {
  name: string
  email: string
  password: string
}

interface ValidatedForm {
  name: string
  email: string
  password: string
}

function validateForm(form: SignupForm): E.Either<string[], ValidatedForm> {
  return pipe(
    validateAll({
      name: pipe(validateName(form.name), E.mapLeft(e => [e])),
      email: pipe(validateEmail(form.email), E.mapLeft(e => [e])),
      password: pipe(validatePassword(form.password), E.mapLeft(e => [e])),
    })
  )
}

// 在组件中使用
function SignupForm() {
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [errors, setErrors] = useState<string[]>([])

  const handleSubmit = () => {
    pipe(
      validateForm(form),
      E.match(
        (errs) => setErrors(errs),     // 显示所有错误
        (valid) => {
          setErrors([])
          submitToServer(valid)         // 提交有效数据
        }
      )
    )
  }

  return (
    <form onSubmit={e => { e.preventDefault(); handleSubmit() }}>
      <input
        value={form.name}
        onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
        placeholder="Name"
      />
      <input
        value={form.email}
        onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
        placeholder="Email"
      />
      <input
        type="password"
        value={form.password}
        onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
        placeholder="Password"
      />

      {errors.length > 0 && (
        <ul style={{ color: 'red' }}>
          {errors.map((err, i) => <li key={i}>{err}</li>)}
        </ul>
      )}

      <button type="submit">Sign Up</button>
    </form>
  )
}
```

### 字段级错误（更好的用户体验）

```typescript
type FieldErrors = Partial<Record<keyof SignupForm, string>>

function validateFormWithFieldErrors(form: SignupForm): E.Either<FieldErrors, ValidatedForm> {
  const errors: FieldErrors = {}

  pipe(validateName(form.name), E.mapLeft(e => { errors.name = e }))
  pipe(validateEmail(form.email), E.mapLeft(e => { errors.email = e }))
  pipe(validatePassword(form.password), E.mapLeft(e => { errors.password = e }))

  return Object.keys(errors).length > 0
    ? E.left(errors)
    : E.right({ name: form.name.trim(), email: form.email, password: form.password })
}

// 在组件中
{errors.email && <span className="error">{errors.email}</span>}
```

---

## 3. 使用 TaskEither 进行数据获取

TaskEither = 可能失败的异步操作。非常适合 API 调用。

### 基本获取 Hook

```typescript
import { useState, useEffect } from 'react'
import * as TE from 'fp-ts/TaskEither'
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// 将 fetch 包装为 TaskEither
const fetchJson = <T>(url: string): TE.TaskEither<Error, T> =>
  TE.tryCatch(
    async () => {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      return res.json()
    },
    (err) => err instanceof Error ? err : new Error(String(err))
  )

// 自定义 hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    setError(null)

    pipe(
      fetchJson<T>(url),
      TE.match(
        (err) => {
          setError(err)
          setLoading(false)
        },
        (result) => {
          setData(result)
          setLoading(false)
        }
      )
    )()
  }, [url])

  return { data, error, loading }
}

// 使用示例
function UserList() {
  const { data, error, loading } = useFetch<User[]>('/api/users')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return (
    <ul>
      {data?.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  )
}
```

### 链式 API 调用

```typescript
// 获取用户，然后获取其文章
const fetchUserWithPosts = (userId: string) => pipe(
  fetchJson<User>(`/api/users/${userId}`),
  TE.flatMap(user => pipe(
    fetchJson<Post[]>(`/api/users/${userId}/posts`),
    TE.map(posts => ({ ...user, posts }))
  ))
)
```

### 并行 API 调用

```typescript
import { sequenceT } from 'fp-ts/Apply'

// 同时获取多个资源
const fetchDashboardData = () => pipe(
  sequenceT(TE.ApplyPar)(
    fetchJson<User>('/api/user'),
    fetchJson<Stats>('/api/stats'),
    fetchJson<Notifications[]>('/api/notifications')
  ),
  TE.map(([user, stats, notifications]) => ({
    user,
    stats,
    notifications
  }))
)
```

---

## 4. RemoteData 模式（处理异步状态的正确方式）

停止使用 `{ data, loading, error }` 布尔值。使用正确的状态机。

### 模式定义

```typescript
// RemoteData 恰好有 4 种状态——没有不可能的组合
type RemoteData<E, A> =
  | { _tag: 'NotAsked' }                    // 尚未开始
  | { _tag: 'Loading' }                     // 进行中
  | { _tag: 'Failure'; error: E }           // 失败
  | { _tag: 'Success'; data: A }            // 成功！

// 构造器
const notAsked = <E, A>(): RemoteData<E, A> => ({ _tag: 'NotAsked' })
const loading = <E, A>(): RemoteData<E, A> => ({ _tag: 'Loading' })
const failure = <E, A>(error: E): RemoteData<E, A> => ({ _tag: 'Failure', error })
const success = <E, A>(data: A): RemoteData<E, A> => ({ _tag: 'Success', data })

// 模式匹配所有状态
function fold<E, A, R>(
  rd: RemoteData<E, A>,
  onNotAsked: () => R,
  onLoading: () => R,
  onFailure: (e: E) => R,
  onSuccess: (a: A) => R
): R {
  switch (rd._tag) {
    case 'NotAsked': return onNotAsked()
    case 'Loading': return onLoading()
    case 'Failure': return onFailure(rd.error)
    case 'Success': return onSuccess(rd.data)
  }
}
```

### 使用 RemoteData 的 Hook

```typescript
function useRemoteData<T>(fetchFn: () => Promise<T>) {
  const [state, setState] = useState<RemoteData<Error, T>>(notAsked())

  const execute = async () => {
    setState(loading())
    try {
      const data = await fetchFn()
      setState(success(data))
    } catch (err) {
      setState(failure(err instanceof Error ? err : new Error(String(err))))
    }
  }

  return { state, execute }
}

// 使用示例
function UserProfile({ userId }: { userId: string }) {
  const { state, execute } = useRemoteData(() =>
    fetch(`/api/users/${userId}`).then(r => r.json())
  )

  useEffect(() => { execute() }, [userId])

  return fold(
    state,
    () => <button onClick={execute}>Load User</button>,
    () => <Spinner />,
    (err) => <ErrorMessage message={err.message} onRetry={execute} />,
    (user) => <UserCard user={user} />
  )
}
```

### 为什么 RemoteData 优于布尔值

```typescript
// ❌ 错误：不可能的状态是可能的
interface BadState {
  data: User | null
  loading: boolean
  error: Error | null
}
// 可能出现：{ data: user, loading: true, error: someError }——这是什么意思？！

// ✅ 正确：只存在有效状态
type GoodState = RemoteData<Error, User>
// 只能是：NotAsked | Loading | Failure | Success
```

---

## 5. 引用稳定性（防止重新渲染）

fp-ts 的值如 `O.some(1)` 每次渲染都会创建新对象。React 会认为它们"改变了"。

### 问题所在

```typescript
// ❌ 错误：每次渲染都创建新的 Option
function BadComponent() {
  const [value, setValue] = useState(O.some(1))

  useEffect(() => {
    // 每次渲染都会执行，因为 O.some(1) !== O.some(1)
    console.log('value changed')
  }, [value])
}
```

### 解决方案 1：useMemo

```typescript
// ✅ 正确：记忆化 Option 创建
function GoodComponent() {
  const [rawValue, setRawValue] = useState<number | null>(1)

  const value = useMemo(
    () => O.fromNullable(rawValue),
    [rawValue]  // 只在 rawValue 变化时重新创建
  )

  useEffect(() => {
    // 现在只在 rawValue 实际变化时执行
    console.log('value changed')
  }, [rawValue])  // 依赖原始值，而非 Option
}
```

### 解决方案 2：fp-ts-react-stable-hooks

```bash
npm install fp-ts-react-stable-hooks
```

```typescript
import { useStableO, useStableEffect } from 'fp-ts-react-stable-hooks'
import * as O from 'fp-ts/Option'
import * as Eq from 'fp-ts/Eq'

function StableComponent() {
  // 使用 fp-ts 相等性而非引用相等性
  const [value, setValue] = useStableO(O.some(1))

  // 理解 Option 相等性的 Effect
  useStableEffect(
    () => { console.log('value changed') },
    [value],
    Eq.tuple(O.getEq(Eq.eqNumber))  // 自定义相等性
  )
}
```

---

## 6. 使用 Context 进行依赖注入

使用 ReaderTaskEither 实现可测试的组件，支持注入依赖。

### 设置依赖

```typescript
import * as RTE from 'fp-ts/ReaderTaskEither'
import { pipe } from 'fp-ts/function'
import { createContext, useContext, ReactNode } from 'react'

// 定义应用需要的服务
interface AppDependencies {
  api: {
    getUser: (id: string) => Promise<User>
    updateUser: (id: string, data: Partial<User>) => Promise<User>
  }
  analytics: {
    track: (event: string, data?: object) => void
  }
}

// 创建 context
const DepsContext = createContext<AppDependencies | null>(null)

// Provider
function AppProvider({ deps, children }: { deps: AppDependencies; children: ReactNode }) {
  return <DepsContext.Provider value={deps}>{children}</DepsContext.Provider>
}

// 使用依赖的 hook
function useDeps(): AppDependencies {
  const deps = useContext(DepsContext)
  if (!deps) throw new Error('Missing AppProvider')
  return deps
}
```

### 在组件中使用

```typescript
function UserProfile({ userId }: { userId: string }) {
  const { api, analytics } = useDeps()
  const [user, setUser] = useState<RemoteData<Error, User>>(notAsked())

  useEffect(() => {
    setUser(loading())
    api.getUser(userId)
      .then(u => {
        setUser(success(u))
        analytics.track('user_viewed', { userId })
      })
      .catch(e => setUser(failure(e)))
  }, [userId, api, analytics])

  // 渲染...
}
```

### 使用模拟依赖进行测试

```typescript
const mockDeps: AppDependencies = {
  api: {
    getUser: jest.fn().mockResolvedValue({ id: '1', name: 'Test User' }),
    updateUser: jest.fn().mockResolvedValue({ id: '1', name: 'Updated' }),
  },
  analytics: {
    track: jest.fn(),
  },
}

test('loads user on mount', async () => {
  render(
    <AppProvider deps={mockDeps}>
      <UserProfile userId="1" />
    </AppProvider>
  )

  await screen.findByText('Test User')
  expect(mockDeps.api.getUser).toHaveBeenCalledWith('1')
})
```

---

## 7. React 19 模式

### use() 处理 Promise（React 19+）

```typescript
import { use, Suspense } from 'react'

// 替代 useEffect + useState 进行数据获取
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise)  // 挂起直到解析完成
  return <div>{user.name}</div>
}

// 父组件提供 promise
function App() {
  const userPromise = fetchUser('1')  // 立即开始获取

  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  )
}
```

### useActionState 处理表单（React 19+）

```typescript
import { useActionState } from 'react'
import * as E from 'fp-ts/Either'

interface FormState {
  errors: string[]
  success: boolean
}

async function submitForm(
  prevState: FormState,
  formData: FormData
): Promise<FormState> {
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  // 使用 Either 进行验证
  const result = pipe(
    validateForm(data),
    E.match(
      (errors) => ({ errors, success: false }),
      async (valid) => {
        await saveToServer(valid)
        return { errors: [], success: true }
      }
    )
  )

  return result
}

function SignupForm() {
  const [state, formAction, isPending] = useActionState(submitForm, {
    errors: [],
    success: false
  })

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <input name="password" type="password" />

      {state.errors.map(e => <p key={e} className="error">{e}</p>)}

      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Sign Up'}
      </button>
    </form>
  )
}
```

### useOptimistic 实现即时反馈（React 19+）

```typescript
import { useOptimistic } from 'react'

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, { ...newTodo, pending: true }]
  )

  const addTodo = async (text: string) => {
    const newTodo = { id: crypto.randomUUID(), text, done: false }

    // 立即在 UI 中显示
    addOptimisticTodo(newTodo)

    // 实际保存（完成后会协调）
    await saveTodo(newTodo)
  }

  return (
    <ul>
      {optimisticTodos.map(todo => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </li>
      ))}
    </ul>
  )
}
```

---

## 8. 常用模式速查表

### 基于 Option 渲染

```typescript
// 模式 1：match
pipe(
  maybeUser,
  O.match(
    () => <LoginButton />,
    (user) => <UserMenu user={user} />
  )
)

// 模式 2：fold（与 match 相同）
O.fold(
  () => <LoginButton />,
  (user) => <UserMenu user={user} />
)(maybeUser)

// 模式 3：getOrElse 用于简单默认值
const name = pipe(
  maybeUser,
  O.map(u => u.name),
  O.getOrElse(() => 'Guest')
)
```

### 基于 Either 渲染

```typescript
pipe(
  validationResult,
  E.match(
    (errors) => <ErrorList errors={errors} />,
    (data) => <SuccessMessage data={data} />
  )
)
```

### 安全的数组渲染

```typescript
import * as A from 'fp-ts/Array'

// 安全获取第一个元素
const firstUser = pipe(
  users,
  A.head,
  O.map(user => <Featured user={user} />),
  O.getOrElse(() => <NoFeaturedUser />)
)

// 查找特定元素
const adminUser = pipe(
  users,
  A.findFirst(u => u.role === 'admin'),
  O.map(admin => <AdminBadge user={admin} />),
  O.toNullable  // 或 O.getOrElse(() => null)
)
```

### 条件属性

```typescript
// 仅当值存在时添加属性
const modalProps = {
  isOpen: true,
  ...pipe(
    maybeTitle,
    O.map(title => ({ title })),
    O.getOrElse(() => ({}))
  )
}
```

---

## 何时使用什么

| 场景 | 使用 |
|-----------|-----|
| 值可能不存在 | `Option<T>` |
| 操作可能失败（同步） | `Either<E, A>` |
| 异步操作可能失败 | `TaskEither<E, A>` |
| 需要加载/错误/成功 UI | `RemoteData<E, A>` |
| 多字段验证的表单 | `Either` 配合验证 applicative |
| 依赖注入 | Context + `ReaderTaskEither` |
| 防止 fp-ts 导致的重新渲染 | `useMemo` 或 `fp-ts-react-stable-hooks` |

---

## 相关库

- **[fp-ts](https://github.com/gcanti/fp-ts)** - 核心库
- **[fp-ts-react-stable-hooks](https://github.com/mblink/fp-ts-react-stable-hooks)** - 稳定 hooks
- **[@devexperts/remote-data-ts](https://github.com/devexperts/remote-data-ts)** - RemoteData
- **[io-ts](https://github.com/gcanti/io-ts)** - 运行时类型验证
- **[zod](https://github.com/colinhacks/zod)** - Schema 验证（与 fp-ts 配合良好）

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
