# Python 性能优化实现手册

本文件包含本技能引用的详细模式、检查清单和代码示例。

# Python 性能优化

全面的 Python 代码性能分析与优化指南，包括 CPU 分析、内存优化和实现最佳实践。

## 何时使用本技能

- 识别 Python 应用程序中的性能瓶颈
- 降低应用程序延迟和响应时间
- 优化 CPU 密集型操作
- 减少内存消耗和内存泄漏
- 提升数据库查询性能
- 优化 I/O 操作
- 加速数据处理管道
- 实现高性能算法
- 分析生产环境应用程序

## 核心概念

### 1. 分析类型
- **CPU 分析**：识别耗时的函数
- **内存分析**：跟踪内存分配和泄漏
- **行级分析**：以逐行粒度进行分析
- **调用图**：可视化函数调用关系

### 2. 性能指标
- **执行时间**：操作耗时
- **内存使用**：峰值和平均内存消耗
- **CPU 利用率**：处理器使用模式
- **I/O 等待**：在 I/O 操作上花费的时间

### 3. 优化策略
- **算法**：更好的算法和数据结构
- **实现**：更高效的代码模式
- **并行化**：多线程/多进程
- **缓存**：避免冗余计算
- **原生扩展**：关键路径上的 C/Rust

## 快速上手

### 基本计时

```python
import time

def measure_time():
    """简单计时测量。"""
    start = time.time()

    # 你的代码
    result = sum(range(1000000))

    elapsed = time.time() - start
    print(f"Execution time: {elapsed:.4f} seconds")
    return result

# 更好：使用 timeit 进行精确测量
import timeit

execution_time = timeit.timeit(
    "sum(range(1000000))",
    number=100
)
print(f"Average time: {execution_time/100:.6f} seconds")
```

## 分析工具

### 模式 1：cProfile - CPU 分析

```python
import cProfile
import pstats
from pstats import SortKey

def slow_function():
    """要分析的函数。"""
    total = 0
    for i in range(1000000):
        total += i
    return total

def another_function():
    """另一个函数。"""
    return [i**2 for i in range(100000)]

def main():
    """要分析的主函数。"""
    result1 = slow_function()
    result2 = another_function()
    return result1, result2

# 分析代码
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # 打印统计
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(10)  # 前 10 个函数

    # 保存到文件供后续分析
    stats.dump_stats("profile_output.prof")
```

**命令行分析：**
```bash
# 分析脚本
python -m cProfile -o output.prof script.py

# 查看结果
python -m pstats output.prof
# 在 pstats 中：
# sort cumtime
# stats 10
```

### 模式 2：line_profiler - 逐行分析

```python
# 安装：pip install line-profiler

# 添加 @profile 装饰器（由 line_profiler 提供）
@profile
def process_data(data):
    """使用行分析处理数据。"""
    result = []
    for item in data:
        processed = item * 2
        result.append(processed)
    return result

# 运行：
# kernprof -l -v script.py
```

**手动行分析：**
```python
from line_profiler import LineProfiler

def process_data(data):
    """要分析的函数。"""
    result = []
    for item in data:
        processed = item * 2
        result.append(processed)
    return result

if __name__ == "__main__":
    lp = LineProfiler()
    lp.add_function(process_data)

    data = list(range(100000))

    lp_wrapper = lp(process_data)
    lp_wrapper(data)

    lp.print_stats()
```

### 模式 3：memory_profiler - 内存使用

```python
# 安装：pip install memory-profiler

from memory_profiler import profile

@profile
def memory_intensive():
    """使用大量内存的函数。"""
    # 创建大列表
    big_list = [i for i in range(1000000)]

    # 创建大字典
    big_dict = {i: i**2 for i in range(100000)}

    # 处理数据
    result = sum(big_list)

    return result

if __name__ == "__main__":
    memory_intensive()

# 运行：
# python -m memory_profiler script.py
```

### 模式 4：py-spy - 生产环境分析

