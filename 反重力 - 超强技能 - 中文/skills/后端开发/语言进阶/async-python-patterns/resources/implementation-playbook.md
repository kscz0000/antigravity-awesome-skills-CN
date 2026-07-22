# Async Python 模式实现指南

本文件包含技能引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. 事件循环（Event Loop）
事件循环是 asyncio 的核心，负责管理和调度异步任务。

**关键特性：**
- 单线程协作式多任务
- 调度协程执行
- 处理 I/O 操作而不阻塞
- 管理回调和 Future 对象

### 2. 协程（Coroutines）
使用 `async def` 定义的函数，可以暂停和恢复执行。

**语法：**
```python
async def my_coroutine():
    result = await some_async_operation()
    return result
```

### 3. 任务（Tasks）
在事件循环上并发运行的已调度协程。

### 4. Future 对象
表示异步操作最终结果的低级对象。

### 5. 异步上下文管理器
支持 `async with` 语法的资源，用于正确清理。

### 6. 异步迭代器
支持 `async for` 语法的对象，用于遍历异步数据源。

## 快速入门

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

## 基础模式

### 模式 1：基本 Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """异步从 URL 获取数据。"""
    await asyncio.sleep(1)  # 模拟 I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### 模式 2：使用 gather() 并发执行

```python
import asyncio
from typing import List

async def fetch_user(user_id: int) -> dict:
    """获取用户数据。"""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    """并发获取多个用户。"""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    user_ids = [1, 2, 3, 4, 5]
    users = await fetch_all_users(user_ids)
    print(f"Fetched {len(users)} users")

asyncio.run(main())
```

### 模式 3：任务创建与管理

```python
import asyncio

async def background_task(name: str, delay: int):
    """长时间运行的后台任务。"""
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} completed")
    return f"Result from {name}"

async def main():
    # 创建任务
    task1 = asyncio.create_task(background_task("Task 1", 2))
    task2 = asyncio.create_task(background_task("Task 2", 1))

    # 执行其他工作
    print("Main: doing other work")
    await asyncio.sleep(0.5)

    # 等待任务完成
    result1 = await task1
    result2 = await task2

    print(f"Results: {result1}, {result2}")

asyncio.run(main())
```

### 模式 4：异步代码错误处理

```python
import asyncio
from typing import List, Optional

async def risky_operation(item_id: int) -> dict:
    """可能失败的操作。"""
    await asyncio.sleep(0.1)
    if item_id % 3 == 0:
        raise ValueError(f"Item {item_id} failed")
    return {"id": item_id, "status": "success"}

async def safe_operation(item_id: int) -> Optional[dict]:
    """带错误处理的包装器。"""
    try:
        return await risky_operation(item_id)
    except ValueError as e:
        print(f"Error: {e}")
        return None

async def process_items(item_ids: List[int]):
    """处理多个项目并进行错误处理。"""
    tasks = [safe_operation(iid) for iid in item_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 过滤失败项
    successful = [r for r in results if r is not None and not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"Success: {len(successful)}, Failed: {len(failed)}")
    return successful

asyncio.run(process_items([1, 2, 3, 4, 5, 6]))
```

### 模式 5：超时处理

```python
import asyncio

async def slow_operation(delay: int) -> str:
    """耗时操作。"""
    await asyncio.sleep(delay)
    return f"Completed after {delay}s"

async def with_timeout():
    """带超时执行操作。"""
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")

asyncio.run(with_timeout())
```

## 高级模式

### 模式 6：异步上下文管理器

```python
import asyncio
from typing import Optional

class AsyncDatabaseConnection:
    """异步数据库连接上下文管理器。"""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection: Optional[object] = None

    async def __aenter__(self):
        print("Opening connection")
        await asyncio.sleep(0.1)  # 模拟连接
        self.connection = {"dsn": self.dsn, "connected": True}
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        await asyncio.sleep(0.1)  # 模拟清理
        self.connection = None

async def query_database():
    """使用异步上下文管理器。"""
    async with AsyncDatabaseConnection("postgresql://localhost") as conn:
        print(f"Using connection: {conn}")
        await asyncio.sleep(0.2)  # 模拟查询
        return {"rows": 10}

asyncio.run(query_database())
```

### 模式 7：异步迭代器和生成器

```python
import asyncio
from typing import AsyncIterator

async def async_range(start: int, end: int, delay: float = 0.1) -> AsyncIterator[int]:
    """带延迟的异步数字生成器。"""
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i

async def fetch_pages(url: str, max_pages: int) -> AsyncIterator[dict]:
    """异步获取分页数据。"""
    for page in range(1, max_pages + 1):
        await asyncio.sleep(0.2)  # 模拟 API 调用
        yield {
            "page": page,
            "url": f"{url}?page={page}",
            "data": [f"item_{page}_{i}" for i in range(5)]
        }

async def consume_async_iterator():
    """消费异步迭代器。"""
    async for number in async_range(1, 5):
        print(f"Number: {number}")

    print("\nFetching pages:")
    async for page_data in fetch_pages("https://api.example.com/items", 3):
        print(f"Page {page_data['page']}: {len(page_data['data'])} items")

asyncio.run(consume_async_iterator())
```

