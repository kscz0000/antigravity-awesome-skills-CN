---
name: sentry-automation
description: "通过 Rube MCP (Composio) 自动化 Sentry 任务：管理 issues/events、配置告警、追踪发布、监控项目和团队。始终先搜索工具以获取当前 schema。触发词：Sentry 自动化、Sentry 错误追踪、Sentry 告警配置、Sentry 发布管理、Sentry 监控、sentry automation、sentry alerts"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Sentry 自动化

通过 Composio 的 Sentry 工具包（经由 Rube MCP）自动化 Sentry 错误追踪和监控操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `sentry` 工具包建立活跃的 Sentry 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用 `RUBE_MANAGE_CONNECTIONS` 配合工具包 `sentry` 进行调用
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Sentry OAuth
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 调查 Issues

**使用场景**：用户想要查找、检查或分流错误 issues

**工具调用序列**：
1. `SENTRY_LIST_AN_ORGANIZATIONS_ISSUES` - 列出组织中的 issues [必需]
2. `SENTRY_GET_ORGANIZATION_ISSUE_DETAILS` - 获取特定 issue 的详细信息 [可选]
3. `SENTRY_LIST_AN_ISSUES_EVENTS` - 查看特定 issue 的独立错误事件 [可选]
4. `SENTRY_RETRIEVE_AN_ISSUE_EVENT` - 获取包含堆栈跟踪的完整事件详情 [可选]
5. `SENTRY_RETRIEVE_ISSUE_TAG_DETAILS` - 检查 issue 的标签分布 [可选]

**关键参数**：
- `organization_id_or_slug`：组织标识符
- `issue_id`：数字格式的 issue ID
- `query`：搜索查询（如 `is:unresolved`、`assigned:me`、`browser:Chrome`）
- `sort`：排序方式（`date`、`new`、`freq`、`priority`）
- `statsPeriod`：统计时间窗口（`24h`、`14d` 等）

**注意事项**：
- `organization_id_or_slug` 是组织 slug（如 'my-org'），不是显示名称
- Issue ID 是数字；不要与 UUID 格式的 event ID 混淆
- 查询语法使用 Sentry 的搜索格式：`is:unresolved`、`assigned:me`、`!has:release`
- 同一 issue 内的事件可能有不同的堆栈跟踪；需检查具体事件获取详情

### 2. 管理项目 Issues

**使用场景**：用户想要查看特定项目范围内的 issues

**工具调用序列**：
1. `SENTRY_RETRIEVE_ORGANIZATION_PROJECTS` - 列出项目以获取项目 slug [前置步骤]
2. `SENTRY_RETRIEVE_PROJECT_ISSUES_LIST` - 列出特定项目的 issues [必需]
3. `SENTRY_RETRIEVE_ISSUE_EVENTS_BY_ID` - 获取特定 issue 的事件 [可选]

**关键参数**：
- `organization_id_or_slug`：组织标识符
- `project_id_or_slug`：项目标识符
- `query`：搜索过滤字符串
- `statsPeriod`：统计时间窗口

**注意事项**：
- 项目 slug 与项目显示名称不同
- 始终先通过 RETRIEVE_ORGANIZATION_PROJECTS 将项目名称解析为 slug
- 项目范围的 issue 列表可能与组织范围的列表有不同的分页

### 3. 配置告警规则

**使用场景**：用户想要为项目创建或管理告警规则

**工具调用序列**：
1. `SENTRY_RETRIEVE_ORGANIZATION_PROJECTS` - 找到告警对应的项目 [前置步骤]
2. `SENTRY_RETRIEVE_PROJECT_RULES_BY_ORG_AND_PROJECT_ID` - 列出现有规则 [可选]
3. `SENTRY_CREATE_PROJECT_RULE_FOR_ALERTS` - 创建新的告警规则 [必需]
4. `SENTRY_CREATE_ORGANIZATION_ALERT_RULE` - 创建组织级指标告警 [备选]
5. `SENTRY_UPDATE_ORGANIZATION_ALERT_RULES` - 更新现有告警规则 [可选]
6. `SENTRY_RETRIEVE_ALERT_RULE_DETAILS` - 检查特定告警规则详情 [可选]
7. `SENTRY_GET_PROJECT_RULE_DETAILS` - 获取项目级规则详情 [可选]

**关键参数**：
- `name`：告警规则名称
- `conditions`：触发条件数组
- `actions`：触发时执行的操作数组
- `filters`：事件过滤器数组
- `frequency`：触发频率（单位：分钟）
- `actionMatch`：条件匹配方式，'all'、'any' 或 'none'

**注意事项**：
- 项目级规则（CREATE_PROJECT_RULE）和组织级指标告警（CREATE_ORGANIZATION_ALERT_RULE）是不同的
- conditions、actions 和 filters 使用特定的 JSON schema；请查阅 Sentry 文档了解有效类型
- `frequency` 单位是分钟；设置过低会导致告警疲劳
- `actionMatch` 默认值可能不同；建议显式设置以避免意外行为

### 4. 管理发布版本

**使用场景**：用户想要创建、追踪或管理发布版本

**工具调用序列**：
1. `SENTRY_LIST_ORGANIZATION_RELEASES` - 列出现有发布版本 [可选]
2. `SENTRY_CREATE_RELEASE_FOR_ORGANIZATION` - 创建新的发布版本 [必需]
3. `SENTRY_UPDATE_RELEASE_DETAILS_FOR_ORGANIZATION` - 更新发布版本元数据 [可选]
4. `SENTRY_CREATE_RELEASE_DEPLOY_FOR_ORG` - 记录发布版本的部署信息 [可选]
5. `SENTRY_UPLOAD_RELEASE_FILE_TO_ORGANIZATION` - 上传 source map 或文件 [可选]

