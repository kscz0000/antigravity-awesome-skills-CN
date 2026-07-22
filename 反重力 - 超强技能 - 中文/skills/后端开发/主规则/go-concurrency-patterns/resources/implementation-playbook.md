# Go 并发模式实现手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# Go 并发模式

Go 并发的生产级模式，涵盖 goroutine、channel、同步原语和 context 管理。

## 使用场景

- 构建并发 Go 应用
- 实现 worker pool 和管道
- 管理 goroutine 生命周期
- 使用 channel 进行通信
- 调试竞态条件
- 实现优雅关闭

## 核心概念

### 1. Go 并发原语

| 原语 | 用途 |
|------|------|
| `goroutine` | 轻量级并发执行 |
| `channel` | goroutine 间通信 |
| `select` | 多路复用 channel 操作 |
| `sync.Mutex` | 互斥锁 |
| `sync.WaitGroup` | 等待 goroutine 完成 |
| `context.Context` | 取消和截止时间 |

### 2. Go 并发格言

```
Don't communicate by sharing memory;
share memory by communicating.
```

## 快速开始

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    results := make(chan string, 10)
    var wg sync.WaitGroup

    // Spawn workers
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go worker(ctx, i, results, &wg)
    }

    // Close results when done
    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect results
    for result := range results {
        fmt.Println(result)
    }
}

func worker(ctx context.Context, id int, results chan<- string, wg *sync.WaitGroup) {
    defer wg.Done()

    select {
    case <-ctx.Done():
        return
    case results <- fmt.Sprintf("Worker %d done", id):
    }
}
```

## 模式

### 模式 1：Worker Pool

```go
package main

import (
    "context"
    "fmt"
    "sync"
)

type Job struct {
    ID   int
    Data string
}

type Result struct {
    JobID int
    Output string
    Err   error
}

func WorkerPool(ctx context.Context, numWorkers int, jobs <-chan Job) <-chan Result {
    results := make(chan Result, len(jobs))

    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    return
                default:
                    result := processJob(job)
                    results <- result
                }
            }
        }(i)
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

func processJob(job Job) Result {
    // Simulate work
    return Result{
        JobID:  job.ID,
        Output: fmt.Sprintf("Processed: %s", job.Data),
    }
}

// Usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    jobs := make(chan Job, 100)

    // Send jobs
    go func() {
        for i := 0; i < 50; i++ {
            jobs <- Job{ID: i, Data: fmt.Sprintf("job-%d", i)}
        }
        close(jobs)
    }()

    // Process with 5 workers
    results := WorkerPool(ctx, 5, jobs)

    for result := range results {
        fmt.Printf("Result: %+v\n", result)
    }
}
```

### 模式 2：Fan-Out/Fan-In 管道

```go
package main

import (
    "context"
    "sync"
)

// Stage 1: Generate numbers
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case <-ctx.Done():
                return
            case out <- n:
            }
        }
    }()
    return out
}

// Stage 2: Square numbers (can run multiple instances)
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case <-ctx.Done():
                return
            case out <- n * n:
            }
        }
    }()
    return out
}

// Fan-in: Merge multiple channels into one
func merge(ctx context.Context, cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    // Start output goroutine for each input channel
    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case <-ctx.Done():
                return
            case out <- n:
            }
        }
    }

    wg.Add(len(cs))
    for _, c := range cs {
        go output(c)
    }

    // Close out after all inputs are done
    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Generate input
    in := generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    // Fan out to multiple squarers
    c1 := square(ctx, in)
    c2 := square(ctx, in)
    c3 := square(ctx, in)

    // Fan in results
    for result := range merge(ctx, c1, c2, c3) {
        fmt.Println(result)
    }
}
```

### 模式 3：信号量限制并发

```go
package main

import (
    "context"
    "fmt"
    "golang.org/x/sync/semaphore"
    "sync"
)

