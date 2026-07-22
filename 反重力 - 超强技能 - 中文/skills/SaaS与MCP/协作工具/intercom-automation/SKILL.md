---
name: intercom-automation
description: "通过 Rube MCP (Composio) 自动化 Intercom 任务：对话、联系人、公司、分群、管理员。始终先搜索工具获取当前 schema。触发词：Intercom自动化、Intercom对话管理、Intercom联系人、Intercom公司管理、Intercom分群、Intercom管理员、Rube MCP Intercom"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Intercom 自动化

通过 Rube MCP 使用 Composio 的 Intercom 工具包自动化 Intercom 操作。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Intercom 连接，toolkit 设为 `intercom`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 能正常响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `intercom`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Intercom OAuth
4. 在运行任何工作流前确认连接状态为 ACTIVE

## 核心工作流

### 1. 管理对话

**适用场景**：用户需要创建、列出、搜索或管理客服对话

**工具调用顺序**：
1. `INTERCOM_LIST_ALL_ADMINS` - 获取管理员 ID 用于分配 [前提]
2. `INTERCOM_LIST_CONVERSATIONS` - 列出所有对话 [可选]
3. `INTERCOM_SEARCH_CONVERSATIONS` - 按条件搜索 [可选]
4. `INTERCOM_GET_CONVERSATION` - 获取对话详情 [可选]
5. `INTERCOM_CREATE_CONVERSATION` - 创建新对话 [可选]

**关键参数**：
- `from`：包含 `type`（'user'/'lead'）和 `id` 的对象，标识对话发起者
- `body`：消息正文（支持 HTML）
- `id`：对话 ID，用于检索
- `query`：搜索查询对象，包含 `field`、`operator`、`value`

**注意事项**：
- CREATE_CONVERSATION 的 `from` 字段必须是联系人（user/lead），不能是管理员
- 对话正文支持 HTML；纯文本会自动包裹在 `<p>` 标签中
- 搜索查询使用结构化过滤对象，不支持自由文本搜索
- 对话 ID 为数字字符串

### 2. 回复与管理对话状态

**适用场景**：用户需要回复、关闭、重新打开或分配对话

**工具调用顺序**：
1. `INTERCOM_GET_CONVERSATION` - 获取当前状态 [前提]
2. `INTERCOM_REPLY_TO_CONVERSATION` - 添加回复 [可选]
3. `INTERCOM_ASSIGN_CONVERSATION` - 分配给管理员/团队 [可选]
4. `INTERCOM_CLOSE_CONVERSATION` - 关闭对话 [可选]
5. `INTERCOM_REOPEN_CONVERSATION` - 重新打开已关闭的对话 [可选]

**关键参数**：
- `conversation_id` / `id`：对话 ID
- `body`：回复消息正文（支持 HTML）
- `type`：回复类型（'admin' 或 'user'）
- `admin_id`：管理员 ID，用于管理员回复、分配及关闭/重新打开
- `assignee_id`：管理员或团队 ID，用于分配
- `message_type`：'comment'（默认）或 'note'（内部备注）

**注意事项**：
- 管理员回复、关闭、重新打开和分配操作必须提供 `admin_id`
- 始终先用 LIST_ALL_ADMINS 或 IDENTIFY_AN_ADMIN 获取管理员 ID
- 重试可能导致重复发送；需实现幂等性检查
- 内部备注使用 `message_type: 'note'`；仅工作区成员可见
- 关闭操作需要 admin_id，body 消息可选

### 3. 管理联系人

**适用场景**：用户需要搜索、查看或管理联系人（用户和潜在客户）

**工具调用顺序**：
1. `INTERCOM_SEARCH_CONTACTS` - 按条件搜索联系人 [必需]
2. `INTERCOM_GET_A_CONTACT` - 获取特定联系人 [可选]
3. `INTERCOM_SHOW_CONTACT_BY_EXTERNAL_ID` - 按外部 ID 查找 [可选]
4. `INTERCOM_LIST_CONTACTS` - 列出所有联系人 [可选]
5. `INTERCOM_LIST_TAGS_ATTACHED_TO_A_CONTACT` - 获取联系人标签 [可选]
6. `INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_CONTACT` - 获取联系人分群 [可选]
7. `INTERCOM_DETACH_A_CONTACT` - 将联系人从公司移除 [可选]

**关键参数**：
- `contact_id`：联系人 ID，用于检索
- `external_id`：外部系统 ID，用于查找
- `query`：搜索过滤对象，包含 `field`、`operator`、`value`
- `pagination`：包含 `per_page` 和 `starting_after` 游标的对象

**注意事项**：
- SEARCH_CONTACTS 使用结构化查询过滤，不支持自由文本；格式：`{field, operator, value}`
- 支持的运算符：`=`、`!=`、`>`、`<`、`~`（包含）、`!~`（不包含）、`IN`、`NIN`
- 联系人类型为 'user'（已识别）或 'lead'（匿名）
- LIST_CONTACTS 返回分页结果；使用 `starting_after` 游标翻页
- 外部 ID 区分大小写

### 4. 管理管理员和团队

**适用场景**：用户需要列出工作区管理员或查找特定管理员

**工具调用顺序**：
1. `INTERCOM_LIST_ALL_ADMINS` - 列出所有管理员和团队 [必需]
2. `INTERCOM_IDENTIFY_AN_ADMIN` - 获取特定管理员详情 [可选]

**关键参数**：
- `admin_id`：管理员 ID，用于识别

