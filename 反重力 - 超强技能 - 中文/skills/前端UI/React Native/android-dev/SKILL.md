---
name: android-dev
description: "生产级 Android 应用开发指南，覆盖原生（Kotlin/Java）、跨平台（Flutter、RN、KMM）以及混合架构。触发词：Android 开发、安卓开发、原生 Android、Jetpack Compose、Kotlin Multiplatform、Flutter、React Native、混合架构、移动端架构。"
risk: safe
source: community
date_added: "2026-06-08"
---

# Android 应用开发技能

## 概述

本技能基于大型科技公司的实践，指导生产级 Android 及跨平台（非 iOS）应用开发，覆盖完整研发生命周期——架构、UI、代码质量、测试、错误处理、发布与维护。

## 何时使用本技能

- 选择技术栈时（参见 §1 技术栈选型）
- 搭建项目架构时（参见 §2 架构）
- 设计 UI、页面或设计系统时（参见 §3 UI 与设计）
- 保障代码质量、模式或 API 时（参见最佳实践）
- 实现错误处理或排查崩溃时（参见 §5 错误处理）
- 规划测试策略时（参见 §6 测试）
- 配置构建、CI/CD 或发布流水线时（参见 §7 构建与发布）
- 优化性能或内存时（参见 §8 性能）
- 调试或修复缺陷时（参见 §9 调试）
- 跟随完整开发路线图时（参见 §10 开发路线图）
- 需要某技术栈的深度参考时（参见 `references/` 目录）

---

## §1 技术栈选型

根据团队、需求与平台目标进行选择。**请勿推荐仅 iOS 的方案。**

### 原生 Android — Kotlin + Jetpack Compose
**适用场景：** 仅 Android 应用、硬件密集型功能、最佳用户体验、新项目。
- 语言：**Kotlin**
- UI：**Jetpack Compose**（现代化声明式 UI）
- 关键库：Room、Retrofit/Ktor、Hilt、WorkManager、DataStore、Navigation Compose
- 参考：`references/native-android.md`

### 原生 Android — Java + XML 视图
**适用场景：** 现有 Java 代码库、团队不熟悉 Kotlin、遗留应用维护、Kotlin 渐进式迁移。
- 语言：**Java**（Google 完整支持，并未弃用）
- UI：**XML 布局**（ConstraintLayout、RecyclerView、ViewBinding）
- 关键库：Room、Retrofit、Hilt、WorkManager、LiveData、ViewModel
- Java 与 Kotlin 在同一项目中**无缝共存**——可渐进式迁移
- 参考：`references/java-android.md`

### Flutter（Dart）
**适用场景：** 一套代码同时覆盖 Android + Web（+ 桌面）、快速迭代、像素级自定义 UI。
- 语言：**Dart**
- UI：Flutter Widget 树（Material 3 / Cupertino Widget 可用，但 Android 目标请使用 Material）
- 关键库：Provider/Riverpod/Bloc、Dio、Drift/Isar、go_router、flutter_local_notifications
- 参考：`references/flutter.md`

### React Native（JavaScript/TypeScript）
**适用场景：** Web + Android 代码复用、JS/TS 团队、生态丰富。
- 语言：**TypeScript**（推荐）
- UI：React Native 核心组件 + NativeWind / React Native Paper
- 关键库：React Navigation、Zustand/Redux Toolkit、React Query、MMKV
- 参考：`references/react-native.md`

### Kotlin Multiplatform（KMM / Compose Multiplatform）
**适用场景：** 在 Android + 桌面 + Web 之间共享业务逻辑，同时保留原生 Android UI。
- 语言：**Kotlin** 全场景
- UI：Android 使用原生 Compose；共享 UI 使用 Compose Multiplatform
- 关键库：Ktor、SQLDelight、Koin、kotlinx.serialization、Napier
- 参考：`references/kmm.md`

### 混合（Capacitor / Ionic）
**适用场景：** Web 优先团队、轻量应用、类 PWA 内容型应用。
- 语言：TypeScript + HTML/CSS
- UI：Ionic 组件或自定义 Web UI
- 避免场景：重型动画、访问原生传感器、高性能游戏
- 参考：`references/hybrid.md`

