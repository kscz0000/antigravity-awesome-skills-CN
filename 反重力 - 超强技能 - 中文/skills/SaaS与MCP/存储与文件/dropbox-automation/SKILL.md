---
name: dropbox-automation
description: "通过 Rube MCP (Composio) 自动化 Dropbox 文件管理、共享、搜索、上传、下载和文件夹操作。始终先搜索工具以获取当前模式。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Dropbox 自动化

通过 Composio 的 Dropbox 工具包自动化 Dropbox 操作，包括文件上传/下载、搜索、文件夹管理、共享链接、批量操作和元数据检索。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 Dropbox 活跃连接，工具包为 `dropbox`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `dropbox` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Dropbox OAuth
4. 在运行任何工作流前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 搜索文件和文件夹

**使用场景**：用户想按名称、内容或类型查找文件或文件夹

**工具序列**：
1. `DROPBOX_SEARCH_FILE_OR_FOLDER` - 使用查询字符串搜索，可选路径范围和过滤器 [必需]
2. `DROPBOX_SEARCH_CONTINUE` - 使用游标分页获取更多结果 [有更多结果时必需]
3. `DROPBOX_GET_METADATA` - 验证并获取搜索结果的规范路径 [可选]
4. `DROPBOX_READ_FILE` - 读取文件内容以确认是目标文档 [可选]

**关键参数**：
- `query`：搜索字符串（不区分大小写，至少 1 个非空白字符）
- `options.path`：将搜索范围限定到某个文件夹（如 `"/Documents"`）；空字符串表示根目录
- `options.file_categories`：按类型过滤（`"image"`、`"document"`、`"pdf"`、`"folder"` 等）
- `options.file_extensions`：按扩展名过滤（如 `["jpg", "png"]`）
- `options.filename_only`：设为 `true` 仅匹配文件名（不匹配内容）
- `options.max_results`：每页结果数（默认 100，最大 1000）

**注意事项**：
- 搜索返回 `has_more: true` 和 `cursor` 时表示还有更多结果；必须继续搜索以避免遗漏匹配项
- search + search_continue 所有分页总共最多 10,000 个匹配
- `DROPBOX_GET_METADATA` 返回的 `path_display` 大小写可能与用户输入不同；始终使用返回的规范路径
- `DROPBOX_READ_FILE` 的文件内容可能以 base64 编码的 `file_content_bytes` 返回；解析前需解码

### 2. 上传和下载文件

**使用场景**：用户想上传文件到 Dropbox 或从中下载文件

**工具序列**：
1. `DROPBOX_UPLOAD_FILE` - 将文件上传到指定路径 [上传时必需]
2. `DROPBOX_READ_FILE` - 从 Dropbox 下载/读取文件 [下载时必需]
3. `DROPBOX_DOWNLOAD_ZIP` - 将整个文件夹下载为 zip 文件 [可选]
4. `DROPBOX_SAVE_URL` - 将公开 URL 的文件直接保存到 Dropbox [可选]
5. `DROPBOX_GET_SHARED_LINK_FILE` - 从共享链接 URL 下载文件 [可选]
6. `DROPBOX_EXPORT_FILE` - 导出 Dropbox Paper 等不可下载文件为 markdown/HTML [可选]

**关键参数**：
- `path`：Dropbox 路径（必须以 `/` 开头，如 `"/Documents/report.pdf"`）
- `mode`：`"add"`（默认，冲突时失败）或 `"overwrite"` 用于上传
- `autorename`：设为 `true` 在冲突时自动重命名而非失败
- `content`：上传用的 FileUploadable 对象，包含 `s3key`、`mimetype` 和 `name`
- `url`：`DROPBOX_SAVE_URL` 用的公开 URL
- `export_format`：Paper 文档用的 `"markdown"`、`"html"` 或 `"plain_text"`

**注意事项**：
- `DROPBOX_SAVE_URL` 是异步操作，大文件可能需要最多 15 分钟
- `DROPBOX_DOWNLOAD_ZIP` 文件夹必须小于 20 GB，单个文件不超过 4 GB，条目少于 10,000 个
- `DROPBOX_READ_FILE` 内容可能是 base64 编码；检查响应格式
- 通过 `DROPBOX_GET_SHARED_LINK_FILE` 下载共享链接可能需要 `link_password` 用于受保护链接

### 3. 共享文件和管理链接

**使用场景**：用户想创建共享链接或管理现有共享链接

**工具序列**：
1. `DROPBOX_GET_METADATA` - 确认文件/文件夹存在并获取规范路径 [前置条件]
2. `DROPBOX_LIST_SHARED_LINKS` - 检查现有共享链接以避免重复 [前置条件]
3. `DROPBOX_CREATE_SHARED_LINK` - 创建新的共享链接 [必需]
4. `DROPBOX_GET_SHARED_LINK_METADATA` - 将共享链接 URL 解析为元数据 [可选]
5. `DROPBOX_LIST_SHARED_FOLDERS` - 列出用户有权访问的所有共享文件夹 [可选]

