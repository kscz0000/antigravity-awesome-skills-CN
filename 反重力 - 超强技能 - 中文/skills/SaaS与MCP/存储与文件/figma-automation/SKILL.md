---
name: figma-automation
description: "通过 Rube MCP (Composio) 自动化 Figma 任务：文件、组件、设计令牌、评论、导出。始终先搜索工具以获取当前模式。"
risk: safe
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Figma 自动化

通过 Composio 的 Figma 工具包（经由 Rube MCP）自动化 Figma 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与工具包 `figma` 建立活跃的 Figma 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `figma` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Figma 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 获取文件数据和组件

**何时使用**：用户想要检查 Figma 设计文件或提取组件信息

**工具序列**：
1. `FIGMA_DISCOVER_FIGMA_RESOURCES` - 从 Figma URL 提取 ID [前置条件]
2. `FIGMA_GET_FILE_JSON` - 获取文件数据（默认简化）[必需]
3. `FIGMA_GET_FILE_NODES` - 获取特定节点数据 [可选]
4. `FIGMA_GET_FILE_COMPONENTS` - 列出已发布组件 [可选]
5. `FIGMA_GET_FILE_COMPONENT_SETS` - 列出组件集 [可选]

**关键参数**：
- `file_key`：URL 中的文件密钥（例如 figma.com/design/abc123XYZ/... 中的 'abc123XYZ'）
- `ids`：逗号分隔的节点 ID（不是数组）
- `depth`：树遍历深度（2 表示页面和顶层子节点）
- `simplify`：True 表示 AI 友好格式（减少 70%+ 大小）

**常见陷阱**：
- 仅支持设计文件；FigJam 画板和 Slides 返回 400 错误
- `ids` 必须是逗号分隔的字符串，不是数组
- URL 中的节点 ID 可能是短横线格式（1-541），但 API 需要冒号格式（1:541）
- 过宽的 ids/depth 可能触发超大负载（413）；缩小范围或降低深度
- 响应数据可能在 `data_preview` 而非 `data` 中

### 2. 导出和渲染图像

**何时使用**：用户想要将设计资源导出为图像

**工具序列**：
1. `FIGMA_GET_FILE_JSON` - 查找要导出的节点 ID [前置条件]
2. `FIGMA_RENDER_IMAGES_OF_FILE_NODES` - 将节点渲染为图像 [必需]
3. `FIGMA_DOWNLOAD_FIGMA_IMAGES` - 下载渲染的图像 [可选]
4. `FIGMA_GET_IMAGE_FILLS` - 获取图像填充 URL [可选]

**关键参数**：
- `file_key`：文件密钥
- `ids`：要渲染的逗号分隔节点 ID
- `format`：'png'、'svg'、'jpg' 或 'pdf'
- `scale`：PNG/JPG 的缩放因子（0.01-4.0）
- `images`：下载用的 {node_id, file_name, format} 数组

**常见陷阱**：
- 图像返回为 node_id 到 URL 的映射；某些 ID 可能为 null（渲染失败）
- URL 是临时的（有效期约 30 天）
- 图像上限为 32 百万像素；更大的请求会自动缩小

### 3. 提取设计令牌

**何时使用**：用户想要提取设计令牌用于开发

**工具序列**：
1. `FIGMA_EXTRACT_DESIGN_TOKENS` - 提取颜色、排版、间距 [必需]
2. `FIGMA_DESIGN_TOKENS_TO_TAILWIND` - 转换为 Tailwind 配置 [可选]

**关键参数**：
- `file_key`：文件密钥
- `include_local_styles`：包含本地样式（默认 true）
- `include_variables`：包含 Figma 变量
- `tokens`：提取的完整令牌对象（用于 Tailwind 转换）

**常见陷阱**：
- Tailwind 转换需要完整的令牌对象，包括 total_tokens 和 sources
- 在传递给转换之前，不要从提取响应中删除字段

### 4. 管理评论和版本

**何时使用**：用户想要查看或添加评论，或检查版本历史

