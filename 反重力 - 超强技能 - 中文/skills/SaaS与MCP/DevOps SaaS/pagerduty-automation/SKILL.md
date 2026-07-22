---
name: pagerduty-automation
description: "通过 Rube MCP (Composio) 自动化 PagerDuty 任务：管理事件、服务、排班、升级策略和值班轮换。始终先搜索工具获取当前 schema。当用户要求'自动化 PagerDuty 任务'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 PagerDuty 自动化

通过 Composio 的 PagerDuty 工具包，经 Rube MCP 自动化 PagerDuty 事件管理和运维操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `pagerduty` 建立活跃的 PagerDuty 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应以验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `pagerduty`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 PagerDuty 认证
4. 运行任何工作流前确认连接状态为 ACTIVE

## 核心工作流

### 1. 管理事件

**使用场景**：用户想创建、更新、确认或解决事件

**工具调用顺序**：
1. `PAGERDUTY_FETCH_INCIDENT_LIST` - 使用筛选器列出事件 [必需]
2. `PAGERDUTY_RETRIEVE_INCIDENT_BY_INCIDENT_ID` - 获取特定事件详情 [可选]
3. `PAGERDUTY_CREATE_INCIDENT_RECORD` - 创建新事件 [可选]
4. `PAGERDUTY_UPDATE_INCIDENT_BY_ID` - 更新事件状态或分配 [可选]
5. `PAGERDUTY_POST_INCIDENT_NOTE_USING_ID` - 为事件添加备注 [可选]
6. `PAGERDUTY_SNOOZE_INCIDENT_BY_DURATION` - 将事件暂停一段时间 [可选]

**关键参数**：
- `statuses[]`：按状态筛选（'triggered', 'acknowledged', 'resolved'）
- `service_ids[]`：按服务 ID 筛选
- `urgencies[]`：按紧急程度筛选（'high', 'low'）
- `title`：事件标题（创建时使用）
- `service`：含 `id` 和 `type` 的服务对象（创建时使用）
- `status`：更新操作的新状态

**注意事项**：
- 创建事件需要同时包含 `id` 和 `type: 'service_reference'` 的 `service` 对象
- 状态流转遵循：triggered -> acknowledged -> resolved
- 不能从 resolved 直接回退到 triggered
- `PAGERDUTY_UPDATE_INCIDENT_BY_ID` 需要事件 ID 作为路径参数
- 暂停时长以秒为单位；暂停期结束后事件会重新触发

### 2. 查看事件告警和分析

**使用场景**：用户想查看事件中的告警或分析事件指标

**工具调用顺序**：
1. `PAGERDUTY_GET_ALERTS_BY_INCIDENT_ID` - 列出事件的告警 [必需]
2. `PAGERDUTY_GET_INCIDENT_ALERT_DETAILS` - 获取特定告警详情 [可选]
3. `PAGERDUTY_FETCH_INCIDENT_ANALYTICS_BY_ID` - 获取事件分析/指标 [可选]

**关键参数**：
- `incident_id`：事件 ID
- `alert_id`：事件中的特定告警 ID
- `statuses[]`：按状态筛选告警

**注意事项**：
- 一个事件可以有多个告警；每个告警有独立的状态
- 告警 ID 的作用域限定在事件内
- 分析数据包括响应时间、参与度指标和解决时间

### 3. 管理服务

**使用场景**：用户想创建、更新或列出服务

**工具调用顺序**：
1. `PAGERDUTY_RETRIEVE_LIST_OF_SERVICES` - 列出所有服务 [必需]
2. `PAGERDUTY_RETRIEVE_SERVICE_BY_ID` - 获取服务详情 [可选]
3. `PAGERDUTY_CREATE_NEW_SERVICE` - 创建新的技术服务 [可选]
4. `PAGERDUTY_UPDATE_SERVICE_BY_ID` - 更新服务配置 [可选]
5. `PAGERDUTY_CREATE_INTEGRATION_FOR_SERVICE` - 为服务添加集成 [可选]
6. `PAGERDUTY_CREATE_BUSINESS_SERVICE` - 创建业务服务 [可选]
7. `PAGERDUTY_UPDATE_BUSINESS_SERVICE_BY_ID` - 更新业务服务 [可选]

