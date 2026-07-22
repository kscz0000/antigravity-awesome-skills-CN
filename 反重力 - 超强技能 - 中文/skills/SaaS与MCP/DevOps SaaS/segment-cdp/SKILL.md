---
name: segment-cdp
description: Segment 客户数据平台专家模式，包括 Analytics.js、服务端追踪、Protocols 追踪计划、身份解析、目标配置和数据治理最佳实践。当用户提到 segment、analytics.js、客户数据平台、cdp、追踪计划、事件追踪、identify track page、数据路由时使用。
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Segment CDP

Segment 客户数据平台专家模式，包括 Analytics.js、服务端追踪、Protocols 追踪计划、身份解析、目标配置和数据治理最佳实践。

## Patterns

### Analytics.js Browser Integration

使用 Analytics.js 进行客户端追踪。包括 track、identify、page 和 group 调用。匿名 ID 在 identify 与用户合并前持续存在。

// Next.js - Analytics provider component
// lib/segment.ts
import { AnalyticsBrowser } from '@segment/analytics-next';

export const analytics = AnalyticsBrowser.load({
  writeKey: process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY!,
});

// Typed event helpers
export interface UserTraits {
  email?: string;
  name?: string;
  plan?: 'free' | 'pro' | 'enterprise';
  createdAt?: string;
  company?: {
    id: string;
    name: string;
  };
}

export function identify(userId: string, traits?: UserTraits) {
  analytics.identify(userId, traits);
}

export function track<T extends Record<string, any>>(
  event: string,
  properties?: T
) {
  analytics.track(event, properties);
}

export function page(name?: string, properties?: Record<string, any>) {
  analytics.page(name, properties);
}

export function group(groupId: string, traits?: Record<string, any>) {
  analytics.group(groupId, traits);
}

// React hook for analytics
// hooks/useAnalytics.ts
import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { analytics, page } from '@/lib/segment';

export function usePageTracking() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    // Track page view on route change
    page(pathname, {
      path: pathname,
      search: searchParams.toString(),
      url: window.location.href,
      title: document.title,
    });
  }, [pathname, searchParams]);
}

// Usage in _app.tsx or layout.tsx
function RootLayout({ children }) {
  usePageTracking();

  return <html>{children}</html>;
}

// Event tracking in components
function PricingButton({ plan }: { plan: string }) {
  const handleClick = () => {
    track('Plan Selected', {
      plan_name: plan,
      page: 'pricing',
      source: 'pricing_page',
    });
  };

  return <button onClick={handleClick}>Select {plan}</button>;
}

// Identify on auth
function onUserLogin(user: User) {
  identify(user.id, {
    email: user.email,
    name: user.name,
    plan: user.plan,
    createdAt: user.createdAt,
  });

  track('User Signed In', {
    method: 'email',
  });
}

### Context

- browser tracking
- website analytics
- client-side events

### Server-Side Tracking with Node.js

使用 @segment/analytics-node 进行高性能服务端追踪。非阻塞式内部批处理。适用于后端事件、webhook 和敏感数据。

// lib/segment-server.ts
import { Analytics } from '@segment/analytics-node';

// Initialize once
const analytics = new Analytics({
  writeKey: process.env.SEGMENT_WRITE_KEY!,
  flushAt: 20,      // Batch size before flush
  flushInterval: 10000,  // Flush every 10 seconds
});

// Typed server-side tracking
export interface ServerContext {
  ip?: string;
  userAgent?: string;
  locale?: string;
}

export function serverIdentify(
  userId: string,
  traits: Record<string, any>,
  context?: ServerContext
) {
  analytics.identify({
    userId,
    traits,
    context: {
      ip: context?.ip,
      userAgent: context?.userAgent,
      locale: context?.locale,
    },
  });
}

export function serverTrack(
  userId: string,
  event: string,
  properties?: Record<string, any>,
  context?: ServerContext
) {
  analytics.track({
    userId,
    event,
    properties,
    timestamp: new Date(),
    context: {
      ip: context?.ip,
      userAgent: context?.userAgent,
    },
  });
}

// Flush on shutdown
export async function closeAnalytics() {
  await analytics.closeAndFlush();
}