### 模式 8：生产者-消费者模式

```python
import asyncio
from asyncio import Queue
from typing import Optional

async def producer(queue: Queue, producer_id: int, num_items: int):
    """生产项目并放入队列。"""
    for i in range(num_items):
        item = f"Item-{producer_id}-{i}"
        await queue.put(item)
        print(f"Producer {producer_id} produced: {item}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # 发送完成信号

async def consumer(queue: Queue, consumer_id: int):
    """从队列消费项目。"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.2)  # 模拟工作
        queue.task_done()

async def producer_consumer_example():
    """运行生产者-消费者模式。"""
    queue = Queue(maxsize=10)

    # 创建任务
    producers = [
        asyncio.create_task(producer(queue, i, 5))
        for i in range(2)
    ]

    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)
    ]

    # 等待生产者完成
    await asyncio.gather(*producers)

    # 等待队列清空
    await queue.join()

    # 取消消费者
    for c in consumers:
        c.cancel()

asyncio.run(producer_consumer_example())
```

### 模式 9：信号量限流

```python
import asyncio
from typing import List

async def api_call(url: str, semaphore: asyncio.Semaphore) -> dict:
    """带限流的 API 调用。"""
    async with semaphore:
        print(f"Calling {url}")
        await asyncio.sleep(0.5)  # 模拟 API 调用
        return {"url": url, "status": 200}

async def rate_limited_requests(urls: List[str], max_concurrent: int = 5):
    """带限流的多请求。"""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [api_call(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = [f"https://api.example.com/item/{i}" for i in range(20)]
    results = await rate_limited_requests(urls, max_concurrent=3)
    print(f"Completed {len(results)} requests")

asyncio.run(main())
```

### 模式 10：异步锁与同步

```python
import asyncio

class AsyncCounter:
    """线程安全的异步计数器。"""

    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        """安全递增计数器。"""
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # 模拟工作
            self.value = current + 1

    async def get_value(self) -> int:
        """获取当前值。"""
        async with self.lock:
            return self.value

async def worker(counter: AsyncCounter, worker_id: int):
    """递增计数器的工作者。"""
    for _ in range(10):
        await counter.increment()
        print(f"Worker {worker_id} incremented")

async def test_counter():
    """测试并发计数器。"""
    counter = AsyncCounter()

    workers = [asyncio.create_task(worker(counter, i)) for i in range(5)]
    await asyncio.gather(*workers)

    final_value = await counter.get_value()
    print(f"Final counter value: {final_value}")

asyncio.run(test_counter())
```

## 实际应用

### 使用 aiohttp 进行网页抓取

```python
import asyncio
import aiohttp
from typing import List, Dict

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict:
    """获取单个 URL。"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            text = await response.text()
            return {
                "url": url,
                "status": response.status,
                "length": len(text)
            }
    except Exception as e:
        return {"url": url, "error": str(e)}

async def scrape_urls(urls: List[str]) -> List[Dict]:
    """并发抓取多个 URL。"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

async def main():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/404",
    ]

    results = await scrape_urls(urls)
    for result in results:
        print(result)

asyncio.run(main())
```

### 异步数据库操作

```python
import asyncio
from typing import List, Optional

# 模拟的异步数据库客户端
class AsyncDB:
    """模拟异步数据库。"""

    async def execute(self, query: str) -> List[dict]:
        """执行查询。"""
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Example"}]

    async def fetch_one(self, query: str) -> Optional[dict]:
        """获取单行。"""
        await asyncio.sleep(0.1)
        return {"id": 1, "name": "Example"}

async def get_user_data(db: AsyncDB, user_id: int) -> dict:
    """并发获取用户及相关数据。"""
    user_task = db.fetch_one(f"SELECT * FROM users WHERE id = {user_id}")
    orders_task = db.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    profile_task = db.fetch_one(f"SELECT * FROM profiles WHERE user_id = {user_id}")

    user, orders, profile = await asyncio.gather(user_task, orders_task, profile_task)

    return {
        "user": user,
        "orders": orders,
        "profile": profile
    }

async def main():
    db = AsyncDB()
    user_data = await get_user_data(db, 1)
    print(user_data)

asyncio.run(main())
```

### WebSocket 服务器

