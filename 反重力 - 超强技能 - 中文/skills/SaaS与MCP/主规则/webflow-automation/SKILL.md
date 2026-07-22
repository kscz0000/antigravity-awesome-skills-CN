---
name: webflow-automation
description: "通过 Rube MCP（Composio）自动化 Webflow 的 CMS 集合、站点发布、页面管理、资源上传和电商订单。始终先搜索工具以获取最新架构。触发词：webflow、webflow 自动化、webflow cms、webflow 站点发布、webflow 页面管理、webflow 资源上传、webflow 电商订单、rube mcp、composio"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Webflow

通过 Composio 的 Webflow 工具包，自动化 Webflow 的 CMS 集合管理、站点发布、页面检查、资源上传以及电商订单获取等操作。

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `webflow` 工具包建立有效的 Webflow 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 配置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用 `webflow` 工具包调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成 Webflow OAuth
4. 在运行任何工作流前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 管理 CMS 集合项

**使用场景**：用户希望在 Webflow CMS 集合中创建、更新、列出或删除条目（博客文章、产品、团队成员等）

**工具调用顺序**：
1. `WEBFLOW_LIST_WEBFLOW_SITES` - 列出站点以查找目标 site_id [前置条件]
2. `WEBFLOW_LIST_COLLECTIONS` - 列出该站点的所有集合 [前置条件]
3. `WEBFLOW_GET_COLLECTION` - 获取集合架构以查找有效的字段 slug [创建/更新的前置条件]
4. `WEBFLOW_LIST_COLLECTION_ITEMS` - 列出已有条目，支持筛选和分页 [可选]
5. `WEBFLOW_GET_COLLECTION_ITEM` - 获取特定条目的完整详情 [可选]
6. `WEBFLOW_CREATE_COLLECTION_ITEM` - 使用字段数据创建新条目 [创建必需]
7. `WEBFLOW_UPDATE_COLLECTION_ITEM` - 更新已有条目的字段 [更新必需]
8. `WEBFLOW_DELETE_COLLECTION_ITEM` - 永久删除条目 [可选]
9. `WEBFLOW_PUBLISH_SITE` - 发布变更以使其生效 [可选]

**CREATE_COLLECTION_ITEM 的关键参数**：
- `collection_id`：来自 LIST_COLLECTIONS 的 24 字符十六进制字符串
- `field_data`：以字段 slug 为键的对象（而非显示名称）；必须包含 `name` 和 `slug`
- `field_data.name`：条目的显示名称
- `field_data.slug`：URL 友好的标识符（小写字母、连字符、无空格）
- `is_draft`：布尔值，是否以草稿形式创建（默认 false）

**UPDATE_COLLECTION_ITEM 的关键参数**：
- `collection_id`：集合标识符
- `item_id`：已有条目的 24 字符十六进制 MongoDB ObjectId
- `fields`：以字段 slug 为键并包含新值的对象
- `live`：布尔值，是否立即发布变更（默认 false）

**字段值类型**：
- 文本/邮箱/链接/日期：string
- 数字：integer 或 float
- 布尔：true/false
- 图片：`{"url": "...", "alt": "...", "fileId": "..."}`
- 多重引用：引用 ID 字符串数组
- 多重图片：图片对象数组
- 选项：option ID 字符串

**常见陷阱**：
- 字段键必须使用集合架构中的确切字段 `slug`，而非显示名称
- 始终先调用 `GET_COLLECTION` 获取架构并识别正确的字段 slug
- `CREATE_COLLECTION_ITEM` 要求 `field_data` 中必须包含 `name` 和 `slug`
- `UPDATE_COLLECTION_ITEM` 无法创建新条目；它要求一个有效的已有 `item_id`
- `item_id` 必须是 24 字符的十六进制 MongoDB ObjectId
- Slug 必须是小写字母数字加连字符：`^[a-z0-9]+(?:-[a-z0-9]+)*$`
- CMS 条目是分阶段的；使用 `PUBLISH_SITE` 或设置 `live: true` 以推送到生产环境

### 2. 管理站点和发布

**使用场景**：用户希望列出站点、检查站点配置或发布阶段性变更

**工具调用顺序**：
1. `WEBFLOW_LIST_WEBFLOW_SITES` - 列出所有可访问的站点 [必需]
2. `WEBFLOW_GET_SITE_INFO` - 获取详细的站点元数据，包括域名和设置 [可选]
3. `WEBFLOW_PUBLISH_SITE` - 将所有阶段性变更部署到线上站点 [发布必需]

