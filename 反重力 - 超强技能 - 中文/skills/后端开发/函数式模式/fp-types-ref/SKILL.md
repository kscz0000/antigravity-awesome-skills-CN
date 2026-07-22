---
name: fp-types-ref
description: fp-ts 类型快速参考。当用户询问该使用哪个类型、需要 Option/Either/Task 决策帮助，或想要 fp-ts 导入时使用。
risk: safe
source: community
version: 1.0.0
tags: [fp-ts, typescript, quick-reference, option, either, task]
---

# fp-ts 快速参考

## 何时使用
- 需要帮助在 `Option`、`Either`、`Task`、`TaskEither` 或相关 fp-ts 类型之间做选择。
- 任务涉及导入、决策指导，或为 TypeScript 流程选择合适的抽象。
- 想要一份常见 fp-ts 类型选择和模式的紧凑参考。

## 我该用哪个类型？

```
操作是异步的吗？
├─ 否：涉及错误吗？
│   ├─ 是 → Either<Error, Value>
│   └─ 否：值可能缺失吗？
│       ├─ 是 → Option<Value>
│       └─ 否 → 直接用值
└─ 是：涉及错误吗？
    ├─ 是 → TaskEither<Error, Value>
    └─ 否：值可能缺失吗？
        ├─ 是 → TaskOption<Value>
        └─ 否 → Task<Value>
```

## 常用导入

```typescript
// Core
import { pipe, flow } from 'fp-ts/function'

// Types
import * as O from 'fp-ts/Option'      // Maybe exists
import * as E from 'fp-ts/Either'      // Success or failure
import * as TE from 'fp-ts/TaskEither' // Async + failure
import * as T from 'fp-ts/Task'        // Async (no failure)
import * as A from 'fp-ts/Array'       // Array utilities
```

## 单行模式

| 需求 | 代码 |
|------|------|
| 包装可空值 | `O.fromNullable(value)` |
| 默认值 | `O.getOrElse(() => default)` |
| 存在时转换 | `O.map(fn)` |
| 链式可选值 | `O.flatMap(fn)` |
| 包装 try/catch | `E.tryCatch(() => risky(), toError)` |
| 包装异步 | `TE.tryCatch(() => fetch(url), toError)` |
| 执行管道 | `pipe(value, fn1, fn2, fn3)` |

## 模式匹配

```typescript
// Option
pipe(maybe, O.match(
  () => 'nothing',
  (val) => `got ${val}`
))

// Either
pipe(result, E.match(
  (err) => `error: ${err}`,
  (val) => `success: ${val}`
))
```

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
