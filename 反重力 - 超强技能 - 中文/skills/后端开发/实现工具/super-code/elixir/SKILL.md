---
name: elixir
description: "Elixir 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Elixir / Erlang：惯用效率参考

## 目录
1. [模式匹配与守卫](#patterns)
2. [管道操作符与转换](#pipes)
3. [进程与 OTP](#otp)
4. [错误处理](#errors)
5. [集合与 Enum](#collections)
6. [结构体与协议](#structs)
7. [Elixir/Erlang 特有反模式](#antipatterns)

---

## 1. 模式匹配与守卫 {#patterns}

```elixir
# ❌ 用 Map.get 提取再检查
value = Map.get(map, :key)
if value != nil do
  process(value)
end

# ✅ — 直接模式匹配
case map do
  %{key: value} -> process(value)
  _ -> :noop
end
# 或用 if：
if value = map[:key], do: process(value)
```

```elixir
# ❌ 嵌套 case 处理多条件
case fetch_user(id) do
  {:ok, user} ->
    case validate(user) do
      {:ok, valid_user} -> save(valid_user)
      {:error, reason} -> {:error, reason}
    end
  {:error, reason} -> {:error, reason}
end

# ✅ — with 子句
with {:ok, user} <- fetch_user(id),
     {:ok, valid_user} <- validate(user) do
  save(valid_user)
end
```

```elixir
# ❌ if/else 处理已知形状
def area(shape) do
  if shape.type == :circle do
    :math.pi() * shape.radius * shape.radius
  else
    shape.width * shape.height
  end
end

# ✅ — 多子句函数搭配模式匹配
def area(%{type: :circle, radius: r}), do: :math.pi() * r * r
def area(%{type: :rect, width: w, height: h}), do: w * h
```

```elixir
# ❌ 运行时类型检查
def process(x) do
  if is_integer(x) and x > 0 do
    x * 2
  end
end

# ✅ — 守卫子句
def process(x) when is_integer(x) and x > 0, do: x * 2
def process(_), do: {:error, :invalid_input}
```

---

## 2. 管道操作符与转换 {#pipes}

```elixir
# ❌ 嵌套函数调用
String.trim(String.downcase(String.replace(input, ~r/\s+/, " ")))

# ✅
input
|> String.replace(~r/\s+/, " ")
|> String.downcase()
|> String.trim()
```

```elixir
# ❌ 别扭地管道传入匿名函数
data
|> (fn x -> x * 2 end).()

# ✅ — 使用 then/1 或命名函数
data
|> then(&(&1 * 2))
# 或更好：提取为命名函数
data |> double()
```

```elixir
# ❌ 单步管道（无可读性收益）
result = list |> Enum.count()

# ✅ — 单操作直接调用
result = Enum.count(list)
```

**2 步以上转换用管道。单操作直接调用。第一个参数通过管道传入。**

---

## 3. 进程与 OTP {#otp}

```elixir
# ❌ 用原始 spawn 做有状态进程
pid = spawn(fn -> loop(%{count: 0}) end)
send(pid, {:increment})

# ✅ — GenServer 做有状态进程
defmodule Counter do
  use GenServer

  def start_link(init \\ 0), do: GenServer.start_link(__MODULE__, init)
  def increment(pid), do: GenServer.call(pid, :increment)

  @impl true
  def init(count), do: {:ok, count}

  @impl true
  def handle_call(:increment, _from, count), do: {:reply, count + 1, count + 1}
end
```

```elixir
# ❌ 无链接的 spawn（崩溃后成为孤儿进程）
spawn(fn -> do_work() end)

# ✅ — Task 做即发即弃并带监督
Task.start(fn -> do_work() end)
# 或做可等待结果：
task = Task.async(fn -> do_work() end)
result = Task.await(task)
```

```elixir
# ❌ 手动进程注册
Process.register(self(), :my_worker)

# ✅ — 使用 Registry 或命名 GenServer
{:ok, _} = Registry.start_link(keys: :unique, name: MyRegistry)
GenServer.start_link(Worker, arg, name: {:via, Registry, {MyRegistry, :my_worker}})
```

```elixir
# ❌ GenServer 中 try/catch（破坏监督）
def handle_call(:work, _from, state) do
  try do
    result = risky_operation()
    {:reply, result, state}
  catch
    _ -> {:reply, :error, state}
  end
end

# ✅ — 让它崩溃；supervisor 会重启
def handle_call(:work, _from, state) do
  result = risky_operation()
  {:reply, result, state}
end
```

**"让它崩溃"——supervisor 负责恢复。不要在 GenServer 内防御性捕获。**

---

## 4. 错误处理 {#errors}

```elixir
# ❌ 对预期失败使用 raise
def find_user(id) do
  case Repo.get(User, id) do
    nil -> raise "User not found"
    user -> user
  end
end

# ✅ — 标记元组用于预期结果
def find_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end
```

```elixir
# ❌ 忽略错误元组
{:ok, result} = might_fail()  # 遇到 {:error, _} 时崩溃

# ✅ — 处理两种情况
case might_fail() do
  {:ok, result} -> process(result)
  {:error, reason} -> Logger.error("Failed: #{inspect(reason)}")
end
```

```elixir
# ❌ 字符串错误
{:error, "something went wrong"}

# ✅ — 原子或结构体错误（可匹配，成本低）
{:error, :timeout}
{:error, %ValidationError{field: :email, reason: :invalid_format}}
```

```elixir
# ❌ ok/error 检查深层嵌套
case step1() do
  {:ok, a} ->
    case step2(a) do
      {:ok, b} ->
        case step3(b) do
          {:ok, c} -> {:ok, c}
          error -> error
        end
      error -> error
    end
  error -> error
end

# ✅
with {:ok, a} <- step1(),
     {:ok, b} <- step2(a),
     {:ok, c} <- step3(b) do
  {:ok, c}
else
  {:error, reason} -> {:error, reason}
end
```

---

## 5. 集合与 Enum {#collections}

```elixir
# ❌ 一次能搞定却做多次遍历
items
|> Enum.filter(&(&1.active))
|> Enum.map(&(&1.name))

# ✅ — for 推导同时过滤和转换
for %{active: true, name: name} <- items, do: name
```

```elixir
# ❌ Enum.count 做空检查（遍历整个列表）
if Enum.count(list) == 0, do: :empty

# ✅
if Enum.empty?(list), do: :empty
# 或模式匹配：
case list do
  [] -> :empty
  _ -> :has_items
end
```

```elixir
# ❌ 用 Enum.reduce 构建映射，Map.new 即可
Enum.reduce(users, %{}, fn user, acc -> Map.put(acc, user.id, user) end)

# ✅
Map.new(users, &{&1.id, &1})
```

```elixir
# ❌ 对大数据集用 Enum（急切——构建中间列表）
huge_list
|> Enum.map(&transform/1)
|> Enum.filter(&valid?/1)
|> Enum.take(10)

# ✅ — Stream 做惰性求值
huge_list
|> Stream.map(&transform/1)
|> Stream.filter(&valid?/1)
|> Enum.take(10)
```

**对大型/无限集合链式转换时用 Stream。小型或最终步骤用 Enum。**

---

## 6. 结构体与协议 {#structs}

```elixir
# ❌ 普通映射做领域实体
user = %{name: "Alice", email: "a@b.com", age: 30}
# 键名拼写错误不会被发现：user.emaail

# ✅ — 结构体强制键名
defmodule User do
  @enforce_keys [:name, :email]
  defstruct [:name, :email, age: 0]
end
user = %User{name: "Alice", email: "a@b.com"}
```

```elixir
# ❌ 只有一个实现的协议（过度抽象）
defprotocol Renderable do
  def render(data)
end
defimpl Renderable, for: HtmlPage do ... end

# ✅ — 直到需要多态之前只用函数
def render(%HtmlPage{} = page), do: ...
```

```elixir
# ❌ 手动更新嵌套结构体
updated = %{user | address: %{user.address | city: "NYC"}}

# ✅
updated = put_in(user.address.city, "NYC")
# 或 Kernel.update_in/3 做转换
```

---

## 7. Elixir/Erlang 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `spawn` 无链接/监控 | `Task.start_link` 或 `GenServer` |
| `try/catch` 在 GenServer 内 | 让它崩溃；supervisor 重启 |
| 字符串错误原因 | 原子或结构体错误 |
| `Enum.count(x) == 0` | `Enum.empty?(x)` 或 `match?([], x)` |
| 可变风格累加器 | `Enum.reduce` / 递归 |
| `if/else` 链处理数据形状 | 多子句函数 + 模式匹配 |
| 嵌套 `case` 处理 ok/error | `with` 表达式 |
| `IO.inspect` 留在生产代码 | `Logger` 带级别 |
| 单步管道 | 直接函数调用 |
| 巨大/无限数据用 `Enum` | `Stream` |
| 裸 PID 传递 | 命名进程 / Registry |
| 布尔返回表示成功/失败 | `{:ok, val}` / `{:error, reason}` 元组 |
| `length(list) > 0` (O(n)) | 模式匹配 `[_ \| _]` |
| 通过 ETS 无包装的共享可变状态 | GenServer 或 Agent 作为访问层 |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
