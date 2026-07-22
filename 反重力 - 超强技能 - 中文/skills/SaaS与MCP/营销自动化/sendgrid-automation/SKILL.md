---
name: sendgrid-automation
description: 通过 Composio 的 SendGrid 工具包自动化 SendGrid 邮件投递工作流，包括营销活动（Single Sends）、联系人和列表管理、发件人身份设置以及邮件分析。触发词：SendGrid自动化、邮件营销、邮件投递、联系人管理、邮件分析、SendGrid工作流
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 SendGrid 自动化

通过 Composio 的 SendGrid 工具包自动化 SendGrid 邮件投递工作流，包括营销活动（Single Sends）、联系人和列表管理、发件人身份设置以及邮件分析。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 SendGrid 连接，工具包为 `sendgrid`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加端点即可工作。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用工具包 `sendgrid` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，请按照返回的认证链接完成 SendGrid API 密钥认证
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和发送营销活动（Single Sends）

**适用场景**：用户想要创建并向联系人列表或细分群体发送营销邮件活动。

**工具调用顺序**：
1. `SENDGRID_RETRIEVE_ALL_LISTS` - 列出可用的营销列表以选择目标 [前置条件]
2. `SENDGRID_CREATE_A_LIST` - 如需要则创建新列表 [可选]
3. `SENDGRID_ADD_OR_UPDATE_A_CONTACT` - 将联系人添加到列表 [可选]
4. `SENDGRID_GET_ALL_SENDER_IDENTITIES` - 获取已验证的发件人 ID [前置条件]
5. `SENDGRID_CREATE_SINGLE_SEND` - 创建活动，包含内容、发件人和收件人 [必需]

**SENDGRID_CREATE_SINGLE_SEND 的关键参数**：
- `name`：活动名称（必需）
- `email__config__subject`：邮件主题行
- `email__config__html__content`：HTML 正文内容
- `email__config__plain__content`：纯文本版本
- `email__config__sender__id`：已验证的发件人身份 ID
- `email__config__design__id`：替代 html_content，使用预构建设计
- `send__to__list__ids`：要发送到的列表 UUID 数组
- `send__to__segment__ids`：细分群体 UUID 数组
- `send__to__all`：设为 true 发送给所有联系人
- `email__config__suppression__group__id` 或 `email__config__custom__unsubscribe__url`：合规要求二选一

**注意事项**：
- 在 CREATE 上设置 `send_at` 不会调度发送；它只是预填 UI 日期；需要单独使用 Schedule 端点
- `send_at: "now"` 仅对 Schedule 端点有效，CREATE 不支持
- 必须提供 `suppression_group_id` 或 `custom_unsubscribe_url` 以满足退订合规要求
- 发件人使用前必须先验证；通过 `SENDGRID_GET_ALL_SENDER_IDENTITIES` 检查
- 嵌套参数使用双下划线表示法（例如 `email__config__subject`）

### 2. 管理联系人和列表

**适用场景**：用户想要创建联系人列表、添加/更新联系人、搜索联系人或从列表中移除联系人。

**工具调用顺序**：
1. `SENDGRID_RETRIEVE_ALL_LISTS` - 列出所有营销列表 [必需]
2. `SENDGRID_CREATE_A_LIST` - 创建新的联系人列表 [可选]
3. `SENDGRID_GET_A_LIST_BY_ID` - 获取列表详情和示例联系人 [可选]
4. `SENDGRID_ADD_OR_UPDATE_A_CONTACT` - 添加/更新联系人并关联列表 [必需]
5. `SENDGRID_GET_CONTACTS_BY_EMAILS` - 通过邮箱查找联系人 [可选]
6. `SENDGRID_GET_CONTACTS_BY_IDENTIFIERS` - 通过邮箱、电话或外部 ID 查找联系人 [可选]
7. `SENDGRID_GET_LIST_CONTACT_COUNT` - 操作后验证联系人数量 [可选]
8. `SENDGRID_REMOVE_CONTACTS_FROM_A_LIST` - 从列表中移除联系人（不删除） [可选]
9. `SENDGRID_REMOVE_LIST_AND_OPTIONAL_CONTACTS` - 删除整个列表 [可选]
10. `SENDGRID_IMPORT_CONTACTS` - 从 CSV 批量导入 [可选]

