# 并发与并行编程

## 原子操作与内存序

```cpp
#include <atomic>
#include <thread>

// 基本原子类型
std::atomic<int> counter{0};
std::atomic<bool> flag{false};

// 内存序
void producer(std::atomic<int>& data, std::atomic<bool>& ready) {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release);  // Release 屏障
}

void consumer(std::atomic<int>& data, std::atomic<bool>& ready) {
    while (!ready.load(std::memory_order_acquire)) {  // Acquire 屏障
        std::this_thread::yield();
    }
    int value = data.load(std::memory_order_relaxed);
}

// 比较并交换（CAS）
bool try_acquire_lock(std::atomic<bool>& lock) {
    bool expected = false;
    return lock.compare_exchange_strong(expected, true,
                                       std::memory_order_acquire,
                                       std::memory_order_relaxed);
}

// 原子加法
int increment_counter(std::atomic<int>& counter) {
    return counter.fetch_add(1, std::memory_order_relaxed);
}
```

## 无锁数据结构

```cpp
#include <atomic>
#include <memory>

// 无锁栈
template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
        Node(const T& value) : data(value), next(nullptr) {}
    };

    std::atomic<Node*> head_{nullptr};

public:
    void push(const T& value) {
        Node* new_node = new Node(value);
        new_node->next = head_.load(std::memory_order_relaxed);

        while (!head_.compare_exchange_weak(new_node->next, new_node,
                                           std::memory_order_release,
                                           std::memory_order_relaxed)) {
            // 使用更新后的 head 重试
        }
    }

    bool pop(T& result) {
        Node* old_head = head_.load(std::memory_order_relaxed);

        while (old_head &&
               !head_.compare_exchange_weak(old_head, old_head->next,
                                           std::memory_order_acquire,
                                           std::memory_order_relaxed)) {
            // 重试
        }

        if (old_head) {
            result = old_head->data;
            delete old_head;  // 注意：存在 ABA 问题
            return true;
        }
        return false;
    }
};

// 无锁队列（单生产者、单消费者）
template<typename T, size_t Size>
class SPSCQueue {
    std::array<T, Size> buffer_;
    alignas(64) std::atomic<size_t> head_{0};
    alignas(64) std::atomic<size_t> tail_{0};

public:
    bool push(const T& item) {
        size_t head = head_.load(std::memory_order_relaxed);
        size_t next_head = (head + 1) % Size;

        if (next_head == tail_.load(std::memory_order_acquire)) {
            return false;  // 队列已满
        }

        buffer_[head] = item;
        head_.store(next_head, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        size_t tail = tail_.load(std::memory_order_relaxed);

        if (tail == head_.load(std::memory_order_acquire)) {
            return false;  // 队列为空
        }

        item = buffer_[tail];
        tail_.store((tail + 1) % Size, std::memory_order_release);
        return true;
    }
};
```

## 线程池

```cpp
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <future>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex queue_mutex_;
    std::condition_variable condition_;
    bool stop_ = false;

public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex_);
                        condition_.wait(lock, [this] {
                            return stop_ || !tasks_.empty();
                        });

                        if (stop_ && tasks_.empty()) {
                            return;
                        }

                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }

                    task();
                }
            });
        }
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            stop_ = true;
        }
        condition_.notify_all();
        for (auto& worker : workers_) {
            worker.join();
        }
    }

    template<typename F, typename... Args>
    auto enqueue(F&& f, Args&&... args)
        -> std::future<typename std::invoke_result_t<F, Args...>> {

        using return_type = typename std::invoke_result_t<F, Args...>;

        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );

        std::future<return_type> result = task->get_future();

        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            if (stop_) {
                throw std::runtime_error("enqueue on stopped ThreadPool");
            }
            tasks_.emplace([task]() { (*task)(); });
        }

        condition_.notify_one();
        return result;
    }
};
```

## 并行 STL 算法

```cpp
#include <algorithm>
#include <execution>
#include <vector>
#include <numeric>

void parallel_algorithms_demo() {
    std::vector<int> vec(1'000'000);
    std::iota(vec.begin(), vec.end(), 0);

    // 并行排序
    std::sort(std::execution::par, vec.begin(), vec.end());

    // 并行 for_each
    std::for_each(std::execution::par_unseq, vec.begin(), vec.end(),
                  [](int& x) { x *= 2; });

    // 并行 transform
    std::vector<int> result(vec.size());
    std::transform(std::execution::par, vec.begin(), vec.end(),
                   result.begin(), [](int x) { return x * x; });

    // 并行 reduce
    int sum = std::reduce(std::execution::par, vec.begin(), vec.end());

    // 并行 transform_reduce（map-reduce）
    int sum_of_squares = std::transform_reduce(
        std::execution::par,
        vec.begin(), vec.end(),
        0,
        std::plus<>(),
        [](int x) { return x * x; }
    );
}
```

