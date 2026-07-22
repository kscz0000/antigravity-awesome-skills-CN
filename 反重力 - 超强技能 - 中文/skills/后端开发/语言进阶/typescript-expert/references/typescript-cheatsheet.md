# TypeScript 速查表

## 类型基础

```typescript
// 原始类型
const name: string = 'John'
const age: number = 30
const isActive: boolean = true
const nothing: null = null
const notDefined: undefined = undefined

// 数组
const numbers: number[] = [1, 2, 3]
const strings: Array<string> = ['a', 'b', 'c']

// 元组
const tuple: [string, number] = ['hello', 42]

// 对象
const user: { name: string; age: number } = { name: 'John', age: 30 }

// 联合类型
const value: string | number = 'hello'

// 字面量类型
const direction: 'up' | 'down' | 'left' | 'right' = 'up'

// Any vs Unknown
const anyValue: any = 'anything'     // ❌ 避免
const unknownValue: unknown = 'safe' // ✅ 推荐，需要类型收窄
```

## 类型别名与接口

```typescript
// 类型别名
type Point = {
  x: number
  y: number
}

// 接口（对象推荐使用）
interface User {
  id: string
  name: string
  email?: string  // 可选
  readonly createdAt: Date  // 只读
}

// 继承
interface Admin extends User {
  permissions: string[]
}

// 交叉类型
type AdminUser = User & { permissions: string[] }
```

## 泛型

```typescript
// 泛型函数
function identity<T>(value: T): T {
  return value
}

// 带约束的泛型
function getLength<T extends { length: number }>(item: T): number {
  return item.length
}

// 泛型接口
interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

// 带默认值的泛型
type Container<T = string> = {
  value: T
}

// 多泛型
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 }
}
```

## 工具类型

```typescript
interface User {
  id: string
  name: string
  email: string
  age: number
}

// Partial - 全部可选
type PartialUser = Partial<User>

// Required - 全部必填
type RequiredUser = Required<User>

// Readonly - 全部只读
type ReadonlyUser = Readonly<User>

// Pick - 选取属性
type UserName = Pick<User, 'id' | 'name'>

// Omit - 排除属性
type UserWithoutEmail = Omit<User, 'email'>

// Record - 键值映射
type UserMap = Record<string, User>

// Extract - 从联合类型中提取
type StringOrNumber = string | number | boolean
type OnlyStrings = Extract<StringOrNumber, string>

// Exclude - 从联合类型中排除
type NotString = Exclude<StringOrNumber, string>

// NonNullable - 移除 null/undefined
type MaybeString = string | null | undefined
type DefinitelyString = NonNullable<MaybeString>

// ReturnType - 获取函数返回类型
function getUser() { return { name: 'John' } }
type UserReturn = ReturnType<typeof getUser>

// Parameters - 获取函数参数类型
type GetUserParams = Parameters<typeof getUser>

// Awaited - 解包 Promise
type ResolvedUser = Awaited<Promise<User>>
```

## 条件类型

```typescript
// 基本条件类型
type IsString<T> = T extends string ? true : false

// infer 关键字
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T

// 分布式条件类型
type ToArray<T> = T extends any ? T[] : never
type Result = ToArray<string | number>  // string[] | number[]

// 非分布式
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never
```

## 模板字面量类型

```typescript
type Color = 'red' | 'green' | 'blue'
type Size = 'small' | 'medium' | 'large'

// 组合
type ColorSize = `${Color}-${Size}`
// 'red-small' | 'red-medium' | 'red-large' | ...

// 事件处理器
type EventName = 'click' | 'focus' | 'blur'
type EventHandler = `on${Capitalize<EventName>}`
// 'onClick' | 'onFocus' | 'onBlur'
```

## 映射类型

```typescript
// 基本映射类型
type Optional<T> = {
  [K in keyof T]?: T[K]
}

// 带键重映射
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}

// 过滤键
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
}
```

## 类型守卫

```typescript
// typeof 守卫
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase()  // string
  }
  return value.toFixed(2)  // number
}

// instanceof 守卫
class Dog { bark() {} }
class Cat { meow() {} }

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark()
  } else {
    animal.meow()
  }
}

// in 守卫
interface Bird { fly(): void }
interface Fish { swim(): void }

function move(animal: Bird | Fish) {
  if ('fly' in animal) {
    animal.fly()
  } else {
    animal.swim()
  }
}

// 自定义类型守卫
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

// 断言函数
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== 'string') {
    throw new Error('Not a string')
  }
}
```

## 可辨识联合

```typescript
// 带类型判别符
type Success<T> = { type: 'success'; data: T }
type Error = { type: 'error'; message: string }
type Loading = { type: 'loading' }

type State<T> = Success<T> | Error | Loading

function handle<T>(state: State<T>) {
  switch (state.type) {
    case 'success':
      return state.data  // T
    case 'error':
      return state.message  // string
    case 'loading':
      return null
  }
}

// 穷尽检查
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`)
}
```

## 品牌类型

```typescript
// 创建品牌类型
type Brand<K, T> = K & { __brand: T }

type UserId = Brand<string, 'UserId'>
type OrderId = Brand<string, 'OrderId'>

// 构造函数
function createUserId(id: string): UserId {
  return id as UserId
}

function createOrderId(id: string): OrderId {
  return id as OrderId
}

// 使用 - 防止混用
function getOrder(orderId: OrderId, userId: UserId) {}

const userId = createUserId('user-123')
const orderId = createOrderId('order-456')

getOrder(orderId, userId)  // ✅ 正确
// getOrder(userId, orderId)  // ❌ 错误 - 类型不匹配
```

## 模块声明

```typescript
// 为无类型包声明模块
declare module 'untyped-package' {
  export function doSomething(): void
  export const value: string
}

// 增强已有模块
declare module 'express' {
  interface Request {
    user?: { id: string }
  }
}

// 声明全局
declare global {
  interface Window {
    myGlobal: string
  }
}
```

## TSConfig 要点

```json
{
  "compilerOptions": {
    // 严格性
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    
    // 模块
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    
    // 输出
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    
    // 性能
    "skipLibCheck": true,
    "incremental": true,
    
    // 路径
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 最佳实践

```typescript
// ✅ 对象优先使用 interface
interface User {
  name: string
}

// ✅ 使用 const 断言
const routes = ['home', 'about'] as const

// ✅ 使用 satisfies 进行验证
const config = {
  api: 'https://api.example.com'
} satisfies Record<string, string>

// ✅ 使用 unknown 代替 any
function parse(input: unknown) {
  if (typeof input === 'string') {
    return JSON.parse(input)
  }
}

// ✅ 公共 API 显式声明返回类型
export function getUser(id: string): User | null {
  // ...
}

// ❌ 避免
const data: any = fetchData()
data.anything.goes.wrong  // 无类型安全
```
