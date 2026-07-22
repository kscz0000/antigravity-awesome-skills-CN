---
name: monday-automation
description: "通过 Rube MCP (Composio) 自动化 Monday.com 工作管理，包括看板、事项、列、分组、子事项和更新。始终先搜索工具以获取当前 schema。当用户要求'自动化 Monday.com 工作管理'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Monday.com

通过 Composio 的 Monday 工具包自动化 Monday.com 工作管理流程，包括看板创建、事项管理、列值更新、分组组织、子事项和更新/评论线程。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 Monday.com 活跃连接，toolkit 设为 `monday`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `monday`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Monday.com OAuth
4. 确认连接状态为 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 创建和管理看板

**适用场景**：用户需要创建新看板、列出现有看板或搭建工作区结构。

**工具调用顺序**：
1. `MONDAY_GET_WORKSPACES` - 列出可用工作区并解析工作区 ID [前置条件]
2. `MONDAY_LIST_BOARDS` - 列出现有看板以检查重复 [可选]
3. `MONDAY_CREATE_BOARD` - 创建带有名称、类型和工作区的新看板 [必需]
4. `MONDAY_CREATE_COLUMN` - 向新看板添加列 [可选]
5. `MONDAY_CREATE_GROUP` - 添加分组以组织事项 [可选]
6. `MONDAY_BOARDS` - 获取看板详细元数据 [可选]

**关键参数**：
- `board_name`：新看板名称（必需）
- `board_kind`："public"、"private" 或 "share"（必需）
- `workspace_id`：数字工作区 ID；省略则使用默认工作区
- `folder_id`：文件夹 ID；若同时提供 `workspace_id`，文件夹必须在该工作区内
- `template_id`：可访问的模板 ID，用于克隆

**注意事项**：
- `board_kind` 为必需参数，必须为 "public"、"private"、"share" 之一
- 若同时提供 `workspace_id` 和 `folder_id`，文件夹必须存在于该工作区内
- `template_id` 必须引用已认证用户可访问的模板
- 看板 ID 为大整数；始终使用 API 响应中的精确值

### 2. 创建和管理事项

**适用场景**：用户需要向看板添加任务/事项、列出现有事项或在分组间移动事项。

**工具调用顺序**：
1. `MONDAY_LIST_BOARDS` - 将看板名称解析为看板 ID [前置条件]
2. `MONDAY_LIST_GROUPS` - 列出看板上的分组以获取 group_id [前置条件]
3. `MONDAY_LIST_COLUMNS` - 获取列 ID 和类型以设置值 [前置条件]
4. `MONDAY_CREATE_ITEM` - 创建带有名称和列值的新事项 [必需]
5. `MONDAY_LIST_BOARD_ITEMS` - 列出看板上所有事项 [可选]
6. `MONDAY_MOVE_ITEM_TO_GROUP` - 将事项移动到其他分组 [可选]
7. `MONDAY_ITEMS_PAGE` - 带过滤的分页事项检索 [可选]

**关键参数**：
- `board_id`：看板 ID（必需，整数）
- `item_name`：事项名称，最长 256 字符（必需）
- `group_id`：放置事项的分组 ID 字符串（可选）
- `column_values`：将列 ID 映射到值的 JSON 对象或字符串

**注意事项**：
- `column_values` 必须使用列 ID（非标题）；通过 `MONDAY_LIST_COLUMNS` 获取
- 列值格式因类型而异：status 使用 `{"index": 0}` 或 `{"label": "Done"}`，date 使用 `{"date": "YYYY-MM-DD"}`，people 使用 `{"personsAndTeams": [{"id": 123, "kind": "person"}]}`
- `item_name` 最长 256 字符
- 子事项看板不支持 `MONDAY_CREATE_ITEM`；需通过 `MONDAY_CREATE_OBJECT` 使用 GraphQL

### 3. 更新事项列值

**适用场景**：用户需要更改现有事项的状态、日期、文本或其他列值。

**工具调用顺序**：
1. `MONDAY_LIST_COLUMNS` 或 `MONDAY_COLUMNS` - 获取列 ID 和类型 [前置条件]
2. `MONDAY_LIST_BOARD_ITEMS` 或 `MONDAY_ITEMS_PAGE` - 查找目标事项 ID [前置条件]
3. `MONDAY_CHANGE_SIMPLE_COLUMN_VALUE` - 用字符串值更新文本、状态或下拉列 [必需]
4. `MONDAY_UPDATE_ITEM` - 用 JSON 更新复杂列类型（时间线、人员、日期）[必需]

