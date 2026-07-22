---
name: outlook-calendar-automation
description: "通过 Rube MCP (Composio) 自动化 Outlook 日历任务：创建事件、管理参与者、查找会议时间、处理邀请。始终先搜索工具获取当前 schema。当用户要求'自动化 Outlook 日历任务'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Outlook 日历自动化

通过 Composio 的 Outlook 工具包，经 Rube MCP 自动化 Outlook 日历操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `outlook` 建立活跃的 Outlook 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应以验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `outlook`
3. 若连接状态非 ACTIVE，按返回的认证链接完成 Microsoft OAuth
4. 运行任何工作流前确认连接状态为 ACTIVE

## 核心工作流

### 1. 创建日历事件

**使用场景**：用户想在 Outlook 日历上安排新事件

**工具调用顺序**：
1. `OUTLOOK_LIST_CALENDARS` - 列出可用日历 [可选]
2. `OUTLOOK_CALENDAR_CREATE_EVENT` - 创建事件 [必需]

**关键参数**：
- `subject`：事件标题
- `start_datetime`：ISO 8601 开始时间（如 '2025-01-03T10:00:00'）
- `end_datetime`：ISO 8601 结束时间（必须晚于开始时间）
- `time_zone`：IANA 或 Windows 时区（如 'America/New_York', 'Pacific Standard Time'）
- `attendees_info`：邮件字符串或参与者对象数组
- `body`：事件描述（纯文本或 HTML）
- `is_html`：正文包含 HTML 时设为 true
- `location`：实体地点字符串
- `is_online_meeting`：需要 Teams 会议链接时设为 true
- `online_meeting_provider`：Teams 集成用 'teamsForBusiness'
- `show_as`：'free', 'tentative', 'busy', 'oof'

**注意事项**：
- start_datetime 必须在时间顺序上早于 end_datetime
- time_zone 为必填项，必须是有效的 IANA 或 Windows 时区名称
- 添加参与者可能立即触发邀请邮件
- 生成 Teams 会议链接需要同时设置 is_online_meeting=true 和 online_meeting_provider='teamsForBusiness'
- user_id 默认为 'me'；访问其他用户日历请用邮箱或 UUID

### 2. 列出和搜索事件

**使用场景**：用户想查找日历上的事件

**工具调用顺序**：
1. `OUTLOOK_GET_MAILBOX_SETTINGS` - 获取用户时区以确保查询准确 [前置条件]
2. `OUTLOOK_LIST_EVENTS` - 使用筛选器搜索事件 [必需]
3. `OUTLOOK_GET_EVENT` - 获取特定事件的完整详情 [可选]
4. `OUTLOOK_GET_CALENDAR_VIEW` - 获取在时间窗口内活跃的事件 [替代方案]

**关键参数**：
- `filter`：OData 筛选器字符串（如 "start/dateTime ge '2024-07-01T00:00:00Z'"）
- `select`：要返回的属性数组
- `orderby`：排序条件（如 ['start/dateTime desc']）
- `top`：每页结果数（1-999）
- `timezone`：结果的显示时区
- `start_datetime`/`end_datetime`：用于 CALENDAR_VIEW 时间窗口（UTC 带 Z 后缀）

**注意事项**：
- OData 筛选器的日期时间值需要单引号和 Z 后缀
- 使用 'start/dateTime' 筛选事件开始时间，不要用 'receivedDateTime'（那是邮件用的）
- 'createdDateTime' 支持 orderby/select 但不支持筛选
- 分页：跟随 @odata.nextLink 直到收集完所有页面
- CALENDAR_VIEW 更适合"今天日历上有什么"的查询（包含跨时段事件）
- LIST_EVENTS 更适合关键词/类别筛选
- 响应事件的 start/end 嵌套为 start.dateTime 和 end.dateTime

### 3. 更新事件

**使用场景**：用户想修改现有日历事件

**工具调用顺序**：
1. `OUTLOOK_LIST_EVENTS` - 查找要更新的事件 [前置条件]
2. `OUTLOOK_UPDATE_CALENDAR_EVENT` - 更新事件 [必需]

**关键参数**：
- `event_id`：事件唯一标识符（来自 LIST_EVENTS）
- `subject`：新事件标题（可选）
- `start_datetime`/`end_datetime`：新时间（可选）
- `time_zone`：新时间的时区
- `attendees`：更新后的参与者列表（提供则替换现有列表）
- `body`：更新的描述，含 contentType 和 content
- `location`：更新的地点

**注意事项**：
- UPDATE 会将提供的字段与现有事件合并；未指定的字段保持不变
- 提供 participants 会替换整个参与者列表；需包含所有期望的参与者
- 提供 categories 会替换整个类别列表
- 更新时间可能触发向参与者重新发送通知
- event_id 为必填项；先从 LIST_EVENTS 获取

### 4. 删除事件和拒绝邀请

**使用场景**：用户想删除事件或拒绝会议邀请

**工具调用顺序**：
1. `OUTLOOK_DELETE_EVENT` - 删除事件 [可选]
2. `OUTLOOK_DECLINE_EVENT` - 拒绝会议邀请 [可选]

**关键参数**：
- `event_id`：要删除或拒绝的事件
- `send_notifications`：向参与者发送取消通知（默认 true）
- `comment`：拒绝原因（用于 DECLINE_EVENT）
- `proposedNewTime`：拒绝时建议替代时间

