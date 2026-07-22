---
name: clickup-automation
description: "通过 Rube MCP (Composio) 自动化 ClickUp 项目管理，包括任务、空间、文件夹、列表、评论和团队操作。始终先搜索工具获取当前 schema。当用户要求自动化 ClickUp 项目管理、创建/更新任务、管理工作区层级、添加评论或管理团队成员时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 ClickUp 自动化

通过 Composio 的 ClickUp 工具包自动化 ClickUp 项目管理工作流，包括任务创建与更新、工作区层级导航、评论和团队成员管理。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并使用 toolkit `clickup` 建立活跃的 ClickUp 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用 toolkit `clickup` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 ClickUp OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理任务

**何时使用**：用户想要创建任务、子任务、更新任务属性，或列出 ClickUp 列表中的任务。

**工具序列**：
1. `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` - 获取工作区/团队 ID [前置条件]
2. `CLICKUP_GET_SPACES` - 列出工作区中的空间 [前置条件]
3. `CLICKUP_GET_FOLDERS` - 列出空间中的文件夹 [前置条件]
4. `CLICKUP_GET_FOLDERLESS_LISTS` - 获取不在文件夹内的列表 [可选]
5. `CLICKUP_GET_LIST` - 验证列表并检查可用状态 [前置条件]
6. `CLICKUP_CREATE_TASK` - 在目标列表中创建任务 [必需]
7. `CLICKUP_CREATE_TASK`（带 `parent`）- 在父任务下创建子任务 [可选]
8. `CLICKUP_UPDATE_TASK` - 修改任务状态、负责人、日期、优先级 [可选]
9. `CLICKUP_GET_TASK` - 获取完整任务详情 [可选]
10. `CLICKUP_GET_TASKS` - 列出列表中的所有任务（带筛选）[可选]
11. `CLICKUP_DELETE_TASK` - 永久删除任务 [可选]

**CLICKUP_CREATE_TASK 的关键参数**：
- `list_id`：目标列表 ID（整数，必需）
- `name`：任务名称（字符串，必需）
- `description`：详细任务描述
- `status`：必须完全匹配（区分大小写）目标列表中配置的状态名称
- `priority`：1（紧急），2（高），3（普通），4（低）
- `assignees`：用户 ID 数组（整数）
- `due_date`：Unix 时间戳（毫秒）
- `parent`：创建子任务时的父任务 ID 字符串
- `tags`：标签名称字符串数组
- `time_estimate`：预估时间（毫秒）

**常见陷阱**：
- `status` 区分大小写，必须匹配列表中已有的状态；使用 `CLICKUP_GET_LIST` 检查可用状态
- `due_date` 和 `start_date` 是 Unix 时间戳，单位为**毫秒**，不是秒
- 子任务的 `parent` 必须是同一列表中的任务（不能是另一个子任务）
- `notify_all` 会触发关注者通知；批量操作时设为 false
- 重试可能创建重复任务；跟踪已创建的任务 ID 以避免重复创建
- 用于里程碑的 `custom_item_id`（ID 1）受工作区计划配额限制

### 2. 导航工作区层级

**何时使用**：用户想要浏览或管理 ClickUp 工作区结构（工作区 > 空间 > 文件夹 > 列表）。

**工具序列**：
1. `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` - 列出所有可访问的工作区 [必需]
2. `CLICKUP_GET_SPACES` - 列出工作区内的空间 [必需]
3. `CLICKUP_GET_SPACE` - 获取特定空间的详情 [可选]
4. `CLICKUP_GET_FOLDERS` - 列出空间中的文件夹 [必需]
5. `CLICKUP_GET_FOLDER` - 获取特定文件夹的详情 [可选]
6. `CLICKUP_CREATE_FOLDER` - 在空间中创建新文件夹 [可选]
7. `CLICKUP_GET_FOLDERLESS_LISTS` - 列出不在任何文件夹内的列表 [必需]
8. `CLICKUP_GET_LIST` - 获取列表详情，包括状态和自定义字段 [可选]

**关键参数**：
- `team_id`：来自 GET_AUTHORIZED_TEAMS_WORKSPACES 的工作区 ID（空间操作必需）
- `space_id`：空间 ID（文件夹和无文件夹列表操作必需）
- `folder_id`：文件夹 ID（GET_FOLDER 必需）
- `list_id`：列表 ID（GET_LIST 必需）
- `archived`：布尔值筛选器，用于已归档/活跃项目

