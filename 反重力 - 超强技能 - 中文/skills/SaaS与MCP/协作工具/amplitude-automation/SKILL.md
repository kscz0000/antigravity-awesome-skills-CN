---
name: amplitude-automation
description: "通过 Rube MCP (Composio) 自动化 Amplitude 任务：事件、用户活动、群组、用户识别。始终先搜索工具以获取当前架构。触发词：Amplitude自动化、事件追踪、用户活动分析、群组管理、Amplitude集成、产品分析自动化、AMPLITUDE_SEND_EVENTS、AMPLITUDE_FIND_USER、AMPLITUDE_GET_USER_ACTIVITY、AMPLITUDE_IDENTIFY、AMPLITUDE_LIST_COHORTS、AMPLITUDE_UPDATE_COHORT_MEMBERSHIP"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Amplitude 自动化

通过 Composio 的 Amplitude 工具包和 Rube MCP 自动化 Amplitude 产品分析。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 Amplitude 工具包
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具架构

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `amplitude` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Amplitude 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 发送事件

**何时使用**：用户想要追踪事件或向 Amplitude 发送事件数据

**工具序列**：
1. `AMPLITUDE_SEND_EVENTS` - 向 Amplitude 发送一个或多个事件 [必需]

**关键参数**：
- `events`：事件对象数组，每个对象包含：
  - `event_type`：事件名称（例如 'page_view'、'purchase'）
  - `user_id`：唯一用户标识符（如果没有 `device_id` 则必需）
  - `device_id`：设备标识符（如果没有 `user_id` 则必需）
  - `event_properties`：包含自定义事件属性的对象
  - `user_properties`：要设置的用户属性对象
  - `time`：事件时间戳，自纪元以来的毫秒数

**注意事项**：
- 每个事件至少需要 `user_id` 或 `device_id` 之一
- 每个事件都必须有 `event_type`；不能为空
- `time` 必须以毫秒为单位（13 位纪元时间），而不是秒
- 存在批量限制；请查看架构了解每次请求的最大事件数
- 事件异步处理；API 响应成功并不意味着数据立即可查询

### 2. 获取用户活动

**何时使用**：用户想要查看特定用户的事件历史

**工具序列**：
1. `AMPLITUDE_FIND_USER` - 通过 ID 或属性查找用户 [前置步骤]
2. `AMPLITUDE_GET_USER_ACTIVITY` - 获取用户事件流 [必需]

**关键参数**：
- `user`：Amplitude 内部用户 ID（来自 FIND_USER）
- `offset`：事件列表的分页偏移量
- `limit`：返回的最大事件数

**注意事项**：
- `user` 参数需要 Amplitude 的内部用户 ID，而不是您应用程序的 user_id
- 必须先调用 FIND_USER 将您的 user_id 解析为 Amplitude 的内部 ID
- 活动默认按时间倒序返回
- 大量活动历史需要通过 `offset` 分页

### 3. 查找和识别用户

**何时使用**：用户想要查找用户或设置用户属性

**工具序列**：
1. `AMPLITUDE_FIND_USER` - 通过各种标识符搜索用户 [必需]
2. `AMPLITUDE_IDENTIFY` - 设置或更新用户属性 [可选]

**关键参数**：
- 对于 FIND_USER：
  - `user`：搜索词（user_id、email 或 Amplitude ID）
- 对于 IDENTIFY：
  - `user_id`：您应用程序的用户标识符
  - `device_id`：设备标识符（user_id 的替代选项）
  - `user_properties`：包含 `$set`、`$unset`、`$add`、`$append` 操作的对象

**注意事项**：
- FIND_USER 在 user_id、device_id 和 Amplitude ID 中搜索
- IDENTIFY 使用特殊的属性操作（`$set`、`$unset`、`$add`、`$append`）
- `$set` 会覆盖现有值；`$setOnce` 仅在未设置时才设置
- IDENTIFY 至少需要 `user_id` 或 `device_id` 之一
- 用户属性更改最终一致；不会立即生效

### 4. 管理群组

**何时使用**：用户想要列出群组、查看群组详情或更新群组成员

**工具序列**：
1. `AMPLITUDE_LIST_COHORTS` - 列出所有已保存的群组 [必需]
2. `AMPLITUDE_GET_COHORT` - 获取群组详细信息 [可选]
3. `AMPLITUDE_UPDATE_COHORT_MEMBERSHIP` - 从群组中添加/移除用户 [可选]
4. `AMPLITUDE_CHECK_COHORT_STATUS` - 检查异步群组操作状态 [可选]

