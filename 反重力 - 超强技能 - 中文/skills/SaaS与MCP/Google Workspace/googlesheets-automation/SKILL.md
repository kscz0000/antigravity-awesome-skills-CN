---
name: googlesheets-automation
description: "通过 Rube MCP (Composio) 自动化 Google Sheets 操作（读取、写入、格式化、筛选、管理电子表格）。读写数据、管理工作表标签、应用格式、编程搜索行。触发词：Google表格自动化、Google Sheets操作、表格读写、电子表格自动化、googlesheets"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Google Sheets

通过 Composio 的 Google Sheets 工具包自动化 Google Sheets 工作流，包括读写数据、管理电子表格和工作表标签、格式化单元格、筛选行以及更新或插入记录。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `googlesheets` 建立有效的 Google Sheets 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 toolkit `googlesheets`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Google OAuth
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 读取和写入数据

**适用场景**：用户想从 Google Sheet 读取数据或向其写入数据

**工具调用顺序**：
1. `GOOGLESHEETS_SEARCH_SPREADSHEETS` - 按名称查找电子表格（ID 未知时）[前置条件]
2. `GOOGLESHEETS_GET_SHEET_NAMES` - 枚举工作表标签名称以定位目标工作表 [前置条件]
3. `GOOGLESHEETS_BATCH_GET` - 从一个或多个范围读取数据 [必需]
4. `GOOGLESHEETS_BATCH_UPDATE` - 向范围写入数据或追加行 [必需]
5. `GOOGLESHEETS_VALUES_UPDATE` - 更新单个指定范围 [替代方案]
6. `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND` - 在表格末尾追加行 [替代方案]

**关键参数**：
- `spreadsheet_id`：电子表格 URL 中的字母数字 ID（位于 '/d/' 和 '/edit' 之间）
- `ranges`：A1 表示法数组（如 'Sheet1!A1:Z1000'）；始终使用有界范围
- `sheet_name`：工作表标签名称（支持不区分大小写匹配）
- `values`：二维数组，每个内部数组代表一行
- `first_cell_location`：A1 表示法的起始单元格（省略则追加）
- `valueInputOption`：'USER_ENTERED'（解析）或 'RAW'（原样）

**注意事项**：
- 大小写错误或不存在的标签名会报错 "Sheet 'X' not found"
- 空范围可能省略 `valueRanges[i].values`；将缺失值视为空数组
- `GOOGLESHEETS_BATCH_UPDATE` 的 values 必须是二维数组（列表的列表），即使只有一行
- 在超过 10,000 行的工作表上使用无界范围如 'A:Z' 可能导致超时；始终用行限制界定范围
- 追加操作遵循检测到的 `tableRange`；使用返回的 `updatedRange` 验证位置

### 2. 创建和管理电子表格

**适用场景**：用户想创建新电子表格或管理其中的工作表标签

**工具调用顺序**：
1. `GOOGLESHEETS_CREATE_GOOGLE_SHEET1` - 创建新电子表格 [必需]
2. `GOOGLESHEETS_ADD_SHEET` - 添加新工作表标签 [必需]
3. `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES` - 重命名、隐藏、重排或着色标签 [可选]
4. `GOOGLESHEETS_GET_SPREADSHEET_INFO` - 获取完整电子表格元数据 [可选]
5. `GOOGLESHEETS_FIND_WORKSHEET_BY_TITLE` - 检查特定标签是否存在 [可选]

**关键参数**：
- `title`：电子表格或工作表标签名称
- `spreadsheetId`：目标电子表格 ID
- `forceUnique`：标签名已存在时自动追加后缀（默认 true）
- `properties.gridProperties`：设置行/列数、冻结行数

**注意事项**：
- 工作表标签名称在同一电子表格内必须唯一
- 默认标签名取决于区域设置（英文为 'Sheet1'，西班牙文为 'Hoja 1'）
- 并行创建多个工作表时不要使用 `index`（会导致 'index too high' 错误）
- 如果账号无权限，`GOOGLESHEETS_GET_SPREADSHEET_INFO` 可能返回 403

### 3. 搜索和筛选行

**适用场景**：用户想查找特定行或对工作表数据应用筛选

**工具调用顺序**：
1. `GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW` - 查找匹配精确单元格值的第一行 [必需]
2. `GOOGLESHEETS_SET_BASIC_FILTER` - 对范围应用筛选/排序 [替代方案]
3. `GOOGLESHEETS_CLEAR_BASIC_FILTER` - 移除现有筛选 [可选]
4. `GOOGLESHEETS_BATCH_GET` - 读取筛选结果 [可选]

**关键参数**：
- `query`：要匹配的精确文本值（匹配整个单元格内容）
- `range`：搜索范围内的 A1 表示法
- `case_sensitive`：是否区分大小写匹配的布尔值（默认 false）
- `filter.range`：带 sheet_id 的网格范围，用于基本筛选
- `filter.criteria`：基于列的筛选条件
- `filter.sortSpecs`：排序规格

**注意事项**：
- `GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW` 匹配整个单元格内容，不支持子字符串匹配
- 包含空格的工作表名在范围中必须用单引号括起（如 "'My Sheet'!A:Z"）
- 查找不支持不带范围的裸工作表名；始终指定范围

### 4. 按键列更新或插入行

**适用场景**：用户想基于唯一键列更新现有行或插入新行

**工具调用顺序**：
1. `GOOGLESHEETS_UPSERT_ROWS` - 更新匹配行或追加新行 [必需]

**关键参数**：
- `spreadsheetId`：目标电子表格 ID
- `sheetName`：工作表标签名称
- `keyColumn`：用作唯一标识符的列标题名（如 'Email'、'SKU'）
- `headers`：数据的列名列表
- `rows`：数据行的二维数组
- `strictMode`：列数不匹配时报错（默认 true）

