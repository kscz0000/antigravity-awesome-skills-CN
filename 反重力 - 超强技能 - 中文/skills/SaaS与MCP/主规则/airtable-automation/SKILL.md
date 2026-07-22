---
name: airtable-automation
description: "通过 Rube MCP (Composio) 自动化 Airtable 任务：记录、数据库、表格、字段、视图。始终先搜索工具以获取当前模式。触发词：Airtable自动化、Airtable记录管理、Airtable字段操作、Airtable表格操作、Rube MCP、Composio Airtable"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Airtable

通过 Composio 的 Airtable 工具包和 Rube MCP 自动化 Airtable 操作。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Airtable 连接，工具包为 `airtable`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `airtable` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Airtable 认证
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 创建和管理记录

**使用时机**：用户想要创建、读取、更新或删除记录

**工具调用顺序**：
1. `AIRTABLE_LIST_BASES` - 发现可用的数据库 [前提条件]
2. `AIRTABLE_GET_BASE_SCHEMA` - 检查表结构 [前提条件]
3. `AIRTABLE_LIST_RECORDS` - 列出/筛选记录 [可选]
4. `AIRTABLE_CREATE_RECORD` / `AIRTABLE_CREATE_RECORDS` - 创建记录 [可选]
5. `AIRTABLE_UPDATE_RECORD` / `AIRTABLE_UPDATE_MULTIPLE_RECORDS` - 更新记录 [可选]
6. `AIRTABLE_DELETE_RECORD` / `AIRTABLE_DELETE_MULTIPLE_RECORDS` - 删除记录 [可选]

**关键参数**：
- `baseId`：数据库 ID（以 'app' 开头，例如 'appXXXXXXXXXXXXXX'）
- `tableIdOrName`：表 ID（以 'tbl' 开头）或表名
- `fields`：字段名到值的映射对象
- `recordId`：记录 ID（以 'rec' 开头），用于更新/删除
- `filterByFormula`：用于筛选的 Airtable 公式
- `typecast`：设为 true 以启用自动类型转换

**常见陷阱**：
- pageSize 上限为 100；使用偏移量分页；在页面之间更改筛选条件可能导致跳过/重复行
- CREATE_RECORDS 每次请求硬限制为 10 条记录；大批量导入需分块处理
- 字段名区分大小写，必须与模式完全匹配
- 字段名错误时返回 422 UNKNOWN_FIELD_NAME；权限问题时返回 403
- INVALID_MULTIPLE_CHOICE_OPTIONS 可能需要设置 typecast=true

### 2. 搜索和筛选记录

**使用时机**：用户想要使用公式查找特定记录

**工具调用顺序**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 验证字段名和类型 [前提条件]
2. `AIRTABLE_LIST_RECORDS` - 使用 filterByFormula 查询 [必需]
3. `AIRTABLE_GET_RECORD` - 获取完整记录详情 [可选]

**关键参数**：
- `filterByFormula`：Airtable 公式（例如 `{Status}='Done'`）
- `sort`：排序对象数组
- `fields`：要返回的字段名数组
- `maxRecords`：所有页面的最大记录总数
- `offset`：上一次响应的分页游标

**常见陷阱**：
- 公式中的字段名必须用 `{}` 包裹，且与模式完全匹配
- 字符串值必须加引号：`{Status}='Active'` 而非 `{Status}=Active`
- 语法错误或不存在的字段返回 422 INVALID_FILTER_BY_FORMULA
- Airtable 速率限制：每个数据库约 5 请求/秒；遇到 429 时使用 Retry-After 处理

### 3. 管理字段和模式

**使用时机**：用户想要创建或修改表字段

**工具调用顺序**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 检查当前模式 [前提条件]
2. `AIRTABLE_CREATE_FIELD` - 创建新字段 [可选]
3. `AIRTABLE_UPDATE_FIELD` - 重命名/描述字段 [可选]
4. `AIRTABLE_UPDATE_TABLE` - 更新表元数据 [可选]

**关键参数**：
- `name`：字段名
- `type`：字段类型（singleLineText、number、singleSelect 等）
- `options`：类型特定选项（选择类型的选项列表、数字类型的精度）
- `description`：字段描述

**常见陷阱**：
- UPDATE_FIELD 只能更改 name/description，不能更改 type/options；需创建替换字段并迁移数据
- 计算字段（formula、rollup、lookup）无法通过 API 创建
- 类型选项缺失或格式错误时返回 422

### 4. 管理评论

**使用时机**：用户想要查看或添加记录评论

**工具调用顺序**：
1. `AIRTABLE_LIST_COMMENTS` - 列出记录上的评论 [必需]

**关键参数**：
- `baseId`：数据库 ID
- `tableIdOrName`：表标识符
- `recordId`：记录 ID（17 个字符，以 'rec' 开头）
- `pageSize`：每页评论数（最多 100）

**常见陷阱**：
- 记录 ID 必须恰好为 17 个字符且以 'rec' 开头

## 常用模式

### Airtable 公式语法

**比较运算**：
- `{Status}='Done'` - 等于
- `{Priority}>1` - 大于
- `{Name}!=''` - 非空

**函数**：
- `AND({A}='x', {B}='y')` - 两个条件同时满足
- `OR({A}='x', {A}='y')` - 任一条件满足
- `FIND('test', {Name})>0` - 包含文本
- `IS_BEFORE({Due Date}, TODAY())` - 日期比较

**转义规则**：
- 值中的单引号：双写（`{Name}='John''s Company'`）

### 分页

- 设置 `pageSize`（最大 100）
- 检查响应中的 `offset` 字符串
- 将 `offset` 原样传递给下一次请求
- 在页面之间保持筛选/排序/视图不变

## 已知陷阱

**ID 格式**：
- 数据库 ID：`appXXXXXXXXXXXXXX`（17 个字符）
- 表 ID：`tblXXXXXXXXXXXXXX`（17 个字符）
- 记录 ID：`recXXXXXXXXXXXXXX`（17 个字符）
- 字段 ID：`fldXXXXXXXXXXXXXX`（17 个字符）

**批量限制**：
- CREATE_RECORDS：每次请求最多 10 条
- UPDATE_MULTIPLE_RECORDS：每次请求最多 10 条
- DELETE_MULTIPLE_RECORDS：每次请求最多 10 条

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出数据库 | AIRTABLE_LIST_BASES | (无) |
| 获取模式 | AIRTABLE_GET_BASE_SCHEMA | baseId |
| 列出记录 | AIRTABLE_LIST_RECORDS | baseId, tableIdOrName |
| 获取记录 | AIRTABLE_GET_RECORD | baseId, tableIdOrName, recordId |
| 创建记录 | AIRTABLE_CREATE_RECORD | baseId, tableIdOrName, fields |
| 批量创建 | AIRTABLE_CREATE_RECORDS | baseId, tableIdOrName, records |
| 更新记录 | AIRTABLE_UPDATE_RECORD | baseId, tableIdOrName, recordId, fields |
| 批量更新 | AIRTABLE_UPDATE_MULTIPLE_RECORDS | baseId, tableIdOrName, records |
| 删除记录 | AIRTABLE_DELETE_RECORD | baseId, tableIdOrName, recordId |
| 创建字段 | AIRTABLE_CREATE_FIELD | baseId, tableIdOrName, name, type |
| 更新字段 | AIRTABLE_UPDATE_FIELD | baseId, tableIdOrName, fieldId |
| 更新表 | AIRTABLE_UPDATE_TABLE | baseId, tableIdOrName, name |
| 列出评论 | AIRTABLE_LIST_COMMENTS | baseId, tableIdOrName, recordId |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
