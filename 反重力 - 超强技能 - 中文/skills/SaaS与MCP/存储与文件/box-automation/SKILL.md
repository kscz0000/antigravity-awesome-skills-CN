---
name: box-automation
description: "通过 Composio 的 Box 工具包自动化 Box 操作，包括文件上传/下载、内容搜索、文件夹管理、协作管理、元数据查询和签名请求。当用户要求'Box自动化'、'Box文件操作'、'Box上传下载'、'Box搜索'、'Box文件夹管理'、'Box协作'、'Box签名请求'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Box 自动化

通过 Composio 的 Box 工具包自动化 Box 操作，包括文件上传/下载、内容搜索、文件夹管理、协作管理、元数据查询和签名请求。

## 前提条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Box 连接，toolkit 设为 `box`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 响应正常，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `box`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Box OAuth
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 上传和下载文件

**适用场景**：用户想要上传文件到 Box 或从 Box 下载文件

**工具调用顺序**：
1. `BOX_SEARCH_FOR_CONTENT` - 路径未知时查找目标文件夹 [前置条件]
2. `BOX_GET_FOLDER_INFORMATION` - 验证文件夹存在并获取 folder_id [前置条件]
3. `BOX_LIST_ITEMS_IN_FOLDER` - 浏览文件夹内容，发现文件 ID [可选]
4. `BOX_UPLOAD_FILE` - 上传文件到指定文件夹 [上传必需]
5. `BOX_DOWNLOAD_FILE` - 按 file_id 下载文件 [下载必需]
6. `BOX_CREATE_ZIP_DOWNLOAD` - 将多个文件/文件夹打包为 zip [可选]

**关键参数**：
- `parent_id`：上传目标文件夹 ID（根文件夹使用 `"0"`）
- `file`：FileUploadable 对象，包含 `s3key`、`mimetype` 和 `name`
- `file_id`：下载文件的唯一标识符
- `version`：可选，下载特定版本时使用的文件版本 ID
- `fields`：逗号分隔的返回属性列表

**注意事项**：
- 上传到已存在同名文件的文件夹可能触发冲突行为；需明确覆盖还是重命名
- 超过 50MB 的文件应使用分块上传 API（标准工具不支持）
- 上传时 `attributes` 部分必须位于 `file` 部分之前，否则会返回 HTTP 400 错误 `metadata_after_file_contents`
- 文件 ID 和文件夹 ID 是数字字符串，可从 Box 网页端 URL 中提取（如 `https://*.app.box.com/files/123` 对应 file_id `"123"`）

### 2. 搜索和浏览内容

**适用场景**：用户想要按名称、内容或元数据查找文件、文件夹或网页链接

**工具调用顺序**：
1. `BOX_SEARCH_FOR_CONTENT` - 对文件、文件夹和网页链接进行全文搜索 [必需]
2. `BOX_LIST_ITEMS_IN_FOLDER` - 浏览指定文件夹内容 [可选]
3. `BOX_GET_FILE_INFORMATION` - 获取指定文件的详细元数据 [可选]
4. `BOX_GET_FOLDER_INFORMATION` - 获取指定文件夹的详细元数据 [可选]
5. `BOX_QUERY_FILES_FOLDERS_BY_METADATA` - 按元数据模板值搜索 [可选]
6. `BOX_LIST_RECENTLY_ACCESSED_ITEMS` - 列出最近访问的项目 [可选]

**关键参数**：
- `query`：搜索字符串，支持运算符（`""` 精确匹配，`AND`、`OR`、`NOT` - 必须大写）
- `type`：按 `"file"`、`"folder"` 或 `"web_link"` 过滤
- `ancestor_folder_ids`：限定搜索范围到指定文件夹（逗号分隔的 ID）
- `file_extensions`：按文件类型过滤（逗号分隔，不含点号）
- `content_types`：搜索范围：`"name"`、`"description"`、`"file_content"`、`"comments"`、`"tags"`
- `created_at_range` / `updated_at_range`：日期过滤，逗号分隔的 RFC3339 时间戳
- `limit`：每页结果数（默认 30）
- `offset`：分页偏移量（最大 10000）
- `folder_id`：用于 `LIST_ITEMS_IN_FOLDER`（根文件夹使用 `"0"`）

**注意事项**：
- offset 超过 10000 的查询会被 HTTP 400 拒绝
- `BOX_SEARCH_FOR_CONTENT` 必须提供 `query` 或 `mdfilters` 参数之一
- 过滤条件配置错误可能静默遗漏预期结果；先用小范围测试查询验证
- 布尔运算符（`AND`、`OR`、`NOT`）必须大写
- `BOX_LIST_ITEMS_IN_FOLDER` 需通过 `marker` 或 `offset`/`usemarker` 分页；部分列表很常见
- 标准文件夹按类型排序（文件夹优先于文件优先于网页链接）

