---
name: hubspot-automation
description: "通过 Rube MCP 和 Composio 集成自动化 HubSpot CRM 操作（联系人、公司、交易、工单、属性）。触发词：HubSpot自动化、HubSpot CRM、联系人管理、公司管理、交易管道、工单搜索、自定义属性、Rube MCP、Composio HubSpot"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 HubSpot CRM 自动化

通过 Composio 的 HubSpot 工具包自动化 HubSpot CRM 工作流，包括联系人/公司管理、交易管道跟踪、工单搜索和自定义属性创建。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 HubSpot 活跃连接，工具包为 `hubspot`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `hubspot` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 HubSpot OAuth
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 创建和管理联系人

**何时使用**：用户想在 HubSpot CRM 中创建新联系人或更新现有联系人

**工具调用顺序**：
1. `HUBSPOT_GET_ACCOUNT_INFO` - 验证连接和权限（前提）
2. `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA` - 搜索现有联系人以避免重复（前提）
3. `HUBSPOT_READ_A_CRM_PROPERTY_BY_NAME` - 检查受约束值的属性元数据（可选）
4. `HUBSPOT_CREATE_CONTACT` - 创建单个联系人（必需）
5. `HUBSPOT_CREATE_CONTACTS` - 批量创建联系人，最多 100 条（替代方案）

**关键参数**：
- `HUBSPOT_CREATE_CONTACT`：`properties` 对象，包含 `email`、`firstname`、`lastname`、`phone`、`company`
- `HUBSPOT_CREATE_CONTACTS`：`inputs` 数组，元素为 `{properties}` 对象，每批最多 100 条
- `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`：`filterGroups` 数组，包含 `{filters: [{propertyName, operator, value}]}`，`properties` 数组指定要返回的字段

**注意事项**：
- 每批最多 100 条记录；大批量导入需分块处理
- 使用错误的属性名或枚举值会返回 400 'Property values were not valid'
- 创建前务必先搜索以避免重复
- `GET_ACCOUNT_INFO` 返回认证错误意味着后续所有调用都会失败

### 2. 管理公司

**何时使用**：用户想创建、搜索或更新公司记录

**工具调用顺序**：
1. `HUBSPOT_SEARCH_COMPANIES` - 搜索现有公司（前提）
2. `HUBSPOT_CREATE_COMPANIES` - 批量创建公司，最多 100 条（必需）
3. `HUBSPOT_UPDATE_COMPANIES` - 批量更新现有公司（替代方案）
4. `HUBSPOT_GET_COMPANY` - 获取单个公司详情（可选）
5. `HUBSPOT_BATCH_READ_COMPANIES_BY_PROPERTIES` - 按属性值批量读取公司（可选）

**关键参数**：
- `HUBSPOT_CREATE_COMPANIES`：`inputs` 数组，元素为 `{properties}` 对象，最多 100 条
- `HUBSPOT_SEARCH_COMPANIES`：`filterGroups`、`properties`、`sorts`、`limit`、`after`（分页游标）

**注意事项**：
- 每批最多 100 条；大批量需分块处理
- 立即存储返回的 ID 以供后续操作使用
- 属性值必须与内部名称精确匹配，而非显示标签

### 3. 管理交易和管道

**何时使用**：用户想搜索交易、查看管道阶段或跟踪交易进度

**工具调用顺序**：
1. `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE` - 映射管道和阶段 ID/名称（前提）
2. `HUBSPOT_SEARCH_DEALS` - 使用筛选条件搜索交易（必需）
3. `HUBSPOT_RETRIEVE_PIPELINE_STAGES` - 获取单个管道的阶段详情（可选）
4. `HUBSPOT_RETRIEVE_OWNERS` - 获取负责人/代表详情（可选）
5. `HUBSPOT_GET_DEAL` - 获取单个交易详情（可选）
6. `HUBSPOT_LIST_DEALS` - 不带筛选条件列出所有交易（兜底方案）

**关键参数**：
- `HUBSPOT_SEARCH_DEALS`：`filterGroups`，支持对 `pipeline`、`dealstage`、`createdate`、`closedate`、`hubspot_owner_id` 的筛选；`properties`、`sorts`、`limit`、`after`
- `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE`：`objectType` 设为 `'deals'`

**注意事项**：
- 结果嵌套在 `response.data.results` 下；属性值通常为字符串（金额、日期）
- 阶段 ID 可能是可读字符串或不透明的数字 ID；使用 `label` 字段进行显示
- 筛选条件必须使用内部属性名（`pipeline`、`dealstage`、`createdate`），而非显示名称
- 通过 `paging.next.after` 进行分页，直到该字段不存在

### 4. 搜索和筛选工单

**何时使用**：用户想按状态、日期或条件查找支持工单