**关键参数**：
- `path`：创建链接用的文件或文件夹路径
- `settings.audience`：`"public"`、`"team"` 或 `"no_one"`
- `settings.access`：`"viewer"` 或 `"editor"`
- `settings.expires`：ISO 8601 格式过期日期（如 `"2026-12-31T23:59:59Z"`）
- `settings.require_password` / `settings.link_password`：密码保护
- `settings.allow_download`：布尔值，下载权限
- `direct_only`：用于 `LIST_SHARED_LINKS`，设为 `true` 仅返回直接链接（不包括父文件夹链接）

**注意事项**：
- 如果路径已存在共享链接，`DROPBOX_CREATE_SHARED_LINK` 会失败并返回 409 Conflict；先检查 `DROPBOX_LIST_SHARED_LINKS`
- 创建链接前始终用 `DROPBOX_GET_METADATA` 验证路径，避免 `path/not_found` 错误
- 复用 `DROPBOX_LIST_SHARED_LINKS` 中的现有链接而非创建重复链接
- `requested_visibility` 已弃用；新实现请使用 `audience`

### 4. 管理文件夹（创建、移动、删除）

**使用场景**：用户想创建、移动、重命名或删除文件和文件夹

**工具序列**：
1. `DROPBOX_CREATE_FOLDER` - 创建单个文件夹 [创建时必需]
2. `DROPBOX_CREATE_FOLDER_BATCH` - 一次创建多个文件夹 [可选]
3. `DROPBOX_MOVE_FILE_OR_FOLDER` - 移动或重命名单个文件/文件夹 [移动时必需]
4. `DROPBOX_MOVE_BATCH` - 一次移动多个项目 [可选]
5. `DROPBOX_DELETE_FILE_OR_FOLDER` - 删除单个文件或文件夹 [删除时必需]
6. `DROPBOX_DELETE_BATCH` - 一次删除多个项目 [可选]
7. `DROPBOX_COPY_FILE_OR_FOLDER` - 将文件或文件夹复制到新位置 [可选]
8. `DROPBOX_CHECK_MOVE_BATCH` / `DROPBOX_CHECK_FOLDER_BATCH` - 轮询异步批量任务状态 [批量操作时必需]

**关键参数**：
- `path`：目标路径（必须以 `/` 开头，区分大小写）
- `from_path` / `to_path`：移动/复制操作的源路径和目标路径
- `autorename`：设为 `true` 在冲突时自动重命名
- `entries`：批量移动用的 `{from_path, to_path}` 数组；批量创建用的路径数组
- `allow_shared_folder`：设为 `true` 允许移动共享文件夹
- `allow_ownership_transfer`：如果移动会更改所有者则设为 `true`

**注意事项**：
- 所有路径区分大小写且必须以 `/` 开头
- 路径不能以 `/` 或空白字符结尾
- 批量操作可能是异步的；使用 `DROPBOX_CHECK_MOVE_BATCH` 或 `DROPBOX_CHECK_FOLDER_BATCH` 轮询
- `DROPBOX_FILES_MOVE_BATCH` (v1) 具有"全有或全无"行为 — 如果任何条目失败，整个批次失败
- 推荐使用 `DROPBOX_MOVE_BATCH` (v2) 而非 `DROPBOX_FILES_MOVE_BATCH` (v1)
- 批量删除/移动每次最多 1000 个条目；批量创建文件夹每次最多 10,000 个路径
- 批量移动操作不支持仅大小写重命名

### 5. 列出文件夹内容

**使用场景**：用户想浏览或枚举 Dropbox 文件夹中的文件

**工具序列**：
1. `DROPBOX_LIST_FILES_IN_FOLDER` - 列出文件夹内容 [必需]
2. `DROPBOX_LIST_FOLDERS` - 替代的文件夹列表，支持已删除条目 [可选]
3. `DROPBOX_GET_METADATA` - 获取特定项目的详情 [可选]

**关键参数**：
- `path`：文件夹路径（空字符串 `""` 表示根目录）
- `recursive`：设为 `true` 列出所有嵌套内容
- `limit`：每次请求的最大结果数（默认/最大 2000）
- `include_deleted`：设为 `true` 包含已删除但可恢复的项目
- `include_media_info`：设为 `true` 获取照片/视频元数据

**注意事项**：
- 根目录使用空字符串 `""`，不是 `"/"`
- 递归列表可能非常大；使用 `limit` 控制页面大小
- 即使使用小限制，结果也可能通过游标分页
- 路径错误时 `DROPBOX_LIST_FILES_IN_FOLDER` 返回 409 Conflict 和 `path/not_found`

## 常见模式