**关键参数**：
- 对于 LIST_COHORTS：无必需参数
- 对于 GET_COHORT：`cohort_id`（来自列表结果）
- 对于 UPDATE_COHORT_MEMBERSHIP：
  - `cohort_id`：目标群组 ID
  - `memberships`：包含 `add` 和/或 `remove` 用户 ID 数组的对象
- 对于 CHECK_COHORT_STATUS：更新响应中的 `request_id`

**注意事项**：
- 所有群组特定操作都需要群组 ID
- UPDATE_COHORT_MEMBERSHIP 是异步的；使用 CHECK_COHORT_STATUS 验证
- 状态检查需要更新响应中的 `request_id`
- 每次请求的成员变更数量可能有限制；大型更新请分批处理
- 只有行为群组支持 API 成员更新

### 5. 浏览事件类别

**何时使用**：用户想要发现 Amplitude 中可用的事件类型和类别

**工具序列**：
1. `AMPLITUDE_GET_EVENT_CATEGORIES` - 列出所有事件类别 [必需]

**关键参数**：
- 无必需参数；返回所有已配置的事件类别

**注意事项**：
- 类别在 Amplitude UI 中配置；API 提供只读访问
- 类别内的事件名称区分大小写
- 在发送事件之前使用这些类别验证 event_type 值

## 常见模式

### ID 解析

**应用程序 user_id -> Amplitude 内部 ID**：
```
1. 使用 user=your_user_id 调用 AMPLITUDE_FIND_USER
2. 从响应中提取 Amplitude 的内部用户 ID
3. 使用内部 ID 调用 GET_USER_ACTIVITY
```

**群组名称 -> 群组 ID**：
```
1. 调用 AMPLITUDE_LIST_COHORTS
2. 在结果中按名称查找群组
3. 提取 id 用于群组操作
```

### 用户属性操作

Amplitude IDENTIFY 支持以下属性操作：
- `$set`：设置属性值（覆盖现有值）
- `$setOnce`：仅在属性未设置时设置
- `$add`：递增数字属性
- `$append`：追加到列表属性
- `$unset`：完全移除属性

示例结构：
```json
{
  "user_properties": {
    "$set": {"plan": "premium", "company": "Acme"},
    "$add": {"login_count": 1}
  }
}
```

### 异步操作模式

对于群组成员更新：
```
1. 调用 AMPLITUDE_UPDATE_COHORT_MEMBERSHIP -> 获取 request_id
2. 使用 request_id 调用 AMPLITUDE_CHECK_COHORT_STATUS
3. 重复步骤 2 直到状态为 'complete' 或 'error'
```

## 已知注意事项

**用户 ID**：
- Amplitude 有自己的内部用户 ID，与应用程序的用户 ID 分开
- FIND_USER 将您的 ID 解析为 Amplitude 的内部 ID
- GET_USER_ACTIVITY 需要 Amplitude 的内部 ID，而不是您的 user_id

**事件时间戳**：
- 必须是自纪元以来的毫秒数（13 位）
- 秒（10 位）会被解释为非常旧的日期
- 省略时间戳则使用服务器接收时间

**速率限制**：
- 事件摄取有每个项目的吞吐量限制
- 尽可能批量处理事件以减少 API 调用
- 群组成员更新有异步处理限制

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 用户活动按时间倒序返回事件
- 群组列表可能包含已归档的群组；检查 status 字段
- 防御性解析，为可选字段提供回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 发送事件 | AMPLITUDE_SEND_EVENTS | events (数组) |
| 查找用户 | AMPLITUDE_FIND_USER | user |
| 获取用户活动 | AMPLITUDE_GET_USER_ACTIVITY | user, offset, limit |
| 识别用户 | AMPLITUDE_IDENTIFY | user_id, user_properties |
| 列出群组 | AMPLITUDE_LIST_COHORTS | (无) |
| 获取群组 | AMPLITUDE_GET_COHORT | cohort_id |
| 更新群组成员 | AMPLITUDE_UPDATE_COHORT_MEMBERSHIP | cohort_id, memberships |
| 检查群组状态 | AMPLITUDE_CHECK_COHORT_STATUS | request_id |
| 列出事件类别 | AMPLITUDE_GET_EVENT_CATEGORIES | (无) |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
