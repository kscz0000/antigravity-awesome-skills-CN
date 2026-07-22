---
name: shopify-apps
description: "Shopify 应用开发的专家模式，涵盖 Remix/React Router 应用、App Bridge 嵌入式应用、Webhook 处理、GraphQL Admin API、Polaris 组件、计费和应用扩展。触发词：Shopify应用、Shopify开发、App Bridge、Polaris、Shopify Webhook、GraphQL Admin API、Shopify计费、应用扩展"
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Shopify 应用

Shopify 应用开发的专家模式，涵盖 Remix/React Router 应用、App Bridge 嵌入式应用、Webhook 处理、GraphQL Admin API、Polaris 组件、计费和应用扩展。

## 模式

### React Router 应用设置

基于 React Router 的现代 Shopify 应用模板

**适用场景**：创建新的 Shopify 应用

### 模板

# 使用 CLI 创建新的 Shopify 应用
npm init @shopify/app@latest my-shopify-app

# 项目结构
# my-shopify-app/
# ├── app/
# │   ├── routes/
# │   │   ├── app._index.tsx        # 应用主页
# │   │   ├── app.tsx               # 带 Provider 的应用布局
# │   │   ├── auth.$.tsx            # 认证回调
# │   │   └── webhooks.tsx          # Webhook 处理器
# │   ├── shopify.server.ts         # 服务器配置
# │   └── root.tsx                  # 根布局
# ├── extensions/                   # 应用扩展
# ├── shopify.app.toml              # 应用配置
# └── package.json

// shopify.app.toml
name = "my-shopify-app"
client_id = "your-client-id"
application_url = "https://your-app.example.com"

[access_scopes]
scopes = "read_products,write_products,read_orders"

[webhooks]
api_version = "2024-10"

[webhooks.subscriptions]
topics = ["orders/create", "products/update"]
uri = "/webhooks"

[auth]
redirect_urls = ["https://your-app.example.com/auth/callback"]

// app/shopify.server.ts
import "@shopify/shopify-app-remix/adapters/node";
import {
  LATEST_API_VERSION,
  shopifyApp,
  DeliveryMethod,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY!,
  apiSecretKey: process.env.SHOPIFY_API_SECRET!,
  scopes: process.env.SCOPES?.split(","),
  appUrl: process.env.SHOPIFY_APP_URL!,
  authPathPrefix: "/auth",
  sessionStorage: new PrismaSessionStorage(prisma),
  distribution: AppDistribution.AppStore,
  future: {
    unstable_newEmbeddedAuthStrategy: true,
  },
  ...(process.env.SHOP_CUSTOM_DOMAIN
    ? { customShopDomains: [process.env.SHOP_CUSTOM_DOMAIN] }
    : {}),
});

export default shopify;
export const apiVersion = LATEST_API_VERSION;
export const authenticate = shopify.authenticate;
export const sessionStorage = shopify.sessionStorage;

### 说明

- React Router 在 2024 年底取代 Remix 成为推荐模板
- 新应用默认启用 unstable_newEmbeddedAuthStrategy
- Webhook 在 shopify.app.toml 中配置，而非代码
- 运行 'shopify app deploy' 应用配置更改

### 使用 App Bridge 的嵌入式应用

在 Shopify Admin 中渲染嵌入式应用

**适用场景**：构建嵌入式管理应用

### 模板

// app/routes/app.tsx - 带 Provider 的应用布局
import { Link, Outlet, useLoaderData, useRouteError } from "@remix-run/react";
import { AppProvider } from "@shopify/shopify-app-remix/react";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";

export const links = () => [{ rel: "stylesheet", href: polarisStyles }];

export async function loader({ request }: LoaderFunctionArgs) {
  await authenticate.admin(request);
  return json({ apiKey: process.env.SHOPIFY_API_KEY! });
}

export default function App() {
  const { apiKey } = useLoaderData<typeof loader>();

  return (
    <AppProvider isEmbeddedApp apiKey={apiKey}>
      <ui-nav-menu>
        <Link to="/app" rel="home">Home</Link>
        <Link to="/app/products">Products</Link>
        <Link to="/app/settings">Settings</Link>
      </ui-nav-menu>
      <Outlet />
    </AppProvider>
  );
}

