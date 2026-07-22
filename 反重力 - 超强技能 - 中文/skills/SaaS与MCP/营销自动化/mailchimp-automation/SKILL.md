---
name: mailchimp-automation
description: "通过 Rube MCP (Composio) 自动化 Mailchimp 邮件营销，包括营销活动、受众、订阅者、细分和数据分析。触发词：Mailchimp自动化、邮件营销自动化、Mailchimp活动、受众管理、订阅者管理、邮件营销分析、Mailchimp MCP、Composio Mailchimp"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Mailchimp 自动化

通过 Composio 的 Mailchimp 工具包，自动化 Mailchimp 邮件营销工作流，包括营销活动的创建与发送、受众/列表管理、订阅者操作、细分以及效果分析。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定工具包 `mailchimp` 建立活跃的 Mailchimp 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定工具包 `mailchimp`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Mailchimp OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和发送邮件营销活动

**适用场景**：用户想要创建、配置、测试并发送邮件营销活动。

**工具调用顺序**：
1. `MAILCHIMP_GET_LISTS_INFO` - 列出可用受众并获取 list_id [前提]
2. `MAILCHIMP_ADD_CAMPAIGN` - 创建新营销活动，指定类型、受众、主题、发件人名称 [必需]
3. `MAILCHIMP_SET_CAMPAIGN_CONTENT` - 设置营销活动的 HTML 内容 [必需]
4. `MAILCHIMP_SEND_TEST_EMAIL` - 在正式发送前发送预览给审核人 [可选]
5. `MAILCHIMP_SEND_CAMPAIGN` - 立即发送营销活动 [必需]
6. `MAILCHIMP_SCHEDULE_CAMPAIGN` - 安排未来发送而非立即发送 [可选]

**MAILCHIMP_ADD_CAMPAIGN 关键参数**：
- `type`: "regular"、"plaintext"、"rss" 或 "variate"（必需）
- `recipients__list__id`: 收件人的受众/列表 ID
- `settings__subject__line`: 邮件主题行
- `settings__from__name`: 发件人显示名称
- `settings__reply__to`: 回复邮箱地址（发送时必需）
- `settings__title`: 内部营销活动标题
- `settings__preview__text`: 收件箱中显示的预览文本

**MAILCHIMP_SET_CAMPAIGN_CONTENT 关键参数**：
- `campaign_id`: 创建步骤返回的营销活动 ID（必需）
- `html`: 邮件的原始 HTML 内容
- `plain_text`: 纯文本版本（省略时自动生成）
- `template__id`: 使用预构建模板替代原始 HTML

**注意事项**：
- `MAILCHIMP_SEND_CAMPAIGN` 不可撤销；务必先发送测试邮件并获得用户明确批准
- 营销活动必须处于"save"（草稿）状态，且具有有效的受众、主题、发件人名称、已验证邮箱和内容后才能发送
- `MAILCHIMP_SCHEDULE_CAMPAIGN` 需要有效的未来日期时间；过去的时间戳会失败
- 模板和 HTML 内容必须包含合规的页脚/退订合并标签
- Mailchimp 使用双下划线表示法表示嵌套参数（如 `settings__subject__line`）

### 2. 管理受众和订阅者

**适用场景**：用户想要查看受众、列出订阅者或查看订阅者详情。

**工具调用顺序**：
1. `MAILCHIMP_GET_LISTS_INFO` - 列出所有受众及其成员数量 [必需]
2. `MAILCHIMP_GET_LIST_INFO` - 获取特定受众的详情 [可选]
3. `MAILCHIMP_LIST_MEMBERS_INFO` - 列出成员，支持状态筛选和分页 [必需]
4. `MAILCHIMP_SEARCH_MEMBERS` - 跨列表按邮箱或姓名搜索 [可选]
5. `MAILCHIMP_GET_MEMBER_INFO` - 获取特定订阅者的详细资料 [可选]
6. `MAILCHIMP_LIST_SEGMENTS` - 列出受众内的细分 [可选]

**MAILCHIMP_LIST_MEMBERS_INFO 关键参数**：
- `list_id`: 受众 ID（必需）
- `status`: "subscribed"、"unsubscribed"、"cleaned"、"pending"、"transactional"、"archived"
- `count`: 每页记录数（默认 10，最大 1000）
- `offset`: 分页偏移量（默认 0）
- `sort_field`: "timestamp_opt"、"timestamp_signup" 或 "last_changed"
- `fields`: 逗号分隔的字段列表，用于限制响应大小

**注意事项**：
- `stats.avg_open_rate` 和 `stats.avg_click_rate` 是 0-1 的小数，不是 0-100 的百分比
- 始终使用 `status="subscribed"` 筛选活跃订阅者；省略则返回所有状态
- 必须使用 `count` 和 `offset` 分页，直到已收集成员数等于 `total_items`
- 大型列表响应可能被截断；数据位于 `response.data.members` 下

### 3. 添加和更新订阅者

**适用场景**：用户想要添加新订阅者、更新现有订阅者或批量管理列表成员。

