---
name: fp-pipe-ref
description: pipe 和 flow 快速参考。当用户需要链式调用函数、组合操作或在 fp-ts 中构建数据管道时使用。触发词：pipe、flow、函数组合、数据管道、fp-ts、链式调用、函数式编程。
risk: unknown
source: community
version: 1.0.0
tags: [fp-ts, pipe, flow, composition, quick-reference]
---

# pipe 与 flow 快速参考

## pipe - 转换值

```typescript
import { pipe } from 'fp-ts/function'

// pipe(初始值, fn1, fn2, fn3)
// = fn3(fn2(fn1(初始值)))

const result = pipe(
  '  hello world  ',
  s => s.trim(),
  s => s.toUpperCase(),
  s => s.split(' ')
)
// ['HELLO', 'WORLD']
```

## flow - 创建可复用管道

```typescript
import { flow } from 'fp-ts/function'

// flow(fn1, fn2, fn3) 返回一个新函数
const process = flow(
  (s: string) => s.trim(),
  s => s.toUpperCase(),
  s => s.split(' ')
)

process('  hello world  ') // ['HELLO', 'WORLD']
process('  foo bar  ')     // ['FOO', 'BAR']
```

## 使用场景
| 使用 | 场景 |
|-----|------|
| `pipe` | 立即转换特定值 |
| `flow` | 创建可复用的转换函数 |

## 配合 fp-ts 类型使用

```typescript
import * as O from 'fp-ts/Option'
import * as A from 'fp-ts/Array'

// Option 链式调用
pipe(
  O.fromNullable(user),
  O.map(u => u.email),
  O.getOrElse(() => 'no email')
)

// 数组链式调用
pipe(
  users,
  A.filter(u => u.active),
  A.map(u => u.name)
)
```

## 常见模式

```typescript
// 数据后置支持偏函数应用
const getActiveNames = flow(
  A.filter((u: User) => u.active),
  A.map(u => u.name)
)

// 可在任意位置复用
getActiveNames(users1)
getActiveNames(users2)
```

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不应替代环境特定的验证、测试或专家审查。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