**关键参数**：
- `name`：服务名称
- `escalation_policy`：含 `id` 和 `type` 的升级策略对象
- `alert_creation`：告警创建模式（'create_alerts_and_incidents' 或 'create_incidents'）
- `status`：服务状态（'active', 'warning', 'critical', 'maintenance', 'disabled'）

**注意事项**：
- 创建服务需要已存在的升级策略
- 业务服务与技术服务不同；业务服务代表业务层面的分组
- 服务集成定义了告警的创建方式（邮件、API、事件）
- 禁用服务会停止该服务的所有事件创建

### 4. 管理排班和值班

**使用场景**：用户想查看或管理值班排班和轮换

**工具调用顺序**：
1. `PAGERDUTY_GET_SCHEDULES` - 列出所有排班 [必需]
2. `PAGERDUTY_RETRIEVE_SCHEDULE_BY_ID` - 获取特定排班详情 [可选]
3. `PAGERDUTY_CREATE_NEW_SCHEDULE_LAYER` - 创建新排班 [可选]
4. `PAGERDUTY_UPDATE_SCHEDULE_BY_ID` - 更新现有排班 [可选]
5. `PAGERDUTY_RETRIEVE_ONCALL_LIST` - 查看当前值班人员 [可选]
6. `PAGERDUTY_CREATE_SCHEDULE_OVERRIDES_CONFIGURATION` - 创建临时替班 [可选]
7. `PAGERDUTY_DELETE_SCHEDULE_OVERRIDE_BY_ID` - 删除替班 [可选]
8. `PAGERDUTY_RETRIEVE_USERS_BY_SCHEDULE_ID` - 列出排班中的用户 [可选]
9. `PAGERDUTY_PREVIEW_SCHEDULE_OBJECT` - 保存前预览排班变更 [可选]

**关键参数**：
- `schedule_id`：排班标识符
- `time_zone`：排班时区（如 'America/New_York'）
- `schedule_layers`：轮换层级配置数组
- `since`/`until`：值班查询的日期范围（ISO 8601）
- `override`：替班对象，含用户、开始和结束时间

**注意事项**：
- 排班层级定义轮换顺序；多个层级可以重叠
- 替班是临时的，优先级高于常规排班
- 值班查询需要 `since` 和 `until` 来限定时间范围
- 时区必须是有效的 IANA 时区字符串
- 复杂排班变更前先预览以验证正确性

### 5. 管理升级策略

**使用场景**：用户想创建或修改升级策略

**工具调用顺序**：
1. `PAGERDUTY_FETCH_ESCALATION_POLICES_LIST` - 列出所有升级策略 [必需]
2. `PAGERDUTY_GET_ESCALATION_POLICY_BY_ID` - 获取策略详情 [可选]
3. `PAGERDUTY_CREATE_ESCALATION_POLICY` - 创建新策略 [可选]
4. `PAGERDUTY_UPDATE_ESCALATION_POLICY_BY_ID` - 更新现有策略 [可选]
5. `PAGERDUTY_AUDIT_ESCALATION_POLICY_RECORDS` - 查看策略审计记录 [可选]

**关键参数**：
- `name`：策略名称
- `escalation_rules`：升级规则对象数组
- `num_loops`：规则循环次数后停止（0 = 不循环）
- `escalation_delay_in_minutes`：升级层级之间的延迟

**注意事项**：
- 每条升级规则至少需要一个目标（用户、排班或团队）
- `escalation_delay_in_minutes` 定义升级到下一级别的等待时间
- 将 `num_loops` 设为 0 表示策略只运行一次就停止
- 如果仍有服务引用该策略，删除会失败

### 6. 管理团队

**使用场景**：用户想创建或管理 PagerDuty 团队