**工具调用顺序**：
1. `HUBSPOT_SEARCH_TICKETS` - 使用 filterGroups 搜索（必需）
2. `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` - 发现可用的属性名称（兜底方案）
3. `HUBSPOT_GET_TICKET` - 获取单个工单详情（可选）
4. `HUBSPOT_GET_TICKETS` - 按 ID 批量获取工单（可选）

**关键参数**：
- `HUBSPOT_SEARCH_TICKETS`：`filterGroups`、`properties`（仅返回列出的字段）、`sorts`、`limit`、`after`

**注意事项**：
- 错误的 `propertyName`/`operator` 会返回零结果但不报错
- 日期筛选可能需要 epoch 毫秒边界；混用格式会导致不匹配
- 仅返回 `properties` 数组中的字段；遗漏字段会导致下游逻辑出错
- 使用 `READ_ALL_PROPERTIES` 发现精确的内部属性名

### 5. 创建和管理自定义属性

**何时使用**：用户想为 CRM 对象添加自定义字段

**工具调用顺序**：
1. `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` - 列出现有属性（前提）
2. `HUBSPOT_READ_PROPERTY_GROUPS_FOR_OBJECT_TYPE` - 列出属性分组（可选）
3. `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE` - 创建单个属性（必需）
4. `HUBSPOT_CREATE_BATCH_OF_PROPERTIES` - 批量创建属性（替代方案）
5. `HUBSPOT_UPDATE_SPECIFIC_CRM_PROPERTY` - 更新现有属性定义（可选）

**关键参数**：
- `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE`：`objectType`、`name`、`label`、`type`（string/number/date/enumeration）、`fieldType`、`groupName`、`options`（用于枚举类型）

**注意事项**：
- 属性名创建后不可更改；请谨慎选择
- 枚举选项必须预先定义 `value` 和 `label`
- 分组必须先存在才能将属性分配给它

## 常用模式

### ID 解析
- **属性显示名称 → 内部名称**：使用 `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE`
- **管道名称 → 管道 ID**：使用 `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE`
- **阶段名称 → 阶段 ID**：从管道阶段响应中提取
- **负责人名称 → 负责人 ID**：使用 `HUBSPOT_RETRIEVE_OWNERS`

### 分页
- 搜索端点使用基于游标的分页
- 沿 `paging.next.after` 继续，直到该字段不存在
- 典型限制：每页 100 条记录
- 将上次响应中的 `after` 值传入以获取下一页

### 批量操作
- 大多数创建/更新端点支持批量操作，每次调用最多 100 条记录
- 对于更大的数据集，按 100 条一组分块
- 在继续操作前存储每批返回的 ID
- 使用批量端点（`CREATE_CONTACTS`、`CREATE_COMPANIES`、`UPDATE_COMPANIES`）而非单条记录端点以提高效率

## 已知注意事项

- **属性名称**：所有搜索/筛选端点使用内部属性名，而非显示标签。始终调用 `READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` 发现正确的名称
- **批量限制**：每次批量操作最多 100 条记录。更大的数据集必须分块处理
- **响应结构**：搜索结果嵌套在 `response.data.results` 下，属性值为字符串
- **日期格式**：日期属性根据端点不同可能是 epoch 毫秒或 ISO 字符串。需防御性解析
- **不可变名称**：属性名创建后无法更改。请仔细规划命名规范
- **游标分页**：使用 `paging.next.after` 游标，而非页码。持续请求直到 `after` 不存在
- **防止重复**：创建联系人/公司前务必先搜索以避免重复
- **认证验证**：首先运行 `HUBSPOT_GET_ACCOUNT_INFO`；认证失败会级联影响所有后续调用

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 创建联系人 | `HUBSPOT_CREATE_CONTACT` | `properties: {email, firstname, lastname}` |
| 批量创建联系人 | `HUBSPOT_CREATE_CONTACTS` | `inputs: [{properties}]`（最多 100 条） |
| 搜索联系人 | `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA` | `filterGroups, properties, limit, after` |
| 创建公司 | `HUBSPOT_CREATE_COMPANIES` | `inputs: [{properties}]`（最多 100 条） |
| 搜索公司 | `HUBSPOT_SEARCH_COMPANIES` | `filterGroups, properties, after` |
| 搜索交易 | `HUBSPOT_SEARCH_DEALS` | `filterGroups, properties, after` |
| 获取管道 | `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE` | `objectType: 'deals'` |
| 搜索工单 | `HUBSPOT_SEARCH_TICKETS` | `filterGroups, properties, after` |
| 列出属性 | `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` | `objectType` |
| 创建属性 | `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE` | `objectType, name, label, type, fieldType` |
| 获取负责人 | `HUBSPOT_RETRIEVE_OWNERS` | 无 |
| 验证连接 | `HUBSPOT_GET_ACCOUNT_INFO` | 无 |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失，请停止并请求澄清。
