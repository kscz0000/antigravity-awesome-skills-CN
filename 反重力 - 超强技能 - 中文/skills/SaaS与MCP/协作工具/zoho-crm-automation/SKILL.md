---
name: zoho-crm-automation
description: "通过 Rube MCP (Composio) 自动化 Zoho CRM 任务：创建/更新记录、搜索联系人、管理线索以及转换线索。始终先搜索工具以获取最新 schema。触发词：Zoho CRM、Rube MCP、Composio、CRM 自动化、线索管理、记录管理、联系人搜索、lead conversion。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Zoho CRM 自动化

通过 Rube MCP，使用 Composio 的 Zoho 工具包自动化 Zoho CRM 操作。

## 前置条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与 toolkit `zoho` 建立活动的 Zoho CRM 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API key——只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用 toolkit `zoho` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按照返回的鉴权链接完成 Zoho OAuth
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 搜索与获取记录

**使用场景**：用户希望按条件查找特定的 CRM 记录

**工具调用顺序**：
1. `ZOHO_LIST_MODULES` - 列出可用的 CRM 模块 [前置]
2. `ZOHO_GET_MODULE_FIELDS` - 获取某模块的字段定义 [可选]
3. `ZOHO_SEARCH_ZOHO_RECORDS` - 按条件搜索记录 [必需]
4. `ZOHO_GET_ZOHO_RECORDS` - 从模块获取记录 [替代方案]

**关键参数**：
- `module`：模块名（例如 'Leads'、'Contacts'、'Deals'、'Accounts'）
- `criteria`：搜索条件字符串（例如 'Email:equals:john@example.com'）
- `fields`：要返回的字段列表，使用逗号分隔
- `per_page`：每页的记录数
- `page`：分页的页码

**常见陷阱**：
- 模块名称区分大小写（例如 'Leads'，不是 'leads'）
- 搜索条件使用特定语法：'Field:operator:value'
- 支持的操作符：equals、starts_with、contains、not_equal、greater_than、less_than
- 复杂条件使用括号和 AND/OR：'(Email:equals:john@example.com)AND(Last_Name:equals:Doe)'
- `GET_ZOHO_RECORDS` 返回所有记录并支持可选过滤；`SEARCH` 用于定向查找

### 2. 创建记录

**使用场景**：用户希望添加新的线索、联系人、商机或其他 CRM 记录

**工具调用顺序**：
1. `ZOHO_GET_MODULE_FIELDS` - 获取模块的必需字段 [前置]
2. `ZOHO_CREATE_ZOHO_RECORD` - 创建一条新记录 [必需]

**关键参数**：
- `module`：目标模块名（例如 'Leads'、'Contacts'）
- `data`：记录数据对象，包含字段-值对
- 必需字段因模块而异（例如 Contacts 的 Last_Name）

**常见陷阱**：
- 每个模块都有必填字段；使用 `GET_MODULE_FIELDS` 来识别它们
- 字段名使用下划线（例如 'Last_Name'、'Email'、'Phone'）
- 查找字段需要传入关联记录的 ID，而不是名称
- 日期字段必须使用 'yyyy-MM-dd' 格式
- 除非配置了重复检查规则，否则允许创建重复记录

### 3. 更新记录

**使用场景**：用户希望修改现有的 CRM 记录

**工具调用顺序**：
1. `ZOHO_SEARCH_ZOHO_RECORDS` - 查找要更新的记录 [前置]
2. `ZOHO_UPDATE_ZOHO_RECORD` - 更新记录 [必需]

**关键参数**：
- `module`：模块名
- `record_id`：要更新的记录的 ID
- `data`：包含要更新字段的对象（仅需传入发生变化的字段）

**常见陷阱**：
- `record_id` 必须是 Zoho 记录 ID（数字字符串）
- 仅传入需要更改的字段；其他字段会保持不变
- 只读字段和系统字段无法更新
- 更新查找字段需要传入关联记录的 ID

### 4. 转换线索

**使用场景**：用户希望将一条线索转换为联系人、客户和/或商机

**工具调用顺序**：
1. `ZOHO_SEARCH_ZOHO_RECORDS` - 查找要转换的线索 [前置]
2. `ZOHO_CONVERT_ZOHO_LEAD` - 转换线索 [必需]

