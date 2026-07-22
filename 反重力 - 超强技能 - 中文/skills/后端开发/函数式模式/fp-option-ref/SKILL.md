---
name: fp-option-ref
description: Option 类型快速参考。处理可空值、可选数据或避免 null 检查时使用。当用户要求处理 Option、可空值、fp-ts Option 参考时使用。
risk: unknown
source: community
version: 1.0.0
tags: [fp-ts, option, nullable, maybe, quick-reference]
---

# Option 快速参考

Option = 可能不存在的值。`Some(value)` 或 `None`。

## 使用场景

- 需要 fp-ts 可空值或可选值的快速参考
- 任务涉及消除 null 检查、安全属性访问或使用 `Option` 进行可选链
- 需要简短的参考卡片而非完整迁移指南

## 创建

```typescript
import * as O from 'fp-ts/Option'

O.some(5)              // Some(5)
O.none                 // None
O.fromNullable(x)      // null/undefined → None，否则 Some(x)
O.fromPredicate(x > 0)(x) // false → None，true → Some(x)
```

## 转换

```typescript
O.map(fn)              // 转换内部值
O.flatMap(fn)          // 链式 Option（fn 返回 Option）
O.filter(predicate)    // 断言为 false 时返回 None
```

## 提取

```typescript
O.getOrElse(() => default)  // 获取值或默认值
O.toNullable(opt)           // 转回 T | null
O.toUndefined(opt)          // 转回 T | undefined
O.match(onNone, onSome)     // 模式匹配
```

## 常用模式

```typescript
import { pipe } from 'fp-ts/function'
import * as O from 'fp-ts/Option'

// 安全属性访问
pipe(
  O.fromNullable(user),
  O.map(u => u.profile),
  O.flatMap(p => O.fromNullable(p.avatar)),
  O.getOrElse(() => '/default-avatar.png')
)

// 数组首个元素
import * as A from 'fp-ts/Array'
pipe(
  users,
  A.head,  // Option<User>
  O.map(u => u.name),
  O.getOrElse(() => 'No users')
)
```

## vs Nullable

```typescript
// ❌ Nullable - 容易忘记检查
const name = user?.profile?.name ?? 'Guest'

// ✅ Option - 显式、可组合
pipe(
  O.fromNullable(user),
  O.flatMap(u => O.fromNullable(u.profile)),
  O.map(p => p.name),
  O.getOrElse(() => 'Guest')
)
```

需要**链式**处理可选值时使用 Option。

## 限制

- 仅在任务明确符合上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，停止并请求澄清
