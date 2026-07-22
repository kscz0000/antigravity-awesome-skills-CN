---
name: jira-automation
description: "通过 Rube MCP (Composio) 自动化 Jira 任务：事项、项目、冲刺、看板、评论、用户。始终先搜索工具获取当前模式。触发词：Jira自动化、Jira任务、Jira事项管理、Jira冲刺、Jira看板、Jira评论、Jira用户管理、Jira MCP、Composio Jira"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Jira 自动化

通过 Rube MCP 使用 Composio 的 Jira 工具包自动化 Jira 操作。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Jira 连接，工具包为 `jira`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `jira` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Jira OAuth
4. 在运行任何工作流之前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 搜索和筛选事项

**适用场景**：用户想使用 JQL 查找事项或浏览项目事项

**工具调用顺序**：
1. `JIRA_SEARCH_FOR_ISSUES_USING_JQL_POST` - 使用 JQL 查询搜索 [必需]
2. `JIRA_GET_ISSUE` - 获取特定事项的完整详情 [可选]

**关键参数**：
- `jql`：JQL 查询字符串（例如 `project = PROJ AND status = "In Progress"`）
- `maxResults`：每页最大结果数（默认 50，最大 100）
- `startAt`：分页偏移量
- `fields`：要返回的字段名数组
- `issueIdOrKey`：事项键，如 'PROJ-123'，用于 GET_ISSUE

**注意事项**：
- JQL 字段名区分大小写，必须与 Jira 配置匹配
- 自定义字段使用 ID，如 `customfield_10001`，而非显示名称
- 结果是分页的；检查 `total` 与 `startAt + maxResults` 以判断是否继续

### 2. 创建和编辑事项

**适用场景**：用户想创建新事项或更新已有事项

**工具调用顺序**：
1. `JIRA_GET_ALL_PROJECTS` - 列出项目以查找项目键 [前置条件]
2. `JIRA_GET_FIELDS` - 获取可用字段及其 ID [前置条件]
3. `JIRA_CREATE_ISSUE` - 创建新事项 [必需]
4. `JIRA_EDIT_ISSUE` - 更新已有事项的字段 [可选]
5. `JIRA_ASSIGN_ISSUE` - 将事项分配给用户 [可选]

**关键参数**：
- `project`：项目键（例如 'PROJ'）
- `issuetype`：事项类型名称（例如 'Bug'、'Story'、'Task'）
- `summary`：事项标题
- `description`：事项描述（Atlassian 文档格式或纯文本）
- `issueIdOrKey`：用于编辑的事项键

**注意事项**：
- 事项类型和必填字段因项目而异；使用 GET_FIELDS 检查
- 自定义字段需要精确的字段 ID，而非显示名称
- 描述可能需要 Atlassian 文档格式（ADF）才能支持富文本内容

### 3. 管理冲刺和看板

**适用场景**：用户想操作敏捷看板、冲刺和待办事项

**工具调用顺序**：
1. `JIRA_LIST_BOARDS` - 列出所有看板 [前置条件]
2. `JIRA_LIST_SPRINTS` - 列出看板的冲刺 [必需]
3. `JIRA_MOVE_ISSUE_TO_SPRINT` - 将事项移至冲刺 [可选]
4. `JIRA_CREATE_SPRINT` - 创建新冲刺 [可选]

**关键参数**：
- `boardId`：来自 LIST_BOARDS 的看板 ID
- `sprintId`：用于移动操作的冲刺 ID
- `name`：冲刺名称（创建时使用）
- `startDate`/`endDate`：ISO 格式的冲刺日期

**注意事项**：
- 看板和冲刺是 Jira Software 专属功能（Jira Core 不支持）
- 每个看板同一时间只能有一个活跃冲刺

### 4. 管理评论

**适用场景**：用户想在事项上添加或查看评论

**工具调用顺序**：
1. `JIRA_LIST_ISSUE_COMMENTS` - 列出现有评论 [可选]
2. `JIRA_ADD_COMMENT` - 在事项上添加评论 [必需]

