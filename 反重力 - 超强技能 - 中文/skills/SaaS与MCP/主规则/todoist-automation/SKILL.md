---
name: todoist-automation
description: "通过 Rube MCP（Composio）自动化 Todoist 的任务管理、项目管理、分区管理、筛选和批量操作。始终先搜索工具以获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Todoist 自动化

通过 Composio 的 Todoist 工具包，自动化 Todoist 操作，包括任务创建与管理、项目组织、分区管理、筛选和批量任务工作流。

## 前置条件

- Rube MCP 已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 的 `todoist` 工具包建立活跃的 Todoist 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `todoist`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Todoist OAuth
4. 运行任何工作流前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理任务

**适用场景**：用户需要创建、更新、完成、重新打开或删除任务

**工具调用序列**：
1. `TODOIST_GET_ALL_PROJECTS` - 列出项目以获取目标项目 ID [前置条件]
2. `TODOIST_GET_ALL_SECTIONS` - 列出项目中的分区以确定任务放置位置 [可选]
3. `TODOIST_CREATE_TASK` - 创建单个任务，包含内容、截止日期、优先级、标签 [必需]
4. `TODOIST_BULK_CREATE_TASKS` - 单次请求创建多个任务 [替代方案]
5. `TODOIST_UPDATE_TASK` - 修改任务属性（内容、截止日期、优先级、标签）[可选]
6. `TODOIST_CLOSE_TASK` - 将任务标记为已完成 [可选]
7. `TODOIST_REOPEN_TASK` - 恢复已完成的任务 [可选]
8. `TODOIST_DELETE_TASK` - 永久删除任务 [可选]

**CREATE_TASK 关键参数**：
- `content`：任务标题（支持 markdown 和超链接）
- `description`：附加备注（不要在此处填写截止日期）
- `project_id`：字母数字项目 ID；省略则添加到收件箱
- `section_id`：字母数字分区 ID，用于在项目内指定放置位置
- `parent_id`：父任务 ID，用于创建子任务
- `priority`：1（普通）到 4（紧急）——注意：Todoist 界面显示 p1=紧急，API 中 p4=紧急
- `due_string`：自然语言日期，如 `"tomorrow at 3pm"`、`"every Friday at 9am"`
- `due_date`：具体日期，`YYYY-MM-DD` 格式
- `due_datetime`：具体日期时间，RFC3339 格式 `YYYY-MM-DDTHH:mm:ssZ`
- `labels`：标签名称字符串数组
- `duration` + `duration_unit`：任务时长（如 `30` + `"minute"`）

**注意事项**：
- 同时只能使用一个 `due_*` 字段（`due_lang` 除外，可与任意字段搭配）
- 不要在 `content` 或 `description` 中嵌入截止日期——使用 `due_string` 字段
- 不要在 `due_string` 中嵌入时长短语如 "for 30 minutes"——使用 `duration` + `duration_unit`
- API 中的 `priority`：1=普通，4=紧急（与 Todoist 界面显示相反，界面中 p1=紧急）
- 任务 ID 可以是纯数字或字母数字混合；使用 API 返回的格式
- `CLOSE_TASK` 标记完成，`DELETE_TASK` 永久删除——两者是不同操作

### 2. 管理项目

**适用场景**：用户需要列出、创建、更新或查看项目

**工具调用序列**：
1. `TODOIST_GET_ALL_PROJECTS` - 列出所有项目及元数据 [必需]
2. `TODOIST_GET_PROJECT` - 按 ID 获取特定项目详情 [可选]
3. `TODOIST_CREATE_PROJECT` - 创建新项目，包含名称、颜色、视图样式 [可选]
4. `TODOIST_UPDATE_PROJECT` - 修改项目属性 [可选]

**关键参数**：
- `name`：项目名称（创建时必填）
- `color`：Todoist 调色板颜色（如 `"blue"`、`"red"`、`"green"`、`"charcoal"`）
- `view_style`：`"list"` 或 `"board"` 布局
- `parent_id`：父项目 ID，用于创建子项目
- `is_favorite` / `favorite`：布尔值，标记为收藏
- `project_id`：更新和查询操作时必填

**注意事项**：
- 名称相似的项目可能导致选错 project_id；务必核实
- `CREATE_PROJECT` 使用 `favorite`，而 `UPDATE_PROJECT` 使用 `is_favorite`——字段名不同
- 后续操作使用 API 返回的项目 `id`，而非 `v2_id`
- 字母数字/URL 格式的项目 ID 在某些工具中可能触发 HTTP 400；优先使用数字 ID

### 3. 管理分区

