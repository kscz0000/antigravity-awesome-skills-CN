---
name: rust
description: "Rust 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Rust：惯用效率参考

## 目录
1. [所有权与借用](#ownership)
2. [错误处理](#errors)
3. [迭代器](#iterators)
4. [模式匹配](#patterns)
5. [结构体与枚举](#structs)
6. [并发](#concurrency)
7. [Rust 特有反模式](#antipatterns)

---

## 1. 所有权与借用 {#ownership}

```rust
// ❌ 为了避免思考生命周期而 clone
fn get_name(user: &User) -> String {
    user.name.clone()
}

// ✅ — 数据存活足够久时返回引用
fn get_name(user: &User) -> &str {
    &user.name
}
```

```rust
// ❌ 借用即可时获取所有权
fn print_name(name: String) {
    println!("{name}");
}

// ✅
fn print_name(name: &str) {
    println!("{name}");
}
```

```rust
// ❌ 热路径中不必要的 .to_string() / .to_owned()
let key = id.to_string();
map.get(&key)

// ✅ — 利用 Borrow trait；HashMap<String, V> 接受 &str 作为键
map.get(id)
```

**函数参数优先用 `&str` 而非 `String`，除非函数需要拥有数据。**

---

## 2. 错误处理 {#errors}

```rust
// ❌ 生产代码中 .unwrap()
let file = File::open(path).unwrap();

// ✅
let file = File::open(path)
    .map_err(|e| AppError::Io { path: path.to_owned(), source: e })?;
```

```rust
// ❌ 每次调用都手动 match Result
match do_thing() {
    Ok(v) => v,
    Err(e) => return Err(e),
}

// ✅ — ? 运算符
let v = do_thing()?;
```

```rust
// ❌ 到处 Box<dyn Error>（丢失类型信息）
fn run() -> Result<(), Box<dyn std::error::Error>> { ... }

// ✅ — 库错误用 thiserror，应用错误用 anyhow
use anyhow::{Context, Result};
fn run() -> Result<()> {
    do_thing().context("failed during run")?;
    Ok(())
}
```

```rust
// ❌ 每个调用点一个错误枚举变体
enum Error { FileOpen, FileRead, Parse, Network, ... }

// ✅ — 用 thiserror 的 #[from] 自动转换
#[derive(thiserror::Error, Debug)]
enum Error {
    #[error("io error")] Io(#[from] std::io::Error),
    #[error("parse error")] Parse(#[from] serde_json::Error),
}
```

---

## 3. 迭代器 {#iterators}

```rust
// ❌ 命令式累加
let mut result = Vec::new();
for item in &items {
    if item.active {
        result.push(item.name.to_uppercase());
    }
}

// ✅
let result: Vec<_> = items.iter()
    .filter(|i| i.active)
    .map(|i| i.name.to_uppercase())
    .collect();
```

```rust
// ❌ 手动求和
let mut total = 0;
for order in &orders { total += order.amount; }

// ✅
let total: u64 = orders.iter().map(|o| o.amount).sum();
```

```rust
// ❌ 基于索引的循环
for i in 0..items.len() {
    process(&items[i]);
}

// ✅
for item in &items {
    process(item);
}
// 需要索引时：
for (i, item) in items.iter().enumerate() {
    process(i, item);
}
```

**惰性链式迭代器；只在需要具体集合时才 `.collect()`。**

---

## 4. 模式匹配 {#patterns}

```rust
// ❌ 应该用 match 的 if-let 链
if let Some(x) = opt {
    if x > 0 {
        use(x)
    }
}

// ✅
if let Some(x) = opt.filter(|&x| x > 0) {
    use(x)
}
// 或带守卫的 match：
match opt {
    Some(x) if x > 0 => use(x),
    _ => {}
}
```

```rust
// ❌ match 中相同分支
match status {
    Status::Active => true,
    Status::Pending => true,
    Status::Inactive => false,
}

// ✅
matches!(status, Status::Active | Status::Pending)
```

```rust
// ❌ 在函数体中解构而非在模式中
fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(c) => { let r = c.radius; r * r * PI }
        Shape::Rect(r)   => { let w = r.width; let h = r.height; w * h }
    }
}

// ✅ — 在模式中解构
match shape {
    Shape::Circle(Circle { radius, .. }) => radius * radius * PI,
    Shape::Rect(Rect { width, height })  => width * height,
}
```

---

## 5. 结构体与枚举 {#structs}

```rust
// ❌ 枚举变体用 bool 表示二态
enum State { Running(bool) } // true = 暂停？

// ✅ — 显式变体
enum State { Running, Paused, Stopped }
```

```rust
// ❌ 许多 Option 字段的结构体（字符串式可选）
struct Config {
    timeout: Option<u64>,
    retries: Option<u32>,
    base_url: Option<String>,
}

// ✅ — 用 Default + builder 模式或 #[derive(Default)] 搭配合理默认值
#[derive(Default)]
struct Config {
    timeout: u64,      // 默认 0 = 无超时
    retries: u32,      // 默认 0
    base_url: String,
}
```

```rust
// ❌ 需要维护不变量的类型却暴露 pub 字段
pub struct Percentage { pub value: f64 }

// ✅ — 私有字段，构造函数强制不变量
pub struct Percentage(f64);
impl Percentage {
    pub fn new(v: f64) -> Option<Self> {
        (0.0..=100.0).contains(&v).then_some(Self(v))
    }
}
```

---

## 6. 并发 {#concurrency}

```rust
// ❌ 读多数据用 Arc<Mutex<T>>
let data = Arc::new(Mutex::new(vec![...]));

// ✅ — 读多用 RwLock
let data = Arc::new(RwLock::new(vec![...]));
```

```rust
// ❌ 为大量小任务生成 OS 线程
for item in items {
    std::thread::spawn(|| process(item));
}

// ✅ — CPU 密集型并行迭代用 rayon
use rayon::prelude::*;
items.par_iter().for_each(|item| process(item));
```

**异步：优先用 `tokio::spawn` + `JoinHandle` 做结构化并发，而非手动 channel。用 `tokio::join!` 做并发 await。**

---

## 7. Rust 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `.clone()` 哄骗借用检查器 | 重新考虑生命周期或重构 |
| 非测试代码中 `.unwrap()` | `?` 运算符或显式处理 |
| 返回位置 `impl Trait` 隐藏复杂类型 | 命名类型或有意使用 `Box<dyn Trait>` |
| `String` 参数当 `&str` 即可 | 参数用 `&str`，拥有存储用 `String` |
| 嵌套 `Option<Option<T>>` | 重新思考数据模型 |
| `unsafe` 块无安全注释 | 始终记录所维护的不变量 |
| `Vec<Box<T>>` 当 `Vec<T>` 可行 | 除非 T 是 unsized，否则避免集合内堆分配 |
| 手动 `Drop` 做本可由 `?` 处理的清理 | 让 RAII + `?` 来做 |


## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
