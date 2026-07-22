---
name: one-drive-automation
description: "通过 Rube MCP (Composio) 自动化 OneDrive 文件管理、搜索、上传、下载、共享、权限和文件夹操作。始终先搜索工具获取最新 schema。当用户要求'OneDrive 自动化'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 OneDrive 自动化

通过 Composio 的 OneDrive 工具包自动化 OneDrive 操作，包括文件上传/下载、搜索、文件夹管理、共享链接、权限管理和云盘浏览。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `one_drive` 工具包建立活跃的 OneDrive 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 使用 `one_drive` 工具包调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Microsoft OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 搜索和浏览文件

**适用场景**：用户想要在 OneDrive 中查找文件或浏览文件夹内容

**工具调用顺序**：
1. `ONE_DRIVE_GET_DRIVE` - 验证云盘访问并获取云盘详情 [前置条件]
2. `ONE_DRIVE_SEARCH_ITEMS` - 跨文件名、元数据和内容的关键词搜索 [必需]
3. `ONE_DRIVE_ONEDRIVE_LIST_ITEMS` - 列出云盘根目录中的所有条目 [可选]
4. `ONE_DRIVE_GET_ITEM` - 获取特定条目的详细元数据，展开子条目 [可选]
5. `ONE_DRIVE_ONEDRIVE_FIND_FILE` - 通过精确名称在文件夹中查找特定文件 [可选]
6. `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` - 通过名称查找特定文件夹 [可选]
7. `ONE_DRIVE_LIST_DRIVES` - 列出所有可访问的云盘 [可选]

**关键参数**：
- `q`：搜索查询（仅支持纯关键词，不支持 KQL 语法）
- `search_scope`：`"root"`（文件夹层级）或 `"drive"`（包含共享条目）
- `top`：每页最大条目数（默认 200）
- `skip_token`：来自 `@odata.nextLink` 的分页令牌
- `select`：逗号分隔的返回字段（如 `"id,name,webUrl,size"`）
- `orderby`：排序方式（如 `"name asc"`、`"name desc"`）
- `item_id`：`GET_ITEM` 的条目 ID
- `expand_relations`：`GET_ITEM` 的展开关系数组，如 `["children"]` 或 `["thumbnails"]`
- `user_id`：`"me"`（默认）或特定用户 ID/邮箱

**注意事项**：
- `ONE_DRIVE_SEARCH_ITEMS` 不支持 KQL 操作符（`folder:`、`file:`、`filetype:`、`path:`）；这些会被当作纯文本处理
- 通配符（`*`、`?`）不支持且会被自动移除；改用文件扩展名关键词（如 `"pdf"` 而非 `"*.pdf"`）
- `ONE_DRIVE_ONEDRIVE_LIST_ITEMS` 仅返回根目录内容；使用递归 `ONE_DRIVE_GET_ITEM` 配合 `expand_relations: ["children"]` 获取更深层级
- 大型文件夹会分页；始终跟踪 `skip_token` / `@odata.nextLink` 直到没有更多页面
- 某些云盘 ID 格式可能因 Microsoft Graph API 限制返回 "ObjectHandle is Invalid" 错误

### 2. 上传和下载文件

**适用场景**：用户想要向 OneDrive 上传文件或从 OneDrive 下载文件

**工具调用顺序**：
1. `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` - 定位目标文件夹 [前置条件]
2. `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` - 上传文件到指定文件夹 [上传必需]
3. `ONE_DRIVE_DOWNLOAD_FILE` - 通过条目 ID 下载文件 [下载必需]
4. `ONE_DRIVE_GET_ITEM` - 下载前获取文件详情 [可选]

**关键参数**：
- `file`：FileUploadable 对象，包含 `s3key`、`mimetype` 和 `name` 用于上传
- `folder`：目标路径（如 `"/Documents/Reports"`）或文件夹 ID 用于上传
- `item_id`：文件的唯一标识符用于下载
- `file_name`：带扩展名的期望文件名用于下载
- `drive_id`：特定云盘 ID（用于 SharePoint 或 OneDrive for Business）
- `user_id`：`"me"`（默认）或特定用户标识符

**注意事项**：
- 上传时冲突自动重命名（默认无覆盖选项）
- 大文件自动通过分块处理
- 同时提供 `drive_id` 和 `user_id` 时，`drive_id` 优先
- 条目 ID 因平台而异：OneDrive for Business 使用 `01...` 前缀，OneDrive Personal 使用 `HASH!NUMBER` 格式
- 条目 ID 区分大小写；请使用 API 返回的原始值

### 3. 共享文件和管理权限

**适用场景**：用户想要共享文件/文件夹或管理访问权限

**工具调用顺序**：
1. `ONE_DRIVE_ONEDRIVE_FIND_FILE` 或 `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` - 定位条目 [前置条件]
2. `ONE_DRIVE_GET_ITEM_PERMISSIONS` - 检查当前权限 [前置条件]
3. `ONE_DRIVE_INVITE_USER_TO_DRIVE_ITEM` - 授予特定用户访问权限 [必需]
4. `ONE_DRIVE_CREATE_LINK` - 创建可共享链接 [可选]
5. `ONE_DRIVE_UPDATE_DRIVE_ITEM_METADATA` - 更新条目元数据 [可选]

