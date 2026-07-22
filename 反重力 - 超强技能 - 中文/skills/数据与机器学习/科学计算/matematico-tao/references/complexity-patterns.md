# Android/Kotlin 中的复杂度模式

## 1. 圈复杂度（McCabe）

### 定义
```
CC(G) = E - N + 2P，其中：
E = 控制流图的边数
N = 节点数
P = 连通分量数（通常为 1）

实用等价公式：
CC = 1 + 决策点数（if, when, for, while, &&, ||, catch）

推荐阈值：
CC ≤ 5：简单，易测试
CC 6-10：中等，可测试
CC 11-20：复杂，难测试——应重构
CC > 20：极复杂——必须拆分
```

### 高圈复杂度的 Android 模式

#### LlmClientFactory（估计 CC ≈ 18）
```kotlin
fun create(provider: LlmProvider, context: Context?): LlmClient {
    return when (provider) {           // +10（11 个分支）
        OPENAI -> {
            val key = store.get("openai")
            if (key != null) {         // +1
                OpenAiClient(key)
            } else {
                throw ConfigError()
            }
        }
        CLAUDE -> {
            val key = store.get("claude")
            if (key != null) {         // +1
                ClaudeClient(key)
            } else {
                throw ConfigError()
            }
        }
        // ... 另外 9 个类似分支
        RPA_CHATGPT -> {
            if (context != null) {     // +1
                RpaClient(context, CHATGPT)
            } else {
                throw ContextRequiredError()
            }
        }
    }
}
// CC ≈ 1 + 10 + 3 = 14 — 应重构
```

**用 Strategy + Registry 重构（CC ≈ 2）：**
```kotlin
typealias ClientFactory = (config: ProviderConfig) -> LlmClient

val registry: Map<LlmProvider, ClientFactory> = mapOf(
    OPENAI to { config -> OpenAiClient(config.requireKey()) },
    CLAUDE to { config -> ClaudeClient(config.requireKey()) },
    // ...
)

fun create(provider: LlmProvider, config: ProviderConfig): LlmClient {
    return registry[provider]?.invoke(config)    // CC = 1
        ?: throw UnsupportedProviderError(provider)  // CC + 1 = 2
}
```

---

## 2. 认知复杂度（Sonar）

### 与 McCabe 的区别
```
圈复杂度计算决策点。
认知复杂度衡量人类阅读的心智负担。

额外惩罚：
- 嵌套结构：每层嵌套 +1
- 流程中断（break, continue, goto）：+1
- 布尔表达式序列：每个不同操作符 +1
```

### 示例：HomeScreen.kt
```kotlin
// Compose 中潜在的高认知复杂度：
@Composable
fun HomeScreen(viewModel: MainViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    when (state.pipelineState) {      // +1
        IDLE -> { ... }
        RECORDING -> {
            if (state.isBluetoothConnected) {  // +2（嵌套）
                if (state.audioSource == SCO) {   // +3（嵌套）
                    ScoRecordingUI()
                } else {
                    GenericRecordingUI()
                }
            } else {
                PhoneMicUI()
            }
        }
        // ...
    }
}
// 估计认知复杂度：~15-25，取决于完整实现
```

---

## 3. 耦合分析

### 耦合度量
```
Ca（传入耦合）：有多少模块依赖 X
  高 Ca → X 被广泛使用 → 难以修改
  core-logging：Ca = 6（所有模块）→ 高度耦合

Ce（传出耦合）：X 依赖多少模块
  高 Ce → X 依赖太多东西 → 脆弱
  app：Ce = 6 → 高，但对编排层来说正常

不稳定性 I = Ce / (Ca + Ce)
  I → 0：模块稳定（难以修改）
  I → 1：模块不稳定（容易修改）

Auri 模块：
  core-logging：Ca=6, Ce=0 → I = 0（稳定）
  app：Ca=0, Ce=6 → I = 1（不稳定——预期：最易变层）
  llm：Ca=1(app), Ce=1(core-logging) → I = 0.5（均衡）
```

### 稳定依赖原则（Martin）
```
规则：模块应仅依赖比自己更稳定的模块
I(依赖方) > I(被依赖方) 对每条边

Auri 验证：
app(I=1) → bluetooth(I≈0.5) ✅ (1 > 0.5)
app(I=1) → core-logging(I=0) ✅ (1 > 0)
voice(I≈0.5) → audio(I≈0.3) ✅ (0.5 > 0.3)
voice(I≈0.5) → core-logging(I=0) ✅ (0.5 > 0)
```

---

## 4. Android 接口复杂度