```bash
# 安装：pip install py-spy

# 分析正在运行的 Python 进程
py-spy top --pid 12345

# 生成火焰图
py-spy record -o profile.svg --pid 12345

# 分析脚本
py-spy record -o profile.svg -- python script.py

# 转储当前调用栈
py-spy dump --pid 12345
```

## 优化模式

### 模式 5：列表推导式 vs 循环

```python
import timeit

# 慢：传统循环
def slow_squares(n):
    """使用循环创建平方数列表。"""
    result = []
    for i in range(n):
        result.append(i**2)
    return result

# 快：列表推导式
def fast_squares(n):
    """使用推导式创建平方数列表。"""
    return [i**2 for i in range(n)]

# 基准测试
n = 100000

slow_time = timeit.timeit(lambda: slow_squares(n), number=100)
fast_time = timeit.timeit(lambda: fast_squares(n), number=100)

print(f"Loop: {slow_time:.4f}s")
print(f"Comprehension: {fast_time:.4f}s")
print(f"Speedup: {slow_time/fast_time:.2f}x")

# 对于简单操作更快：map
def faster_squares(n):
    """使用 map 获得更好性能。"""
    return list(map(lambda x: x**2, range(n)))
```

### 模式 6：用于内存的生成器表达式

```python
import sys

def list_approach():
    """内存密集型列表。"""
    data = [i**2 for i in range(1000000)]
    return sum(data)

def generator_approach():
    """内存高效的生成器。"""
    data = (i**2 for i in range(1000000))
    return sum(data)

# 内存比较
list_data = [i for i in range(1000000)]
gen_data = (i for i in range(1000000))

print(f"List size: {sys.getsizeof(list_data)} bytes")
print(f"Generator size: {sys.getsizeof(gen_data)} bytes")

# 生成器使用恒定内存，与大小无关
```

### 模式 7：字符串拼接

```python
import timeit

def slow_concat(items):
    """慢速字符串拼接。"""
    result = ""
    for item in items:
        result += str(item)
    return result

def fast_concat(items):
    """使用 join 进行快速字符串拼接。"""
    return "".join(str(item) for item in items)

def faster_concat(items):
    """使用列表更快。"""
    parts = [str(item) for item in items]
    return "".join(parts)

items = list(range(10000))

# 基准测试
slow = timeit.timeit(lambda: slow_concat(items), number=100)
fast = timeit.timeit(lambda: fast_concat(items), number=100)
faster = timeit.timeit(lambda: faster_concat(items), number=100)

print(f"Concatenation (+): {slow:.4f}s")
print(f"Join (generator): {fast:.4f}s")
print(f"Join (list): {faster:.4f}s")
```

### 模式 8：字典查找 vs 列表搜索

```python
import timeit

# 创建测试数据
size = 10000
items = list(range(size))
lookup_dict = {i: i for i in range(size)}

def list_search(items, target):
    """列表中的 O(n) 搜索。"""
    return target in items

def dict_search(lookup_dict, target):
    """字典中的 O(1) 搜索。"""
    return target in lookup_dict

target = size - 1  # 列表的最坏情况

# 基准测试
list_time = timeit.timeit(
    lambda: list_search(items, target),
    number=1000
)
dict_time = timeit.timeit(
    lambda: dict_search(lookup_dict, target),
    number=1000
)

print(f"List search: {list_time:.6f}s")
print(f"Dict search: {dict_time:.6f}s")
print(f"Speedup: {list_time/dict_time:.0f}x")
```

### 模式 9：局部变量访问

```python
import timeit

# 全局变量（慢）
GLOBAL_VALUE = 100

def use_global():
    """访问全局变量。"""
    total = 0
    for i in range(10000):
        total += GLOBAL_VALUE
    return total

def use_local():
    """使用局部变量。"""
    local_value = 100
    total = 0
    for i in range(10000):
        total += local_value
    return total

# 局部变量更快
global_time = timeit.timeit(use_global, number=1000)
local_time = timeit.timeit(use_local, number=1000)

print(f"Global access: {global_time:.4f}s")
print(f"Local access: {local_time:.4f}s")
print(f"Speedup: {global_time/local_time:.2f}x")
```