**MONDAY_CHANGE_SIMPLE_COLUMN_VALUE 关键参数**：
- `board_id`：看板 ID（整数，必需）
- `item_id`：事项 ID（整数，必需）
- `column_id`：列 ID 字符串（必需）
- `value`：简单字符串值（如 "Done"、"Working on it"）
- `create_labels_if_missing`：设为 true 可自动创建状态/下拉标签（默认 true）

**MONDAY_UPDATE_ITEM 关键参数**：
- `board_id`：看板 ID（整数，必需）
- `item_id`：事项 ID（整数，必需）
- `column_id`：列 ID 字符串（必需）
- `value`：与列类型 schema 匹配的 JSON 对象
- `create_labels_if_missing`：默认 false；状态/下拉列设为 true

**注意事项**：
- 简单文本/状态/下拉更新使用 `MONDAY_CHANGE_SIMPLE_COLUMN_VALUE`（字符串值）
- 复杂类型如时间线、人员、日期使用 `MONDAY_UPDATE_ITEM`（JSON 值）
- 列 ID 为带下划线的小写字符串（如 "status_1"、"date_2"、"text"）；通过 `MONDAY_LIST_COLUMNS` 获取
- 状态值可通过标签名（"Done"）或索引号（"1"）设置
- `create_labels_if_missing` 默认值不同：CHANGE_SIMPLE 为 true，UPDATE_ITEM 为 false

### 4. 使用分组和看板结构

**适用场景**：用户需要将事项组织到分组中、添加列或查看看板结构。

**工具调用顺序**：
1. `MONDAY_LIST_BOARDS` - 解析看板 ID [前置条件]
2. `MONDAY_LIST_GROUPS` - 列出看板上所有分组 [必需]
3. `MONDAY_CREATE_GROUP` - 创建新分组 [可选]
4. `MONDAY_LIST_COLUMNS` 或 `MONDAY_COLUMNS` - 查看列结构 [必需]
5. `MONDAY_CREATE_COLUMN` - 向看板添加新列 [可选]
6. `MONDAY_MOVE_ITEM_TO_GROUP` - 跨分组重新组织事项 [可选]

**关键参数**：
- `board_id`：看板 ID（所有分组/列操作的必需参数）
- `group_name`：新分组名称（CREATE_GROUP）
- `column_type`：必须为有效的 GraphQL 枚举值，snake_case 格式（如 "status"、"text"、"long_text"、"numbers"、"date"、"dropdown"、"people"）
- `title`：列显示标题
- `defaults`：状态/下拉标签的 JSON 字符串，如 `'{"labels": ["To Do", "In Progress", "Done"]}'`

**注意事项**：
- `column_type` 必须为精确的 snake_case 值；"person" 无效，应使用 "people"
- 分组 ID 为字符串（如 "topics"、"new_group_12345"），非整数
- `MONDAY_COLUMNS` 接受 `board_ids` 数组，返回包含设置的列元数据
- `MONDAY_LIST_COLUMNS` 更简单，接受单个 `board_id`

### 5. 管理子事项和更新

**适用场景**：用户需要查看任务的子事项或向事项添加评论/更新。

**工具调用顺序**：
1. `MONDAY_LIST_BOARD_ITEMS` - 查找父事项 ID [前置条件]
2. `MONDAY_LIST_SUBITEMS_BY_PARENT` - 检索带列值的子事项 [必需]
3. `MONDAY_CREATE_UPDATE` - 向事项添加评论/更新 [可选]
4. `MONDAY_CREATE_OBJECT` - 通过 GraphQL mutation 创建子事项 [可选]

**MONDAY_LIST_SUBITEMS_BY_PARENT 关键参数**：
- `parent_item_ids`：父事项 ID 数组（整数数组，必需）
- `include_column_values`：设为 true 包含列数据（默认 true）
- `include_parent_fields`：设为 true 包含父事项信息（默认 true）

**MONDAY_CREATE_OBJECT 关键参数**（GraphQL）：
- `query`：完整 GraphQL mutation 字符串
- `variables`：可选变量对象

**注意事项**：
- 子事项只能通过其父事项查询
- 创建子事项需使用 `MONDAY_CREATE_OBJECT` 配合 `create_subitem` GraphQL mutation
- `MONDAY_CREATE_UPDATE` 用于向事项添加评论/更新（Monday 的"更新"功能），而非修改事项值
- `MONDAY_CREATE_OBJECT` 是原始 GraphQL 端点；确保 mutation 语法正确

## 常用模式

