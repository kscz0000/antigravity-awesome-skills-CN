---
name: posthog-automation
description: "通过 Rube MCP（Composio）自动化 PostHog 任务：事件、功能标志、项目、用户档案、注释。务必先搜索工具以获取当前 schema。当用户要求'自动化 PostHog'、'PostHog 事件'、'功能标志管理'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 PostHog 自动化

借助 Composio 的 PostHog 工具包，通过 Rube MCP 实现 PostHog 产品分析和功能标志管理的自动化。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 配合工具包 `posthog` 建立活跃的 PostHog 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API key——只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `posthog`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 PostHog 认证
4. 确认连接状态显示 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 捕获事件

**使用场景**：用户想向 PostHog 发送事件数据以进行分析追踪

**工具调用顺序**：
1. `POSTHOG_CAPTURE_EVENT` - 向 PostHog 发送一个或多个事件 [必需]

**关键参数**：
- `event`：事件名称（例如 '$pageview'、'user_signed_up'、'purchase_completed'）
- `distinct_id`：唯一用户标识（必填）
- `properties`：包含事件特定属性的对象
- `timestamp`：ISO 8601 格式的时间戳（可选；默认为服务器时间）

**注意事项**：
- 每个事件都必须提供 `distinct_id`，用于标识用户/设备
- PostHog 系统事件使用 `$` 前缀（例如 '$pageview'、'$identify'）
- 自定义事件**不应**使用 `$` 前缀
- 属性是自由格式的；需在各事件间保持 schema 一致
- 事件是异步处理的；入库延迟通常在秒级

### 2. 列出和筛选事件

**使用场景**：用户想浏览或搜索已捕获的事件

**工具调用顺序**：
1. `POSTHOG_LIST_AND_FILTER_PROJECT_EVENTS` - 带筛选条件查询事件 [必需]

**关键参数**：
- `project_id`：PostHog 项目 ID（必填）
- `event`：按事件名称筛选
- `person_id`：按人员 ID 筛选
- `after`：此 ISO 8601 时间戳之后的事件
- `before`：此 ISO 8601 时间戳之前的事件
- `limit`：返回的最大事件数
- `offset`：分页偏移量

**注意事项**：
- `project_id` 是必填项；先通过 LIST_PROJECTS 获取
- 日期筛选使用 ISO 8601 格式（例如 '2024-01-15T00:00:00Z'）
- 大量事件需要分页；使用 `offset` 和 `limit`
- 结果默认按时间倒序返回
- 事件属性是嵌套结构；解析时需注意

### 3. 管理功能标志

**使用场景**：用户想创建、查看或管理功能标志

**工具调用顺序**：
1. `POSTHOG_LIST_AND_MANAGE_PROJECT_FEATURE_FLAGS` - 列出现有功能标志 [必需]
2. `POSTHOG_RETRIEVE_FEATURE_FLAG_DETAILS` - 获取标志的详细配置 [可选]
3. `POSTHOG_CREATE_FEATURE_FLAGS_FOR_PROJECT` - 创建新的功能标志 [可选]

**关键参数**：
- 列出时：`project_id`（必填）
- 查看详情时：`project_id`、`id`（功能标志 ID）
- 创建时：
  - `project_id`：目标项目
  - `key`：标志键名（例如 'new-dashboard-beta'）
  - `name`：人类可读的名称
  - `filters`：定向规则和灰度比例
  - `active`：是否启用该标志

**注意事项**：
- 功能标志的 `key` 在同一项目内必须唯一
- 标志键名应使用 kebab-case（例如 'my-feature-flag'）
- `filters` 定义带有属性和灰度比例的定向分组
- 创建标志时设置 `active: true` 会立即对匹配用户启用
- 由于 PostHog 的轮询机制，标志变更在数秒内生效

### 4. 管理项目

**使用场景**：用户想列出或查看 PostHog 项目和组织

**工具调用顺序**：
1. `POSTHOG_LIST_PROJECTS_IN_ORGANIZATION_WITH_PAGINATION` - 列出所有项目 [必需]

**关键参数**：
- `organization_id`：组织标识符（根据认证方式可能可选）
- `limit`：每页结果数
- `offset`：分页偏移量

