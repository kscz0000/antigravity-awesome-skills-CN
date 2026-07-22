---
name: multi-platform-apps-multi-platform
description: "使用 API 优先架构和平行实现策略，在 Web、移动端和桌面端之间一致地构建和部署相同功能。当用户要求跨平台功能开发、多端一致性实现或 API 优先架构设计时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 多平台功能开发工作流

使用 API 优先架构和平行实现策略，在 Web、移动端和桌面端之间一致地构建和部署相同功能。

[深度思考：此工作流编排多个专业智能体，确保跨平台功能对等的同时保持平台特定优化。协调策略强调共享合约和并行开发，配合定期同步点。通过预先建立 API 契约和数据模型，团队可以独立工作同时确保一致性。工作流的优势包括更快的上市时间、更少的集成问题以及可维护的跨平台代码库。]

## 使用此技能的场景

- 处理多平台功能开发工作流任务或流程
- 需要多平台功能开发的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与多平台功能开发工作流无关
- 需要此范围之外的其他领域或工具

## 指引

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 阶段一：架构与 API 设计（顺序执行）

### 1. 定义功能需求与 API 契约
- 使用 Task 工具，subagent_type="backend-architect"
- 提示词："为功能设计 API 契约：$ARGUMENTS。创建 OpenAPI 3.1 规范，包含：
  - RESTful 端点，使用正确的 HTTP 方法和状态码
  - GraphQL schema（适用于复杂数据查询）
  - WebSocket 事件（用于实时功能）
  - 请求/响应 schema 及验证规则
  - 认证和授权要求
  - 限流和缓存策略
  - 错误响应格式和错误码
  定义所有平台将使用的共享数据模型。"
- 预期输出：完整的 API 规范、数据模型和集成指南

### 2. 设计系统与 UI/UX 一致性
- 使用 Task 工具，subagent_type="ui-ux-designer"
- 提示词："使用 API 规范为功能创建跨平台设计系统：[前一步输出]。包含：
  - 各平台组件规范（Material Design、iOS HIG、Fluent）
  - Web 响应式布局（移动优先方案）
  - iOS（SwiftUI）和 Android（Material You）原生模式
  - 桌面端特定考虑（键盘快捷键、窗口管理）
  - 无障碍要求（WCAG 2.2 Level AA）
  - 深色/浅色主题规范
  - 动画和过渡指南"
- 上下文来源：API 端点、数据结构、认证流程
- 预期输出：设计系统文档、组件库规范、平台指南

### 3. 共享业务逻辑架构
- 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
- 提示词："为跨平台功能设计共享业务逻辑架构。定义：
  - 核心领域模型和实体（平台无关）
  - 业务规则和验证逻辑
  - 状态管理模式（MVI/Redux/BLoC）
  - 缓存和离线策略
  - 错误处理和重试策略
  - 平台特定适配器模式
  考虑使用 Kotlin Multiplatform 用于移动端或 TypeScript 用于 Web/桌面端共享。"
- 上下文来源：API 契约、数据模型、UI 需求
- 预期输出：共享代码架构、平台抽象层、实现指南

## 阶段二：并行平台实现

### 4a. Web 实现（React/Next.js）
- 使用 Task 工具，subagent_type="frontend-developer"
- 提示词："使用以下技术实现 Web 版本：
  - React 18+ 配合 Next.js 14+ App Router
  - TypeScript 确保类型安全
  - TanStack Query 用于 API 集成：[API 规范]
  - Zustand/Redux Toolkit 用于状态管理
  - Tailwind CSS 配合设计系统：[设计规范]
  - Progressive Web App 能力
  - 适当使用 SSR/SSG 优化
  - Web Vitals 优化（LCP < 2.5s，FID < 100ms）
  遵循共享业务逻辑：[架构文档]"
- 上下文来源：API 契约、设计系统、共享逻辑模式
- 预期输出：完整的 Web 实现及测试

### 4b. iOS 实现（SwiftUI）
- 使用 Task 工具，subagent_type="ios-developer"
- 提示词："使用以下技术实现 iOS 版本：
  - SwiftUI 配合 iOS 17+ 特性
  - Swift 5.9+ 配合 async/await
  - URLSession 配合 Combine 用于 API：[API 规范]
  - Core Data/SwiftData 用于持久化
  - 设计系统合规：[iOS HIG 规范]
  - Widget 扩展（如适用）
  - 平台特定功能（Face ID、Haptics、Live Activities）
  - 可测试的 MVVM 架构
  遵循共享模式：[架构文档]"
