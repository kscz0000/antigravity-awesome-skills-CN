---
name: ruby
description: "Ruby 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Ruby：惯用效率参考

## 目录
1. [Enumerable 与集合](#enumerable)
2. [块、Proc 与 Lambda](#blocks)
3. [字符串处理](#strings)
4. [错误处理](#errors)
5. [类与模块](#classes)
6. [Ruby 惯用写法](#idioms)
7. [Ruby 特有反模式](#antipatterns)

---

## 1. Enumerable 与集合 {#enumerable}

```ruby
# ❌ 手动累加
result = []
items.each do |item|
  result << item.name.upcase if item.active?
end

# ✅
result = items.select(&:active?).map { |i| i.name.upcase }
```

```ruby
# ❌ 手动分组
grouped = {}
items.each do |item|
  grouped[item.category] ||= []
  grouped[item.category] << item
end

# ✅
grouped = items.group_by(&:category)
```

```ruby
# ❌ 手动求和
total = 0
orders.each { |o| total += o.amount }

# ✅
total = orders.sum(&:amount)
```

```ruby
# ❌ 检查存在再访问
if hash.key?(key)
  value = hash[key]
end

# ✅
value = hash[key] # 缺失返回 nil
# 或带默认值：
value = hash.fetch(key, default_value)
# 或缺失时抛异常：
value = hash.fetch(key) # 抛 KeyError
```

**优先用 `map`/`select`/`reject`/`sum` 而非手动循环。单方法块用 `&:method`。**

---

## 2. 块、Proc 与 Lambda {#blocks}

```ruby
# ❌ 不必要的显式块转 proc
items.map { |item| item.to_s }

# ✅
items.map(&:to_s)
```

```ruby
# ❌ Proc.new 当 lambda 更安全（元数检查 + return 行为）
handler = Proc.new { |x| x * 2 }

# ✅
handler = ->(x) { x * 2 }
```

```ruby
# ❌ 多行块用 { }
items.map { |item|
  result = transform(item)
  validate(result)
  result
}

# ✅ — 多行用 do/end，单行用 { }
items.map do |item|
  result = transform(item)
  validate(result)
  result
end
```

---

## 3. 字符串处理 {#strings}

```ruby
# ❌ 循环中字符串拼接
result = ""
items.each { |i| result += i.name + ", " }

# ✅
result = items.map(&:name).join(", ")
```

```ruby
# ❌ 字符串拼接组装
greeting = "Hello, " + name + "! You have " + count.to_s + " messages."

# ✅
greeting = "Hello, #{name}! You have #{count} messages."
```

```ruby
# ❌ 可冻结的字符串未冻结（Ruby 3+ 鼓励冻结）
SEPARATOR = ", "

# ✅
SEPARATOR = ", ".freeze
# 或在文件顶部加 `# frozen_string_literal: true`
```

**多行字符串用 heredoc（`<<~HEREDOC`）。`<<~` 会去除缩进。**

---

## 4. 错误处理 {#errors}

```ruby
# ❌ rescue Exception（捕获一切包括 SignalException、SystemExit）
begin
  risky
rescue Exception => e
  log(e)
end

# ✅ — rescue StandardError（默认）
begin
  risky
rescue StandardError => e
  log(e)
  raise
end
# 或：rescue => e（等同于 StandardError）
```

```ruby
# ❌ rescue 当流程控制
begin
  value = hash.fetch(key)
rescue KeyError
  value = default
end

# ✅
value = hash.fetch(key, default)
```

```ruby
# ❌ 内联 rescue 隐藏错误
result = dangerous_operation rescue nil

# ✅ — 内联 rescue 仅用于真正简单的回退
result = Integer(input) rescue nil  # 解析时可接受
```

---

## 5. 类与模块 {#classes}

```ruby
# ❌ 手动访问器
class User
  def name
    @name
  end
  def name=(value)
    @name = value
  end
end

# ✅
class User
  attr_accessor :name
end
```

```ruby
# ❌ 深继承共享行为
class Animal; end
class Pet < Animal; end
class Dog < Pet; end

# ✅ — 共享行为用 mixin，继承用于"是一个"
module Trainable
  def train = puts("Training #{name}")
end

class Dog
  include Trainable
  attr_reader :name
  def initialize(name) = @name = name
end
```

```ruby
# ❌ 只含类方法的类（用类做命名空间）
class MathUtils
  def self.square(x) = x * x
  def self.cube(x) = x ** 3
end

# ✅
module MathUtils
  module_function
  def square(x) = x * x
  def cube(x) = x ** 3
end
```

---

## 6. Ruby 惯用写法 {#idioms}

```ruby
# ❌ 显式布尔返回
def active?
  if status == :active
    true
  else
    false
  end
end

# ✅
def active? = status == :active
```

```ruby
# ❌ 方法调用前 nil 检查
if user && user.name
  puts user.name
end

# ✅ (Ruby 2.3+)
puts user&.name if user&.name
# 或安全导航：
user&.name&.then { |n| puts n }
```

```ruby
# ❌ 冗长条件赋值
if @cache.nil?
  @cache = expensive_compute
end

# ✅
@cache ||= expensive_compute
```

```ruby
# ❌ Multiple assignment from array manually
first = arr[0]
second = arr[1]

# ✅
first, second = arr
```

---

## 7. Ruby 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `rescue Exception` | `rescue StandardError` |
| `for x in collection` | `collection.each` |
| 手动 `attr_reader`/`writer` | `attr_accessor` / `attr_reader` |
| `class` 做纯命名空间 | `module` |
| 字符串拼接用 `+` | 字符串插值 `#{}` |
| `if !condition` | `unless condition` |
| `== true` / `== false` | 直接真假判断 |
| `and`/`or` 做控制流 | `&&`/`||`（优先级不同） |
| 方法末尾 `return` | 隐式返回（最后一个表达式） |
| 生产中猴子补丁核心类 | refinements 或包装 |
| `eval` / `send` 调用已知方法 | 直接方法调用 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
