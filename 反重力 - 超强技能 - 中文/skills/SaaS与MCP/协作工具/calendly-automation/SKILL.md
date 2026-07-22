---
name: calendly-automation
description: "通过 Rube MCP (Composio) 自动化 Calendly 日程安排、事件管理、邀请者追踪、可用性检查和组织管理。当用户要求'Calendly自动化'、'日程安排'、'事件管理'、'检查可用时间'或'组织管理'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Calendly 自动化

通过 Composio 的 Calendly 工具包自动化 Calendly 操作，包括事件列表、邀请者管理、调度链接创建、可用性查询和组织管理。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `calendly` 建立活跃的 Calendly 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema
- 许多操作需要用户的 Calendly URI，可通过 `CALENDLY_GET_CURRENT_USER` 获取

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `calendly`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Calendly OAuth
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 列出和查看已安排事件

**使用场景**：用户想查看即将到来、过去或筛选后的 Calendly 事件

**工具调用顺序**：
1. `CALENDLY_GET_CURRENT_USER` - 获取已认证用户 URI 和组织 URI [前置条件]
2. `CALENDLY_LIST_EVENTS` - 按用户、组织或群组范围列出事件 [必需]
3. `CALENDLY_GET_EVENT` - 通过 UUID 获取特定事件的详细信息 [可选]

**关键参数**：
- `user`：完整的 Calendly API URI（如 `https://api.calendly.com/users/{uuid}`）- 不能是 `"me"`
- `organization`：组织范围查询的完整组织 URI
- `status`：`"active"` 或 `"canceled"`
- `min_start_time` / `max_start_time`：UTC 时间戳（如 `2024-01-01T00:00:00.000000Z`）
- `invitee_email`：按邀请者邮箱筛选事件（仅作筛选器，非范围）
- `sort`：`"start_time:asc"` 或 `"start_time:desc"`
- `count`：每页结果数（默认 20）
- `page_token`：上一次响应的分页 token

**常见陷阱**：
- 必须且只能提供 `user`、`organization` 或 `group` 中的一个——省略或组合范围会导致失败
- `user` 参数需要完整的 API URI，不能是 `"me"`——先使用 `CALENDLY_GET_CURRENT_USER`
- `invitee_email` 是筛选器而非范围；仍需提供 user/organization/group 之一
- 分页使用 `count` + `page_token`；循环直到 `page_token` 不存在即为完整结果
- 组织或群组范围查询可能需要管理员权限

### 2. 管理事件邀请者

**使用场景**：用户想查看谁预订了事件或获取邀请者详情

**工具调用顺序**：
1. `CALENDLY_LIST_EVENTS` - 找到目标事件 [前置条件]
2. `CALENDLY_LIST_EVENT_INVITEES` - 列出特定事件的所有邀请者 [必需]
3. `CALENDLY_GET_EVENT_INVITEE` - 获取单个邀请者的详细信息 [可选]

**关键参数**：
- `uuid`：事件 UUID（用于 `LIST_EVENT_INVITEES`）
- `event_uuid` + `invitee_uuid`：`GET_EVENT_INVITEE` 两者都必需
- `email`：按邮箱地址筛选邀请者
- `status`：`"active"` 或 `"canceled"`
- `sort`：`"created_at:asc"` 或 `"created_at:desc"`
- `count`：每页结果数（默认 20）

**常见陷阱**：
- `CALENDLY_LIST_EVENT_INVITEES` 的 `uuid` 参数是事件 UUID，不是邀请者 UUID
- 使用 `page_token` 分页直到不存在为止，获取完整邀请者列表
- 已取消的邀请者默认不显示；使用 `status: "canceled"` 查看它们

### 3. 创建调度链接和检查可用性

**使用场景**：用户想生成预订链接或查看可用时段

**工具调用顺序**：
1. `CALENDLY_GET_CURRENT_USER` - 获取用户 URI [前置条件]
2. `CALENDLY_LIST_USER_S_EVENT_TYPES` - 列出可用事件类型 [必需]
3. `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_TIMES` - 查看某事件类型的可用时段 [可选]
4. `CALENDLY_CREATE_SCHEDULING_LINK` - 生成一次性调度链接 [必需]
5. `CALENDLY_LIST_USER_AVAILABILITY_SCHEDULES` - 查看用户的可用性日程 [可选]

**关键参数**：
- `owner`：事件类型 URI（如 `https://api.calendly.com/event_types/{uuid}`）
- `owner_type`：`"EventType"`（默认）
- `max_event_count`：一次性链接必须精确为 `1`
- `start_time` / `end_time`：可用性查询的 UTC 时间戳（最长 7 天范围）
- `active`：布尔值，筛选活跃/非活跃事件类型
- `user`：列出事件类型的用户 URI

**常见陷阱**：
- 如果 token 缺少权限或 owner URI 无效，`CALENDLY_CREATE_SCHEDULING_LINK` 可能返回 403
- `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_TIMES` 需要 UTC 时间戳且最长 7 天范围；更长的查询需拆分
- 可用时段结果不分页——一次响应返回所有结果
- 事件类型 URI 必须是完整的 API URI（如 `https://api.calendly.com/event_types/...`）

### 4. 取消事件

**使用场景**：用户想取消已安排的 Calendly 事件

**工具调用顺序**：
1. `CALENDLY_LIST_EVENTS` - 找到要取消的事件 [前置条件]
2. `CALENDLY_GET_EVENT` - 取消前确认事件详情 [前置条件]
3. `CALENDLY_LIST_EVENT_INVITEES` - 查看受影响的人员 [可选]
4. `CALENDLY_CANCEL_EVENT` - 取消事件 [必需]

