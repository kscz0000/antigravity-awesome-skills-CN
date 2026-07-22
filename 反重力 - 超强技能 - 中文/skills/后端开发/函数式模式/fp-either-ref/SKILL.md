---
name: fp-either-ref
description: Either 类型快速参考。当用户需要错误处理、验证或可能失败并带有类型化错误的操作时使用。
risk: unknown
source: community
version: 1.0.0
tags: [fp-ts, either, error-handling, validation, quick-reference]
---

# Either 快速参考

Either = 成功或失败。`Right(值)` 或 `Left(错误)`。

## 何时使用
- 需要类型化同步错误处理的 fp-ts 快速参考。
- 任务涉及验证、可能失败的操作，或将抛出异常的代码转换为 `Either`。
- 想要简洁的速查表而非冗长的教程。

## 创建

```typescript
import * as E from 'fp-ts/Either'

E.right(value)           // 成功
E.left(error)            // 失败
E.fromNullable(err)(x)   // null → Left(err)，否则 Right(x)
E.tryCatch(fn, toError)  // try/catch → Either
```

## 转换

```typescript
E.map(fn)                // 转换 Right 值
E.mapLeft(fn)            // 转换 Left 错误
E.flatMap(fn)            // 链式调用（fn 返回 Either）
E.filterOrElse(pred, toErr) // 如果 pred 失败，Right → Left
```

## 提取

```typescript
E.getOrElse(err => default)  // 获取 Right 或默认值
E.match(onLeft, onRight)     // 模式匹配
E.toUnion(either)            // E | A（丢失类型信息）
```

## 常用模式

```typescript
import { pipe } from 'fp-ts/function'
import * as E from 'fp-ts/Either'

// 验证
const validateEmail = (s: string): E.Either<string, string> =>
  s.includes('@') ? E.right(s) : E.left('Invalid email')

// 链式验证（遇到第一个错误即停止）
pipe(
  E.right({ email: 'test@example.com', age: 25 }),
  E.flatMap(d => pipe(validateEmail(d.email), E.map(() => d))),
  E.flatMap(d => d.age >= 18 ? E.right(d) : E.left('Must be 18+'))
)

// 转换抛出异常的代码
const parseJson = (s: string) => E.tryCatch(
  () => JSON.parse(s),
  (e) => `Parse error: ${e}`
)
```

## vs try/catch

```typescript
// ❌ try/catch - 错误不在类型中
try {
  const data = JSON.parse(input)
  process(data)
} catch (e) {
  handleError(e)
}

// ✅ Either - 错误在类型中显式声明
pipe(
  E.tryCatch(() => JSON.parse(input), String),
  E.map(process),
  E.match(handleError, identity)
)
```

当**错误类型很重要**且需要链式操作时使用 Either。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