**工具调用顺序**：
1. `MAILCHIMP_GET_LIST_INFO` - 验证目标受众存在 [前提]
2. `MAILCHIMP_SEARCH_MEMBERS` - 检查联系人是否已存在 [可选]
3. `MAILCHIMP_ADD_OR_UPDATE_LIST_MEMBER` - 更新插入订阅者（创建或更新）[必需]
4. `MAILCHIMP_ADD_MEMBER_TO_LIST` - 添加新订阅者（仅创建）[可选]
5. `MAILCHIMP_BATCH_ADD_OR_REMOVE_MEMBERS` - 批量管理细分成员 [可选]

**MAILCHIMP_ADD_OR_UPDATE_LIST_MEMBER 关键参数**：
- `list_id`: 受众 ID（必需）
- `subscriber_hash`: 小写邮箱的 MD5 哈希（必需）
- `email_address`: 订阅者邮箱（必需）
- `status_if_new`: 新订阅者的状态："subscribed"、"pending" 等（必需）
- `status`: 现有订阅者的状态
- `merge_fields`: 包含合并标签键的对象（如 `{"FNAME": "John", "LNAME": "Doe"}`）
- `tags`: 标签字符串数组

**MAILCHIMP_ADD_MEMBER_TO_LIST 关键参数**：
- `list_id`: 受众 ID（必需）
- `email_address`: 订阅者邮箱（必需）
- `status`: "subscribed"、"pending"、"unsubscribed"、"cleaned"、"transactional"（必需）

**注意事项**：
- `subscriber_hash` 必须是**小写**邮箱的 MD5 哈希；大小写错误会导致 404 或重复记录
- 使用 `MAILCHIMP_ADD_OR_UPDATE_LIST_MEMBER`（upsert）而非 `MAILCHIMP_ADD_MEMBER_TO_LIST` 以避免重复错误
- `status_if_new` 仅决定新联系人的状态；现有联系人使用 `status`
- 使用 `skip_merge_validation: true` 跳过必填合并字段验证
- `MAILCHIMP_BATCH_ADD_OR_REMOVE_MEMBERS` 管理的是静态细分成员，而非列表成员

### 4. 查看营销活动报告和分析

**适用场景**：用户想要查看营销活动效果、打开率、点击率或订阅者互动情况。

**工具调用顺序**：
1. `MAILCHIMP_LIST_CAMPAIGNS` - 列出已发送的营销活动及报告摘要 [必需]
2. `MAILCHIMP_SEARCH_CAMPAIGNS` - 按名称、主题或内容查找营销活动 [可选]
3. `MAILCHIMP_GET_CAMPAIGN_REPORT` - 获取营销活动的详细效果报告 [必需]
4. `MAILCHIMP_LIST_CAMPAIGN_REPORTS` - 批量获取多个营销活动的报告 [可选]
5. `MAILCHIMP_LIST_CAMPAIGN_DETAILS` - 获取链接级别的点击统计 [可选]
6. `MAILCHIMP_GET_CAMPAIGN_LINK_DETAILS` - 深入查看特定链接的点击数据 [可选]
7. `MAILCHIMP_LIST_CLICKED_LINK_SUBSCRIBERS` - 查看谁点击了特定链接 [可选]
8. `MAILCHIMP_GET_SUBSCRIBER_EMAIL_ACTIVITY` - 获取每个订阅者的营销活动活动 [可选]
9. `MAILCHIMP_GET_CAMPAIGN_CONTENT` - 获取营销活动 HTML 内容 [可选]

**MAILCHIMP_LIST_CAMPAIGNS 关键参数**：
- `status`: "save"、"paused"、"schedule"、"sending"、"sent"
- `count` / `offset`: 分页（默认 10，最大 1000）
- `since_send_time` / `before_send_time`: ISO 8601 日期范围筛选
- `sort_field`: "create_time" 或 "send_time"
- `fields`: 限制响应字段以提升性能

**MAILCHIMP_GET_CAMPAIGN_REPORT 关键参数**：
- `campaign_id`: 营销活动 ID（必需）
- 返回：打开、点击、退回、退订、时间序列、行业统计

**注意事项**：
- `MAILCHIMP_LIST_CAMPAIGNS` 仅返回高层级的 `report_summary`；使用 `MAILCHIMP_GET_CAMPAIGN_REPORT` 获取详细指标
- 草稿/未发送的营销活动缺少有意义的报告数据
- 在 LIST_CAMPAIGNS 上使用 `fields` 参数时，需显式请求 `send_time` 和 `report_summary` 子字段
- 分页默认值较低（10 条记录）；使用 `count` 和 `offset` 迭代直到覆盖 `total_items`
- `send_time` 为带时区的 ISO 8601 格式；需谨慎解析

## 常用模式

### ID 解析
操作前始终将名称解析为 ID：
- **受众名称 -> list_id**：`MAILCHIMP_GET_LISTS_INFO` 并按名称匹配
- **订阅者邮箱 -> subscriber_hash**：在代码中计算小写邮箱的 MD5
- **营销活动名称 -> campaign_id**：使用查询条件调用 `MAILCHIMP_SEARCH_CAMPAIGNS`
- **细分名称 -> segment_id**：使用 list_id 调用 `MAILCHIMP_LIST_SEGMENTS`