**关键参数**：
- `version`：发布版本字符串（如 '1.0.0'、commit SHA）
- `projects`：该发布版本所属的项目 slug 数组
- `dateReleased`：发布时间戳（ISO 8601 格式）
- `environment`：部署环境名称（如 'production'、'staging'）

**注意事项**：
- 发布版本在组织内必须唯一
- 发布版本可跨多个项目；使用 `projects` 数组
- 部署发布版本与创建发布版本是独立操作；使用 CREATE_RELEASE_DEPLOY
- 上传 source map 需要发布版本已存在

### 5. 监控组织和团队

**使用场景**：用户想要查看组织结构、团队或成员列表

**工具调用序列**：
1. `SENTRY_GET_ORGANIZATION_DETAILS` 或 `SENTRY_GET_ORGANIZATION_BY_ID_OR_SLUG` - 获取组织信息 [必需]
2. `SENTRY_LIST_TEAMS_IN_ORGANIZATION` - 列出所有团队 [可选]
3. `SENTRY_LIST_ORGANIZATION_MEMBERS` - 列出组织成员 [可选]
4. `SENTRY_GET_PROJECT_LIST` - 列出所有可访问的项目 [可选]

**关键参数**：
- `organization_id_or_slug`：组织标识符
- `cursor`：用于大型结果集的分页游标

**注意事项**：
- 组织 slug 是 URL 安全标识符，不是显示名称
- 成员列表可能有分页；使用游标分页
- 团队和成员的可见性取决于认证用户的权限

### 6. 管理监控器（Cron 监控）

**使用场景**：用户想要更新 cron 任务监控配置

**工具调用序列**：
1. `SENTRY_UPDATE_A_MONITOR` - 更新监控器配置 [必需]

**关键参数**：
- `organization_id_or_slug`：组织标识符
- `monitor_id_or_slug`：监控器标识符
- `name`：监控器显示名称
- `schedule`：Cron 调度表达式或间隔
- `checkin_margin`：延迟签到的宽限期（单位：分钟）
- `max_runtime`：预期最大运行时间（单位：分钟）

**注意事项**：
- 监控器 slug 从名称自动生成；API 调用时使用 slug
- 调度变更立即生效
- 缺失签到在宽限期过后触发告警

## 常用模式

### ID 解析

**组织名称 -> Slug**：
```
1. 调用 SENTRY_GET_ORGANIZATION_DETAILS
2. 从响应中提取 slug 字段
```

**项目名称 -> Slug**：
```
1. 调用 SENTRY_RETRIEVE_ORGANIZATION_PROJECTS
2. 按名称查找项目，提取 slug
```

### 分页

- Sentry 使用基于游标的分页，通过 `Link` 响应头实现
- 检查响应中的游标值
- 在下一次请求中传递游标，直到没有更多页面

### 搜索查询语法

- `is:unresolved` - 未解决的 issues
- `is:resolved` - 已解决的 issues
- `assigned:me` - 分配给当前用户
- `assigned:team-slug` - 分配给某团队
- `!has:release` - 没有关联发布版本的 issues
- `first-release:1.0.0` - 首次出现在该发布版本中的 issues
- `times-seen:>100` - 出现超过 100 次
- `browser:Chrome` - 按浏览器标签过滤

## 已知陷阱

**ID 格式**：
- 组织：使用 slug（如 'my-org'），不是显示名称
- 项目：使用 slug（如 'my-project'），不是显示名称
- Issue ID：数字整数
- Event ID：UUID（32 位十六进制字符串）

**权限**：
- API Token 的作用域必须匹配所执行的操作
- 组织级操作需要组织级权限
- 项目级操作需要项目访问权限

**速率限制**：
- Sentry 强制执行组织级速率限制
- 收到 429 响应时实施退避策略
- 批量操作应错开执行

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|----------|
| 列出组织 issues | SENTRY_LIST_AN_ORGANIZATIONS_ISSUES | organization_id_or_slug, query |
| 获取 issue 详情 | SENTRY_GET_ORGANIZATION_ISSUE_DETAILS | organization_id_or_slug, issue_id |
| 列出 issue 事件 | SENTRY_LIST_AN_ISSUES_EVENTS | issue_id |
| 获取事件详情 | SENTRY_RETRIEVE_AN_ISSUE_EVENT | organization_id_or_slug, event_id |
| 列出项目 issues | SENTRY_RETRIEVE_PROJECT_ISSUES_LIST | organization_id_or_slug, project_id_or_slug |
| 列出项目 | SENTRY_RETRIEVE_ORGANIZATION_PROJECTS | organization_id_or_slug |
| 获取组织详情 | SENTRY_GET_ORGANIZATION_DETAILS | organization_id_or_slug |
| 列出团队 | SENTRY_LIST_TEAMS_IN_ORGANIZATION | organization_id_or_slug |
| 列出成员 | SENTRY_LIST_ORGANIZATION_MEMBERS | organization_id_or_slug |
| 创建告警规则 | SENTRY_CREATE_PROJECT_RULE_FOR_ALERTS | organization_id_or_slug, project_id_or_slug |
| 创建指标告警 | SENTRY_CREATE_ORGANIZATION_ALERT_RULE | organization_id_or_slug |
| 创建发布版本 | SENTRY_CREATE_RELEASE_FOR_ORGANIZATION | organization_id_or_slug, version |
| 部署发布版本 | SENTRY_CREATE_RELEASE_DEPLOY_FOR_ORG | organization_id_or_slug, version |
| 列出发布版本 | SENTRY_LIST_ORGANIZATION_RELEASES | organization_id_or_slug |
| 更新监控器 | SENTRY_UPDATE_A_MONITOR | organization_id_or_slug, monitor_id_or_slug |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
