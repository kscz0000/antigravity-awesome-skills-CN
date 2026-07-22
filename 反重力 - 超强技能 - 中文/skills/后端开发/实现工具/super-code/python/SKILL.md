---
name: python
description: "Python 语言特定的 super-code 指南。"
risk: safe
source: community
date_added: "2026-06-16"
---
# Python：惯用效率参考

## 目录
1. [推导式与生成器](#comprehensions)
2. [解构与拆包](#unpacking)
3. [内置函数与标准库](#builtins)
4. [函数与默认值](#functions)
5. [类与 dataclass](#classes)
6. [错误处理](#errors)
7. [类型提示](#types)
8. [Python 特有反模式](#antipatterns)

---

## 1. 推导式与生成器 {#comprehensions}

```python
# ❌ 命令式累加
result = []
for item in items:
    if item.active:
        result.append(item.name.upper())

# ✅
result = [item.name.upper() for item in items if item.active]
```

```python
# ❌ 循环中构建字典
d = {}
for k, v in pairs:
    d[k] = v

# ✅
d = dict(pairs)
# 或
d = {k: v for k, v in pairs}
```

```python
# ❌ 生成器不必要地转为列表
total = sum(list(x * 2 for x in nums))

# ✅ — 生成器表达式直接在 sum() 中使用
total = sum(x * 2 for x in nums)
```

**结果只消费一次且不存储时，用生成器表达式（而非列表推导式）。**

---

## 2. 解构与拆包 {#unpacking}

```python
# ❌ 索引访问
first = items[0]
rest = items[1:]

# ✅
first, *rest = items
```

```python
# ❌ 临时变量交换
tmp = a
a = b
b = tmp

# ✅
a, b = b, a
```

```python
# ❌ items() 带单独索引
for i in range(len(items)):
    print(i, items[i])

# ✅
for i, item in enumerate(items):
    print(i, item)
```

```python
# ❌ zip 带单独索引
for i in range(len(a)):
    process(a[i], b[i])

# ✅
for x, y in zip(a, b):
    process(x, y)
```

---

## 3. 内置函数与标准库 {#builtins}

```python
# ❌ 手动最大值搜索
max_val = items[0]
for item in items[1:]:
    if item > max_val:
        max_val = item

# ✅
max_val = max(items)
```

```python
# ❌ 手动分组
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)

# ✅ — 同样的效果，只是对 defaultdict 保持明确；它就是正确的工具
# （这个示例本身已经是正确的——不要用循环替代 defaultdict）
```

```python
# ❌ 字典默认值手动哨兵
if key in d:
    val = d[key]
else:
    val = default

# ✅
val = d.get(key, default)
```

```python
# ❌ 自己写计数器
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1

# ✅
from collections import Counter
counts = Counter(items)
```

**在为组合或流式逻辑写嵌套循环之前，先用 `itertools`（chain、islice、groupby、product）。**

---

## 4. 函数与默认值 {#functions}

```python
# ❌ 可变默认参数（bug，不只是风格）
def append_to(item, lst=[]):
    lst.append(item)
    return lst

# ✅
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

```python
# ❌ 所有参数用位置传参
create_user("Alice", True, False, 30)

# ✅ — 布尔/含糊参数用关键字参数提升可读性
create_user("Alice", is_admin=True, is_active=False, age=30)
```

```python
# ❌ Long function doing multiple things
def process_and_save(data):
    # 40 lines of transform
    # 20 lines of DB write
    ...

# ✅ — split only if each part is reused OR independently testable
def _transform(data): ...
def _save(record): ...
def process_and_save(data): _save(_transform(data))
```

---

## 5. 类与 dataclass {#classes}

```python
# ❌ 数据容器手动 __init__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ✅
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

```python
# ❌ 类仅为持有函数命名空间
class MathUtils:
    @staticmethod
    def add(a, b): return a + b

# ✅ — 模块级函数；类用于状态 + 行为
def add(a, b): return a + b
```

```python
# ❌ __repr__ written manually when dataclass gives it free
# (see above — use @dataclass)
```

**不可变值对象用 `@dataclass(frozen=True)`。需要元组拆包时用 `NamedTuple`。**

---

## 6. 错误处理 {#errors}

```python
# ❌ 裸 except
try:
    risky()
except:
    pass

# ✅ — 捕获特定异常；不要静默吞掉
try:
    risky()
except ValueError as e:
    logger.warning("Invalid value: %s", e)
```

```python
# ❌ LBYL（先看再跳）当 EAFP 更清晰时
if os.path.exists(path):
    with open(path) as f:
        data = f.read()

# ✅ (EAFP)
try:
    with open(path) as f:
        data = f.read()
except FileNotFoundError:
    data = None
```

```python
# ❌ 用 raise e 重新抛出（丢失回溯）
except Exception as e:
    raise e

# ✅
except Exception:
    raise  # 裸 raise 保留原始回溯
```

---

## 7. 类型提示 {#types}

```python
# ❌ 过于冗长的 Union 语法（新代码用 Python <3.10 风格）
from typing import Optional, Union
def f(x: Optional[int]) -> Union[str, None]: ...

# ✅ (Python 3.10+)
def f(x: int | None) -> str | None: ...
```

```python
# ❌ Any 当 TypeVar 或 Protocol 更有信息量
from typing import Any
def first(lst: list[Any]) -> Any: ...

# ✅
from typing import TypeVar
T = TypeVar("T")
def first(lst: list[T]) -> T: ...
```

**不要给每个局部变量加类型提示——注释函数签名和类字段；明显的局部变量让推断即可。**

---

## 8. Python 特有反模式 {#antipatterns}

| 反模式 | 推荐写法 |
|---|---|
| `len(lst) == 0` | `not lst` |
| `if x == True:` | `if x:` |
| `if x == None:` | `if x is None:` |
| `range(len(lst))` 做迭代 | `enumerate(lst)` |
| 循环中字符串拼接 | `"".join(parts)` |
| `import *` | 显式导入 |
| 捕获 `Exception` 日志后重新抛出 | 裸 `raise` 或让它传播 |
| `print()` 做调试输出 | `logging.debug()` |
| `os.path.join` (Python 3.4+) | `pathlib.Path / "subpath"` |
| 值对象手动 `__eq__` + `__hash__` | `@dataclass(eq=True, frozen=True)` |



## 局限性
- 这些是语言特定指南，不涵盖整体架构决策。
- 过度压缩可能降低可读性；请酌情判断。
