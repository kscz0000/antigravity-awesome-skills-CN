---
name: asana-automation
description: "通过 Rube MCP (Composio) 自动化 Asana 操作：任务、项目、分区、团队、工作区。始终先搜索工具获取当前 schema。触发词：Asana自动化、Asana任务、Asana项目管理、Asana工作区、Asana团队管理"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Asana 自动化

通过 Composio 的 Asana 工具包经由 Rube MCP 自动化 Asana 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Asana 连接，工具包为 `asana`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `asana` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Asana OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 管理任务

**何时使用**：用户想要创建、搜索、列出或组织任务

**工具序列**：
1. `ASANA_GET_MULTIPLE_WORKSPACES` - 获取工作区 ID [前置条件]
2. `ASANA_SEARCH_TASKS_IN_WORKSPACE` - 搜索任务 [可选]
3. `ASANA_GET_TASKS_FROM_A_PROJECT` - 列出项目任务 [可选]
4. `ASANA_CREATE_A_TASK` - 创建新任务 [可选]
5. `ASANA_GET_A_TASK` - 获取任务详情 [可选]
6. `ASANA_CREATE_SUBTASK` - 创建子任务 [可选]
7. `ASANA_GET_TASK_SUBTASKS` - 列出子任务 [可选]

**关键参数**：
- `workspace`：工作区 GID（搜索/创建时必需）
- `projects`：要添加任务的项目 GID 数组
- `name`：任务名称
- `notes`：任务描述
- `assignee`：负责人（用户 GID 或邮箱）
- `due_on`：截止日期（YYYY-MM-DD）

**注意事项**：
- 大多数操作需要工作区 GID；请先获取
- 任务 GID 以字符串形式返回，而非整数
- 搜索范围是工作区，而非项目

### 2. 管理项目和分区

**何时使用**：用户想要创建项目、管理分区或组织任务

**工具序列**：
1. `ASANA_GET_WORKSPACE_PROJECTS` - 列出工作区项目 [可选]
2. `ASANA_GET_A_PROJECT` - 获取项目详情 [可选]
3. `ASANA_CREATE_A_PROJECT` - 创建新项目 [可选]
4. `ASANA_GET_SECTIONS_IN_PROJECT` - 列出分区 [可选]
5. `ASANA_CREATE_SECTION_IN_PROJECT` - 创建新分区 [可选]
6. `ASANA_ADD_TASK_TO_SECTION` - 将任务移至分区 [可选]
7. `ASANA_GET_TASKS_FROM_A_SECTION` - 列出分区中的任务 [可选]

**关键参数**：
- `project_gid`：项目 GID
- `name`：项目或分区名称
- `workspace`：创建时的工作区 GID
- `task`：分区分配的任务 GID
- `section`：分区 GID

**注意事项**：
- 项目属于工作区；创建时需要工作区 GID
- 分区在项目中有序排列
- DUPLICATE_PROJECT 创建副本，可选择是否包含任务

### 3. 管理团队和用户

**何时使用**：用户想要列出团队、团队成员或工作区用户

**工具序列**：
1. `ASANA_GET_TEAMS_IN_WORKSPACE` - 列出工作区团队 [可选]
2. `ASANA_GET_USERS_FOR_TEAM` - 列出团队成员 [可选]
3. `ASANA_GET_USERS_FOR_WORKSPACE` - 列出所有工作区用户 [可选]
4. `ASANA_GET_CURRENT_USER` - 获取当前认证用户 [可选]
5. `ASANA_GET_MULTIPLE_USERS` - 获取多个用户详情 [可选]

**关键参数**：
- `workspace_gid`：工作区 GID
- `team_gid`：团队 GID

**注意事项**：
- 用户是工作区范围的
- 团队成员资格需要团队 GID

### 4. 并行操作

**何时使用**：用户需要高效执行批量操作

**工具序列**：
1. `ASANA_SUBMIT_PARALLEL_REQUESTS` - 并行执行多个 API 调用 [必需]

**关键参数**：
- `actions`：包含 method、path 和 data 的操作对象数组

**注意事项**：
- 每个操作必须是有效的 Asana API 调用
- 单个请求失败不会回滚已成功的请求

## 常用模式

### ID 解析

**工作区名称 -> GID**：
```
1. 调用 ASANA_GET_MULTIPLE_WORKSPACES
2. 按名称查找工作区
3. 提取 gid 字段
```

**项目名称 -> GID**：
```
1. 使用工作区 GID 调用 ASANA_GET_WORKSPACE_PROJECTS
2. 按名称查找项目
3. 提取 gid 字段
```

### 分页

- Asana 使用基于游标的分页，通过 `offset` 参数实现
- 检查响应中的 `next_page`
- 使用 `next_page.offset` 中的 `offset` 值进行下一次请求

## 已知注意事项

**GID 格式**：
- 所有 Asana ID 都是字符串（GID），而非整数
- GID 是全局唯一标识符

**工作区范围**：
- 大多数操作需要工作区上下文
- 任务、项目和用户都是工作区范围的

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出工作区 | ASANA_GET_MULTIPLE_WORKSPACES | (无) |
| 搜索任务 | ASANA_SEARCH_TASKS_IN_WORKSPACE | workspace, text |
| 创建任务 | ASANA_CREATE_A_TASK | workspace, name, projects |
| 获取任务 | ASANA_GET_A_TASK | task_gid |
| 创建子任务 | ASANA_CREATE_SUBTASK | parent, name |
| 列出子任务 | ASANA_GET_TASK_SUBTASKS | task_gid |
| 项目任务 | ASANA_GET_TASKS_FROM_A_PROJECT | project_gid |
| 列出项目 | ASANA_GET_WORKSPACE_PROJECTS | workspace |
| 创建项目 | ASANA_CREATE_A_PROJECT | workspace, name |
| 获取项目 | ASANA_GET_A_PROJECT | project_gid |
| 复制项目 | ASANA_DUPLICATE_PROJECT | project_gid |
| 列出分区 | ASANA_GET_SECTIONS_IN_PROJECT | project_gid |
| 创建分区 | ASANA_CREATE_SECTION_IN_PROJECT | project_gid, name |
| 添加到分区 | ASANA_ADD_TASK_TO_SECTION | section, task |
| 分区任务 | ASANA_GET_TASKS_FROM_A_SECTION | section_gid |
| 列出团队 | ASANA_GET_TEAMS_IN_WORKSPACE | workspace_gid |
| 团队成员 | ASANA_GET_USERS_FOR_TEAM | team_gid |
| 工作区用户 | ASANA_GET_USERS_FOR_WORKSPACE | workspace_gid |
| 当前用户 | ASANA_GET_CURRENT_USER | (无) |
| 并行请求 | ASANA_SUBMIT_PARALLEL_REQUESTS | actions |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
