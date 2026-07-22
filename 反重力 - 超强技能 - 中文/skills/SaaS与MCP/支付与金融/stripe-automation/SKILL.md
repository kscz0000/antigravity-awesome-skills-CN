---
name: stripe-automation
description: "通过 Rube MCP（Composio）自动化 Stripe 任务：客户、收款、订阅、发票、产品、退款。始终先搜索工具获取最新 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Stripe

通过 Composio 的 Stripe 工具包和 Rube MCP，自动化 Stripe 支付操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 配合 toolkit `stripe` 建立活跃的 Stripe 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `stripe`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Stripe 连接
4. 运行任何工作流前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 管理客户

**适用场景**：创建、更新、搜索或列出 Stripe 客户

**工具调用顺序**：
1. `STRIPE_SEARCH_CUSTOMERS` - 按邮箱/姓名搜索客户 [可选]
2. `STRIPE_LIST_CUSTOMERS` - 列出所有客户 [可选]
3. `STRIPE_CREATE_CUSTOMER` - 创建新客户 [可选]
4. `STRIPE_POST_CUSTOMERS_CUSTOMER` - 更新客户 [可选]

**关键参数**：
- `email`：客户邮箱
- `name`：客户姓名
- `description`：客户描述
- `metadata`：键值对元数据
- `customer`：更新时使用的客户 ID（如 'cus_xxx'）

**注意事项**：
- Stripe 允许相同邮箱创建重复客户；先搜索以避免重复
- 客户 ID 以 'cus_' 开头

### 2. 管理收款与支付

**适用场景**：创建收款、支付意向或查看收款记录

**工具调用顺序**：
1. `STRIPE_LIST_CHARGES` - 按条件列出收款 [可选]
2. `STRIPE_CREATE_PAYMENT_INTENT` - 创建支付意向 [可选]
3. `STRIPE_CONFIRM_PAYMENT_INTENT` - 确认支付意向 [可选]
4. `STRIPE_POST_CHARGES` - 创建直接收款 [可选]
5. `STRIPE_CAPTURE_CHARGE` - 捕获已授权的收款 [可选]

**关键参数**：
- `amount`：以最小货币单位计的金额（如 USD 以分为单位）
- `currency`：三位 ISO 货币代码（如 'usd'）
- `customer`：客户 ID
- `payment_method`：支付方式 ID
- `description`：收款描述

**注意事项**：
- 金额以最小货币单位表示（USD 下 100 = $1.00）
- 货币代码必须小写（如 'usd' 而非 'USD'）
- 推荐使用支付意向而非直接收款

### 3. 管理订阅

**适用场景**：创建、列出、更新或取消订阅

**工具调用顺序**：
1. `STRIPE_LIST_SUBSCRIPTIONS` - 列出订阅 [可选]
2. `STRIPE_POST_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS` - 创建订阅 [可选]
3. `STRIPE_RETRIEVE_SUBSCRIPTION` - 获取订阅详情 [可选]
4. `STRIPE_UPDATE_SUBSCRIPTION` - 修改订阅 [可选]

**关键参数**：
- `customer`：客户 ID
- `items`：价格项数组（含 price_id 和 quantity）
- `subscription`：用于检索/更新的订阅 ID（如 'sub_xxx'）

**注意事项**：
- 订阅需要有效客户且已绑定支付方式
- 订阅项使用价格 ID（非产品 ID）
- 取消可立即生效或在当前周期结束时生效

### 4. 管理发票

**适用场景**：创建、列出或搜索发票

**工具调用顺序**：
1. `STRIPE_LIST_INVOICES` - 列出发票 [可选]
2. `STRIPE_SEARCH_INVOICES` - 搜索发票 [可选]
3. `STRIPE_CREATE_INVOICE` - 创建发票 [可选]

**关键参数**：
- `customer`：发票对应的客户 ID
- `collection_method`：'charge_automatically' 或 'send_invoice'
- `days_until_due`：发票到期天数

**注意事项**：
- 发票默认自动定稿；使用 `auto_advance: false` 创建草稿发票

### 5. 管理产品与价格

