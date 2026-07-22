# Kotlin/Android 的形式化并发模型

## 1. CSP 模型（通信顺序进程）

### 形式化定义
CSP 进程定义如下：
```
P ::= STOP                  -- 死进程（死锁）
    | SKIP                  -- 正常终止进程
    | a → P                 -- 前缀：执行事件 a，然后 P
    | P □ Q                 -- 外部选择：环境决定
    | P ⊓ Q                 -- 内部选择：P 决定
    | P ‖ Q                 -- 并行组合
    | P \ A                  -- 隐藏事件集合 A
```

### 在 Kotlin 协程中的应用
```kotlin
// 每个协程是一个 CSP 进程
// launch { } ≡ 并发进程
// channel.send(x) ≡ 输出事件
// channel.receive() ≡ 输入事件

// CSP 中的经典死锁：
// P = a → b → STOP
// Q = b → a → STOP
// P ‖ Q → 各自等待对方先行动 → 死锁

// Kotlin 等价写法：
val channelA = Channel<Int>()
val channelB = Channel<Int>()
launch { channelA.send(1); channelB.receive() }  // P
launch { channelB.send(2); channelA.receive() }  // Q
// 死锁：双方阻塞等待
```

---

## 2. Actor 模型

### 定义
每个 Actor 拥有：
- 邮箱（mailbox）— 消息队列
- 行为— 函数：消息 → (新状态, [新 Actor], [新消息])
- 封装的本地状态— 不共享

### Kotlin 协程中的实现
```kotlin
// 通过 Channel + 协程实现 Actor
fun CoroutineScope.counterActor() = actor<CounterMsg> {
    var counter = 0
    for (msg in channel) {
        when (msg) {
            is IncCounter -> counter++
            is GetCounter -> msg.response.complete(counter)
        }
    }
}

// 形式化性质：
// - 无竞态条件：状态封装
// - 无死锁：若邮箱无界且无循环
// - 线性化：操作对客户端看似原子
```

---

## 3. Android 内存模型（JMM - Java 内存模型）

### Happens-Before 关系
```
JMM 保证可见性的规则：
1. 程序顺序：a₁ →ₚ a₂ 若 a₁ 在同一线程中先于 a₂
2. 监视器锁：unlock(m) → lock(m)
3. volatile：对 volatile 变量 write(v) → read(v)
4. 线程启动：start(t) → t 的任何动作
5. 线程汇合：t 的任何动作 → join(t)
6. 终结器：构造函数结束 → finalize() 开始
```

### StateFlow 与原子性
```kotlin
// MutableStateFlow 内部使用 CAS（Compare-And-Swap）
// 保证：compareAndSet 更新是无锁且无等待的
// 读取 .value 始终是最新版本（volatile 语义）

// 正确：原子更新
_state.update { currentState ->
    currentState.copy(isRecording = true)
}

// 错误：非原子的读-改-写
val current = _state.value          // 读
_state.value = current.copy(...)    // 分离写 → 竞态条件！
```

---

## 4. Android 中的死锁分析

### 常见死锁模式

#### 模式 1：主线程中的 runBlocking
```kotlin
// 死锁：runBlocking 阻塞 Main，协程需要 Main
fun onClickButton() {
    runBlocking {  // 阻塞 Main 线程
        viewModel.doSomething()  // 需要 Main 来更新
        // 死锁！
    }
}

// 正确：
fun onClickButton() {
    lifecycleScope.launch {
        viewModel.doSomething()
    }
}
```

#### 模式 2：Mutex 不可重入（Kotlin 中不存在可重入 Mutex）
```kotlin
// Kotlin Mutex 不可重入——与 synchronized(this) 不同
val mutex = Mutex()

suspend fun outer() {
    mutex.withLock {
        inner()  // 尝试获取同一 mutex → 死锁！
    }
}

suspend fun inner() {
    mutex.withLock {  // 阻塞等待 outer() 释放
        // 永远到不了这里
    }
}
```

#### 模式 3：无消费者的 Channel 会合
```kotlin
val channel = Channel<Result>()  // 无缓冲

launch {
    channel.send(result)  // 阻塞直到有人接收
}
// 若无活跃接收者 → 协程永远挂起
// 若作用域存活则可能导致内存泄漏

// 正确：使用 Channel(BUFFERED) 或确保接收者存在
```

---

## 5. 活性分析（无饥饿）