### 决策矩阵

| 需求 | 原生 Kotlin | 原生 Java | Flutter | RN | KMM | 混合 |
|---|---|---|---|---|---|---|
| 仅 Android（新建） | ✅ 最佳 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 仅 Android（已有 Java） | ⚠️ 迁移 | ✅ 最佳 | ❌ | ❌ | ⚠️ | ❌ |
| Android + Web | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ 最佳 |
| Android + 桌面 | ❌ | ❌ | ✅ | ⚠️ | ✅ | ⚠️ |
| 仅共享业务逻辑 | N/A | N/A | N/A | N/A | ✅ 最佳 | N/A |
| 原生性能 | ✅ | ✅ | ✅ | ⚠️ | ✅ | ❌ |
| JS/TS 团队 | ❌ | ❌ | ❌ | ✅ 最佳 | ❌ | ✅ |
| 像素级自定义 UI | ✅ | ⚠️ | ✅ 最佳 | ⚠️ | ✅ | ❌ |

---

## §2 架构

### 核心原则：关注点分离
每个生产级 Android 项目都必须将 **UI**、**业务逻辑** 与 **数据** 分离为独立、可单独测试的层级。

### 推荐架构：Clean Architecture + MVI/MVVM

```
app/
├── ui/              # Composables / Activities / Fragments / 屏幕状态
├── presentation/    # ViewModel、UI 状态、UI 事件
├── domain/          # 用例、领域模型、仓库接口
├── data/            # 仓库实现、远程（API）、本地（数据库）、映射器
└── di/              # 依赖注入模块
```

**数据流（单向）：**
```
用户操作 → ViewModel/Store → 用例 → 仓库 → 数据源
                    ↓
             UI 状态（sealed class / StateFlow）
                    ↓
             Composable / View 渲染状态
```

### 各技术栈的关键架构模式

**原生（MVVM + MVI）：**
- 使用 `StateFlow` / `SharedFlow` 进行响应式状态管理
- `sealed class UiState` + `sealed class UiEvent`
- 使用 Hilt 进行依赖注入，使用协程 + Flow 处理异步
- Repository 模式包装 Room + Retrofit

**Flutter（BLoC 或 Riverpod）：**
- 使用 `Bloc` 或 `Cubit` 实现业务逻辑隔离
- 使用 `AsyncNotifierProvider`（Riverpod）管理数据与状态
- 仓库以抽象类形式定义，通过注入提供实现

**React Native（Redux Toolkit 或 Zustand）：**
- 使用 RTK Query 或 React Query 管理服务端状态
- 使用 Zustand 切片管理客户端状态
- 通过自定义 Hook 封装每个功能的业务逻辑

**KMM：**
- 共享 `commonMain` 承载领域层与数据层
- 使用 `expect/actual` 实现平台相关代码
- Kotlin 协程 + Flow 桥接到平台（Android 上为 StateFlow）

### 模块结构（大型应用的多模块拆分）

```
:app            # 入口、依赖注入装配
:core:ui        # 设计系统、共享 Composable
:core:network   # API 客户端、拦截器
:core:database  # Room / SQLDelight 配置
:feature:home
:feature:profile
:feature:settings
```

---

## §3 UI 与设计

### 设计系统先行
在编写页面之前，先定义：
1. **颜色令牌**——主色、辅色、表面色、表面之上的颜色、错误色；明暗双套变体
2. **字号体系**——Display、Headline、Title、Body、Label（Material 3 字号体系）
3. **间距体系**——4dp 网格（4、8、12、16、24、32、48dp）
4. **形状令牌**——每个组件族的圆角
5. **组件库**——Button、TextField、Card、BottomSheet、TopAppBar 等

### Jetpack Compose UI 规范
- 使用 `MaterialTheme` 令牌；禁止硬编码颜色或尺寸
- 使用 `CompositionLocal` 注入主题、语言、触感反馈
- 正确使用 `remember` / `rememberSaveable`（`saveable` 用于跨屏幕旋转存活的 UI 状态）
- 将大型 Composable 拆分为子 Composable；单个函数 ≤ 80 行
- 列表场景使用 `LazyColumn`/`LazyVerticalGrid`；禁止在 `Column` 内用 forEach 渲染大量数据
- 副作用仅出现在 `LaunchedEffect`、`DisposableEffect`、`SideEffect` 中
- 避免状态提升反模式：将状态提升到最近的共同祖先

