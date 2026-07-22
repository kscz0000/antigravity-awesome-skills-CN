# 组件索引

使用此文件查找组件和横切指导。每个条目标注了适用场景。

## 可用组件

- TabView：`references/tabview.md` — 构建标签页应用或任何标签式功能集时使用。
- NavigationStack：`references/navigationstack.md` — 需要推送导航和编程式路由时使用，尤其适用于每标签页独立历史。
- Sheet 与展示：`references/sheets.md` — 本地 item 驱动的 Sheet、集中式模态路由和 Sheet 专属操作模式。
- Form 与设置：`references/form.md` — 设置、分组输入和结构化数据录入。
- macOS 设置：`references/macos-settings.md` — 使用 SwiftUI Settings 场景构建 macOS 设置窗口时使用。
- 分栏视图与列：`references/split-views.md` — iPad/macOS 多列布局或自定义次级列。
- List 与 Section：`references/list.md` — 信息流内容和设置行。
- ScrollView 与 Lazy 堆栈：`references/scrollview.md` — 自定义布局、水平滚动器或网格。
- 滚动展示详情：`references/scroll-reveal.md` — 详情页面在用户滚动或滑动时展示次级内容或操作。
- 网格：`references/grids.md` — 图标选择器、媒体画廊和瓦片布局。
- 主题化与动态字体：`references/theming.md` — 应用级主题令牌、颜色和字体缩放。
- 控件（开关、选择器、滑块）：`references/controls.md` — 设置控件和输入选择。
- 输入工具栏（底部固定）：`references/input-toolbar.md` — 带固定输入栏的聊天/编辑器页面。
- 顶部栏覆盖层（iOS 26+ 及兼容方案）：`references/top-bar.md` — 滚动内容上方的固定选择器或胶囊栏。
- 覆盖层与 Toast：`references/overlay.md` — 横幅或 Toast 等临时 UI。
- 焦点处理：`references/focus.md` — 字段链接和键盘焦点管理。
- 搜索栏：`references/searchable.md` — 带范围和异步结果的原生搜索 UI。
- 异步图片与媒体：`references/media.md` — 远程媒体、预览和媒体查看器。
- 触觉反馈：`references/haptics.md` — 关键操作的触觉反馈。
- 匹配过渡：`references/matched-transitions.md` — 平滑的源到目标动画。
- 深度链接与 URL 路由：`references/deeplinks.md` — 应用内 URL 导航。
- 标题菜单：`references/title-menus.md` — 导航标题中的筛选或上下文菜单。
- 菜单栏命令：`references/menu-bar.md` — 添加或自定义 macOS/iPadOS 菜单栏命令。
- 加载与占位符：`references/loading-placeholders.md` — 骨架屏、空状态和加载 UX。
- 轻量级客户端：`references/lightweight-clients.md` — 小型、基于闭包的 API 客户端注入 store。

## 横切参考

- 应用连接与依赖图：`references/app-wiring.md` — 连接应用壳、安装共享依赖、决定什么应放在环境中。
- 异步状态与任务生命周期：`references/async-state.md` — 视图加载数据、响应变化输入或需要取消/防抖指导时使用。
- 预览：`references/previews.md` — 添加 `#Preview`、fixtures、mock 环境或隔离预览设置时使用。
- 性能防护：`references/performance.md` — 页面内容多、滚动密集、频繁更新或出现不必要的重渲染迹象时使用。

## 计划中的组件（按需创建文件）

- Web 内容：创建 `references/webview.md` — 嵌入式 Web 内容或应用内浏览。
- 状态编辑器模式：创建 `references/composer.md` — 组合或编辑器工作流。
- 文本输入与验证：创建 `references/text-input.md` — 表单、验证和文本密集输入。
- 设计系统使用：创建 `references/design-system.md` — 应用共享样式规则时使用。

## 添加条目

- 添加组件文件并在此处链接，附简短的"适用场景"描述。
- 每个组件参考保持简短且可操作。