**关键参数**：
- `issueIdOrKey`：事项键，如 'PROJ-123'
- `body`：评论正文（支持 ADF 富文本）

**注意事项**：
- 评论支持 ADF（Atlassian 文档格式）进行格式化
- @提及使用账户 ID，而非用户名

### 5. 管理项目和用户

**适用场景**：用户想列出项目、查找用户或管理项目角色

**工具调用顺序**：
1. `JIRA_GET_ALL_PROJECTS` - 列出所有项目 [可选]
2. `JIRA_GET_PROJECT` - 获取项目详情 [可选]
3. `JIRA_FIND_USERS` / `JIRA_GET_ALL_USERS` - 搜索用户 [可选]
4. `JIRA_GET_PROJECT_ROLES` - 列出项目角色 [可选]
5. `JIRA_ADD_USERS_TO_PROJECT_ROLE` - 将用户添加到角色 [可选]

**关键参数**：
- `projectIdOrKey`：项目键
- `query`：FIND_USERS 的搜索文本
- `roleId`：角色操作的角色 ID

**注意事项**：
- 用户操作使用账户 ID（而非邮箱或显示名称）
- 项目角色与全局权限不同

## 常用模式

### JQL 语法

**常用运算符**：
- `project = "PROJ"` - 按项目筛选
- `status = "In Progress"` - 按状态筛选
- `assignee = currentUser()` - 当前用户的事项
- `created >= -7d` - 最近 7 天创建
- `labels = "bug"` - 按标签筛选
- `priority = High` - 按优先级筛选
- `ORDER BY created DESC` - 按创建时间降序排列

**组合运算符**：
- `AND` - 两个条件同时满足
- `OR` - 任一条件满足
- `NOT` - 否定条件

### 分页

- 使用 `startAt` 和 `maxResults` 参数
- 检查响应中的 `total` 以确定剩余页数
- 持续翻页直到 `startAt + maxResults >= total`

## 已知注意事项

**字段名称**：
- 自定义字段使用 ID，如 `customfield_10001`
- 使用 JIRA_GET_FIELDS 发现字段 ID 和名称
- JQL 中的字段名可能与 API 字段名不同

**认证**：
- Jira Cloud 使用账户 ID，而非用户名
- 站点 URL 必须在连接中正确配置

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索事项 (JQL) | JIRA_SEARCH_FOR_ISSUES_USING_JQL_POST | jql, maxResults |
| 获取事项 | JIRA_GET_ISSUE | issueIdOrKey |
| 创建事项 | JIRA_CREATE_ISSUE | project, issuetype, summary |
| 编辑事项 | JIRA_EDIT_ISSUE | issueIdOrKey, fields |
| 分配事项 | JIRA_ASSIGN_ISSUE | issueIdOrKey, accountId |
| 添加评论 | JIRA_ADD_COMMENT | issueIdOrKey, body |
| 列出评论 | JIRA_LIST_ISSUE_COMMENTS | issueIdOrKey |
| 列出项目 | JIRA_GET_ALL_PROJECTS | (无) |
| 获取项目 | JIRA_GET_PROJECT | projectIdOrKey |
| 列出看板 | JIRA_LIST_BOARDS | (无) |
| 列出冲刺 | JIRA_LIST_SPRINTS | boardId |
| 移至冲刺 | JIRA_MOVE_ISSUE_TO_SPRINT | sprintId, issues |
| 创建冲刺 | JIRA_CREATE_SPRINT | name, boardId |
| 查找用户 | JIRA_FIND_USERS | query |
| 获取字段 | JIRA_GET_FIELDS | (无) |
| 列出筛选器 | JIRA_LIST_FILTERS | (无) |
| 项目角色 | JIRA_GET_PROJECT_ROLES | projectIdOrKey |
| 项目版本 | JIRA_GET_PROJECT_VERSIONS | projectIdOrKey |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
