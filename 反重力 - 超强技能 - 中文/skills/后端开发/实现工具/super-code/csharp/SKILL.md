---
name: csharp
description: "C# 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# C#：惯用效率参考

## 目录
1. [LINQ 与集合](#linq)
2. [空值处理](#nulls)
3. [Async/Await](#async)
4. [记录与模式匹配](#records)
5. [错误处理](#errors)
6. [资源管理](#resources)
7. [C# 特有反模式](#antipatterns)

---

## 1. LINQ 与集合 {#linq}

```csharp
// ❌ 命令式累加
var result = new List<string>();
foreach (var item in items) {
    if (item.IsActive) result.Add(item.Name.ToUpper());
}

// ✅
var result = items
    .Where(i => i.IsActive)
    .Select(i => i.Name.ToUpper())
    .ToList();
```

```csharp
// ❌ 手动分组
var grouped = new Dictionary<string, List<Item>>();
foreach (var item in items) {
    if (!grouped.ContainsKey(item.Category))
        grouped[item.Category] = new List<Item>();
    grouped[item.Category].Add(item);
}

// ✅
var grouped = items.GroupBy(i => i.Category)
    .ToDictionary(g => g.Key, g => g.ToList());
```

```csharp
// ❌ 检查 Any() 再 First()
if (items.Any(i => i.IsValid)) {
    var first = items.First(i => i.IsValid);
}

// ✅
var first = items.FirstOrDefault(i => i.IsValid);
if (first is not null) { ... }
```

**2 个以上操作的链式调用优先用方法语法。复杂 join 可用查询语法。**

---

## 2. 空值处理 {#nulls}

```csharp
// ❌ 嵌套空值检查
string city = null;
if (user != null && user.Address != null) {
    city = user.Address.City;
}

// ✅
var city = user?.Address?.City;
```

```csharp
// ❌ 三元运算符做空值回退
var name = user != null ? user.Name : "Unknown";

// ✅
var name = user?.Name ?? "Unknown";
```

```csharp
// ❌ 空值检查后再触发事件
if (OnChanged != null) OnChanged(this, args);

// ✅
OnChanged?.Invoke(this, args);
```

```csharp
// ❌ 手动抛出 ArgumentNullException
if (name == null) throw new ArgumentNullException(nameof(name));

// ✅ (C# 10+)
ArgumentNullException.ThrowIfNull(name);
```

**项目全局启用可空引用类型（`<Nullable>enable</Nullable>`）。**

---

## 3. Async/Await {#async}

```csharp
// ❌ 阻塞异步代码
var result = GetDataAsync().Result; // 死锁风险

// ✅
var result = await GetDataAsync();
```

```csharp
// ❌ async void（异常不可观察）
async void OnButtonClick() { await DoWork(); }

// ✅ — async Task；只有真正需要的事件处理器才用 async void
async Task OnButtonClick() { await DoWork(); }
```

```csharp
// ❌ 独立工作顺序 await
var a = await FetchA();
var b = await FetchB();

// ✅
var (a, b) = (await Task.WhenAll(FetchA(), FetchB())) switch
{
    var r => (r[0], r[1])
};
// 或用 ValueTuple 更清晰：
var taskA = FetchA();
var taskB = FetchB();
var a = await taskA;
var b = await taskB;
```

```csharp
// ❌ 在库中用 Task.Run 包装同步代码
public Task<int> GetValue() => Task.Run(() => ComputeSync());

// ✅ — 让调用方决定；暴露同步方法
public int GetValue() => ComputeSync();
```

**库代码添加 `ConfigureAwait(false)`。应用/UI 代码省略。**

---

## 4. 记录与模式匹配 {#records}

```csharp
// ❌ 数据类型手动实现相等、ToString、Deconstruct
class Point {
    public int X { get; init; }
    public int Y { get; init; }
    // + Equals, GetHashCode, ToString...
}

// ✅ (C# 9+)
record Point(int X, int Y);
```

```csharp
// ❌ if-else 链做类型检查
if (shape is Circle) {
    var c = (Circle)shape;
    return c.Radius * c.Radius * Math.PI;
} else if (shape is Rectangle) { ... }

// ✅
return shape switch {
    Circle { Radius: var r } => r * r * Math.PI,
    Rectangle { Width: var w, Height: var h } => w * h,
    _ => throw new ArgumentException($"Unknown shape: {shape}")
};
```

```csharp
// ❌ 用 && 做范围检查
if (score >= 0 && score <= 100) { ... }

// ✅ (C# 9+)
if (score is >= 0 and <= 100) { ... }
```

---

## 5. 错误处理 {#errors}

```csharp
// ❌ 捕获 Exception 只为日志并吞掉
try { Process(); }
catch (Exception ex) { logger.LogError(ex, "error"); }

// ✅ — 捕获特定异常，无法处理则重新抛出
try { Process(); }
catch (HttpRequestException ex) {
    throw new ServiceException("upstream failure", ex);
}
```

```csharp
// ❌ throw ex（重置堆栈跟踪）
catch (Exception ex) { throw ex; }

// ✅
catch (Exception ex) { throw; } // 保留堆栈跟踪
// 或包装：throw new AppException("context", ex);
```

```csharp
// ❌ 用异常做流程控制
try { return dict[key]; }
catch (KeyNotFoundException) { return defaultValue; }

// ✅
return dict.TryGetValue(key, out var value) ? value : defaultValue;
```

---

## 6. 资源管理 {#resources}

```csharp
// ❌ 手动 Dispose
var conn = new SqlConnection(cs);
conn.Open();
// ... 使用 conn ...
conn.Dispose(); // 异常时遗漏

// ✅
using var conn = new SqlConnection(cs);
conn.Open();
// 作用域结束时释放
```

```csharp
// ❌ 冗长的 using 块
using (var reader = new StreamReader(path)) {
    return reader.ReadToEnd();
}

// ✅ (C# 8+)
using var reader = new StreamReader(path);
return reader.ReadToEnd();
// 或直接：return File.ReadAllText(path);
```

---

## 7. C# 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `string.Format("{0}", x)` | `$"{x}"` 字符串插值 |
| `List<T>` 作为公共 API 返回 | `IReadOnlyList<T>` 或 `IEnumerable<T>` |
| `async void` | `async Task` |
| `.Result` / `.Wait()` 对 Task | `await` |
| `throw ex` | `throw`（保留堆栈跟踪） |
| 数据类型手动 `IEquatable` | `record` |
| `object` 参数 | 带约束的泛型 |
| `DateTime.Now` | `DateTime.UtcNow` 或 `DateTimeOffset` |
| 可变公共字段 | `{ get; set; }` 或 `{ get; init; }` 属性 |
| `catch (Exception) { }`（吞掉所有） | 捕获特定异常，未知异常重新抛出 |
| `IDisposable` 不加 `using` | `using` 声明 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。