### ID 解析
操作前始终将显示名称解析为 ID：
- **看板名 -> board_id**：`MONDAY_LIST_BOARDS` 按名称匹配
- **分组名 -> group_id**：`MONDAY_LIST_GROUPS` 配合 `board_id`
- **列标题 -> column_id**：`MONDAY_LIST_COLUMNS` 配合 `board_id`
- **工作区名 -> workspace_id**：`MONDAY_GET_WORKSPACES` 按名称匹配
- **事项名 -> item_id**：`MONDAY_LIST_BOARD_ITEMS` 或 `MONDAY_ITEMS_PAGE`

### 分页
Monday.com 对事项使用基于游标的分页：
- `MONDAY_ITEMS_PAGE` 在响应中返回 `cursor` 用于下一页
- 将 `cursor` 传入下次调用；提供 cursor 时忽略 `board_id` 和 `query_params`
- 游标缓存 60 分钟
- 每页最大 `limit` 为 500
- `MONDAY_LIST_BOARDS` 和 `MONDAY_GET_WORKSPACES` 使用基于页码的分页，参数为 `page` 和 `limit`

### 列值格式化
不同列类型需要不同的值格式：
- **Status**：`{"index": 0}` 或 `{"label": "Done"}` 或简单字符串 "Done"
- **Date**：`{"date": "YYYY-MM-DD"}`
- **People**：`{"personsAndTeams": [{"id": 123, "kind": "person"}]}`
- **Text/Numbers**：纯字符串或数字
- **Timeline**：`{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}`

## 已知注意事项

### ID 格式
- 看板 ID 和事项 ID 为大整数（如 1234567890）
- 分组 ID 为字符串（如 "topics"、"new_group_12345"）
- 列 ID 为短字符串（如 "status_1"、"date4"、"text"）
- 工作区 ID 为整数

### 速率限制
- Monday.com GraphQL API 采用基于复杂度的速率限制
- 列较多的大看板会增加查询复杂度
- 触发限制时使用 `limit` 参数减少每次请求的事项数

### 参数特性
- CREATE_COLUMN 的 `column_type` 必须为精确的 snake_case 枚举值；用 "people" 而非 "person"
- CREATE_ITEM 的 `column_values` 同时接受 JSON 字符串和对象格式
- `MONDAY_CHANGE_SIMPLE_COLUMN_VALUE` 默认自动创建缺失标签；`MONDAY_UPDATE_ITEM` 不会
- `MONDAY_CREATE_OBJECT` 是原始 GraphQL 接口；用于没有专用工具的操作（如 create_subitem、delete_item、archive_board）

### 响应结构
- 看板事项以数组返回，包含 `id`、`name` 和 `state` 字段
- 列值同时包含原始 `value`（JSON）和渲染后的 `text`（显示字符串）
- 子事项嵌套在父事项下，无法独立查询

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出工作区 | `MONDAY_GET_WORKSPACES` | `kind`, `state`, `limit` |
| 创建工作区 | `MONDAY_CREATE_WORKSPACE` | `name`, `kind` |
| 列出看板 | `MONDAY_LIST_BOARDS` | `limit`, `page`, `state` |
| 创建看板 | `MONDAY_CREATE_BOARD` | `board_name`, `board_kind`, `workspace_id` |
| 获取看板元数据 | `MONDAY_BOARDS` | `board_ids`, `board_kind` |
| 列出分组 | `MONDAY_LIST_GROUPS` | `board_id` |
| 创建分组 | `MONDAY_CREATE_GROUP` | `board_id`, `group_name` |
| 列出列 | `MONDAY_LIST_COLUMNS` | `board_id` |
| 获取列元数据 | `MONDAY_COLUMNS` | `board_ids`, `column_types` |
| 创建列 | `MONDAY_CREATE_COLUMN` | `board_id`, `column_type`, `title` |
| 创建事项 | `MONDAY_CREATE_ITEM` | `board_id`, `item_name`, `column_values` |
| 列出看板事项 | `MONDAY_LIST_BOARD_ITEMS` | `board_id` |
| 分页事项 | `MONDAY_ITEMS_PAGE` | `board_id`, `limit`, `query_params` |
| 更新列（简单） | `MONDAY_CHANGE_SIMPLE_COLUMN_VALUE` | `board_id`, `item_id`, `column_id`, `value` |
| 更新列（复杂） | `MONDAY_UPDATE_ITEM` | `board_id`, `item_id`, `column_id`, `value` |
| 移动事项到分组 | `MONDAY_MOVE_ITEM_TO_GROUP` | `item_id`, `group_id` |
| 列出子事项 | `MONDAY_LIST_SUBITEMS_BY_PARENT` | `parent_item_ids` |
| 添加评论/更新 | `MONDAY_CREATE_UPDATE` | `item_id`, `body` |
| 原始 GraphQL mutation | `MONDAY_CREATE_OBJECT` | `query`, `variables` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清