**关键参数**：
- `lead_id`：要转换的线索的 ID
- `deal`：在转换过程中创建商机时的商机详情
- `account`：转换的客户详情
- `contact`：转换的联系人详情

**常见陷阱**：
- 线索转换是不可逆的；该线索记录会从 Leads 模块中删除
- 一次转换最多可创建三条记录：联系人、客户和商机
- 可能根据公司名称匹配已有的客户
- Lead 与 Contact/Account/Deal 模块之间的自定义字段映射会影响转换结果

### 5. 管理标签和关联记录

**使用场景**：用户希望为记录打标签或管理记录之间的关系

**工具调用顺序**：
1. `ZOHO_CREATE_ZOHO_TAG` - 创建新标签 [可选]
2. `ZOHO_UPDATE_RELATED_RECORDS` - 更新关联/链接的记录 [可选]

**关键参数**：
- `module`：标签所属的模块
- `tag_name`：标签名称
- `record_id`：父记录 ID（用于关联记录）
- `related_module`：关联记录所属的模块
- `data`：要更新的关联记录数据

**常见陷阱**：
- 标签是模块特定的；在 Leads 中创建的标签在 Contacts 中不可用
- 关联记录同时需要父记录 ID 和关联模块
- 标签名称在同一模块内必须唯一
- 批量标签操作可能会触发限流

## 常见模式

### 模块与字段发现

```
1. Call ZOHO_LIST_MODULES to get all available modules
2. Call ZOHO_GET_MODULE_FIELDS with module name
3. Identify required fields, field types, and picklist values
4. Use field API names (not display labels) in data objects
```

### 搜索条件语法

**简单搜索**：
```
criteria: '(Email:equals:john@example.com)'
```

**组合条件**：
```
criteria: '((Last_Name:equals:Doe)AND(Email:contains:example.com))'
```

**支持的操作符**：
- `equals`、`not_equal`
- `starts_with`、`contains`
- `greater_than`、`less_than`、`greater_equal`、`less_equal`
- `between`（用于日期/数字）

### 分页

- 设置 `per_page`（最大 200）和 `page`，起始值为 1
- 检查响应中的 `info.more_records` 标志
- 不断递增 page，直到 `more_records` 为 false
- 总记录数可在响应 info 中获取

## 已知陷阱

**字段名称**：
- 使用 API 名称，而不是显示标签（例如使用 'Last_Name'，而不是 'Last Name'）
- 自定义字段的 API 名称形如 'Custom_Field1' 或用户自定义名称
- 选项列表（picklist）值必须完全匹配（区分大小写）

**限流**：
- API 调用限制取决于你的 Zoho CRM 套餐
- 免费版：5000 次 API 调用/天；企业版：25000+/天
- 在批量操作之间增加延时
- 监控 429 响应并遵守限流响应头

**数据格式**：
- 日期：'yyyy-MM-dd' 格式
- 日期时间：'yyyy-MM-ddTHH:mm:ss+HH:mm' 格式
- 货币：不带格式的数值
- 电话：字符串值（不强制特定格式）

**模块访问**：
- 访问权限取决于用户角色和档案权限
- 在你的 CRM 设置中，某些模块可能被隐藏或受限
- 自定义模块具有自定义的 API 名称

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|------------|
| 列出模块 | ZOHO_LIST_MODULES | （无） |
| 获取模块字段 | ZOHO_GET_MODULE_FIELDS | module |
| 搜索记录 | ZOHO_SEARCH_ZOHO_RECORDS | module, criteria |
| 获取记录 | ZOHO_GET_ZOHO_RECORDS | module, fields, per_page, page |
| 创建记录 | ZOHO_CREATE_ZOHO_RECORD | module, data |
| 更新记录 | ZOHO_UPDATE_ZOHO_RECORD | module, record_id, data |
| 转换线索 | ZOHO_CONVERT_ZOHO_LEAD | lead_id, deal, account, contact |
| 创建标签 | ZOHO_CREATE_ZOHO_TAG | module, tag_name |
| 更新关联记录 | ZOHO_UPDATE_RELATED_RECORDS | module, record_id, related_module, data |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为针对特定环境的验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
