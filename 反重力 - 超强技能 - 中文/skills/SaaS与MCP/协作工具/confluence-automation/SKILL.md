---
name: confluence-automation
description: "通过 Rube MCP (Composio) 自动化 Confluence 页面创建、内容搜索、空间管理、标签和层级导航。始终先搜索工具获取当前模式。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Confluence 自动化

通过 Composio 的 Confluence 工具包自动化 Confluence 操作，包括页面创建和更新、使用 CQL 进行内容搜索、空间管理、标签标记和页面层级导航。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与工具包 `confluence` 建立活跃的 Confluence 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `confluence` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Confluence OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和更新页面

**何时使用**：用户想要创建新文档或更新现有 Confluence 页面

**工具调用顺序**：
1. `CONFLUENCE_GET_SPACES` - 列出空间以找到目标空间 ID [前置条件]
2. `CONFLUENCE_SEARCH_CONTENT` - 查找现有页面以避免重复或定位父页面 [可选]
3. `CONFLUENCE_GET_PAGE_BY_ID` - 更新前获取当前页面内容和版本号 [更新的前置条件]
4. `CONFLUENCE_CREATE_PAGE` - 在空间中创建新页面 [创建时必需]
5. `CONFLUENCE_UPDATE_PAGE` - 用新内容和递增的版本号更新现有页面 [更新时必需]
6. `CONFLUENCE_ADD_CONTENT_LABEL` - 创建后为页面添加标签 [可选]

**关键参数**：
- `spaceId`: 空间 ID 或键（例如 `"DOCS"`、`"12345678"`）— 空间键会自动转换为 ID
- `title`: 页面标题（在空间内必须唯一）
- `parentId`: 创建子页面时的父页面 ID；省略则放置在空间首页下
- `body.storage.value`: Confluence 存储格式的 HTML/XHTML 内容
- `body.storage.representation`: 创建操作必须为 `"storage"`
- `version.number`: 更新时必须为当前版本 + 1
- `version.message`: 可选的变更描述

**常见陷阱**：
- Confluence 强制要求空间内页面标题唯一；创建重复标题的页面会失败
- `UPDATE_PAGE` 要求 `version.number` 设置为当前版本 + 1；始终先用 `GET_PAGE_BY_ID` 获取当前版本
- 内容必须是 Confluence 存储格式（XHTML），而非纯文本或 Markdown
- `CREATE_PAGE` 使用 `body.storage.value`，而 `UPDATE_PAGE` 使用 `body.value` 配合 `body.representation`
- `GET_PAGE_BY_ID` 需要数字长整型 ID，而非 UUID 或字符串

### 2. 搜索内容

**何时使用**：用户想要在 Confluence 中查找页面、博客文章或内容

**工具调用顺序**：
1. `CONFLUENCE_SEARCH_CONTENT` - 带智能相关性排名的关键词搜索 [必需]
2. `CONFLUENCE_CQL_SEARCH` - 使用 Confluence 查询语言进行高级搜索 [替代方案]
3. `CONFLUENCE_GET_PAGE_BY_ID` - 为选定的搜索结果获取完整内容 [可选]
4. `CONFLUENCE_GET_PAGES` - 当搜索相关性较弱时按日期浏览页面 [备选方案]

**SEARCH_CONTENT 关键参数**：
- `query`: 与页面标题匹配的搜索文本，带智能排名
- `spaceKey`: 限制在特定空间内搜索
- `limit`: 最大结果数（默认 25，最大 250）
- `start`: 分页偏移量（从 0 开始）

**CQL_SEARCH 关键参数**：
- `cql`: CQL 查询字符串（例如 `text ~ "API docs" AND space = DOCS AND type = page`）
- `expand`: 逗号分隔的属性（例如 `content.space`、`content.body.storage`）
- `excerpt`: `highlight`、`indexed` 或 `none`
- `limit`: 最大结果数（最大 250；使用 body 扩展时降至 25-50）

**CQL 运算符和字段**：
- 字段：`text`、`title`、`label`、`space`、`type`、`creator`、`lastModified`、`created`、`ancestor`
- 运算符：`=`、`!=`、`~`（包含）、`!~`、`>`、`<`、`>=`、`<=`、`IN`、`NOT IN`
- 函数：`currentUser()`、`now("-7d")`、`now("-30d")`
- 示例：`title ~ "meeting" AND lastModified > now("-7d") ORDER BY lastModified DESC`

