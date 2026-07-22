---
name: square-automation
description: "通过 Rube MCP（Composio）自动化 Square 任务：支付、订单、发票、门店管理。务必先搜索工具获取当前 schema。触发词：Square自动化、Square支付、订单管理、发票管理、Rube MCP、Composio"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Square 自动化

通过 Composio 的 Square 工具包（Rube MCP）自动化 Square 支付处理、订单管理和发票操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 toolkit `square` 建立活跃的 Square 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 使用 toolkit `square` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 Square OAuth
4. 在运行任何工作流之前确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出和监控支付

**适用场景**：用户想查看支付历史或检查支付状态

**工具调用顺序**：
1. `SQUARE_LIST_PAYMENTS` - 使用可选过滤器检索支付记录 [必需]
2. `SQUARE_CANCEL_PAYMENT` - 如有需要取消待处理的支付 [可选]

**关键参数**：
- `begin_time` / `end_time`：RFC 3339 格式的时间戳，用于日期范围过滤
- `sort_order`：'ASC' 或 'DESC'，按时间排序
- `cursor`：上一次响应中的分页游标
- `location_id`：按特定门店过滤支付

**注意事项**：
- 时间戳必须是 RFC 3339 格式（例如 '2024-01-01T00:00:00Z'）
- 大结果集需要分页；持续跟随 `cursor` 直到其为空
- 只有待处理的支付可以取消；已完成的支付需要退款
- `SQUARE_CANCEL_PAYMENT` 需要从列表结果中获取精确的 `payment_id`

### 2. 搜索和管理订单

**适用场景**：用户想按条件查找订单或更新订单详情

**工具调用顺序**：
1. `SQUARE_LIST_LOCATIONS` - 获取门店 ID 用于过滤 [前置条件]
2. `SQUARE_SEARCH_ORDERS` - 使用过滤器搜索订单 [必需]
3. `SQUARE_RETRIEVE_ORDER` - 获取特定订单的完整详情 [可选]
4. `SQUARE_UPDATE_ORDER` - 修改订单状态或详情 [可选]

**关键参数**：
- `location_ids`：要搜索的门店 ID 数组（搜索时必需）
- `query`：包含日期范围、状态、履约类型的搜索过滤对象
- `order_id`：用于检索/更新操作的特定订单 ID
- `cursor`：搜索结果的分页游标

**注意事项**：
- SEARCH_ORDERS 需要 `location_ids`；先从 LIST_LOCATIONS 获取 ID
- 订单状态包括：OPEN、COMPLETED、CANCELED、DRAFT
- UPDATE_ORDER 需要当前 `version` 字段以防止冲突
- 搜索结果是分页的；持续跟随 `cursor` 直到其为空

### 3. 管理门店

**适用场景**：用户想查看营业门店或获取门店详情

**工具调用顺序**：
1. `SQUARE_LIST_LOCATIONS` - 列出所有营业门店 [必需]

**关键参数**：
- 无需必需参数；返回所有可访问的门店
- 响应包含 `id`、`name`、`address`、`status`、`timezone`

**注意事项**：
- 大多数其他 Square 操作（订单、支付）都需要门店 ID
- 首次获取后始终缓存门店 ID 以避免重复调用
- 非活跃门店可能仍会出现在结果中；请检查 `status` 字段

### 4. 发票管理

**适用场景**：用户想列出、查看或取消发票

**工具调用顺序**：
1. `SQUARE_LIST_LOCATIONS` - 获取门店 ID 用于过滤 [前置条件]
2. `SQUARE_LIST_INVOICES` - 列出某门店的发票 [必需]
3. `SQUARE_GET_INVOICE` - 获取发票详细信息 [可选]
4. `SQUARE_CANCEL_INVOICE` - 取消已计划或未支付的发票 [可选]

**关键参数**：
- `location_id`：列出发票时必需
- `invoice_id`：获取/取消操作时必需
- `cursor`：列表结果的分页游标
- `limit`：每页结果数量

**注意事项**：
- LIST_INVOICES 需要 `location_id`；先通过 LIST_LOCATIONS 解析
- 只有 SCHEDULED、UNPAID 或 PARTIALLY_PAID 状态的发票可以取消
- CANCEL_INVOICE 需要发票的 `version` 以防止竞态条件
- 已取消的发票无法恢复

## 通用模式

### ID 解析

**门店名称 → 门店 ID**：
```
1. 调用 SQUARE_LIST_LOCATIONS
2. 在响应中按名称查找门店
3. 提取 id 字段（例如 'L1234ABCD'）
```

**订单查找**：
```
1. 使用 location_ids 和查询过滤器调用 SQUARE_SEARCH_ORDERS
2. 从结果中提取 order_id
3. 使用 order_id 进行 RETRIEVE_ORDER 或 UPDATE_ORDER
```

### 分页

- 检查响应中是否有 `cursor` 字段
- 在下一个请求的 `cursor` 参数中传入游标值
- 持续请求直到 `cursor` 为空或不存在
- 使用 `limit` 控制每页大小

### 日期范围过滤

- 使用 RFC 3339 格式：`2024-01-01T00:00:00Z`
- 支付：使用 `begin_time` 和 `end_time` 参数
- 订单：使用带 date_time_filter 的查询过滤器
- 所有时间戳均为 UTC 时间

## 已知注意事项

**ID 格式**：
- 门店 ID 是字母数字字符串（例如 'L1234ABCD'）
- 支付 ID 和订单 ID 是更长的字母数字字符串
- 在执行其他操作之前，始终先将门店名称解析为 ID

**版本控制**：
- UPDATE_ORDER 和 CANCEL_INVOICE 需要当前 `version` 字段
- 先获取资源以获取其当前版本
- 版本不匹配会返回 409 Conflict 错误

**速率限制**：
- Square API 对每个端点有速率限制
- 批量操作需实现退避机制
- 大数据集的分页应包含短暂延迟

**响应解析**：
- 响应可能将数据嵌套在 `data` 键下
- 金额以最小货币单位表示（美元为美分）
- 解析时需防御性处理，为可选字段设置回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出支付 | SQUARE_LIST_PAYMENTS | begin_time, end_time, location_id, cursor |
| 取消支付 | SQUARE_CANCEL_PAYMENT | payment_id |
| 搜索订单 | SQUARE_SEARCH_ORDERS | location_ids, query, cursor |
| 获取订单 | SQUARE_RETRIEVE_ORDER | order_id |
| 更新订单 | SQUARE_UPDATE_ORDER | order_id, version |
| 列出门店 | SQUARE_LIST_LOCATIONS | （无） |
| 列出发票 | SQUARE_LIST_INVOICES | location_id, cursor |
| 获取发票 | SQUARE_GET_INVOICE | invoice_id |
| 取消发票 | SQUARE_CANCEL_INVOICE | invoice_id, version |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