**SENDGRID_ADD_OR_UPDATE_A_CONTACT 的关键参数**：
- `contacts`：联系人对象数组（最多 30,000 个或 6MB），每个至少包含一个标识符：`email`、`phone_number_id`、`external_id` 或 `anonymous_id`（必需）
- `list_ids`：要关联联系人的列表 UUID 字符串数组

**注意事项**：
- `SENDGRID_ADD_OR_UPDATE_A_CONTACT` 是异步操作；返回 202 和 `job_id`；联系人可能需要 10-30 秒才会出现
- 列表 ID 是 UUID（例如 "ca7a3796-e8a8-4029-9ccb-df8937940562"），不是整数
- 列表名称必须唯一；重复名称会导致 400 错误
- `SENDGRID_ADD_A_SINGLE_RECIPIENT_TO_A_LIST` 使用旧版 API；优先使用带 `list_ids` 的 `SENDGRID_ADD_OR_UPDATE_A_CONTACT`
- `SENDGRID_REMOVE_LIST_AND_OPTIONAL_CONTACTS` 不可逆；需要用户明确确认
- 邮箱地址会被 SendGrid 自动转为小写

### 3. 管理发件人身份

**适用场景**：用户想要设置或查看发件人身份（From 地址）用于发送邮件。

**工具调用顺序**：
1. `SENDGRID_GET_ALL_SENDER_IDENTITIES` - 列出所有现有发件人身份 [必需]
2. `SENDGRID_CREATE_A_SENDER_IDENTITY` - 创建新的发件人身份 [可选]
3. `SENDGRID_VIEW_A_SENDER_IDENTITY` - 查看特定发件人的详情 [可选]
4. `SENDGRID_UPDATE_A_SENDER_IDENTITY` - 更新发件人详情 [可选]
5. `SENDGRID_CREATE_VERIFIED_SENDER_REQUEST` - 创建并验证新发件人 [可选]
6. `SENDGRID_AUTHENTICATE_A_DOMAIN` - 设置域名认证以自动验证 [可选]

**SENDGRID_CREATE_A_SENDER_IDENTITY 的关键参数**：
- `from__email`：发件人邮箱地址（必需）
- `from__name`：显示名称（必需）
- `reply__to__email`：回复地址（必需）
- `nickname`：内部标识符（必需）
- `address`、`city`、`country`：符合 CAN-SPAM 法案的物理地址（必需）

**注意事项**：
- 新发件人使用前必须先验证；如果域名未认证，会发送验证邮件
- 每个账户最多 100 个唯一的发件人身份
- 避免使用具有严格 DMARC 策略的域名（gmail.com、yahoo.com）作为发件地址
- `SENDGRID_CREATE_VERIFIED_SENDER_REQUEST` 会发送验证邮件；发件人在验证前不可用

### 4. 查看邮件统计和活动

**适用场景**：用户想要查看邮件投递统计、退信率、打开/点击指标或邮件活动。

**工具调用顺序**：
1. `SENDGRID_RETRIEVE_GLOBAL_EMAIL_STATISTICS` - 获取账户级投递指标 [必需]
2. `SENDGRID_GET_ALL_CATEGORIES` - 发现可用的筛选类别 [可选]
3. `SENDGRID_RETRIEVE_EMAIL_STATISTICS_FOR_CATEGORIES` - 按类别获取细分统计 [可选]
4. `SENDGRID_FILTER_ALL_MESSAGES` - 按收件人、状态或日期搜索邮件活动 [可选]
5. `SENDGRID_FILTER_MESSAGES_BY_MESSAGE_ID` - 获取特定邮件的详细事件 [可选]
6. `SENDGRID_REQUEST_CSV` - 将活动数据导出为 CSV（适用于大数据集） [可选]
7. `SENDGRID_DOWNLOAD_CSV` - 下载导出的 CSV 文件 [可选]

