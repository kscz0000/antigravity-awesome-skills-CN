---
name: coda-automation
description: "通过 Rube MCP (Composio) 自动化 Coda 任务：管理文档、页面、表格、行、公式、权限和发布。始终先搜索工具获取当前 schema。当用户要求'自动化 Coda'、'管理 Coda 文档'、'操作 Coda 表格'或相关主题时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Coda 自动化

通过 Rube MCP 使用 Composio 的 Coda 工具包自动化 Coda 文档和数据操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `coda` 建立活跃的 Coda 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `coda` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Coda 认证
4. 运行任何工作流前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 搜索和浏览文档

**适用场景**：用户想要查找、列出或检查 Coda 文档

**工具调用顺序**：
1. `CODA_SEARCH_DOCS` 或 `CODA_LIST_AVAILABLE_DOCS` - 查找文档 [必需]
2. `CODA_RESOLVE_BROWSER_LINK` - 将 Coda URL 解析为文档/页面/表格 ID [备选]
3. `CODA_LIST_PAGES` - 列出文档中的页面 [可选]
4. `CODA_GET_A_PAGE` - 获取特定页面详情 [可选]

**关键参数**：
- `query`：查找文档的搜索词
- `isOwner`：筛选用户拥有的文档
- `docId`：页面操作所需的文档 ID
- `pageIdOrName`：页面标识符或名称
- `url`：解析操作所需的浏览器 URL

**注意事项**：
- 文档 ID 是字母数字字符串（如 'AbCdEfGhIj'）
- `CODA_RESOLVE_BROWSER_LINK` 是将 Coda URL 转换为 API ID 的最佳方式
- 页面名称在文档内可能不唯一；优先使用页面 ID
- 搜索结果包含与用户共享的文档，不只是用户拥有的文档

### 2. 操作表格和数据

**适用场景**：用户想要读取、写入或查询表格数据

**工具调用顺序**：
1. `CODA_LIST_TABLES` - 列出文档中的表格 [前置]
2. `CODA_LIST_COLUMNS` - 获取表格的列定义 [前置]
3. `CODA_LIST_TABLE_ROWS` - 列出所有行，支持可选筛选 [必需]
4. `CODA_SEARCH_ROW` - 按查询搜索特定行 [备选]
5. `CODA_GET_A_ROW` - 按 ID 获取特定行 [可选]
6. `CODA_UPSERT_ROWS` - 在表格中插入或更新行 [可选]
7. `CODA_GET_A_COLUMN` - 获取特定列的详情 [可选]

**关键参数**：
- `docId`：包含表格的文档 ID
- `tableIdOrName`：表格标识符或名称
- `query`：搜索行的筛选查询
- `rows`：upsert 操作的行对象数组
- `keyColumns`：upsert 时用于匹配的列 ID
- `sortBy`：排序结果的列
- `useColumnNames`：在行数据中使用列名而非 ID

**注意事项**：
- 表格名称可能包含空格；需要时进行 URL 编码
- `CODA_UPSERT_ROWS` 在 `keyColumns` 无匹配时执行插入，有匹配时执行更新
- `keyColumns` 必须引用具有唯一值的列才能可靠执行 upsert
- 列 ID 与列名不同；先列出列以映射名称到 ID
- `useColumnNames: true` 允许在行数据中使用可读名称
- 行数据值必须匹配列类型（文本、数字、日期等）

### 3. 管理公式

**适用场景**：用户想要列出或计算文档中的公式

**工具调用顺序**：
1. `CODA_LIST_FORMULAS` - 列出文档中所有命名公式 [必需]
2. `CODA_GET_A_FORMULA` - 获取特定公式的当前值 [可选]

**关键参数**：
- `docId`：文档 ID
- `formulaIdOrName`：公式标识符或名称

**注意事项**：
- 公式是在文档中定义的命名计算
- 公式值在服务端计算；结果反映当前状态
- 公式名称区分大小写

### 4. 导出文档内容

**适用场景**：用户想要将文档或页面导出为 HTML 或 Markdown

**工具调用顺序**：
1. `CODA_BEGIN_CONTENT_EXPORT` - 启动导出任务 [必需]
2. `CODA_CONTENT_EXPORT_STATUS` - 轮询导出状态直到完成 [必需]

**关键参数**：
- `docId`：要导出的文档 ID
- `outputFormat`：导出格式（'html' 或 'markdown'）
- `pageIdOrName`：要导出的特定页面（可选，省略则导出整个文档）
- `requestId`：状态轮询的导出请求 ID

**注意事项**：
- 导出是异步的；轮询状态直到 `status` 为 'complete'
- 大型文档导出可能需要较长时间
- 完成响应中的导出 URL 是临时的；及时下载
- 轮询过于频繁可能触发速率限制；使用 2-5 秒间隔

### 5. 管理权限和共享

**适用场景**：用户想要查看或管理文档访问权限

**工具调用顺序**：
1. `CODA_GET_SHARING_METADATA` - 查看当前共享设置 [必需]
2. `CODA_GET_ACL_SETTINGS` - 获取访问控制列表设置 [可选]
3. `CODA_ADD_PERMISSION` - 授予用户或邮箱访问权限 [可选]