type RateLimitedWorker struct {
    sem *semaphore.Weighted
}

func NewRateLimitedWorker(maxConcurrent int64) *RateLimitedWorker {
    return &RateLimitedWorker{
        sem: semaphore.NewWeighted(maxConcurrent),
    }
}

func (w *RateLimitedWorker) Do(ctx context.Context, tasks []func() error) []error {
    var (
        wg     sync.WaitGroup
        mu     sync.Mutex
        errors []error
    )

    for _, task := range tasks {
        // Acquire semaphore (blocks if at limit)
        if err := w.sem.Acquire(ctx, 1); err != nil {
            return []error{err}
        }

        wg.Add(1)
        go func(t func() error) {
            defer wg.Done()
            defer w.sem.Release(1)

            if err := t(); err != nil {
                mu.Lock()
                errors = append(errors, err)
                mu.Unlock()
            }
        }(task)
    }

    wg.Wait()
    return errors
}

// Alternative: Channel-based semaphore
type Semaphore chan struct{}

func NewSemaphore(n int) Semaphore {
    return make(chan struct{}, n)
}

func (s Semaphore) Acquire() {
    s <- struct{}{}
}

func (s Semaphore) Release() {
    <-s
}
```

### 模式 4：优雅关闭

```go
package main

import (
    "context"
    "fmt"
    "os"
    "os/signal"
    "sync"
    "syscall"
    "time"
)

type Server struct {
    shutdown chan struct{}
    wg       sync.WaitGroup
}

func NewServer() *Server {
    return &Server{
        shutdown: make(chan struct{}),
    }
}

func (s *Server) Start(ctx context.Context) {
    // Start workers
    for i := 0; i < 5; i++ {
        s.wg.Add(1)
        go s.worker(ctx, i)
    }
}

func (s *Server) worker(ctx context.Context, id int) {
    defer s.wg.Done()
    defer fmt.Printf("Worker %d stopped\n", id)

    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            // Cleanup
            fmt.Printf("Worker %d cleaning up...\n", id)
            time.Sleep(500 * time.Millisecond) // Simulated cleanup
            return
        case <-ticker.C:
            fmt.Printf("Worker %d working...\n", id)
        }
    }
}

func (s *Server) Shutdown(timeout time.Duration) {
    // Signal shutdown
    close(s.shutdown)

    // Wait with timeout
    done := make(chan struct{})
    go func() {
        s.wg.Wait()
        close(done)
    }()

    select {
    case <-done:
        fmt.Println("Clean shutdown completed")
    case <-time.After(timeout):
        fmt.Println("Shutdown timed out, forcing exit")
    }
}

func main() {
    // Setup signal handling
    ctx, cancel := context.WithCancel(context.Background())

    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

    server := NewServer()
    server.Start(ctx)

    // Wait for signal
    sig := <-sigCh
    fmt.Printf("\nReceived signal: %v\n", sig)

    // Cancel context to stop workers
    cancel()

    // Wait for graceful shutdown
    server.Shutdown(5 * time.Second)
}
```

### 模式 5：带取消的 Error Group

```go
package main

import (
    "context"
    "fmt"
    "golang.org/x/sync/errgroup"
    "net/http"
)

func fetchAllURLs(ctx context.Context, urls []string) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)

    results := make([]string, len(urls))

    for i, url := range urls {
        i, url := i, url // Capture loop variables

        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
            if err != nil {
                return fmt.Errorf("creating request for %s: %w", url, err)
            }

            resp, err := http.DefaultClient.Do(req)
            if err != nil {
                return fmt.Errorf("fetching %s: %w", url, err)
            }
            defer resp.Body.Close()

            results[i] = fmt.Sprintf("%s: %d", url, resp.StatusCode)
            return nil
        })
    }

    // Wait for all goroutines to complete or one to fail
    if err := g.Wait(); err != nil {
        return nil, err // First error cancels all others
    }

    return results, nil
}