**SENDGRID_RETRIEVE_GLOBAL_EMAIL_STATISTICS 的关键参数**：
- `start_date`：开始日期 YYYY-MM-DD（必需）
- `end_date`：结束日期 YYYY-MM-DD
- `aggregated_by`："day"、"week" 或 "month"
- `limit` / `offset`：分页（默认 500）

**SENDGRID_FILTER_ALL_MESSAGES 的关键参数**：
- `query`：类 SQL 查询字符串，例如 `status="delivered"`、`to_email="user@example.com"`，日期范围使用 `BETWEEN TIMESTAMP`
- `limit`：1-1000（默认 10）

**注意事项**：
- `SENDGRID_FILTER_ALL_MESSAGES` 需要"30 天额外邮件活动历史"付费附加组件；没有则返回 403
- 全局统计嵌套在 `details[].stats[0].metrics` 下，不是扁平结构
- 类别统计仅可查询过去 13 个月的数据
- `SENDGRID_RETRIEVE_EMAIL_STATISTICS_FOR_CATEGORIES` 每次请求最多 10 个类别
- CSV 导出每 12 小时限一次请求；链接 3 天后过期

### 5. 管理退订列表

**适用场景**：用户想要检查或管理退订组以满足邮件合规要求。

**工具调用顺序**：
1. `SENDGRID_GET_SUPPRESSION_GROUPS` - 列出所有退订组 [必需]
2. `SENDGRID_RETRIEVE_ALL_SUPPRESSION_GROUPS_FOR_AN_EMAIL_ADDRESS` - 检查特定邮箱的退订状态 [可选]

**注意事项**：
- 被退订的地址即使存在于营销列表中也无法投递
- 由于退订，活动发送数量可能低于列表数量

## 常用模式

### ID 解析
操作前始终将名称解析为 ID：
- **列表名称 -> list_id**：`SENDGRID_RETRIEVE_ALL_LISTS` 然后按名称匹配
- **发件人名称 -> sender_id**：`SENDGRID_GET_ALL_SENDER_IDENTITIES` 然后匹配
- **联系人邮箱 -> contact_id**：`SENDGRID_GET_CONTACTS_BY_EMAILS` 传入邮箱数组
- **模板名称 -> template_id**：使用 SendGrid UI 或模板端点

### 分页
- `SENDGRID_RETRIEVE_ALL_LISTS`：基于 token 的分页，使用 `page_token` 和 `page_size`（最大 1000）
- `SENDGRID_RETRIEVE_GLOBAL_EMAIL_STATISTICS`：基于偏移量的分页，使用 `limit`（最大 500）和 `offset`
- 始终对列表检索进行分页，避免遗漏已有列表

### 异步操作
联系人操作（`ADD_OR_UPDATE_A_CONTACT`、`IMPORT_CONTACTS`）是异步的：
- 返回 202 和 `job_id`
- 等待 10-30 秒后再用 `GET_CONTACTS_BY_EMAILS` 验证
- 使用 `GET_LIST_CONTACT_COUNT` 确认列表增长

## 已知陷阱

### ID 格式
- 营销列表 ID 是 UUID（例如 "ca7a3796-e8a8-4029-9ccb-df8937940562"）
- 旧版列表 ID 是整数；不要与 Marketing API 端点混用
- 发件人身份 ID 是整数
- 模板 ID：动态模板以 "d-" 开头，旧版模板是 UUID
- 联系人 ID 是 UUID

### 速率限制
- SendGrid 可能返回 HTTP 429；请遵守 `Retry-After` 头
- CSV 导出每 12 小时限一次请求
- 批量联系人 upsert 最大值：每次请求 30,000 个联系人或 6MB