**关键参数**：
- `docId`：文档 ID
- `access`：权限级别（'readonly'、'write'、'comment'）
- `principal`：包含收件人邮箱或用户 ID 的对象
- `suppressEmail`：是否跳过共享通知邮件

**注意事项**：
- 权限级别：'readonly'（只读）、'write'（写入）、'comment'（评论）
- 添加权限默认发送邮件通知；使用 `suppressEmail` 阻止
- 某些情况下无法通过 API 移除权限；检查 ACL 设置

### 6. 发布和自定义文档

**适用场景**：用户想要发布文档或管理自定义域名

**工具调用顺序**：
1. `CODA_PUBLISH_DOC` - 公开发布文档 [必需]
2. `CODA_UNPUBLISH_DOC` - 取消发布文档 [可选]
3. `CODA_ADD_CUSTOM_DOMAIN` - 为已发布文档添加自定义域名 [可选]
4. `CODA_GET_DOC_CATEGORIES` - 获取文档分类以便发现 [可选]

**关键参数**：
- `docId`：文档 ID
- `slug`：已发布文档的自定义 URL slug
- `categoryIds`：用于可发现性的分类 ID

**注意事项**：
- 发布后任何拥有链接的人都可以访问文档
- 自定义域名需要 DNS 配置
- 取消发布移除公开访问但保留共享访问

## 常用模式

### ID 解析

**文档 URL -> 文档 ID**：
```
1. Call CODA_RESOLVE_BROWSER_LINK with the Coda URL
2. Extract docId from the response
```

**表格名称 -> 表格 ID**：
```
1. Call CODA_LIST_TABLES with docId
2. Find table by name, extract id
```

**列名称 -> 列 ID**：
```
1. Call CODA_LIST_COLUMNS with docId and tableIdOrName
2. Find column by name, extract id
```

### 分页

- Coda 使用基于游标的分页，通过 `pageToken` 实现
- 检查响应中的 `nextPageToken`
- 在下一次请求中作为 `pageToken` 传递，直到不存在
- 默认页面大小因端点而异

### 行 Upsert 模式

```
1. Call CODA_LIST_COLUMNS to get column IDs
2. Build row objects with column ID keys and values
3. Set keyColumns to unique identifier column(s)
4. Call CODA_UPSERT_ROWS with rows and keyColumns
```

## 已知注意事项

**ID 格式**：
- 文档 ID：字母数字字符串
- 表格/列/行 ID：带前缀的字符串（如 'grid-abc'、'c-xyz'）
- 使用 RESOLVE_BROWSER_LINK 将 URL 转换为 ID

**数据类型**：
- 行值必须匹配列类型
- 日期列需要 ISO 8601 格式
- 选择/多选列需要精确的选项值
- 人员列需要邮箱地址

**速率限制**：
- Coda API 有每个 token 的速率限制
- 429 响应时实现退避策略
- 通过 UPSERT_ROWS 批量行操作比单独更新更高效

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索文档 | CODA_SEARCH_DOCS | query |
| 列出文档 | CODA_LIST_AVAILABLE_DOCS | isOwner |
| 解析 URL | CODA_RESOLVE_BROWSER_LINK | url |
| 列出页面 | CODA_LIST_PAGES | docId |
| 获取页面 | CODA_GET_A_PAGE | docId, pageIdOrName |
| 列出表格 | CODA_LIST_TABLES | docId |
| 列出列 | CODA_LIST_COLUMNS | docId, tableIdOrName |
| 列出行 | CODA_LIST_TABLE_ROWS | docId, tableIdOrName |
| 搜索行 | CODA_SEARCH_ROW | docId, tableIdOrName, query |
| 获取行 | CODA_GET_A_ROW | docId, tableIdOrName, rowIdOrName |
| Upsert 行 | CODA_UPSERT_ROWS | docId, tableIdOrName, rows, keyColumns |
| 获取列 | CODA_GET_A_COLUMN | docId, tableIdOrName, columnIdOrName |
| 按下按钮 | CODA_PUSH_A_BUTTON | docId, tableIdOrName, rowIdOrName, columnIdOrName |
| 列出公式 | CODA_LIST_FORMULAS | docId |
| 获取公式 | CODA_GET_A_FORMULA | docId, formulaIdOrName |
| 开始导出 | CODA_BEGIN_CONTENT_EXPORT | docId, outputFormat |
| 导出状态 | CODA_CONTENT_EXPORT_STATUS | docId, requestId |
| 获取共享 | CODA_GET_SHARING_METADATA | docId |
| 添加权限 | CODA_ADD_PERMISSION | docId, access, principal |
| 发布文档 | CODA_PUBLISH_DOC | docId, slug |
| 取消发布 | CODA_UNPUBLISH_DOC | docId |
| 列出 packs | CODA_LIST_PACKS | (none) |

## 使用时机
当任务明确匹配上述范围时使用此技能。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