### 无障碍（不可妥协）
- 所有可交互元素必须有 `contentDescription` 或 `semantics { }`
- 最小可点击区域：**48×48dp**
- 每次发版前进行 `TalkBack` 兼容性测试
- 支持动态字号（文字使用 `sp` 而非 `dp`）
- 颜色对比度 ≥ 4.5:1（WCAG AA）

### 导航
- **原生：** Navigation Compose + 类型化的 `NavHost` 与 `SafeArgs` 等价方案
- **Flutter：** `go_router` + 命名路由与守卫
- **RN：** React Navigation v7 + 类型化的 `NavigationProp`
- 每个可从外部打开的页面都注册深链接处理
- 谨慎管理返回栈——禁止重复入栈，使用 `popUpTo` / `launchSingleTop`

### 响应式与自适应 UI
- 支持所有屏幕尺寸：手机、可折叠设备、平板（`WindowSizeClass`）
- 在 320dp、360dp、411dp、600dp+、840dp+ 宽度下测试
- 通过 `WindowInfoTracker` 感知可折叠铰链
- Android 15+ 必须启用 Edge-to-Edge 显示并处理 `WindowInsets`

---

## 最佳实践

### 语言规范

**Kotlin：**
- 根据场景选用 `data class`、`sealed class`、`object`、`enum class`
- 禁止 `!!` 非空断言——使用 `?.let`、`?: return` 或带提示信息的 `requireNotNull`
- 协程：始终显式指定 `CoroutineScope` + `Dispatcher`；禁止使用 `GlobalScope`
- 在 Compose 状态类上使用 `@Stable` / `@Immutable` 以实现智能重组

**Java：**
- 每个方法的参数与返回值都标注 `@NonNull` / `@Nullable`
- 禁止在未检查的对象上调用方法——显式进行空检查或使用 `Objects.requireNonNull`
- 在 Fragment 的 `onDestroyView()` 中始终将 `binding` 引用置空，防止内存泄漏
- 后台任务使用 `ExecutorService`（`AsyncTask` 已弃用）；或使用 `LiveData` + Room 自带的线程切换
- 在 RecyclerView 中优先使用 `ListAdapter` + `DiffUtil` 而非手动 `notifyDataSetChanged()`
- 使用 `ViewBinding`——禁止使用 `findViewById`

**Dart（Flutter）：**
- 必须启用空安全——禁止在未显式空检查的情况下使用 `!`
- 不可变状态对象搭配 `copyWith`
- 所有无状态 Widget 使用 `const` 构造函数

**TypeScript（RN）：**
- `tsconfig` 中始终启用 `strict: true`
- 使用 Zod 或 io-ts 对 API 响应进行运行时类型校验
- 禁止使用 `any`——使用 `unknown` 并收窄类型

### 依赖管理
- 在 `build.gradle.kts` / `pubspec.yaml` / `package.json` 中固定所有依赖版本
- 每月审计依赖安全漏洞
- 避免传递依赖冲突——使用依赖解析策略
- 保持依赖数量最小——每多一个库都增加维护负担

### 代码审查清单（PR 准入门槛）
- [ ] 新公共 API 有 KDoc / DartDoc / JSDoc
- [ ] 无硬编码字符串——使用字符串资源 / l10n
- [ ] 设计令牌之外无硬编码尺寸或颜色
- [ ] 主线程无阻塞 I/O
- [ ] 无内存泄漏（单例中不持有 `Activity` Context）
- [ ] 协程作用域 / 流已正确取消 / 释放
- [ ] 任何非平凡功能都受特性开关保护

---

## §5 错误处理

### 黄金法则
**绝不能让异常静默传播给用户或直接导致应用崩溃。**

### 错误分类