**PUBLISH_SITE 的关键参数**：
- `site_id`：来自 LIST_WEBFLOW_SITES 的站点标识符
- `custom_domains`：自定义域名 ID 字符串数组（来自 GET_SITE_INFO）
- `publish_to_webflow_subdomain`：布尔值，是否发布到 `{shortName}.webflow.io`
- 必须指定 `custom_domains` 或 `publish_to_webflow_subdomain` 中的至少一个

**常见陷阱**：
- `PUBLISH_SITE` 会重新发布所选域名的所有阶段性变更 — 需确认没有意外未发布的草稿
- 速率限制：每分钟只能成功发布 1 次
- 对于没有自定义域名的站点，必须设置 `publish_to_webflow_subdomain: true`
- `custom_domains` 接受的是域名 ID（十六进制字符串），而非域名
- 发布属于生产操作 — 务必先与用户确认

### 3. 管理页面

**使用场景**：用户希望列出页面、检查页面元数据或查看页面 DOM 结构

**工具调用顺序**：
1. `WEBFLOW_LIST_WEBFLOW_SITES` - 查找目标 site_id [前置条件]
2. `WEBFLOW_LIST_PAGES` - 列出站点的所有页面，支持分页 [必需]
3. `WEBFLOW_GET_PAGE` - 获取特定页面的详细元数据 [可选]
4. `WEBFLOW_GET_PAGE_DOM` - 获取静态页面的 DOM/内容节点结构 [可选]

**关键参数**：
- `site_id`：站点标识符（列出页面时必需）
- `page_id`：24 字符的十六进制页面标识符
- `locale_id`：多语言站点的可选语言环境筛选
- `limit`：每页最大结果数（最大 100）
- `offset`：分页偏移量

**常见陷阱**：
- `LIST_PAGES` 通过 offset/limit 进行分页；当站点页面较多时需迭代
- 页面 ID 是 24 字符的十六进制字符串，匹配模式 `^[0-9a-fA-F]{24}$`
- `GET_PAGE_DOM` 返回节点结构，而非渲染后的 HTML
- 页面包括静态页面和 CMS 驱动的页面

### 4. 上传资源

**使用场景**：用户希望将图片、文件或其他资源上传到 Webflow 站点

**工具调用顺序**：
1. `WEBFLOW_LIST_WEBFLOW_SITES` - 查找目标 site_id [前置条件]
2. `WEBFLOW_UPLOAD_ASSET` - 使用 base64 编码内容上传文件 [必需]

**关键参数**：
- `site_id`：站点标识符
- `file_name`：文件名称（例如 `"logo.png"`）
- `file_content`：文件的 base64 编码二进制内容（不是占位符或 URL）
- `content_type`：MIME 类型（例如 `"image/png"`、`"image/jpeg"`、`"application/pdf"`）
- `md5`：原始文件字节的 MD5 哈希值（32 字符的十六进制字符串）
- `asset_folder_id`：可选的文件夹归属

**常见陷阱**：
- `file_content` 必须是实际的 base64 编码数据，而非变量引用或占位符
- `md5` 必须从原始字节计算，而不是从 base64 字符串计算
- 内部是两步流程：先生成 S3 预签名 URL，然后上传
- 大文件可能遇到超时；上传内容应保持合理大小

### 5. 管理电商订单

**使用场景**：用户希望查看 Webflow 站点的电商订单

**工具调用顺序**：
1. `WEBFLOW_LIST_WEBFLOW_SITES` - 查找已启用电商的站点 [前置条件]
2. `WEBFLOW_LIST_ORDERS` - 列出所有订单，可按状态筛选 [必需]
3. `WEBFLOW_GET_ORDER` - 获取特定订单的详细信息 [可选]

**关键参数**：
- `site_id`：站点标识符（必须已启用电商）
- `order_id`：用于获取详细信息的特定订单标识符
- `status`：按状态筛选订单

**常见陷阱**：
- 必须在 Webflow 站点上启用电商，订单相关接口才能正常工作
- 订单接口为只读；通过这些工具不能创建/更新/删除订单

## 通用模式

