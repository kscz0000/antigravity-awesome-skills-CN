---
name: wrike-automation
description: "通过 Rube MCP (Composio) 自动化 Wrike 项目管理：创建任务/文件夹、管理项目、分配工作和跟踪进度。始终先搜索工具以获取当前 schema。触发词：Wrike 自动化、Rube MCP、Composio、Wrike 任务、Wrike 项目管理、任务创建、文件夹管理、成员管理、OAuth 认证"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Wrike

通过 Rube MCP 借助 Composio 的 Wrike 工具包自动化 Wrike 项目管理操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `wrike` 建立有效的 Wrike 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `wrike` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE，按照返回的认证链接完成 Wrike OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和管理任务

**使用场景**：用户希望在 Wrike 中创建、分配或更新任务

**工具调用顺序**：
1. `WRIKE_GET_FOLDERS` - 查找目标文件夹/项目 [前置]
2. `WRIKE_GET_ALL_CUSTOM_FIELDS` - 获取自定义字段 ID（如果需要）[可选]
3. `WRIKE_CREATE_TASK` - 创建新任务 [必需]
4. `WRIKE_MODIFY_TASK` - 更新任务属性 [可选]

**关键参数**：
- `folderId`：任务将要创建于的父文件夹 ID
- `title`：任务标题
- `description`：任务描述（支持 HTML）
- `responsibles`：要分配的用户 ID 数组
- `status`：'Active'、'Completed'、'Deferred'、'Cancelled'
- `importance`：'High'、'Normal'、'Low'
- `customFields`：{id, value} 对象数组
- `dates`：包含 type、start、due、duration 的对象

**陷阱**：
- folderId 是必需的；任务必须属于某个文件夹
- responsibles 需要 Wrike 用户 ID，而非邮箱或姓名
- 自定义字段 ID 必须从 GET_ALL_CUSTOM_FIELDS 获取
- priorityBefore 和 priorityAfter 互斥
- 团队版可能不支持 status 字段
- dates.start 和 dates.due 使用 'YYYY-MM-DD' 格式

### 2. 管理文件夹和项目

**使用场景**：用户希望创建、修改或整理文件夹和项目

**工具调用顺序**：
1. `WRIKE_GET_FOLDERS` - 列出已有文件夹 [必需]
2. `WRIKE_CREATE_FOLDER` - 创建新文件夹/项目 [可选]
3. `WRIKE_MODIFY_FOLDER` - 更新文件夹属性 [可选]
4. `WRIKE_LIST_SUBFOLDERS_BY_FOLDER_ID` - 列出子文件夹 [可选]
5. `WRIKE_DELETE_FOLDER` - 永久删除文件夹 [可选]

**关键参数**：
- `folderId`：创建时的父文件夹 ID；修改时的目标文件夹 ID
- `title`：文件夹名称
- `description`：文件夹描述
- `customItemTypeId`：设置此值以创建为项目而非文件夹
- `shareds`：要共享的用户 ID 或邮箱数组
- `project`：在 GET_FOLDERS 中按项目 (true) 或文件夹 (false) 过滤

**陷阱**：
- DELETE_FOLDER 是永久性的，会删除所有内容（任务、子文件夹、文档）
- 不能将 rootFolderId 或 recycleBinId 修改为父级
- 创建文件夹会自动与创建者共享
- customItemTypeId 将文件夹转换为项目
- GET_FOLDERS 设置 descendants=true 时返回文件夹树（可能很大）

### 3. 检索和跟踪任务

**使用场景**：用户希望查找任务、检查状态或监控进度

**工具调用顺序**：
1. `WRIKE_FETCH_ALL_TASKS` - 列出任务，可带过滤条件 [必需]
2. `WRIKE_GET_TASK_BY_ID` - 获取特定任务的详细信息 [可选]

**关键参数**：
- `status`：按任务状态过滤（'Active'、'Completed' 等）
- `dueDate`：按截止日期范围过滤（start/end/equal）
- `fields`：要在响应中包含的附加字段
- `page_size`：每页结果数（1-100）
- `taskId`：用于详细检索的特定任务 ID
- `resolve_user_names`：自动将用户 ID 解析为姓名（默认 true）

**陷阱**：
- FETCH_ALL_TASKS 每页最多分页 100 项
- dueDate 过滤器支持 'equal'、'start' 和 'end' 字段
- 日期格式：'yyyy-MM-dd' 或 'yyyy-MM-ddTHH:mm:ss'
- GET_TASK_BY_ID 返回只读的详细信息
- 单个任务查询默认返回 customFields

### 4. 启动任务蓝图

**使用场景**：用户希望从预定义模板创建任务

**工具调用顺序**：
1. `WRIKE_LIST_TASK_BLUEPRINTS` - 列出可用的蓝图 [前置]
2. `WRIKE_LIST_SPACE_TASK_BLUEPRINTS` - 列出特定空间中的蓝图 [备选]
3. `WRIKE_LAUNCH_TASK_BLUEPRINT_ASYNC` - 启动蓝图 [必需]

**关键参数**：
- `task_blueprint_id`：要启动的蓝图 ID
- `title`：根任务的标题
- `parent_id`：父文件夹/项目 ID（或 super_task_id）
- `super_task_id`：父任务 ID（或 parent_id）
- `reschedule_date`：任务重新调度的目标日期
- `reschedule_mode`：'RescheduleStartDate' 或 'RescheduleFinishDate'
- `entry_limit`：要复制的最大任务数（1-250）

