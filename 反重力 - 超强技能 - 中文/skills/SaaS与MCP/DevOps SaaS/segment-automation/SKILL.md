---
name: segment-automation
description: "通过 Rube MCP（Composio）自动化 Segment 任务：跟踪事件、识别用户、管理分组、页面浏览、别名、批量操作。始终先搜索工具获取当前模式。触发词：Segment、客户数据平台、事件跟踪、用户识别、数据集成、用户分组、批量操作、数据管道"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Segment 自动化

通过 Composio 的 Segment 工具包和 Rube MCP 自动化 Segment 客户数据平台操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 和工具包 `segment` 建立活跃的 Segment 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `segment` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Segment 认证
4. 运行任何工作流前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 跟踪事件

**使用场景**：用户希望向 Segment 发送事件数据以传输到下游目标

**工具序列**：
1. `SEGMENT_TRACK` - 发送单个跟踪事件 [必需]

**关键参数**：
- `userId`：用户标识符（如果没有 `anonymousId` 则必需）
- `anonymousId`：匿名标识符（如果没有 `userId` 则必需）
- `event`：事件名称（例如 'Order Completed'、'Button Clicked'）
- `properties`：包含事件特定属性的对象
- `timestamp`：ISO 8601 时间戳（可选；默认为服务器时间）
- `context`：包含上下文元数据的对象（IP、用户代理等）

**注意事项**：
- 至少需要 `userId` 或 `anonymousId` 之一
- `event` 名称是必需的，应遵循一致的命名规范
- 属性是自由格式对象；确保跨事件的模式一致性
- 时间戳必须是 ISO 8601 格式（例如 '2024-01-15T10:30:00Z'）
- 事件异步处理；成功的 API 响应表示已接受，而非已送达

### 2. 识别用户

**使用场景**：用户希望在 Segment 中将特征与用户档案关联

**工具序列**：
1. `SEGMENT_IDENTIFY` - 设置用户特征和身份 [必需]

**关键参数**：
- `userId`：用户标识符（如果没有 `anonymousId` 则必需）
- `anonymousId`：匿名标识符
- `traits`：包含用户属性的对象（邮箱、姓名、套餐等）
- `timestamp`：ISO 8601 时间戳
- `context`：上下文元数据

**注意事项**：
- 至少需要 `userId` 或 `anonymousId` 之一
- 特征会与现有特征合并，而非替换
- 要移除特征，将其设置为 `null`
- 新用户的识别调用应在跟踪调用之前进行
- 除非目标已配置，否则避免在特征中发送 PII

### 3. 批量操作

**使用场景**：用户希望在单个请求中发送多个事件、识别或其他调用

**工具序列**：
1. `SEGMENT_BATCH` - 在一个请求中发送多个 Segment 调用 [必需]

**关键参数**：
- `batch`：消息对象数组，每个包含：
  - `type`：消息类型（'track'、'identify'、'group'、'page'、'alias'）
  - `userId` / `anonymousId`：用户标识符
  - 基于类型的其他字段（event、properties、traits 等）

**注意事项**：
- 批次中的每个消息必须有有效的 `type` 字段
- 有最大批次大小限制；查看模式获取当前限制
- 批次中的所有消息独立处理；一个失败不影响其他
- 每个消息必须独立满足其类型的要求（例如 track 需要事件名称）
- 批量是发送多个调用的最高效方式；优先于单独调用

### 4. 用户分组

**使用场景**：用户希望将用户与公司、团队或组织关联

**工具序列**：
1. `SEGMENT_GROUP` - 将用户与分组关联 [必需]

**关键参数**：
- `userId`：用户标识符（如果没有 `anonymousId` 则必需）
- `anonymousId`：匿名标识符
- `groupId`：分组/组织标识符（必需）
- `traits`：包含分组属性的对象（名称、行业、规模、套餐）
- `timestamp`：ISO 8601 时间戳

**注意事项**：
- `groupId` 是必需的；它标识公司或组织
- 分组特征会与该分组的现有特征合并
- 一个用户可以属于多个分组
- 分组特征更新分组档案，而非用户档案

### 5. 跟踪页面浏览

**使用场景**：用户希望在 Segment 中记录页面浏览事件

**工具序列**：
1. `SEGMENT_PAGE` - 发送页面浏览事件 [必需]