**适用场景**：列出或搜索产品及其定价

**工具调用顺序**：
1. `STRIPE_LIST_PRODUCTS` - 列出产品 [可选]
2. `STRIPE_SEARCH_PRODUCTS` - 搜索产品 [可选]
3. `STRIPE_LIST_PRICES` - 列出价格 [可选]
4. `STRIPE_GET_PRICES_SEARCH` - 搜索价格 [可选]

**关键参数**：
- `active`：按启用/停用状态筛选
- `query`：搜索端点的查询关键词

**注意事项**：
- 产品和价格是独立对象；一个产品可对应多个价格
- 价格 ID（如 'price_xxx'）用于订阅和结账

### 6. 处理退款

**适用场景**：对收款发起退款

**工具调用顺序**：
1. `STRIPE_LIST_REFUNDS` - 列出退款 [可选]
2. `STRIPE_POST_CHARGES_CHARGE_REFUNDS` - 创建退款 [可选]
3. `STRIPE_CREATE_REFUND` - 通过支付意向创建退款 [可选]

**关键参数**：
- `charge`：退款对应的收款 ID
- `amount`：部分退款金额（省略则全额退款）
- `reason`：退款原因（'duplicate'、'fraudulent'、'requested_by_customer'）

**注意事项**：
- 退款可能需要 5-10 个工作日才会出现在客户账单上
- 金额以最小货币单位表示

## 常见模式

### 金额格式

Stripe 使用最小货币单位：
- USD：$10.50 = 1050 分
- EUR：10.50 = 1050 分
- JPY：1000 = 1000（无小数）

### 分页

- 使用 `limit` 参数（最大 100）
- 检查响应中的 `has_more` 字段
- 传入 `starting_after` 并设为最后一个对象 ID 以获取下一页
- 持续翻页直到 `has_more` 为 false

## 已知陷阱

**金额单位**：
- 始终使用最小货币单位（USD/EUR 以分为单位）
- 零小数货币（JPY、KRW）直接使用金额数值

**ID 前缀**：
- 客户：`cus_`，收款：`ch_`，订阅：`sub_`
- 发票：`in_`，产品：`prod_`，价格：`price_`
- 支付意向：`pi_`，退款：`re_`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 创建客户 | STRIPE_CREATE_CUSTOMER | email, name |
| 搜索客户 | STRIPE_SEARCH_CUSTOMERS | query |
| 更新客户 | STRIPE_POST_CUSTOMERS_CUSTOMER | customer, fields |
| 列出收款 | STRIPE_LIST_CHARGES | customer, limit |
| 创建支付意向 | STRIPE_CREATE_PAYMENT_INTENT | amount, currency |
| 确认支付 | STRIPE_CONFIRM_PAYMENT_INTENT | payment_intent |
| 列出订阅 | STRIPE_LIST_SUBSCRIPTIONS | customer |
| 创建订阅 | STRIPE_POST_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS | customer, items |
| 更新订阅 | STRIPE_UPDATE_SUBSCRIPTION | subscription, fields |
| 列出发票 | STRIPE_LIST_INVOICES | customer |
| 创建发票 | STRIPE_CREATE_INVOICE | customer |
| 搜索发票 | STRIPE_SEARCH_INVOICES | query |
| 列出产品 | STRIPE_LIST_PRODUCTS | active |
| 搜索产品 | STRIPE_SEARCH_PRODUCTS | query |
| 列出价格 | STRIPE_LIST_PRICES | product |
| 搜索价格 | STRIPE_GET_PRICES_SEARCH | query |
| 列出退款 | STRIPE_LIST_REFUNDS | charge |
| 创建退款 | STRIPE_CREATE_REFUND | charge, amount |
| 支付方式 | STRIPE_LIST_CUSTOMER_PAYMENT_METHODS | customer |
| 结账会话 | STRIPE_CREATE_CHECKOUT_SESSION | line_items |
| 列出支付意向 | STRIPE_LIST_PAYMENT_INTENTS | customer |

## 适用场景
本技能适用于执行概览中描述的工作流或操作。

## 使用限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出结果不能替代针对特定环境的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
