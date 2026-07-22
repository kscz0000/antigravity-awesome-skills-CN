---
name: notion-automation
description: "通过 Rube MCP (Composio) 自动化 Notion 任务：页面、数据库、块、评论、用户。始终先搜索工具获取当前模式。触发词：Notion自动化、Notion操作、Notion页面管理、Notion数据库查询、Notion块管理、Notion评论、Rube MCP、Composio Notion"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Notion

通过 Composio 的 Notion 工具包和 Rube MCP 自动化 Notion 操作。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Notion 连接，工具包为 `notion`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包为 `notion`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Notion OAuth
4. 在运行任何工作流之前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 创建和管理页面

**何时使用**：用户想要创建、更新或归档 Notion 页面

**工具调用顺序**：
1. `NOTION_SEARCH_NOTION_PAGE` - 查找父页面或现有页面 [前置条件]
2. `NOTION_CREATE_NOTION_PAGE` - 在父页面下创建新页面 [可选]
3. `NOTION_RETRIEVE_PAGE` - 获取页面元数据/属性 [可选]
4. `NOTION_UPDATE_PAGE` - 更新页面属性、标题、图标、封面 [可选]
5. `NOTION_ARCHIVE_NOTION_PAGE` - 软删除（归档）页面 [可选]

**关键参数**：
- `query`：SEARCH_NOTION_PAGE 的搜索文本
- `parent_id`：父页面或数据库 ID
- `page_id`：用于检索/更新/归档的页面 ID
- `properties`：匹配父级模式的页面属性值

**注意事项**：
- RETRIEVE_PAGE 仅返回元数据/属性，不返回正文内容；请使用 FETCH_BLOCK_CONTENTS 获取页面正文
- ARCHIVE_NOTION_PAGE 是软删除（设置 archived=true），不是永久删除
- 宽泛的搜索可能看起来不完整，除非通过 has_more/next_cursor 完整分页

### 2. 查询和管理数据库

**何时使用**：用户想要查询数据库行、插入条目或更新记录

**工具调用顺序**：
1. `NOTION_SEARCH_NOTION_PAGE` - 按名称查找数据库 [前置条件]
2. `NOTION_FETCH_DATABASE` - 检查模式和属性 [前置条件]
3. `NOTION_QUERY_DATABASE` / `NOTION_QUERY_DATABASE_WITH_FILTER` - 查询行 [必需]
4. `NOTION_INSERT_ROW_DATABASE` - 添加新条目 [可选]
5. `NOTION_UPDATE_ROW_DATABASE` - 更新现有条目 [可选]

**关键参数**：
- `database_id`：数据库 ID（来自搜索或 URL）
- `filter`：匹配 Notion 筛选语法的筛选对象
- `sorts`：排序对象数组
- `start_cursor`：上一次响应的分页游标
- `properties`：匹配数据库模式的属性值，用于插入/更新

**注意事项**：
- 404 object_not_found 通常意味着 database_id 错误或数据库未与集成共享
- 结果是分页的；忽略 has_more/next_cursor 会静默截断读取
- 模式不匹配或缺少必需属性会导致 400 validation_error
- 公式和只读字段无法通过 INSERT_ROW_DATABASE 设置
- 筛选器中的属性名必须与模式完全匹配（区分大小写）

### 3. 管理块和页面内容

**何时使用**：用户想要读取、追加或修改页面中的内容块

**工具调用顺序**：
1. `NOTION_FETCH_BLOCK_CONTENTS` - 读取页面的子块 [必需]
2. `NOTION_ADD_MULTIPLE_PAGE_CONTENT` - 向页面追加块 [可选]
3. `NOTION_APPEND_TEXT_BLOCKS` - 追加纯文本块 [可选]
4. `NOTION_REPLACE_PAGE_CONTENT` - 替换所有页面内容 [可选]
5. `NOTION_DELETE_BLOCK` - 删除特定块 [可选]

**关键参数**：
- `block_id` / `page_id`：目标页面或块 ID
- `content_blocks`：块对象数组（不是 child_blocks）
- `text`：APPEND_TEXT_BLOCKS 的纯文本内容

**注意事项**：
- 使用 `content_blocks` 参数，不是 `child_blocks`——后者会验证失败
- ADD_MULTIPLE_PAGE_CONTENT 在已归档页面上会失败；需先通过 UPDATE_PAGE 取消归档
- 创建的块在 response.data.results 中；保存块 ID 以供后续编辑
- DELETE_BLOCK 是归档操作（archived=true），不是永久删除

### 4. 管理数据库模式

**何时使用**：用户想要创建数据库或修改其结构

