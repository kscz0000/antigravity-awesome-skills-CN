---
name: outlook-automation
description: "通过 Rube MCP (Composio) 自动化 Outlook 任务：邮件、日历、联系人、文件夹、附件。始终先搜索工具获取当前 schema。当用户要求'自动化 Outlook 任务'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Outlook 自动化

通过 Composio 的 Outlook 工具包，经 Rube MCP 自动化 Microsoft Outlook 操作。

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

### 1. 搜索和筛选邮件

**使用场景**：用户想在邮箱中查找特定邮件

**工具调用顺序**：
1. `OUTLOOK_SEARCH_MESSAGES` - 使用 KQL 语法跨所有文件夹搜索 [必需]
2. `OUTLOOK_GET_MESSAGE` - 获取完整邮件详情 [可选]
3. `OUTLOOK_LIST_OUTLOOK_ATTACHMENTS` - 列出邮件附件 [可选]
4. `OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT` - 下载附件 [可选]

**关键参数**：
- `query`：KQL 搜索字符串（from:, to:, subject:, received:, hasattachment:）
- `from_index`：分页起始位置（从 0 开始）
- `size`：每页结果数（最多 25）
- `message_id`：邮件 ID（使用搜索结果中的 hitId）

**注意事项**：
- 仅支持 Microsoft 365/企业账户（不支持 @hotmail.com/@outlook.com）
- 分页依赖 hitsContainers[0].moreResultsAvailable；仅当为 false 时停止
- 使用搜索结果中的 hitId 作为下游调用的 message_id，而非 resource.id
- 索引延迟：最新邮件可能不会立即出现
- 内联图片会显示为附件；通过 mimetype 筛选真实文档

### 2. 查询文件夹中的邮件

**使用场景**：用户想用 OData 筛选器列出特定文件夹中的邮件

**工具调用顺序**：
1. `OUTLOOK_LIST_MAIL_FOLDERS` - 列出邮件文件夹获取文件夹 ID [前置条件]
2. `OUTLOOK_QUERY_EMAILS` - 使用结构化筛选器查询邮件 [必需]

**关键参数**：
- `folder`：文件夹名称（'inbox', 'sentitems', 'drafts'）或文件夹 ID
- `filter`：OData 筛选器（如 `isRead eq false and importance eq 'high'`）
- `top`：最大结果数（1-1000）
- `orderby`：排序字段和方向
- `select`：要返回的字段数组

**注意事项**：
- QUERY_EMAILS 仅搜索单个文件夹；跨文件夹搜索请用 SEARCH_MESSAGES
- 自定义文件夹需要文件夹 ID，而非显示名称；请用 LIST_MAIL_FOLDERS
- 始终检查 response['@odata.nextLink'] 进行分页
- 无法按收件人或正文内容筛选；请用 SEARCH_MESSAGES

### 3. 管理日历事件

**使用场景**：用户想列出、搜索或查看日历事件

**工具调用顺序**：
1. `OUTLOOK_LIST_EVENTS` - 使用筛选器列出事件 [可选]
2. `OUTLOOK_GET_CALENDAR_VIEW` - 获取时间窗口内的事件 [可选]
3. `OUTLOOK_GET_EVENT` - 获取特定事件详情 [可选]
4. `OUTLOOK_LIST_CALENDARS` - 列出可用日历 [可选]
5. `OUTLOOK_GET_SCHEDULE` - 获取忙闲信息 [可选]

**关键参数**：
- `filter`：OData 筛选器（使用 start/dateTime，不要用 receivedDateTime）
- `start_datetime`/`end_datetime`：ISO 8601 格式，用于日历视图
- `timezone`：IANA 时区（如 'America/New_York'）
- `calendar_id`：可选的非主日历 ID
- `select`：要返回的字段

**注意事项**：
- 仅使用日历事件属性（start/dateTime, end/dateTime），不要用邮件属性（receivedDateTime）
- 日历视图需要 start_datetime 和 end_datetime
- 循环事件需要 `expand_recurring_events=true` 才能查看各个实例
- 拒绝状态通过 attendees[].status.response 按参与者分别设置

### 4. 管理联系人

**使用场景**：用户想列出、创建或整理联系人

