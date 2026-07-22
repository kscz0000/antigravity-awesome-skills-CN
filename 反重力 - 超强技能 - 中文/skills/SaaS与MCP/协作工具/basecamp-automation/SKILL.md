---
name: basecamp-automation
description: "通过 Rube MCP (Composio) 自动化 Basecamp 项目管理、待办事项、消息、人员和待办列表组织。始终先搜索工具以获取当前 schema。当用户要求'自动化 Basecamp 项目管理、创建待办列表、管理消息板、管理人员访问权限'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Basecamp

通过 Composio 的 Basecamp 工具包自动化 Basecamp 操作，包括项目管理、待办列表创建、任务管理、消息板发布、人员管理和待办分组组织。

## 前提条件

- 必须连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `basecamp` 建立 Basecamp 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 响应正常，验证 Rube MCP 可用
2. 使用工具包 `basecamp` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Basecamp OAuth
4. 在运行任何工作流之前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 管理待办列表和任务

**使用时机**：用户想要创建待办列表、添加任务或在 Basecamp 项目中组织工作

**工具调用顺序**：
1. `BASECAMP_GET_PROJECTS` - 列出项目以找到目标 bucket_id [前提条件]
2. `BASECAMP_GET_BUCKETS_TODOSETS` - 获取项目内的待办集合 [前提条件]
3. `BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS` - 列出现有待办列表以避免重复 [可选]
4. `BASECAMP_POST_BUCKETS_TODOSETS_TODOLISTS` - 在待办集合中创建新待办列表 [创建列表时必需]
5. `BASECAMP_GET_BUCKETS_TODOLISTS` - 获取特定待办列表的详情 [可选]
6. `BASECAMP_POST_BUCKETS_TODOLISTS_TODOS` - 在待办列表中创建待办事项 [创建任务时必需]
7. `BASECAMP_CREATE_TODO` - 创建单个待办事项的替代工具 [替代方案]
8. `BASECAMP_GET_BUCKETS_TODOLISTS_TODOS` - 列出待办列表中的待办事项 [可选]

**创建待办列表的关键参数**：
- `bucket_id`：整数类型的项目/bucket ID（来自 GET_PROJECTS）
- `todoset_id`：整数类型的待办集合 ID（来自 GET_BUCKETS_TODOSETS）
- `name`：待办列表标题（必填）
- `description`：HTML 格式的描述（支持富文本）

**创建待办事项的关键参数**：
- `bucket_id`：整数类型的项目/bucket ID
- `todolist_id`：整数类型的待办列表 ID
- `content`：待办事项内容（必填）
- `description`：待办事项的 HTML 详细说明
- `assignee_ids`：整数类型的人员 ID 数组
- `due_on`：截止日期，格式为 `YYYY-MM-DD`
- `starts_on`：开始日期，格式为 `YYYY-MM-DD`
- `notify`：布尔值，是否通知被分配人（默认为 false）
- `completion_subscriber_ids`：完成时通知的人员 ID

**注意事项**：
- 一个项目（bucket）可以包含多个待办集合；选择错误的 `todoset_id` 会在错误的分区创建列表
- 创建前始终检查现有待办列表以避免近乎重复的名称
- 成功响应包含面向用户的 URL（`app_url`、`app_todos_url`）；优先返回这些而非原始 ID
- 所有 ID（`bucket_id`、`todoset_id`、`todolist_id`）都是整数，不是字符串
- 描述仅支持 HTML 格式，不支持 Markdown

### 2. 发布和管理消息

**使用时机**：用户想要向项目消息板发布消息或更新现有消息

**工具调用顺序**：
1. `BASECAMP_GET_PROJECTS` - 找到目标项目和 bucket_id [前提条件]
2. `BASECAMP_GET_MESSAGE_BOARD` - 获取项目的消息板 ID [前提条件]
3. `BASECAMP_CREATE_MESSAGE` - 在消息板上创建新消息 [必需]
4. `BASECAMP_POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` - 替代消息创建工具 [备选]
5. `BASECAMP_GET_MESSAGE` - 按 ID 读取特定消息 [可选]
6. `BASECAMP_PUT_BUCKETS_MESSAGES` - 更新现有消息 [可选]

**关键参数**：
- `bucket_id`：整数类型的项目/bucket ID
- `message_board_id`：整数类型的消息板 ID（来自 GET_MESSAGE_BOARD）
- `subject`：消息标题（必填）
- `content`：消息的 HTML 正文
- `status`：设为 `"active"` 可立即发布
- `category_id`：消息类型分类（可选）
- `subscriptions`：要通知的人员 ID 数组；省略则通知所有项目成员