- 上下文来源：API 契约、iOS 设计指南、共享模型
- 预期输出：原生 iOS 实现及单元/UI 测试

### 4c. Android 实现（Kotlin/Compose）
- 使用 Task 工具，subagent_type="mobile-developer"
- 提示词："使用以下技术实现 Android 版本：
  - Jetpack Compose 配合 Material 3
  - Kotlin coroutines 和 Flow
  - Retrofit/Ktor 用于 API：[API 规范]
  - Room 数据库用于本地存储
  - Hilt 用于依赖注入
  - Material You 动态主题：[设计规范]
  - 平台功能（生物认证、小组件）
  - Clean Architecture 配合 MVI 模式
  遵循共享逻辑：[架构文档]"
- 上下文来源：API 契约、Material Design 规范、共享模式
- 预期输出：原生 Android 实现及测试

### 4d. 桌面端实现（可选 - Electron/Tauri）
- 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
- 提示词："使用 Tauri 2.0 或 Electron 实现桌面版本：
  - 尽可能复用 Web 代码库
  - 原生操作系统集成（系统托盘、通知）
  - 文件系统访问（如需要）
  - 自动更新功能
  - 代码签名和公证设置
  - 键盘快捷键和菜单栏
  - 多窗口支持（如适用）
  复用 Web 组件：[Web 实现]"
- 上下文来源：Web 实现、桌面端特定需求
- 预期输出：桌面应用及平台安装包

## 阶段三：集成与验证

### 5. API 文档与测试
- 使用 Task 工具，subagent_type="documentation-generation::api-documenter"
- 提示词："创建完整的 API 文档，包括：
  - 交互式 OpenAPI/Swagger 文档
  - 平台特定集成指南
  - 各平台 SDK 示例
  - 认证流程图
  - 限流和配额信息
  - Postman/Insomnia 集合
  - WebSocket 连接示例
  - 错误处理最佳实践
  - API 版本管理策略
  使用平台实现测试所有端点。"
- 上下文来源：已实现的平台、API 使用模式
- 预期输出：完整的 API 文档门户、测试结果

### 6. 跨平台测试与功能对等
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："验证所有平台的功能对等性：
  - 功能测试矩阵（功能表现一致）
  - UI 一致性验证（遵循设计系统）
  - 各平台性能基准
  - 无障碍测试（平台特定工具）
  - 网络韧性测试（离线、慢速连接）
  - 数据同步验证
  - 平台特定边界情况
  - 端到端用户旅程测试
  创建测试报告，记录所有平台差异。"
- 上下文来源：所有平台实现、API 文档
- 预期输出：测试报告、对等性矩阵、性能指标

### 7. 平台特定优化
- 使用 Task 工具，subagent_type="application-performance::performance-engineer"
- 提示词："优化各平台实现：
  - Web：包体积、懒加载、CDN 配置、SEO
  - iOS：应用体积、启动时间、内存使用、电量
  - Android：APK 体积、启动时间、帧率、电量
  - Desktop：二进制体积、资源使用、启动时间
  - API：响应时间、缓存、压缩
  在保持功能对等的同时利用平台优势。
  记录优化技术和权衡取舍。"
- 上下文来源：测试结果、性能指标
- 预期输出：优化后的实现、性能提升

## 配置选项

- **--platforms**：指定目标平台（web,ios,android,desktop）
- **--api-first**：在 UI 实现之前生成 API（默认：true）
- **--shared-code**：使用 Kotlin Multiplatform 或类似方案（默认：evaluate）
- **--design-system**：使用现有或创建新设计系统（默认：create）
- **--testing-strategy**：单元测试、集成测试、端到端测试（默认：all）

## 成功标准

- API 契约在实现前定义并验证
- 所有平台实现功能对等，差异 <5%
- 性能指标满足平台特定标准
- 无障碍标准达标（最低 WCAG 2.2 AA）
- 跨平台测试显示一致行为
- 所有平台文档完整
- 平台间代码复用率 >40%（适用情况下）
- 用户体验针对各平台惯例优化

## 平台特定注意事项

**Web**：PWA 能力、SEO 优化、浏览器兼容性
**iOS**：App Store 指南、TestFlight 分发、iOS 特定功能
**Android**：Play Store 要求、Android App Bundles、设备碎片化
**Desktop**：代码签名、自动更新、操作系统特定安装程序

初始功能规格：$ARGUMENTS

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果所需输入、权限、安全边界或成功标准缺失，请停下来请求澄清。