### 3. 管理文件夹

**适用场景**：用户想要创建、更新、移动、复制或删除文件夹

**工具调用顺序**：
1. `BOX_GET_FOLDER_INFORMATION` - 验证文件夹存在并检查权限 [前置条件]
2. `BOX_CREATE_FOLDER` - 创建新文件夹 [创建必需]
3. `BOX_UPDATE_FOLDER` - 重命名、移动或更新文件夹设置 [更新必需]
4. `BOX_COPY_FOLDER` - 将文件夹复制到新位置 [可选]
5. `BOX_DELETE_FOLDER` - 将文件夹移至回收站 [删除必需]
6. `BOX_PERMANENTLY_REMOVE_FOLDER` - 永久删除已回收的文件夹 [可选]

**关键参数**：
- `name`：文件夹名称（不允许 `/`、`\`、尾部空格或 `.`/`..`）
- `parent__id`：父文件夹 ID（根文件夹使用 `"0"`）
- `folder_id`：操作目标文件夹 ID
- `parent.id`：通过 `BOX_UPDATE_FOLDER` 移动时的目标文件夹 ID
- `recursive`：设为 `true` 可删除非空文件夹
- `shared_link`：包含 `access`、`password`、`permissions` 的对象，用于创建文件夹共享链接
- `description`、`tags`：可选元数据字段

**注意事项**：
- `BOX_DELETE_FOLDER` 默认移至回收站；永久删除需使用 `BOX_PERMANENTLY_REMOVE_FOLDER`
- 非空文件夹需设置 `recursive: true` 才能删除
- 根文件夹（ID `"0"`）无法复制或删除
- 文件夹名称不能包含 `/`、`\`、不可打印 ASCII 字符或尾部空格
- 移动文件夹需通过 `BOX_UPDATE_FOLDER` 设置 `parent.id`

### 4. 共享文件和管理协作

**适用场景**：用户想要共享文件、管理访问权限或处理协作关系

**工具调用顺序**：
1. `BOX_GET_FILE_INFORMATION` - 获取文件详情和当前共享状态 [前置条件]
2. `BOX_LIST_FILE_COLLABORATIONS` - 列出有权访问文件的用户 [必需]
3. `BOX_UPDATE_COLLABORATION` - 更改访问级别或接受/拒绝邀请 [必需]
4. `BOX_GET_COLLABORATION` - 获取指定协作的详情 [可选]
5. `BOX_UPDATE_FILE` - 创建共享链接、锁定文件或更新权限 [可选]
6. `BOX_UPDATE_FOLDER` - 为文件夹创建共享链接 [可选]

**关键参数**：
- `collaboration_id`：唯一协作标识符
- `role`：访问级别（`"editor"`、`"viewer"`、`"co-owner"`、`"owner"`、`"previewer"`、`"uploader"`、`"viewer uploader"`、`"previewer uploader"`）
- `status`：协作邀请状态：`"accepted"`、`"pending"` 或 `"rejected"`
- `file_id`：要共享或管理的文件
- `lock__access`：设为 `"lock"` 可锁定文件
- `permissions__can__download`：下载权限设为 `"company"` 或 `"open"`

**注意事项**：
- 仅特定角色可邀请协作者；权限不足会导致授权错误
- `can_view_path` 会增加被邀请者"所有文件"页面的加载时间；每用户限制 1000 个
- 协作过期功能需要企业管理员启用相应设置
- 嵌套参数名使用双下划线表示（如 `lock__access`、`parent__id`）

### 5. Box 签名请求

**适用场景**：用户想要管理文档签名请求

**工具调用顺序**：
1. `BOX_LIST_BOX_SIGN_REQUESTS` - 列出所有签名请求 [必需]
2. `BOX_GET_BOX_SIGN_REQUEST_BY_ID` - 获取指定签名请求的详情 [可选]
3. `BOX_CANCEL_BOX_SIGN_REQUEST` - 取消待处理的签名请求 [可选]

**关键参数**：
- `sign_request_id`：签名请求的 UUID
- `shared_requests`：设为 `true` 可包含用户作为协作者（非所有者）的请求
- `senders`：按发件人邮箱过滤（需 `shared_requests: true`）
- `limit` / `marker`：分页参数

**注意事项**：
- 需要企业账户启用 Box Sign 功能
- 签名文件或父文件夹被删除后，请求不会出现在列表中
- 仅创建者可取消签名请求
- 签名请求状态包括：`converting`、`created`、`sent`、`viewed`、`signed`、`declined`、`cancelled`、`expired`、`error_converting`、`error_sending`

## 常用模式

### ID 解析
Box 对所有实体使用数字字符串 ID：
- **根文件夹**：始终为 ID `"0"`
- **从 URL 获取文件 ID**：`https://*.app.box.com/files/123` 对应 file_id `"123"`
- **从 URL 获取文件夹 ID**：`https://*.app.box.com/folder/123` 对应 folder_id `"123"`
- **搜索转 ID**：使用 `BOX_SEARCH_FOR_CONTENT` 查找项目，然后从结果中提取 ID
- **ETag**：使用 `if_match` 配合文件的 ETag 实现安全的并发删除操作

