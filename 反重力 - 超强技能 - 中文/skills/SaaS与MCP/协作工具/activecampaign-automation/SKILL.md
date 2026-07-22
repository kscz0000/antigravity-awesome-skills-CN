---
name: activecampaign-automation
description: "通过 Rube MCP (Composio) 自动化 ActiveCampaign 任务：管理联系人、标签、列表订阅、自动化注册和任务。触发词：ActiveCampaign自动化、AC自动化、邮件营销自动化、联系人管理、标签管理、自动化工作流、营销自动化、CRM自动化、ActiveCampaign集成"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 ActiveCampaign 自动化

通过 Composio 的 ActiveCampaign 工具包，经由 Rube MCP 自动化 ActiveCampaign CRM 和营销自动化操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 和工具包 `active_campaign` 建立有效的 ActiveCampaign 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `active_campaign` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 ActiveCampaign 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和查找联系人

**何时使用**：用户想要创建新联系人或查找现有联系人

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 搜索现有联系人 [可选]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT` - 创建新联系人 [必需]

**查找的关键参数**：
- `email`：按邮箱地址搜索
- `id`：按 ActiveCampaign 联系人 ID 搜索
- `phone`：按电话号码搜索

**创建的关键参数**：
- `email`：联系人邮箱地址（必需）
- `first_name`：联系人名字
- `last_name`：联系人姓氏
- `phone`：联系人电话号码
- `organization_name`：联系人所属组织
- `job_title`：联系人职位
- `tags`：逗号分隔的标签列表

**注意事项**：
- `email` 是创建联系人时唯一必需的字段
- 电话搜索在内部使用通用搜索参数；可能返回部分匹配结果
- 在 FIND_CONTACT 中同时使用 `email` 和 `phone` 时，结果在客户端进行过滤
- 创建时提供的标签会立即应用
- 使用已存在的邮箱创建联系人可能会更新现有联系人

### 2. 管理联系人标签

**何时使用**：用户想要为联系人添加或移除标签

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 通过邮箱或 ID 查找联系人 [前置条件]
2. `ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG` - 添加或移除标签 [必需]

**关键参数**：
- `action`：'Add' 或 'Remove'（必需）
- `tags`：标签名称，逗号分隔的字符串或字符串数组（必需）
- `contact_id`：联系人 ID（提供此参数或 contact_email）
- `contact_email`：联系人邮箱地址（contact_id 的替代选项）

**注意事项**：
- `action` 值需要大写：'Add' 或 'Remove'（非小写）
- 标签可以是逗号分隔的字符串（'tag1, tag2'）或数组（['tag1', 'tag2']）
- 必须提供 `contact_id` 或 `contact_email` 其中之一；`contact_id` 优先
- 添加不存在的标签会自动创建该标签
- 移除不存在的标签是空操作（不会报错）

### 3. 管理列表订阅

**何时使用**：用户想要订阅或取消订阅联系人列表

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找联系人 [前置条件]
2. `ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION` - 订阅或取消订阅 [必需]

**关键参数**：
- `action`：'subscribe' 或 'unsubscribe'（必需）
- `list_id`：数字列表 ID 字符串（必需）
- `email`：联系人邮箱地址（提供此参数或 contact_id）
- `contact_id`：数字联系人 ID 字符串（email 的替代选项）

**注意事项**：
- `action` 值为小写：'subscribe' 或 'unsubscribe'
- `list_id` 是数字字符串（例如 '2'），不是列表名称
- 列表 ID 可以通过 GET /api/3/lists 端点获取（不作为 Composio 工具提供；使用 ActiveCampaign UI）
- 如果同时提供 `email` 和 `contact_id`，`contact_id` 优先
- 取消订阅会将状态更改为 '2'（已取消订阅），但关系记录仍然保留

### 4. 将联系人添加到自动化

**何时使用**：用户想要将联系人注册到自动化工作流

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 验证联系人存在 [前置条件]
2. `ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION` - 将联系人注册到自动化 [必需]

**关键参数**：
- `contact_email`：要注册的联系人邮箱（必需）
- `automation_id`：目标自动化 ID（必需）

**注意事项**：
- 联系人必须已存在于 ActiveCampaign 中
- 自动化只能通过 ActiveCampaign UI 创建，不能通过 API 创建
- `automation_id` 必须引用现有的、处于活动状态的自动化
- 该工具执行两步流程：通过邮箱查找联系人，然后注册
- 自动化 ID 可在 ActiveCampaign UI 中找到，或通过 GET /api/3/automations 获取

### 5. 创建联系人任务

**何时使用**：用户想要创建与联系人关联的跟进任务

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找要关联任务的联系人 [前置条件]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK` - 创建任务 [必需]