### 分页
Mailchimp 使用基于偏移量的分页：
- 使用 `count`（每页大小，最大 1000）和 `offset`（跳过 N 条记录）
- 持续迭代直到已收集记录数等于响应中的 `total_items`
- 默认 `count` 为 10；批量操作时务必显式设置
- 搜索端点最多 10 页（每页 30 条，共 300 条结果）

### 订阅者哈希
许多端点需要 `subscriber_hash`（小写邮箱的 MD5）：
```
import hashlib
subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
```

## 已知注意事项

### ID 格式
- `list_id`（受众 ID）是短字母数字字符串（如 "abc123def4"）
- `campaign_id` 是字母数字字符串
- `subscriber_hash` 是 MD5 十六进制字符串（32 个字符）
- 细分 ID 是整数

### 速率限制
- Mailchimp 强制执行 API 速率限制；批量订阅者操作请使用批处理
- 高频调用 GET_MEMBER_INFO 和 ADD_OR_UPDATE_LIST_MEMBER 可能触发限流
- 批量细分操作请使用 `MAILCHIMP_BATCH_ADD_OR_REMOVE_MEMBERS`

### 参数特性
- 嵌套参数使用双下划线表示法：`settings__subject__line`、`recipients__list__id`
- `avg_open_rate` 和 `avg_click_rate` 是 0-1 的小数，不是百分比
- `status_if_new` 仅在 upsert 操作中适用于新联系人
- `subscriber_hash` 必须是小写邮箱的 MD5；错误的大小写会创建幽灵记录
- 营销活动 `type` 在创建时必需；最常用的是 "regular"
- `MAILCHIMP_SEND_CAMPAIGN` 成功时返回 HTTP 204（无响应体）

### 内容与合规
- 营销活动 HTML 必须包含退订链接和物理地址（合并标签）
- 发送前必须通过 `MAILCHIMP_SET_CAMPAIGN_CONTENT` 设置内容
- 测试邮件要求营销活动已设置内容

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出受众 | `MAILCHIMP_GET_LISTS_INFO` | `count`、`offset` |
| 获取受众详情 | `MAILCHIMP_GET_LIST_INFO` | `list_id` |
| 创建营销活动 | `MAILCHIMP_ADD_CAMPAIGN` | `type`、`recipients__list__id`、`settings__subject__line` |
| 设置营销活动内容 | `MAILCHIMP_SET_CAMPAIGN_CONTENT` | `campaign_id`、`html` |
| 发送测试邮件 | `MAILCHIMP_SEND_TEST_EMAIL` | `campaign_id`、`test_emails` |
| 发送营销活动 | `MAILCHIMP_SEND_CAMPAIGN` | `campaign_id` |
| 安排营销活动 | `MAILCHIMP_SCHEDULE_CAMPAIGN` | `campaign_id`、`schedule_time` |
| 获取营销活动信息 | `MAILCHIMP_GET_CAMPAIGN_INFO` | `campaign_id` |
| 搜索营销活动 | `MAILCHIMP_SEARCH_CAMPAIGNS` | `query` |
| 列出营销活动 | `MAILCHIMP_LIST_CAMPAIGNS` | `status`、`count`、`offset` |
| 复制营销活动 | `MAILCHIMP_REPLICATE_CAMPAIGN` | `campaign_id` |
| 列出订阅者 | `MAILCHIMP_LIST_MEMBERS_INFO` | `list_id`、`status`、`count`、`offset` |
| 搜索成员 | `MAILCHIMP_SEARCH_MEMBERS` | `query`、`list_id` |
| 获取成员信息 | `MAILCHIMP_GET_MEMBER_INFO` | `list_id`、`subscriber_hash` |
| 添加订阅者 | `MAILCHIMP_ADD_MEMBER_TO_LIST` | `list_id`、`email_address`、`status` |
| 更新插入订阅者 | `MAILCHIMP_ADD_OR_UPDATE_LIST_MEMBER` | `list_id`、`subscriber_hash`、`email_address`、`status_if_new` |
| 批量管理成员 | `MAILCHIMP_BATCH_ADD_OR_REMOVE_MEMBERS` | `list_id`、`segment_id` |
| 列出细分 | `MAILCHIMP_LIST_SEGMENTS` | `list_id` |
| 营销活动报告 | `MAILCHIMP_GET_CAMPAIGN_REPORT` | `campaign_id` |
| 所有报告 | `MAILCHIMP_LIST_CAMPAIGN_REPORTS` | `count`、`offset` |
| 链接点击详情 | `MAILCHIMP_LIST_CAMPAIGN_DETAILS` | `campaign_id`、`count` |
| 订阅者活动 | `MAILCHIMP_GET_SUBSCRIBER_EMAIL_ACTIVITY` | `campaign_id`、`subscriber_hash` |
| 成员近期活动 | `MAILCHIMP_VIEW_RECENT_ACTIVITY` | `list_id`、`subscriber_hash` |
| 营销活动内容 | `MAILCHIMP_GET_CAMPAIGN_CONTENT` | `campaign_id` |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出替代环境特定的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