// Usage in API routes
// app/api/webhooks/stripe/route.ts
export async function POST(req: Request) {
  const event = await req.json();

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;

      serverTrack(
        session.client_reference_id,
        'Order Completed',
        {
          order_id: session.id,
          total: session.amount_total / 100,
          currency: session.currency,
          payment_method: session.payment_method_types[0],
        },
        { ip: req.headers.get('x-forwarded-for') || undefined }
      );

      // Also update user traits
      serverIdentify(session.client_reference_id, {
        total_spent: session.amount_total / 100,
        last_purchase_date: new Date().toISOString(),
      });
      break;

    case 'customer.subscription.created':
      serverTrack(
        event.data.object.metadata.user_id,
        'Subscription Started',
        {
          plan: event.data.object.items.data[0].price.nickname,
          amount: event.data.object.items.data[0].price.unit_amount / 100,
          interval: event.data.object.items.data[0].price.recurring.interval,
        }
      );
      break;
  }

  return new Response('ok');
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  await closeAnalytics();
  process.exit(0);
});

### Context

- server-side tracking
- backend events
- webhook processing

### Tracking Plan Design

使用 Object + Action 命名规范设计事件模式。定义必需属性、类型和验证规则。连接到 Protocols 进行强制执行。

// Tracking plan definition (conceptual YAML structure)
// This maps to Segment Protocols configuration
/*
tracking_plan:
  display_name: "MyApp Tracking Plan"
  rules:
    events:
      - name: "User Signed Up"
        description: "User completed registration"
        rules:
          required:
            - signup_method
          properties:
            signup_method:
              type: string
              enum: [email, google, github]
            referral_code:
              type: string
            utm_source:
              type: string

      - name: "Product Viewed"
        description: "User viewed a product page"
        rules:
          required:
            - product_id
            - product_name
          properties:
            product_id:
              type: string
            product_name:
              type: string
            category:
              type: string
            price:
              type: number
            currency:
              type: string
              default: USD

      - name: "Order Completed"
        description: "User completed a purchase"
        rules:
          required:
            - order_id
            - total
            - products
          properties:
            order_id:
              type: string
            total:
              type: number
            currency:
              type: string
            products:
              type: array
              items:
                type: object
                properties:
                  product_id: { type: string }
                  name: { type: string }
                  price: { type: number }
                  quantity: { type: integer }

    identify:
      traits:
        - name: email
          type: string
          required: true
        - name: name
          type: string
        - name: plan
          type: string
          enum: [free, pro, enterprise]
        - name: company
          type: object
          properties:
            id: { type: string }
            name: { type: string }
*/

// TypeScript implementation with type safety
// types/segment-events.ts
export interface TrackingEvents {
  'User Signed Up': {
    signup_method: 'email' | 'google' | 'github';
    referral_code?: string;
    utm_source?: string;
  };

  'Product Viewed': {
    product_id: string;
    product_name: string;
    category?: string;
    price?: number;
    currency?: string;
  };

  'Order Completed': {
    order_id: string;
    total: number;
    currency?: string;
    products: Array<{
      product_id: string;
      name: string;
      price: number;
      quantity: number;
    }>;
  };

  'Feature Used': {
    feature_name: string;
    usage_count?: number;
  };
}

// Type-safe track function
export function trackEvent<T extends keyof TrackingEvents>(
  event: T,
  properties: TrackingEvents[T]
) {
  analytics.track(event, properties);
}

// Usage - compile-time type checking
trackEvent('Order Completed', {
  order_id: 'ord_123',
  total: 99.99,
  products: [
    { product_id: 'prod_1', name: 'Widget', price: 49.99, quantity: 2 },
  ],
});

// This would be a TypeScript error:
// trackEvent('Order Completed', { total: 99.99 });  // Missing order_id

### Context

- tracking plan
- data governance
- event schema

### Identity Resolution

追踪匿名用户，然后通过 identify() 与已识别用户合并。使用 alias() 在系统之间进行身份合并。将用户分组到公司/组织中。

// Identity flow implementation
// lib/identity.ts

// Anonymous user tracking
export function trackAnonymousAction(event: string, properties?: object) {
  // Analytics.js automatically generates anonymousId
  analytics.track(event, properties);
}

// When user signs up or logs in
export async function identifyUser(user: {
  id: string;
  email: string;
  name?: string;
  plan?: string;
}) {
  // This merges anonymous history with user profile
  await analytics.identify(user.id, {
    email: user.email,
    name: user.name,
    plan: user.plan,
    created_at: new Date().toISOString(),
  });

  // Track the identification event
  analytics.track('User Identified', {
    method: 'signup',
  });
}

// B2B: Associate user with company
export function associateWithCompany(company: {
  id: string;
  name: string;
  plan?: string;
  employees?: number;
  industry?: string;
}) {
  analytics.group(company.id, {
    name: company.name,
    plan: company.plan,
    employees: company.employees,
    industry: company.industry,
  });
}

