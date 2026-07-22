---
name: typescript
description: "TypeScript 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# TypeScript / JavaScript：惯用效率参考

## 目录
1. [数组与对象操作](#arrays)
2. [解构与展开](#destructuring)
3. [Async / Promise](#async)
4. [函数与闭包](#functions)
5. [TypeScript 类型](#types)
6. [React（如适用）](#react)
7. [TS/JS 特有反模式](#antipatterns)

---

## 1. 数组与对象操作 {#arrays}

```ts
// ❌ 命令式 push 循环
const result: string[] = []
for (const item of items) {
    if (item.active) result.push(item.name.toUpperCase())
}

// ✅
const result = items.filter(i => i.active).map(i => i.name.toUpperCase())
```

```ts
// ❌ 手动 reduce 求和
let total = 0
for (const o of orders) total += o.amount

// ✅
const total = orders.reduce((sum, o) => sum + o.amount, 0)
```

```ts
// ❌ 手动对象拷贝 + 覆盖
const updated = Object.assign({}, user)
updated.name = "Alice"

// ✅
const updated = { ...user, name: "Alice" }
```

```ts
// ❌ 属性访问前做存在性检查
const city = user.address ? user.address.city : undefined

// ✅
const city = user.address?.city
```

---

## 2. 解构与展开 {#destructuring}

```ts
// ❌ 分开变量赋值
const name = user.name
const age = user.age

// ✅
const { name, age } = user
```

```ts
// ❌ 数组元素索引访问
const first = arr[0]
const second = arr[1]

// ✅
const [first, second] = arr
```

```ts
// ❌ 用 concat 合并数组
const merged = a.concat(b).concat(c)

// ✅
const merged = [...a, ...b, ...c]
```

```ts
// ❌ 用 delete 省略键（会修改原对象）
const copy = { ...obj }
delete copy.password

// ✅ — 解构省略
const { password, ...safe } = obj
```

---

## 3. Async / Promise {#async}

```ts
// ❌ Promise 链当 async/await 更清晰
fetchUser(id)
    .then(user => fetchOrders(user.id))
    .then(orders => process(orders))
    .catch(handleError)

// ✅
try {
    const user = await fetchUser(id)
    const orders = await fetchOrders(user.id)
    process(orders)
} catch (e) {
    handleError(e)
}
```

```ts
// ❌ 独立操作顺序 await
const user = await fetchUser(id)
const config = await fetchConfig()

// ✅ — 并行运行
const [user, config] = await Promise.all([fetchUser(id), fetchConfig()])
```

```ts
// ❌ 把已经是异步的函数包在 new Promise 中
const result = await new Promise((resolve) => {
    someAsyncFn().then(resolve)
})

// ✅
const result = await someAsyncFn()
```

**不要在 `.map()` 内 `await` 而不加 `Promise.all`——那会把本该并行的变成顺序执行。**

---

## 4. 函数与闭包 {#functions}

```ts
// ❌ 箭头函数用不必要的块体
const double = (x: number) => { return x * 2 }

// ✅
const double = (x: number) => x * 2
```

```ts
// ❌ 默认参数用 if 守卫
function greet(name?: string) {
    if (!name) name = "World"
    return `Hello, ${name}`
}

// ✅
function greet(name = "World") {
    return `Hello, ${name}`
}
```

```ts
// ❌ 模块作用域内无意义的 IIFE
;(function() {
    const x = compute()
    doSomething(x)
})()

// ✅ — 模块作用域直接写顶层语句
const x = compute()
doSomething(x)
```

---

## 5. TypeScript 类型 {#types}

```ts
// ❌ 推断明显时显式返回类型
function add(a: number, b: number): number {
    return a + b
}

// ✅ — 让 TS 推断简单返回类型
function add(a: number, b: number) {
    return a + b
}
```

```ts
// ❌ any
function process(data: any) { ... }

// ✅ — 用 unknown + 类型守卫，或正确类型/泛型
function process<T extends Record<string, unknown>>(data: T) { ... }
```

```ts
// ❌ 单次使用的内联形状建独立接口
interface UserNameProps { name: string }
function UserName({ name }: UserNameProps) { ... }

// ✅ — 单次使用用内联
function UserName({ name }: { name: string }) { ... }
// 2+ 处复用时再提取接口
```

```ts
// ❌ 类型断言 (as) 压制真实类型错误
const el = document.getElementById("app") as HTMLDivElement
el.innerText = "hi" // el 为 null 时崩溃

// ✅
const el = document.getElementById("app")
if (!(el instanceof HTMLDivElement)) throw new Error("Missing #app")
el.innerText = "hi"
```

**联合/交叉/别名优先用 `type`；可扩展对象形状用 `interface`。**

---

## 6. React（如适用）](#react)

```tsx
// ❌ Effect 做派生状态
const [doubled, setDoubled] = useState(0)
useEffect(() => { setDoubled(count * 2) }, [count])

// ✅ — 渲染时计算
const doubled = count * 2
```

```tsx
// ❌ 默认到处 useCallback
const handler = useCallback(() => doSomething(id), [id])

// ✅ — 仅在传给 memo 子组件或用作 effect 依赖时
// 否则：const handler = () => doSomething(id)
```

```tsx
// ❌ 对象字面量作为 prop（每次渲染新引用）
<Component config={{ debug: true }} />

// ✅
const config = useMemo(() => ({ debug: true }), [])
<Component config={config} />
// 或真正静态时：定义在组件外
const CONFIG = { debug: true }
```

```tsx
// ❌ 可重排/过滤的列表用索引做 key
items.map((item, i) => <Row key={i} {...item} />)

// ✅
items.map(item => <Row key={item.id} {...item} />)
```

---

## 7. TS/JS 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `== null`（松散） | `=== null` 或 `?? / ?.` |
| `typeof x === "undefined"` | `x === undefined` 或 `x == null`（null/undefined 都可时） |
| `!!x` 当布尔隐式转换即可 | `Boolean(x)` 更清晰，或条件中直接用 `x` |
| `var` | 默认 `const`，重新赋值时 `let` |
| 数组用 `for...in` | `for...of` 或数组方法 |
| 无插值的模板字面量 | 普通字符串 `'...'` |
| `console.log` 留在生产代码 | 删除或用 logger |
| `Object.keys(obj).forEach(...)` | `for (const [k, v] of Object.entries(obj))` |
| 超过 2 层嵌套三元 | if/else 或提前返回 |
| `try { ... } catch (e) {}`（静默吞掉） | 日志或重新抛出 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