**常见陷阱**：
- ClickUp 层级结构为：工作区（团队）> 空间 > 文件夹 > 列表 > 任务
- 列表可以直接存在于空间下（无文件夹）或文件夹内
- 必须使用 `CLICKUP_GET_FOLDERLESS_LISTS` 查找不在文件夹内的列表；`CLICKUP_GET_FOLDERS` 只返回文件夹
- ClickUp API 中的 `team_id` 指的是工作区 ID，不是用户组

### 3. 为任务添加评论

**何时使用**：用户想要添加评论、查看现有评论或管理任务上的评论线程。

**工具序列**：
1. `CLICKUP_GET_TASK` - 验证任务存在并获取 task_id [前置条件]
2. `CLICKUP_CREATE_TASK_COMMENT` - 为任务添加新评论 [必需]
3. `CLICKUP_GET_TASK_COMMENTS` - 列出任务上的现有评论 [可选]
4. `CLICKUP_UPDATE_COMMENT` - 编辑评论文本、负责人或解决状态 [可选]

**CLICKUP_CREATE_TASK_COMMENT 的关键参数**：
- `task_id`：任务 ID 字符串（必需）
- `comment_text`：评论内容，支持 ClickUp 格式（必需）
- `assignee`：分配评论的用户 ID（必需）
- `notify_all`：true/false，用于关注者通知（必需）

**CLICKUP_GET_TASK_COMMENTS 的关键参数**：
- `task_id`：任务 ID 字符串（必需）
- `start` / `start_id`：用于获取较早评论的分页（每页最多 25 条）

**常见陷阱**：
- `CLICKUP_CREATE_TASK_COMMENT` 需要全部四个字段：`task_id`、`comment_text`、`assignee` 和 `notify_all`
- 评论上的 `assignee` 是将评论（而非任务）分配给该用户
- 评论分页为每页 25 条；使用 `start`（Unix 毫秒）和 `start_id` 获取较早页面
- `CLICKUP_UPDATE_COMMENT` 需要全部四个字段：`comment_id`、`comment_text`、`assignee`、`resolved`

### 4. 管理团队成员和分配

**何时使用**：用户想要查看工作区成员、检查席位使用情况或查询用户详情。

**工具序列**：
1. `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` - 列出工作区并获取 team_id [必需]
2. `CLICKUP_GET_WORKSPACE_SEATS` - 检查席位使用情况（成员 vs 访客）[必需]
3. `CLICKUP_GET_TEAMS` - 列出工作区内的用户组 [可选]
4. `CLICKUP_GET_USER` - 获取特定用户详情（仅限企业版）[可选]
5. `CLICKUP_GET_CUSTOM_ROLES` - 列出自定义权限角色 [可选]

**关键参数**：
- `team_id`：工作区 ID（所有团队操作必需）
- `user_id`：GET_USER 的特定用户 ID
- `group_ids`：逗号分隔的组 ID，用于筛选团队

**常见陷阱**：
- `CLICKUP_GET_WORKSPACE_SEATS` 返回席位数量，而非成员详情；需区分成员和访客
- `CLICKUP_GET_TEAMS` 返回用户组，而非工作区成员；空组不代表没有成员
- `CLICKUP_GET_USER` 仅在 ClickUp 企业版上可用
- 多工作区设置中，需要为每个工作区重复查询席位

### 5. 筛选和查询任务

**何时使用**：用户想要使用特定筛选条件（状态、负责人、日期、标签、自定义字段）查找任务。

**工具序列**：
1. `CLICKUP_GET_TASKS` - 使用多个条件筛选列表中的任务 [必需]
2. `CLICKUP_GET_TASK` - 获取单个任务的完整详情 [可选]

**CLICKUP_GET_TASKS 的关键参数**：
- `list_id`：列表 ID（整数，必需）
- `statuses`：状态字符串数组，用于筛选
- `assignees`：用户 ID 字符串数组
- `tags`：标签名称字符串数组
- `due_date_gt` / `due_date_lt`：Unix 时间戳（毫秒），用于日期范围
- `include_closed`：布尔值，是否包含已关闭任务
- `subtasks`：布尔值，是否包含子任务
- `order_by`："id"、"created"、"updated" 或 "due_date"
- `page`：页码，从 0 开始（每页最多 100 个任务）

**常见陷阱**：
- 只返回主列表为 `list_id` 的任务；子列表中的任务不包含在内
- 日期筛选使用 Unix 时间戳（毫秒）
- 状态字符串必须完全匹配；空格需使用 URL 编码（如 "to%20do"）
- 页码从 0 开始；每页最多返回 100 个任务
- `custom_fields` 筛选接受 JSON 字符串数组，而非对象