| 类型 | 策略 |
|------|------|
| 网络错误 | 指数退避重试；展示重试 UI |
| 鉴权错误（401/403） | 刷新令牌 → 重新请求 → 失败则登出 |
| 校验错误 | 立即展示字段内联错误 |
| 数据解析错误 | 记录日志 + 回退到缓存/默认状态 |
| 意外崩溃 | 在顶层捕获；展示错误页 + 上报 |
| 后台任务失败 | 通过 WorkManager 重试；关键任务通知用户 |

### Result / Either 模式（Kotlin）
```kotlin
sealed class AppResult<out T> {
    data class Success<T>(val data: T) : AppResult<T>()
    data class Error(val exception: AppException) : AppResult<Nothing>()
}

sealed class AppException(msg: String) : Exception(msg) {
    class NetworkException(msg: String) : AppException(msg)
    class AuthException(msg: String) : AppException(msg)
    class ParseException(msg: String) : AppException(msg)
    class UnknownException(msg: String) : AppException(msg)
}
```

仓库与用例函数全部以 `AppResult<T>` 作为返回类型。ViewModel 将其映射为 `UiState.Error`。

### 崩溃上报
- 从第一天起集成 **Firebase Crashlytics** 或 **Sentry**
- 在崩溃发生前设置用户标识与自定义键
- 所有捕获到的错误均记录为非致命异常
- 启用 ANR 监控
- 无崩溃会话比例目标：**≥ 99.5%**

### 离线 / 网络韧性
- 缓存优先策略：先展示旧数据，后台拉取新数据
- `Room` / `Drift` / `MMKV` 作为单一数据源
- 通过 `ConnectivityManager` 暴露网络状态并在 UI 上体现
- 所有网络调用都包装超时与重试策略

---

## §6 测试

### 测试金字塔

```
         /\
        /E2E\        ← 10%  (UI 测试：Espresso、Maestro、Appium)
       /------\
      / 集成   \     ← 20%  (仓库、数据库、API 契约测试)
     /----------\
    /    单元    \   ← 70%  (ViewModel、用例、工具类)
   /--------------\
```

### 单元测试（70%）
- 每个 ViewModel、用例、仓库、映射器都需覆盖
- **原生：** JUnit5 + MockK + Turbine（Flow 测试）+ Kotest 断言
- **Flutter：** `flutter_test` + `mocktail`
- **RN：** Jest + `@testing-library/react-native` + `msw` 模拟 API
- 覆盖率目标：领域层 + 表现层 **≥ 80%**

### 集成测试（20%）
- 使用内存数据库进行 Room DB 测试
- 使用 `MockWebServer`（OkHttp）进行 Retrofit/Ktor 测试
- 验证仓库的缓存与远程协同
- 针对真实预发布环境进行 API 契约测试

### UI / 端到端测试（10%）
- **Espresso** 用于关键用户旅程（登录、结算、核心操作）
- **Maestro** 用于跨平台端到端流程（Flutter + RN 也推荐）
- 发版前在真实设备农场（Firebase Test Lab / BrowserStack）上运行
- 每个 PR 触发冒烟测试；完整 E2E 套件夜间运行

### 测试数据管理
- 使用工厂 / 构建器生成测试数据，禁止复制粘贴对象
- 密封测试：测试用例之间禁止共享可变状态
- 复杂依赖（仓库、数据源）优先使用假对象而非 Mock

---

## §7 构建与发布

### 构建变体
```
debug       → 开发 API，开启日志，无混淆，可调试
staging     → 预发布 API，开启日志，已混淆，不可调试
release     → 生产 API，关闭日志，已混淆，已签名
```

### Gradle 最佳实践（原生）
- 仅使用 `build.gradle.kts`——新项目禁止使用 Groovy DSL
- 使用版本目录（`libs.versions.toml`）管理所有依赖版本
- 使用 `buildConfig` 管理环境相关的常量
- 使用 Baseline Profile 优化启动性能
- Release 启用 R8 全模式；ProGuard 规则纳入版本控制

### CI/CD 流水线

```
PR 提交
  └─ lint + 单元测试 + 构建 debug APK          [< 5 分钟]

合并到 main
  └─ 单元 + 集成测试 + staging 构建           [< 15 分钟]
  └─ 部署到 Firebase App Distribution（QA）

发布标签
  └─ 完整测试套件 + 设备农场 E2E             [< 45 分钟]
  └─ 构建 release AAB
  └─ 上传到 Play Console（内部测试轨道）
  └─ 推进：内部 → 封闭测试 → 开放测试 → 正式发布
```