**适用场景**：用户需要在项目中使用分区来组织任务

**工具调用序列**：
1. `TODOIST_GET_ALL_PROJECTS` - 查找目标项目 ID [前置条件]
2. `TODOIST_GET_ALL_SECTIONS` - 列出现有分区以避免重复 [前置条件]
3. `TODOIST_CREATE_SECTION` - 在项目中创建新分区 [必需]
4. `TODOIST_UPDATE_SECTION` - 重命名现有分区 [可选]
5. `TODOIST_DELETE_SECTION` - 永久删除分区 [可选]

**关键参数**：
- `project_id`：必填——要创建分区的项目
- `name`：分区名称（创建时必填）
- `order`：项目内的整数位置（数值越小越靠前）
- `section_id`：更新和删除操作时必填

**注意事项**：
- `CREATE_SECTION` 需要 `project_id` 和 `name`——省略 project_id 会导致 400 错误
- 使用字母数字 ID 时可能出现 HTTP 400 "project_id is invalid"；优先使用数字 ID
- 删除分区可能以非显而易见的方式移动或重新分组其任务
- 响应可能同时包含 `id` 和 `v2_id`；始终存储并复用正确的标识符
- 操作前先检查现有分区，避免创建重复项

### 4. 搜索和筛选任务

**适用场景**：用户需要按条件查找任务、查看今日任务或获取已完成任务历史

**工具调用序列**：
1. `TODOIST_GET_ALL_TASKS` - 获取未完成任务，支持可选筛选查询 [必需]
2. `TODOIST_GET_TASK` - 按 ID 获取特定任务的完整详情 [可选]
3. `TODOIST_GET_COMPLETED_TASKS_BY_COMPLETION_DATE` - 获取指定日期范围内的已完成任务 [可选]
4. `TODOIST_LIST_FILTERS` - 列出用户的自定义已保存筛选器 [可选]

**GET_ALL_TASKS 关键参数**：
- `filter`：Todoist 筛选语法字符串
  - 关键词：`today`、`tomorrow`、`overdue`、`no date`、`recurring`、`subtask`
  - 优先级：`p1`（紧急）、`p2`、`p3`、`p4`（普通）
  - 项目：`#ProjectName`（必须在账户中存在）
  - 标签：`@LabelName`（必须在账户中存在）
  - 日期范围：`7 days`、`-7 days`、`due before: YYYY-MM-DD`、`due after: YYYY-MM-DD`
  - 搜索：`search: keyword` 进行内容文本搜索
  - 运算符：`&`（与）、`|`（或）、`!`（非）
- `ids`：要获取的特定任务 ID 列表

**GET_COMPLETED_TASKS_BY_COMPLETION_DATE 关键参数**：
- `since`：起始日期，RFC3339 格式（如 `2024-01-01T00:00:00Z`）
- `until`：结束日期，RFC3339 格式
- `project_id`、`section_id`、`parent_id`：可选筛选条件
- `cursor`：来自上一次响应的分页游标
- `limit`：每页最大结果数（默认 50）

**注意事项**：
- `GET_ALL_TASKS` 仅返回未完成任务；获取已完成任务请使用 `GET_COMPLETED_TASKS_BY_COMPLETION_DATE`
- 筛选条件必须引用账户中实际存在的实体；任意文本会导致 HTTP 400 错误
- 不要在 GET_ALL_TASKS 筛选器中使用 `completed`、`!completed` 或 `completed after`——会导致 400 错误
- `GET_COMPLETED_TASKS_BY_COMPLETION_DATE` 的 `since` 和 `until` 之间日期范围限制约为 3 个月
- 搜索使用筛选器内的 `search: keyword` 语法，而非单独的参数

### 5. 批量创建任务

**适用场景**：用户需要一次性批量创建多个任务来搭建项目

**工具调用序列**：
1. `TODOIST_GET_ALL_PROJECTS` - 查找目标项目 ID [前置条件]
2. `TODOIST_GET_ALL_SECTIONS` - 查找分区 ID 以确定任务放置位置 [可选]
3. `TODOIST_BULK_CREATE_TASKS` - 单次请求创建多个任务 [必需]

**关键参数**：
- `tasks`：任务对象数组，每个对象至少需要 `content`
- 每个任务对象支持：`content`、`description`、`project_id`、`section_id`、`parent_id`、`priority`、`labels`、`due`（含 `string`、`date` 或 `datetime` 的对象）、`duration`、`order`

**注意事项**：
- 数组中每个任务至少需要 `content` 字段
- 批量创建中的 `due` 字段是包含嵌套字段（`string`、`date`、`datetime`、`lang`）的对象——结构与 CREATE_TASK 的扁平字段不同
- 同一批次中的任务可以指向不同的项目/分区

