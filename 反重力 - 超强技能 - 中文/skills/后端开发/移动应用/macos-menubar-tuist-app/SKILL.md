---
name: macos-menubar-tuist-app
description: 构建、重构或审查使用 Tuist 的 SwiftUI macOS 菜单栏应用。当用户要求'构建 macOS 菜单栏应用'、'Tuist 菜单栏项目'、'menubar app'时使用。
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# macos-menubar-tuist-app

使用 Tuist 优先的工作流和稳定的启动脚本来构建和维护 macOS 菜单栏应用。保持严格的架构边界，使网络、状态和 UI 保持可测试和可预测。

## 适用场景

- 开发基于 LSUIElement 的 Tuist + SwiftUI 菜单栏工具时。
- 需要 Tuist 配置清单、启动脚本或菜单栏应用的架构指导时。

## 核心规则

- 除非明确要求，否则保持应用为纯菜单栏模式。默认使用 `LSUIElement = true`。
- 将网络传输和解码逻辑放在视图之外。不要在 SwiftUI 视图体中调用网络请求。
- 将状态转换放在 store 层（`@Observable` 或等价方案），而非行/视图展示代码中。
- 模型解码要能应对 API 变动：使用可选字段、安全回退和防御性解析。
- 将 Tuist 配置清单视为唯一真实来源。不要依赖手动编辑的 Xcode 生成产物。
- 当 `tuist run` 无法可靠解析 macOS 目标/设备时，优先使用脚本启动进行本地迭代。
- 在本地运行脚本中构建生成项目时，优先使用 `tuist xcodebuild build` 而非原始 `xcodebuild`。

## 文件布局

默认使用以下放置方式：

- `Project.swift`：应用 target、设置、资源、`Info.plist` 键
- `Sources/*Model*.swift`：API/领域模型和解码
- `Sources/*Client*.swift`：请求、响应映射、传输相关
- `Sources/*Store*.swift`：可观察状态、刷新策略、过滤、缓存
- `Sources/*Menu*View*.swift`：菜单组合和顶层 UI 状态
- `Sources/*Row*View*.swift`：行渲染和轻量交互
- `run-menubar.sh`：规范的本地重启/构建/启动路径
- `stop-menubar.sh`：需要时的显式停止辅助脚本

## 工作流

1. 确认 Tuist 管理权
- 验证 `Tuist.swift` 和 `Project.swift`（或 workspace 配置清单）存在。
- 修改启动行为前先读取现有运行脚本。

2. 编码前先探测后端行为
- 用 `curl` 验证端点结构、认证要求和分页行为。
- 如果端点忽略 `limit/page`，在 store 中实现全量列表处理和本地裁剪。

3. 自底向上实现各层
- 先定义/调整模型。
- 添加或更新 client 请求/解码逻辑。
- 更新 store 刷新、过滤和缓存策略。
- 最后连接视图。

4. 保持应用入口精简
- 应用入口只关注 scene/menu 连接和依赖注入。
- 不要在 `App` 或 menu scene 声明中嵌入业务逻辑。

5. 标准化启动操作
- 确保运行脚本在重新启动前先终止已有实例。
- 确保运行脚本不会打开 Xcode。
- 需要生成项目时使用 `tuist generate --no-open`。
- 运行脚本构建生成项目时，优先使用 `TUIST_SKIP_UPDATE_CHECK=1 tuist xcodebuild build ...` 而非直接调用原始 `xcodebuild`。

## 验证矩阵

编辑后运行验证：

```bash
TUIST_SKIP_UPDATE_CHECK=1 tuist xcodebuild build -scheme <TargetName> -configuration Debug
```

如果启动工作流有变更：

```bash
./run-menubar.sh
```

如果 shell 脚本有变更：

```bash
bash -n run-menubar.sh
bash -n stop-menubar.sh
./run-menubar.sh
```

## 常见故障与修复方向

- `tuist run` 无法解析 macOS 目标：
使用运行/停止脚本作为规范的本地运行路径。

- 菜单 UI 刷新后卡顿或不一致：
将派生状态和过滤移入 store；保持视图只负责渲染。

- API 负载变更导致解码失败：
用可选字段和默认值放宽模型解码，然后在 UI 中安全地展示缺失数据。

- 需求要求快速 UI 修补：
在修改行/菜单展示之前，先追溯 model/client/store 中的根因。

## 完成检查清单

- 除非明确变更，保持纯菜单栏行为。
- 网络和状态逻辑不要放在 SwiftUI 视图体中。
- Tuist 配置清单和运行脚本与实际构建/运行流程保持一致。
- 对涉及的区域运行验证矩阵。
- 报告具体执行的命令和结果。

## 局限性

- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来请求澄清。