**注意事项**：
- LIST_ALL_ADMINS 同时返回管理员和团队
- 对话回复、分配、关闭和重新打开操作需要管理员 ID
- 团队以 `type: 'team'` 出现在管理员列表中

### 5. 查看分群和计数

**适用场景**：用户需要查看分群或获取聚合计数

**工具调用顺序**：
1. `INTERCOM_LIST_SEGMENTS` - 列出所有分群 [可选]
2. `INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_CONTACT` - 联系人的分群 [可选]
3. `INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_COMPANIES` - 公司的分群 [可选]
4. `INTERCOM_GET_COUNTS` - 获取聚合计数 [可选]

**关键参数**：
- `contact_id`：联系人 ID，用于分群查询
- `company_id`：公司 ID，用于分群查询
- `type`：计数类型（'conversation'、'company'、'user'、'tag'、'segment'）
- `count`：子计数类型

**注意事项**：
- GET_COUNTS 返回近似计数，非精确数值
- 分群成员资格是计算得出的；变更可能不会立即反映

### 6. 管理公司

**适用场景**：用户需要列出公司或管理公司与联系人的关系

**工具调用顺序**：
1. `INTERCOM_LIST_ALL_COMPANIES` - 列出所有公司 [必需]
2. `INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_COMPANIES` - 获取公司分群 [可选]
3. `INTERCOM_DETACH_A_CONTACT` - 将联系人从公司移除 [可选]

**关键参数**：
- `company_id`：公司 ID
- `contact_id`：联系人 ID，用于解除关联
- `page`：页码，用于分页
- `per_page`：每页结果数

**注意事项**：
- 公司与联系人的关系通过联系人端点管理
- DETACH_A_CONTACT 移除的是联系人与公司的关联，而非联系人本身

## 常用模式

### 搜索查询过滤

**单条件过滤**：
```json
{
  "field": "email",
  "operator": "=",
  "value": "user@example.com"
}
```

**多条件过滤（AND）**：
```json
{
  "operator": "AND",
  "value": [
    {"field": "role", "operator": "=", "value": "user"},
    {"field": "created_at", "operator": ">", "value": 1672531200}
  ]
}
```

**联系人支持的字段**：email, name, role, created_at, updated_at, signed_up_at, last_seen_at, external_id

**对话支持的字段**：created_at, updated_at, source.type, state, open, read

### 分页

- 大部分列表端点使用基于游标的分页
- 检查响应中的 `pages.next` 和 `starting_after` 游标
- 在 `pagination.starting_after` 中传入游标获取下一页
- 持续翻页直到 `pages.next` 为 null

### 管理员 ID 解析

```
1. Call INTERCOM_LIST_ALL_ADMINS to get all admins
2. Find the desired admin by name or email
3. Use admin.id for replies, assignments, and state changes
```

## 已知注意事项

**管理员 ID 要求**：
- 以下操作需要管理员 ID：以管理员身份回复、分配、关闭、重新打开
- 始终先用 LIST_ALL_ADMINS 解析管理员 ID

**HTML 内容**：
- 对话正文为 HTML 格式
- 纯文本会自动包裹在段落标签中
- 对 HTML 输入进行消毒处理，防止渲染问题

**幂等性**：
- 回复和对话创建操作不具备幂等性
- 重试或超时时可能发生重复发送
- 跟踪消息 ID 以防止重复

**速率限制**：
- 默认：约 1000 请求/分钟（因套餐而异）
- 429 响应包含速率限制头信息
- 实现指数退避重试策略

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出对话 | INTERCOM_LIST_CONVERSATIONS | (pagination) |
| 搜索对话 | INTERCOM_SEARCH_CONVERSATIONS | query |
| 获取对话 | INTERCOM_GET_CONVERSATION | id |
| 创建对话 | INTERCOM_CREATE_CONVERSATION | from, body |
| 回复对话 | INTERCOM_REPLY_TO_CONVERSATION | conversation_id, body, admin_id |
| 分配对话 | INTERCOM_ASSIGN_CONVERSATION | conversation_id, admin_id, assignee_id |
| 关闭对话 | INTERCOM_CLOSE_CONVERSATION | id, admin_id |
| 重新打开对话 | INTERCOM_REOPEN_CONVERSATION | id, admin_id |
| 搜索联系人 | INTERCOM_SEARCH_CONTACTS | query |
| 获取联系人 | INTERCOM_GET_A_CONTACT | contact_id |
| 按外部 ID 查找联系人 | INTERCOM_SHOW_CONTACT_BY_EXTERNAL_ID | external_id |
| 列出联系人 | INTERCOM_LIST_CONTACTS | (pagination) |
| 联系人标签 | INTERCOM_LIST_TAGS_ATTACHED_TO_A_CONTACT | contact_id |
| 联系人分群 | INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_CONTACT | contact_id |
| 解除联系人关联 | INTERCOM_DETACH_A_CONTACT | contact_id, company_id |
| 列出管理员 | INTERCOM_LIST_ALL_ADMINS | (none) |
| 识别管理员 | INTERCOM_IDENTIFY_AN_ADMIN | admin_id |
| 列出分群 | INTERCOM_LIST_SEGMENTS | (none) |
| 公司分群 | INTERCOM_LIST_ATTACHED_SEGMENTS_FOR_COMPANIES | company_id |
| 获取计数 | INTERCOM_GET_COUNTS | type, count |
| 列出公司 | INTERCOM_LIST_ALL_COMPANIES | page, per_page |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 若缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
