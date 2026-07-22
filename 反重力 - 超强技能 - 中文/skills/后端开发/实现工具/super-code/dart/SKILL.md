---
name: dart
description: "Dart 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Dart：惯用效率参考

## 目录
1. [空安全](#nulls)
2. [集合与迭代](#collections)
3. [类与记录](#classes)
4. [Async/Await 与 Stream](#async)
5. [错误处理](#errors)
6. [Flutter 特有模式](#flutter)
7. [Dart 特有反模式](#antipatterns)

---

## 1. 空安全 {#nulls}

```dart
// ❌ 手动空值检查
String display;
if (user.name != null) {
  display = user.name!;
} else {
  display = 'Unknown';
}

// ✅
final display = user.name ?? 'Unknown';
```

```dart
// ❌ 嵌套空值检查
if (user != null && user.address != null && user.address!.city != null) {
  print(user.address!.city!);
}

// ✅
final city = user?.address?.city;
if (city != null) print(city);
```

```dart
// ❌ 可空类型更合适时用 late
late String name; // 赋值前访问会崩溃

// ✅ — 只在保证初始化先于访问时用 late
String? name; // 真正可空
// late 适合：late final _controller = TextEditingController();
```

```dart
// ❌ 到处用 bang 运算符 (!)
final name = user.name!;
final city = user.address!.city!;

// ✅ — 通过空值检查提升类型
final name = user.name;
if (name == null) return;
// name 现在是非空（已提升）
```

---

## 2. 集合与迭代 {#collections}

```dart
// ❌ 命令式累加
final result = <String>[];
for (final item in items) {
  if (item.isActive) result.add(item.name.toUpperCase());
}

// ✅
final result = items
    .where((i) => i.isActive)
    .map((i) => i.name.toUpperCase())
    .toList();
```

```dart
// ❌ 手动构建映射
final map = <String, List<Item>>{};
for (final item in items) {
  map.putIfAbsent(item.category, () => []).add(item);
}

// ✅（用 collection-if/for 不同方式——但 groupBy 非内置）
// 上面的循环实际上就是 Dart 惯用写法。用 package:collection 的 groupBy：
import 'package:collection/collection.dart';
final map = groupBy(items, (Item i) => i.category);
```

```dart
// ❌ 用 add() 调用构建列表
final widgets = <Widget>[];
widgets.add(Header());
if (showSubtitle) widgets.add(Subtitle());
widgets.add(Body());

// ✅ — collection-if
final widgets = [
  Header(),
  if (showSubtitle) Subtitle(),
  Body(),
];
```

```dart
// ❌ 手动展开
final all = <int>[];
all.addAll(listA);
all.addAll(listB);

// ✅
final all = [...listA, ...listB];
```

---

## 3. 类与记录 {#classes}

```dart
// ❌ 手动数据类样板
class Point {
  final int x, y;
  const Point(this.x, this.y);
  @override bool operator ==(Object other) => ...
  @override int get hashCode => ...
  @override String toString() => 'Point($x, $y)';
}

// ✅ (Dart 3.0+)
typedef Point = ({int x, int y});
// 或需要命名类语义时：
class Point {
  final int x, y;
  const Point(this.x, this.y);
}
// 用 package:equatable 或 Dart 记录做相等判断
```

```dart
// ❌ 冗长构造函数
class User {
  final String name;
  final int age;
  User(String name, int age) : name = name, age = age;
}

// ✅ — 初始化形式参数
class User {
  final String name;
  final int age;
  const User(this.name, this.age);
}
```

```dart
// ❌ 不可变对象上的可变字段
class Config {
  String host;
  int port;
  Config(this.host, this.port);
}

// ✅
class Config {
  final String host;
  final int port;
  const Config(this.host, this.port);
}
```

```dart
// ❌ if-else 链按类型 switch
if (shape is Circle) {
  return (shape as Circle).radius * pi;
} else if (shape is Rectangle) { ... }

// ✅ (Dart 3.0+)
return switch (shape) {
  Circle(:final radius) => radius * radius * pi,
  Rectangle(:final width, :final height) => width * height,
};
```

---

## 4. Async/Await 与 Stream {#async}

```dart
// ❌ .then() 链
fetchUser()
    .then((user) => fetchPosts(user))
    .then((posts) => display(posts))
    .catchError((e) => log(e));

// ✅
try {
  final user = await fetchUser();
  final posts = await fetchPosts(user);
  display(posts);
} catch (e) {
  log(e);
}
```

```dart
// ❌ 独立工作顺序 await
final a = await fetchA();
final b = await fetchB();

// ✅
final results = await Future.wait([fetchA(), fetchB()]);
// 或带类型解构：
final (a, b) = await (fetchA(), fetchB()).wait; // Dart 3.0+ record
```

```dart
// ❌ StreamBuilder 在 build 中做太多
StreamBuilder(
  stream: stream,
  builder: (ctx, snap) {
    if (snap.hasError) return Error();
    if (!snap.hasData) return Loading();
    final data = snap.data!;
    // 50 行 widget 树...
  },
)

// ✅ — 提取 widget，或简单场景用 listen + setState
```

---

## 5. 错误处理 {#errors}

```dart
// ❌ 捕获 Exception（太宽泛）
try { process(); }
on Exception catch (e) { print(e); }

// ✅ — 捕获特定类型
try {
  process();
} on FormatException catch (e) {
  throw AppException('Invalid format', cause: e);
} on HttpException catch (e) {
  throw AppException('Network error', cause: e);
}
```

```dart
// ❌ 出错时返回 null
Future<User?> fetchUser() async {
  try { return await api.getUser(); }
  catch (_) { return null; } // 调用方不知道原因
}

// ✅ — 让异常传播，或使用 sealed Result 类型
sealed class Result<T> {}
class Success<T> extends Result<T> { final T value; Success(this.value); }
class Failure<T> extends Result<T> { final Object error; Failure(this.error); }
```

---

## 6. Flutter 特有模式 {#flutter}

```dart
// ❌ 状态变更时重建整棵树
setState(() {
  // 只改一个值，但 build() 方法构建 200 个 widget
});

// ✅ — 将子树提取为独立 widget 或使用 ValueListenableBuilder
ValueListenableBuilder<int>(
  valueListenable: counter,
  builder: (_, value, __) => Text('$value'),
)
```

```dart
// ❌ 可 const 的 widget 不加 const
Container(color: Colors.blue)

// ✅
const ColoredBox(color: Colors.blue)
// 构造函数尽可能标记 const；调用处使用 `const` 关键字
```

```dart
// ❌ 到处用 Navigator.push + MaterialPageRoute
Navigator.push(context, MaterialPageRoute(builder: (_) => DetailPage()));

// ✅ — 命名路由或 GoRouter
context.go('/detail');
```

---

## 7. Dart 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| 随意使用 `!` bang 运算符 | 空值检查和类型提升 |
| 到处 `dynamic` | 正确类型 |
| 不检查就 `as` 转换 | 模式匹配或 `is` 检查 |
| 值对象的可变字段 | `final` 字段 |
| `print()` 做日志 | `package:logging` 或结构化日志 |
| 手动 `==`/`hashCode` | 记录、equatable 或代码生成 |
| 复杂状态用 `setState` | Riverpod / Bloc / Provider |
| 深层 widget 嵌套 | 提取为 widget 类 |
| 基于字符串的路由 | 类型化路由 (GoRouter) |
| `late` 当逃生舱 | 可空类型或正确初始化 |
| `Future.delayed` 做防抖 | `Timer` 或专用防抖工具 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。