### 模式 10：函数调用开销

```python
import timeit

def calculate_inline():
    """内联计算。"""
    total = 0
    for i in range(10000):
        total += i * 2 + 1
    return total

def helper_function(x):
    """辅助函数。"""
    return x * 2 + 1

def calculate_with_function():
    """使用函数调用的计算。"""
    total = 0
    for i in range(10000):
        total += helper_function(i)
    return total

# 内联更快，因为没有调用开销
inline_time = timeit.timeit(calculate_inline, number=1000)
function_time = timeit.timeit(calculate_with_function, number=1000)

print(f"Inline: {inline_time:.4f}s")
print(f"Function calls: {function_time:.4f}s")
```

## 高级优化

### 模式 11：用于数值运算的 NumPy

```python
import timeit
import numpy as np

def python_sum(n):
    """使用纯 Python 求和。"""
    return sum(range(n))

def numpy_sum(n):
    """使用 NumPy 求和。"""
    return np.arange(n).sum()

n = 1000000

python_time = timeit.timeit(lambda: python_sum(n), number=100)
numpy_time = timeit.timeit(lambda: numpy_sum(n), number=100)

print(f"Python: {python_time:.4f}s")
print(f"NumPy: {numpy_time:.4f}s")
print(f"Speedup: {python_time/numpy_time:.2f}x")

# 向量化运算
def python_multiply():
    """Python 中的逐元素乘法。"""
    a = list(range(100000))
    b = list(range(100000))
    return [x * y for x, y in zip(a, b)]

def numpy_multiply():
    """NumPy 中的向量化乘法。"""
    a = np.arange(100000)
    b = np.arange(100000)
    return a * b

py_time = timeit.timeit(python_multiply, number=100)
np_time = timeit.timeit(numpy_multiply, number=100)

print(f"\nPython multiply: {py_time:.4f}s")
print(f"NumPy multiply: {np_time:.4f}s")
print(f"Speedup: {py_time/np_time:.2f}x")
```

### 模式 12：使用 functools.lru_cache 进行缓存

```python
from functools import lru_cache
import timeit

def fibonacci_slow(n):
    """无缓存的递归斐波那契。"""
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

@lru_cache(maxsize=None)
def fibonacci_fast(n):
    """有缓存的递归斐波那契。"""
    if n < 2:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)

# 递归算法大幅加速
n = 30

slow_time = timeit.timeit(lambda: fibonacci_slow(n), number=1)
fast_time = timeit.timeit(lambda: fibonacci_fast(n), number=1000)

print(f"Without cache (1 run): {slow_time:.4f}s")
print(f"With cache (1000 runs): {fast_time:.4f}s")

# 缓存信息
print(f"Cache info: {fibonacci_fast.cache_info()}")
```

### 模式 13：使用 __slots__ 节省内存

```python
import sys

class RegularClass:
    """使用 __dict__ 的常规类。"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SlottedClass:
    """使用 __slots__ 节省内存的类。"""
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# 内存比较
regular = RegularClass(1, 2, 3)
slotted = SlottedClass(1, 2, 3)

print(f"Regular class size: {sys.getsizeof(regular)} bytes")
print(f"Slotted class size: {sys.getsizeof(slotted)} bytes")

# 大量实例时显著节省
regular_objects = [RegularClass(i, i+1, i+2) for i in range(10000)]
slotted_objects = [SlottedClass(i, i+1, i+2) for i in range(10000)]

print(f"\nMemory for 10000 regular objects: ~{sys.getsizeof(regular) * 10000} bytes")
print(f"Memory for 10000 slotted objects: ~{sys.getsizeof(slotted) * 10000} bytes")
```

### 模式 14：用于 CPU 密集型任务的多进程