### 形式化定义
```
饥饿：进程 P 处于饥饿状态若：
∃ 无限执行序列使得 P 永远无法推进，
即使 P 有资格执行。

用 LTL 表示：
¬Starvation(P) ≡ GF(ready(P)) → GF(running(P))
（"每当 P 就绪，P 终将执行"）
```

### 在 Android/Kotlin 上下文中
```kotlin
// 协程调度器的公平性：
// - Dispatchers.Default：处理器绑定工作，协程间轮转
// - Dispatchers.IO：可扩展线程池（默认 64 线程），公平调度
// - Dispatchers.Main：Main 线程上的 FIFO 队列

// 饥饿风险：
// 1. Dispatchers.Default 有大量 CPU 密集型协程 → 新协程等待
// 2. Dispatchers.IO.limitedParallelism(n) → n 很小 → 队列很长

// Auri 示例：
// VoicePipeline 在 Main 上运行（用于 UI 更新）
// LLM 请求在 IO 上运行
// 若 LLM 请求阻塞 IO 线程池 → STT 可能等待
```

---

## 6. 用 TLA+ 验证性质

### VoicePipeline 示例
```tla
VARIABLES state, sttResult, llmResult

Init == state = "IDLE" /\ sttResult = "" /\ llmResult = ""

StartRecording ==
    /\ state = "IDLE"
    /\ state' = "RECORDING"
    /\ UNCHANGED <<sttResult, llmResult>>

StopAndTranscribe ==
    /\ state = "RECORDING"
    /\ state' = "TRANSCRIBING"
    /\ UNCHANGED <<sttResult, llmResult>>

STTComplete ==
    /\ state = "TRANSCRIBING"
    /\ sttResult' \in STRING \ {""}
    /\ state' = "QUERYING_LLM"
    /\ UNCHANGED <<llmResult>>

-- 安全性：
NoDeadlock == state \in {"IDLE","RECORDING","TRANSCRIBING",
                          "QUERYING_LLM","SPEAKING","ERROR"}

-- 活性：
EventuallyIdle == <>(state = "IDLE")
```

---

## 7. 竞态条件 — Kotlin/Android 检查清单

### 需要保护的变量
```kotlin
// ❌ 不安全：协程间共享 var 无同步
var isConnected: Boolean = false
launch(Dispatchers.IO) { isConnected = true }
launch(Dispatchers.Default) { if (isConnected) ... }  // 竞态！

// ✅ 安全：@Volatile 用于简单读写
@Volatile var isConnected: Boolean = false

// ✅ 安全：AtomicBoolean 用于 CAS 操作
val isConnected = AtomicBoolean(false)
isConnected.compareAndSet(false, true)

// ✅ 安全：StateFlow 用于可观察状态
private val _isConnected = MutableStateFlow(false)
val isConnected = _isConnected.asStateFlow()
```

### Kotlin 协程中的安全模式
```kotlin
// Mutex 用于临界区
val mutex = Mutex()
mutex.withLock {
    // 临界区
}

// Actor 用于封装可变状态
val stateActor = actor<StateMessage> { ... }

// StateFlow 用于响应式状态
val state = MutableStateFlow(initialState)
state.update { it.copy(...) }  // 通过 CAS 原子更新
```

---

## 8. Android 中的内存泄漏分析

### Context 泄漏（最常见）
```kotlin
// ❌ 泄漏：长生命周期对象捕获 Activity context
class LlmClient(val context: Context) {  // 若 context = Activity → 泄漏
    // 客户端可能比 Activity 存活更久
}

// ✅ 正确：长生命周期对象使用 Application context
class LlmClient(val context: Context) {
    init {
        // 长时间操作使用 context.applicationContext
    }
}
```

### 协程泄漏
```kotlin
// ❌ 泄漏：在不当作用域中启动协程
fun startRecording() {
    GlobalScope.launch {  // 永远不会被取消！
        // ...
    }
}

// ✅ 正确：作用域绑定到生命周期
class EarLlmService : Service() {
    private val serviceScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    override fun onDestroy() {
        serviceScope.cancel()  // 取消所有协程
    }
}
```

### 监听器泄漏（蓝牙）
```kotlin
// ❌ 泄漏：注册了监听器但从未移除
audioManager.registerAudioDeviceCallback(callback, null)
// onDestroy 忘记调用 unregisterAudioDeviceCallback

// ✅ 正确：注册/注销对称
override fun onStart() { register(callback) }
override fun onStop() { unregister(callback) }
```
