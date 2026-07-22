---
name: zoom-automation
description: "通过 Rube MCP（Composio）自动化 Zoom 会议的创建、管理、录像、网络研讨会和参会者跟踪。始终先搜索工具以获取最新的 schema。触发词：Zoom、Zoom 自动化、Zoom 会议、网络研讨会、Webinar、参会者、录像、会议调度、Rube MCP、Composio。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Zoom 自动化

通过 Composio 的 Zoom 工具包，自动化执行 Zoom 操作，包括会议调度、网络研讨会管理、云录像检索、参会者跟踪和使用报告。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与 toolkit `zoom` 建立活跃的 Zoom 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具 schema
- 大多数功能需要付费的 Zoom 账户（Pro 套餐或更高级别）

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可工作。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用 toolkit `zoom` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE 状态，请按照返回的认证链接完成 Zoom OAuth
4. 运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和调度会议

**何时使用**：用户希望创建具有特定时间、时长和设置的 Zoom 会议

**工具序列**：
1. `ZOOM_GET_USER` - 验证已认证用户并检查许可证类型 [前置条件]
2. `ZOOM_CREATE_A_MEETING` - 创建具有主题、时间、时长和设置的会议 [必需]
3. `ZOOM_GET_A_MEETING` - 检索完整的会议详情，包括 join_url [可选]
4. `ZOOM_UPDATE_A_MEETING` - 修改会议设置或重新调度 [可选]
5. `ZOOM_ADD_A_MEETING_REGISTRANT` - 为启用了注册的会议注册参会者 [可选]

**关键参数**：
- `userId`：用户级应用始终使用 `"me"`
- `topic`：会议主题
- `type`：`1`（即时）、`2`（已调度）、`3`（周期性无固定时间）、`8`（周期性固定时间）
- `start_time`：ISO 8601 格式（UTC 使用 `yyyy-MM-ddTHH:mm:ssZ`，使用 timezone 字段时使用 `yyyy-MM-ddTHH:mm:ss`）
- `timezone`：时区 ID（例如 `"America/New_York"`）
- `duration`：时长（分钟）
- `settings__auto_recording`：`"none"`、`"local"` 或 `"cloud"`
- `settings__waiting_room`：布尔值，启用等候室
- `settings__join_before_host`：布尔值（启用等候室时将被禁用）
- `settings__meeting_invitees`：包含电子邮件地址的邀请对象数组

**陷阱**：
- `start_time` 必须是未来时间；Zoom 始终以 UTC 存储和返回时间，与输入时区无关
- 如果 type `2` 未设置 `start_time`，则会成为 30 天后过期的即时会议
- 参会者的 `join_url` 和主持人的 `start_url` 来自创建响应——请持久化保存
- `start_url` 在 2 小时后过期（`custCreate` 用户为 90 天）
- 会议创建存在速率限制：100 次/天
- 设置名称使用双下划线表示嵌套（例如 `settings__host_video`）

### 2. 列出和管理会议

**何时使用**：用户希望查看即将开始、正在进行或已结束的会议

**工具序列**：
1. `ZOOM_LIST_MEETINGS` - 按类型列出会议（已调度、正在进行、即将开始、已结束）[必需]
2. `ZOOM_GET_A_MEETING` - 获取特定会议的详细信息 [可选]
3. `ZOOM_UPDATE_A_MEETING` - 修改会议详情 [可选]

**关键参数**：
- `userId`：已认证用户使用 `"me"`
- `type`：`"scheduled"`（默认）、`"live"`、`"upcoming"`、`"upcoming_meetings"`、`"previous_meetings"`
- `page_size`：每页记录数（默认 30）
- `next_page_token`：上一页响应的分页令牌
- `from` / `to`：日期范围过滤器

**陷阱**：
- `ZOOM_LIST_MEETINGS` 排除即时会议，仅显示未过期的已调度会议
- 对于已结束的会议，使用 `type: "previous_meetings"`
- 分页：始终跟随 `next_page_token` 直至为空，以获取完整结果
- 令牌过期：`next_page_token` 在 15 分钟后过期
- 会议 ID 可能超过 10 位数字；应以长整型存储，而非标准整型

### 3. 管理录像

