---
name: postmark-automation
description: "通过 Rube MCP（Composio）自动化 Postmark 邮件发送任务：发送模板邮件、管理模板、监控投递统计和退信。始终先搜索工具以获取当前 schema。当用户要求'发送模板邮件'、'管理邮件模板'、'查看投递统计'、'处理退信'、'Postmark自动化'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Postmark

通过 Composio 的 Postmark 工具包（经由 Rube MCP）自动化 Postmark 事务邮件操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立与工具包 `postmark` 的活跃 Postmark 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应正常，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包选择 `postmark`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Postmark 认证
4. 确认连接状态为 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 发送模板批量邮件

**使用场景**：用户希望一次调用向多个收件人发送模板邮件

**工具调用序列**：
1. `POSTMARK_LIST_TEMPLATES` - 查找可用模板及其 ID [前置步骤]
2. `POSTMARK_VALIDATE_TEMPLATE` - 发送前用模型数据验证模板 [可选]
3. `POSTMARK_SEND_BATCH_WITH_TEMPLATES` - 使用模板发送批量邮件 [必需]

**关键参数**：
- `TemplateId` 或 `TemplateAlias`：模板标识符
- `Messages`：消息对象数组，包含 `From`、`To`、`TemplateModel`
- `TemplateModel`：与模板变量匹配的键值对

**注意事项**：
- 每次批量调用最多 500 条消息
- `TemplateId` 和 `TemplateAlias` 二选一，不能同时使用
- `TemplateModel` 的键必须与模板变量名完全匹配（区分大小写）
- 发件人地址必须是已验证的 Sender Signature 或来自已验证的域名

### 2. 管理邮件模板

**使用场景**：用户希望创建、编辑或查看邮件模板

**工具调用序列**：
1. `POSTMARK_LIST_TEMPLATES` - 列出所有模板及其 ID 和名称 [必需]
2. `POSTMARK_GET_TEMPLATE` - 获取模板完整详情，包括 HTML/文本正文 [可选]
3. `POSTMARK_EDIT_TEMPLATE` - 更新模板内容或设置 [可选]
4. `POSTMARK_VALIDATE_TEMPLATE` - 用示例数据测试模板渲染效果 [可选]

**关键参数**：
- `TemplateId`：用于 GET/EDIT 操作的数字模板 ID
- `Name`：模板显示名称
- `Subject`：邮件主题（支持模板变量）
- `HtmlBody`：模板的 HTML 内容
- `TextBody`：纯文本备用内容
- `TemplateType`：'Standard' 或 'Layout'

**注意事项**：
- 模板 ID 是数字整数，不是字符串
- 编辑模板会替换整个内容；需要保留的字段必须一并传入
- Layout 模板包裹 Standard 模板；修改 Layout 会影响所有关联模板
- 发送前先验证，尽早发现缺失变量

### 3. 监控投递统计

**使用场景**：用户希望检查邮件投递健康度、打开/点击率或出站概览

**工具调用序列**：
1. `POSTMARK_GET_DELIVERY_STATS` - 获取按类型分组的退信计数 [必需]
2. `POSTMARK_GET_OUTBOUND_OVERVIEW` - 获取已发送/已打开/已点击/已退信摘要 [必需]
3. `POSTMARK_GET_TRACKED_EMAIL_COUNTS` - 获取一段时间内的追踪邮件量 [可选]

**关键参数**：
- `fromdate`：统计筛选起始日期（YYYY-MM-DD）
- `todate`：统计筛选结束日期（YYYY-MM-DD）
- `tag`：按消息标签筛选统计
- `messagestreamid`：按消息流筛选（如 'outbound'、'broadcast'）

**注意事项**：
- 日期参数使用 YYYY-MM-DD 格式，不含时间部分
- 统计数据为聚合结果；追踪单条消息需要单独的 API 调用
- 未指定 `messagestreamid` 时默认包含所有消息流

### 4. 管理退信和投诉

**使用场景**：用户希望查看退信邮件或垃圾邮件投诉

**工具调用序列**：
1. `POSTMARK_GET_BOUNCES` - 列出退信消息及详情 [必需]
2. `POSTMARK_GET_SPAM_COMPLAINTS` - 列出垃圾邮件投诉记录 [可选]
3. `POSTMARK_GET_DELIVERY_STATS` - 获取退信摘要计数 [可选]