### 分页
Box 支持两种分页方式：
- **偏移量分页**：使用 `offset` + `limit`（最大偏移量 10000）
- **标记分页**：设置 `usemarker: true` 并跟踪响应中的 `marker`（大数据集首选）
- 始终分页至完成，避免部分结果

### 嵌套参数
Box 工具使用双下划线表示嵌套对象：
- `parent__id` 表示父文件夹引用
- `lock__access`、`lock__expires__at`、`lock__is__download__prevented` 表示文件锁定
- `permissions__can__download` 表示下载权限

## 已知注意事项

### ID 格式
- 所有 ID 都是数字字符串（如 `"123456"`，不是整数）
- 根文件夹始终为 `"0"`
- 文件和文件夹 ID 可从 Box 网页端 URL 中提取

### 速率限制
- Box API 按端点设置速率限制
- 搜索和列表操作应合理使用分页
- 批量操作应在请求之间加入延迟

### 参数特性
- `fields` 参数会改变响应结构：指定后仅返回精简表示 + 请求的字段
- 搜索需要 `query` 或 `mdfilters` 之一；两者单独都是可选的，但必须提供其中一个
- `BOX_UPDATE_FILE` 将 `lock` 设为 `null` 可移除锁定（仅限原始 API）
- 元数据查询 `from` 字段格式：`enterprise_{enterprise_id}.templateKey` 或 `global.templateKey`

### 权限
- 权限不足时删除操作会失败；始终处理错误响应
- 协作角色决定允许的操作
- 企业设置可能限制某些共享选项

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索内容 | `BOX_SEARCH_FOR_CONTENT` | `query`、`type`、`ancestor_folder_ids` |
| 列出文件夹项目 | `BOX_LIST_ITEMS_IN_FOLDER` | `folder_id`、`limit`、`marker` |
| 获取文件信息 | `BOX_GET_FILE_INFORMATION` | `file_id`、`fields` |
| 获取文件夹信息 | `BOX_GET_FOLDER_INFORMATION` | `folder_id`、`fields` |
| 上传文件 | `BOX_UPLOAD_FILE` | `file`、`parent_id` |
| 下载文件 | `BOX_DOWNLOAD_FILE` | `file_id` |
| 创建文件夹 | `BOX_CREATE_FOLDER` | `name`、`parent__id` |
| 更新文件夹 | `BOX_UPDATE_FOLDER` | `folder_id`、`name`、`parent` |
| 复制文件夹 | `BOX_COPY_FOLDER` | `folder_id`、`parent__id` |
| 删除文件夹 | `BOX_DELETE_FOLDER` | `folder_id`、`recursive` |
| 永久删除文件夹 | `BOX_PERMANENTLY_REMOVE_FOLDER` | folder_id |
| 更新文件 | `BOX_UPDATE_FILE` | `file_id`、`name`、`parent__id` |
| 删除文件 | `BOX_DELETE_FILE` | `file_id`、`if_match` |
| 列出协作 | `BOX_LIST_FILE_COLLABORATIONS` | `file_id` |
| 更新协作 | `BOX_UPDATE_COLLABORATION` | `collaboration_id`、`role` |
| 获取协作 | `BOX_GET_COLLABORATION` | `collaboration_id` |
| 按元数据查询 | `BOX_QUERY_FILES_FOLDERS_BY_METADATA` | `from`、`ancestor_folder_id`、`query` |
| 列出收藏集 | `BOX_LIST_ALL_COLLECTIONS` | （无） |
| 列出收藏集项目 | `BOX_LIST_COLLECTION_ITEMS` | `collection_id` |
| 列出签名请求 | `BOX_LIST_BOX_SIGN_REQUESTS` | `limit`、`marker` |
| 获取签名请求 | `BOX_GET_BOX_SIGN_REQUEST_BY_ID` | `sign_request_id` |
| 取消签名请求 | `BOX_CANCEL_BOX_SIGN_REQUEST` | `sign_request_id` |
| 最近访问项目 | `BOX_LIST_RECENTLY_ACCESSED_ITEMS` | （无） |
| 创建 zip 下载 | `BOX_CREATE_ZIP_DOWNLOAD` | item IDs |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