**工具调用顺序**：
1. `NOTION_FETCH_DATABASE` - 检查当前模式 [前置条件]
2. `NOTION_CREATE_DATABASE` - 创建新数据库 [可选]
3. `NOTION_UPDATE_SCHEMA_DATABASE` - 修改数据库属性 [可选]

**关键参数**：
- `parent_id`：新数据库的父页面 ID
- `title`：数据库标题
- `properties`：带类型和选项的属性定义
- `database_id`：用于模式更新的数据库 ID

**注意事项**：
- 无法通过 UPDATE_SCHEMA 更改属性类型；必须创建新属性并迁移数据
- 公式、汇总和关联属性具有复杂的配置要求

### 5. 管理用户和评论

**何时使用**：用户想要列出工作区用户或管理页面上的评论

**工具调用顺序**：
1. `NOTION_LIST_USERS` - 列出所有工作区用户 [可选]
2. `NOTION_GET_ABOUT_ME` - 获取当前认证用户 [可选]
3. `NOTION_CREATE_COMMENT` - 向页面添加评论 [可选]
4. `NOTION_FETCH_COMMENTS` - 列出页面上的评论 [可选]

**关键参数**：
- `page_id`：评论的页面 ID（也称为 `discussion_id`）
- `rich_text`：富文本数组形式的评论内容

**注意事项**：
- 评论关联到页面，而非单个块
- 人员类型属性筛选需要 LIST_USERS 返回的用户 ID

## 常用模式

### ID 解析

**页面/数据库名称 -> ID**：
```
1. 调用 NOTION_SEARCH_NOTION_PAGE，query=名称
2. 使用 has_more/next_cursor 分页直到找到
3. 从匹配结果中提取 id
```

**数据库模式检查**：
```
1. 调用 NOTION_FETCH_DATABASE，传入 database_id
2. 提取 properties 对象获取字段名和类型
3. 在查询和插入中使用精确的属性名
```

### 分页

- 设置 `page_size` 指定每页结果数（最大 100）
- 检查响应中的 `has_more` 布尔值
- 在下次请求中传入 `start_cursor` 或 `next_cursor`
- 持续请求直到 `has_more` 为 false

### Notion 筛选语法

**单一筛选**：
```json
{"property": "Status", "select": {"equals": "Done"}}
```

**复合筛选**：
```json
{"and": [
  {"property": "Status", "select": {"equals": "In Progress"}},
  {"property": "Assignee", "people": {"contains": "user-id"}}
]}
```

## 已知注意事项

**集成共享**：
- 页面和数据库必须与 Notion 集成共享才能访问
- 当项目未与集成共享时，标题查询可能返回 0 条结果

**属性类型**：
- 属性名区分大小写，必须与模式完全匹配
- 公式、汇总和 created_time 字段为只读
- 选择/多选值必须匹配已有选项，除非创建新选项

**响应解析**：
- 响应数据可能嵌套在 `data_preview` 或 `data.results` 下
- 防御性解析，对不同嵌套层级设置回退处理

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索页面/数据库 | NOTION_SEARCH_NOTION_PAGE | query |
| 创建页面 | NOTION_CREATE_NOTION_PAGE | parent_id, properties |
| 获取页面元数据 | NOTION_RETRIEVE_PAGE | page_id |
| 更新页面 | NOTION_UPDATE_PAGE | page_id, properties |
| 归档页面 | NOTION_ARCHIVE_NOTION_PAGE | page_id |
| 复制页面 | NOTION_DUPLICATE_PAGE | page_id |
| 获取页面块 | NOTION_FETCH_BLOCK_CONTENTS | block_id |
| 追加块 | NOTION_ADD_MULTIPLE_PAGE_CONTENT | page_id, content_blocks |
| 追加文本 | NOTION_APPEND_TEXT_BLOCKS | page_id, text |
| 替换内容 | NOTION_REPLACE_PAGE_CONTENT | page_id, content_blocks |
| 删除块 | NOTION_DELETE_BLOCK | block_id |
| 查询数据库 | NOTION_QUERY_DATABASE | database_id, filter, sorts |
| 带筛选查询 | NOTION_QUERY_DATABASE_WITH_FILTER | database_id, filter |
| 插入行 | NOTION_INSERT_ROW_DATABASE | database_id, properties |
| 更新行 | NOTION_UPDATE_ROW_DATABASE | page_id, properties |
| 获取数据库模式 | NOTION_FETCH_DATABASE | database_id |
| 创建数据库 | NOTION_CREATE_DATABASE | parent_id, title, properties |
| 更新模式 | NOTION_UPDATE_SCHEMA_DATABASE | database_id, properties |
| 列出用户 | NOTION_LIST_USERS | (无) |
| 创建评论 | NOTION_CREATE_COMMENT | page_id, rich_text |
| 列出评论 | NOTION_FETCH_COMMENTS | page_id |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