// With concurrency limit
func fetchWithLimit(ctx context.Context, urls []string, limit int) ([]string, error) {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(limit) // Max concurrent goroutines

    results := make([]string, len(urls))
    var mu sync.Mutex

    for i, url := range urls {
        i, url := i, url

        g.Go(func() error {
            result, err := fetchURL(ctx, url)
            if err != nil {
                return err
            }

            mu.Lock()
            results[i] = result
            mu.Unlock()
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }

    return results, nil
}
```

### 模式 6：sync.Map 并发 Map

```go
package main

import (
    "sync"
)

// For frequent reads, infrequent writes
type Cache struct {
    m sync.Map
}

func (c *Cache) Get(key string) (interface{}, bool) {
    return c.m.Load(key)
}

func (c *Cache) Set(key string, value interface{}) {
    c.m.Store(key, value)
}

func (c *Cache) GetOrSet(key string, value interface{}) (interface{}, bool) {
    return c.m.LoadOrStore(key, value)
}

func (c *Cache) Delete(key string) {
    c.m.Delete(key)
}

// For write-heavy workloads, use sharded map
type ShardedMap struct {
    shards    []*shard
    numShards int
}

type shard struct {
    sync.RWMutex
    data map[string]interface{}
}

func NewShardedMap(numShards int) *ShardedMap {
    m := &ShardedMap{
        shards:    make([]*shard, numShards),
        numShards: numShards,
    }
    for i := range m.shards {
        m.shards[i] = &shard{data: make(map[string]interface{})}
    }
    return m
}

func (m *ShardedMap) getShard(key string) *shard {
    // Simple hash
    h := 0
    for _, c := range key {
        h = 31*h + int(c)
    }
    return m.shards[h%m.numShards]
}

func (m *ShardedMap) Get(key string) (interface{}, bool) {
    shard := m.getShard(key)
    shard.RLock()
    defer shard.RUnlock()
    v, ok := shard.data[key]
    return v, ok
}

func (m *ShardedMap) Set(key string, value interface{}) {
    shard := m.getShard(key)
    shard.Lock()
    defer shard.Unlock()
    shard.data[key] = value
}
```

### 模式 7：带超时和默认的 Select

```go
func selectPatterns() {
    ch := make(chan int)

    // Timeout pattern
    select {
    case v := <-ch:
        fmt.Println("Received:", v)
    case <-time.After(time.Second):
        fmt.Println("Timeout!")
    }

    // Non-blocking send/receive
    select {
    case ch <- 42:
        fmt.Println("Sent")
    default:
        fmt.Println("Channel full, skipping")
    }

    // Priority select (check high priority first)
    highPriority := make(chan int)
    lowPriority := make(chan int)

    for {
        select {
        case msg := <-highPriority:
            fmt.Println("High priority:", msg)
        default:
            select {
            case msg := <-highPriority:
                fmt.Println("High priority:", msg)
            case msg := <-lowPriority:
                fmt.Println("Low priority:", msg)
            }
        }
    }
}
```

## 竞态检测

```bash
# Run tests with race detector
go test -race ./...

# Build with race detector
go build -race .

# Run with race detector
go run -race main.go
```

## 最佳实践

### 应该做的
- **使用 context** - 用于取消和截止时间
- **关闭 channel** - 仅从发送方关闭
- **使用 errgroup** - 用于带错误的并发操作
- **缓冲 channel** - 当你知道数量时
- **优先使用 channel** - 尽可能优先于 mutex

### 不应该做的
- **不要泄漏 goroutine** - 始终有退出路径
- **不要从接收方关闭** - 会导致 panic
- **不要使用共享内存** - 除非必要
- **不要忽略 context 取消** - 检查 ctx.Done()
- **不要用 time.Sleep 同步** - 使用正确的原语

## 资源

- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
- [Effective Go - Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go by Example - Goroutines](https://gobyexample.com/goroutines)
