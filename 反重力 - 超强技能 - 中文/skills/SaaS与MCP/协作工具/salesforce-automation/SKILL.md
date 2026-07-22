---
name: salesforce-automation
description: "通过 Rube MCP (Composio) 自动化 Salesforce 任务：线索、联系人、账户、商机、SOQL 查询。始终先搜索工具获取当前模式。触发词：Salesforce自动化、Salesforce操作、线索管理、联系人管理、商机管理、SOQL查询、Salesforce MCP、Composio Salesforce"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Salesforce 自动化

通过 Composio 的 Salesforce 工具包和 Rube MCP 自动化 Salesforce CRM 操作。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Salesforce 连接，工具包为 `salesforce`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 使用工具包 `salesforce` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Salesforce OAuth
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 管理线索

**适用场景**：用户想要创建、搜索、更新或列出线索

**工具序列**：
1. `SALESFORCE_SEARCH_LEADS` - 按条件搜索线索 [可选]
2. `SALESFORCE_LIST_LEADS` - 列出所有线索 [可选]
3. `SALESFORCE_CREATE_LEAD` - 创建新线索 [可选]
4. `SALESFORCE_UPDATE_LEAD` - 更新线索字段 [可选]
5. `SALESFORCE_ADD_LEAD_TO_CAMPAIGN` - 将线索添加到营销活动 [可选]
6. `SALESFORCE_APPLY_LEAD_ASSIGNMENT_RULES` - 应用分配规则 [可选]

**关键参数**：
- `LastName`：创建线索时必填
- `Company`：创建线索时必填
- `Email`、`Phone`、`Title`：常用线索字段
- `lead_id`：用于更新的线索 ID
- `campaign_id`：营销活动操作的营销活动 ID

**注意事项**：
- LastName 和 Company 是创建线索时的必填字段
- 线索 ID 为 15 或 18 位字符的 Salesforce ID

### 2. 管理联系人和账户

**适用场景**：用户想要管理联系人及其关联的账户

**工具序列**：
1. `SALESFORCE_SEARCH_CONTACTS` - 搜索联系人 [可选]
2. `SALESFORCE_LIST_CONTACTS` - 列出联系人 [可选]
3. `SALESFORCE_CREATE_CONTACT` - 创建新联系人 [可选]
4. `SALESFORCE_SEARCH_ACCOUNTS` - 搜索账户 [可选]
5. `SALESFORCE_CREATE_ACCOUNT` - 创建新账户 [可选]
6. `SALESFORCE_ASSOCIATE_CONTACT_TO_ACCOUNT` - 将联系人关联到账户 [可选]

**关键参数**：
- `LastName`：创建联系人时必填
- `Name`：创建账户时的账户名称
- `AccountId`：要关联到联系人的账户 ID
- `contact_id`、`account_id`：关联操作所需的 ID

**注意事项**：
- 联系人至少需要 LastName
- 账户关联需要有效的联系人和账户 ID

### 3. 管理商机

**适用场景**：用户想要跟踪和管理销售商机

**工具序列**：
1. `SALESFORCE_SEARCH_OPPORTUNITIES` - 搜索商机 [可选]
2. `SALESFORCE_LIST_OPPORTUNITIES` - 列出所有商机 [可选]
3. `SALESFORCE_GET_OPPORTUNITY` - 获取商机详情 [可选]
4. `SALESFORCE_CREATE_OPPORTUNITY` - 创建新商机 [可选]
5. `SALESFORCE_RETRIEVE_OPPORTUNITIES_DATA` - 检索商机数据 [可选]

**关键参数**：
- `Name`：商机名称（必填）
- `StageName`：销售阶段（必填）
- `CloseDate`：预计结单日期（必填）
- `Amount`：交易金额
- `AccountId`：关联账户

**注意事项**：
- Name、StageName 和 CloseDate 是创建时的必填字段
- 阶段名称必须与 Salesforce 中配置的完全一致

### 4. 运行 SOQL 查询

**适用场景**：用户想要使用自定义 SOQL 查询 Salesforce 数据