**工具序列**：
1. `FIGMA_GET_COMMENTS_IN_A_FILE` - 列出所有文件评论 [可选]
2. `FIGMA_ADD_A_COMMENT_TO_A_FILE` - 添加评论 [可选]
3. `FIGMA_GET_REACTIONS_FOR_A_COMMENT` - 获取评论反应 [可选]
4. `FIGMA_GET_VERSIONS_OF_A_FILE` - 获取版本历史 [可选]

**关键参数**：
- `file_key`：文件密钥
- `as_md`：以 Markdown 格式返回评论
- `message`：评论文本
- `comment_id`：用于反应的评论 ID

**常见陷阱**：
- 评论可以使用 client_meta 定位到特定节点
- 回复评论不能嵌套（只有一层回复）

### 5. 浏览项目和团队

**何时使用**：用户想要列出团队项目或文件

**工具序列**：
1. `FIGMA_GET_PROJECTS_IN_A_TEAM` - 列出团队项目 [可选]
2. `FIGMA_GET_FILES_IN_A_PROJECT` - 列出项目文件 [可选]
3. `FIGMA_GET_TEAM_STYLES` - 列出团队已发布样式 [可选]

**关键参数**：
- `team_id`：URL 中的团队 ID（figma.com/files/team/TEAM_ID/...）
- `project_id`：项目 ID

**常见陷阱**：
- 团队 ID 无法通过编程方式获取；从 Figma URL 中提取
- 团队端点仅返回已发布的样式/组件

## 常见模式

### URL 解析

从 Figma URL 提取 ID：
```
1. 使用 figma_url 调用 FIGMA_DISCOVER_FIGMA_RESOURCES
2. 从响应中提取 file_key、node_id、team_id
3. 将短横线格式的节点 ID（1-541）转换为冒号格式（1:541）
```

### 节点遍历

```
1. 使用 depth=2 调用 FIGMA_GET_FILE_JSON 获取概览
2. 从响应中识别目标节点
3. 使用特定 ids 和更高深度再次调用以获取详细信息
```

## 已知陷阱

**文件类型支持**：
- GET_FILE_JSON 仅支持设计文件（figma.com/design/ 或 figma.com/file/）
- FigJam 画板和 Slides 不受支持

**节点 ID 格式**：
- URL 使用短横线格式：`node-id=1-541`
- API 使用冒号格式：`1:541`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 解析 URL | FIGMA_DISCOVER_FIGMA_RESOURCES | figma_url |
| 获取文件 JSON | FIGMA_GET_FILE_JSON | file_key, ids, depth |
| 获取节点 | FIGMA_GET_FILE_NODES | file_key, ids |
| 渲染图像 | FIGMA_RENDER_IMAGES_OF_FILE_NODES | file_key, ids, format |
| 下载图像 | FIGMA_DOWNLOAD_FIGMA_IMAGES | file_key, images |
| 获取组件 | FIGMA_GET_COMPONENT | file_key, node_id |
| 文件组件 | FIGMA_GET_FILE_COMPONENTS | file_key |
| 组件集 | FIGMA_GET_FILE_COMPONENT_SETS | file_key |
| 设计令牌 | FIGMA_EXTRACT_DESIGN_TOKENS | file_key |
| 令牌转 Tailwind | FIGMA_DESIGN_TOKENS_TO_TAILWIND | tokens |
| 文件评论 | FIGMA_GET_COMMENTS_IN_A_FILE | file_key |
| 添加评论 | FIGMA_ADD_A_COMMENT_TO_A_FILE | file_key, message |
| 文件版本 | FIGMA_GET_VERSIONS_OF_A_FILE | file_key |
| 团队项目 | FIGMA_GET_PROJECTS_IN_A_TEAM | team_id |
| 项目文件 | FIGMA_GET_FILES_IN_A_PROJECT | project_id |
| 团队样式 | FIGMA_GET_TEAM_STYLES | team_id |
| 文件样式 | FIGMA_GET_FILE_STYLES | file_key |
| 图像填充 | FIGMA_GET_IMAGE_FILLS | file_key |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
