---
name: swift
description: "Swift 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Swift：惯用效率参考

## 目录
1. [可选值](#optionals)
2. [集合与函数式转换](#collections)
3. [值类型与引用类型](#value-types)
4. [错误处理](#errors)
5. [并发](#concurrency)
6. [面向协议设计](#protocols)
7. [Swift 特有反模式](#antipatterns)

---

## 1. 可选值 {#optionals}

```swift
// ❌ 强制解包
let name = user.name!

// ✅ — guard 或 if-let
guard let name = user.name else { return }
```

```swift
// ❌ if-let 金字塔
if let user = fetchUser() {
    if let address = user.address {
        if let city = address.city {
            display(city)
        }
    }
}

// ✅ — 链式可选绑定
if let city = fetchUser()?.address?.city {
    display(city)
}
// 或 guard-let 提前退出
guard let city = fetchUser()?.address?.city else { return }
display(city)
```

```swift
// ❌ 三元运算符做默认值
let name = user.name != nil ? user.name! : "Unknown"

// ✅
let name = user.name ?? "Unknown"
```

```swift
// ❌ 副作用用 Optional map（不如 if-let 清晰）
user.name.map { display($0) }

// ✅ — map 用于转换，if-let 用于副作用
let upper = user.name.map { $0.uppercased() }
if let name = user.name { display(name) }
```

---

## 2. 集合与函数式转换 {#collections}

```swift
// ❌ 命令式过滤 + 映射
var result: [String] = []
for item in items {
    if item.isActive { result.append(item.name.uppercased()) }
}

// ✅
let result = items
    .filter(\.isActive)
    .map { $0.name.uppercased() }
```

```swift
// ❌ 手动构建字典
var dict: [String: User] = [:]
for user in users { dict[user.id] = user }

// ✅
let dict = Dictionary(uniqueKeysWithValues: users.map { ($0.id, $0) })
// 或处理可能重复：
let dict = Dictionary(grouping: users, by: \.department)
```

```swift
// ❌ 检查 isEmpty 再访问 first
if !items.isEmpty { process(items[0]) }

// ✅
if let first = items.first { process(first) }
```

```swift
// ❌ 基于索引的循环
for i in 0..<items.count { process(items[i]) }

// ✅
for item in items { process(item) }
// 需要索引时：
for (i, item) in items.enumerated() { process(i, item) }
```

**支持的地方用键路径（`\.isActive`）作为闭包简写。**

---

## 3. 值类型与引用类型 {#value-types}

```swift
// ❌ 纯数据用类（值语义即可时用了引用语义）
class Point {
    var x: Double
    var y: Double
    init(x: Double, y: Double) { self.x = x; self.y = y }
}

// ✅
struct Point { var x, y: Double }
```

```swift
// ❌ 大结构体反复拷贝（性能影响）
struct HugeData { var buffer: [UInt8] /* 数千元素 */ }
func process(_ data: HugeData) { ... } // 拷贝整个缓冲区

// ✅ — 用类或传 inout 做修改
func process(_ data: inout HugeData) { ... }
// 或对大值类型使用写时复制包装
```

**默认用 `struct`。需要标识、继承或引用语义时用 `class`。**

---

## 4. 错误处理 {#errors}

```swift
// ❌ 用可选值掩盖错误
func parse(_ input: String) -> Data? { ... } // 调用方不知道为什么失败

// ✅
func parse(_ input: String) throws -> Data { ... }
```

```swift
// ❌ 生产代码中 try!
let data = try! JSONDecoder().decode(User.self, from: jsonData)

// ✅
do {
    let data = try JSONDecoder().decode(User.self, from: jsonData)
} catch {
    logger.error("decode failed: \(error)")
    throw AppError.decodingFailed(underlying: error)
}
```

```swift
// ❌ 泛型 Error 类型
enum AppError: Error { case generic(String) }

// ✅ — 具体、可操作的错误用例
enum AppError: Error {
    case networkUnreachable
    case invalidInput(field: String, reason: String)
    case unauthorized
}
```

```swift
// ❌ 捕获所有错误并忽略
do { try riskyOperation() } catch { }

// ✅
do {
    try riskyOperation()
} catch let error as NetworkError {
    handleNetworkError(error)
} catch {
    throw error // 重新抛出未知错误
}
```

---

## 5. 并发 {#concurrency}

```swift
// ❌ 回调式异步（末日金字塔）
fetchUser { user in
    fetchPosts(for: user) { posts in
        fetchComments(for: posts.first!) { comments in
            display(comments)
        }
    }
}

// ✅ (Swift 5.5+)
let user = try await fetchUser()
let posts = try await fetchPosts(for: user)
let comments = try await fetchComments(for: posts[0])
display(comments)
```

```swift
// ❌ 独立工作顺序 await
let a = try await fetchA()
let b = try await fetchB()

// ✅
async let a = fetchA()
async let b = fetchB()
let (resultA, resultB) = try await (a, b)
```

```swift
// ❌ 异步上下文中用 DispatchQueue.main.async 更新 UI
DispatchQueue.main.async { label.text = result }

// ✅
await MainActor.run { label.text = result }
// 或标记函数/类 @MainActor
```

**用 `actor` 管理可变共享状态，替代手动锁/队列。**

---

## 6. 面向协议设计 {#protocols}

```swift
// ❌ 深层类继承层次
class Animal { ... }
class Dog: Animal { ... }
class GuideDog: Dog { ... }

// ✅ — 协议 + 组合
protocol Animal { var name: String { get } }
protocol Trainable { func train() }
struct Dog: Animal, Trainable { ... }
```

```swift
// ❌ 协议为所有内容提供默认实现
protocol Renderable {
    func render()
}
extension Renderable {
    func render() { /* 默认 */ }
}
// 每个遵循者都用默认——协议毫无意义

// ✅ — 只对提供真正共享逻辑的情况做默认实现
```

```swift
// ❌ 泛型参数足够时用关联类型
protocol Container {
    associatedtype Element
    func get() -> Element
}

// ✅ — 简单情况用 `some` 或泛型参数
func process(_ item: some Equatable) { ... }
```

---

## 7. Swift 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| 生产代码中强制解包 `!` | `guard let` / `if let` / `??` |
| 测试外 `try!` | `do/catch` |
| 纯数据用 `class` | `struct` |
| 深层继承层次 | 协议组合 |
| 纯 Swift 可行时 `@objc` | 原生 Swift 类型 |
| `NSArray` / `NSDictionary` | `Array` / `Dictionary` |
| async/await 代码中 `DispatchQueue` | `actor` / `MainActor` |
| 隐式解包可选值做字段 | 常规可选值或带 init 的非可选 |
| 到处 `Any` / `AnyObject` | 带协议约束的泛型 |
| 庞大的字符串 `switch` | 带 raw value 的枚举 |
| 单例模式（全局可变状态） | 依赖注入 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