### 参数怪癖
- 嵌套参数使用双下划线：`email__config__subject`、`from__email`
- CREATE_SINGLE_SEND 上的 `send_at` 仅设置 UI 默认值，不会调度发送
- `SENDGRID_ADD_A_SINGLE_RECIPIENT_TO_A_LIST` 使用旧版 API；`recipient_id` 是 Base64 编码的小写邮箱
- `SENDGRID_RETRIEVE_ALL_LISTS` 和 `SENDGRID_GET_ALL_LISTS` 都存在；优先使用 RETRIEVE_ALL_LISTS（Marketing API）
- 联系人添加是异步的（202）；始终在延迟后验证

### 旧版 vs Marketing API
- 部分工具使用旧版 Contact Database API（`/v3/contactdb/`），在新账户上可能返回 403
- 优先使用 Marketing API 工具：`SENDGRID_ADD_OR_UPDATE_A_CONTACT`、`SENDGRID_RETRIEVE_ALL_LISTS`、`SENDGRID_CREATE_SINGLE_SEND`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|---------|----------|
| 列出营销列表 | `SENDGRID_RETRIEVE_ALL_LISTS` | `page_size`、`page_token` |
| 创建列表 | `SENDGRID_CREATE_A_LIST` | `name` |
| 按 ID 获取列表 | `SENDGRID_GET_A_LIST_BY_ID` | `id` |
| 获取列表数量 | `SENDGRID_GET_LIST_CONTACT_COUNT` | `id` |
| 添加/更新联系人 | `SENDGRID_ADD_OR_UPDATE_A_CONTACT` | `contacts`、`list_ids` |
| 按邮箱搜索联系人 | `SENDGRID_GET_CONTACTS_BY_EMAILS` | `emails` |
| 按标识符搜索 | `SENDGRID_GET_CONTACTS_BY_IDENTIFIERS` | `identifier_type`、`identifiers` |
| 从列表移除 | `SENDGRID_REMOVE_CONTACTS_FROM_A_LIST` | `id`、`contact_ids` |
| 删除列表 | `SENDGRID_REMOVE_LIST_AND_OPTIONAL_CONTACTS` | `id`、`delete_contacts` |
| 导入联系人 CSV | `SENDGRID_IMPORT_CONTACTS` | 字段映射 |
| 创建 Single Send | `SENDGRID_CREATE_SINGLE_SEND` | `name`、`email__config__*`、`send__to__list__ids` |
| 列出发件人身份 | `SENDGRID_GET_ALL_SENDER_IDENTITIES` | （无） |
| 创建发件人 | `SENDGRID_CREATE_A_SENDER_IDENTITY` | `from__email`、`from__name`、`address` |
| 验证发件人 | `SENDGRID_CREATE_VERIFIED_SENDER_REQUEST` | `from_email`、`nickname`、`address` |
| 认证域名 | `SENDGRID_AUTHENTICATE_A_DOMAIN` | `domain` |
| 全局邮件统计 | `SENDGRID_RETRIEVE_GLOBAL_EMAIL_STATISTICS` | `start_date`、`aggregated_by` |
| 类别统计 | `SENDGRID_RETRIEVE_EMAIL_STATISTICS_FOR_CATEGORIES` | `start_date`、`categories` |
| 筛选邮件活动 | `SENDGRID_FILTER_ALL_MESSAGES` | `query`、`limit` |
| 邮件详情 | `SENDGRID_FILTER_MESSAGES_BY_MESSAGE_ID` | `msg_id` |
| 导出 CSV | `SENDGRID_REQUEST_CSV` | `query` |
| 下载 CSV | `SENDGRID_DOWNLOAD_CSV` | `download_uuid` |
| 列出类别 | `SENDGRID_GET_ALL_CATEGORIES` | （无） |
| 退订组 | `SENDGRID_GET_SUPPRESSION_GROUPS` | （无） |
| 获取模板 | `SENDGRID_RETRIEVE_A_SINGLE_TRANSACTIONAL_TEMPLATE` | `template_id` |
| 复制模板 | `SENDGRID_DUPLICATE_A_TRANSACTIONAL_TEMPLATE` | `template_id`、`name` |

## 适用场景
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
