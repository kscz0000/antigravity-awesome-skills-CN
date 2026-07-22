---
name: java
description: "Java 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Java：惯用效率参考

## 目录
1. [Stream 与集合](#streams)
2. [Optional](#optional)
3. [记录与数据类](#records)
4. [Switch 表达式](#switch)
5. [并发](#concurrency)
6. [错误处理](#errors)
7. [Java 特有反模式](#antipatterns)

---

## 1. Stream 与集合 {#streams}

```java
// ❌ 命令式累加
List<String> result = new ArrayList<>();
for (Item item : items) {
    if (item.isActive()) result.add(item.getName().toUpperCase());
}

// ✅
List<String> result = items.stream()
    .filter(Item::isActive)
    .map(item -> item.getName().toUpperCase())
    .toList(); // Java 16+；之前用 .collect(Collectors.toList())
```

```java
// ❌ 手动分组
Map<String, List<Item>> grouped = new HashMap<>();
for (Item item : items) {
    grouped.computeIfAbsent(item.getCategory(), k -> new ArrayList<>()).add(item);
}

// ✅
Map<String, List<Item>> grouped = items.stream()
    .collect(Collectors.groupingBy(Item::getCategory));
```

```java
// ❌ 手动求和
int total = 0;
for (Order o : orders) total += o.getAmount();

// ✅
int total = orders.stream().mapToInt(Order::getAmount).sum();
```

**优先用方法引用（`Item::isActive`）而非等价 lambda（`item -> item.isActive()`）。**

---

## 2. Optional {#optional}

```java
// ❌ 空值检查链
String city = null;
if (user != null && user.getAddress() != null) {
    city = user.getAddress().getCity();
}

// ✅
String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse(null);
```

```java
// ❌ Optional.get() 不先检查 isPresent()
String name = optional.get(); // 空时抛异常

// ✅
String name = optional.orElse("default");
// 或：optional.orElseThrow(() -> new IllegalStateException("name required"));
```

```java
// ❌ Optional 作为字段或参数（反模式）
class User { private Optional<String> nickname; }

// ✅ — Optional 只用于返回类型
class User { private String nickname; } // 可空字段
public Optional<String> getNickname() { return Optional.ofNullable(nickname); }
```

---

## 3. 记录与数据类 {#records}

```java
// ❌ 手动 POJO
class Point {
    private final int x, y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int getX() { return x; }
    public int getY() { return y; }
    // + equals, hashCode, toString...
}

// ✅ (Java 16+)
record Point(int x, int y) {}
```

```java
// ❌ 2 个字段的对象用 Builder 模式
User user = new User.Builder().name("Alice").age(30).build();

// ✅ — 小对象直接用 record 或构造函数
record User(String name, int age) {}
var user = new User("Alice", 30);
```

**任何不可变数据载体都用 `record`。Builder 仅保留给多可选字段的对象。**

---

## 4. Switch 表达式 {#switch}

```java
// ❌ switch 语句带 fall-through 和 break
String label;
switch (status) {
    case ACTIVE: label = "Active"; break;
    case INACTIVE: label = "Inactive"; break;
    default: label = "Unknown";
}

// ✅ (Java 14+)
String label = switch (status) {
    case ACTIVE -> "Active";
    case INACTIVE -> "Inactive";
    default -> "Unknown";
};
```

```java
// ❌ instanceof + 转换
if (shape instanceof Circle) {
    Circle c = (Circle) shape;
    return c.radius() * c.radius() * Math.PI;
}

// ✅ 模式匹配 (Java 16+)
if (shape instanceof Circle c) {
    return c.radius() * c.radius() * Math.PI;
}
```

---

## 5. 并发 {#concurrency}

```java
// ❌ 裸 Thread 创建
Thread t = new Thread(() -> doWork());
t.start();

// ✅
ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor(); // Java 21
exec.submit(() -> doWork());
```

```java
// ❌ 对 this 做 synchronized 做细粒度状态
synchronized(this) { counter++; }

// ✅
AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet();
```

**并行异步工作优先用 `CompletableFuture.allOf()` 而非阻塞 `.get()` 链。**

---

## 6. 错误处理 {#errors}

```java
// ❌ 捕获 Exception 只为日志并吞掉
try {
    risky();
} catch (Exception e) {
    log.error("error", e);
}

// ✅ — 无法处理则包装为非受检异常重新抛出
try {
    risky();
} catch (IOException e) {
    throw new UncheckedIOException(e);
}
```

```java
// ❌ 每个方法都声明受检异常
public void process() throws IOException, SQLException, ParseException { ... }

// ✅ — 在边界包装；内部方法抛出非受检异常
```

---

## 7. Java 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `new ArrayList<String>()` (Java 7+) | `new ArrayList<>()`（钻石操作符） |
| `"string".equals(variable)`（尤达风格） | `Objects.equals(variable, "string")` |
| `for (int i = 0; i < list.size(); i++)` | 增强 for 或 stream |
| 单线程代码用 `StringBuffer` | `StringBuilder` |
| `e.printStackTrace()` | `log.error("msg", e)` |
| `null` 返回表示"未找到" | `Optional<T>` 返回类型 |
| 公共字段 | private + 访问器，或 `record` |
| 可变 `static` 字段 | 避免；使用依赖注入 |
| `instanceof` + 转换不用模式匹配 | 模式匹配 (Java 16+) |


## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