**注意事项**：
- 项目 ID 是数字类型；大多数其他端点都需要用到
- 可能需要组织 ID；请检查你的 PostHog 配置
- 分页基于偏移量；持续迭代直到结果为空
- 项目设置中包含 API key 和配置详情

### 5. 用户档案与认证

**使用场景**：用户想查看当前用户信息或验证 API 访问权限

**工具调用顺序**：
1. `POSTHOG_WHOAMI` - 获取当前 API 用户信息 [可选]
2. `POSTHOG_RETRIEVE_CURRENT_USER_PROFILE` - 获取详细用户档案 [可选]

**关键参数**：
- 两个调用都不需要必填参数
- 返回当前已认证用户的详情、权限和组织信息

**注意事项**：
- WHOAMI 是轻量级检查，可用于验证 API 连通性
- 用户档案包含组织成员身份和权限信息
- 这些端点可确认 API key 的访问级别和范围

## 常见模式

### ID 解析

**组织 -> 项目 ID**：
```
1. Call POSTHOG_LIST_PROJECTS_IN_ORGANIZATION_WITH_PAGINATION
2. Find project by name in results
3. Extract id (numeric) for use in other endpoints
```

**功能标志名称 -> 标志 ID**：
```
1. Call POSTHOG_LIST_AND_MANAGE_PROJECT_FEATURE_FLAGS with project_id
2. Find flag by key or name
3. Extract id for detailed operations
```

### 功能标志定向

功能标志支持复杂的定向规则：
```json
{
  "filters": {
    "groups": [
      {
        "properties": [
          {"key": "email", "value": "@company.com", "operator": "icontains"}
        ],
        "rollout_percentage": 100
      },
      {
        "properties": [],
        "rollout_percentage": 10
      }
    ]
  }
}
```
- 分组按顺序评估；第一个匹配的分组决定灰度策略
- 属性用于按用户特征进行筛选
- 灰度比例决定匹配用户中有多大比例能看到该标志

### 分页

- 事件：使用 `offset` 和 `limit`（基于偏移量）
- 功能标志：使用 `offset` 和 `limit`（基于偏移量）
- 项目：使用 `offset` 和 `limit`（基于偏移量）
- 持续请求直到结果数组为空或小于 `limit`

## 已知问题

**项目 ID**：
- 大多数 API 端点都需要
- 务必先将项目名称解析为数字 ID
- 一个组织下可以有多个项目

**事件命名**：
- 系统事件使用 `$` 前缀（$pageview、$identify、$autocapture）
- 自定义事件**不应**使用 `$` 前缀
- 事件名称区分大小写；需保持一致性

**功能标志**：
- 标志键名在同一项目内必须唯一
- 使用 kebab-case 命名标志键
- 变更在数秒内生效
- 删除标志是不可逆的；建议改用禁用

**速率限制**：
- 事件入库有吞吐量限制
- 尽量批量发送事件以提高效率
- API 端点有每分钟速率限制

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `results` 键下
- 分页响应包含 `count`、`next`、`previous` 字段
- 事件属性是嵌套对象；访问时需注意
- 防御性解析，对可选字段设置回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 捕获事件 | POSTHOG_CAPTURE_EVENT | event, distinct_id, properties |
| 列出事件 | POSTHOG_LIST_AND_FILTER_PROJECT_EVENTS | project_id, event, after, before |
| 列出功能标志 | POSTHOG_LIST_AND_MANAGE_PROJECT_FEATURE_FLAGS | project_id |
| 获取标志详情 | POSTHOG_RETRIEVE_FEATURE_FLAG_DETAILS | project_id, id |
| 创建标志 | POSTHOG_CREATE_FEATURE_FLAGS_FOR_PROJECT | project_id, key, filters |
| 列出项目 | POSTHOG_LIST_PROJECTS_IN_ORGANIZATION_WITH_PAGINATION | organization_id |
| 身份查询 | POSTHOG_WHOAMI | （无） |
| 用户档案 | POSTHOG_RETRIEVE_CURRENT_USER_PROFILE | （无） |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来寻求澄清。