## 同步原语

```cpp
#include <mutex>
#include <shared_mutex>
#include <condition_variable>

// 互斥量类型
std::mutex mtx;
std::recursive_mutex rec_mtx;
std::timed_mutex timed_mtx;
std::shared_mutex shared_mtx;

// RAII 锁
void exclusive_access() {
    std::lock_guard<std::mutex> lock(mtx);
    // 临界区
}

void unique_lock_example() {
    std::unique_lock<std::mutex> lock(mtx);
    // 可以解锁和重新加锁
    lock.unlock();
    // 执行一些工作
    lock.lock();
}

// 读写锁
class SharedData {
    mutable std::shared_mutex mutex_;
    std::string data_;

public:
    std::string read() const {
        std::shared_lock<std::shared_mutex> lock(mutex_);
        return data_;
    }

    void write(std::string new_data) {
        std::unique_lock<std::shared_mutex> lock(mutex_);
        data_ = std::move(new_data);
    }
};

// 条件变量
class Queue {
    std::queue<int> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;

public:
    void push(int value) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            queue_.push(value);
        }
        cv_.notify_one();
    }

    int pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return !queue_.empty(); });
        int value = queue_.front();
        queue_.pop();
        return value;
    }
};

// std::scoped_lock - 多互斥量
std::mutex mtx1, mtx2;

void transfer(Account& from, Account& to, int amount) {
    std::scoped_lock lock(from.mutex, to.mutex);  // 无死锁
    from.balance -= amount;
    to.balance += amount;
}
```

## 异步与 Future

```cpp
#include <future>

// std::async
auto future = std::async(std::launch::async, []() {
    return expensive_computation();
});

// 获取结果（阻塞直到就绪）
auto result = future.get();

// Promise 和 Future
void producer(std::promise<int> promise) {
    int value = compute_value();
    promise.set_value(value);
}

void consumer(std::future<int> future) {
    int value = future.get();
}

std::promise<int> promise;
std::future<int> future = promise.get_future();

std::thread producer_thread(producer, std::move(promise));
std::thread consumer_thread(consumer, std::move(future));

// 打包任务
std::packaged_task<int(int, int)> task([](int a, int b) {
    return a + b;
});

std::future<int> task_future = task.get_future();
std::thread task_thread(std::move(task), 5, 3);

int sum = task_future.get();  // 8
task_thread.join();
```

## 基于协程的并发

```cpp
#include <coroutine>
#include <optional>

// 异步任务协程
template<typename T>
struct AsyncTask {
    struct promise_type {
        std::optional<T> value;
        std::exception_ptr exception;

        AsyncTask get_return_object() {
            return AsyncTask{
                std::coroutine_handle<promise_type>::from_promise(*this)
            };
        }

        std::suspend_never initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        void return_value(T v) {
            value = std::move(v);
        }

        void unhandled_exception() {
            exception = std::current_exception();
        }
    };

    std::coroutine_handle<promise_type> handle;

    AsyncTask(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~AsyncTask() { if (handle) handle.destroy(); }

    T get() {
        if (!handle.done()) {
            handle.resume();
        }

        if (handle.promise().exception) {
            std::rethrow_exception(handle.promise().exception);
        }

        return *handle.promise().value;
    }
};

// 用法
AsyncTask<int> async_compute() {
    co_return 42;
}
```

## 快速参考

| 原语 | 用途 | 性能 |
|-----------|----------|-------------|
| std::atomic | 简单共享状态 | 无锁 |
| std::mutex | 独占访问 | 内核调用 |
| std::shared_mutex | 读多写少场景 | 优于互斥量 |
| 无锁结构 | 高竞争场景 | 最佳吞吐量 |
| 线程池 | 任务并行 | 避免线程开销 |
| 并行 STL | 数据并行 | 自动扩展 |
| std::async | 简单异步任务 | 线程池 |
| 协程 | 异步 I/O | 最小开销 |

## 内存序指南

| 内存序 | 保证 | 用途 |
|----------|-----------|----------|
| relaxed | 无同步 | 计数器 |
| acquire | 加载屏障 | 消费者 |
| release | 存储屏障 | 生产者 |
| acq_rel | 两者兼具 | 读写改操作 |
| seq_cst | 全序 | 默认值 |
