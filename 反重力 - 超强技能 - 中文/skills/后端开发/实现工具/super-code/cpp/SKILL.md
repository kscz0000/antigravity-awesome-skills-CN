---
name: cpp
description: "C++ 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# C++：惯用效率参考

## 目录
1. [内存与所有权](#memory)
2. [现代类型与容器](#types)
3. [移动语义与引用](#move)
4. [模板与概念](#templates)
5. [错误处理](#errors)
6. [并发](#concurrency)
7. [C++ 特有反模式](#antipatterns)

---

## 1. 内存与所有权 {#memory}

```cpp
// ❌ 裸 new/delete
Widget* w = new Widget();
// ... 15 行之后 ...
delete w;

// ✅
auto w = std::make_unique<Widget>();
```

```cpp
// ❌ 唯一所有权却用 shared
auto w = std::make_shared<Widget>();
transfer(w); // 只有一个所有者

// ✅ — unique_ptr；转移时 move
auto w = std::make_unique<Widget>();
transfer(std::move(w));
```

```cpp
// ❌ new[] 做动态数组
int* arr = new int[n];
// ... 使用 ...
delete[] arr;

// ✅
std::vector<int> arr(n);
```

```cpp
// ❌ 手动 RAII 包装文件/互斥锁
FILE* f = fopen(path, "r");
// ... 必须记住 fclose ...

// ✅
std::ifstream f(path);
// 作用域退出时自动关闭
// 对于非标准资源：unique_ptr 搭配自定义删除器
auto f = std::unique_ptr<FILE, decltype(&fclose)>(fopen(path, "r"), fclose);
```

**规则：如果你输入了 `new`，几乎肯定应该用 `make_unique` 或 `make_shared`。**

---

## 2. 现代类型与容器 {#types}

```cpp
// ❌ C 风格字符串操作
char buf[256];
sprintf(buf, "%s:%d", host, port);

// ✅
auto addr = std::format("{}:{}", host, port); // C++20
// 或：auto addr = host + ":" + std::to_string(port);
```

```cpp
// ❌ 输出参数用于多返回值
void compute(int input, int& result, std::string& error);

// ✅
struct ComputeResult { int value; std::string error; };
ComputeResult compute(int input);
// 或：std::pair / std::tuple 搭配结构化绑定
auto [value, error] = compute(input);
```

```cpp
// ❌ 手动循环查找元素
int idx = -1;
for (int i = 0; i < vec.size(); i++) {
    if (vec[i] == target) { idx = i; break; }
}

// ✅
auto it = std::ranges::find(vec, target); // C++20
// 或：std::find(vec.begin(), vec.end(), target);
```

```cpp
// ❌ 检查 .find() != .end() 再访问
auto it = map.find(key);
if (it != map.end()) { use(it->second); }

// ✅ (C++20)
if (map.contains(key)) { use(map[key]); }
// 或在需要值且避免双重查找时保留迭代器版本
```

**不需要所有权的函数参数使用 `std::string_view`。**

---

## 3. 移动语义与引用 {#move}

```cpp
// ❌ 将大容器拷贝传入函数
void process(std::vector<Data> items) { ... } // 调用时拷贝

// ✅ — 只读用 const 引用，汇入用 move
void process(const std::vector<Data>& items) { ... }  // 只读
void consume(std::vector<Data> items) { ... }          // 汇入：调用方 move 进来
```

```cpp
// ❌ 对 const 对象 std::move（静默拷贝）
const std::string s = "hello";
take(std::move(s)); // 仍然拷贝

// ✅ — 不要 const 你打算 move 的对象
std::string s = "hello";
take(std::move(s));
```

```cpp
// ❌ 从局部变量返回 std::move（阻止 NRVO）
std::vector<int> build() {
    std::vector<int> v;
    // ... 填充 ...
    return std::move(v); // 劣化

// ✅ — 直接返回局部变量；编译器应用 NRVO 或隐式 move
    return v;
}
```

---

## 4. 模板与概念 {#templates}

```cpp
// ❌ SFINAE 汤
template<typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
T square(T x) { return x * x; }

// ✅ (C++20 concepts)
template<std::integral T>
T square(T x) { return x * x; }
```

```cpp
// ❌ 只为一个类型做模板
template<typename T>
void log(T msg) { std::cout << msg; }
// 只用 std::string 调用过

// ✅ — 除非需要多种类型，否则不要模板化
void log(std::string_view msg) { std::cout << msg; }
```

**概念让模板错误可读——优先于 SFINAE 和 static_assert。**

---

## 5. 错误处理 {#errors}

```cpp
// ❌ 通过 int 返回错误码（C++ 中的 C 风格）
int parse(const std::string& input, Data& out);

// ✅ — std::expected (C++23) 或异常
std::expected<Data, ParseError> parse(const std::string& input);
// 或对异常条件 throw
Data parse(const std::string& input); // throws ParseError
```

```cpp
// ❌ 按值捕获（切片派生异常）
try { ... }
catch (std::exception e) { ... }

// ✅
catch (const std::exception& e) { ... }
```

```cpp
// ❌ 析构函数中抛异常
~MyClass() {
    if (cleanup() < 0) throw CleanupError(); // 终止程序

// ✅ — 析构函数必须 noexcept；日志/吞掉错误
~MyClass() noexcept {
    if (cleanup() < 0) log_error("cleanup failed");
}
```

---

## 6. 并发 {#concurrency}

```cpp
// ❌ 手动线程 + join 跟踪
std::thread t(work);
// ... 必须记住 t.join() ...

// ✅ (C++20)
std::jthread t(work); // 析构时自动 join
```

```cpp
// ❌ 手动 lock/unlock
mtx.lock();
data.push_back(item);
mtx.unlock(); // 异常时遗漏

// ✅
{
    std::scoped_lock lock(mtx);
    data.push_back(item);
}
```

```cpp
// ❌ 轮询共享 bool 等待完成
while (!done.load()) { std::this_thread::sleep_for(10ms); }

// ✅ — 使用 std::future 或 condition_variable
auto future = std::async(std::launch::async, compute);
auto result = future.get();
```

**使用 `std::scoped_lock` 而非 `lock_guard`——它处理多个互斥锁并避免死锁。**

---

## 7. C++ 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| 裸 `new`/`delete` | `make_unique` / `make_shared` |
| `(Type)expr` C 风格转换 | `static_cast<Type>(expr)` |
| `#define` 常量 | `constexpr` 变量 |
| `NULL` | `nullptr` |
| 头文件中 `using namespace std;` | 显式 `std::` 前缀 |
| 手动循环做 transform/filter | `std::ranges` 或 `<algorithm>` |
| `std::endl` | `'\n'`（endl 会刷新——慢） |
| `char*` 做字符串参数 | `std::string_view` |
| 异常规范 `throw()` | `noexcept` |
| 继承 `std::` 容器 | 组合，而非继承 |
| `volatile` 用于线程同步 | `std::atomic` |
| 仅头文件的巨型模板 | 编译时间敏感处分离声明/定义 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。