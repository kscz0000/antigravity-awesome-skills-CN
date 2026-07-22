---
name: convertkit-automation
description: "通过 Rube MCP (Composio) 自动化 ConvertKit (Kit) 任务：管理订阅者、标签、广播和广播统计。始终先搜索工具以获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 ConvertKit (Kit) 自动化

通过 Composio 的 Kit 工具包（经由 Rube MCP）自动化 ConvertKit（现称为 Kit）邮件营销操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立有效的 Kit 连接（工具包名称为 `kit`）
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `kit` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Kit 认证
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出和搜索订阅者

**适用场景**：用户想要浏览、搜索或筛选邮件订阅者

**工具调用顺序**：
1. `KIT_LIST_SUBSCRIBERS` - 使用筛选条件和分页列出订阅者 [必需]

**关键参数**：
- `status`：按状态筛选（'active' 或 'inactive'）
- `email_address`：精确邮箱搜索
- `created_after`/`created_before`：日期范围筛选（YYYY-MM-DD）
- `updated_after`/`updated_before`：日期范围筛选（YYYY-MM-DD）
- `sort_field`：排序字段，可选 'id'、'cancelled_at' 或 'updated_at'
- `sort_order`：排序方向，'asc' 或 'desc'
- `per_page`：每页结果数（最小为 1）
- `after`/`before`：分页游标字符串
- `include_total_count`：设为 'true' 以获取订阅者总数

**注意事项**：
- 如果 `sort_field` 为 'cancelled_at'，则 `status` 必须设为 'cancelled'
- 日期筛选使用 YYYY-MM-DD 格式（不含时间部分）
- `email_address` 为精确匹配；不支持部分邮箱搜索
- 分页使用基于游标的方式，通过 `after`/`before` 游标字符串实现
- `include_total_count` 是字符串 'true'，不是布尔值

### 2. 管理订阅者标签

**适用场景**：用户想要为订阅者添加标签以进行细分

**工具调用顺序**：
1. `KIT_LIST_SUBSCRIBERS` - 通过邮箱查找订阅者 ID [前置步骤]
2. `KIT_TAG_SUBSCRIBER` - 将订阅者与标签关联 [必需]
3. `KIT_LIST_TAG_SUBSCRIBERS` - 列出特定标签下的订阅者 [可选]

**标签操作关键参数**：
- `tag_id`：数字标签 ID（必需）
- `subscriber_id`：数字订阅者 ID（必需）

**注意事项**：
- `tag_id` 和 `subscriber_id` 都必须是正整数
- 标签 ID 必须引用已存在的标签；标签通过 Kit 网页界面创建
- 为已打标签的订阅者再次打标签是幂等的（不会报错）
- 订阅者 ID 从 LIST_SUBSCRIBERS 返回；使用 `email_address` 筛选查找特定订阅者

### 3. 取消订阅者订阅

**适用场景**：用户想要取消订阅者的所有通信

**工具调用顺序**：
1. `KIT_LIST_SUBSCRIBERS` - 查找订阅者 ID [前置步骤]
2. `KIT_DELETE_SUBSCRIBER` - 取消订阅者订阅 [必需]

**关键参数**：
- `id`：订阅者 ID（必需，正整数）

**注意事项**：
- 此操作将永久取消订阅者接收所有邮件通信
- 订阅者的历史数据会保留，但不再收到邮件
- 操作是幂等的；取消已取消订阅的订阅者会成功且不报错
- 成功时返回空响应（HTTP 204 No Content）
- 订阅者 ID 必须存在；不存在的 ID 返回 404

### 4. 列出和查看广播

**适用场景**：用户想要浏览邮件广播或获取特定广播的详情

**工具调用顺序**：
1. `KIT_LIST_BROADCASTS` - 分页列出所有广播 [必需]
2. `KIT_GET_BROADCAST` - 获取特定广播的详细信息 [可选]
3. `KIT_GET_BROADCAST_STATS` - 获取广播的性能统计 [可选]

**列出的关键参数**：
- `per_page`：每页结果数（1-500）
- `after`/`before`：分页游标字符串
- `include_total_count`：设为 'true' 获取总数

**详情的关键参数**：
- `id`：广播 ID（必需，正整数）

**注意事项**：
- 广播的 `per_page` 最大值为 500
- 广播统计仅对已发送的广播可用
- 草稿广播没有统计数据
- 广播 ID 是数字整数

### 5. 删除广播

**适用场景**：用户想要永久删除广播

**工具调用顺序**：
1. `KIT_LIST_BROADCASTS` - 找到要删除的广播 [前置步骤]
2. `KIT_GET_BROADCAST` - 验证是否为正确的广播 [可选]
3. `KIT_DELETE_BROADCAST` - 永久删除广播 [必需]

**关键参数**：
- `id`：广播 ID（必需）

**注意事项**：
- 删除是永久性的，无法撤销
- 删除已发送的广播会移除它，但不会撤回已发送的邮件
- 删除前请确认广播 ID

## 常见模式

### 通过邮箱查找订阅者

```
1. 使用 email_address='user@example.com' 调用 KIT_LIST_SUBSCRIBERS
2. 从响应中提取订阅者 ID
3. 使用 ID 进行打标签、取消订阅或其他操作
```

### 分页

Kit 使用基于游标的分页：
- 检查响应中的 `after` 游标值
- 在下一个请求中将游标作为 `after` 参数传递
- 持续执行直到不再返回游标
- 使用 `include_total_count: 'true'` 跟踪进度

### 基于标签的细分

```
1. 在 Kit 网页界面创建标签
2. 使用 KIT_TAG_SUBSCRIBER 为订阅者分配标签
3. 使用 KIT_LIST_TAG_SUBSCRIBERS 查看每个标签下的订阅者
```

## 已知注意事项

**ID 格式**：
- 订阅者 ID：正整数（如 3887204736）
- 标签 ID：正整数
- 广播 ID：正整数
- 所有 ID 都是数字，不是字符串

**状态值**：
- 订阅者状态：'active'、'inactive'、'cancelled'
- 某些操作受状态限制（例如按 cancelled_at 排序需要 status='cancelled'）

**字符串与布尔参数**：
- `include_total_count` 是字符串 'true'，不是布尔值 true
- `sort_order` 是字符串枚举：'asc' 或 'desc'

**速率限制**：
- Kit API 对每个账户有速率限制
- 收到 429 响应时实现退避策略
- 批量操作应适当控制节奏

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 使用防御性解析和回退模式
- 游标值是不透明字符串；按返回值原样使用

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出订阅者 | KIT_LIST_SUBSCRIBERS | status, email_address, per_page |
| 为订阅者打标签 | KIT_TAG_SUBSCRIBER | tag_id, subscriber_id |
| 列出标签订阅者 | KIT_LIST_TAG_SUBSCRIBERS | tag_id |
| 取消订阅 | KIT_DELETE_SUBSCRIBER | id |
| 列出广播 | KIT_LIST_BROADCASTS | per_page, after |
| 获取广播 | KIT_GET_BROADCAST | id |
| 获取广播统计 | KIT_GET_BROADCAST_STATS | id |
| 删除广播 | KIT_DELETE_BROADCAST | id |

## 使用时机
当任务与概述中描述的工作流或操作匹配时，使用此技能。

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
