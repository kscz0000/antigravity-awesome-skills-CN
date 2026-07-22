---
name: klaviyo-automation
description: "通过 Rube MCP (Composio) 自动化 Klaviyo 任务：管理邮件/SMS 营销活动、查看活动消息、追踪标签、监控发送任务。始终先搜索工具获取最新 schema。触发词：Klaviyo自动化、邮件营销自动化、SMS营销、活动管理、Klaviyo MCP、Rube MCP、营销活动监控"
risk: safe
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Klaviyo 自动化

通过 Composio 的 Klaviyo 工具包，经 Rube MCP 自动化 Klaviyo 邮件和 SMS 营销操作。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `klaviyo` 建立活跃的 Klaviyo 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 能正常响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `klaviyo`
3. 如果连接状态不是 ACTIVE，按返回的认证链接完成 Klaviyo 身份验证
4. 运行任何工作流前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 列出和筛选营销活动

**适用场景**：用户需要浏览、搜索或筛选营销活动

**工具调用顺序**：
1. `KLAVIYO_GET_CAMPAIGNS` - 按渠道和状态筛选列出活动 [必需]

**关键参数**：
- `channel`：活动渠道 — 'email' 或 'sms'（Klaviyo API 必填）
- `filter`：附加筛选字符串（如 `equals(status,"draft")`）
- `sort`：排序字段，`-` 前缀表示降序（如 '-created_at'、'name'）
- `page_cursor`：下一页的分页游标
- `include_archived`：是否包含已归档的活动（默认：false）

**注意事项**：
- `channel` 为必填项；省略可能导致结果不完整或异常
- 必须分页才能获取完整数据；单次调用仅返回一页（默认约 10 条）
- 持续跟随 `page_cursor` 直到耗尽，以获取所有活动
- 通过 `filter` 进行状态筛选（如 `equals(status,"draft")`）可能返回混合状态；务必在客户端校验 `data[].attributes.status`
- 状态字符串区分大小写，且可能是复合值（如 'Cancelled: No Recipients'）
- 响应结构为嵌套格式：`response.data.data`，状态位于 `data[].attributes.status`

### 2. 获取活动详情

**适用场景**：用户需要某个活动的详细信息

**工具调用顺序**：
1. `KLAVIYO_GET_CAMPAIGNS` - 查找活动以获取其 ID [前置步骤]
2. `KLAVIYO_GET_CAMPAIGN` - 获取完整活动详情 [必需]

**关键参数**：
- `campaign_id`：活动 ID 字符串（如 '01GDDKASAP8TKDDA2GRZDSVP4H'）
- `include_messages`：在响应中包含活动消息
- `include_tags`：在响应中包含标签

**注意事项**：
- 活动 ID 为字母数字字符串，非纯数字
- `include_messages` 和 `include_tags` 通过 Klaviyo 的 include 机制在响应中添加关联数据
- 活动详情包含受众、发送策略、追踪选项和调度信息

### 3. 查看活动消息

**适用场景**：用户需要查看活动的邮件/SMS 内容

**工具调用顺序**：
1. `KLAVIYO_GET_CAMPAIGN` - 查找活动及其消息 ID [前置步骤]
2. `KLAVIYO_GET_CAMPAIGN_MESSAGE` - 获取消息内容详情 [必需]

**关键参数**：
- `id`：消息 ID 字符串
- `fields__campaign__message`：消息属性的稀疏字段集（如 'content.subject'、'content.from_email'、'content.body'）
- `fields__campaign`：活动属性的稀疏字段集
- `fields__template`：模板属性的稀疏字段集
- `include`：要包含的关联资源（'campaign'、'template'）

**注意事项**：
- 消息 ID 与活动 ID 不同；需从活动响应中提取
- 稀疏字段集语法使用点号表示嵌套字段：'content.subject'、'content.from_email'
- 邮件消息包含内容字段：subject、preview_text、from_email、from_label、reply_to_email
- SMS 消息包含内容字段：body
- 包含 'template' 可获取邮件的 HTML/文本内容

### 4. 管理活动标签

**适用场景**：用户需要查看与活动关联的标签以便组织管理

**工具调用顺序**：
1. `KLAVIYO_GET_CAMPAIGN_RELATIONSHIPS_TAGS` - 获取活动的标签 ID [必需]

**关键参数**：
- `id`：活动 ID 字符串

**注意事项**：
- 仅返回标签 ID，不返回标签名称/详情
- 标签 ID 可配合 Klaviyo 的标签端点获取完整详情
- 速率限制：突发 3次/秒，持续 60次/分钟（比其他端点更严格）

### 5. 监控活动发送任务

**适用场景**：用户需要检查活动发送操作的状态

**工具调用顺序**：
1. `KLAVIYO_GET_CAMPAIGN_SEND_JOB` - 检查发送任务状态 [必需]

**关键参数**：
- `id`：发送任务 ID

**注意事项**：
- 发送任务 ID 在发起活动发送时返回
- 任务状态指示发送是否排队中、进行中、已完成或失败
- 速率限制：突发 10次/秒，持续 150次/分钟

## 常用模式

### 活动发现模式

```
1. Call KLAVIYO_GET_CAMPAIGNS with channel='email'
2. Paginate through all results via page_cursor
3. Filter by status client-side for accuracy
4. Extract campaign IDs for detailed inspection
```

### 稀疏字段集模式

Klaviyo 支持稀疏字段集以减小响应体积：
```
fields__campaign__message=['content.subject', 'content.from_email', 'send_times']
fields__campaign=['name', 'status', 'send_time']
fields__template=['name', 'html', 'text']
```

### 分页

- Klaviyo 使用基于游标的分页
- 检查响应分页元数据中的 `page_cursor`
- 在下次请求中将游标作为 `page_cursor` 传入
- 默认每页约 10 个活动
- 持续请求直到不再返回游标

### 筛选语法

```
- equals(status,"draft") - Campaigns in draft status
- equals(name,"Newsletter") - Campaign named "Newsletter"
- greater-than(created_at,"2024-01-01T00:00:00Z") - Created after date
```

## 已知注意事项

**API 版本**：
- Klaviyo API 使用版本化端点（如 v2024-07-15）
- 响应 schema 可能随 API 版本变化
- 工具响应遵循 Composio 集成中配置的版本

**响应嵌套**：
- 数据为嵌套结构：`response.data.data[].attributes`
- 活动状态位于 `data[].attributes.status`
- 解析嵌套结构出错会导致结果为空或不正确
- 务必沿完整路径进行防御性导航

**速率限制**：
- 突发：10次/秒（标签端点 3次/秒）
- 持续：150次/分钟（标签端点 60次/分钟）
- 所需权限范围：campaigns:read
- 收到 429 响应时实施退避策略

**状态值**：
- 状态字符串区分大小写
- 存在复合状态（如 'Cancelled: No Recipients'）
- 服务端筛选可能返回混合状态；务必在客户端校验

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出活动 | KLAVIYO_GET_CAMPAIGNS | channel, filter, sort, page_cursor |
| 获取活动详情 | KLAVIYO_GET_CAMPAIGN | campaign_id, include_messages, include_tags |
| 获取活动消息 | KLAVIYO_GET_CAMPAIGN_MESSAGE | id, fields__campaign__message |
| 获取活动标签 | KLAVIYO_GET_CAMPAIGN_RELATIONSHIPS_TAGS | id |
| 获取发送任务状态 | KLAVIYO_GET_CAMPAIGN_SEND_JOB | id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
