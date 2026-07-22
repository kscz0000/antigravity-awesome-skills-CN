---
name: fp-taskeither-ref
description: >
  TaskEither 速查表。当用户需要异步错误处理、API 调用或可能失败的 Promise 操作时使用。触发词：TaskEither、fp-ts、异步错误处理、Either 链、Promise 包装、TypeScript 函数式。
risk: unknown
source: community
version: 1.0.0
tags: [fp-ts, taskeither, async, promise, error-handling, quick-reference]
---

# TaskEither 速查表

TaskEither = 可能失败的异步操作。类似 `Promise<Either<E, A>>`。

## 何时使用

- 你需要 fp-ts 中可能失败的异步操作的速查。
- 任务涉及 API 调用、Promise 包装或组合异步错误处理流水线。
- 你想要关于 `TaskEither` 操作符和模式的简明速查。

## 创建

```typescript
import * as TE from 'fp-ts/TaskEither'

TE.right(value)          // 异步成功
TE.left(error)           // 异步失败
TE.tryCatch(asyncFn, toError)  // Promise → TaskEither
TE.fromEither(either)    // Either → TaskEither
```

## 转换

```typescript
TE.map(fn)               // 转换成功值
TE.mapLeft(fn)           // 转换错误
TE.flatMap(fn)           // 链式（fn 返回 TaskEither）
TE.orElse(fn)            // 从错误恢复
```

## 执行

```typescript
// TaskEither 是惰性的——必须调用 () 来运行
const result = await myTaskEither()  // Either<E, A>

// 或模式匹配
await pipe(
  myTaskEither,
  TE.match(
    (err) => console.error(err),
    (val) => console.log(val)
  )
)()
```

## 常见模式

```typescript
import { pipe } from 'fp-ts/function'
import * as TE from 'fp-ts/TaskEither'

// 包装 fetch
const fetchUser = (id: string) => TE.tryCatch(
  () => fetch(`/api/users/${id}`).then(r => r.json()),
  (e) => ({ type: 'NETWORK_ERROR', message: String(e) })
)

// 链式异步调用
pipe(
  fetchUser('123'),
  TE.flatMap(user => fetchPosts(user.id)),
  TE.map(posts => posts.length)
)

// 并行调用
import { sequenceT } from 'fp-ts/Apply'
sequenceT(TE.ApplyPar)(
  fetchUser('1'),
  fetchPosts('1'),
  fetchComments('1')
)

// 带恢复
pipe(
  fetchUser('123'),
  TE.orElse(() => TE.right(defaultUser)),
  TE.getOrElse(() => defaultUser)
)
```

## vs async/await

```typescript
// ❌ async/await - 错误被隐藏
async function getUser(id: string) {
  try {
    const res = await fetch(`/api/users/${id}`)
    return await res.json()
  } catch (e) {
    return null  // 错误信息丢失
  }
}

// ✅ TaskEither - 错误类型化且可组合
const getUser = (id: string) => pipe(
  TE.tryCatch(() => fetch(`/api/users/${id}`), toNetworkError),
  TE.flatMap(res => TE.tryCatch(() => res.json(), toParseError))
)
```

当你需要异步操作的**类型化错误**时使用 TaskEither。

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
