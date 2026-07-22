---
name: android-jetpack-compose-expert
description: "使用 Jetpack Compose 构建现代 Android UI 的专家指南，涵盖状态管理、导航、性能优化和 Material Design 3。触发词：Jetpack Compose、Compose UI、Android UI、声明式UI、Compose状态管理、Compose导航、Compose性能、Material3、Compose架构、MVI Compose、MVVM Compose"
risk: safe
source: community
date_added: "2026-02-27"
---

# Android Jetpack Compose 专家指南

## 概述

使用 Jetpack Compose 构建生产级 Android 应用的综合指南。本技能涵盖架构模式、使用 ViewModel 的状态管理、导航类型安全以及性能优化技术。

## 何时使用本技能

- 使用 Jetpack Compose 启动新 Android 项目时使用。
- 将旧版 XML 布局迁移到 Compose 时使用。
- 实现复杂 UI 状态管理和副作用时使用。
- 优化 Compose 性能（重组次数、稳定性）时使用。
- 设置类型安全导航时使用。

## 分步指南

### 1. 项目设置与依赖

确保 `libs.versions.toml` 包含必要的 Compose BOM 和库。

```kotlin
[versions]
composeBom = "2024.02.01"
activityCompose = "1.8.2"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
```

### 2. 状态管理模式（MVI/MVVM）

使用 `ViewModel` 配合 `StateFlow` 暴露 UI 状态。避免暴露 `MutableStateFlow`。

```kotlin
// UI 状态定义
data class UserUiState(
    val isLoading: Boolean = false,
    val user: User? = null,
    val error: String? = null
)

// ViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    fun loadUser() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val user = userRepository.getUser()
                _uiState.update { it.copy(user = user, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}
```

### 3. 创建 Screen Composable

在 "Screen" composable 中消费状态，并将数据向下传递给无状态组件。

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserContent(
        uiState = uiState,
        onRetry = viewModel::loadUser
    )
}

@Composable
fun UserContent(
    uiState: UserUiState,
    onRetry: () -> Unit
) {
    Scaffold { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when {
                uiState.isLoading -> CircularProgressIndicator()
                uiState.error != null -> ErrorView(uiState.error, onRetry)
                uiState.user != null -> UserProfile(uiState.user)
            }
        }
    }
}
```

## 示例

### 示例 1：类型安全导航

使用新版 Navigation Compose 类型安全（在最新版本中可用）。

```kotlin
// 定义目标页面
@Serializable
object Home

@Serializable
data class Profile(val userId: String)

// 设置 NavHost
@Composable
fun AppNavHost(navController: NavHostController) {
    NavHost(navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(onNavigateToProfile = { id ->
                navController.navigate(Profile(userId = id))
            })
        }
        composable<Profile> { backStackEntry ->
            val profile: Profile = backStackEntry.toRoute()
            ProfileScreen(userId = profile.userId)
        }
    }
}
```

## 最佳实践

- ✅ **应该：** 使用 `remember` 和 `derivedStateOf` 最小化重组期间的不必要计算。
- ✅ **应该：** 如果 UI 状态中使用的数据类包含 `List` 或其他不稳定类型，将其标记为 `@Immutable` 或 `@Stable` 以启用智能重组跳过。
- ✅ **应该：** 使用 `LaunchedEffect` 处理由状态变化触发的一次性副作用（如显示 Snackbar）。
- ❌ **不要：** 在没有 `remember` 的情况下直接在 Composable 函数体内执行耗时操作（如列表排序）。
- ❌ **不要：** 将 `ViewModel` 实例传递给子组件。只传递数据（状态）和 lambda 回调（事件）。

## 故障排除

**问题：** 无限重组循环。
**解决方案：** 检查是否在组合过程中创建了新对象实例（如 `List` 或 `Modifier`）而没有使用 `remember`，或者是否在组合阶段而非副作用或回调中更新状态。使用 Layout Inspector 调试重组次数。

## 局限性
- 仅当任务明确符合上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