**关键参数**：
- `item_id`：要共享的文件或文件夹
- `recipients`：包含 `email` 或 `object_id` 的对象数组
- `roles`：包含 `"read"` 或 `"write"` 的数组
- `send_invitation`：`true` 发送通知邮件，`false` 静默授权
- `require_sign_in`：`true` 要求认证才能访问
- `message`：邀请的自定义消息（最多 2000 字符）
- `expiration_date_time`：ISO 8601 格式的权限过期日期
- `retain_inherited_permissions`：`true`（默认）保留现有的继承权限

**注意事项**：
- 在 `INVITE_USER_TO_DRIVE_ITEM` 中使用错误的 `item_id` 会更改非目标条目的权限；务必先验证
- 写入或更高权限影响重大；授予前需获得用户明确确认
- `GET_ITEM_PERMISSIONS` 返回继承和所有者条目；不要假设响应仅反映最近的变更
- `permissions` 无法通过 `ONE_DRIVE_GET_ITEM` 展开；需使用独立的权限端点
- `require_sign_in` 和 `send_invitation` 至少有一个必须为 `true`

### 4. 管理文件夹（创建、移动、删除、复制）

**适用场景**：用户想要创建、移动、重命名、删除或复制文件和文件夹

**工具调用顺序**：
1. `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` - 定位源文件夹和目标文件夹 [前置条件]
2. `ONE_DRIVE_ONEDRIVE_CREATE_FOLDER` - 创建新文件夹 [创建必需]
3. `ONE_DRIVE_MOVE_ITEM` - 移动文件或文件夹到新位置 [移动必需]
4. `ONE_DRIVE_COPY_ITEM` - 复制文件或文件夹（异步操作）[复制必需]
5. `ONE_DRIVE_DELETE_ITEM` - 将条目移至回收站 [删除必需]
6. `ONE_DRIVE_UPDATE_DRIVE_ITEM_METADATA` - 重命名或更新条目属性 [可选]

**关键参数**：
- `name`：创建时的文件夹名称或重命名/复制时的新名称
- `parent_folder`：路径（如 `"/Documents/Reports"`）或创建时的文件夹 ID
- `itemId`：要移动的条目
- `parentReference`：包含 `id`（目标文件夹 ID）的对象用于移动：`{"id": "folder_id"}`
- `item_id`：要复制或删除的条目
- `parent_reference`：包含 `id` 和可选 `driveId` 的对象用于复制目标
- `@microsoft.graph.conflictBehavior`：复制时的冲突行为，`"fail"`、`"replace"` 或 `"rename"`
- `if_match`：删除时的乐观并发 ETag

**注意事项**：
- `ONE_DRIVE_MOVE_ITEM` 不支持跨云盘移动；跨云盘传输请使用 `ONE_DRIVE_COPY_ITEM`
- 移动的 `parentReference` 需要文件夹 ID（非文件夹名称）；先用 `ONEDRIVE_FIND_FOLDER` 解析
- `ONE_DRIVE_COPY_ITEM` 是异步操作；响应提供监控进度的 URL
- `ONE_DRIVE_DELETE_ITEM` 移至回收站，非永久删除
- 文件夹创建时冲突自动重命名（如 "New Folder" 变为 "New Folder 1"）
- `ONE_DRIVE_COPY_ITEM` 需提供 `name` 或 `parent_reference`（或两者）

### 5. 跟踪变更和云盘信息

**适用场景**：用户想要监控变更或获取云盘/配额信息

**工具调用顺序**：
1. `ONE_DRIVE_GET_DRIVE` - 获取云盘属性和元数据 [必需]
2. `ONE_DRIVE_GET_QUOTA` - 检查存储配额（总量、已用、剩余）[可选]
3. `ONE_DRIVE_LIST_SITE_DRIVE_ITEMS_DELTA` - 跟踪 SharePoint 站点云盘的变更 [可选]
4. `ONE_DRIVE_GET_ITEM_VERSIONS` - 获取文件的版本历史 [可选]

**关键参数**：
- `drive_id`：云盘标识符（或 `"me"` 表示个人云盘）
- `site_id`：SharePoint 站点标识符用于增量跟踪
- `token`：增量令牌（`"latest"` 获取当前状态，URL 获取下一页，或时间戳）
- `item_id`：版本历史的文件 ID

**注意事项**：
- 增量查询仅适用于 SharePoint 站点云盘，通过 `ONE_DRIVE_LIST_SITE_DRIVE_ITEMS_DELTA`
- 令牌 `"latest"` 返回当前增量令牌但不含条目（可用作起始点）
- 深层或大型云盘可能需要数分钟遍历；使用分批和恢复逻辑

## 常见模式