### ID 解析
Webflow 始终使用 24 字符的十六进制 ID：
- **站点 ID**：`WEBFLOW_LIST_WEBFLOW_SITES` — 通过名称查找，获取 `id`
- **集合 ID**：使用 `site_id` 调用 `WEBFLOW_LIST_COLLECTIONS`
- **条目 ID**：使用 `collection_id` 调用 `WEBFLOW_LIST_COLLECTION_ITEMS`
- **页面 ID**：使用 `site_id` 调用 `WEBFLOW_LIST_PAGES`
- **域名 ID**：`WEBFLOW_GET_SITE_INFO` — 位于 `customDomains` 数组
- **字段 slug**：`WEBFLOW_GET_COLLECTION` — 位于集合的 `fields` 数组

### 分页
Webflow 使用基于 offset 的分页：
- `offset`：起始索引（从 0 开始）
- `limit`：每页条目数（最大 100）
- 持续按 limit 增加 offset，直到返回结果数少于 limit
- 适用于：LIST_COLLECTION_ITEMS、LIST_PAGES

### CMS 工作流
典型的 CMS 内容创建流程：
1. 从 LIST_WEBFLOW_SITES 获取 site_id
2. 从 LIST_COLLECTIONS 获取 collection_id
3. 从 GET_COLLECTION 获取字段架构（以了解字段 slug）
4. 使用正确的字段 slug 创建/更新条目
5. 发布站点以使变更生效

## 已知陷阱

### ID 格式
- 所有 Webflow ID 都是 24 字符的十六进制字符串（MongoDB ObjectId）
- 示例：`580e63fc8c9a982ac9b8b745`
- 模式：`^[0-9a-fA-F]{24}$`
- 无效的 ID 会返回 404 错误

### 字段 slug 与显示名称
- CMS 操作要求使用字段 `slug` 值，而非显示名称
- 显示名称为 "Author Name" 的字段，其 slug 可能为 `author-name`
- 始终调用 `GET_COLLECTION` 来发现正确的字段 slug
- 使用错误的字段名会静默忽略数据或导致验证错误

### 发布
- `PUBLISH_SITE` 会部署所有阶段性变更，而不仅仅是特定条目
- 速率限制为每分钟 1 次发布
- 必须指定至少一个域名目标（自定义域名或 webflow 子域名）
- 这是会影响生产的操作；务必确认意图

### 认证范围
- 不同操作需要不同的 OAuth 范围：`sites:read`、`cms:read`、`cms:write`、`pages:read`
- 403 错误通常表示缺少 OAuth 范围
- 如果操作因授权错误而失败，请检查连接权限

### 破坏性操作
- `DELETE_COLLECTION_ITEM` 会永久删除 CMS 条目
- `PUBLISH_SITE` 会立即使所有阶段性变更生效
- 在执行这些操作前务必与用户确认

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|------------|
| 列出站点 | `WEBFLOW_LIST_WEBFLOW_SITES` | （无） |
| 获取站点信息 | `WEBFLOW_GET_SITE_INFO` | `site_id` |
| 发布站点 | `WEBFLOW_PUBLISH_SITE` | `site_id`、`custom_domains` 或 `publish_to_webflow_subdomain` |
| 列出集合 | `WEBFLOW_LIST_COLLECTIONS` | `site_id` |
| 获取集合架构 | `WEBFLOW_GET_COLLECTION` | `collection_id` |
| 列出集合条目 | `WEBFLOW_LIST_COLLECTION_ITEMS` | `collection_id`、`limit`、`offset` |
| 获取集合条目 | `WEBFLOW_GET_COLLECTION_ITEM` | `collection_id`、`item_id` |
| 创建集合条目 | `WEBFLOW_CREATE_COLLECTION_ITEM` | `collection_id`、`field_data` |
| 更新集合条目 | `WEBFLOW_UPDATE_COLLECTION_ITEM` | `collection_id`、`item_id`、`fields` |
| 删除集合条目 | `WEBFLOW_DELETE_COLLECTION_ITEM` | `collection_id`、`item_id` |
| 列出页面 | `WEBFLOW_LIST_PAGES` | `site_id`、`limit`、`offset` |
| 获取页面 | `WEBFLOW_GET_PAGE` | `page_id` |
| 获取页面 DOM | `WEBFLOW_GET_PAGE_DOM` | `page_id` |
| 上传资源 | `WEBFLOW_UPLOAD_ASSET` | `site_id`、`file_name`、`file_content`、`content_type`、`md5` |
| 列出订单 | `WEBFLOW_LIST_ORDERS` | `site_id`、`status` |
| 获取订单 | `WEBFLOW_GET_ORDER` | `site_id`、`order_id` |

## 使用时机
此技能适用于执行上述概览中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将此技能的输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