**关键参数**：
- `relid`：要关联任务的联系人 ID（必需）
- `duedate`：ISO 8601 格式的截止日期，带时区（必需，例如 '2025-01-15T14:30:00-05:00'）
- `dealTasktype`：基于可用类型的任务类型 ID（必需）
- `title`：任务标题
- `note`：任务描述/内容
- `assignee`：分配任务的用户 ID
- `edate`：ISO 8601 格式的结束日期（必须晚于 duedate）
- `status`：0 表示未完成，1 表示已完成

**注意事项**：
- `duedate` 必须是带时区偏移的有效 ISO 8601 日期时间；不要使用占位符值
- `edate` 必须晚于 `duedate`
- `dealTasktype` 是引用 ActiveCampaign 中配置的任务类型的字符串 ID
- `relid` 是数字联系人 ID，不是邮箱地址
- `assignee` 是用户 ID；通过 ActiveCampaign UI 将用户名解析为 ID

## 常见模式

### 联系人查找流程

```
1. 使用 email 调用 ACTIVE_CAMPAIGN_FIND_CONTACT
2. 如果找到，提取联系人 ID 用于后续操作
3. 如果未找到，使用 ACTIVE_CAMPAIGN_CREATE_CONTACT 创建联系人
4. 使用联系人 ID 进行标签、订阅或自动化操作
```

### 批量联系人标签

```
1. 为每个联系人调用 ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG
2. 使用 contact_email 避免单独的查找调用
3. 合理延迟批量操作以遵守速率限制
```

### ID 解析

**联系人邮箱 -> 联系人 ID**：
```
1. 使用 email 调用 ACTIVE_CAMPAIGN_FIND_CONTACT
2. 从响应中提取 id
```

## 已知注意事项

**操作大小写**：
- 标签操作：'Add', 'Remove'（首字母大写）
- 订阅操作：'subscribe', 'unsubscribe'（小写）
- 大小写混淆会导致错误

**ID 类型**：
- 联系人 ID：数字字符串（例如 '123'）
- 列表 ID：数字字符串
- 自动化 ID：数字字符串
- 所有 ID 都应作为字符串传递，而非整数

**自动化**：
- 自动化无法通过 API 创建；只能进行注册
- 自动化必须处于活动状态才能接受新联系人
- 将已在自动化中的联系人注册可能无效

**速率限制**：
- ActiveCampaign API 对每个账户有速率限制
- 在收到 429 响应时实施退避策略
- 批量操作应适当间隔

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用回退模式进行防御性解析
- 联系人搜索可能返回多个结果；按邮箱匹配以确保准确性

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 查找联系人 | ACTIVE_CAMPAIGN_FIND_CONTACT | email, id, phone |
| 创建联系人 | ACTIVE_CAMPAIGN_CREATE_CONTACT | email, first_name, last_name, tags |
| 添加/移除标签 | ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG | action, tags, contact_email |
| 订阅/取消订阅 | ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION | action, list_id, email |
| 添加到自动化 | ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION | contact_email, automation_id |
| 创建任务 | ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK | relid, duedate, dealTasktype, title |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