**陷阱**：
- parent_id 或 super_task_id 二选一，不可同时使用
- 蓝图启动是异步的；任务可能需要时间才会出现
- reschedule_date 需要同时设置 reschedule_mode
- entry_limit 上限为每个蓝图启动 250 个任务/文件夹
- copy_descriptions 默认为 false；设置为 true 以包含任务描述

### 5. 管理工作区和成员

**使用场景**：用户希望管理空间、成员或邀请

**工具调用顺序**：
1. `WRIKE_GET_SPACE` - 获取空间详情 [可选]
2. `WRIKE_GET_CONTACTS` - 列出工作区联系人/成员 [可选]
3. `WRIKE_CREATE_INVITATION` - 邀请用户加入工作区 [可选]
4. `WRIKE_DELETE_SPACE` - 永久删除空间 [可选]

**关键参数**：
- `spaceId`：空间标识符
- `email`：邀请的邮箱
- `role`：用户角色（'Admin'、'Regular User'、'External User'）
- `firstName`/`lastName`：被邀请者姓名

**陷阱**：
- DELETE_SPACE 不可逆，会删除空间的所有内容
- 邀请时 userTypeId 和 role/external 互斥
- 自定义邮件主题/消息需要付费版 Wrike
- GET_CONTACTS 返回工作区级联系人，而非任务特定分配

## 常见模式

### 文件夹 ID 解析

```
1. Call WRIKE_GET_FOLDERS (optionally with project=true for projects only)
2. Navigate folder tree to find target
3. Extract folder id (e.g., 'IEAGKVLFK4IHGQOI')
4. Use as folderId in task/folder creation
```

### 自定义字段设置

```
1. Call WRIKE_GET_ALL_CUSTOM_FIELDS to get definitions
2. Find field by name, extract id and type
3. Format value according to type (text, dropdown, number, date)
4. Include as {id: 'FIELD_ID', value: 'VALUE'} in customFields array
```

### 任务分配

```
1. Call WRIKE_GET_CONTACTS to find user IDs
2. Use user IDs in responsibles array when creating tasks
3. Or use addResponsibles/removeResponsibles when modifying tasks
```

### 分页

- FETCH_ALL_TASKS：使用 page_size（最大 100）并检查是否有更多结果
- GET_FOLDERS：当 descendants=false 且设置了 pageSize 时使用 nextPageToken
- LIST_TASK_BLUEPRINTS：使用 next_page_token 和 page_size（默认 100）

## 已知陷阱

**ID 格式**：
- Wrike ID 是不透明的字母数字字符串（例如 'IEAGTXR7I4IHGABC'）
- 任务 ID、文件夹 ID、空间 ID 和用户 ID 都使用此格式
- 自定义字段 ID 遵循相同模式
- 永远不要猜测 ID；始终通过列表/搜索操作解析

**权限**：
- 操作取决于用户角色和共享设置
- 共享文件夹/任务仅对共享用户可见
- 管理员操作需要相应角色
- 某些功能（自定义状态、计费类型）取决于版本

**删除安全性**：
- DELETE_FOLDER 永久删除所有内容
- DELETE_SPACE 删除整个空间及其内容
- 考虑使用 MODIFY_FOLDER 移到回收站
- 可以通过 MODIFY_FOLDER 设置 restore=true 从回收站还原

**日期处理**：
- 日期使用 'yyyy-MM-dd' 格式
- 日期时间使用 'yyyy-MM-ddTHH:mm:ssZ' 或带时区偏移
- 任务日期包含 type（'Planned'、'Actual'）、start、due、duration
- duration 单位为分钟

## 快速参考

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Create task | WRIKE_CREATE_TASK | folderId, title, responsibles, status |
| Modify task | WRIKE_MODIFY_TASK | taskId, title, status, addResponsibles |
| Get task by ID | WRIKE_GET_TASK_BY_ID | taskId |
| Fetch all tasks | WRIKE_FETCH_ALL_TASKS | status, dueDate, page_size |
| Get folders | WRIKE_GET_FOLDERS | project, descendants |
| Create folder | WRIKE_CREATE_FOLDER | folderId, title |
| Modify folder | WRIKE_MODIFY_FOLDER | folderId, title, addShareds |
| Delete folder | WRIKE_DELETE_FOLDER | folderId |
| List subfolders | WRIKE_LIST_SUBFOLDERS_BY_FOLDER_ID | folderId |
| Get custom fields | WRIKE_GET_ALL_CUSTOM_FIELDS | (none) |
| List blueprints | WRIKE_LIST_TASK_BLUEPRINTS | limit, page_size |
| Launch blueprint | WRIKE_LAUNCH_TASK_BLUEPRINT_ASYNC | task_blueprint_id, title, parent_id |
| Get space | WRIKE_GET_SPACE | spaceId |
| Delete space | WRIKE_DELETE_SPACE | spaceId |
| Get contacts | WRIKE_GET_CONTACTS | (none) |
| Invite user | WRIKE_CREATE_INVITATION | email, role |

## 使用时机
此技能适用于执行上述概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将此输出视为可替代环境特定验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