## 常用模式

### ID 解析
操作前始终将可读名称解析为 ID：
- **项目名称 → 项目 ID**：调用 `TODOIST_GET_ALL_PROJECTS`，按 `name` 字段匹配
- **分区名称 → 分区 ID**：调用 `TODOIST_GET_ALL_SECTIONS` 并传入 `project_id`
- **任务内容 → 任务 ID**：调用 `TODOIST_GET_ALL_TASKS` 并使用 `filter` 或 `search: keyword`

### 分页
- `TODOIST_GET_ALL_TASKS`：返回所有匹配的未完成任务（无需分页）
- `TODOIST_GET_COMPLETED_TASKS_BY_COMPLETION_DATE`：使用游标分页；按响应中的 `cursor` 继续获取直到无更多结果
- `TODOIST_GET_ALL_PROJECTS` 和 `TODOIST_GET_ALL_SECTIONS`：返回所有结果（无需分页）

### 截止日期处理
- 自然语言：使用 `due_string`（如 `"tomorrow at 3pm"`、`"every Monday"`）
- 具体日期：使用 `due_date`，`YYYY-MM-DD` 格式
- 具体日期时间：使用 `due_datetime`，RFC3339 格式（`YYYY-MM-DDTHH:mm:ssZ`）
- 同时只使用一个 due 字段（`due_lang` 除外，可与任意字段搭配）
- 循环任务：在 `due_string` 中使用自然语言（如 `"every Friday at 9am"`）

## 已知陷阱

### ID 格式
- 任务 ID 可以是纯数字（`"2995104339"`）或字母数字混合（`"6X4Vw2Hfmg73Q2XR"`）
- 项目 ID 同样格式不一；优先使用 API 返回的格式
- 某些工具仅接受数字 ID；如遇 400 错误，尝试通过 GET_PROJECT 获取数字 `id`
- 响应对象可能同时包含 `id` 和 `v2_id`；API 操作使用 `id`

### 优先级反转
- API 优先级：1 = 普通，4 = 紧急
- Todoist 界面显示：p1 = 紧急，p4 = 普通
- 两者相反；务必与用户确认其使用的约定

### 筛选语法
- 筛选条件必须引用用户账户中的真实实体
- `#NonExistentProject` 或 `@NonExistentLabel` 会导致 HTTP 400
- 搜索文本使用 `search: keyword`，而非裸关键词
- 使用 `&`（与）、`|`（或）、`!`（非）组合条件
- `completed` 筛选器在 GET_ALL_TASKS 端点上不起作用

### 速率限制
- Todoist API 有速率限制；批量操作应尽可能使用 `BULK_CREATE_TASKS`
- 快速连续请求之间应留出间隔，避免触发限流

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出所有项目 | `TODOIST_GET_ALL_PROJECTS` | （无） |
| 获取项目 | `TODOIST_GET_PROJECT` | `project_id` |
| 创建项目 | `TODOIST_CREATE_PROJECT` | `name`、`color`、`view_style` |
| 更新项目 | `TODOIST_UPDATE_PROJECT` | `project_id`、`name`、`color` |
| 列出分区 | `TODOIST_GET_ALL_SECTIONS` | `project_id` |
| 创建分区 | `TODOIST_CREATE_SECTION` | `project_id`、`name`、`order` |
| 更新分区 | `TODOIST_UPDATE_SECTION` | `section_id`、`name` |
| 删除分区 | `TODOIST_DELETE_SECTION` | `section_id` |
| 获取所有任务 | `TODOIST_GET_ALL_TASKS` | `filter`、`ids` |
| 获取任务 | `TODOIST_GET_TASK` | `task_id` |
| 创建任务 | `TODOIST_CREATE_TASK` | `content`、`project_id`、`due_string`、`priority` |
| 批量创建任务 | `TODOIST_BULK_CREATE_TASKS` | `tasks`（数组） |
| 更新任务 | `TODOIST_UPDATE_TASK` | `task_id`、`content`、`due_string` |
| 完成任务 | `TODOIST_CLOSE_TASK` | `task_id` |
| 重新打开任务 | `TODOIST_REOPEN_TASK` | `task_id` |
| 删除任务 | `TODOIST_DELETE_TASK` | `task_id` |
| 已完成任务 | `TODOIST_GET_COMPLETED_TASKS_BY_COMPLETION_DATE` | `since`、`until` |
| 列出筛选器 | `TODOIST_LIST_FILTERS` | `sync_token` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，应停止并请求澄清。