**关键参数**：
- `uuid`：要取消的事件 UUID
- `reason`：可选的取消原因（可能包含在给邀请者的通知中）

**常见陷阱**：
- 取消操作不可逆——调用前务必与用户确认
- 取消可能触发通知发送给邀请者
- 只能取消活跃事件；已取消的事件会返回错误
- 执行 `CALENDLY_CANCEL_EVENT` 前必须获得用户明确确认

### 5. 管理组织和邀请

**使用场景**：用户想邀请成员、管理组织或处理组织邀请

**工具调用顺序**：
1. `CALENDLY_GET_CURRENT_USER` - 获取用户和组织上下文 [前置条件]
2. `CALENDLY_GET_ORGANIZATION` - 获取组织详情 [可选]
3. `CALENDLY_LIST_ORGANIZATION_INVITATIONS` - 查看现有邀请 [可选]
4. `CALENDLY_CREATE_ORGANIZATION_INVITATION` - 发送组织邀请 [必需]
5. `CALENDLY_REVOKE_USER_S_ORGANIZATION_INVITATION` - 撤销待处理的邀请 [可选]
6. `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` - 移除成员 [可选]

**关键参数**：
- `uuid`：组织 UUID
- `email`：要邀请的用户邮箱地址
- `status`：按 `"pending"`、`"accepted"` 或 `"declined"` 筛选邀请

**常见陷阱**：
- 只有组织所有者/管理员可以管理邀请和移除操作；其他人会收到授权错误
- 同一邮箱的重复活跃邀请会被拒绝——先检查现有邀请
- 组织所有者无法通过 `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` 移除
- 邀请状态包括 pending、accepted、declined 和 revoked——需分别处理

## 常用模式

### ID 解析
Calendly 使用完整的 API URI 作为标识符，而非简单 ID：
- **当前用户 URI**：`CALENDLY_GET_CURRENT_USER` 返回 `resource.uri`（如 `https://api.calendly.com/users/{uuid}`）
- **组织 URI**：在当前用户响应的 `resource.current_organization` 中找到
- **事件 UUID**：从事件 URI 或列表响应中提取
- **事件类型 URI**：来自 `CALENDLY_LIST_USER_S_EVENT_TYPES` 响应

重要：切勿在列表/筛选端点中使用 `"me"` 作为用户参数。始终先解析为完整 URI。

### 分页
大多数 Calendly 列表端点使用基于 token 的分页：
- 设置 `count` 指定页面大小（默认 20）
- 跟随 `pagination.next_page_token` 中的 `page_token` 直到不存在
- 使用 `字段:方向` 格式排序（如 `start_time:asc`、`created_at:desc`）

### 时间处理
- 所有时间戳必须为 UTC 格式：`yyyy-MM-ddTHH:mm:ss.ffffffZ`
- 使用 `min_start_time` / `max_start_time` 对事件进行日期范围筛选
- 可用时段查询最长 7 天范围；更长的查询需拆分为多次调用

## 已知陷阱

### URI 格式
- 所有实体引用使用完整的 Calendly API URI（如 `https://api.calendly.com/users/{uuid}`）
- 切勿在需要 URI 的地方传入裸 UUID，切勿向列表端点传入 `"me"`
- 当工具需要 UUID 参数时（如 `CALENDLY_GET_EVENT`），从 URI 中提取 UUID

### 范围要求
- `CALENDLY_LIST_EVENTS` 必须且只能指定一个范围（user、organization 或 group）——不能多也不能少
- 组织/群组范围查询可能需要管理员权限
- Token 范围决定可用操作；403 错误表示权限不足

### 数据关系
- 事件有邀请者（预订的参会者）
- 事件类型定义调度页面（时长、可用性规则）
- 组织包含用户和群组
- 调度链接绑定到事件类型，而非直接绑定到事件

### 速率限制
- Calendly API 有速率限制；避免对大数据集进行紧密循环
- 合理分页，批量操作时添加延迟

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 获取当前用户 | `CALENDLY_GET_CURRENT_USER` | (无) |
| 通过 UUID 获取用户 | `CALENDLY_GET_USER` | `uuid` |
| 列出事件 | `CALENDLY_LIST_EVENTS` | `user`, `status`, `min_start_time` |
| 获取事件详情 | `CALENDLY_GET_EVENT` | `uuid` |
| 取消事件 | `CALENDLY_CANCEL_EVENT` | `uuid`, `reason` |
| 列出邀请者 | `CALENDLY_LIST_EVENT_INVITEES` | `uuid`, `status`, `email` |
| 获取邀请者 | `CALENDLY_GET_EVENT_INVITEE` | `event_uuid`, `invitee_uuid` |
| 列出事件类型 | `CALENDLY_LIST_USER_S_EVENT_TYPES` | `user`, `active` |
| 获取事件类型 | `CALENDLY_GET_EVENT_TYPE` | `uuid` |
| 检查可用性 | `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_TIMES` | 事件类型 URI, `start_time`, `end_time` |
| 创建调度链接 | `CALENDLY_CREATE_SCHEDULING_LINK` | `owner`, `max_event_count` |
| 列出可用性日程 | `CALENDLY_LIST_USER_AVAILABILITY_SCHEDULES` | 用户 URI |
| 获取组织 | `CALENDLY_GET_ORGANIZATION` | `uuid` |
| 邀请加入组织 | `CALENDLY_CREATE_ORGANIZATION_INVITATION` | `uuid`, `email` |
| 列出组织邀请 | `CALENDLY_LIST_ORGANIZATION_INVITATIONS` | `uuid`, `status` |
| 撤销组织邀请 | `CALENDLY_REVOKE_USER_S_ORGANIZATION_INVITATION` | 组织 UUID, 邀请 UUID |
| 从组织移除 | `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` | 成员 UUID |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