**推荐 CI：** GitHub Actions、Bitrise 或 CircleCI。

### Play Store 发布策略
- 正式发布前必须经过 **内部 → 封闭 → 开放测试**
- 使用**分阶段发布**：5% → 20% → 50% → 100%，每个阶段监控 24-48 小时
- 扩大发布前监控 Crashlytics + ANR 率 + 评分
- 重大变更**不得跳过分阶段发布**

### 应用签名
- 上传密钥（Play App Signing）：存储在 CI 密钥库中，禁止提交到仓库
- 使用 Google Play App Signing 管理分发密钥
- 在团队运行手册中记录密钥恢复流程

---

## §8 性能

### 启动性能
- 应用启动时间目标：**冷启动 < 1 秒**，**温启动 < 500 毫秒**
- 使用 **App Startup 库** 延迟初始化第三方库
- Baseline Profile 生成后提交到代码库
- 重量级初始化移出主线程

### UI 性能
- 目标：**60fps**（支持的设备上 90/120fps）；**零卡顿**
- 使用 **Android Studio Profiler** + `FrameMetrics` API 进行度量
- 避免在 `draw()` / `onMeasure()` / 组合中分配对象
- 在 Compose 中使用 `derivedStateOf` 避免不必要的重组
- 图片加载：Coil（Compose）/ Glide / Picasso——禁止在缩略图中加载原图

### 内存
- ViewModel 与单例中禁止持有 `Activity` / `Context` 引用
- 跨越生命周期持有监听器时使用 `WeakReference`
- 位图回收与内存缓存容量配置
- 通过 **LeakCanary** 在 debug 构建中进行堆转储 + 泄漏检测（始终启用）

### 网络
- 遵守 HTTP 缓存头
- 使用图片 CDN + WebP 格式
- 验证 Gzip/Brotli 压缩
- 必要时进行请求合并
- 配置连接池

### 电量
- 后台任务仅通过带合适约束的 **WorkManager** 调度
- 定位更新：仅请求所需精度；进入后台时停止
- 谨慎使用 Wakelock，并显式释放

---

## §9 调试与缺陷修复

### 调试流程

1. **稳定复现**——记录精确步骤、设备、操作系统版本、账号状态
2. **隔离**——属于 UI、业务逻辑、网络还是持久化？
3. **埋点**——加入有针对性的日志 / 断点，禁止撒网式日志
4. **假设**——动手修改前提出 1-3 个具体假设
5. **修复根因**——不要打补丁掩盖症状；追溯到源头
6. **回归测试**——编写修复前失败、修复后通过的测试
7. **记录**——注释说明修复为何生效，而不仅仅是做了什么

### 常见 Android 缺陷模式

| 缺陷 | 可能原因 | 修复 |
|-----|---------|------|
| ANR | 主线程 I/O / 长时计算 | 改用协程/Dispatcher.IO |
| 内存泄漏 | 单例持有 Context | 使用 `applicationContext`；WeakRef |
| 屏幕旋转崩溃 | 未使用 ViewModel；状态未保存 | `rememberSaveable` / ViewModel |
| UI 卡顿 | 重组循环 | `derivedStateOf`、稳定参数 |
| API 调用后白屏 | 错误被静默吞掉 | 检查错误状态传播 |
| 深链接失效 | Manifest 缺少 intent-filter | 通过 `adb shell am start` 验证 |
| 推送通知静默 | 后台限制 | 在多厂商真机上测试 |

### 日志规范
- **生产环境：** 仅使用 Firebase Crashlytics（release 构建中禁止 `Log.d`）
- **Debug/Staging：** 使用 Timber 配合 DebugTree
- 日志级别：ERROR（崩溃）、WARN（可恢复）、INFO（关键事件）、DEBUG（仅开发）
- 禁止记录 PII——日志中需对邮箱、电话、令牌脱敏