## 常用模式

### ID 解析
始终通过层级结构将名称解析为 ID：
- **工作区名称 -> team_id**：`CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` 并按名称匹配
- **空间名称 -> space_id**：使用 `team_id` 调用 `CLICKUP_GET_SPACES`
- **文件夹名称 -> folder_id**：使用 `space_id` 调用 `CLICKUP_GET_FOLDERS`
- **列表名称 -> list_id**：导航文件夹或使用 `CLICKUP_GET_FOLDERLESS_LISTS`
- **任务名称 -> task_id**：使用 `list_id` 调用 `CLICKUP_GET_TASKS` 并按名称匹配

### 分页
- `CLICKUP_GET_TASKS`：基于页码，`page` 从 0 开始，每页最多 100 个任务
- `CLICKUP_GET_TASK_COMMENTS`：使用 `start`（Unix 毫秒）和 `start_id` 进行游标分页，每页最多 25 条
- 持续获取直到返回的项目数少于页面大小

## 已知陷阱

### ID 格式
- 工作区/团队 ID 是大整数
- 空间、文件夹和列表 ID 是整数
- 任务 ID 是字母数字字符串（如 "9hz"、"abc123"）
- 用户 ID 是整数
- 评论 ID 是整数

### 速率限制
- ClickUp 强制执行速率限制；批量创建任务可能触发 429 响应
- 存在 `Retry-After` 头时请遵守
- 批量操作时设置 `notify_all=false` 以减少通知负载

### 参数特性
- API 中的 `team_id` 指工作区 ID，不是用户组
- 任务上的 `status` 区分大小写且因列表而异
- 日期是 Unix 时间戳，单位为**毫秒**（秒数乘以 1000）
- `priority` 是整数 1-4（1=紧急，4=低），不是字符串
- `CLICKUP_CREATE_TASK_COMMENT` 将 `assignee` 和 `notify_all` 标记为必需
- 要清空任务描述，向 `CLICKUP_UPDATE_TASK` 传递单个空格 `" "`

### 层级规则
- 子任务的父任务本身不能是子任务
- 子任务的父任务必须在同一列表中
- 列表可以是无文件夹的（直接在空间中）或在文件夹内
- CLICKUP_CREATE_TASK 不支持子项目看板

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出工作区 | `CLICKUP_GET_AUTHORIZED_TEAMS_WORKSPACES` | (无) |
| 列出空间 | `CLICKUP_GET_SPACES` | `team_id` |
| 获取空间详情 | `CLICKUP_GET_SPACE` | `space_id` |
| 列出文件夹 | `CLICKUP_GET_FOLDERS` | `space_id` |
| 获取文件夹详情 | `CLICKUP_GET_FOLDER` | `folder_id` |
| 创建文件夹 | `CLICKUP_CREATE_FOLDER` | `space_id`, `name` |
| 无文件夹列表 | `CLICKUP_GET_FOLDERLESS_LISTS` | `space_id` |
| 获取列表详情 | `CLICKUP_GET_LIST` | `list_id` |
| 创建任务 | `CLICKUP_CREATE_TASK` | `list_id`, `name`, `status`, `assignees` |
| 更新任务 | `CLICKUP_UPDATE_TASK` | `task_id`, `status`, `priority` |
| 获取任务 | `CLICKUP_GET_TASK` | `task_id`, `include_subtasks` |
| 列出任务 | `CLICKUP_GET_TASKS` | `list_id`, `statuses`, `page` |
| 删除任务 | `CLICKUP_DELETE_TASK` | `task_id` |
| 添加评论 | `CLICKUP_CREATE_TASK_COMMENT` | `task_id`, `comment_text`, `assignee` |
| 列出评论 | `CLICKUP_GET_TASK_COMMENTS` | `task_id`, `start`, `start_id` |
| 更新评论 | `CLICKUP_UPDATE_COMMENT` | `comment_id`, `comment_text`, `resolved` |
| 工作区席位 | `CLICKUP_GET_WORKSPACE_SEATS` | `team_id` |
| 列出用户组 | `CLICKUP_GET_TEAMS` | `team_id` |
| 获取用户详情 | `CLICKUP_GET_USER` | `team_id`, `user_id` |
| 自定义角色 | `CLICKUP_GET_CUSTOM_ROLES` | `team_id` |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
