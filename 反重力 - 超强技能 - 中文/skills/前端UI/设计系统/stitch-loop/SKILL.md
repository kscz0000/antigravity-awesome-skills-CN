---
name: stitch-loop
description: |
  教导智能体使用 Stitch 进行迭代式网站构建，采用自主接力棒传递循环模式。当用户要求"用 Stitch 构建网站"、"迭代式网站开发"、"自主前端构建"、"Stitch 循环模式"、"baton-passing loop"、"Stitch 自动化构建"时使用此技能。
allowed-tools:
  - "stitch*:*"
  - "chrome*:*"
  - "Read"
  - "Write"
  - "Bash"
risk: unknown
source: community
---

# Stitch 构建循环

你是一个**自主前端构建器**，参与迭代式站点构建循环。你的目标是使用 Stitch 生成页面，将其集成到站点中，并为下一次迭代准备指令。

## 何时使用

- 你正在使用 Stitch 通过跨运行或跨智能体的接力式循环迭代构建网站。
- 每次迭代应读取下一个提示词、生成或集成页面，并交接下一个任务。
- 你需要一个规范化的自主循环来实现多步骤前端站点构建。

## 概述

构建循环模式通过"接力棒"系统实现持续、自主的网站开发。每次迭代：
1. 从接力棒文件（`.stitch/next-prompt.md`）读取当前任务
2. 使用 Stitch MCP 工具生成页面
3. 将页面集成到站点结构中
4. 将下一个任务写入接力棒文件，为下一次迭代做准备

## 前置条件

**必需：**
- 访问 Stitch MCP Server
- 一个 Stitch 项目（已存在或将要创建）
- 一个 `.stitch/DESIGN.md` 文件（如需要可使用 `design-md` 技能生成）
- 一个 `.stitch/SITE.md` 文件，记录站点愿景和路线图

**可选：**
- Chrome DevTools MCP Server — 支持对生成的页面进行可视化验证

## 接力棒系统

`.stitch/next-prompt.md` 文件充当迭代之间的接力棒：

```markdown
---
page: about
---
A page describing how jules.top tracking works.

**DESIGN SYSTEM (REQUIRED):**
[Copy from .stitch/DESIGN.md Section 6]

**Page Structure:**
1. Header with navigation
2. Explanation of tracking methodology
3. Footer with links
```

**关键规则：**
- YAML frontmatter 中的 `page` 字段决定输出文件名
- 提示词内容必须包含来自 `.stitch/DESIGN.md` 的设计系统块
- 你**必须**在完成工作前更新此文件以继续循环

## 执行协议

### 步骤 1：读取接力棒

解析 `.stitch/next-prompt.md` 以提取：
- 从 `page` frontmatter 字段获取**页面名称**
- 从 markdown 正文获取**提示词内容**

### 步骤 2：查阅上下文文件

生成之前，读取以下文件：

| 文件 | 用途 |
|------|------|
| `.stitch/SITE.md` | 站点愿景、**Stitch Project ID**、现有页面（站点地图）、路线图 |
| `.stitch/DESIGN.md` | Stitch 提示词所需的视觉样式 |

**重要检查：**
- Section 4（站点地图）— 不要重新创建已存在的页面
- Section 5（路线图）— 如果有待办事项，从这里选取任务
- Section 6（创意自由）— 如果路线图为空，从这里选取新页面创意

### 步骤 3：使用 Stitch 生成

使用 Stitch MCP 工具生成页面：

1. **发现命名空间**：运行 `list_tools` 查找 Stitch MCP 前缀
2. **获取或创建项目**：
   - 如果 `.stitch/metadata.json` 存在，使用其中的 `projectId`
   - 否则，调用 `[prefix]:create_project`，然后调用 `[prefix]:get_project` 获取完整项目详情，并保存到 `.stitch/metadata.json`（见下方 schema）
   - 生成每个屏幕后，再次调用 `[prefix]:get_project` 并用每个屏幕的完整元数据（id、sourceScreen、dimensions、canvas position）更新 `.stitch/metadata.json` 中的 `screens` 映射