**何时使用**：用户希望列出、检索或删除云录像

**工具序列**：
1. `ZOOM_LIST_ALL_RECORDINGS` - 列出用户在指定日期范围内的所有云录像 [必需]
2. `ZOOM_GET_MEETING_RECORDINGS` - 获取特定会议的录像 [可选]
3. `ZOOM_DELETE_MEETING_RECORDINGS` - 将录像移至回收站或永久删除 [可选]
4. `ZOOM_LIST_ARCHIVED_FILES` - 列出已归档的会议/网络研讨会文件 [可选]

**关键参数**：
- `userId`：已认证用户使用 `"me"`
- `from` / `to`：`yyyy-mm-dd` 格式的日期范围（最大 1 个月范围）
- `meetingId`：会议 ID 或 UUID，用于检索特定录像
- `action`：删除时使用 `"trash"`（可恢复）或 `"delete"`（永久）
- `include_fields`：设置为 `"download_access_token"` 以获取用于下载录像的 JWT
- `trash`：设置为 `true` 可列出回收站中的录像

**陷阱**：
- 日期范围最大为 1 个月；如果范围超出此限制，API 会自动调整 `from`
- 账户必须启用云录像功能
- 以 `/` 开头或包含 `//` 的 UUID 必须进行双重 URL 编码
- `ZOOM_DELETE_MEETING_RECORDINGS` 默认使用 `"trash"` 操作（可恢复）；`"delete"` 是永久操作
- 对于有密码保护的录像，下载 URL 需要在 Authorization 头中携带 OAuth 令牌
- 需要 Pro 套餐或更高级别

### 4. 获取会议参会者和报告

**何时使用**：用户希望查看参加已结束会议的人员或获取使用统计

**工具序列**：
1. `ZOOM_GET_PAST_MEETING_PARTICIPANTS` - 列出已结束会议的参会者 [必需]
2. `ZOOM_GET_A_MEETING` - 获取即将开始的会议的详情和注册信息 [可选]
3. `ZOOM_GET_DAILY_USAGE_REPORT` - 获取每日使用统计（会议数、参会者数、分钟数）[可选]
4. `ZOOM_GET_A_MEETING_SUMMARY` - 获取 AI 生成的会议摘要 [可选]

**关键参数**：
- `meetingId`：会议 ID（最新实例）或 UUID（特定发生）
- `page_size`：每页记录数（默认 30）
- `next_page_token`：大型参会者列表的分页令牌

**陷阱**：
- `ZOOM_GET_PAST_MEETING_PARTICIPANTS` 仅适用于付费套餐上已结束的会议
- 单独会议（无其他参会者）返回空结果
- UUID 编码：以 `/` 开头或包含 `//` 的 UUID 必须进行双重编码
- 始终使用 `next_page_token` 分页至空，以避免遗漏参会者
- `ZOOM_GET_A_MEETING_SUMMARY` 需要启用 AI Companion 的付费套餐；免费账户会收到 400 错误
- `ZOOM_GET_DAILY_USAGE_REPORT` 存在严格的速率限制；避免频繁调用

### 5. 管理网络研讨会

**何时使用**：用户希望列出网络研讨会或为网络研讨会注册参会者

**工具序列**：
1. `ZOOM_LIST_WEBINARS` - 列出已调度或即将开始的网络研讨会 [必需]
2. `ZOOM_GET_A_WEBINAR` - 获取详细的网络研讨会信息 [可选]
3. `ZOOM_ADD_A_WEBINAR_REGISTRANT` - 为网络研讨会注册参会者 [可选]

**关键参数**：
- `userId`：已认证用户使用 `"me"`
- `type`：`"scheduled"`（默认）或 `"upcoming"`
- `page_size`：每页记录数（默认 30）
- `next_page_token`：分页令牌

**陷阱**：
- 网络研讨会功能需要 Pro 套餐或更高级别，并配备 Webinar 插件
- 免费/基础账户无法使用网络研讨会工具
- 仅显示未过期的网络研讨会
- 网络研讨会必须启用注册功能，`ZOOM_ADD_A_WEBINAR_REGISTRANT` 才能工作

## 通用模式

