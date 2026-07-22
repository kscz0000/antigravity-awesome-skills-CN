---
name: scala
description: "Scala 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Scala：惯用效率参考

## 目录
1. [集合与函数式转换](#collections)
2. [模式匹配](#patterns)
3. [样例类与 ADT](#case-classes)
4. [Option 与错误处理](#option)
5. [隐式与 Given/Using](#implicits)
6. [并发](#concurrency)
7. [Scala 特有反模式](#antipatterns)

---

## 1. 集合与函数式转换 {#collections}

```scala
// ❌ 命令式累加
val result = new ArrayBuffer[String]()
for (item <- items) {
  if (item.isActive) result += item.name.toUpperCase
}

// ✅
val result = items.filter(_.isActive).map(_.name.toUpperCase)
```

```scala
// ❌ 手动分组
val grouped = mutable.Map[String, List[Item]]()
for (item <- items) {
  grouped(item.category) = grouped.getOrElse(item.category, Nil) :+ item
}

// ✅
val grouped = items.groupBy(_.category)
```

```scala
// ❌ 手动折叠当 sum/product 可用
var total = 0
for (o <- orders) total += o.amount

// ✅
val total = orders.map(_.amount).sum
```

```scala
// ❌ 对可能为空的集合用 head
val first = items.head // 空时抛异常

// ✅
val first = items.headOption // 返回 Option[T]
```

```scala
// ❌ 链式 filter + head 做 find
val found = items.filter(_.id == targetId).head

// ✅
val found = items.find(_.id == targetId) // 返回 Option[T]
```

**大集合用 `view` 做惰性求值，避免中间分配。**

---

## 2. 模式匹配 {#patterns}

```scala
// ❌ if-else 链做类型分派
if (shape.isInstanceOf[Circle]) {
  val c = shape.asInstanceOf[Circle]
  c.radius * c.radius * Math.PI
} else if (shape.isInstanceOf[Rect]) { ... }

// ✅
shape match {
  case Circle(r) => r * r * Math.PI
  case Rect(w, h) => w * h
}
```

```scala
// ❌ 嵌套 match 带相同穿透
x match {
  case 1 => "low"
  case 2 => "low"
  case 3 => "mid"
  case _ => "high"
}

// ✅
x match {
  case 1 | 2 => "low"
  case 3     => "mid"
  case _     => "high"
}
```

```scala
// ❌ match 提取再使用
val result = opt match {
  case Some(x) => x.toString
  case None    => "N/A"
}

// ✅
val result = opt.map(_.toString).getOrElse("N/A")
// 或：
val result = opt.fold("N/A")(_.toString)
```

---

## 3. 样例类与 ADT {#case-classes}

```scala
// ❌ 普通类做数据
class User(val name: String, val age: Int) {
  override def equals(obj: Any): Boolean = ...
  override def hashCode(): Int = ...
  override def toString: String = ...
}

// ✅
case class User(name: String, age: Int)
```

```scala
// ❌ 密封 trait 带不相关 case object
sealed trait Result
case class Success(value: Int) extends Result
case class Failure(error: String) extends Result
case object Unknown extends Result // "Unknown" 是什么意思？

// ✅ — 每个变体应携带它所代表的数据
sealed trait Result[+A]
case class Success[A] (value: A) extends Result[A]
case class Failure(error: Throwable) extends Result[Nothing]
```

```scala
// ❌ (Scala 3) 冗长枚举
sealed trait Color
object Color {
  case object Red extends Color
  case object Green extends Color
  case object Blue extends Color
}

// ✅ (Scala 3)
enum Color { case Red, Green, Blue }
```

---

## 4. Option 与错误处理 {#option}

```scala
// ❌ 空值检查
val name: String = if (user != null) user.name else "Unknown"

// ✅
val name = Option(user).map(_.name).getOrElse("Unknown")
```

```scala
// ❌ Option 上 .get（违背初衷）
val name = userOpt.get // None 时抛异常

// ✅
val name = userOpt.getOrElse("default")
// 或：userOpt.map(process).getOrElse(fallback)
// 或：userOpt match { case Some(u) => ... case None => ... }
```

```scala
// ❌ Try 加 .get
val result = Try(parse(input)).get // 失败时抛异常

// ✅
val result = Try(parse(input)) match {
  case Success(v) => v
  case Failure(e) => handleError(e)
}
// 或：Try(parse(input)).getOrElse(default)
// 或：Try(parse(input)).toEither
```

```scala
// ❌ 用异常处理预期失败
def findUser(id: String): User = {
  val user = db.query(id)
  if (user == null) throw new NotFoundException(id)
  user
}

// ✅ — 缺失用 Option，预期错误用 Either
def findUser(id: String): Option[User] = db.query(id)
// 或：
def findUser(id: String): Either[AppError, User]
```

---

## 5. 隐式与 Given/Using {#implicits}

```scala
// ❌ (Scala 2) 隐式转换隐藏 bug
implicit def stringToInt(s: String): Int = s.toInt

// ✅ — 扩展方法替代隐式转换
extension (s: String)
  def toIntSafe: Option[Int] = s.toIntOption
```

```scala
// ❌ (Scala 2) 宽类型隐式参数
def query(sql: String)(implicit conn: Connection): ResultSet

// ✅ (Scala 3)
def query(sql: String)(using conn: Connection): ResultSet
```

```scala
// ❌ 从各处导入隐式
import com.lib.implicits._

// ✅ — 只导入你需要的
import com.lib.given
// 或指定：import com.lib.{given ExecutionContext}
```

---

## 6. 并发 {#concurrency}

```scala
// ❌ 生产代码中 Thread.sleep
Thread.sleep(5000)

// ✅ — 使用调度器 / 定时器抽象
import scala.concurrent.duration._
system.scheduler.scheduleOnce(5.seconds)(doWork())
```

```scala
// ❌ Future 内阻塞
Future {
  val result = blockingHttpCall() // 饿死线程池
  process(result)
}

// ✅
Future {
  blocking { val result = blockingHttpCall() }
  // 或用专用阻塞 ExecutionContext
}
```

```scala
// ❌ 循环中 Await future
for (f <- futures) Await.result(f, Duration.Inf)

// ✅
val all = Future.sequence(futures)
all.map(results => process(results))
```

**优先用 `Future.sequence`/`Future.traverse` 而非手动 await 循环。**

---

## 7. Scala 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| Option/Try 上 `.get` | `.getOrElse` / 模式匹配 |
| `null` | `Option` |
| `isInstanceOf` + `asInstanceOf` | 模式匹配 |
| 隐式转换 (Scala 2) | 扩展方法 (Scala 3) |
| `var` 做累加 | `val` + 函数式转换 |
| `return` 关键字 | 最后一个表达式即返回值 |
| 默认用可变集合 | 不可变集合 |
| `Any` / `AnyRef` 参数 | 带类型边界的泛型 |
| 深层嵌套 `for` 推导 | 拆分为命名值 |
| 元组替代样例类 | 有语义的含义用样例类 |
| 生产中 `Await.result` | 用 `map`/`flatMap` 组合 |




## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