3. **生成屏幕**：调用 `[prefix]:generate_screen_from_text`，参数为：
   - `projectId`：项目 ID
   - `prompt`：来自接力棒的完整提示词（包含设计系统块）
   - `deviceType`：`DESKTOP`（或按指定）
4. **获取资源**：下载前，检查 `.stitch/designs/{page}.html` 和 `.stitch/designs/{page}.png` 是否已存在：
   - **如果文件已存在**：询问用户是从 Stitch 项目刷新设计还是复用现有本地文件。仅在用户确认时重新下载。
   - **如果文件不存在**：继续下载：
     - `htmlCode.downloadUrl` — 下载并保存为 `.stitch/designs/{page}.html`
     - `screenshot.downloadUrl` — 在下载前向 URL 追加 `=w{width}`，其中 `{width}` 是屏幕元数据中的 `width` 值（Google CDN 默认提供低分辨率缩略图）。保存为 `.stitch/designs/{page}.png`

### 步骤 4：集成到站点

1. 将生成的 HTML 从 `.stitch/designs/{page}.html` 移动到 `site/public/{page}.html`
2. 修复所有资源路径，使其相对于 public 文件夹
3. 更新导航：
   - 查找现有占位符链接（如 `href="#"`）并将其连接到新页面
   - 如果合适，将新页面添加到全局导航
4. 确保所有页面的页眉/页脚一致

### 步骤 4.5：可视化验证（可选）

如果 **Chrome DevTools MCP Server** 可用，验证生成的页面：

1. **检查可用性**：运行 `list_tools` 查看 `chrome*` 工具是否存在
2. **启动开发服务器**：使用 Bash 启动本地服务器（如 `npx serve site/public`）
3. **导航到页面**：调用 `[chrome_prefix]:navigate` 打开 `http://localhost:3000/{page}.html`
4. **捕获截图**：调用 `[chrome_prefix]:screenshot` 捕获渲染后的页面
5. **可视化对比**：与 Stitch 截图（`.stitch/designs/{page}.png`）对比以验证保真度
6. **停止服务器**：终止开发服务器进程

> **注意：** 此步骤是可选的。如果未安装 Chrome DevTools MCP，跳至步骤 5。

### 步骤 5：更新站点文档

修改 `.stitch/SITE.md`：
- 将新页面添加到 Section 4（站点地图），标记为 `[x]`
- 从 Section 6（创意自由）中移除你已使用的创意
- 如果你完成了待办事项，更新 Section 5（路线图）

### 步骤 6：准备下一个接力棒（关键）

**你必须在完成之前更新 `.stitch/next-prompt.md`。** 这能保持循环继续。

1. **决定下一个页面**：
   - 检查 `.stitch/SITE.md` Section 5（路线图）中的待办事项
   - 如果为空，从 Section 6（创意自由）中选取
   - 或发明符合站点愿景的新内容
2. **编写接力棒**，包含正确的 YAML frontmatter：

```markdown
---
page: achievements
---
A competitive achievements page showing developer badges and milestones.

**DESIGN SYSTEM (REQUIRED):**
[Copy the entire design system block from .stitch/DESIGN.md]

**Page Structure:**
1. Header with title and navigation
2. Badge grid showing unlocked/locked states
3. Progress bars for milestone tracking
```

## 文件结构参考

```
project/
├── .stitch/
│   ├── metadata.json   # Stitch 项目和屏幕 ID（持久化！）
│   ├── DESIGN.md       # 视觉设计系统（来自 design-md 技能）
│   ├── SITE.md         # 站点愿景、站点地图、路线图
│   ├── next-prompt.md  # 接力棒 — 当前任务
│   └── designs/        # Stitch 输出的暂存区
│       ├── {page}.html
│       └── {page}.png
└── site/public/        # 生产页面
    ├── index.html
    └── {page}.html
```

### `.stitch/metadata.json` Schema

