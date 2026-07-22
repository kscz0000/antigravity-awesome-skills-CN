---
name: pipedrive-automation
description: "通过 Rube MCP (Composio) 自动化 Pipedrive CRM 操作，包括交易、联系人、组织、活动、备注和管道管理。始终先搜索工具获取当前 schema。触发词：Pipedrive自动化、CRM自动化、交易管理、管道管理、联系人管理、活动调度、Pipedrive操作、Composio Pipedrive"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Pipedrive 自动化

通过 Composio 的 Pipedrive 工具包自动化 Pipedrive CRM 工作流，包括交易管理、联系人和组织操作、活动调度、备注以及管道/阶段查询。

## 前提条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与工具包 `pipedrive` 建立 Pipedrive 活跃连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `pipedrive` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Pipedrive OAuth
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 创建和管理交易

**使用时机**：用户想要创建新交易、更新现有交易或查看销售管道中的交易详情。

**工具调用顺序**：
1. `PIPEDRIVE_SEARCH_ORGANIZATIONS` - 查找要关联到交易的现有组织 [可选]
2. `PIPEDRIVE_ADD_AN_ORGANIZATION` - 如果未找到则创建组织 [可选]
3. `PIPEDRIVE_SEARCH_PERSONS` - 查找要关联的现有联系人 [可选]
4. `PIPEDRIVE_ADD_A_PERSON` - 如果未找到则创建联系人 [可选]
5. `PIPEDRIVE_GET_ALL_PIPELINES` - 解析管道 ID [前置条件]
6. `PIPEDRIVE_GET_ALL_STAGES` - 解析管道内的阶段 ID [前置条件]
7. `PIPEDRIVE_ADD_A_DEAL` - 创建带有标题、金额、org_id、person_id、stage_id 的交易 [必需]
8. `PIPEDRIVE_UPDATE_A_DEAL` - 创建后修改交易属性 [可选]
9. `PIPEDRIVE_ADD_A_PRODUCT_TO_A_DEAL` - 附加行项目/产品 [可选]

**关键参数**：
- `title`：交易标题（创建时必需）
- `value`：交易金额
- `currency`：3 字母 ISO 货币代码（如 "USD"）
- `pipeline_id` / `stage_id`：管道位置的数字 ID
- `org_id` / `person_id`：关联到组织和联系人
- `status`："open"、"won" 或 "lost"
- `expected_close_date`：格式 YYYY-MM-DD

**注意事项**：
- `title` 是 `PIPEDRIVE_ADD_A_DEAL` 唯一必需的字段；其他均为可选
- 自定义字段在响应中显示为长哈希键；使用 dealFields 端点映射它们
- `PIPEDRIVE_UPDATE_A_DEAL` 需要交易的数字 `id`
- 将 `status` 设为 "lost" 时还需要提供 `lost_reason`

### 2. 管理联系人（人员和组织）

**使用时机**：用户想要在 Pipedrive 中创建、更新、搜索或列出联系人和公司。

**工具调用顺序**：
1. `PIPEDRIVE_SEARCH_PERSONS` - 按姓名、邮箱或电话搜索现有人员 [前置条件]
2. `PIPEDRIVE_ADD_A_PERSON` - 如果未找到则创建新联系人 [必需]
3. `PIPEDRIVE_UPDATE_A_PERSON` - 修改现有联系人详情 [可选]
4. `PIPEDRIVE_GET_DETAILS_OF_A_PERSON` - 获取完整联系人记录 [可选]
5. `PIPEDRIVE_SEARCH_ORGANIZATIONS` - 搜索现有组织 [前置条件]
6. `PIPEDRIVE_ADD_AN_ORGANIZATION` - 如果未找到则创建新组织 [必需]
7. `PIPEDRIVE_UPDATE_AN_ORGANIZATION` - 修改组织属性 [可选]
8. `PIPEDRIVE_GET_DETAILS_OF_AN_ORGANIZATION` - 获取完整组织记录 [可选]

**关键参数**：
- `name`：人员和组织创建时均必需
- `email`：包含 `value`、`label`、`primary` 字段的对象数组（用于人员）
- `phone`：包含 `value`、`label`、`primary` 字段的对象数组（用于人员）
- `org_id`：将人员关联到组织
- `visible_to`：1 = 仅所有者，3 = 全公司
- `term`：SEARCH_PERSONS / SEARCH_ORGANIZATIONS 的搜索词（最少 2 个字符）

**注意事项**：
- `PIPEDRIVE_ADD_AN_ORGANIZATION` 可能自动与现有组织合并；检查 `response.additional_data.didMerge`
- 邮箱和电话字段是对象数组，不是纯字符串：`[{"value": "test@example.com", "label": "work", "primary": true}]`
- `PIPEDRIVE_SEARCH_PERSONS` 不支持 `*` 或 `@` 等通配符；使用 `PIPEDRIVE_GET_ALL_PERSONS` 列出所有
- 通过 `PIPEDRIVE_DELETE_A_PERSON` 或 `PIPEDRIVE_DELETE_AN_ORGANIZATION` 删除是软删除，保留 30 天后永久删除

