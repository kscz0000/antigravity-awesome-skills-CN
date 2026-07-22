# 应用开发参考

使用 OAuth、GraphQL/REST API、webhook 和计费构建 Shopify 应用的指南。

## OAuth 认证

### OAuth 2.0 流程

**1. 重定向到授权 URL：**

```
https://{shop}.myshopify.com/admin/oauth/authorize?
  client_id={api_key}&
  scope={scopes}&
  redirect_uri={redirect_uri}&
  state={nonce}
```

**2. 处理回调：**

```javascript
app.get("/auth/callback", async (req, res) => {
  const { code, shop, state } = req.query;

  // 验证 state 以防止 CSRF
  if (state !== storedState) {
    return res.status(403).send("Invalid state");
  }

  // 用授权码换取访问令牌
  const accessToken = await exchangeCodeForToken(shop, code);

  // 安全存储令牌
  await storeAccessToken(shop, accessToken);

  res.redirect(`https://${shop}/admin/apps/${appHandle}`);
});
```

**3. 用授权码换取令牌：**

```javascript
async function exchangeCodeForToken(shop, code) {
  const response = await fetch(`https://${shop}/admin/oauth/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_id: process.env.SHOPIFY_API_KEY,
      client_secret: process.env.SHOPIFY_API_SECRET,
      code,
    }),
  });

  const { access_token } = await response.json();
  return access_token;
}
```

### 访问权限范围

**常用权限范围：**

- `read_products`, `write_products` - 产品目录
- `read_orders`, `write_orders` - 订单管理
- `read_customers`, `write_customers` - 客户数据
- `read_inventory`, `write_inventory` - 库存水平
- `read_fulfillments`, `write_fulfillments` - 订单履约
- `read_shipping`, `write_shipping` - 运费
- `read_analytics` - 商店分析
- `read_checkouts`, `write_checkouts` - 结账数据

完整列表：https://shopify.dev/api/usage/access-scopes

### 会话令牌（嵌入式应用）

适用于使用 App Bridge 的嵌入式应用：

```javascript
import { getSessionToken } from '@shopify/app-bridge/utilities';

async function authenticatedFetch(url, options = {}) {
  const app = createApp({ ... });
  const token = await getSessionToken(app);

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });
}
```

## GraphQL Admin API

### 发起请求

```javascript
async function graphqlRequest(shop, accessToken, query, variables = {}) {
  const response = await fetch(
    `https://${shop}/admin/api/2026-01/graphql.json`,
    {
      method: "POST",
      headers: {
        "X-Shopify-Access-Token": accessToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, variables }),
    },
  );

  const data = await response.json();

  if (data.errors) {
    throw new Error(`GraphQL errors: ${JSON.stringify(data.errors)}`);
  }

  return data.data;
}
```

### 产品操作

**创建产品：**

```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

变量：

```json
{
  "input": {
    "title": "New Product",
    "productType": "Apparel",
    "vendor": "Brand",
    "status": "ACTIVE",
    "variants": [
      { "price": "29.99", "sku": "SKU-001", "inventoryQuantity": 100 }
    ]
  }
}
```

**更新产品：**

```graphql
mutation UpdateProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

**查询产品：**

```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        status
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### 订单操作

**查询订单：**

```graphql
query GetOrders($first: Int!) {
  orders(first: $first) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          email
          firstName
          lastName
        }
      }
    }
  }
}
```

**履约订单：**

```graphql
mutation FulfillOrder($fulfillment: FulfillmentInput!) {
  fulfillmentCreate(fulfillment: $fulfillment) {
    fulfillment {
      id
      status
      trackingInfo {
        number
        url
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

## Webhook

### 配置

在 `shopify.app.toml` 中：

```toml
[webhooks]
api_version = "2025-01"

[[webhooks.subscriptions]]
topics = ["orders/create"]
uri = "/webhooks/orders/create"

[[webhooks.subscriptions]]
topics = ["products/update"]
uri = "/webhooks/products/update"