### ID 解析
- **用户**：使用 `"me"` 表示已认证用户，或特定用户邮箱/GUID
- **从查找获取条目 ID**：使用 `ONE_DRIVE_ONEDRIVE_FIND_FILE` 或 `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` 获取条目 ID
- **从搜索获取条目 ID**：从 `ONE_DRIVE_SEARCH_ITEMS` 结果中提取
- **云盘 ID**：使用 `ONE_DRIVE_LIST_DRIVES` 或 `ONE_DRIVE_GET_DRIVE` 发现云盘
- **文件夹路径转 ID**：使用 `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` 配合路径，然后从响应中提取 ID

ID 格式因平台而异：
- OneDrive for Business/SharePoint：`01NKDM7HMOJTVYMDOSXFDK2QJDXCDI3WUK`
- OneDrive Personal：`D4648F06C91D9D3D!54927`

### 分页
OneDrive 使用基于令牌的分页：
- 跟踪 `@odata.nextLink` 或 `skip_token` 直到没有更多页面
- 设置 `top` 控制页面大小（因端点而异）
- `ONE_DRIVE_ONEDRIVE_LIST_ITEMS` 内部自动处理分页
- 激进的并行请求可能触发 HTTP 429；遵守 `Retry-After` 头

### 路径 vs ID
大多数 OneDrive 工具接受路径或 ID：
- **路径**：以 `/` 开头（如 `"/Documents/Reports"`）
- **ID**：使用 API 响应中的唯一条目标识符
- **权限的条目路径**：使用 `:/path/to/item:/` 格式

## 已知陷阱

### ID 格式
- 条目 ID 区分大小写且因平台而异
- 不要将网页 URL、共享链接或手动构造的标识符用作条目 ID
- 始终使用 Microsoft Graph API 返回的原始 ID

### 速率限制
- 激进的并行 `ONE_DRIVE_GET_ITEM` 调用可能触发 HTTP 429 Too Many Requests
- 遵守 `Retry-After` 头并实施节流
- 深层云盘遍历应使用分批和延迟

### 搜索限制
- 不支持 KQL；仅使用纯关键词
- 不支持通配符；使用扩展名关键词（如 `"pdf"` 而非 `"*.pdf"`）
- 搜索中不支持基于路径的过滤；改用文件夹列表
- `q='*'` 仅通配符查询返回 HTTP 400 invalidRequest

### 参数注意事项
- 同时提供 `drive_id` 和 `user_id` 时，`drive_id` 优先
- `permissions` 无法通过 `GET_ITEM` 展开；使用专用权限端点
- 移动操作在 `parentReference` 中需要文件夹 ID，而非文件夹名称
- 复制操作是异步的；响应提供监控 URL

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索文件 | `ONE_DRIVE_SEARCH_ITEMS` | `q`, `search_scope`, `top` |
| 列出根目录条目 | `ONE_DRIVE_ONEDRIVE_LIST_ITEMS` | `user_id`, `select`, `top` |
| 获取条目详情 | `ONE_DRIVE_GET_ITEM` | `item_id`, `expand_relations` |
| 按名称查找文件 | `ONE_DRIVE_ONEDRIVE_FIND_FILE` | `name`, `folder` |
| 按名称查找文件夹 | `ONE_DRIVE_ONEDRIVE_FIND_FOLDER` | `name`, `folder` |
| 上传文件 | `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` | `file`, `folder` |
| 下载文件 | `ONE_DRIVE_DOWNLOAD_FILE` | `item_id`, `file_name` |
| 创建文件夹 | `ONE_DRIVE_ONEDRIVE_CREATE_FOLDER` | `name`, `parent_folder` |
| 移动条目 | `ONE_DRIVE_MOVE_ITEM` | `itemId`, `parentReference` |
| 复制条目 | `ONE_DRIVE_COPY_ITEM` | `item_id`, `parent_reference`, `name` |
| 删除条目 | `ONE_DRIVE_DELETE_ITEM` | `item_id` |
| 共享给用户 | `ONE_DRIVE_INVITE_USER_TO_DRIVE_ITEM` | `item_id`, `recipients`, `roles` |
| 创建共享链接 | `ONE_DRIVE_CREATE_LINK` | `item_id`, link type |
| 获取权限 | `ONE_DRIVE_GET_ITEM_PERMISSIONS` | `item_id` |
| 更新元数据 | `ONE_DRIVE_UPDATE_DRIVE_ITEM_METADATA` | `item_id`, fields |
| 获取云盘信息 | `ONE_DRIVE_GET_DRIVE` | `drive_id` |
| 列出云盘 | `ONE_DRIVE_LIST_DRIVES` | user/group/site scope |
| 获取配额 | `ONE_DRIVE_GET_QUOTA` | (none) |
| 跟踪变更 | `ONE_DRIVE_LIST_SITE_DRIVE_ITEMS_DELTA` | `site_id`, `token` |
| 版本历史 | `ONE_DRIVE_GET_ITEM_VERSIONS` | `item_id` |

## 适用场景
此技能适用于执行概述中描述的工作流或操作。

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来要求澄清。