### ID 解析
- **基于路径**：大多数 Dropbox 工具使用路径字符串（如 `"/Documents/file.pdf"`）
- **基于 ID**：部分工具接受 `id:...` 格式（如 `"id:4g0reWVRsAAAAAAAAAAAQ"`）
- **规范路径**：始终使用 `DROPBOX_GET_METADATA` 响应中的 `path_display` 或 `path_lower` 进行后续调用
- **共享链接 URL**：使用 `DROPBOX_GET_SHARED_LINK_METADATA` 将 URL 解析为路径/ID

### 分页
Dropbox 在大多数端点使用基于游标的分页：
- 搜索：使用 `DROPBOX_SEARCH_CONTINUE` 跟进 `has_more` + `cursor`（总共最多 10,000 个匹配）
- 文件夹列表：跟进响应中的游标直到没有更多页面
- 共享链接：跟进 `DROPBOX_LIST_SHARED_LINKS` 中的 `has_more` + `cursor`
- 批量任务状态：使用 `DROPBOX_CHECK_MOVE_BATCH` / `DROPBOX_CHECK_FOLDER_BATCH` 轮询

### 异步操作
多个 Dropbox 操作异步运行：
- `DROPBOX_SAVE_URL` - 返回任务 ID；轮询或设置 `wait: true`（默认最多 120 秒）
- `DROPBOX_MOVE_BATCH` / `DROPBOX_FILES_MOVE_BATCH` - 可能返回任务 ID
- `DROPBOX_CREATE_FOLDER_BATCH` - 可能返回任务 ID
- `DROPBOX_DELETE_BATCH` - 返回任务 ID

## 已知注意事项

### 路径格式
- 所有路径必须以 `/` 开头（部分端点根目录用空字符串除外）
- 路径不能以 `/` 结尾或包含尾部空白
- 写操作的路径区分大小写
- API 返回的 `path_display` 大小写可能与用户输入不同；始终优先使用 API 返回的路径

### 速率限制
- Dropbox API 有每个端点的速率限制；批量操作有助于减少调用次数
- 搜索在所有分页中总共限制 10,000 个匹配
- `DROPBOX_SAVE_URL` 对大文件有 15 分钟超时

### 文件内容
- `DROPBOX_READ_FILE` 可能以 base64 编码的 `file_content_bytes` 返回内容
- 不可下载文件（Dropbox Paper、Google Docs）需要使用 `DROPBOX_EXPORT_FILE`
- 共享链接的下载 URL 需要正确的认证头

### 共享
- 已存在共享链接时创建新链接会返回 409 Conflict 错误
- 创建新链接前始终检查 `DROPBOX_LIST_SHARED_LINKS`
- 共享文件夹访问可能不会出现在标准路径列表中；使用 `DROPBOX_LIST_SHARED_FOLDERS`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索文件 | `DROPBOX_SEARCH_FILE_OR_FOLDER` | `query`, `options.path` |
| 继续搜索 | `DROPBOX_SEARCH_CONTINUE` | `cursor` |
| 列出文件夹 | `DROPBOX_LIST_FILES_IN_FOLDER` | `path`, `recursive`, `limit` |
| 列出文件夹 | `DROPBOX_LIST_FOLDERS` | `path`, `recursive` |
| 获取元数据 | `DROPBOX_GET_METADATA` | `path` |
| 读取/下载文件 | `DROPBOX_READ_FILE` | `path` |
| 上传文件 | `DROPBOX_UPLOAD_FILE` | `path`, `content`, `mode` |
| 保存 URL 到 Dropbox | `DROPBOX_SAVE_URL` | `path`, `url` |
| 下载文件夹 zip | `DROPBOX_DOWNLOAD_ZIP` | `path` |
| 导出 Paper 文档 | `DROPBOX_EXPORT_FILE` | `path`, `export_format` |
| 下载共享链接 | `DROPBOX_GET_SHARED_LINK_FILE` | `url` |
| 创建共享链接 | `DROPBOX_CREATE_SHARED_LINK` | `path`, `settings` |
| 列出共享链接 | `DROPBOX_LIST_SHARED_LINKS` | `path`, `direct_only` |
| 共享链接元数据 | `DROPBOX_GET_SHARED_LINK_METADATA` | `url` |
| 列出共享文件夹 | `DROPBOX_LIST_SHARED_FOLDERS` | `limit` |
| 创建文件夹 | `DROPBOX_CREATE_FOLDER` | `path` |
| 批量创建文件夹 | `DROPBOX_CREATE_FOLDER_BATCH` | `paths` |
| 移动文件/文件夹 | `DROPBOX_MOVE_FILE_OR_FOLDER` | `from_path`, `to_path` |
| 批量移动 | `DROPBOX_MOVE_BATCH` | `entries` |
| 删除文件/文件夹 | `DROPBOX_DELETE_FILE_OR_FOLDER` | `path` |
| 批量删除 | `DROPBOX_DELETE_BATCH` | `entries` |
| 复制文件/文件夹 | `DROPBOX_COPY_FILE_OR_FOLDER` | `from_path`, `to_path` |
| 检查批量状态 | `DROPBOX_CHECK_MOVE_BATCH` | `async_job_id` |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