**注意事项**：
- `status="draft"` 可能导致 HTTP 400；使用 `status="active"` 作为可靠选项
- `bucket_id` 和 `message_board_id` 必须属于同一项目；不匹配会导致失败或错误路由
- 消息内容仅支持 HTML 标签，不支持 Markdown
- 通过 `PUT_BUCKETS_MESSAGES` 更新会替换整个正文——需包含完整的修正内容，而非仅差异部分
- 优先使用响应中的 `app_url` 作为面向用户的确认链接
- `CREATE_MESSAGE` 和 `POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` 功能相同；优先使用 CREATE_MESSAGE，失败时回退到 POST

### 3. 管理人员和访问权限

**使用时机**：用户想要列出人员、管理项目访问权限或添加新用户

**工具调用顺序**：
1. `BASECAMP_GET_PEOPLE` - 列出当前用户可见的所有人员 [必需]
2. `BASECAMP_GET_PROJECTS` - 找到目标项目 [前提条件]
3. `BASECAMP_LIST_PROJECT_PEOPLE` - 列出特定项目的人员 [必需]
4. `BASECAMP_GET_PROJECTS_PEOPLE` - 列出项目成员的替代方式 [替代方案]
5. `BASECAMP_PUT_PROJECTS_PEOPLE_USERS` - 授予或撤销项目访问权限 [更改访问权限时必需]

**PUT_PROJECTS_PEOPLE_USERS 的关键参数**：
- `project_id`：整数类型的项目 ID
- `grant`：要添加到项目的整数类型人员 ID 数组
- `revoke`：要从项目中移除的整数类型人员 ID 数组
- `create`：包含 `name`、`email_address` 及可选 `company_name`、`title` 的对象数组，用于新用户
- 必须至少提供 `grant`、`revoke` 或 `create` 之一

**注意事项**：
- 人员 ID 是整数；始终先通过 GET_PEOPLE 将姓名解析为 ID
- 人员管理中的 `project_id` 与其他操作中的 `bucket_id` 相同
- `LIST_PROJECT_PEOPLE` 和 `GET_PROJECTS_PEOPLE` 几乎相同；任选其一
- 通过 `create` 创建用户时会一步完成项目访问授权

### 4. 使用分组组织待办事项

**使用时机**：用户想要将待办列表中的待办事项组织为带颜色标记的分组

**工具调用顺序**：
1. `BASECAMP_GET_PROJECTS` - 找到目标项目 [前提条件]
2. `BASECAMP_GET_BUCKETS_TODOLISTS` - 获取待办列表详情 [前提条件]
3. `BASECAMP_GET_TODOLIST_GROUPS` - 列出待办列表中的现有分组 [可选]
4. `BASECAMP_GET_BUCKETS_TODOLISTS_GROUPS` - 替代分组列表工具 [替代方案]
5. `BASECAMP_POST_BUCKETS_TODOLISTS_GROUPS` - 在待办列表中创建新分组 [必需]
6. `BASECAMP_CREATE_TODOLIST_GROUP` - 替代分组创建工具 [替代方案]

**关键参数**：
- `bucket_id`：整数类型的项目/bucket ID
- `todolist_id`：整数类型的待办列表 ID
- `name`：分组标题（必填）
- `color`：视觉颜色标识——可选值：`white`、`red`、`orange`、`yellow`、`green`、`blue`、`aqua`、`purple`、`gray`、`pink`、`brown`
- `status`：列表筛选——`"archived"` 或 `"trashed"`（省略则显示活跃分组）

**注意事项**：
- `POST_BUCKETS_TODOLISTS_GROUPS` 和 `CREATE_TODOLIST_GROUP` 几乎相同；任选其一
- 颜色值必须来自固定调色板；不支持任意十六进制/RGB 值
- 分组是待办列表内的子分区，不是独立实体

### 5. 浏览和检查项目

**使用时机**：用户想要列出项目、获取项目详情或浏览项目结构

**工具调用顺序**：
1. `BASECAMP_GET_PROJECTS` - 列出所有活跃项目 [必需]
2. `BASECAMP_GET_PROJECT` - 获取特定项目的完整详情 [可选]
3. `BASECAMP_GET_PROJECTS_BY_PROJECT_ID` - 替代的项目详情获取方式 [替代方案]

**关键参数**：
- `status`：按 `"archived"` 或 `"trashed"` 筛选；省略则显示活跃项目
- `project_id`：整数类型的项目 ID，用于获取详情

**注意事项**：
- 项目按创建时间从新到旧排序
- 响应包含 `dock` 数组，其中有工具（todoset、message_board 等）及其 ID
- 使用 dock 工具 ID 查找 `todoset_id`、`message_board_id` 等供后续操作使用

## 常用模式