```python
import asyncio
from typing import Set

# 模拟的 WebSocket 连接
class WebSocket:
    """模拟 WebSocket。"""

    def __init__(self, client_id: str):
        self.client_id = client_id

    async def send(self, message: str):
        """发送消息。"""
        print(f"Sending to {self.client_id}: {message}")
        await asyncio.sleep(0.01)

    async def recv(self) -> str:
        """接收消息。"""
        await asyncio.sleep(1)
        return f"Message from {self.client_id}"

class WebSocketServer:
    """简单的 WebSocket 服务器。"""

    def __init__(self):
        self.clients: Set[WebSocket] = set()

    async def register(self, websocket: WebSocket):
        """注册新客户端。"""
        self.clients.add(websocket)
        print(f"Client {websocket.client_id} connected")

    async def unregister(self, websocket: WebSocket):
        """注销客户端。"""
        self.clients.remove(websocket)
        print(f"Client {websocket.client_id} disconnected")

    async def broadcast(self, message: str):
        """向所有客户端广播消息。"""
        if self.clients:
            tasks = [client.send(message) for client in self.clients]
            await asyncio.gather(*tasks)

    async def handle_client(self, websocket: WebSocket):
        """处理单个客户端连接。"""
        await self.register(websocket)
        try:
            async for message in self.message_iterator(websocket):
                await self.broadcast(f"{websocket.client_id}: {message}")
        finally:
            await self.unregister(websocket)

    async def message_iterator(self, websocket: WebSocket):
        """遍历客户端消息。"""
        for _ in range(3):  # 模拟 3 条消息
            yield await websocket.recv()
```

## 性能最佳实践

### 1. 使用连接池

```python
import asyncio
import aiohttp

async def with_connection_pool():
    """使用连接池提高效率。"""
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [session.get(f"https://api.example.com/item/{i}") for i in range(50)]
        responses = await asyncio.gather(*tasks)
        return responses
```

### 2. 批量操作

```python
async def batch_process(items: List[str], batch_size: int = 10):
    """批量处理项目。"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [process_item(item) for item in batch]
        await asyncio.gather(*tasks)
        print(f"Processed batch {i // batch_size + 1}")

async def process_item(item: str):
    """处理单个项目。"""
    await asyncio.sleep(0.1)
    return f"Processed: {item}"
```

### 3. 避免阻塞操作

```python
import asyncio
import concurrent.futures
from typing import Any

def blocking_operation(data: Any) -> Any:
    """CPU 密集型阻塞操作。"""
    import time
    time.sleep(1)
    return data * 2

async def run_in_executor(data: Any) -> Any:
    """在线程池中运行阻塞操作。"""
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_operation, data)
        return result

async def main():
    results = await asyncio.gather(*[run_in_executor(i) for i in range(5)])
    print(results)

asyncio.run(main())
```

## 常见陷阱

### 1. 忘记 await

```python
# 错误 - 返回协程对象，未执行
result = async_function()

# 正确
result = await async_function()
```

### 2. 阻塞事件循环

```python
# 错误 - 阻塞事件循环
import time
async def bad():
    time.sleep(1)  # 阻塞！

# 正确
async def good():
    await asyncio.sleep(1)  # 非阻塞
```

### 3. 未处理取消

```python
async def cancelable_task():
    """处理取消的任务。"""
    try:
        while True:
            await asyncio.sleep(1)
            print("Working...")
    except asyncio.CancelledError:
        print("Task cancelled, cleaning up...")
        # 执行清理
        raise  # 重新抛出以传播取消
```

### 4. 混合同步和异步代码

```python
# 错误 - 不能直接从同步函数调用异步函数
def sync_function():
    result = await async_function()  # SyntaxError!

# 正确
def sync_function():
    result = asyncio.run(async_function())
```

## 测试异步代码

```python
import asyncio
import pytest

# 使用 pytest-asyncio
@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数。"""
    result = await fetch_data("https://api.example.com")
    assert result is not None

@pytest.mark.asyncio
async def test_with_timeout():
    """带超时测试。"""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(5), timeout=1.0)
```

## 资源

- **Python asyncio 文档**: https://docs.python.org/3/library/asyncio.html
- **aiohttp**: 异步 HTTP 客户端/服务器
- **FastAPI**: 现代异步 Web 框架
- **asyncpg**: 异步 PostgreSQL 驱动
- **motor**: 异步 MongoDB 驱动

## 最佳实践总结

1. **使用 asyncio.run()** 作为入口点（Python 3.7+）
2. **始终 await 协程** 以执行它们
3. **使用 gather() 并发执行** 多个任务
4. **实现正确的错误处理** 使用 try/except
5. **使用超时** 防止操作挂起
6. **池化连接** 以获得更好性能
7. **避免异步代码中的阻塞操作**
8. **使用信号量** 进行限流
9. **正确处理任务取消**
10. **使用 pytest-asyncio 测试异步代码**
