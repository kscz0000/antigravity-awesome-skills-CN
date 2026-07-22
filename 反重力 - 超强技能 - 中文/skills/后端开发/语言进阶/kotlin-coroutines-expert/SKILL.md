---
name: kotlin-coroutines-expert
description: "Kotlin 协程与 Flow 专家模式，涵盖结构化并发、错误处理和测试策略。触发词：Kotlin协程、协程模式、Flow、结构化并发、协程错误处理、协程测试、suspend函数、StateFlow、SharedFlow、异步编程"
risk: safe
source: community
date_added: "2026-02-27"
---

# Kotlin 协程专家

## 概述

掌握 Kotlin 协程异步编程的指南。涵盖结构化并发、`Flow` 转换、异常处理和测试策略等高级主题。

## 何时使用此技能

- 在 Kotlin 中实现异步操作时使用。
- 使用 `Flow` 设计响应式数据流时使用。
- 调试协程取消或异常时使用。
- 为挂起函数或 Flow 编写单元测试时使用。

## 分步指南

### 1. 结构化并发

始终在定义的 `CoroutineScope` 内启动协程。使用 `coroutineScope` 或 `supervisorScope` 对并发任务进行分组。

```kotlin
suspend fun loadDashboardData(): DashboardData = coroutineScope {
    val userDeferred = async { userRepo.getUser() }
    val settingsDeferred = async { settingsRepo.getSettings() }
    
    DashboardData(
        user = userDeferred.await(),
        settings = settingsDeferred.await()
    )
}
```

### 2. 异常处理

对顶层作用域使用 `CoroutineExceptionHandler`，但在挂起函数内部使用 `try-catch` 进行精细控制。

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught $exception")
}

viewModelScope.launch(handler) {
    try {
        riskyOperation()
    } catch (e: IOException) {
        // Handle network error specifically
    }
}
```

### 3. 使用 Flow 的响应式流

使用 `StateFlow` 保存需要保留的状态，使用 `SharedFlow` 处理事件。

```kotlin
// Cold Flow (Lazy)
val searchResults: Flow<List<Item>> = searchQuery
    .debounce(300)
    .flatMapLatest { query -> searchRepo.search(query) }
    .flowOn(Dispatchers.IO)

// Hot Flow (State)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()
```

## 示例

### 示例 1：带错误处理的并行执行

```kotlin
suspend fun fetchDataWithErrorHandling() = supervisorScope {
    val task1 = async { 
        try { api.fetchA() } catch (e: Exception) { null } 
    }
    val task2 = async { api.fetchB() }
    
    // If task2 fails, task1 is NOT cancelled because of supervisorScope
    val result1 = task1.await()
    val result2 = task2.await() // May throw
}
```

## 最佳实践

- ✅ **推荐：** 对阻塞式 I/O 操作使用 `Dispatchers.IO`。
- ✅ **推荐：** 在作用域不再需要时取消它（例如 `ViewModel.onCleared`）。
- ✅ **推荐：** 使用 `TestScope` 和 `runTest` 进行协程单元测试。
- ❌ **禁止：** 使用 `GlobalScope`。它会破坏结构化并发并可能导致泄漏。
- ❌ **禁止：** 捕获 `CancellationException`，除非你会重新抛出它。

## 故障排除

**问题：** 协程测试挂起或不可预测地失败。
**解决方案：** 确保使用 `runTest` 并将 `TestDispatcher` 注入到你的类中，以便控制虚拟时间。

## 局限性
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