### Activity/Fragment 生命周期复杂度
```
Android Activity 生命周期有 7 个主要状态：
CREATED → STARTED → RESUMED → PAUSED → STOPPED → DESTROYED（+ RESTARTED）

形式化的有效转换：
T = {
  CREATED → STARTED (onStart),
  STARTED → RESUMED (onResume),
  RESUMED → PAUSED (onPause),
  PAUSED → STOPPED (onStop) 或 PAUSED → RESUMED (onResume),
  STOPPED → DESTROYED (onDestroy) 或 STOPPED → CREATED (onRestart),
  CREATED → DESTROYED (onDestroy — 未经 start，罕见)
}

陷阱：onResume 中的代码假设"干净"状态，但它可能在
仅经过 onPause 而未经过 onCreate 后被调用 → 部分初始化状态
```

### Jetpack Compose 重组合
```
重组合复杂度：
- 每个 @Composable 调用可能随时被重组合
- @Composable 内读取 State<T> 自动创建订阅
- 重组合是智能的：仅重组合必要的最小子树

常见问题：
1. Lambda 捕获可变变量 → 意外重组合
2. remember { } 无 key → 依赖变化时不重新计算
3. 缺少 derivedStateOf { } → 每次重组合都重新计算

度量：每个 @Composable 的 State 读取数
> 5 次读取/composable → 考虑拆分为更小组件
```

---

## 5. 特定算法的复杂度分析

### 按键检测（HeadsetButtonController）
```
问题：检测单击、双击、长按
输入：带时间戳的 key_down、key_up 事件序列

当前算法（估计）：
- 350ms 窗口用于双击检测
- 600ms 阈值用于长按
- 实现：协程 + delay + cancel

复杂度：
- 时间：O(1) 每事件（delay 是异步的）
- 空间：O(1) 状态（仅时间戳）
- 延迟：350ms 确认单击（不可避免）

替代方案：显式状态机
状态 = (tapCount: Int, lastTapTime: Long, isLongPressing: Boolean)
比嵌套 delay 更可测试、更形式化
```

### 音频优先级选择（AudioRouteController）
```
问题：给定可用源集合，选择最优源
输入：Set<AudioSource>（通常大小 1-4）

算法：max(availableSources, key=priority)
复杂度：O(n)，n = |availableSources| ≤ 5
优化：预排序可用 O(1)（有序 Set）

正确性不变量：
∀ s ∈ availableSources: priority(selectedSource) ≥ priority(s)
```

### LLM 响应处理
```
问题：处理 LLM 的流式响应
输入：Stream<String> 的 token 流

可能算法：
1. 完整缓冲：累积所有内容，一次性处理
   - 延迟：O(total_tokens / bandwidth) — 高
   - 内存：O(total_tokens) — 线性

2. 部分流式（建议实现）：累积到完整句子
   - 检测句末：regex \.|\!|\?
   - 感知延迟：O(首句 / bandwidth) — 低
   - 复杂度：每处理一句 O(1) 内存

建议：部分流式以改善用户体验
句子阈值：~15-20 词或第一个 ., !, ?
```

---

## 6. 主要操作的 Big-O

```
操作                                   | 复杂度     | 备注
───────────────────────────────────────┼───────────┼─────────────────────
蓝牙扫描                               | O(1) 均摊 | 有超时上限
SCO 连接                               | O(1)      | 固定协议
音频路由选择                           | O(n)      | n=源数（~5）
STT (SpeechRecognizer)                | O(w²) 最坏| w=词数（HMM）
LLM 推理（本地 Ollama）               | O(t·d²)   | t=token, d=维度
LLM 推理（API）                        | O(t) 感知 | 网络延迟
TTS 合成                               | O(c)      | c=字符数
工具执行（如设闹钟）                   | O(1)      | Android API 调用
Gmail 搜索                             | O(n log n)| n=邮件数（服务端）
StateFlow 更新（CAS）                  | O(1) 摊还 | 无锁
协程启动                               | O(1)      | ~1μs 开销
```

---

## 7. 代码熵分析

### 软件系统的 Shannon 熵定义
```
Halstead 复杂度：
η₁ = 不同运算符数
η₂ = 不同操作数数
N₁ = 运算符总出现次数
N₂ = 操作数总出现次数

容量：V = (N₁+N₂) · log₂(η₁+η₂)
难度：D = (η₁/2) · (N₂/η₂)
工作量：E = D · V

解读：
- 高容量 → 文件大/复杂
- 高难度 → 唯一运算符多 vs 重复少
- 高工作量 → 难以理解

Kotlin 文件估计：
MainViewModel.kt：估计 V ≈ 5000-10000, D ≈ 15-25 — 复杂
LlmProvider.kt：估计 V ≈ 500-1000, D ≈ 5-10 — 简单
```