### 3. 调度和跟踪活动

**使用时机**：用户想要创建与交易、联系人或组织关联的通话、会议、任务或其他活动。

**工具调用顺序**：
1. `PIPEDRIVE_SEARCH_PERSONS` 或 `PIPEDRIVE_GET_DETAILS_OF_A_DEAL` - 解析关联实体 ID [前置条件]
2. `PIPEDRIVE_ADD_AN_ACTIVITY` - 创建带有主题、类型、截止日期的活动 [必需]
3. `PIPEDRIVE_UPDATE_AN_ACTIVITY` - 修改活动详情或标记为已完成 [可选]
4. `PIPEDRIVE_GET_DETAILS_OF_AN_ACTIVITY` - 获取活动记录 [可选]
5. `PIPEDRIVE_GET_ALL_ACTIVITIES_ASSIGNED_TO_A_PARTICULAR_USER` - 列出用户的活动 [可选]

**关键参数**：
- `subject`：活动标题（必需）
- `type`：活动类型键字符串，如 "call"、"meeting"、"task"、"email"（必需）
- `due_date`：格式 YYYY-MM-DD
- `due_time`：格式 HH:MM
- `duration`：格式 HH:MM（如 "00:30" 表示 30 分钟）
- `deal_id` / `person_id` / `org_id`：关联到相关实体
- `done`：0 = 未完成，1 = 已完成

**注意事项**：
- `PIPEDRIVE_ADD_AN_ACTIVITY` 的 `subject` 和 `type` 都是必需的
- `type` 必须匹配账户中已有的 ActivityTypes key_string
- `done` 是整数（0 或 1），不是布尔值
- 响应的 additional_data 中包含 `more_activities_scheduled_in_context`

### 4. 添加和管理备注

**使用时机**：用户想要将备注附加到交易、人员、组织、线索或项目。

**工具调用顺序**：
1. `PIPEDRIVE_SEARCH_PERSONS` 或 `PIPEDRIVE_GET_DETAILS_OF_A_DEAL` - 解析实体 ID [前置条件]
2. `PIPEDRIVE_ADD_A_NOTE` - 创建关联到实体的 HTML 内容备注 [必需]
3. `PIPEDRIVE_UPDATE_A_NOTE` - 修改备注内容 [可选]
4. `PIPEDRIVE_GET_ALL_NOTES` - 按实体筛选列出备注 [可选]
5. `PIPEDRIVE_GET_ALL_COMMENTS_FOR_A_NOTE` - 获取备注的评论 [可选]

**关键参数**：
- `content`：HTML 格式的备注正文（必需）
- `deal_id` / `person_id` / `org_id` / `lead_id` / `project_id`：至少需要一个实体关联
- `pinned_to_deal_flag` / `pinned_to_person_flag`：列出时筛选置顶备注

**注意事项**：
- `content` 是必需的且支持 HTML；纯文本可用但会在服务端被清理
- 必须提供 `deal_id`、`person_id`、`org_id`、`lead_id` 或 `project_id` 中的至少一个
- `PIPEDRIVE_GET_ALL_NOTES` 默认返回所有实体的备注；使用实体 ID 参数筛选

### 5. 查询管道和阶段

**使用时机**：用户想要查看销售管道、阶段或管道/阶段内的交易。

**工具调用顺序**：
1. `PIPEDRIVE_GET_ALL_PIPELINES` - 列出所有管道及其 ID [必需]
2. `PIPEDRIVE_GET_ONE_PIPELINE` - 获取特定管道的详情和交易摘要 [可选]
3. `PIPEDRIVE_GET_ALL_STAGES` - 列出所有阶段，可按管道筛选 [必需]
4. `PIPEDRIVE_GET_ONE_STAGE` - 获取特定阶段的详情 [可选]
5. `PIPEDRIVE_GET_DEALS_IN_A_PIPELINE` - 列出管道中跨阶段的交易 [可选]
6. `PIPEDRIVE_GET_DEALS_IN_A_STAGE` - 列出特定阶段的交易 [可选]

**关键参数**：
- `id`：管道或阶段 ID（单项端点必需）
- `pipeline_id`：按管道筛选阶段
- `totals_convert_currency`：3 字母货币代码或 "default_currency" 用于转换金额
- `get_summary`：设为 1 获取管道响应中的交易摘要

**注意事项**：
- `PIPEDRIVE_GET_ALL_PIPELINES` 不接受参数；返回所有管道
- `PIPEDRIVE_GET_ALL_STAGES` 除非指定 `pipeline_id`，否则返回所有管道的阶段
- 管道摘要中的交易计数仅在设置 `totals_convert_currency` 时使用 `per_stages_converted`

## 常用模式