**关键参数**：
- `userId`：用户标识符（如果没有 `anonymousId` 则必需）
- `anonymousId`：匿名标识符
- `name`：页面名称（例如 'Home'、'Pricing'、'Dashboard'）
- `category`：页面类别（例如 'Docs'、'Marketing'）
- `properties`：包含页面特定属性的对象（url、title、referrer）

**注意事项**：
- 至少需要 `userId` 或 `anonymousId` 之一
- `name` 和 `category` 是可选的，但建议填写以获得正确的分析
- 标准属性包括 `url`、`title`、`referrer`、`path`、`search`
- 页面调用通常是自动化的；手动使用用于服务端页面跟踪

### 6. 用户别名与源管理

**使用场景**：用户希望合并匿名用户和已识别用户，或管理源配置

**工具序列**：
1. `SEGMENT_ALIAS` - 将两个用户身份链接在一起 [可选]
2. `SEGMENT_LIST_SCHEMA_SETTINGS_IN_SOURCE` - 查看源模式设置 [可选]
3. `SEGMENT_UPDATE_SOURCE` - 更新源配置 [可选]

**关键参数**：
- ALIAS：
  - `userId`：新用户标识符（已识别的 ID）
  - `previousId`：旧用户标识符（匿名 ID）
- 源操作：
  - `sourceId`：源标识符

**注意事项**：
- ALIAS 是单向操作；无法撤销
- `previousId` 是匿名/旧 ID，`userId` 是新/已识别 ID
- 并非所有目标都支持别名调用；查看目标文档
- ALIAS 应在用户首次识别时调用一次（例如注册时）
- 源更新可能影响数据收集；仔细审查更改

## 常见模式

### 用户生命周期

标准 Segment 用户生命周期：
```
1. 匿名用户访问 -> 使用 anonymousId 进行 PAGE 调用
2. 用户交互 -> 使用 anonymousId 进行 TRACK 调用
3. 用户注册 -> ALIAS（anonymousId -> userId），然后使用 traits 进行 IDENTIFY
4. 用户执行操作 -> 使用 userId 进行 TRACK 调用
5. 用户加入组织 -> 使用 GROUP 调用将 userId 链接到 groupId
```

### 批量优化

用于批量数据摄取：
```
1. 在内存中收集事件（消息对象数组）
2. 每个消息包含 type、userId/anonymousId 和类型特定字段
3. 使用收集的消息调用 SEGMENT_BATCH
4. 检查响应中的任何单个消息错误
```

### 命名规范

Segment 建议一致的事件命名：
- **事件**：使用"对象 动作"格式（例如 'Order Completed'、'Article Viewed'）
- **属性**：使用 snake_case（例如 'order_total'、'product_name'）
- **特征**：使用 snake_case（例如 'first_name'、'plan_type'）

## 已知注意事项

**身份解析**：
- 每次调用都必须包含 `userId` 或 `anonymousId`
- 每个用户身份合并只使用一次 ALIAS
- 跟踪前先识别以确保正确的用户关联

**数据质量**：
- 事件名称应在所有源中保持一致
- 属性应遵循定义的模式以确保下游兼容性
- 除非目标已配置，否则避免发送敏感 PII

**速率限制**：
- 使用 BATCH 进行批量操作以保持在速率限制内
- 单独调用按源进行速率限制
- 批量调用更高效且更不容易被限流

**响应解析**：
- 成功响应表示已接受，而非已送达目标
- 响应数据可能嵌套在 `data` 键下
- 检查批量响应中的错误字段以发现单个消息失败

**时间戳**：
- 必须是带时区的 ISO 8601 格式（例如 '2024-01-15T10:30:00Z'）
- 省略时间戳将使用服务器接收时间
- 历史数据导入应包含明确的时间戳

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 跟踪事件 | SEGMENT_TRACK | userId, event, properties |
| 识别用户 | SEGMENT_IDENTIFY | userId, traits |
| 批量调用 | SEGMENT_BATCH | batch（消息数组） |
| 用户分组 | SEGMENT_GROUP | userId, groupId, traits |
| 页面浏览 | SEGMENT_PAGE | userId, name, properties |
| 身份别名 | SEGMENT_ALIAS | userId, previousId |
| 源模式 | SEGMENT_LIST_SCHEMA_SETTINGS_IN_SOURCE | sourceId |
| 更新源 | SEGMENT_UPDATE_SOURCE | sourceId |
| 数据仓库 | SEGMENT_LIST_CONNECTED_WAREHOUSES_FROM_SOURCE | sourceId |

## 使用场景
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。