```python
import multiprocessing as mp
import time

def cpu_intensive_task(n):
    """CPU 密集型计算。"""
    return sum(i**2 for i in range(n))

def sequential_processing():
    """顺序处理任务。"""
    start = time.time()
    results = [cpu_intensive_task(1000000) for _ in range(4)]
    elapsed = time.time() - start
    return elapsed, results

def parallel_processing():
    """并行处理任务。"""
    start = time.time()
    with mp.Pool(processes=4) as pool:
        results = pool.map(cpu_intensive_task, [1000000] * 4)
    elapsed = time.time() - start
    return elapsed, results

if __name__ == "__main__":
    seq_time, seq_results = sequential_processing()
    par_time, par_results = parallel_processing()

    print(f"Sequential: {seq_time:.2f}s")
    print(f"Parallel: {par_time:.2f}s")
    print(f"Speedup: {seq_time/par_time:.2f}x")
```

### 模式 15：用于 I/O 密集型任务的异步 I/O

```python
import asyncio
import aiohttp
import time
import requests

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

def synchronous_requests():
    """同步 HTTP 请求。"""
    start = time.time()
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.status_code)
    elapsed = time.time() - start
    return elapsed, results

async def async_fetch(session, url):
    """异步 HTTP 请求。"""
    async with session.get(url) as response:
        return response.status

async def asynchronous_requests():
    """异步 HTTP 请求。"""
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    return elapsed, results

# 异步对 I/O 密集型工作快得多
sync_time, sync_results = synchronous_requests()
async_time, async_results = asyncio.run(asynchronous_requests())

print(f"Synchronous: {sync_time:.2f}s")
print(f"Asynchronous: {async_time:.2f}s")
print(f"Speedup: {sync_time/async_time:.2f}x")
```

## 数据库优化

### 模式 16：批量数据库操作

```python
import sqlite3
import time

def create_db():
    """创建测试数据库。"""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    return conn

def slow_inserts(conn, count):
    """逐条插入记录。"""
    start = time.time()
    cursor = conn.cursor()
    for i in range(count):
        cursor.execute("INSERT INTO users (name) VALUES (?)", (f"User {i}",))
        conn.commit()  # 每次插入都提交
    elapsed = time.time() - start
    return elapsed

def fast_inserts(conn, count):
    """使用单次提交批量插入。"""
    start = time.time()
    cursor = conn.cursor()
    data = [(f"User {i}",) for i in range(count)]
    cursor.executemany("INSERT INTO users (name) VALUES (?)", data)
    conn.commit()  # 单次提交
    elapsed = time.time() - start
    return elapsed

# 基准测试
conn1 = create_db()
slow_time = slow_inserts(conn1, 1000)

conn2 = create_db()
fast_time = fast_inserts(conn2, 1000)

print(f"Individual inserts: {slow_time:.4f}s")
print(f"Batch insert: {fast_time:.4f}s")
print(f"Speedup: {slow_time/fast_time:.2f}x")
```

### 模式 17：查询优化

```python
# 为频繁查询的列使用索引
"""
-- 慢：无索引
SELECT * FROM users WHERE email = 'user@example.com';

-- 快：有索引
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
"""

# 使用查询计划
import sqlite3

conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# 分析查询性能
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?", ("test@example.com",))
print(cursor.fetchall())

# 仅选择需要的列
# 慢：SELECT *
# 快：SELECT id, name
```

## 内存优化

### 模式 18：检测内存泄漏

```python
import tracemalloc
import gc

def memory_leak_example():
    """泄漏内存的示例。"""
    leaked_objects = []

    for i in range(100000):
        # 添加对象但从不删除
        leaked_objects.append([i] * 100)

    # 在真实代码中，这将是一个意外的引用

def track_memory_usage():
    """跟踪内存分配。"""
    tracemalloc.start()

    # 之前拍摄快照
    snapshot1 = tracemalloc.take_snapshot()

    # 运行代码
    memory_leak_example()

    # 之后拍摄快照
    snapshot2 = tracemalloc.take_snapshot()

    # 比较
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()

# 监控内存
track_memory_usage()

# 强制垃圾回收
gc.collect()
```