**注意事项**：
- send_notifications=true 时删除会发送取消邮件
- 拒绝时支持提议新时间，start/end 使用 ISO 8601 格式
- 删除循环事件的主事件会删除所有实例
- DECLINE_EVENT 中的 sendResponse 控制是否通知组织者

### 5. 查找可用会议时间

**使用场景**：用户想在多人之间找到最佳会议时段

**工具调用顺序**：
1. `OUTLOOK_FIND_MEETING_TIMES` - 获取会议时间建议 [必需]
2. `OUTLOOK_GET_SCHEDULE` - 查询特定人员的忙闲状态 [替代方案]

**关键参数**：
- `attendees`：参与者对象数组，含 email 和 type
- `meetingDuration`：ISO 8601 时长（如 'PT1H' 表示 1 小时，'PT30M' 表示 30 分钟）
- `timeConstraint`：搜索的时间段
- `minimumAttendeePercentage`：最低置信度阈值（0-100）
- `Schedules`：GET_SCHEDULE 用的邮箱数组
- `StartTime`/`EndTime`：排程查询的时间窗口（最多 62 天）

**注意事项**：
- FIND_MEETING_TIMES 默认在工作时间内搜索；用 activityDomain='unrestricted' 搜索全天候时段
- 时间约束的时间段需要 dateTime 和 timeZone 的起止值
- GET_SCHEDULE 的查询周期不能超过 62 天
- 会议建议会考虑参与者可用性，但对复杂人员组合可能返回次优时间

## 常用模式

### 事件 ID 解析

```
1. Call OUTLOOK_LIST_EVENTS with time-bound filter
2. Find target event by subject or other criteria
3. Extract event id (e.g., 'AAMkAGI2TAAA=')
4. Use in UPDATE, DELETE, or GET_EVENT calls
```

### 日历 OData 筛选器语法

**时间范围筛选**：
```
filter: "start/dateTime ge '2024-07-01T00:00:00Z' and start/dateTime le '2024-07-31T23:59:59Z'"
```

**主题包含**：
```
filter: "contains(subject, 'Project Review')"
```

**组合筛选**：
```
filter: "contains(subject, 'Review') and categories/any(c:c eq 'Work')"
```

### 时区处理

- 获取用户时区：`OUTLOOK_GET_MAILBOX_SETTINGS` 配合 select=['timeZone']
- 在筛选器日期时间值中使用一致的时区
- Calendar View 需要带 Z 后缀的 UTC 时间戳
- LIST_EVENTS 筛选器接受带时区的日期时间值

### 创建在线会议

```
1. Set is_online_meeting: true
2. Set online_meeting_provider: 'teamsForBusiness'
3. Create event with OUTLOOK_CALENDAR_CREATE_EVENT
4. Teams join link available in response onlineMeeting field
5. Or retrieve via OUTLOOK_GET_EVENT for the full join URL
```

## 已知注意事项

**日期时间格式**：
- 需要 ISO 8601 格式：'2025-01-03T10:00:00'
- Calendar View 需要带 Z 的 UTC：'2025-01-03T10:00:00Z'
- 筛选器值需要单引号："'2025-01-03T00:00:00Z'"
- 时区不匹配会导致事件时间偏移；始终先解析用户时区

**OData 筛选器错误**：
- 400 Bad Request 通常表示筛选器语法问题
- 并非所有事件属性都支持筛选（createdDateTime 不支持）
- 遇到 400 错误时调整语法/边界后重试
- 有效的筛选字段：start/dateTime, end/dateTime, subject, categories, isAllDay

**参与者管理**：
- 添加参与者会触发邀请邮件
- 更新参与者会替换完整列表；需包含所有期望的参与者
- 参与者类型：'required', 'optional', 'resource'
- 日历委托影响可访问的日历范围

**响应结构**：
- 事件嵌套在 response.data.value
- 事件时间在 event.start.dateTime 和 event.end.dateTime
- Calendar View 可能嵌套在 data.results[i].response.data.value
- 使用防御性解析，对不同嵌套层级做回退处理

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 创建事件 | OUTLOOK_CALENDAR_CREATE_EVENT | subject, start_datetime, end_datetime, time_zone |
| 列出事件 | OUTLOOK_LIST_EVENTS | filter, select, top, timezone |
| 获取事件详情 | OUTLOOK_GET_EVENT | event_id |
| 日历视图 | OUTLOOK_GET_CALENDAR_VIEW | start_datetime, end_datetime |
| 更新事件 | OUTLOOK_UPDATE_CALENDAR_EVENT | event_id, subject, start_datetime |
| 删除事件 | OUTLOOK_DELETE_EVENT | event_id, send_notifications |
| 拒绝事件 | OUTLOOK_DECLINE_EVENT | event_id, comment |
| 查找会议时间 | OUTLOOK_FIND_MEETING_TIMES | attendees, meetingDuration |
| 获取排程 | OUTLOOK_GET_SCHEDULE | Schedules, StartTime, EndTime |
| 列出日历 | OUTLOOK_LIST_CALENDARS | user_id |
| 邮箱设置 | OUTLOOK_GET_MAILBOX_SETTINGS | select |

## 使用场景
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。