**关键参数**：
- `count`：每页返回的记录数
- `offset`：结果分页偏移量
- `type`：退信类型筛选（如 'HardBounce'、'SoftBounce'、'SpamNotification'）
- `fromdate`/`todate`：日期范围筛选
- `emailFilter`：按收件人邮箱筛选

**注意事项**：
- 退信类型包括：HardBounce、SoftBounce、SpamNotification、SpamComplaint、Transient 等
- 硬退信表示永久投递失败；应移除这些地址
- 垃圾邮件投诉会影响发件人信誉；需定期监控
- 分页使用 `count` 和 `offset`，而非 page token

### 5. 配置服务器设置

**使用场景**：用户希望查看或修改 Postmark 服务器配置

**工具调用序列**：
1. `POSTMARK_GET_SERVER` - 获取当前服务器设置 [必需]
2. `POSTMARK_EDIT_SERVER` - 更新服务器配置 [可选]

**关键参数**：
- `Name`：服务器显示名称
- `SmtpApiActivated`：启用/禁用 SMTP API 访问
- `BounceHookUrl`：退信通知的 Webhook URL
- `InboundHookUrl`：入站邮件处理的 Webhook URL
- `TrackOpens`：启用/禁用打开追踪
- `TrackLinks`：链接追踪模式（'None'、'HtmlAndText'、'HtmlOnly'、'TextOnly'）

**注意事项**：
- 服务器修改会影响通过该服务器发送的所有消息
- Webhook URL 必须是可公开访问的 HTTPS 端点
- 更改 `SmtpApiActivated` 会立即影响 SMTP 中继访问
- 追踪设置仅对后续消息生效，不会追溯应用

## 常用模式

### 模板变量解析

```
1. Call POSTMARK_GET_TEMPLATE with TemplateId
2. Inspect HtmlBody/TextBody for {{variable}} placeholders
3. Build TemplateModel dict with matching keys
4. Call POSTMARK_VALIDATE_TEMPLATE to verify rendering
```

### 分页

- 设置 `count` 控制每页结果数（因端点而异）
- 使用 `offset` 跳过已获取的结果
- 每页将 offset 递增 count，直到返回结果数 < count
- 响应元数据中可能返回总记录数

## 已知陷阱

**认证**：
- Postmark 使用服务器级 API token，而非账户级
- 每个服务器有独立的 token；确保使用正确的服务器上下文
- 发件人地址必须是已验证的 Sender Signature 或来自已验证的域名

**速率限制**：
- 批量发送限制为每次调用 500 条消息
- API 速率限制因端点而异；遇到 429 响应时实现退避重试

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用防御性解析并设置回退模式
- 模板 ID 始终是数字整数

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 发送模板批量邮件 | POSTMARK_SEND_BATCH_WITH_TEMPLATES | Messages, TemplateId/TemplateAlias |
| 列出模板 | POSTMARK_LIST_TEMPLATES | Count, Offset, TemplateType |
| 获取模板详情 | POSTMARK_GET_TEMPLATE | TemplateId |
| 编辑模板 | POSTMARK_EDIT_TEMPLATE | TemplateId, Name, Subject, HtmlBody |
| 验证模板 | POSTMARK_VALIDATE_TEMPLATE | TemplateId, TemplateModel |
| 投递统计 | POSTMARK_GET_DELIVERY_STATS | （无或日期筛选） |
| 出站概览 | POSTMARK_GET_OUTBOUND_OVERVIEW | fromdate, todate, tag |
| 获取退信 | POSTMARK_GET_BOUNCES | count, offset, type, emailFilter |
| 获取垃圾投诉 | POSTMARK_GET_SPAM_COMPLAINTS | count, offset, fromdate, todate |
| 追踪邮件计数 | POSTMARK_GET_TRACKED_EMAIL_COUNTS | fromdate, todate, tag |
| 获取服务器配置 | POSTMARK_GET_SERVER | （无） |
| 编辑服务器配置 | POSTMARK_EDIT_SERVER | Name, TrackOpens, TrackLinks |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
