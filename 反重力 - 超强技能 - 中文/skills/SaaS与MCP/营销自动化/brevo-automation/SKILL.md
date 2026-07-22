---
name: brevo-automation
description: "通过 Rube MCP 的 Composio Brevo 工具包自动化 Brevo（原 Sendinblue）邮件营销操作。当用户要求'管理 Brevo 邮件营销'、'Brevo 自动化'、'Sendinblue 邮件操作'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Brevo 自动化

通过 Rube MCP 的 Composio Brevo 工具包自动化 Brevo（原 Sendinblue）邮件营销操作。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Brevo 连接，toolkit 设为 `brevo`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 能正常响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `brevo`
3. 如果连接状态不是 ACTIVE，按返回的认证链接完成 Brevo 认证
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 管理邮件营销活动

**适用场景**：用户想要列出、查看或更新邮件营销活动

**工具调用顺序**：
1. `BREVO_LIST_EMAIL_CAMPAIGNS` - 列出所有营销活动（支持筛选）[必需]
2. `BREVO_UPDATE_EMAIL_CAMPAIGN` - 更新营销活动内容或设置 [可选]

**列出操作的关键参数**：
- `type`：营销活动类型（'classic' 或 'trigger'）
- `status`：营销活动状态（'suspended'、'archive'、'sent'、'queued'、'draft'、'inProcess'、'inReview'）
- `startDate`/`endDate`：日期范围筛选（YYYY-MM-DDTHH:mm:ss.SSSZ 格式）
- `statistics`：要包含的统计类型（'globalStats'、'linksStats'、'statsByDomain'）
- `limit`：每页结果数（最大 100，默认 50）
- `offset`：分页偏移量
- `sort`：排序方式（'asc' 或 'desc'）
- `excludeHtmlContent`：设为 `true` 可减小响应体积

**更新操作的关键参数**：
- `campaign_id`：营销活动数字 ID（必需）
- `name`：营销活动名称
- `subject`：邮件主题行
- `htmlContent`：HTML 邮件正文（与 `htmlUrl` 互斥）
- `htmlUrl`：HTML 内容的 URL
- `sender`：发件人对象，包含 `name`、`email` 或 `id`
- `recipients`：收件人对象，包含 `listIds` 和 `exclusionListIds`
- `scheduledAt`：计划发送时间（YYYY-MM-DDTHH:mm:ss.SSSZ）

**注意事项**：
- `startDate` 和 `endDate` 必须同时提供或同时省略
- 日期筛选仅在未传 `status` 或 `status` 设为 'sent' 时生效
- `htmlContent` 和 `htmlUrl` 互斥
- 营销活动的 `sender` 邮箱必须是 Brevo 中已验证的发件人
- A/B 测试字段（`subjectA`、`subjectB`、`splitRule`、`winnerCriteria`）需要 `abTesting: true`
- `scheduledAt` 使用带时区的完整 ISO 8601 格式

### 2. 创建和管理邮件模板

**适用场景**：用户想要创建、编辑、列出或删除邮件模板

**工具调用顺序**：
1. `BREVO_GET_ALL_EMAIL_TEMPLATES` - 列出所有模板 [必需]
2. `BREVO_CREATE_OR_UPDATE_EMAIL_TEMPLATE` - 创建新模板或更新已有模板 [必需]
3. `BREVO_DELETE_EMAIL_TEMPLATE` - 删除非活跃模板 [可选]

**列出操作的关键参数**：
- `templateStatus`：筛选活跃（`true`）或非活跃（`false`）模板
- `limit`：每页结果数（最大 1000，默认 50）
- `offset`：分页偏移量
- `sort`：排序方式（'asc' 或 'desc'）

**创建/更新操作的关键参数**：
- `templateId`：传入则更新；省略则创建新模板
- `templateName`：模板显示名称（创建时必需）
- `subject`：邮件主题行（创建时必需）
- `htmlContent`：HTML 模板正文（最少 10 个字符；使用此参数或 `htmlUrl`）
- `sender`：发件人对象，包含 `name` 和 `email`，或 `id`（创建时必需）
- `replyTo`：回复邮箱地址
- `isActive`：激活或停用模板
- `tag`：模板分类标签