[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks/app/uninstalled"

# GDPR 强制 webhook
[webhooks.privacy_compliance]
customer_data_request_url = "/webhooks/gdpr/data-request"
customer_deletion_url = "/webhooks/gdpr/customer-deletion"
shop_deletion_url = "/webhooks/gdpr/shop-deletion"
```

### Webhook 处理器

```javascript
import crypto from "crypto";

function verifyWebhook(req) {
  const hmac = req.headers["x-shopify-hmac-sha256"];
  const body = req.rawBody; // 原始请求体缓冲区

  const hash = crypto
    .createHmac("sha256", process.env.SHOPIFY_API_SECRET)
    .update(body, "utf8")
    .digest("base64");

  return hmac === hash;
}

app.post("/webhooks/orders/create", async (req, res) => {
  if (!verifyWebhook(req)) {
    return res.status(401).send("Unauthorized");
  }

  const order = req.body;
  console.log("New order:", order.id, order.name);

  // 处理订单...

  res.status(200).send("OK");
});
```

### 常用 Webhook 主题

**订单：**

- `orders/create`, `orders/updated`, `orders/delete`
- `orders/paid`, `orders/cancelled`, `orders/fulfilled`

**产品：**

- `products/create`, `products/update`, `products/delete`

**客户：**

- `customers/create`, `customers/update`, `customers/delete`

**库存：**

- `inventory_levels/update`

**应用：**

- `app/uninstalled`（清理时必需）

## 计费集成

### 应用收费

**一次性收费：**

```graphql
mutation CreateCharge($input: AppPurchaseOneTimeInput!) {
  appPurchaseOneTimeCreate(input: $input) {
    appPurchaseOneTime {
      id
      name
      price {
        amount
      }
      status
      confirmationUrl
    }
    userErrors {
      field
      message
    }
  }
}
```

变量：

```json
{
  "input": {
    "name": "Premium Feature",
    "price": { "amount": 49.99, "currencyCode": "USD" },
    "returnUrl": "https://your-app.com/billing/callback"
  }
}
```

**周期性收费（订阅）：**

```graphql
mutation CreateSubscription(
  $name: String!
  $returnUrl: URL!
  $lineItems: [AppSubscriptionLineItemInput!]!
  $trialDays: Int
) {
  appSubscriptionCreate(
    name: $name
    returnUrl: $returnUrl
    lineItems: $lineItems
    trialDays: $trialDays
  ) {
    appSubscription {
      id
      name
      status
    }
    confirmationUrl
    userErrors {
      field
      message
    }
  }
}
```

变量：

```json
{
  "name": "Monthly Subscription",
  "returnUrl": "https://your-app.com/billing/callback",
  "trialDays": 7,
  "lineItems": [
    {
      "plan": {
        "appRecurringPricingDetails": {
          "price": { "amount": 29.99, "currencyCode": "USD" },
          "interval": "EVERY_30_DAYS"
        }
      }
    }
  ]
}
```

**按用量计费：**

```graphql
mutation CreateUsageCharge(
  $subscriptionLineItemId: ID!
  $price: MoneyInput!
  $description: String!
) {
  appUsageRecordCreate(
    subscriptionLineItemId: $subscriptionLineItemId
    price: $price
    description: $description
  ) {
    appUsageRecord {
      id
      price {
        amount
        currencyCode
      }
      description
    }
    userErrors {
      field
      message
    }
  }
}
```

变量：

```json
{
  "subscriptionLineItemId": "gid://shopify/AppSubscriptionLineItem/123",
  "price": { "amount": "5.00", "currencyCode": "USD" },
  "description": "100 API calls used"
}
```

## Metafields

### 创建/更新 Metafields

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

变量：

```json
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123",
      "namespace": "custom",
      "key": "instructions",
      "value": "Handle with care",
      "type": "single_line_text_field"
    }
  ]
}
```

**Metafield 类型：**

- `single_line_text_field`, `multi_line_text_field`
- `number_integer`, `number_decimal`
- `date`, `date_time`
- `url`, `json`
- `file_reference`, `product_reference`

## 速率限制

### GraphQL 基于成本的限制

**限制值：**

- 可用点数：2000
- 恢复速率：100 点/秒
- 最大查询成本：2000

**检查成本：**

```javascript
const response = await graphqlRequest(shop, token, query);
const cost = response.extensions?.cost;

console.log(
  `Cost: ${cost.actualQueryCost}/${cost.throttleStatus.maximumAvailable}`,
);
```

**处理限流：**

```javascript
async function graphqlWithRetry(shop, token, query, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await graphqlRequest(shop, token, query);
    } catch (error) {
      if (error.message.includes("Throttled") && i < retries - 1) {
        await sleep(Math.pow(2, i) * 1000); // 指数退避
        continue;
      }
      throw error;
    }
  }
}
```

## 最佳实践

**安全：**

- 将凭证存储在环境变量中
- 验证 webhook HMAC 签名
- 验证 OAuth state 参数
- 所有端点使用 HTTPS
- 在你的端点实现速率限制

**性能：**

- 安全缓存访问令牌
- 大数据集使用批量操作
- 查询实现分页
- 监控 GraphQL 查询成本

**可靠性：**

- 重试实现指数退避
- 处理 webhook 投递失败
- 记录错误用于调试
- 监控应用健康指标

**合规：**

- 实现 GDPR webhook（强制）
- 处理客户数据删除请求
- 提供数据导出功能
- 遵循数据保留策略