// Alias: Link identities (e.g., pre-signup email to user ID)
export function linkIdentities(previousId: string, newUserId: string) {
  // Use when you identified someone with a temporary ID
  // and now have their permanent user ID
  analytics.alias(newUserId, previousId);
}

// Full signup flow
export async function handleSignup(
  email: string,
  password: string,
  company?: { name: string; size: string }
) {
  // 1. Create user in your system
  const user = await createUser(email, password);

  // 2. Identify with Segment (merges anonymous history)
  await identifyUser({
    id: user.id,
    email: user.email,
    name: user.name,
    plan: 'free',
  });

  // 3. Track signup event
  analytics.track('User Signed Up', {
    signup_method: 'email',
    plan: 'free',
  });

  // 4. If B2B, associate with company
  if (company) {
    const companyRecord = await createCompany(company, user.id);

    associateWithCompany({
      id: companyRecord.id,
      name: company.name,
      employees: parseInt(company.size),
    });
  }
}

### Context

- user identification
- anonymous tracking
- b2b tracking

### Destinations Configuration

将数据路由到分析工具、数据仓库和营销平台。客户端工具使用 device-mode，服务端处理使用 cloud-mode。

// Segment destinations are configured in the Segment UI
// but here's how to optimize your implementation

// Conditional tracking based on destination needs
// lib/segment-destinations.ts

interface DestinationConfig {
  mixpanel: boolean;
  amplitude: boolean;
  googleAnalytics: boolean;
  warehouse: boolean;
  hubspot: boolean;
}

// Only send events needed by specific destinations
export function trackWithDestinations(
  event: string,
  properties: Record<string, any>,
  options?: {
    integrations?: Partial<DestinationConfig>;
  }
) {
  analytics.track(event, properties, {
    integrations: {
      // Override specific destinations
      All: true,  // Send to all by default
      ...options?.integrations,
    },
  });
}

// Example: Track revenue event only to revenue-tracking destinations
export function trackRevenue(order: {
  orderId: string;
  total: number;
  currency: string;
}) {
  analytics.track('Order Completed', {
    order_id: order.orderId,
    revenue: order.total,
    currency: order.currency,
  }, {
    integrations: {
      // Explicitly enable revenue destinations
      'Google Analytics 4': true,
      'Mixpanel': true,
      'Amplitude': true,
      // Disable non-revenue destinations
      'Intercom': false,
      'Zendesk': false,
    },
  });
}

// Send PII only to secure destinations
export function identifyWithPII(userId: string, traits: {
  email: string;
  phone?: string;
  address?: string;
}) {
  analytics.identify(userId, traits, {
    integrations: {
      'All': false,  // Disable all by default
      // Only send PII to trusted destinations
      'HubSpot': true,
      'Salesforce': true,
      'Warehouse': true,  // Your data warehouse
      // Don't send PII to analytics tools
      'Mixpanel': false,
      'Amplitude': false,
    },
  });
}

// Context enrichment for all events
export function enrichedTrack(
  event: string,
  properties: Record<string, any>
) {
  analytics.track(event, {
    ...properties,
    // Add common context
    app_version: process.env.NEXT_PUBLIC_APP_VERSION,
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString(),
  }, {
    context: {
      app: {
        name: 'MyApp',
        version: process.env.NEXT_PUBLIC_APP_VERSION,
      },
    },
  });
}

### Context

- data routing
- destination setup
- tool integration

### HTTP Tracking API

适用于任何环境的直接 HTTP API。适用于边缘函数、worker 和非 Node.js 后端。每个请求最多批处理 500KB。

// Edge/Serverless tracking via HTTP API
// lib/segment-http.ts

const SEGMENT_WRITE_KEY = process.env.SEGMENT_WRITE_KEY!;
const SEGMENT_API = 'https://api.segment.io/v1';

// Base64 encode write key for auth
const authHeader = `Basic ${btoa(SEGMENT_WRITE_KEY + ':')}`;

interface SegmentEvent {
  userId?: string;
  anonymousId?: string;
  event?: string;
  name?: string;  // For page calls
  properties?: Record<string, any>;
  traits?: Record<string, any>;
  context?: Record<string, any>;
  timestamp?: string;
}

async function segmentRequest(
  endpoint: string,
  payload: SegmentEvent
): Promise<void> {
  const response = await fetch(`${SEGMENT_API}${endpoint}`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ...payload,
      timestamp: payload.timestamp || new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    console.error('Segment API error:', await response.text());
  }
}

