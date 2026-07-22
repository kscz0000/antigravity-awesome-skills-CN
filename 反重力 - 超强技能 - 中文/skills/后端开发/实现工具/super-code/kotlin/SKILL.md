---
name: kotlin
description: "Kotlin 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Kotlin + Compose：惯用效率参考

## 目录
1. [集合与数据转换](#collections)
2. [空安全](#null-safety)
3. [函数与 Lambda](#functions)
4. [类与对象](#classes)
5. [协程与 Flow](#coroutines)
6. [Compose UI](#compose)
7. [Kotlin 特有反模式](#antipatterns)

---

## 1. 集合与数据转换 {#collections}

**优先用作用域函数和标准库转换而非命令式循环。**

```kotlin
// ❌ 冗长
val result = mutableListOf<String>()
for (item in items) {
    if (item.isActive) {
        result.add(item.name.uppercase())
    }
}

// ✅ 惯用
val result = items.filter { it.isActive }.map { it.name.uppercase() }
```

```kotlin
// ❌ 手动分组
val map = mutableMapOf<String, MutableList<Item>>()
for (item in items) {
    map.getOrPut(item.category) { mutableListOf() }.add(item)
}

// ✅
val map = items.groupBy { it.category }
```

```kotlin
// ❌ 手动折叠
var total = 0
for (order in orders) total += order.amount

// ✅
val total = orders.sumOf { it.amount }
```

**使用 `associate`、`associateBy`、`partition`、`flatMap`、`zip` 替代手动等价写法。**

---

## 2. 空安全 {#null-safety}

```kotlin
// ❌ Elvis 能搞定时不必要的空检查
val name: String
if (user?.name != null) {
    name = user.name
} else {
    name = "Guest"
}

// ✅
val name = user?.name ?: "Guest"
```

```kotlin
// ❌ 双重空检查
if (response != null && response.body != null) {
    process(response.body!!)
}

// ✅
response?.body?.let { process(it) }
```

```kotlin
// ❌ 无防护的 !!
val value = nullable!!.doSomething()

// ✅ 在边界显式声明非空契约
val value = requireNotNull(nullable) { "nullable must be set before calling X" }.doSomething()
// 或提前返回：
val n = nullable ?: return
```

---

## 3. 函数与 Lambda {#functions}

```kotlin
// ❌ 单表达式函数用不必要的块体
fun double(x: Int): Int {
    return x * 2
}

// ✅
fun double(x: Int) = x * 2
```

```kotlin
// ❌ Lambda 捕获未使用的参数
items.forEach { item -> doSomething() }

// ✅
items.forEach { doSomething() }
```

```kotlin
// ❌ 冗余的 with/apply 嵌套
val builder = Builder()
builder.setName("x")
builder.setAge(1)
val result = builder.build()

// ✅
val result = Builder().apply {
    setName("x")
    setAge(1)
}.build()
```

**优先用 `let`、`run`、`apply`、`also`、`with` 替代重复的接收者引用——但嵌套不超过 2 层。**

---

## 4. 类与对象 {#classes}

```kotlin
// ❌ 不可变数据用可变类
class Point {
    var x: Int = 0
    var y: Int = 0
}

// ✅
data class Point(val x: Int, val y: Int)
```

```kotlin
// ❌ 伴生对象仅为持有常量
class Foo {
    companion object {
        val TAG = "Foo"
    }
}

// ✅ — 仅在本文件使用时放在顶层
private const val TAG = "Foo"
class Foo
```

```kotlin
// ❌ 枚举加 when 需要在两处更新
enum class Status { ACTIVE, INACTIVE }
fun label(s: Status) = when(s) { Status.ACTIVE -> "Active"; Status.INACTIVE -> "Inactive" }

// ✅ — 把展示逻辑放在枚举自身
enum class Status(val label: String) { ACTIVE("Active"), INACTIVE("Inactive") }
```

**变体携带不同数据时用密封类/接口而非枚举。**

---

## 5. 协程与 Flow {#coroutines}

```kotlin
// ❌ 不必要的 async/await 对，结果立即使用
val result = async { fetchData() }.await()

// ✅
val result = fetchData() // 直接挂起函数，无需 async
```

```kotlin
// ❌ 循环中 collect
while (true) {
    val value = channel.receive()
    process(value)
}

// ✅
channel.consumeEach { process(it) }
// 或对 Flow：
flow.collect { process(it) }
```

```kotlin
// ❌ StateFlow + 手动 emit 样板
private val _state = MutableStateFlow(initial)
val state: StateFlow<State> = _state
// ... 在多处：_state.value = newValue

// ✅ — 用 update{} 做原子修改
_state.update { it.copy(field = newValue) }
```

**不要在构造函数或 init 块中启动协程。不要使用 GlobalScope。**

---

## 6. Compose UI {#compose}

```kotlin
// ❌ 对计算量小的派生状态做不必要的 remember
val displayName = remember { user.firstName + " " + user.lastName }

// ✅ — 仅在计算昂贵或涉及对象创建时用 remember
val displayName = "${user.firstName} ${user.lastName}"
```

```kotlin
// ❌ 传递整个状态对象，而可组合项只需一个字段
@Composable
fun UserBadge(user: User) { Text(user.name) }

// ✅ — 只传需要的（稳定性 + 最小重组）
@Composable
fun UserBadge(name: String) { Text(name) }
```

```kotlin
// ❌ 内联点击处理 lambda（每次重组创建新实例）
Button(onClick = { viewModel.onSave() }) { ... }

// ✅
val onSave = remember { { viewModel.onSave() } }
Button(onClick = onSave) { ... }
// 或作为参数传入
```

```kotlin
// ❌ 嵌套 Column/Row 仅为了分组子项
Column {
    Column {
        Text("a")
        Text("b")
    }
}

// ✅
Column {
    Text("a")
    Text("b")
}
```

**未知或大尺寸列表用 `LazyColumn`/`LazyRow`。永远不要在无界高度的 `Column` 中放 `LazyColumn`。**

---

## 7. Kotlin 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `if (x == true)` | `if (x)` |
| `if (x == null) return else x!!` | `val x = x ?: return` |
| `listOf().toMutableList()` 创建已知大小列表 | `mutableListOf()` |
| `when` 只有一个分支加 else | `if/else` |
| `.toString()` 作用在字符串上 | 删除它 |
| 函数上显式 `Unit` 返回类型 | 省略（推断） |
| `object : Runnable { override fun run() { ... } }` | `Runnable { ... }`（SAM） |
| 纯 Kotlin 代码中 `@JvmStatic` | 仅 Java 互操作需要 |
| 每个函数都包 try/catch 做日志 | 在边界处理，不在内部 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
