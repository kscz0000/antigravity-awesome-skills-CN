# Auri/EarLLM — 数学分析完整上下文

## 系统概览

**项目**：Auri v2.5.0 (EarLLM One)
**位置**：`C:\Users\renat\earbudllm`
**类型**：多模块 Android 应用（Kotlin + Jetpack Compose）
**功能**：语音 → STT → LLM → TTS 流水线，通过蓝牙耳机交互

---

## 模块架构

```
app（编排器）
├── core-logging（横切关注点：日志、指标）
├── bluetooth（蓝牙连接 — A2DP, HFP, SCO）
├── audio（PCM 采集、路由、硬件按钮）
├── voice（STT, TTS, 语音流水线）
├── llm（客户端：OpenAI, Claude, Gemini, Ollama, RPA）
└── integrations（Gmail OAuth2）
```

### 依赖图（形式化）
```
G = (V, E)，其中：
V = {app, bluetooth, audio, voice, llm, integrations, core-logging}
E = {
  app → bluetooth,
  app → audio,
  app → voice,
  app → llm,
  app → integrations,
  app → core-logging,
  audio → core-logging,
  voice → audio,
  voice → core-logging,
  llm → core-logging,
  integrations → core-logging
}

性质：
- 无环：是（DAG）✅
- core-logging：汇节点（出度 = 0）
- app：源节点（来自其他模块的入度 = 0）
- 强连通分量：每个模块自成一个 SCC（DAG）
```

---

## 主状态机

### VoicePipeline 状态
```
S = {IDLE, RECORDING, TRANSCRIBING, QUERYING_LLM, SPEAKING, ERROR}

转移 δ：
IDLE + startRecording → RECORDING
RECORDING + stopRecording → TRANSCRIBING
RECORDING + error → ERROR
TRANSCRIBING + sttResult(text) → QUERYING_LLM
TRANSCRIBING + sttResult(empty) → ERROR（3 秒后自动重置 → IDLE）
TRANSCRIBING + error → ERROR
QUERYING_LLM + llmResult → SPEAKING
QUERYING_LLM + error → ERROR
SPEAKING + ttsComplete → IDLE
ERROR + timeout(3s) → IDLE
ERROR + userReset → IDLE

已验证性质：
✅ 无不可达状态（所有状态都有从 IDLE 的路径）
✅ 无死锁（所有状态都有出转移）
✅ 自愈：ERROR 总是能恢复到 IDLE
⚠️  SPEAKING 无取消机制——TTS 卡住时可能阻塞
```

### BluetoothController 状态
```
S = {DISCONNECTED, SCANNING, CONNECTING, CONNECTED, SCO_CONNECTING, SCO_ACTIVE, ERROR}

音频源优先级（单调函数）：
priority: AudioSource → ℤ
  BLE_AUDIO  → 5
  BT_SCO     → 4
  USB_MIC    → 3
  WIRED      → 2
  BUILTIN    → 1

不变量：currentSource = argmax{priority(s) | s ∈ availableSources}
```

---

## 并发分析

### 协程作用域
```
viewModelScope (MainViewModel)：
- 生命周期：绑定到 ViewModel，onCleared() 时取消
- 调度器：Main 用于 UI，IO 用于网络/磁盘，Default 用于 CPU

已识别模式：
- StateFlow<VoicePipelineState> 作为集中事件总线
- Compose 屏幕中通过 LaunchedEffect collect { }
- MutableStateFlow 原子更新（线程安全）

潜在风险：
- SharedFlow 无回放：收集器慢时事件可能丢失
- launch { } 无 supervisorScope：失败会取消所有子协程
- 嵌套 withContext(Dispatchers.IO)：不必要的上下文切换开销
```

