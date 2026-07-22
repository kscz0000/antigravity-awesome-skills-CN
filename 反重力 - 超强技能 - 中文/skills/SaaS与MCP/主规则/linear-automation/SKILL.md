---
name: linear-automation
description: "通过 Rube MCP (Composio) 自动化 Linear 任务：issue、项目、周期、团队、标签。始终先搜索工具获取最新 schema。当用户要求'管理 Linear issue'、'创建 Linear 项目'、'操作 Linear 周期'、'Linear 自动化'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Linear

通过 Composio 的 Linear 工具包和 Rube MCP 自动化 Linear 操作。

## 前提条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立了 Linear 连接，toolkit 为 `linear`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `linear`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Linear OAuth
4. 确认连接状态为 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 管理 Issue

**适用场景**：用户需要创建、搜索、更新或列出 Linear issue

**工具调用顺序**：
1. `LINEAR_GET_ALL_LINEAR_TEAMS` - 获取团队 ID [前置条件]
2. `LINEAR_LIST_LINEAR_STATES` - 获取团队的工作流状态 [前置条件]
3. `LINEAR_CREATE_LINEAR_ISSUE` - 创建新 issue [可选]
4. `LINEAR_SEARCH_ISSUES` / `LINEAR_LIST_LINEAR_ISSUES` - 查找 issue [可选]
5. `LINEAR_GET_LINEAR_ISSUE` - 获取 issue 详情 [可选]
6. `LINEAR_UPDATE_ISSUE` - 更新 issue 属性 [可选]

**关键参数**：
- `team_id`：团队 ID（创建时必填）
- `title`：issue 标题
- `description`：issue 描述（支持 Markdown）
- `state_id`：工作流状态 ID
- `assignee_id`：负责人用户 ID
- `priority`：0（无）、1（紧急）、2（高）、3（中）、4（低）
- `label_ids`：标签 ID 数组

**注意事项**：
- 创建 issue 必须提供 Team ID，先调用 GET_ALL_LINEAR_TEAMS
- State ID 是团队级别的，需用对应团队调用 LIST_LINEAR_STATES
- 优先级使用整数 0-4，不是字符串名称

### 2. 管理项目

**适用场景**：用户需要创建或更新 Linear 项目

**工具调用顺序**：
1. `LINEAR_LIST_LINEAR_PROJECTS` - 列出现有项目 [可选]
2. `LINEAR_CREATE_LINEAR_PROJECT` - 创建新项目 [可选]
3. `LINEAR_UPDATE_LINEAR_PROJECT` - 更新项目详情 [可选]

**关键参数**：
- `name`：项目名称
- `description`：项目描述
- `team_ids`：关联团队的 ID 数组
- `state`：项目状态（如 'planned'、'started'、'completed'）

**注意事项**：
- 项目跨团队，可关联多个团队

### 3. 管理周期

**适用场景**：用户需要操作 Linear 周期（迭代）

**工具调用顺序**：
1. `LINEAR_GET_ALL_LINEAR_TEAMS` - 获取团队 ID [前置条件]
2. `LINEAR_GET_CYCLES_BY_TEAM_ID` / `LINEAR_LIST_LINEAR_CYCLES` - 列出周期 [必需]

**关键参数**：
- `team_id`：周期操作对应的团队 ID
- `number`：周期编号

**注意事项**：
- 周期是团队级别的，始终按 team_id 限定范围

### 4. 管理标签和评论

**适用场景**：用户需要创建标签或在 issue 上评论

**工具调用顺序**：
1. `LINEAR_CREATE_LINEAR_LABEL` - 创建新标签 [可选]
2. `LINEAR_CREATE_LINEAR_COMMENT` - 在 issue 上评论 [可选]
3. `LINEAR_UPDATE_LINEAR_COMMENT` - 编辑评论 [可选]

**关键参数**：
- `name`：标签名称
- `color`：标签颜色（十六进制）
- `issue_id`：评论目标 issue 的 ID
- `body`：评论正文（Markdown）

**注意事项**：
- 标签可限定在团队或工作区级别
- 评论正文支持 Markdown 格式

### 5. 自定义 GraphQL 查询

**适用场景**：用户需要标准工具无法覆盖的高级查询

**工具调用顺序**：
1. `LINEAR_RUN_QUERY_OR_MUTATION` - 执行自定义 GraphQL [必需]

**关键参数**：
- `query`：GraphQL 查询或变更字符串
- `variables`：查询变量

**注意事项**：
- 需要了解 Linear 的 GraphQL schema
- GraphQL 查询受速率限制

## 常用模式

### ID 解析

**团队名称 -> 团队 ID**：
```
1. Call LINEAR_GET_ALL_LINEAR_TEAMS
2. Find team by name in response
3. Extract id field
```

**状态名称 -> 状态 ID**：
```
1. Call LINEAR_LIST_LINEAR_STATES with team_id
2. Find state by name
3. Extract id field
```

### 分页

- Linear 工具返回分页结果
- 检查响应中的分页游标
- 将游标传入下次请求获取后续页

## 已知注意事项

**团队范围限定**：
- Issue、状态和周期都是团队级别的
- 创建 issue 前务必先解析 team_id

**优先级数值**：
- 0 = 无优先级，1 = 紧急，2 = 高，3 = 中，4 = 低
- 使用整数值，不是字符串名称

## 速查表

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出团队 | LINEAR_GET_ALL_LINEAR_TEAMS | (无) |
| 创建 issue | LINEAR_CREATE_LINEAR_ISSUE | team_id, title, description |
| 搜索 issue | LINEAR_SEARCH_ISSUES | query |
| 列出 issue | LINEAR_LIST_LINEAR_ISSUES | team_id, filters |
| 获取 issue | LINEAR_GET_LINEAR_ISSUE | issue_id |
| 更新 issue | LINEAR_UPDATE_ISSUE | issue_id, fields |
| 列出状态 | LINEAR_LIST_LINEAR_STATES | team_id |
| 列出项目 | LINEAR_LIST_LINEAR_PROJECTS | (无) |
| 创建项目 | LINEAR_CREATE_LINEAR_PROJECT | name, team_ids |
| 更新项目 | LINEAR_UPDATE_LINEAR_PROJECT | project_id, fields |
| 列出周期 | LINEAR_LIST_LINEAR_CYCLES | team_id |
| 获取周期 | LINEAR_GET_CYCLES_BY_TEAM_ID | team_id |
| 创建标签 | LINEAR_CREATE_LINEAR_LABEL | name, color |
| 创建评论 | LINEAR_CREATE_LINEAR_COMMENT | issue_id, body |
| 更新评论 | LINEAR_UPDATE_LINEAR_COMMENT | comment_id, body |
| 列出用户 | LINEAR_LIST_LINEAR_USERS | (无) |
| 当前用户 | LINEAR_GET_CURRENT_USER | (无) |
| 执行 GraphQL | LINEAR_RUN_QUERY_OR_MUTATION | query, variables |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清