**注意事项**：
- `keyColumn` 必须是实际的标题名称，不是列字母（如 'Email' 而非 'A'）
- 如果未提供 `headers`，`rows` 的第一行将被视为标题
- `strictMode=true` 时，值多于标题的行会导致错误
- 自动向工作表添加缺失的列

### 5. 格式化单元格

**适用场景**：用户想对单元格应用格式（加粗、颜色、字号）

**工具调用顺序**：
1. `GOOGLESHEETS_GET_SPREADSHEET_INFO` - 获取目标标签的数字 sheetId [前置条件]
2. `GOOGLESHEETS_FORMAT_CELL` - 对范围应用格式 [必需]
3. `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES` - 更改冻结行、列宽 [可选]

**关键参数**：
- `spreadsheet_id`：电子表格 ID
- `worksheet_id`：数字 sheetId（不是标签名）；从 GET_SPREADSHEET_INFO 获取
- `range`：A1 表示法（如 'A1:F1'）— 优于索引字段
- `bold`、`italic`、`underline`、`strikethrough`：布尔格式选项
- `red`、`green`、`blue`：背景颜色，0.0-1.0 浮点数（不是 0-255 整数）
- `fontSize`：字号（磅）

**注意事项**：
- 需要数字 `worksheet_id`，不是标签标题；从电子表格元数据获取
- 颜色通道为 0-1 浮点数（如 1.0 表示全红），不是 0-255 整数
- 响应可能返回空对象（[{}]）；通过回读验证格式效果
- 每次调用格式化一个范围；批量格式化需要多次调用

## 常用模式

### ID 解析
- **电子表格名称 → ID**：`GOOGLESHEETS_SEARCH_SPREADSHEETS` 配合 `query`
- **标签名 → sheetId**：`GOOGLESHEETS_GET_SPREADSHEET_INFO`，从工作表元数据中提取
- **标签存在性检查**：`GOOGLESHEETS_FIND_WORKSHEET_BY_TITLE`

### 速率限制
Google Sheets 实施严格的速率限制：
- 每分钟最多 60 次读取和 60 次写入
- 超限会导致错误；尽量使用批量操作
- 使用 `GOOGLESHEETS_BATCH_GET` 和 `GOOGLESHEETS_BATCH_UPDATE` 提高效率

### 数据模式
- 写入前始终先读取，了解现有布局
- 使用 `GOOGLESHEETS_UPSERT_ROWS` 处理 CRM 同步、库存更新和去重场景
- 追加模式（省略 `first_cell_location`）是添加新记录最安全的方式
- 使用 `GOOGLESHEETS_CLEAR_VALUES` 清除内容但保留格式

## 已知注意事项

- **标签名**：默认值取决于区域设置；非英文账号可能不存在 'Sheet1'
- **范围表示法**：包含空格的工作表名在 A1 表示法中需要单引号
- **无界范围**：大型工作表上可能超时；始终指定行边界（如 'A1:Z10000'）
- **二维数组**：所有 value 参数必须是列表的列表，即使只有一行
- **颜色值**：浮点数 0.0-1.0，不是整数 0-255
- **格式化 ID**：`FORMAT_CELL` 需要数字 sheetId，不是标签标题
- **速率限制**：每分钟 60 次读取和 60 次写入；批量操作以保持在限制内
- **删除维度**：`GOOGLESHEETS_DELETE_DIMENSION` 不可逆；仔细检查边界

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 搜索电子表格 | `GOOGLESHEETS_SEARCH_SPREADSHEETS` | `query`, `search_type` |
| 创建电子表格 | `GOOGLESHEETS_CREATE_GOOGLE_SHEET1` | `title` |
| 列出标签 | `GOOGLESHEETS_GET_SHEET_NAMES` | `spreadsheet_id` |
| 添加标签 | `GOOGLESHEETS_ADD_SHEET` | `spreadsheetId`, `title` |
| 读取数据 | `GOOGLESHEETS_BATCH_GET` | `spreadsheet_id`, `ranges` |
| 读取单个范围 | `GOOGLESHEETS_VALUES_GET` | `spreadsheet_id`, `range` |
| 写入数据 | `GOOGLESHEETS_BATCH_UPDATE` | `spreadsheet_id`, `sheet_name`, `values` |
| 更新范围 | `GOOGLESHEETS_VALUES_UPDATE` | `spreadsheet_id`, `range`, `values` |
| 追加行 | `GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND` | `spreadsheetId`, `range`, `values` |
| 更新或插入行 | `GOOGLESHEETS_UPSERT_ROWS` | `spreadsheetId`, `sheetName`, `keyColumn`, `rows` |
| 查找行 | `GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW` | `spreadsheet_id`, `query` |
| 格式化单元格 | `GOOGLESHEETS_FORMAT_CELL` | `spreadsheet_id`, `worksheet_id`, `range` |
| 设置筛选 | `GOOGLESHEETS_SET_BASIC_FILTER` | `spreadsheetId`, `filter` |
| 清除值 | `GOOGLESHEETS_CLEAR_VALUES` | `spreadsheet_id`, range |
| 删除行/列 | `GOOGLESHEETS_DELETE_DIMENSION` | `spreadsheet_id`, `sheet_name`, dimension |
| 电子表格信息 | `GOOGLESHEETS_GET_SPREADSHEET_INFO` | `spreadsheet_id` |
| 更新标签属性 | `GOOGLESHEETS_UPDATE_SHEET_PROPERTIES` | `spreadsheetId`, properties |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