**常见陷阱**：
- `CONFLUENCE_SEARCH_CONTENT` 最多获取 300 个页面并应用客户端过滤 — 不是真正的全文搜索
- `CONFLUENCE_CQL_SEARCH` 是真正的全文搜索；使用 `text ~ "term"` 进行内容正文搜索
- 可能出现 HTTP 429 速率限制；限制为约 2 请求/秒并使用退避策略
- 在 CQL_SEARCH 中使用 body 扩展可能将最大结果降至 25-50
- 搜索索引不是即时的；最近创建的页面可能不会立即出现

### 3. 管理空间

**何时使用**：用户想要列出、创建或检查 Confluence 空间

**工具调用顺序**：
1. `CONFLUENCE_GET_SPACES` - 列出所有空间，可选过滤 [必需]
2. `CONFLUENCE_GET_SPACE_BY_ID` - 获取特定空间的详细元数据 [可选]
3. `CONFLUENCE_CREATE_SPACE` - 用键和名称创建新空间 [可选]
4. `CONFLUENCE_GET_SPACE_PROPERTIES` - 检索存储为空间属性的自定义元数据 [可选]
5. `CONFLUENCE_GET_SPACE_CONTENTS` - 列出空间中的页面、博客文章或附件 [可选]
6. `CONFLUENCE_GET_LABELS_FOR_SPACE` - 列出空间上的标签 [可选]

**关键参数**：
- `key`: 空间键 — 仅限字母数字，不允许下划线或连字符（例如 `DOCS`、`PROJECT1`）
- `name`: 人类可读的空间名称
- `type`: `global` 或 `personal`
- `status`: `current`（活跃）或 `archived`
- `spaceKey`: 对于 GET_SPACE_CONTENTS，按空间键过滤
- `id`: GET_SPACE_BY_ID 的数字空间 ID（不是空间键）

**常见陷阱**：
- 空间键必须仅包含字母数字（不允许下划线、连字符或特殊字符）
- `GET_SPACE_BY_ID` 需要数字空间 ID，而非空间键；使用 `GET_SPACES` 查找数字 ID
- 可点击的空间 URL 可能需要组装：将 `_links.webui`（相对路径）与 `_links.base` 拼接
- 默认分页为 25；显式设置 `limit`（空间最大 200）

### 4. 导航页面层级和标签

**何时使用**：用户想要探索页面树、子页面、祖先或管理标签

**工具调用顺序**：
1. `CONFLUENCE_SEARCH_CONTENT` - 查找目标页面 ID [前置条件]
2. `CONFLUENCE_GET_CHILD_PAGES` - 列出父页面的直接子页面 [必需]
3. `CONFLUENCE_GET_PAGE_ANCESTORS` - 获取页面的完整祖先链 [可选]
4. `CONFLUENCE_GET_LABELS_FOR_PAGE` - 列出特定页面上的标签 [可选]
5. `CONFLUENCE_ADD_CONTENT_LABEL` - 为页面添加标签 [可选]
6. `CONFLUENCE_GET_LABELS_FOR_SPACE_CONTENT` - 列出空间中所有内容的标签 [可选]
7. `CONFLUENCE_GET_PAGE_VERSIONS` - 审计页面的编辑历史 [可选]

**关键参数**：
- `id`: 子页面、祖先、标签和版本的页面 ID
- `cursor`: GET_CHILD_PAGES 的不透明分页游标（来自 `_links.next`）
- `limit`: 每页项目数（子页面最大 250）
- `sort`: 子页面排序选项：`id`、`-id`、`created-date`、`-created-date`、`modified-date`、`-modified-date`、`child-position`、`-child-position`

**常见陷阱**：
- `GET_CHILD_PAGES` 只返回直接子页面，不返回嵌套的后代；需要递归获取完整树
- GET_CHILD_PAGES 的分页使用基于游标的分页（不是 start/limit）
- 在用作父页面前验证搜索返回的正确页面 ID；搜索可能返回相似标题
- `GET_PAGE_VERSIONS` 需要页面 ID，而非版本号

## 常见模式