export function ErrorBoundary() {
  const error = useRouteError();
  return (
    <AppProvider isEmbeddedApp>
      <Page>
        <Card>
          <Text as="p" variant="bodyMd">
            Something went wrong. Please try again.
          </Text>
        </Card>
      </Page>
    </AppProvider>
  );
}

// app/routes/app._index.tsx - 应用主页
import {
  Page,
  Layout,
  Card,
  Text,
  BlockStack,
  Button,
} from "@shopify/polaris";
import { TitleBar } from "@shopify/app-bridge-react";

export async function loader({ request }: LoaderFunctionArgs) {
  const { admin } = await authenticate.admin(request);

  // GraphQL 查询
  const response = await admin.graphql(`
    query {
      shop {
        name
        email
      }
    }
  `);

  const { data } = await response.json();
  return json({ shop: data.shop });
}

export default function Index() {
  const { shop } = useLoaderData<typeof loader>();

  return (
    <Page>
      <TitleBar title="My Shopify App" />
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="200">
              <Text as="h2" variant="headingMd">
                Welcome to {shop.name}!
              </Text>
              <Text as="p" variant="bodyMd">
                Your app is now connected to this store.
              </Text>
              <Button variant="primary">
                Get Started
              </Button>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

### 说明

- 2025 年 7 月起，Built for Shopify 认证要求使用 App Bridge
- Polaris 组件与 Shopify Admin 设计一致
- TitleBar 和导航来自 App Bridge
- 始终使用 authenticate.admin() 验证请求

### Webhook 处理

使用 HMAC 验证的安全 Webhook 处理

**适用场景**：接收 Shopify Webhook

### 模板

// app/routes/webhooks.tsx
import type { ActionFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";
import db from "../db.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  // 验证 Webhook（校验 HMAC 签名）
  const { topic, shop, payload, admin } = await authenticate.webhook(request);

  console.log(`Received ${topic} webhook for ${shop}`);

  // 根据主题处理
  switch (topic) {
    case "ORDERS_CREATE":
      // 排队异步处理
      await queueOrderProcessing(payload);
      break;

    case "PRODUCTS_UPDATE":
      await handleProductUpdate(shop, payload);
      break;

    case "APP_UNINSTALLED":
      // 清理店铺数据
      await db.session.deleteMany({ where: { shop } });
      await db.shopData.delete({ where: { shop } });
      break;

    case "CUSTOMERS_DATA_REQUEST":
    case "CUSTOMERS_REDACT":
    case "SHOP_REDACT":
      // GDPR Webhook - 必须处理
      await handleGDPRWebhook(topic, payload);
      break;

    default:
      console.log(`Unhandled webhook topic: ${topic}`);
  }

  // 关键：立即返回 200
  // Shopify 要求 5 秒内响应
  return new Response(null, { status: 200 });
};

// 响应后异步处理
async function queueOrderProcessing(payload: any) {
  // 使用任务队列（BullMQ 等）
  await jobQueue.add("process-order", {
    orderId: payload.id,
    orderData: payload,
  });
}

async function handleProductUpdate(shop: string, payload: any) {
  // 仅执行快速同步操作
  await db.product.upsert({
    where: { shopifyId: payload.id },
    update: {
      title: payload.title,
      updatedAt: new Date(),
    },
    create: {
      shopifyId: payload.id,
      shop,
      title: payload.title,
    },
  });
}

async function handleGDPRWebhook(topic: string, payload: any) {
  // GDPR 合规 - 所有应用必须处理
  switch (topic) {
    case "CUSTOMERS_DATA_REQUEST":
      // 30 天内返回客户数据
      break;
    case "CUSTOMERS_REDACT":
      // 删除客户数据
      break;
    case "SHOP_REDACT":
      // 删除所有店铺数据（卸载后 48 小时）
      break;
  }
}

### 说明

- 必须在 5 秒内响应，否则 Webhook 失败
- 重型处理使用任务队列
- GDPR Webhook 对 App Store 应用是必须的
- HMAC 验证由 authenticate.webhook() 处理

### GraphQL Admin API

使用 GraphQL 查询和变更店铺数据

**适用场景**：与 Shopify Admin API 交互

### 模板

// 使用认证 admin 客户端的 GraphQL 查询
export async function loader({ request }: LoaderFunctionArgs) {
  const { admin } = await authenticate.admin(request);

  // 分页查询产品
  const response = await admin.graphql(`
    query GetProducts($first: Int!, $after: String) {
      products(first: $first, after: $after) {
        edges {
          node {
            id
            title
            status
            totalInventory
            priceRangeV2 {
              minVariantPrice {
                amount
                currencyCode
              }
            }
            images(first: 1) {
              edges {
                node {
                  url
                  altText
                }
              }
            }
          }
          cursor
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `, {
    variables: {
      first: 10,
      after: null,
    },
  });

  const { data } = await response.json();
  return json({ products: data.products });
}

// 变更操作
export async function action({ request }: ActionFunctionArgs) {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();
  const productId = formData.get("productId");
  const newTitle = formData.get("title");

  const response = await admin.graphql(`
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
  `, {
    variables: {
      input: {
        id: productId,
        title: newTitle,
      },
    },
  });

  const { data } = await response.json();

  if (data.productUpdate.userErrors.length > 0) {
    return json({
      errors: data.productUpdate.userErrors,
    }, { status: 400 });
  }

  return json({ product: data.productUpdate.product });
}

// 大数据集的批量操作
async function bulkUpdateProducts(admin: AdminApiContext) {
  // 创建批量操作
  const response = await admin.graphql(`
    mutation {
      bulkOperationRunMutation(
        mutation: "mutation call($input: ProductInput!) {
          productUpdate(input: $input) { product { id } }
        }",
        stagedUploadPath: "path-to-staged-upload"
      ) {
        bulkOperation {
          id
          status
        }
        userErrors {
          message
        }
      }
    }
  `);

  // 轮询等待完成或使用 Webhook
  // BULK_OPERATIONS_FINISH Webhook
}

### 说明

- 2025 年 4 月起，新公开应用必须使用 GraphQL
- 速率限制：每 60 秒 1000 点
- 超过 250 个项目使用批量操作
- App Bridge 可直接访问 API

### 计费 API 集成

为应用实现订阅计费

**适用场景**：Shopify 应用变现

### 模板

// app/routes/app.billing.tsx
import { json, redirect } from "@remix-run/node";
import { Page, Card, Button, BlockStack, Text } from "@shopify/polaris";
import { authenticate } from "../shopify.server";

const PLANS = {
  basic: {
    name: "Basic",
    amount: 9.99,
    currencyCode: "USD",
    interval: "EVERY_30_DAYS",
  },
  pro: {
    name: "Pro",
    amount: 29.99,
    currencyCode: "USD",
    interval: "EVERY_30_DAYS",
  },
};

export async function loader({ request }: LoaderFunctionArgs) {
  const { admin, billing } = await authenticate.admin(request);

  // 检查当前订阅
  const response = await admin.graphql(`
    query {
      currentAppInstallation {
        activeSubscriptions {
          id
          name
          status
          lineItems {
            plan {
              pricingDetails {
                ... on AppRecurringPricing {
                  price {
                    amount
                    currencyCode
                  }
                  interval
                }
              }
            }
          }
        }
      }
    }
  `);

  const { data } = await response.json();
  return json({
    subscription: data.currentAppInstallation.activeSubscriptions[0],
  });
}

export async function action({ request }: ActionFunctionArgs) {
  const { admin, session } = await authenticate.admin(request);
  const formData = await request.formData();
  const planKey = formData.get("plan") as keyof typeof PLANS;
  const plan = PLANS[planKey];

  // 创建订阅收费
  const response = await admin.graphql(`
    mutation CreateSubscription($name: String!, $lineItems: [AppSubscriptionLineItemInput!]!, $returnUrl: URL!, $test: Boolean) {
      appSubscriptionCreate(
        name: $name
        lineItems: $lineItems
        returnUrl: $returnUrl
        test: $test
      ) {
        appSubscription {
          id
          status
        }
        confirmationUrl
        userErrors {
          field
          message
        }
      }
    }
  `, {
    variables: {
      name: plan.name,
      lineItems: [
        {
          plan: {
            appRecurringPricingDetails: {
              price: {
                amount: plan.amount,
                currencyCode: plan.currencyCode,
              },
              interval: plan.interval,
            },
          },
        },
      ],
      returnUrl: `https://${session.shop}/admin/apps/${process.env.SHOPIFY_API_KEY}`,
      test: process.env.NODE_ENV !== "production",
    },
  });

  const { data } = await response.json();

  if (data.appSubscriptionCreate.userErrors.length > 0) {
    return json({
      errors: data.appSubscriptionCreate.userErrors,
    }, { status: 400 });
  }

  // 重定向商家审批收费
  return redirect(data.appSubscriptionCreate.confirmationUrl);
}

export default function Billing() {
  const { subscription } = useLoaderData<typeof loader>();
  const submit = useSubmit();

  return (
    <Page title="Billing">
      <Card>
        {subscription ? (
          <BlockStack gap="200">
            <Text as="p" variant="bodyMd">
              Current plan: {subscription.name}
            </Text>
            <Text as="p" variant="bodyMd">
              Status: {subscription.status}
            </Text>
          </BlockStack>
        ) : (
          <BlockStack gap="400">
            <Text as="h2" variant="headingMd">
              Choose a Plan
            </Text>
            <Button onClick={() => submit({ plan: "basic" }, { method: "post" })}>
              Basic - $9.99/month
            </Button>
            <Button onClick={() => submit({ plan: "pro" }, { method: "post" })}>
              Pro - $29.99/month
            </Button>
          </BlockStack>
        )}
      </Card>
    </Page>
  );
}

### 说明

- 开发店铺使用 test: true
- 商家必须审批订阅
- 每个应用最多一个循环收费 + 一个使用量收费
- 循环收费为 30 天计费周期

### 应用扩展开发

扩展 Shopify 结账、管理后台或店铺前台

**适用场景**：构建应用扩展

### 模板

# shopify.extension.toml（在 extensions/my-extension/ 目录下）
api_version = "2024-10"

[[extensions]]
type = "ui_extension"
name = "Product Customizer"
handle = "product-customizer"

[[extensions.targeting]]
target = "admin.product-details.block.render"
module = "./src/AdminBlock.tsx"

[extensions.capabilities]
api_access = true

[extensions.settings]
[[extensions.settings.fields]]
key = "show_preview"
type = "boolean"
name = "Show Preview"

// extensions/my-extension/src/AdminBlock.tsx
import {
  reactExtension,
  useApi,
  useSettings,
  BlockStack,
  Text,
  Button,
  InlineStack,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension(
  "admin.product-details.block.render",
  () => <ProductCustomizer />
);

function ProductCustomizer() {
  const { data, extension } = useApi<"admin.product-details.block.render">();
  const settings = useSettings();

  const productId = data?.selected?.[0]?.id;

  const handleCustomize = async () => {
    // 从扩展发起 API 调用
    const result = await fetch("/api/customize", {
      method: "POST",
      body: JSON.stringify({ productId }),
    });
  };

  return (
    <BlockStack gap="base">
      <Text fontWeight="bold">Product Customizer</Text>
      <Text>
        Customize product: {productId}
      </Text>
      {settings.show_preview && (
        <Text size="small">Preview enabled</Text>
      )}
      <InlineStack gap="base">
        <Button onPress={handleCustomize}>
          Apply Customization
        </Button>
      </InlineStack>
    </BlockStack>
  );
}

// 结账 UI 扩展
// [[extensions.targeting]]
// target = "purchase.checkout.block.render"

// extensions/checkout-ext/src/Checkout.tsx
import {
  reactExtension,
  Banner,
  useCartLines,
  useTotalAmount,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension(
  "purchase.checkout.block.render",
  () => <CheckoutBanner />
);

function CheckoutBanner() {
  const cartLines = useCartLines();
  const total = useTotalAmount();

  if (total.amount > 100) {
    return (
      <Banner status="success">
        You qualify for free shipping!
      </Banner>
    );
  }

  return null;
}

### 说明

- 扩展运行在沙盒 iframe 中
- React 项目使用 @shopify/ui-extensions-react
- 相比完整应用，可用 API 有限
- 使用 'shopify app deploy' 部署

## 重要陷阱

### Webhook 必须在 5 秒内响应

严重程度：高

场景：接收 Shopify 的 Webhook

症状：
Webhook 递送标记为失败。
Shopify 日志中出现"你的应用未及时响应"。
订单/产品更新丢失。
Webhook 被反复重试后取消。

原因：
Shopify 要求在 5 秒内返回 2xx 响应。如果应用在响应前处理 Webhook 数据，将会超时。

Shopify 会在 48 小时内最多重试失败的 Webhook 19 次。
持续失败后，Webhook 可能被完全取消。

重型处理（API 调用、数据库操作）必须在响应发送后进行。

推荐修复：

## 立即响应，异步处理

```typescript
// app/routes/webhooks.tsx
export const action = async ({ request }: ActionFunctionArgs) => {
  const { topic, shop, payload } = await authenticate.webhook(request);

  // 排队异步处理
  await jobQueue.add("process-webhook", {
    topic,
    shop,
    payload,
  });

  // 关键：立即返回 200
  return new Response(null, { status: 200 });
};

// Worker 进程处理实际工作
// workers/webhook-processor.ts
import { Worker } from "bullmq";

const worker = new Worker("process-webhook", async (job) => {
  const { topic, shop, payload } = job.data;

  switch (topic) {
    case "ORDERS_CREATE":
      await processOrder(shop, payload);
      break;
    // ... 其他处理器
  }
});
```

## 简单操作快速处理即可

```typescript
// 简单的数据库更新如果够快也可以
export const action = async ({ request }: ActionFunctionArgs) => {
  const { topic, payload } = await authenticate.webhook(request);

  // 快速数据库更新（< 1 秒）
  await db.product.update({
    where: { shopifyId: payload.id },
    data: { title: payload.title },
  });

  return new Response(null, { status: 200 });
};
```

## 监控 Webhook 性能

```typescript
// 记录响应时间
const start = Date.now();

await handleWebhook(payload);

const duration = Date.now() - start;
console.log(`Webhook processed in ${duration}ms`);

// 接近超时时告警
if (duration > 3000) {
  console.warn("Webhook processing taking too long!");
}
```

### API 速率限制导致 429 错误

严重程度：高

场景：向 Shopify 发起 API 调用

症状：
HTTP 429 Too Many Requests 错误。
"Throttled" 响应。
应用变得无响应。
操作静默失败或部分失败。

原因：
Shopify 执行严格的速率限制：
- REST：每个店铺每秒 2 个请求
- GraphQL：每 60 秒 1000 点

超出限制会立即产生 429 错误。
持续违规可能导致临时封禁。

批量操作计入限制。

推荐修复：

## 检查速率限制头

```typescript
// REST API
// X-Shopify-Shop-Api-Call-Limit: 39/40

// GraphQL - 检查响应扩展
const response = await admin.graphql(`...`);
const { data, extensions } = await response.json();

const cost = extensions?.cost;
// {
//   "requestedQueryCost": 42,
//   "actualQueryCost": 42,
//   "throttleStatus": {
//     "maximumAvailable": 1000,
//     "currentlyAvailable": 958,
//     "restoreRate": 50
//   }
// }
```

## 实现指数退避重试

```typescript
async function shopifyRequest(
  fn: () => Promise<Response>,
  maxRetries = 3
): Promise<Response> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fn();

      if (response.status === 429) {
        // 获取 retry-after 头或使用默认值
        const retryAfter = parseInt(
          response.headers.get("Retry-After") || "2"
        );
        await sleep(retryAfter * 1000 * Math.pow(2, attempt));
        continue;
      }

      return response;
    } catch (error) {
      lastError = error as Error;
    }
  }

  throw lastError!;
}
```

## 大数据集使用批量操作

```typescript
// 不要发起 1000 次单独调用，使用批量变更
const response = await admin.graphql(`
  mutation {
    bulkOperationRunMutation(
      mutation: "mutation($input: ProductInput!) {
        productUpdate(input: $input) { product { id } }
      }",
      stagedUploadPath: "..."
    ) {
      bulkOperation { id status }
      userErrors { message }
    }
  }
`);
```

## 请求排队

```typescript
import { RateLimiter } from "limiter";

// REST 每秒 2 个请求
const limiter = new RateLimiter({
  tokensPerInterval: 2,
  interval: "second",
});

async function rateLimitedRequest(fn: () => Promise<any>) {
  await limiter.removeTokens(1);
  return fn();
}
```

### 受保护客户数据需要特殊权限

严重程度：高

场景：在 Webhook 或 API 中访问客户 PII

症状：
订单/客户的 Webhook 递送失败。
客户数据字段为空或 null。
应用在开发环境正常但生产环境失败。
"Protected customer data access" 错误。

原因：
自 2024 年 4 月起，访问受保护的客户数据（PII）需要 Shopify 的明确审批。这与 OAuth 权限分开。

受保护数据包括：
- 客户姓名、邮箱、地址
- 订单客户信息
- 订阅客户详情

即使有 read_orders 权限，没有受保护数据访问权限也无法在 Webhook 中接收客户数据。

推荐修复：

## 申请受保护客户数据访问权限

1. 前往 Partner Dashboard > App > API access
2. 在"Protected customer data access"下
3. 申请所需数据类型的访问权限
4. 说明使用场景
5. 等待 Shopify 审批（可能需要数天）

## 检查数据访问级别

```typescript
// 查询应用的数据访问权限
const response = await admin.graphql(`
  query {
    currentAppInstallation {
      accessScopes {
        handle
      }
    }
  }
`);
```

## 优雅处理缺失数据

```typescript
// Webhook 载荷可能包含脱敏字段
async function processOrder(payload: any) {
  const customerEmail = payload.customer?.email;

  if (!customerEmail) {
    // 客户数据不可用
    // 可能没有受保护访问权限或数据已脱敏
    console.log("Customer data not available");
    return;
  }

  await sendOrderConfirmation(customerEmail);
}
```

## 使用 Customer Account API 直接访问

```typescript
// 如果客户已登录，可以通过
// Customer Account API 访问其数据
// （与 Admin API 不同）
```

### 重复 Webhook 定义导致冲突

严重程度：中

场景：同时在 TOML 和代码中配置 Webhook

症状：
Webhook 递送重复。
某些 Webhook 触发两次。
Webhook 订阅注册失败。
Webhook 行为不可预测。

原因：
Shopify 应用可以在两个地方定义 Webhook：
1. shopify.app.toml（声明式，推荐）
2. 代码中的 afterAuth hook（命令式，旧版）

如果在两处定义相同的 Webhook，会导致：
- 重复订阅
- 注册时的竞争条件
- 应用更新时的冲突

推荐修复：

## 仅使用 TOML（推荐）

```toml
# shopify.app.toml
[webhooks]
api_version = "2024-10"

[webhooks.subscriptions]
topics = [
  "orders/create",
  "orders/updated",
  "products/create",
  "products/update",
  "app/uninstalled"
]
uri = "/webhooks"
```

## 移除基于代码的注册

```typescript
// 使用 TOML 时不要这样做
const shopify = shopifyApp({
  // ...
  hooks: {
    afterAuth: async ({ session }) => {
      // 从此处移除 Webhook 注册
      // 让 TOML 处理
    },
  },
});
```

## 部署以应用 TOML 更改

```bash
# Webhook 在部署时注册
shopify app deploy
```

## 检查当前订阅

```typescript
const response = await admin.graphql(`
  query {
    webhookSubscriptions(first: 50) {
      edges {
        node {
          id
          topic
          endpoint {
            ... on WebhookHttpEndpoint {
              callbackUrl
            }
          }
        }
      }
    }
  }
`);
```

### Webhook URL 末尾斜杠导致 404

严重程度：中

场景：设置 Webhook 端点

症状：
Webhook 返回 404 Not Found。
Webhook 递送立即失败。
本地开发正常但生产环境失败。
日志显示请求发往 /webhooks/ 而非 /webhooks。

原因：
Shopify 会自动在 Webhook URL 末尾添加斜杠。
如果服务器不同时处理 /webhooks 和 /webhooks/，Webhook 将返回 404。

常见于对末尾斜杠严格的框架。

推荐修复：

## 同时处理两种 URL 格式

```typescript
// Remix/React Router - 默认同时支持两种
// app/routes/webhooks.tsx 处理 /webhooks

// Express - 添加中间件
app.use((req, res, next) => {
  if (req.path.endsWith('/') && req.path.length > 1) {
    const query = req.url.slice(req.path.length);
    const safePath = req.path.slice(0, -1);
    res.redirect(301, safePath + query);
  }
  next();
});
```

## 配置 Web 服务器

```nginx
# Nginx - 去除末尾斜杠
location ~ ^(.+)/$ {
  return 301 $1;
}

# 或重写到处理器
location /webhooks {
  try_files $uri $uri/ @webhooks;
}
location @webhooks {
  proxy_pass http://app:3000/webhooks;
}
```

## 测试两种格式

```bash
# 测试无斜杠
curl -X POST https://your-app.com/webhooks

# 测试有斜杠
curl -X POST https://your-app.com/webhooks/
```

### REST API 必须迁移到 GraphQL（2025 年 4 月）

严重程度：高

场景：构建新公开应用或维护现有应用

症状：
应用商店提交因使用 REST API 被拒绝。
控制台出现弃用警告。
部分 REST 端点停止工作。
某些功能仅 GraphQL 可用。

原因：
自 2024 年 10 月起，REST Admin API 已是旧版。
2025 年 4 月起，新公开应用必须使用 GraphQL。

现有应用的 REST 端点将继续工作，但新功能仅限 GraphQL。

Metafields、批量操作和许多新功能需要 GraphQL。

推荐修复：

## 所有新代码使用 GraphQL

```typescript
// REST（旧版）
const response = await fetch(
  `https://${shop}/admin/api/2024-10/products.json`,
  {
    headers: { "X-Shopify-Access-Token": token },
  }
);

// GraphQL（推荐）
const response = await admin.graphql(`
  query {
    products(first: 10) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
`);
```

## 迁移现有 REST 调用

```typescript
// REST: GET /products/{id}.json
// GraphQL 等效：
const response = await admin.graphql(`
  query GetProduct($id: ID!) {
    product(id: $id) {
      id
      title
      status
      variants(first: 10) {
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
`, {
  variables: { id: `gid://shopify/Product/${productId}` },
});
```

## Webhook 也使用 GraphQL

```toml
# shopify.app.toml
[webhooks]
api_version = "2024-10"  # 使用最新 GraphQL 版本
```

### App Bridge 是 Built for Shopify 认证的必要条件（2025 年 7 月）

严重程度：高

场景：构建嵌入式 Shopify 应用

症状：
应用在"Built for Shopify"计划中被拒绝。
应用在管理后台显示不正常。
导航和界面问题。
App Bridge 版本警告。

原因：
2025 年 7 月起，所有寻求"Built for Shopify"状态的应用必须使用最新版本的 App Bridge 且为嵌入式应用。

使用旧版 App Bridge 或非嵌入式的应用将失去 Built for Shopify 权益（更好的展示位置、徽章）。

Shopify 现在通过无版本号的 script 标签提供 App Bridge 和 Polaris，可自动更新。

推荐修复：

## 通过 script 标签使用最新 App Bridge

```html
<!-- 自动保持最新 -->
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
```

## 在 React 中使用 AppProvider

```typescript
// app/routes/app.tsx
import { AppProvider } from "@shopify/shopify-app-remix/react";

export default function App() {
  return (
    <AppProvider isEmbeddedApp apiKey={apiKey}>
      <Outlet />
    </AppProvider>
  );
}
```

## 启用嵌入式认证策略

```typescript
// shopify.server.ts
const shopify = shopifyApp({
  // ...
  future: {
    unstable_newEmbeddedAuthStrategy: true,
  },
});
```

## 检查嵌入状态

```typescript
import { useAppBridge } from "@shopify/app-bridge-react";

function MyComponent() {
  const app = useAppBridge();
  const isEmbedded = app.hostOrigin !== window.location.origin;
}
```

### 缺少 GDPR Webhook 会阻止 App Store 审批

严重程度：高

场景：向 Shopify App Store 提交应用

症状：
应用提交被拒绝。
"GDPR webhooks not implemented" 错误。
人工审核合规性不通过。
数据请求 Webhook 未处理。

原因：
Shopify 要求所有应用处理三个 GDPR Webhook：
1. customers/data_request - 提供客户数据
2. customers/redact - 删除客户数据
3. shop/redact - 删除所有店铺数据

创建应用时会自动订阅这些 Webhook。
即使不存储数据，也必须实现处理器。

推荐修复：

## 实现所有 GDPR 处理器

```typescript
// app/routes/webhooks.tsx
export const action = async ({ request }: ActionFunctionArgs) => {
  const { topic, payload, shop } = await authenticate.webhook(request);

  switch (topic) {
    case "CUSTOMERS_DATA_REQUEST":
      await handleDataRequest(shop, payload);
      break;

    case "CUSTOMERS_REDACT":
      await handleCustomerRedact(shop, payload);
      break;

    case "SHOP_REDACT":
      await handleShopRedact(shop, payload);
      break;
  }

  return new Response(null, { status: 200 });
};

async function handleDataRequest(shop: string, payload: any) {
  const customerId = payload.customer.id;

  // 30 天内返回客户数据
  // 通常发送到 data_request.destination_url
  const customerData = await db.customer.findUnique({
    where: { shopifyId: customerId, shop },
  });

  if (customerData) {
    // 发送到提供的 URL 或邮箱
    await sendDataToMerchant(payload.data_request, customerData);
  }
}

async function handleCustomerRedact(shop: string, payload: any) {
  const customerId = payload.customer.id;

  // 删除客户的个人数据
  await db.customer.deleteMany({
    where: { shopifyId: customerId, shop },
  });

  await db.order.updateMany({
    where: { customerId, shop },
    data: { customerEmail: null, customerName: null },
  });
}

async function handleShopRedact(shop: string, payload: any) {
  // 店铺已卸载 48 小时以上
  // 删除该店铺的所有数据
  await db.session.deleteMany({ where: { shop } });
  await db.customer.deleteMany({ where: { shop } });
  await db.order.deleteMany({ where: { shop } });
  await db.settings.deleteMany({ where: { shop } });
}
```

## 即使不存储任何数据

```typescript
// 仍然必须返回 200
case "CUSTOMERS_DATA_REQUEST":
case "CUSTOMERS_REDACT":
case "SHOP_REDACT":
  // 未存储数据，但必须确认
  console.log(`GDPR ${topic} for ${shop} - no data stored`);
  break;
```

## 验证检查

### 硬编码 Shopify API Secret

严重程度：错误

API Secret 绝不能硬编码

提示：硬编码的 Shopify API Secret，请使用环境变量。

### 硬编码 Shopify API Key

严重程度：错误

API Key 应使用环境变量

提示：硬编码的 Shopify API Key，请使用环境变量。

### 缺少 HMAC 验证

严重程度：错误

Webhook 端点必须验证 HMAC 签名

提示：Webhook 处理器缺少 HMAC 验证，请使用 authenticate.webhook()。

### 同步 Webhook 处理

严重程度：警告

Webhook 处理器应快速响应

提示：Webhook 处理器中有多个 await 调用，请考虑异步处理。

### 缺少 Webhook 响应

严重程度：错误

Webhook 必须返回 200 状态码

提示：Webhook 处理器可能未返回正确响应。

### 重复 Webhook 注册

严重程度：警告

Webhook 应仅在 TOML 中定义

提示：基于代码的 Webhook 注册，请在 shopify.app.toml 中定义 Webhook。

### REST API 使用

严重程度：信息

REST API 已弃用，请使用 GraphQL

提示：检测到 REST API 使用，请考虑迁移到 GraphQL。

### 缺少速率限制处理

严重程度：警告

API 调用应处理 429 响应

提示：API 调用缺少速率限制处理，请实现重试逻辑。

### 内存会话存储

严重程度：警告

内存会话无法扩展

提示：内存会话存储，请使用 PrismaSessionStorage 或类似方案。

### 缺少会话验证

严重程度：错误

路由应验证会话

提示：Loader 缺少认证，请使用 authenticate.admin(request)。

## 协作

### 委派触发器

- 用户需要支付处理 -> stripe-integration（Shopify Payments 或 Stripe 集成）
- 用户需要自定义认证 -> auth-specialist（超越 Shopify OAuth）
- 用户需要邮件/短信通知 -> twilio-communications（Shopify 外的客户通知）
- 用户需要 AI 功能 -> llm-architect（产品描述、聊天机器人）
- 用户需要无服务器部署 -> aws-serverless（Lambda 或 Vercel 部署）

## 适用场景
- 用户提到或暗示：shopify app
- 用户提到或暗示：shopify
- 用户提到或暗示：embedded app
- 用户提到或暗示：polaris
- 用户提到或暗示：app bridge
- 用户提到或暗示：shopify webhook

## 限制
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出作为环境特定验证、测试或专家评审的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清