**工具调用顺序**：
1. `PAGERDUTY_CREATE_NEW_TEAM_WITH_DETAILS` - 创建新团队 [必需]

**关键参数**：
- `name`：团队名称
- `description`：团队描述

**注意事项**：
- 团队名称在账户内必须唯一
- 团队用于限定服务、升级策略和排班的作用域

## 常用模式

### ID 解析

**服务名称 -> 服务 ID**：
```
1. Call PAGERDUTY_RETRIEVE_LIST_OF_SERVICES
2. Find service by name in response
3. Extract id field
```

**排班名称 -> 排班 ID**：
```
1. Call PAGERDUTY_GET_SCHEDULES
2. Find schedule by name in response
3. Extract id field
```

### 事件生命周期

```
1. Incident triggered (via API, integration, or manual creation)
2. On-call user notified per escalation policy
3. User acknowledges -> status: 'acknowledged'
4. User resolves -> status: 'resolved'
```

### 分页

- PagerDuty 使用基于偏移量的分页
- 检查响应中的 `more` 布尔字段
- 使用 `offset` 和 `limit` 参数
- 继续直到 `more` 为 false

## 已知注意事项

**ID 格式**：
- 所有 PagerDuty ID 都是字母数字字符串（如 'P1234AB'）
- 服务引用需要 `type: 'service_reference'`
- 用户引用需要 `type: 'user_reference'`

**状态流转**：
- 事件：triggered -> acknowledged -> resolved（仅单向）
- 服务：active, warning, critical, maintenance, disabled

**速率限制**：
- PagerDuty API 按账户实施速率限制
- 遇到 429 响应时实现指数退避
- 批量操作应间隔执行

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用防御性解析和回退模式
- 分页使用 `offset`/`limit`/`more` 模式

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出事件 | PAGERDUTY_FETCH_INCIDENT_LIST | statuses[], service_ids[] |
| 获取事件 | PAGERDUTY_RETRIEVE_INCIDENT_BY_INCIDENT_ID | incident_id |
| 创建事件 | PAGERDUTY_CREATE_INCIDENT_RECORD | title, service |
| 更新事件 | PAGERDUTY_UPDATE_INCIDENT_BY_ID | incident_id, status |
| 添加事件备注 | PAGERDUTY_POST_INCIDENT_NOTE_USING_ID | incident_id, content |
| 暂停事件 | PAGERDUTY_SNOOZE_INCIDENT_BY_DURATION | incident_id, duration |
| 获取事件告警 | PAGERDUTY_GET_ALERTS_BY_INCIDENT_ID | incident_id |
| 事件分析 | PAGERDUTY_FETCH_INCIDENT_ANALYTICS_BY_ID | incident_id |
| 列出服务 | PAGERDUTY_RETRIEVE_LIST_OF_SERVICES | (无) |
| 获取服务 | PAGERDUTY_RETRIEVE_SERVICE_BY_ID | service_id |
| 创建服务 | PAGERDUTY_CREATE_NEW_SERVICE | name, escalation_policy |
| 更新服务 | PAGERDUTY_UPDATE_SERVICE_BY_ID | service_id |
| 列出排班 | PAGERDUTY_GET_SCHEDULES | (无) |
| 获取排班 | PAGERDUTY_RETRIEVE_SCHEDULE_BY_ID | schedule_id |
| 获取值班 | PAGERDUTY_RETRIEVE_ONCALL_LIST | since, until |
| 创建替班 | PAGERDUTY_CREATE_SCHEDULE_OVERRIDES_CONFIGURATION | schedule_id |
| 列出升级策略 | PAGERDUTY_FETCH_ESCALATION_POLICES_LIST | (无) |
| 创建升级策略 | PAGERDUTY_CREATE_ESCALATION_POLICY | name, escalation_rules |
| 创建团队 | PAGERDUTY_CREATE_NEW_TEAM_WITH_DETAILS | name, description |

## 使用场景
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。