### AuriToolExecutor — 幂等性分析
```
9 个工具：
1. alarm    — 非幂等（创建重复闹钟）
2. calendar — 非幂等（创建重复事件）
3. reminder — 非幂等
4. time     — 幂等（只读）
5. email    — 非幂等（可能发送重复邮件）
6. draft    — 准幂等（相同内容的草稿）
7. call     — 非幂等（发起通话）
8. whatsapp — 非幂等
9. app      — 若 app 已打开则幂等

风险：无去重机制，重试逻辑可能导致重复操作
建议：为每个工具实现幂等键
```

---

## 性能分析

### 延迟流水线（A04 上端到端实测）
```
组件              典型延迟         模型
──────────────────────────────────────────────
音频采集           ~100ms           确定性
STT（在线）        200-800ms        对数正态分布
STT（Vosk 离线）  N/A（桩）        —
LLM（Ollama A04） 10-15s           高方差（~3 tok/s）
LLM（OpenAI API） 1-3s             Gamma 分布
TTS                50-200ms         确定性

端到端总延迟（Ollama A04）：μ ≈ 12s, σ ≈ 3s
端到端总延迟（OpenAI）：μ ≈ 2.5s, σ ≈ 0.8s

LLM 流水线的 M/M/1 排队模型：
- λ（请求率）：~0.1 req/s（典型使用中每 10 秒 1 次）
- μ（Ollama A04 服务率）：~0.08 req/s
- ρ = λ/μ = 1.25 > 1 → 持续负载下不稳定！
- ρ（OpenAI）≈ 0.3 → 有足够缓冲时稳定
```

### 内存消耗
```
各组件估计：
- App 基础：~50MB
- 蓝牙栈：~5MB
- 音频缓冲（PCM, 16kHz, 16-bit, 5s）：~160KB
- STT 模型（Android）：~2MB（在线）/ ~50MB（Vosk）
- LLM 上下文（OpenAI/Claude）：仅 token（网络）
- 本地 LLM（llama3.2:1b）：~800MB RAM

使用 Ollama 本地总计：~850MB → 2GB RAM 设备上很危险
```

---

## 安全分析

### 攻击面
```
1. API 密钥：EncryptedSharedPreferences（AES-256-GCM）✅
2. 蓝牙 SCO：语音通信无加密（设计限制）⚠️
3. HTTP 明文（Ollama localhost）：通过 network_security_config 显式允许 ⚠️
4. LAN 访问：明文允许 192.168.*.* — 公共网络上有风险 ❌
5. Gmail OAuth2 token：持久化在 token store 中——需验证加密
6. 音频录制：需要 RECORD_AUDIO 权限——需验证时效范围
```

---

## 高复杂度点

### LlmClientFactory（高圈复杂度）
```
函数：factory(provider, context) → LlmClient
分支：
- 11 个 provider（OPENAI, CLAUDE, GEMINI, AI_STUDIO, OLLAMA, STUB + 5 个 RPA 变体）
- Context 可空 vs 非空
- Config（base_url, model）存在 vs 缺失

估计圈复杂度：CC ≈ 15-20
建议：重构为 Strategy + Registry 模式
```

### MainViewModel（潜在的 God Object）
```
已识别职责：
1. VoicePipeline 编排
2. LLM provider 选择管理
3. 蓝牙状态
4. 对话历史
5. 工具执行代理
6. 设置同步

违反 SRP（单一职责原则）
解决方案：分解为专用子 ViewModel
```

---

## 系统全局不变量

```
GLOBAL-INV-01：
  任意时刻最多 1 个前台服务处于录音状态
  形式化：|{s ∈ Services | s.isRecording = true}| ≤ 1

GLOBAL-INV-02：
  API 密钥永远不会出现在日志中
  形式化：∀ 日志条目 l: ¬contains(l.text, apiKey)

GLOBAL-INV-03：
  SCO 连接存在当且仅当 isRecording = true 且 source = BT_SCO
  形式化：scoActive ↔ (isRecording ∧ audioSource = BT_SCO)

GLOBAL-INV-04：
  流水线始终处于已定义状态（无 undefined/null 状态）
  形式化：pipelineState ∈ S（如上定义，不含 null）
```