// HTTP API methods
export async function httpIdentify(
  userId: string,
  traits: Record<string, any>,
  context?: Record<string, any>
) {
  await segmentRequest('/identify', {
    userId,
    traits,
    context,
  });
}

export async function httpTrack(
  userId: string,
  event: string,
  properties?: Record<string, any>,
  context?: Record<string, any>
) {
  await segmentRequest('/track', {
    userId,
    event,
    properties,
    context,
  });
}

export async function httpPage(
  userId: string,
  name: string,
  properties?: Record<string, any>
) {
  await segmentRequest('/page', {
    userId,
    name,
    properties,
  });
}

// Batch API for high volume
export async function httpBatch(
  events: Array<{
    type: 'identify' | 'track' | 'page' | 'group';
    userId?: string;
    anonymousId?: string;
    event?: string;
    name?: string;
    properties?: Record<string, any>;
    traits?: Record<string, any>;
  }>
) {
  // Max 500KB per batch, 32KB per event
  await segmentRequest('/batch', {
    batch: events.map(e => ({
      ...e,
      timestamp: new Date().toISOString(),
    })),
  } as any);
}

// Cloudflare Worker example
export default {
  async fetch(request: Request): Promise<Response> {
    const { userId, action, data } = await request.json();

    // Track in edge function
    await httpTrack(userId, action, data, {
      ip: request.headers.get('cf-connecting-ip'),
      userAgent: request.headers.get('user-agent'),
    });

    return new Response('ok');
  },
};

### Context

- edge functions
- serverless
- http tracking

## Sharp Edges

### Anonymous ID Persists Until Explicit Reset

严重程度：MEDIUM

### Device Mode Bypasses Protocols Blocking

严重程度：HIGH

### HTTP API Has Strict Size Limits

严重程度：MEDIUM

### Track Calls Without Identify Are Anonymous

严重程度：HIGH

### Write Key in Client is Visible (But Intentional)

严重程度：LOW

### Events May Be Lost on Page Navigation

严重程度：MEDIUM

### Timestamps Without Timezone Cause Analytics Issues

严重程度：MEDIUM

### Tracking Before Consent Violates GDPR

严重程度：HIGH

## Validation Checks

### Dynamic Event Name

严重程度：ERROR

事件名称应为静态，不应包含动态值

消息：检测到动态事件名称。请使用静态事件名称配合动态属性。

### Inconsistent Event Name Casing

严重程度：WARNING

事件名称应遵循一致的大小写规范

消息：事件名称中存在混合大小写。请使用一致的命名规范（如 Title Case）。

### Track Without Prior Identify

严重程度：WARNING

在追踪关键事件前应先识别用户

消息：收入/转化事件未先进行 identify。请确保用户已被识别。

### Missing Analytics Reset on Logout

严重程度：WARNING

用户登出时应重置分析

消息：登出时未调用 analytics.reset()。匿名 ID 将延续到下一个用户。

### Hardcoded Segment Write Key

严重程度：ERROR

Write key 应使用环境变量

消息：硬编码的 Segment write key。请使用环境变量。

### PII Sent to All Destinations

严重程度：WARNING

PII 应有目标控制

消息：追踪中包含 PII 但未设置目标控制。请考虑限制目标。

### Event Without Proper Timestamp

严重程度：INFO

显式时间戳有助于历史数据处理

消息：服务端追踪未指定时间戳。建议添加时间戳。

### Potentially Large Property Values

严重程度：WARNING

超过 32KB 的属性将被拒绝

消息：可能存在过大的属性值。Segment 对每个事件有 32KB 限制。

### Tracking Before Consent Check

严重程度：ERROR

GDPR 要求在追踪前获得同意

消息：未经同意检查即进行追踪。请为 GDPR 实施同意管理。

## Collaboration

### Delegation Triggers

- user needs A/B testing -> analytics-specialist (Segment + LaunchDarkly/Optimizely integration)
- user needs data warehouse -> data-engineer (Segment to BigQuery/Snowflake/Redshift)
- user needs customer support integration -> zendesk-integration (Identify calls syncing to support tools)
- user needs marketing automation -> hubspot-integration (Segment to HubSpot destination)
- user needs consent management -> privacy-specialist (GDPR/CCPA compliance with Segment)

## When to Use
- User mentions or implies: segment
- User mentions or implies: analytics.js
- User mentions or implies: customer data platform
- User mentions or implies: cdp
- User mentions or implies: tracking plan
- User mentions or implies: event tracking
- User mentions or implies: identify track page
- User mentions or implies: data routing

## Limitations
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