### ID 解析
Basecamp 使用层级 ID 结构。始终自顶向下解析：
- **项目 (bucket_id)**：`BASECAMP_GET_PROJECTS` -- 按名称查找，获取 `id`
- **待办集合 (todoset_id)**：在项目 dock 中或通过 `BASECAMP_GET_BUCKETS_TODOSETS` 获取
- **消息板 (message_board_id)**：在项目 dock 中或通过 `BASECAMP_GET_MESSAGE_BOARD` 获取
- **待办列表 (todolist_id)**：`BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS`
- **人员 (person_id)**：`BASECAMP_GET_PEOPLE` 或 `BASECAMP_LIST_PROJECT_PEOPLE`
- 注意：`bucket_id` 和 `project_id` 在不同上下文中指代同一实体

### 分页
Basecamp 在列表端点使用基于页码的分页：
- 响应头或响应体可能指示还有更多页面
- `GET_PROJECTS`、`GET_BUCKETS_TODOSETS_TODOLISTS` 及其他列表端点返回分页结果
- 持续获取直到没有更多结果返回

### 内容格式
- 所有富文本字段使用 HTML，而非 Markdown
- 用 `<div>` 标签包裹内容；使用 `<strong>`、`<em>`、`<ul>`、`<ol>`、`<li>`、`<a>` 等
- 示例：`<div><strong>重要提示：</strong>请在周五前完成</div>`

## 已知注意事项

### ID 格式
- 所有 Basecamp ID 都是整数，不是字符串或 UUID
- `bucket_id` = `project_id`（同一实体，不同工具中的不同参数名）
- 待办集合 ID、待办列表 ID 和消息板 ID 在项目的 `dock` 数组中找到
- 人员 ID 是整数；操作前通过 `GET_PEOPLE` 解析姓名

### 状态字段
- 消息的 `status="draft"` 可能导致 HTTP 400；始终使用 `status="active"`
- 项目/待办列表状态筛选：`"archived"`、`"trashed"`，或省略以显示活跃项

### 内容格式
- 仅支持 HTML，不支持 Markdown
- 更新会替换整个正文，而非部分差异
- 无效的 HTML 标签可能被静默移除

### 速率限制
- Basecamp API 有速率限制；快速连续请求需间隔开
- 包含大量待办事项的大型项目应仔细分页

### URL 处理
- 优先使用 API 响应中的 `app_url` 作为面向用户的链接
- 不要手动从 ID 拼接 Basecamp URL

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出项目 | `BASECAMP_GET_PROJECTS` | `status` |
| 获取项目 | `BASECAMP_GET_PROJECT` | `project_id` |
| 获取项目详情 | `BASECAMP_GET_PROJECTS_BY_PROJECT_ID` | `project_id` |
| 获取待办集合 | `BASECAMP_GET_BUCKETS_TODOSETS` | `bucket_id`, `todoset_id` |
| 列出待办列表 | `BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS` | `bucket_id`, `todoset_id` |
| 获取待办列表 | `BASECAMP_GET_BUCKETS_TODOLISTS` | `bucket_id`, `todolist_id` |
| 创建待办列表 | `BASECAMP_POST_BUCKETS_TODOSETS_TODOLISTS` | `bucket_id`, `todoset_id`, `name` |
| 创建待办事项 | `BASECAMP_POST_BUCKETS_TODOLISTS_TODOS` | `bucket_id`, `todolist_id`, `content` |
| 创建待办事项（替代） | `BASECAMP_CREATE_TODO` | `bucket_id`, `todolist_id`, `content` |
| 列出待办事项 | `BASECAMP_GET_BUCKETS_TODOLISTS_TODOS` | `bucket_id`, `todolist_id` |
| 列出待办分组 | `BASECAMP_GET_TODOLIST_GROUPS` | `bucket_id`, `todolist_id` |
| 创建待办分组 | `BASECAMP_POST_BUCKETS_TODOLISTS_GROUPS` | `bucket_id`, `todolist_id`, `name`, `color` |
| 创建待办分组（替代） | `BASECAMP_CREATE_TODOLIST_GROUP` | `bucket_id`, `todolist_id`, `name` |
| 获取消息板 | `BASECAMP_GET_MESSAGE_BOARD` | `bucket_id`, `message_board_id` |
| 创建消息 | `BASECAMP_CREATE_MESSAGE` | `bucket_id`, `message_board_id`, `subject`, `status` |
| 创建消息（替代） | `BASECAMP_POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` | `bucket_id`, `message_board_id`, `subject` |
| 获取消息 | `BASECAMP_GET_MESSAGE` | `bucket_id`, `message_id` |
| 更新消息 | `BASECAMP_PUT_BUCKETS_MESSAGES` | `bucket_id`, `message_id` |
| 列出所有人员 | `BASECAMP_GET_PEOPLE` | (无) |
| 列出项目人员 | `BASECAMP_LIST_PROJECT_PEOPLE` | `project_id` |
| 管理访问权限 | `BASECAMP_PUT_PROJECTS_PEOPLE_USERS` | `project_id`, `grant`, `revoke`, `create` |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
