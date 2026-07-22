---
name: php
description: "PHP 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# PHP：惯用效率参考

## 目录
1. [数组与集合](#arrays)
2. [类型安全](#types)
3. [错误处理](#errors)
4. [字符串处理](#strings)
5. [OOP 与现代 PHP](#oop)
6. [函数与闭包](#functions)
7. [PHP 特有反模式](#antipatterns)

---

## 1. 数组与集合 {#arrays}

```php
// ❌ 手动累加
$result = [];
foreach ($items as $item) {
    if ($item->isActive()) {
        $result[] = strtoupper($item->getName());
    }
}

// ✅
$result = array_map(
    fn($i) => strtoupper($i->getName()),
    array_filter($items, fn($i) => $i->isActive())
);
```

```php
// ❌ 手动键值分组
$grouped = [];
foreach ($items as $item) {
    $grouped[$item->getCategory()][] = $item;
}

// ✅ (PHP 8.1+) — 或用上面的循环；PHP 没有内置 groupBy
// foreach 实际上是 PHP 分组的惯用写法。不必强制用 array_*。
```

```php
// ❌ 检查 isset 再访问
if (isset($data['key'])) {
    $value = $data['key'];
} else {
    $value = 'default';
}

// ✅
$value = $data['key'] ?? 'default';
```

```php
// ❌ array_push 加单个元素
array_push($items, $newItem);

// ✅
$items[] = $newItem;
```

**转换用 `array_map`/`array_filter`。当数组函数可读性不如循环时，`foreach` 也完全可以。**

---

## 2. 类型安全 {#types}

```php
// ❌ 无类型声明
function process($items) {
    return $items;
}

// ✅ (PHP 8.0+)
function process(array $items): array {
    return $items;
}
```

```php
// ❌ 联合类型表示可空
function find(string $key): string|null { ... }

// ✅
function find(string $key): ?string { ... }
```

```php
// ❌ 松散比较
if ($value == '0') { ... } // 0、''、false、null 都为 true

// ✅
if ($value === '0') { ... }
```

```php
// ❌ 用 gettype() 做类型检查
if (gettype($x) === 'integer') { ... }

// ✅
if (is_int($x)) { ... }
// 或用联合类型，完全避免检查
```

**每个文件顶部启用 `declare(strict_types=1)`。**

---

## 3. 错误处理 {#errors}

```php
// ❌ 用 @ 抑制错误
$data = @file_get_contents($path);

// ✅
$data = file_get_contents($path);
if ($data === false) {
    throw new RuntimeException("Failed to read: $path");
}
```

```php
// ❌ 捕获 \Exception 并吞掉
try { process(); }
catch (\Exception $e) { /* 静默 */ }

// ✅
try {
    process();
} catch (SpecificException $e) {
    $this->logger->error($e->getMessage(), ['exception' => $e]);
    throw new AppException('Processing failed', previous: $e);
}
```

```php
// ❌ 返回混合类型表示错误
function divide(int $a, int $b): int|false {
    if ($b === 0) return false;
    return intdiv($a, $b);
}

// ✅ — 异常情况抛异常
function divide(int $a, int $b): int {
    if ($b === 0) throw new \DivisionByZeroError();
    return intdiv($a, $b);
}
```

---

## 4. 字符串处理 {#strings}

```php
// ❌ 拼接做变量插值
$msg = 'Hello, ' . $name . '! You have ' . $count . ' messages.';

// ✅
$msg = "Hello, {$name}! You have {$count} messages.";
```

```php
// ❌ 手动字符串包含检查
if (strpos($haystack, $needle) !== false) { ... }

// ✅ (PHP 8.0+)
if (str_contains($haystack, $needle)) { ... }
```

```php
// ❌ substr 做前缀/后缀检查
if (substr($str, 0, 4) === 'http') { ... }
if (substr($str, -4) === '.php') { ... }

// ✅ (PHP 8.0+)
if (str_starts_with($str, 'http')) { ... }
if (str_ends_with($str, '.php')) { ... }
```

---

## 5. OOP 与现代 PHP {#oop}

```php
// ❌ 手动构造函数属性赋值
class User {
    private string $name;
    private int $age;
    public function __construct(string $name, int $age) {
        $this->name = $name;
        $this->age = $age;
    }
}

// ✅ (PHP 8.0+)
class User {
    public function __construct(
        private readonly string $name,
        private readonly int $age,
    ) {}
}
```

```php
// ❌ 类常量当枚举
class Status {
    const ACTIVE = 'active';
    const INACTIVE = 'inactive';
}

// ✅ (PHP 8.1+)
enum Status: string {
    case Active = 'active';
    case Inactive = 'inactive';
}
```

```php
// ❌ instanceof 链
if ($shape instanceof Circle) { ... }
elseif ($shape instanceof Rectangle) { ... }

// ✅ (PHP 8.0+)
$area = match(true) {
    $shape instanceof Circle => $shape->radius ** 2 * M_PI,
    $shape instanceof Rectangle => $shape->width * $shape->height,
    default => throw new \InvalidArgumentException("Unknown shape"),
};
```

```php
// ❌ 静态方法命名构造函数返回 new self()
class Money {
    public static function fromCents(int $cents): self {
        $m = new self();
        $m->cents = $cents;
        return $m;
    }
}

// ✅ (PHP 8.0+) — 构造函数提升 + 命名参数
class Money {
    public function __construct(
        public readonly int $cents,
    ) {}
}
$m = new Money(cents: 500);
```

---

## 6. 函数与闭包 {#functions}

```php
// ❌ 冗长闭包做简单操作
$doubled = array_map(function ($x) { return $x * 2; }, $numbers);

// ✅ (PHP 7.4+)
$doubled = array_map(fn($x) => $x * 2, $numbers);
```

```php
// ❌ 传递全局变量或使用 `global` 关键字
global $db;
function getUser(int $id) {
    global $db;
    return $db->find($id);
}

// ✅ — 依赖注入
function getUser(int $id, PDO $db): ?User {
    return $db->find($id);
}
```

```php
// ❌ Named arguments abused for every call
str_pad(string: $s, length: 10, pad_string: ' ', pad_type: STR_PAD_LEFT);

// ✅ — named args are useful for readability on ambiguous params; don't force
str_pad($s, 10, ' ', STR_PAD_LEFT);
// but named args shine for: new User(name: 'Alice', age: 30)
```

---

## 7. PHP 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `==` 做比较 | `===`（严格相等） |
| `@` 错误抑制 | 显式错误处理 |
| `global` 关键字 | 依赖注入 |
| 对用户输入用 `extract()` | 显式访问键 |
| 库代码中 `die()` / `exit()` | 抛异常 |
| `strpos !== false` 做包含检查 | `str_contains()` (PHP 8.0) |
| 手动构造函数赋值 | 构造函数提升 (PHP 8.0) |
| 类常量做枚举 | `enum` (PHP 8.1) |
| `mixed` 返回类型 | 具体类型化返回 |
| `array` 万能 | 类型化类 / DTO |
| `var_dump` / `print_r` 调试 | 正确日志 (PSR-3) |
| 不用 `declare(strict_types=1)` | 始终启用 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