### ID 解析
- **用户 ID**：用户级应用始终使用 `"me"` 来指代已认证用户
- **会议 ID**：数字 ID（以长整型存储）；用于最新实例
- **会议 UUID**：用于周期性会议的特定发生；如果以 `/` 开头或包含 `//` 则需进行双重编码
- **发生 ID**：与周期性会议一起使用，以定位特定发生

### 分页
大多数 Zoom 列表端点使用基于令牌的分页：
- 跟随 `next_page_token` 直至其为空或缺失
- 令牌在 15 分钟后过期
- 设置显式的 `page_size`（默认 30，不同端点有所不同）
- 不要使用 `page_number`（在许多端点上已弃用）

### 时间处理
- Zoom 在内部始终以 UTC 存储所有时间
- 提供 `timezone` 字段与 `start_time` 一起用于本地时间输入
- 使用 ISO 8601 格式：`yyyy-MM-ddTHH:mm:ssZ`（UTC）或 `yyyy-MM-ddTHH:mm:ss`（使用 timezone 字段）
- 仅日期字段使用 `yyyy-mm-dd` 格式

## 已知陷阱

### 套餐要求
- 大多数录像和参会者功能需要 Pro 套餐或更高级别
- 网络研讨会功能需要 Webinar 插件
- AI 会议摘要需要启用 AI Companion 功能
- 归档文件需要由 Zoom 支持团队启用"会议和网络研讨会归档"功能

### 速率限制
- 会议创建：100 次/天，每个会议 24 小时内 100 次更新
- `ZOOM_GET_PAST_MEETING_PARTICIPANTS`：中等限制；批处理时增加延迟
- `ZOOM_GET_DAILY_USAGE_REPORT`：严格的速率限制
- `ZOOM_GET_A_MEETING`、`ZOOM_GET_MEETING_RECORDINGS`：轻度速率限制
- `ZOOM_LIST_MEETINGS`、`ZOOM_LIST_ALL_RECORDINGS`：中等速率限制

### 参数怪癖
- 嵌套设置使用双下划线表示法（例如 `settings__waiting_room`）
- `start_url` 在 2 小时后过期；如有需要可通过 API 续期
- 当 `waiting_room` 为 `true` 时，`join_before_host` 自动被禁用
- 周期性会议字段（`recurrence__*`）仅适用于 type `3` 和 `8`
- `password` 字段最多 10 个字符，仅允许字母数字以及 `@`、`-`、`_`、`*`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 创建会议 | `ZOOM_CREATE_A_MEETING` | `userId`、`topic`、`start_time`、`type` |
| 获取会议详情 | `ZOOM_GET_A_MEETING` | `meetingId` |
| 更新会议 | `ZOOM_UPDATE_A_MEETING` | `meetingId`、待更新字段 |
| 列出会议 | `ZOOM_LIST_MEETINGS` | `userId`、`type`、`page_size` |
| 获取用户信息 | `ZOOM_GET_USER` | `userId` |
| 列出录像 | `ZOOM_LIST_ALL_RECORDINGS` | `userId`、`from`、`to` |
| 获取录像 | `ZOOM_GET_MEETING_RECORDINGS` | `meetingId` |
| 删除录像 | `ZOOM_DELETE_MEETING_RECORDINGS` | `meetingId`、`action` |
| 过去的参会者 | `ZOOM_GET_PAST_MEETING_PARTICIPANTS` | `meetingId`、`page_size` |
| 每日使用报告 | `ZOOM_GET_DAILY_USAGE_REPORT` | 日期参数 |
| 会议摘要 | `ZOOM_GET_A_MEETING_SUMMARY` | `meetingId` |
| 列出网络研讨会 | `ZOOM_LIST_WEBINARS` | `userId`、`type` |
| 获取网络研讨会 | `ZOOM_GET_A_WEBINAR` | webinar ID |
| 注册会议 | `ZOOM_ADD_A_MEETING_REGISTRANT` | `meetingId`、参会者详情 |
| 注册网络研讨会 | `ZOOM_ADD_A_WEBINAR_REGISTRANT` | webinar ID、参会者详情 |
| 列出归档文件 | `ZOOM_LIST_ARCHIVED_FILES` | `from`、`to` |

## 何时使用
此技能适用于执行上述概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时，才使用此技能。
- 请勿将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
