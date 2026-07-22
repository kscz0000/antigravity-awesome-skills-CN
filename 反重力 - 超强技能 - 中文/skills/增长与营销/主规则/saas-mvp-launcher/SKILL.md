---
name: saas-mvp-launcher
description: "当从零开始规划或构建SaaS MVP时使用。提供涵盖技术栈、架构、认证、支付和发布清单的结构化路线图。触发词：SaaS MVP、SaaS启动器、SaaS构建、MVP规划、技术栈选择、架构设计、认证集成、支付集成、发布清单"
risk: safe
source: community
date_added: "2026-03-04"
---

# SaaS MVP 启动器

## 概述

本技能指导你在最短时间内构建生产就绪的SaaS MVP。涵盖从创意验证、技术栈选择到认证、支付、数据库设计、部署和发布的完整流程——使用现代且经过实战检验的工具。

## 使用场景

- 从零开始构建新产品时使用
- 需要为Web应用选择技术栈时使用
- 为SaaS设置认证、计费或数据库时使用
- 上线前需要结构化发布清单时使用
- 设计多租户应用架构时使用
- 对现有早期SaaS进行技术评审时使用

## 分步指南

### 1. 构建前先验证

编写任何代码前，先验证创意：

```
验证清单：
- [ ] 能否用一句话描述问题？
- [ ] 精确客户是谁？（不是"所有人"）
- [ ] 他们目前为解决此问题付费多少？
- [ ] 是否与5位以上潜在客户交谈过？
- [ ] 他们是否愿意为你的解决方案支付$X/月？
```

**规则：** 如果无法让3人预付款或签署意向书，暂不构建。

### 2. 选择技术栈

推荐的现代SaaS技术栈（2026年）：

| 层级 | 选择 | 原因 |
|------|------|------|
| 前端 | Next.js 15 + TypeScript | 全栈，优秀开发体验，Vercel部署 |
| 样式 | Tailwind CSS + shadcn/ui | 快速，无障碍，可定制 |
| 后端 | Next.js API Routes 或 tRPC | 类型安全，代码共置 |
| 数据库 | PostgreSQL via Supabase | 可靠，可扩展，免费层 |
| ORM | Prisma 或 Drizzle | 类型安全查询，迁移管理 |
| 认证 | Clerk 或 NextAuth.js | 社交登录，会话管理 |
| 支付 | Stripe | 行业标准，文档完善 |
| 邮件 | Resend + React Email | 现代，开发者友好 |
| 部署 | Vercel（前端）+ Railway（后端） | 零配置，快速CI/CD |
| 监控 | Sentry + PostHog | 错误跟踪 + 分析 |

### 3. 项目结构

```
my-saas/
├── app/                    # Next.js App Router
│   ├── (auth)/             # 认证路由（登录、注册）
│   ├── (dashboard)/        # 受保护的应用路由
│   ├── (marketing)/        # 公开的落地页
│   └── api/                # API路由
├── components/
│   ├── ui/                 # shadcn/ui组件
│   └── [feature]/          # 功能特定组件
├── lib/
│   ├── db.ts               # 数据库客户端（Prisma/Drizzle）
│   ├── stripe.ts           # Stripe客户端
│   └── email.ts            # 邮件客户端（Resend）
├── prisma/
│   └── schema.prisma       # 数据库模式
├── .env.local              # 环境变量
└── middleware.ts           # 认证中间件
```

### 4. 核心数据库模式（多租户SaaS）

```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  createdAt     DateTime  @default(now())
  subscription  Subscription?
  workspaces    WorkspaceMember[]
}

model Workspace {
  id        String    @id @default(cuid())
  name      String
  slug      String    @unique
  plan      Plan      @default(FREE)
  members   WorkspaceMember[]
  createdAt DateTime  @default(now())
}

model Subscription {
  id                 String   @id @default(cuid())
  userId             String   @unique
  user               User     @relation(fields: [userId], references: [id])
  stripeCustomerId   String   @unique
  stripePriceId      String
  stripeSubId        String   @unique
  status             String   # active, canceled, past_due
  currentPeriodEnd   DateTime
}

enum Plan {
  FREE
  PRO
  ENTERPRISE
}
```

### 5. 认证设置（Clerk）

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/pricing',
  '/blog(.*)',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
]);

export default clerkMiddleware((auth, req) => {
  if (!isPublicRoute(req)) {
    auth().protect();
  }
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

### 6. Stripe集成（订阅）

```typescript
// lib/stripe.ts
import Stripe from 'stripe';
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-27.acacia',
});

// 创建结账会话
export async function createCheckoutSession(userId: string, priceId: string) {
  return stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    metadata: { userId },
  });
}
```

### 7. 发布前清单

**技术：**
- [ ] 认证功能正常（注册、登录、登出、密码重置）
- [ ] 支付流程端到端正常（订阅、取消、升级）
- [ ] 错误监控已配置（Sentry）
- [ ] 环境变量已文档化
- [ ] 数据库备份已配置
- [ ] API路由已设置速率限制
- [ ] 所有表单使用Zod进行输入验证
- [ ] 已强制HTTPS，安全头已设置

**产品：**
- [ ] 落地页具有清晰的价值主张
- [ ] 定价页面有2-3个层级
- [ ] 引导流程（5分钟内获得首次价值）
- [ ] 邮件序列（欢迎、试用结束、支付失败）
- [ ] 服务条款和隐私政策页面
- [ ] 支持渠道（邮件/聊天）

**营销：**
- [ ] 域名已购买并配置
- [ ] 所有页面已设置SEO元标签
- [ ] 已安装Google Analytics或PostHog
- [ ] 社交媒体账号已创建
- [ ] Product Hunt草稿已准备

## 最佳实践

- ✅ **推荐：** 在4-6周内发布可工作的MVP，然后根据反馈迭代
- ✅ **推荐：** 从第一天开始收费——免费用户无法验证产品市场契合度
- ✅ **推荐：** 先构建"快乐路径"，稍后处理边缘情况
- ✅ **推荐：** 使用功能标志进行渐进式发布（如Vercel Edge Config）
- ✅ **推荐：** 从发布当天开始监控用户行为——而不是问题出现后
- ❌ **避免：** 在与客户交谈前构建所有功能
- ❌ **避免：** 在达到$10k MRR前优化扩展性
- ❌ **避免：** 构建自定义认证系统——使用Clerk、Auth.js或Supabase Auth
- ❌ **避免：** 跳过引导流程——这是大多数SaaS流失用户的地方

## 故障排除

**问题：** 用户注册但未激活（未使用核心功能）
**解决方案：** 减少获得首次价值的步骤。使用PostHog跟踪用户在引导流程中的流失点。

**问题：** 试用后高流失率
**解决方案：** 添加退出调查。大多数流失是由于感知价值不足，而非价格问题。

**问题：** 本地未收到Stripe webhook事件
**解决方案：** 使用Stripe CLI：`stripe listen --forward-to localhost:3000/api/webhooks/stripe`

**问题：** 生产环境数据库迁移失败
**解决方案：** 在生产环境中始终运行 `prisma migrate deploy`（而非 `prisma migrate dev`）。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。