### 厂商特定问题
- 在 **Samsung**、**Xiaomi/MIUI**、**OnePlus/OxygenOS**、**华为（无 GMS）** 上对关键流程进行测试
- 各厂商对后台限制差异巨大——测试推送、闹钟、后台同步
- 维护一份物理或云端设备农场，覆盖头部市场份额机型

---

## §10 开发路线图

任何新 Android 项目都应遵循以下阶段结构：

### 阶段 0 —— 基础（第 1-2 周）
- [ ] 技术栈决策文档化，含选型理由
- [ ] 定义模块结构
- [ ] 定义设计系统令牌（颜色、字号、间距、形状）
- [ ] CI 流水线已运行（lint + 单元测试 + 构建）
- [ ] 集成崩溃上报（Crashlytics/Sentry）
- [ ] 集成基础分析（Firebase/Amplitude）
- [ ] API 契约 / Mock 服务器已搭建
- [ ] DI 框架已配置
- [ ] 导航骨架已实现
- [ ] Flavor / 构建变体配置完成

### 阶段 1 —— 核心功能（第 3-8 周）
- [ ] 鉴权流程（登录、注册、令牌刷新、登出）
- [ ] 核心页面框架，含真实导航
- [ ] 网络层（客户端、拦截器、错误处理）
- [ ] 本地持久化层（数据库 schema + DAO）
- [ ] 仓库层连接远程与本地
- [ ] 每个功能的 ViewModel + UI 状态
- [ ] 所有 ViewModel 与用例的单元测试
- [ ] 特性开关基础设施

### 阶段 2 —— 打磨（第 9-12 周）
- [ ] 基于 Figma/规范的 Design QA
- [ ] 无障碍审计（TalkBack、对比度、可点击区域）
- [ ] 暗色模式实现与验证
- [ ] 本地化（字符串外置、RTL 支持如需要）
- [ ] 每个页面都有加载、空、错误状态
- [ ] 深链接处理
- [ ] Widget / 通知实现
- [ ] 离线模式验证

### 阶段 3 —— 加固（第 12-14 周）
- [ ] 性能剖析（启动、滚动、内存）
- [ ] 设备农场（Firebase Test Lab）上的 E2E 测试套件
- [ ] 安全审查（证书绑定、生物识别、安全存储）
- [ ] Proguard / R8 规则已验证
- [ ] staging 环境无崩溃率 ≥ 99.5%
- [ ] Play Store 商品详情、截图、隐私政策

### 阶段 4 —— 发布
- [ ] AAB 已签名并上传到内部测试轨道
- [ ] 分阶段发布计划已制定
- [ ] 监控仪表盘已搭建（Crashlytics、Play Console vitals）
- [ ] 回滚方案已文档化
- [ ] 已分配值守轮值

### 阶段 5 —— 上市后（持续）
- 每日监控无崩溃率
- ANR 率 < 0.47%（Play Store 阈值）
- 监控应用评分；每周处理差评
- 每月评估依赖更新
- 每次新 Android 版本发布进行 Beta 测试

---

## 局限性

- 本技能范围限定在 Android 及 Android 相关的交付路径；不覆盖仅 iOS 的架构、App Store 发布操作或 Apple 平台 UI 指南。
- 版本号、Play Console 政策阈值与推荐库可能变化；发布前请对照当前 Android、Google Play 与库文档核实关键细节。
- 代码片段是架构模式而非完整应用；请根据实际项目调整包名、依赖版本、权限、隐私披露与安全控制。
- 本指南不能替代生产发布所需的设备 QA、无障碍审查、安全审查、法律 / 隐私审查或商店合规检查。

## 补充资源

需要深入了解特定技术栈时，请阅读：
- `references/native-android.md` — Kotlin、Compose、Room、Hilt、协程
- `references/java-android.md` — Java、XML 视图、ViewBinding、LiveData、Retrofit、Room、Hilt、迁移路径
- `references/flutter.md` — Dart、BLoC/Riverpod、Drift、go_router
- `references/react-native.md` — TypeScript、RN 架构、Hermes、新架构
- `references/kmm.md` — KMM 共享模块、SQLDelight、Ktor、Compose Multiplatform
- `references/hybrid.md` — Capacitor、Ionic、PWA 考量