### 模式 19：迭代器 vs 列表

```python
import sys

def process_file_list(filename):
    """将整个文件加载到内存中。"""
    with open(filename) as f:
        lines = f.readlines()  # 加载所有行
        return sum(1 for line in lines if line.strip())

def process_file_iterator(filename):
    """逐行处理文件。"""
    with open(filename) as f:
        return sum(1 for line in f if line.strip())

# 迭代器使用恒定内存
# 列表将整个文件加载到内存中
```

### 模式 20：用于缓存的 Weakref

```python
import weakref

class CachedResource:
    """可以被垃圾回收的资源。"""
    def __init__(self, data):
        self.data = data

# 常规缓存防止垃圾回收
regular_cache = {}

def get_resource_regular(key):
    """从常规缓存获取资源。"""
    if key not in regular_cache:
        regular_cache[key] = CachedResource(f"Data for {key}")
    return regular_cache[key]

# 弱引用缓存允许垃圾回收
weak_cache = weakref.WeakValueDictionary()

def get_resource_weak(key):
    """从弱缓存获取资源。"""
    resource = weak_cache.get(key)
    if resource is None:
        resource = CachedResource(f"Data for {key}")
        weak_cache[key] = resource
    return resource

# 当没有强引用存在时，对象可以被 GC
```

## 基准测试工具

### 自定义基准测试装饰器

```python
import time
from functools import wraps

def benchmark(func):
    """基准测试函数执行的装饰器。"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f} seconds")
        return result
    return wrapper

@benchmark
def slow_function():
    """要基准测试的函数。"""
    time.sleep(0.5)
    return sum(range(1000000))

result = slow_function()
```

### 使用 pytest-benchmark 进行性能测试

```python
# 安装：pip install pytest-benchmark

def test_list_comprehension(benchmark):
    """基准测试列表推导式。"""
    result = benchmark(lambda: [i**2 for i in range(10000)])
    assert len(result) == 10000

def test_map_function(benchmark):
    """基准测试 map 函数。"""
    result = benchmark(lambda: list(map(lambda x: x**2, range(10000))))
    assert len(result) == 10000

# 运行：pytest test_performance.py --benchmark-compare
```

## 最佳实践

1. **分析先于优化** - 测量以找出真正的瓶颈
2. **专注于热路径** - 优化最频繁运行的代码
3. **使用适当的数据结构** - 字典用于查找，集合用于成员关系
4. **避免过早优化** - 清晰为先，然后再优化
5. **使用内置函数** - 它们以 C 实现
6. **缓存昂贵的计算** - 使用 lru_cache
7. **批处理 I/O 操作** - 减少系统调用
8. **对大型数据集使用生成器**
9. **对数值运算考虑使用 NumPy**
10. **分析生产环境代码** - 对线上系统使用 py-spy

## 常见陷阱

- 不分析就进行优化
- 不必要地使用全局变量
- 不使用适当的数据结构
- 创建不必要的数据副本
- 不为数据库使用连接池
- 忽视算法复杂度
- 过度优化罕见的代码路径
- 不考虑内存使用

## 资源

- **cProfile**：内置 CPU 分析器
- **memory_profiler**：内存使用分析
- **line_profiler**：逐行分析
- **py-spy**：用于生产环境的采样分析器
- **NumPy**：高性能数值计算
- **Cython**：将 Python 编译为 C
- **PyPy**：具有 JIT 的替代 Python 解释器

## 性能检查清单

- [ ] 分析代码以识别瓶颈
- [ ] 使用了适当的数据结构
- [ ] 在有益的地方实现了缓存
- [ ] 优化了数据库查询
- [ ] 对大型数据集使用了生成器
- [ ] 对 CPU 密集型任务考虑了多进程
- [ ] 对 I/O 密集型任务使用了异步 I/O
- [ ] 最小化热循环中的函数调用开销
- [ ] 检查了内存泄漏
- [ ] 在优化前后进行了基准测试
