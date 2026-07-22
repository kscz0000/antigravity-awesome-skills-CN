---
name: go
description: "Go 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Go：惯用效率参考

## 目录
1. [错误处理](#errors)
2. [切片与映射](#slices)
3. [Goroutine 与 Channel](#concurrency)
4. [结构体与接口](#structs)
5. [函数与闭包](#functions)
6. [Go 特有反模式](#antipatterns)

---

## 1. 错误处理 {#errors}

```go
// ❌ 忽略错误
result, _ := os.Open(path)

// ✅ — 始终处理；只在错误确实无关时使用 _
result, err := os.Open(path)
if err != nil {
    return fmt.Errorf("open %s: %w", path, err)
}
```

```go
// ❌ 冗余错误变量
err := doA()
if err != nil { return err }
err = doB()
if err != nil { return err }

// ✅ — 每个 :=/: 都没问题；这是惯用 Go。不必"修复"。
// 可以简化的是：if 体只有单条 return 时合为一行
if err := doA(); err != nil { return err }
if err := doB(); err != nil { return err }
```

```go
// ❌ 无附加值的自定义错误类型
type MyError struct{ msg string }
func (e MyError) Error() string { return e.msg }

// ✅ — 除非调用方需要检查类型，否则用 errors.New 或 fmt.Errorf
var ErrNotFound = errors.New("not found")
return fmt.Errorf("lookup %q: %w", key, ErrNotFound)
```

**用 `%w`（而非 `%v`）包装错误，以便调用方使用 `errors.Is` / `errors.As`。**

---

## 2. 切片与映射 {#slices}

```go
// ❌ 已知大小时不预分配
var result []string
for _, item := range items {
    result = append(result, item.Name)
}

// ✅
result := make([]string, 0, len(items))
for _, item := range items {
    result = append(result, item.Name)
}
```

```go
// ❌ 映射写入前手动存在性检查
if _, ok := m[key]; !ok {
    m[key] = []string{}
}
m[key] = append(m[key], value)

// ✅ — append 到 nil 切片在 Go 中合法
m[key] = append(m[key], value)
```

```go
// ❌ 赋值复制映射（复制引用）
copy := original

// ✅
copy := make(map[K]V, len(original))
for k, v := range original { copy[k] = v }
```

---

## 3. Goroutine 与 Channel {#concurrency}

```go
// ❌ 即发即忘的 goroutine 无生命周期管理
go doWork()

// ✅ — 用 errgroup 或 WaitGroup 跟踪完成
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    doWork()
}()
wg.Wait()
```

```go
// ❌ 无缓冲 channel 造成不必要的 goroutine 阻塞
ch := make(chan Result)
go func() { ch <- compute() }()
result := <-ch

// ✅ — 单结果时，缓冲 channel 避免接收方提前退出时的 goroutine 泄漏
ch := make(chan Result, 1)
go func() { ch <- compute() }()
result := <-ch
```

```go
// ❌ select 带忙等待 default
for {
    select {
    case v := <-ch:
        process(v)
    default:
        // 自旋
    }
}

// ✅ — 阻塞 select 除非你确实需要非阻塞
for v := range ch {
    process(v)
}
```

**用 `golang.org/x/sync/errgroup` 做扇出并收集错误。**

---

## 4. 结构体与接口 {#structs}

```go
// ❌ 大接口
type Storage interface {
    Get(key string) ([]byte, error)
    Set(key string, val []byte) error
    Delete(key string) error
    List(prefix string) ([]string, error)
    // ... 还有 10 个方法
}

// ✅ — 小而可组合的接口
type Getter interface { Get(key string) ([]byte, error) }
type Setter interface { Set(key string, val []byte) error }
type Storage interface { Getter; Setter }
```

```go
// ❌ 构造函数返回具体结构体（将调用方绑定到实现）
func NewStore() *RedisStore { ... }

// ✅ — 当已有或预期多种实现时返回接口
func NewStore() Storage { return &RedisStore{...} }
```

```go
// ❌ 小值类型用指针接收者
func (p *Point) X() float64 { return p.x }

// ✅ — 小的不可变类型用值接收者
func (p Point) X() float64 { return p.x }
```

**规则：方法修改状态或结构体较大（>3 个非平凡字段）时用指针接收者。否则用值接收者。**

---

## 5. 函数与闭包 {#functions}

```go
// ❌ 命名返回值仅为避免变量声明
func divide(a, b float64) (result float64, err error) {
    result = a / b
    return
}

// ✅ — 命名返回值仅用于延迟修改或文档时才值得
func divide(a, b float64) (float64, error) {
    if b == 0 { return 0, errors.New("division by zero") }
    return a / b, nil
}
```

```go
// ❌ 闭包捕获循环变量（经典 Go bug，Go 1.22+ 已修复）
// 1.22 前：每个 goroutine 捕获同一个 i
for i := 0; i < n; i++ {
    go func() { use(i) }()
}

// ✅ (Go <1.22 — 作为参数传入)
for i := 0; i < n; i++ {
    go func(i int) { use(i) }(i)
}
// Go 1.22+：循环变量每次迭代独立作用域，原始写法安全
```

---

## 6. Go 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `if err != nil { return err }` 重复 5+ 次 | 可接受——这是惯用 Go |
| `panic` 用于预期错误 | `return err` |
| `init()` 带副作用 | 在 `main` 或构造函数中显式初始化 |
| `interface{}` / `any` 不用泛型 | 使用泛型 (Go 1.18+) 或类型化接口 |
| Mutex 字段不在其保护的数据旁 | 把 `mu` 直接放在它守护的字段上方 |
| Channel 的 channel | 通常是过度工程化的标志；重新设计 |
| 测试中 `time.Sleep` | 用 `testing` 钩子或 channel 同步 |
| 导出类型含未导出字段（当字段是全部意义时） | `record` 风格结构体，全部导出字段 |
| `log.Fatal` 在 `main` 之外 | 将错误返回到调用栈 |


## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。