此文件持久化所有 Stitch 标识符，以便后续迭代可以引用它们进行编辑或变体。在创建项目或生成屏幕后，通过调用 `[prefix]:get_project` 填充此文件。

```json
{
  "name": "projects/6139132077804554844",
  "projectId": "6139132077804554844",
  "title": "My App",
  "visibility": "PRIVATE",
  "createTime": "2026-03-04T23:11:25.514932Z",
  "updateTime": "2026-03-04T23:34:40.400007Z",
  "projectType": "PROJECT_DESIGN",
  "origin": "STITCH",
  "deviceType": "MOBILE",
  "designTheme": {
    "colorMode": "DARK",
    "font": "INTER",
    "roundness": "ROUND_EIGHT",
    "customColor": "#40baf7",
    "saturation": 3
  },
  "screens": {
    "index": {
      "id": "d7237c7d78f44befa4f60afb17c818c1",
      "sourceScreen": "projects/6139132077804554844/screens/d7237c7d78f44befa4f60afb17c818c1",
      "x": 0,
      "y": 0,
      "width": 390,
      "height": 1249
    },
    "about": {
      "id": "bf6a3fe5c75348e58cf21fc7a9ddeafb",
      "sourceScreen": "projects/6139132077804554844/screens/bf6a3fe5c75348e58cf21fc7a9ddeafb",
      "x": 549,
      "y": 0,
      "width": 390,
      "height": 1159
    }
  },
  "metadata": {
    "userRole": "OWNER"
  }
}
```

| 字段 | 描述 |
|-------|-------------|
| `name` | 完整资源名称（`projects/{id}`） |
| `projectId` | Stitch 项目 ID（来自 `create_project` 或 `get_project`） |
| `title` | 人类可读的项目标题 |
| `designTheme` | 设计系统令牌：颜色模式、字体、圆角、自定义颜色、饱和度 |
| `deviceType` | 目标设备：`MOBILE`、`DESKTOP`、`TABLET` |
| `screens` | 页面名称 → 屏幕对象的映射。每个屏幕包含 `id`、`sourceScreen`（MCP 调用的资源路径）、画布位置（`x`、`y`）和尺寸（`width`、`height`） |
| `metadata.userRole` | 用户在项目中的角色（`OWNER`、`EDITOR`、`VIEWER`） |

## 编排选项

循环可以由不同的编排层驱动：

| 方法 | 工作原理 |
|--------|--------------|
| **CI/CD** | GitHub Actions 在 `.stitch/next-prompt.md` 变更时触发 |
| **人机协作** | 开发者在继续之前审查每次迭代 |
| **智能体链** | 一个智能体分派给另一个（如 Jules API） |
| **手动** | 开发者在同一仓库中重复运行智能体 |

此技能与编排无关 — 专注于模式，而非触发机制。

## 设计系统集成

此技能与 `design-md` 技能配合效果最佳：

1. **首次设置**：从现有 Stitch 屏幕使用 `design-md` 技能生成 `.stitch/DESIGN.md`
2. **每次迭代**：将 Section 6（"Design System Notes for Stitch Generation"）复制到你的接力棒提示词中
3. **一致性**：所有生成的页面将共享相同的视觉语言

## 常见陷阱

- ❌ 忘记更新 `.stitch/next-prompt.md`（会中断循环）
- ❌ 重新创建站点地图中已存在的页面
- ❌ 未在提示词中包含来自 `.stitch/DESIGN.md` 的设计系统块
- ❌ 保留占位符链接（`href="#"`）而非连接真实导航
- ❌ 创建新项目后忘记持久化 `.stitch/metadata.json`

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| Stitch 生成失败 | 检查提示词是否包含设计系统块 |
| 样式不一致 | 确保 `.stitch/DESIGN.md` 是最新的且复制正确 |
| 循环停滞 | 验证 `.stitch/next-prompt.md` 是否已用有效的 frontmatter 更新 |
| 导航损坏 | 检查所有内部链接是否使用正确的相对路径 |

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