### ID 解析
在操作前始终将人类可读的名称解析为 ID：
- **空间键 -> 空间 ID**：带 `spaceKey` 过滤的 `CONFLUENCE_GET_SPACES`，或 `CREATE_PAGE` 直接接受空间键
- **页面标题 -> 页面 ID**：带 `query` 参数的 `CONFLUENCE_SEARCH_CONTENT`，然后提取页面 ID
- **从 URL 获取空间 ID**：从 Confluence URL 中提取数字 ID 或使用 GET_SPACES

### 分页
Confluence 使用两种分页方式：
- **基于偏移量**（大多数端点）：`start`（从 0 开始的偏移量）+ `limit`（页面大小）。将 `start` 递增 `limit`，直到返回的结果少于 `limit`。
- **基于游标**（GET_CHILD_PAGES、GET_PAGES）：使用响应中 `_links.next` 的 `cursor`。持续直到没有 `next` 链接。

### 内容格式化
- 页面使用 Confluence 存储格式（XHTML），而非 Markdown
- 基本元素：`<p>`、`<h1>`-`<h6>`、`<strong>`、`<em>`、`<code>`、`<ul>`、`<ol>`、`<li>`
- 表格：`<table><tbody><tr><th>` / `<td>` 结构
- 宏：`<ac:structured-macro ac:name="code">` 用于代码块等
- 始终将内容包装在正确的 XHTML 标签中

## 已知陷阱

### ID 格式
- 空间 ID 是数字（例如 `557060`）；空间键是短字符串（例如 `DOCS`）
- GET_PAGE_BY_ID 的页面 ID 是数字长整型值；某些工具接受 UUID 格式
- `GET_SPACE_BY_ID` 需要数字 ID，而非空间键
- `GET_PAGE_BY_ID` 接受整数，而非字符串

### 速率限制
- 搜索端点可能出现 HTTP 429；遵守 Retry-After 头
- 限制为约 2 请求/秒，使用指数退避和抖动
- CQL_SEARCH 中的 body 扩展将结果限制降至 25-50

### 内容格式
- 内容必须是 Confluence 存储格式（XHTML），而非 Markdown 或纯文本
- 无效的 XHTML 会导致页面创建/更新失败
- `CREATE_PAGE` 将 body 嵌套在 `body.storage.value` 下；`UPDATE_PAGE` 使用 `body.value` + `body.representation`

### 版本冲突
- 更新需要精确的下一个版本号（当前 + 1）
- 并发编辑可能导致版本冲突；始终在更新前立即获取当前版本
- 更新时的标题更改仍必须在空间内唯一

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出空间 | `CONFLUENCE_GET_SPACES` | `type`、`status`、`limit` |
| 按 ID 获取空间 | `CONFLUENCE_GET_SPACE_BY_ID` | `id` |
| 创建空间 | `CONFLUENCE_CREATE_SPACE` | `key`、`name`、`type` |
| 空间内容 | `CONFLUENCE_GET_SPACE_CONTENTS` | `spaceKey`、`type`、`status` |
| 空间属性 | `CONFLUENCE_GET_SPACE_PROPERTIES` | `id`、`key` |
| 搜索内容 | `CONFLUENCE_SEARCH_CONTENT` | `query`、`spaceKey`、`limit` |
| CQL 搜索 | `CONFLUENCE_CQL_SEARCH` | `cql`、`expand`、`limit` |
| 列出页面 | `CONFLUENCE_GET_PAGES` | `spaceId`、`sort`、`limit` |
| 按 ID 获取页面 | `CONFLUENCE_GET_PAGE_BY_ID` | `id`（整数） |
| 创建页面 | `CONFLUENCE_CREATE_PAGE` | `title`、`spaceId`、`body` |
| 更新页面 | `CONFLUENCE_UPDATE_PAGE` | `id`、`title`、`body`、`version` |
| 删除页面 | `CONFLUENCE_DELETE_PAGE` | `id` |
| 子页面 | `CONFLUENCE_GET_CHILD_PAGES` | `id`、`limit`、`sort` |
| 页面祖先 | `CONFLUENCE_GET_PAGE_ANCESTORS` | `id` |
| 页面标签 | `CONFLUENCE_GET_LABELS_FOR_PAGE` | `id` |
| 添加标签 | `CONFLUENCE_ADD_CONTENT_LABEL` | 内容 ID、标签 |
| 页面版本 | `CONFLUENCE_GET_PAGE_VERSIONS` | `id` |
| 空间标签 | `CONFLUENCE_GET_LABELS_FOR_SPACE` | 空间 ID |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