**注意事项**：
- 传入 `templateId` 时为更新操作，省略时为创建操作
- 创建时 `templateName`、`subject` 和 `sender` 为必需参数
- `htmlContent` 至少 10 个字符
- 模板个性化使用 `{{contact.ATTRIBUTE}}` 语法
- 只有非活跃模板才能被删除
- `htmlContent` 和 `htmlUrl` 互斥

### 3. 管理发件人

**适用场景**：用户想要查看已授权的发件人身份

**工具调用顺序**：
1. `BREVO_GET_ALL_SENDERS` - 列出所有已验证发件人 [必需]

**关键参数**：（无需必填参数）

**注意事项**：
- 发件人必须先验证才能在营销活动或模板中使用
- 发件人验证需通过 Brevo 网页界面完成，不支持 API 验证
- 发件人 ID 可用于营销活动和模板的 `sender.id` 字段

### 4. 配置 A/B 测试营销活动

**适用场景**：用户想要设置或修改营销活动的 A/B 测试配置

**工具调用顺序**：
1. `BREVO_LIST_EMAIL_CAMPAIGNS` - 找到目标营销活动 [前置步骤]
2. `BREVO_UPDATE_EMAIL_CAMPAIGN` - 配置 A/B 测试设置 [必需]

**关键参数**：
- `campaign_id`：要配置的营销活动
- `abTesting`：设为 `true` 启用 A/B 测试
- `subjectA`：变体 A 的主题行
- `subjectB`：变体 B 的主题行
- `splitRule`：测试的百分比分配（1-99）
- `winnerCriteria`：决定胜出者的标准，'open' 或 'click'
- `winnerDelay`：选择胜出者前等待的小时数（1-168）

**注意事项**：
- 必须先启用 A/B 测试（`abTesting: true`）才能设置变体字段
- `splitRule` 是接收变体 A 的联系人百分比
- `winnerDelay` 定义测试多长时间后将胜出版本发送给剩余联系人
- 仅适用于 'classic' 类型的营销活动

## 常用模式

### 营销活动生命周期

```
1. Create campaign (status: draft)
2. Set recipients (listIds)
3. Configure content (htmlContent or htmlUrl)
4. Optionally schedule (scheduledAt)
5. Send or schedule via Brevo UI (API update can set scheduledAt)
```

### 分页

- 使用 `limit`（每页大小）和 `offset`（起始索引）
- 默认 limit 为 50；各端点最大值不同（营销活动 100，模板 1000）
- 每翻一页将 `offset` 增加 `limit`
- 通过响应中的 `count` 判断总可用数量

### 模板个性化

```
- First name: {{contact.FIRSTNAME}}
- Last name: {{contact.LASTNAME}}
- Custom attribute: {{contact.CUSTOM_ATTRIBUTE}}
- Mirror link: {{mirror}}
- Unsubscribe link: {{unsubscribe}}
```

## 已知注意事项

**日期格式**：
- 所有日期使用带毫秒的 ISO 8601 格式：YYYY-MM-DDTHH:mm:ss.SSSZ
- 在日期时间格式中传入时区以确保结果准确
- `startDate` 和 `endDate` 必须成对使用

**发件人验证**：
- 所有发件人邮箱必须先在 Brevo 中验证才能使用
- 未验证的发件人会导致营销活动创建/更新失败
- 使用 GET_ALL_SENDERS 检查可用的已验证发件人

**速率限制**：
- Brevo API 根据账户套餐有速率限制
- 收到 429 响应时实施退避策略
- 模板操作的速率限制低于读取操作

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用带回退模式的防御性解析
- 营销活动和模板 ID 为数字整数

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出营销活动 | BREVO_LIST_EMAIL_CAMPAIGNS | type, status, limit, offset |
| 更新营销活动 | BREVO_UPDATE_EMAIL_CAMPAIGN | campaign_id, subject, htmlContent |
| 列出模板 | BREVO_GET_ALL_EMAIL_TEMPLATES | templateStatus, limit, offset |
| 创建模板 | BREVO_CREATE_OR_UPDATE_EMAIL_TEMPLATE | templateName, subject, htmlContent, sender |
| 更新模板 | BREVO_CREATE_OR_UPDATE_EMAIL_TEMPLATE | templateId, htmlContent |
| 删除模板 | BREVO_DELETE_EMAIL_TEMPLATE | templateId |
| 列出发件人 | BREVO_GET_ALL_SENDERS | （无） |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能
- 不要将输出视为环境特定验证、测试或专家审查的替代
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清