### ID 解析
操作前始终将显示名称解析为数字 ID：
- **组织名称 -> org_id**：使用 `term` 参数调用 `PIPEDRIVE_SEARCH_ORGANIZATIONS`
- **人员名称 -> person_id**：使用 `term` 参数调用 `PIPEDRIVE_SEARCH_PERSONS`
- **管道名称 -> pipeline_id**：调用 `PIPEDRIVE_GET_ALL_PIPELINES` 后按名称匹配
- **阶段名称 -> stage_id**：使用 `pipeline_id` 调用 `PIPEDRIVE_GET_ALL_STAGES` 后按名称匹配

### 分页
大多数列表端点使用基于偏移的分页：
- 使用 `start`（偏移量）和 `limit`（页大小）参数
- 检查 `additional_data.pagination.more_items_in_collection` 判断是否还有更多页
- 使用 `additional_data.pagination.next_start` 作为下一页的 `start` 值
- 部分端点默认 limit 约为 500；显式设置以实现可预测的分页

## 已知注意事项

### ID 格式
- 所有实体 ID（交易、人员、组织、活动、管道、阶段）均为数字整数
- 线索 ID 是 UUID 字符串，不是整数
- 自定义字段键是长字母数字哈希值（如 "a1b2c3d4e5f6..."）

### 速率限制
- Pipedrive 执行按公司的 API 速率限制；批量操作应控制节奏
- `PIPEDRIVE_GET_ALL_PERSONS` 和 `PIPEDRIVE_GET_ALL_ORGANIZATIONS` 可能返回大数据集；始终使用分页

### 参数特性
- 人员的邮箱和电话是对象数组，不是纯字符串
- `visible_to` 是数字：1 = 仅所有者，3 = 全公司，5 = 特定组
- 活动的 `done` 是整数 0/1，不是布尔值 true/false
- 组织创建可能静默自动合并重复项；检查响应中的 `didMerge`
- `PIPEDRIVE_SEARCH_PERSONS` 至少需要 2 个字符且不支持通配符

### 响应结构
- 自定义字段在响应中显示为哈希键；通过相应的 Fields 端点映射
- 响应在包装执行中通常嵌套在 `response.data.data` 下
- 搜索结果在 `response.data.items` 下，不在顶层

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 创建交易 | `PIPEDRIVE_ADD_A_DEAL` | `title`, `value`, `org_id`, `stage_id` |
| 更新交易 | `PIPEDRIVE_UPDATE_A_DEAL` | `id`, `status`, `value`, `stage_id` |
| 获取交易详情 | `PIPEDRIVE_GET_DETAILS_OF_A_DEAL` | `id` |
| 搜索人员 | `PIPEDRIVE_SEARCH_PERSONS` | `term`, `fields` |
| 添加人员 | `PIPEDRIVE_ADD_A_PERSON` | `name`, `email`, `phone`, `org_id` |
| 更新人员 | `PIPEDRIVE_UPDATE_A_PERSON` | `id`, `name`, `email` |
| 获取人员详情 | `PIPEDRIVE_GET_DETAILS_OF_A_PERSON` | `id` |
| 列出所有人员 | `PIPEDRIVE_GET_ALL_PERSONS` | `start`, `limit`, `filter_id` |
| 搜索组织 | `PIPEDRIVE_SEARCH_ORGANIZATIONS` | `term`, `fields` |
| 添加组织 | `PIPEDRIVE_ADD_AN_ORGANIZATION` | `name`, `visible_to` |
| 更新组织 | `PIPEDRIVE_UPDATE_AN_ORGANIZATION` | `id`, `name`, `address` |
| 获取组织详情 | `PIPEDRIVE_GET_DETAILS_OF_AN_ORGANIZATION` | `id` |
| 添加活动 | `PIPEDRIVE_ADD_AN_ACTIVITY` | `subject`, `type`, `due_date`, `deal_id` |
| 更新活动 | `PIPEDRIVE_UPDATE_AN_ACTIVITY` | `id`, `done`, `due_date` |
| 获取活动详情 | `PIPEDRIVE_GET_DETAILS_OF_AN_ACTIVITY` | `id` |
| 列出用户活动 | `PIPEDRIVE_GET_ALL_ACTIVITIES_ASSIGNED_TO_A_PARTICULAR_USER` | `user_id`, `start`, `limit` |
| 添加备注 | `PIPEDRIVE_ADD_A_NOTE` | `content`, `deal_id` 或 `person_id` |
| 列出备注 | `PIPEDRIVE_GET_ALL_NOTES` | `deal_id`, `person_id`, `start`, `limit` |
| 列出管道 | `PIPEDRIVE_GET_ALL_PIPELINES` | (无) |
| 获取管道详情 | `PIPEDRIVE_GET_ONE_PIPELINE` | `id` |
| 列出阶段 | `PIPEDRIVE_GET_ALL_STAGES` | `pipeline_id` |
| 管道中的交易 | `PIPEDRIVE_GET_DEALS_IN_A_PIPELINE` | `id`, `stage_id` |
| 阶段中的交易 | `PIPEDRIVE_GET_DEALS_IN_A_STAGE` | `id`, `start`, `limit` |
| 向交易添加产品 | `PIPEDRIVE_ADD_A_PRODUCT_TO_A_DEAL` | `id`, `product_id`, `item_price` |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