**工具序列**：
1. `SALESFORCE_RUN_SOQL_QUERY` / `SALESFORCE_QUERY` - 执行 SOQL [必填]

**关键参数**：
- `query`：SOQL 查询字符串

**注意事项**：
- SOQL 语法与 SQL 不同；使用 Salesforce 对象和字段的 API 名称
- 字段 API 名称可能与显示标签不同（例如 `Account.Name` 而非 `Account Name`）
- 大数据集的结果会分页返回

### 5. 管理任务

**适用场景**：用户想要创建、搜索、更新或完成任务

**工具序列**：
1. `SALESFORCE_SEARCH_TASKS` - 搜索任务 [可选]
2. `SALESFORCE_UPDATE_TASK` - 更新任务字段 [可选]
3. `SALESFORCE_COMPLETE_TASK` - 将任务标记为已完成 [可选]

**关键参数**：
- `task_id`：用于更新的任务 ID
- `Status`：任务状态值
- `Subject`：任务主题

**注意事项**：
- 任务状态值必须与 Salesforce 中的选项列表一致

## 常用模式

### SOQL 语法

**基本查询**：
```
SELECT Id, Name, Email FROM Contact WHERE LastName = 'Smith'
```

**关联查询**：
```
SELECT Id, Name, Account.Name FROM Contact WHERE Account.Industry = 'Technology'
```

**日期过滤**：
```
SELECT Id, Name FROM Lead WHERE CreatedDate = TODAY
SELECT Id, Name FROM Opportunity WHERE CloseDate = NEXT_MONTH
```

### 分页

- 大结果集的 SOQL 查询会返回分页令牌
- 使用 `SALESFORCE_QUERY` 配合 nextRecordsUrl 进行分页
- 检查响应中的 `done` 字段；如果为 false，继续翻页

## 已知注意事项

**字段 API 名称**：
- 始终使用 API 名称，而非显示标签
- 自定义字段以 `__c` 后缀结尾
- 使用 SALESFORCE_GET_ALL_CUSTOM_OBJECTS 发现自定义对象

**ID 格式**：
- Salesforce ID 为 15 位（区分大小写）或 18 位（不区分大小写）字符
- 大多数操作接受两种格式

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 创建线索 | SALESFORCE_CREATE_LEAD | LastName, Company |
| 搜索线索 | SALESFORCE_SEARCH_LEADS | query |
| 列出线索 | SALESFORCE_LIST_LEADS | (filters) |
| 更新线索 | SALESFORCE_UPDATE_LEAD | lead_id, fields |
| 创建联系人 | SALESFORCE_CREATE_CONTACT | LastName |
| 搜索联系人 | SALESFORCE_SEARCH_CONTACTS | query |
| 创建账户 | SALESFORCE_CREATE_ACCOUNT | Name |
| 搜索账户 | SALESFORCE_SEARCH_ACCOUNTS | query |
| 关联联系人 | SALESFORCE_ASSOCIATE_CONTACT_TO_ACCOUNT | contact_id, account_id |
| 创建商机 | SALESFORCE_CREATE_OPPORTUNITY | Name, StageName, CloseDate |
| 获取商机 | SALESFORCE_GET_OPPORTUNITY | opportunity_id |
| 搜索商机 | SALESFORCE_SEARCH_OPPORTUNITIES | query |
| 运行 SOQL | SALESFORCE_RUN_SOQL_QUERY | query |
| 查询 | SALESFORCE_QUERY | query |
| 搜索任务 | SALESFORCE_SEARCH_TASKS | query |
| 更新任务 | SALESFORCE_UPDATE_TASK | task_id, fields |
| 完成任务 | SALESFORCE_COMPLETE_TASK | task_id |
| 获取用户信息 | SALESFORCE_GET_USER_INFO | (none) |
| 自定义对象 | SALESFORCE_GET_ALL_CUSTOM_OBJECTS | (none) |
| 创建记录 | SALESFORCE_CREATE_A_RECORD | object_type, fields |
| 转移所有权 | SALESFORCE_MASS_TRANSFER_OWNERSHIP | records, new_owner |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