**工具调用顺序**：
1. `OUTLOOK_LIST_CONTACTS` - 列出联系人 [可选]
2. `OUTLOOK_CREATE_CONTACT` - 创建新联系人 [可选]
3. `OUTLOOK_GET_CONTACT_FOLDERS` - 列出联系人文件夹 [可选]
4. `OUTLOOK_CREATE_CONTACT_FOLDER` - 创建联系人文件夹 [可选]

**关键参数**：
- `givenName`/`surname`：联系人姓名
- `emailAddresses`：邮件对象数组
- `displayName`：完整显示名称
- `contact_folder_id`：可选的联系人文件夹

**注意事项**：
- 创建联系人支持多个字段，但只需 givenName 或 surname 即可

### 5. 管理邮件文件夹

**使用场景**：用户想整理邮件文件夹

**工具调用顺序**：
1. `OUTLOOK_LIST_MAIL_FOLDERS` - 列出顶层文件夹 [必需]
2. `OUTLOOK_LIST_CHILD_MAIL_FOLDERS` - 列出子文件夹 [可选]
3. `OUTLOOK_CREATE_MAIL_FOLDER` - 创建新文件夹 [可选]

**关键参数**：
- `parent_folder_id`：已知名称或文件夹 ID
- `displayName`：新文件夹名称
- `include_hidden_folders`：显示隐藏文件夹

**注意事项**：
- 已知文件夹名称：'inbox', 'sentitems', 'drafts', 'deleteditems', 'junkemail', 'archive'
- 自定义文件夹操作需要文件夹 ID，而非显示名称

## 常用模式

### KQL 搜索语法

**属性筛选**：
- `from:user@example.com` - 发件人
- `to:recipient@example.com` - 收件人
- `subject:invoice` - 主题包含
- `received>=2025-01-01` - 日期筛选
- `hasattachment:yes` - 有附件

**组合条件**：
- `AND` - 两个条件都满足
- `OR` - 满足任一条件
- 括号用于分组

### OData 筛选器语法

**邮件筛选**：
- `isRead eq false` - 未读邮件
- `importance eq 'high'` - 高重要性
- `hasAttachments eq true` - 有附件
- `receivedDateTime ge 2025-01-01T00:00:00Z` - 日期筛选

**日历筛选**：
- `start/dateTime ge '2025-01-01T00:00:00Z'` - 该日期之后的事件
- `contains(subject, 'Meeting')` - 主题包含文本

## 已知注意事项

**账户类型**：
- SEARCH_MESSAGES 需要 Microsoft 365/企业账户
- 个人账户（@hotmail.com, @outlook.com）API 访问受限

**字段混淆**：
- 邮件属性（receivedDateTime）与日历属性（start/dateTime）不同
- 不要在日历查询中使用邮件字段，反之亦然

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 搜索邮件 | OUTLOOK_SEARCH_MESSAGES | query, from_index, size |
| 查询文件夹 | OUTLOOK_QUERY_EMAILS | folder, filter, top |
| 获取邮件 | OUTLOOK_GET_MESSAGE | message_id |
| 列出附件 | OUTLOOK_LIST_OUTLOOK_ATTACHMENTS | message_id |
| 下载附件 | OUTLOOK_DOWNLOAD_OUTLOOK_ATTACHMENT | message_id, attachment_id |
| 列出文件夹 | OUTLOOK_LIST_MAIL_FOLDERS | (无) |
| 子文件夹 | OUTLOOK_LIST_CHILD_MAIL_FOLDERS | parent_folder_id |
| 列出事件 | OUTLOOK_LIST_EVENTS | filter, timezone |
| 日历视图 | OUTLOOK_GET_CALENDAR_VIEW | start_datetime, end_datetime |
| 获取事件 | OUTLOOK_GET_EVENT | event_id |
| 列出日历 | OUTLOOK_LIST_CALENDARS | (无) |
| 忙闲查询 | OUTLOOK_GET_SCHEDULE | schedules, times |
| 列出联系人 | OUTLOOK_LIST_CONTACTS | top, filter |
| 创建联系人 | OUTLOOK_CREATE_CONTACT | givenName, emailAddresses |
| 联系人文件夹 | OUTLOOK_GET_CONTACT_FOLDERS | (无) |

## 使用场景
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。
