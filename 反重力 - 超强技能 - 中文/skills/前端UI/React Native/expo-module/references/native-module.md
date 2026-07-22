# 原生模块 DSL 参考

Swift 作为首选语言展示。Kotlin 遵循相同的 DSL 结构（参见 SKILL.md 中两者对比）。在 Kotlin 语法有显著差异时，会单独注明。

## Name

设置在 JavaScript 中使用的模块标识符。

```swift
Name("MyModule")
```

## Constant

首次访问时计算一次，然后缓存。

```swift
Constant("PI") { 3.14159 }
```

## Function（同步）

在完成前阻塞 JS 线程。最多支持 8 个参数。

```swift
Function("add") { (a: Int, b: Int) -> Int in
  return a + b
}
```

## AsyncFunction

返回 Promise。默认在后台线程运行。

```swift
AsyncFunction("fetchData") { (url: URL) -> String in
  let data = try Data(contentsOf: url)
  return String(data: data, encoding: .utf8) ?? ""
}

// 强制在主队列执行
AsyncFunction("updateUI") { () -> Void in
  // UI 操作
}.runOnQueue(.main)
```

**Kotlin 差异：**

```kotlin
// 支持 Kotlin 协程
AsyncFunction("fetchData") Coroutine { url: java.net.URL ->
  withContext(Dispatchers.IO) {
    url.readText()
  }
}
```

## Property

用于 JS 对象属性的 getter/setter。

```swift
// 只读
Property("version") { "1.0.0" }

// 读写
Property("volume")
  .get { () -> Float in self.volume }
  .set { (newValue: Float) in self.volume = newValue }
```

## Events

声明模块可以向 JS 发送的事件。必须在使用 `sendEvent` 之前声明。

```swift
// 声明
Events("onChange", "onError")

// 从原生发送（Swift）
sendEvent("onChange", ["value": newValue])
```

**Kotlin 差异** —— 使用 `bundleOf`：

```kotlin
sendEvent("onChange", bundleOf("value" to newValue))
```

**JS 订阅：**

```typescript
import { useEvent } from "expo";
import MyModule from "./MyModule";

// 基于 Hook（推荐）
const event = useEvent(MyModule, "onChange");

// 手动订阅
const subscription = MyModule.addListener("onChange", (event) => {
  console.log(event.value);
});
// 清理：subscription.remove()
```

### OnStartObserving / OnStopObserving

在第一个监听器附加 / 最后一个监听器分离时调用。可以限定到特定事件。

```swift
OnStartObserving("onChange") {
  // 开始产生事件
}

OnStopObserving("onChange") {
  // 停止产生事件
}
```

---

## 类型系统

### 基本类型

| Swift | Kotlin | JS |
|-------|--------|----|
| `Bool` | `Boolean` | `boolean` |
| `Int`, `Int32` | `Int` | `number` |
| `Int64` | `Long` | `number` |
| `Float`, `Float32` | `Float` | `number` |
| `Double` | `Double` | `number` |
| `String` | `String` | `string` |
| `URL` | `java.net.URL` / `android.net.Uri` | `string` |
| `CGPoint` | - | `{ x, y }` |
| `CGSize` | - | `{ width, height }` |
| `CGRect` | - | `{ x, y, width, height }` |
| `UIColor` / `CGColor` | `android.graphics.Color` | `string`（ProcessedColorValue） |
| `Data` | `kotlin.ByteArray` | `Uint8Array` |

### Records（类结构体类型）

```swift
struct UserRecord: Record {
  @Field var name: String = ""
  @Field var age: Int = 0
  @Field var email: String?
}

Function("createUser") { (user: UserRecord) -> Bool in
  return true
}
```

**Kotlin 差异** —— 使用 `class` 而非 `struct`，可空字段需要显式的 `= null`：

```kotlin
class UserRecord : Record {
  @Field var name: String = ""
  @Field var age: Int = 0
  @Field var email: String? = null
}
```

### Enums（Enumerable）

```swift
enum Theme: String, Enumerable {
  case light
  case dark
  case system
}

Function("setTheme") { (theme: Theme) in
  // 类型安全的枚举值
}
```

**Kotlin 差异** —— 使用 `enum class` 并显式提供 `value` 属性：

```kotlin
enum class Theme(val value: String) : Enumerable {
  LIGHT("light"),
  DARK("dark"),
  SYSTEM("system")
}
```

### Either 类型（联合类型）

```swift
Function("process") { (input: Either<String, Int>) in
  if let str = input.get(String.self) {
    // 处理字符串
  } else if let num = input.get(Int.self) {
    // 处理数字
  }
}
```

同样可用：`EitherOfThree<A, B, C>`、`EitherOfFour<A, B, C, D>`。

### JavaScript 值（直接 JS 操作）

用于在 JS 线程上运行的同步函数中的高级用法：

```swift
Function("callback") { (fn: JavaScriptFunction<String>) in
  let result = fn("arg1", "arg2")
}
```

---

## Shared Objects

将原生类实例桥接到 JS，并具备自动生命周期管理。当 JS 与原生代码都不持有引用时，实例会被释放。

### 定义 Shared Object

```swift
class ImageContext: SharedObject {
  private var image: UIImage

  init(image: UIImage) {
    self.image = image
    super.init()
  }

  func rotate(degrees: Double) {
    image = image.rotated(degrees: degrees)
  }
}
```

**Kotlin 差异** —— 构造函数接收 `RuntimeContext`，重写 `sharedObjectDidRelease()` 进行清理：

```kotlin
class ImageContext(
  runtimeContext: RuntimeContext,
  private var bitmap: Bitmap
) : SharedObject(runtimeContext) {

  fun rotate(degrees: Float) { /* ... */ }

  override fun sharedObjectDidRelease() {
    if (!bitmap.isRecycled) bitmap.recycle()
  }
}
```

### 通过 Class DSL 暴露

```swift
Class("Context", ImageContext.self) {
  Constructor { (path: String) -> ImageContext in
    return ImageContext(image: UIImage(contentsOfFile: path)!)
  }

  Function("rotate") { (ctx: ImageContext, degrees: Double) -> ImageContext in
    ctx.rotate(degrees: degrees)
    return ctx
  }

  Property("width")
    .get { (ctx: ImageContext) -> Int in ctx.width }
}
```

其他 Class DSL 组件：`StaticFunction`、`StaticAsyncFunction`、`AsyncFunction`。

### SharedRef

用于在模块之间传递类型化对象的专用 shared reference：

```swift
final class ImageRef: SharedRef<UIImage> {}
```

### JS 用法

```typescript
const ctx = await ImageModule.create("/path/to/image.png");
ctx.rotate(90);
console.log(ctx.width);
```