---
name: shopify-automation
description: "通过 Rube MCP（Composio）自动化 Shopify 操作：产品、订单、客户、库存、集合。始终先搜索工具以获取当前 schema。触发词：Shopify自动化、Shopify API、产品管理、订单管理、库存管理、Shopify集成、Composio、Rube MCP"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Shopify 自动化

通过 Composio 的 Shopify 工具包（Rube MCP）自动化 Shopify 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 toolkit `shopify` 的活跃 Shopify 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用 toolkit `shopify` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按返回的认证链接完成 Shopify OAuth
4. 在运行任何工作流前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 管理产品

**适用场景**：用户想要列出、搜索、创建或管理产品

**工具调用序列**：
1. `SHOPIFY_GET_PRODUCTS` / `SHOPIFY_GET_PRODUCTS_PAGINATED` - 列出产品 [可选]
2. `SHOPIFY_GET_PRODUCT` - 获取单个产品详情 [可选]
3. `SHOPIFY_BULK_CREATE_PRODUCTS` - 批量创建产品 [可选]
4. `SHOPIFY_GET_PRODUCTS_COUNT` - 获取产品数量 [可选]

**关键参数**：
- `product_id`：用于单个检索的产品 ID
- `title`：产品标题
- `vendor`：产品供应商
- `status`：'active'、'draft' 或 'archived'

**注意事项**：
- 大型目录的分页结果需要使用游标分页
- 产品变体嵌套在产品对象内部

### 2. 管理订单

**适用场景**：用户想要列出、搜索或查看订单

**工具调用序列**：
1. `SHOPIFY_GET_ORDERS_WITH_FILTERS` - 带过滤条件列出订单 [必需]
2. `SHOPIFY_GET_ORDER` - 获取单个订单详情 [可选]
3. `SHOPIFY_GET_FULFILLMENT` - 获取履约详情 [可选]
4. `SHOPIFY_GET_FULFILLMENT_EVENTS` - 跟踪履约事件 [可选]

**关键参数**：
- `status`：订单状态过滤（'any'、'open'、'closed'、'cancelled'）
- `financial_status`：支付状态过滤
- `fulfillment_status`：履约状态过滤
- `order_id`：用于单个检索的订单 ID
- `created_at_min`/`created_at_max`：日期范围过滤

**注意事项**：
- 订单 ID 是数字；API 调用使用字符串格式
- 默认订单列表可能不包含所有状态；使用 'any' 获取全部

### 3. 管理客户

**适用场景**：用户想要列出或搜索客户

**工具调用序列**：
1. `SHOPIFY_GET_ALL_CUSTOMERS` - 列出所有客户 [必需]

**关键参数**：
- `limit`：每页客户数
- `since_id`：分页游标

**注意事项**：
- 客户数据包含订单数和消费总额
- 大型客户列表需要分页

### 4. 管理集合

**适用场景**：用户想要管理产品集合

**工具调用序列**：
1. `SHOPIFY_GET_SMART_COLLECTIONS` - 列出智能集合 [可选]
2. `SHOPIFY_GET_SMART_COLLECTION_BY_ID` - 获取集合详情 [可选]
3. `SHOPIFY_CREATE_SMART_COLLECTIONS` - 创建智能集合 [可选]
4. `SHOPIFY_ADD_PRODUCT_TO_COLLECTION` - 将产品添加到集合 [可选]
5. `SHOPIFY_GET_PRODUCTS_IN_COLLECTION` - 列出集合中的产品 [可选]

**关键参数**：
- `collection_id`：集合 ID
- `product_id`：要添加到集合的产品 ID
- `rules`：智能集合的自动包含规则

**注意事项**：
- 智能集合根据规则自动填充；手动集合使用 custom collections API
- 集合计数端点提供近似计数

### 5. 管理库存

**适用场景**：用户想要检查或管理库存水平

**工具调用序列**：
1. `SHOPIFY_GET_INVENTORY_LEVELS` / `SHOPIFY_RETRIEVES_A_LIST_OF_INVENTORY_LEVELS` - 检查库存 [必需]
2. `SHOPIFY_LIST_LOCATION` - 列出店铺位置 [可选]

**关键参数**：
- `inventory_item_ids`：要检查的库存项 ID
- `location_ids`：按位置过滤

**注意事项**：
- 库存按每个变体的每个位置跟踪
- 多位置店铺需要 location_ids

## 常用模式

### 分页

- 使用 `limit` 和 `page_info` 游标进行分页
- 检查响应中的 `next` 链接头
- 持续直到没有更多页面

### GraphQL 查询

用于高级操作：
```
1. 使用自定义查询调用 SHOPIFY_GRAPH_QL_QUERY
2. 从 data 对象解析响应
```

## 已知陷阱

**API 版本控制**：
- Shopify REST API 有版本化端点
- 某些功能需要特定 API 版本

**速率限制**：
- REST API：标准套餐每秒 2 个请求
- GraphQL：每秒 1000 点

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出产品 | SHOPIFY_GET_PRODUCTS | （过滤器） |
| 获取产品 | SHOPIFY_GET_PRODUCT | product_id |
| 产品分页 | SHOPIFY_GET_PRODUCTS_PAGINATED | limit, page_info |
| 批量创建 | SHOPIFY_BULK_CREATE_PRODUCTS | products |
| 产品计数 | SHOPIFY_GET_PRODUCTS_COUNT | （无） |
| 列出订单 | SHOPIFY_GET_ORDERS_WITH_FILTERS | status, financial_status |
| 获取订单 | SHOPIFY_GET_ORDER | order_id |
| 列出客户 | SHOPIFY_GET_ALL_CUSTOMERS | limit |
| 店铺详情 | SHOPIFY_GET_SHOP_DETAILS | （无） |
| 验证访问 | SHOPIFY_VALIDATE_ACCESS | （无） |
| 智能集合 | SHOPIFY_GET_SMART_COLLECTIONS | （无） |
| 集合中的产品 | SHOPIFY_GET_PRODUCTS_IN_COLLECTION | collection_id |
| 库存水平 | SHOPIFY_GET_INVENTORY_LEVELS | inventory_item_ids |
| 位置 | SHOPIFY_LIST_LOCATION | （无） |
| 履约 | SHOPIFY_GET_FULFILLMENT | order_id, fulfillment_id |
| GraphQL | SHOPIFY_GRAPH_QL_QUERY | query |
| 批量查询 | SHOPIFY_BULK_QUERY_OPERATION | query |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出作为环境特定验证、测试或专家评审的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清