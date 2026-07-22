---
name: nextjs-saas
description: Next.js SaaS 模板原则。认证、支付、邮件。触发词：SaaS应用、订阅系统、Next.js SaaS
---
# Next.js SaaS 模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Next.js 14 (App Router) |
| 认证 | NextAuth.js v5 |
| 支付 | Stripe |
| 数据库 | PostgreSQL + Prisma |
| 邮件 | Resend |
| UI | Tailwind (询问用户: shadcn/Headless UI/自定义?) |

---

## 目录结构

```
project-name/
├── prisma/
├── src/
│   ├── app/
│   │   ├── (auth)/      # 登录、注册
│   │   ├── (dashboard)/ # 受保护路由
│   │   ├── (marketing)/ # 落地页、定价
│   │   └── api/
│   │       ├── auth/[...nextauth]/
│   │       └── webhooks/stripe/
│   ├── components/
│   │   ├── auth/
│   │   ├── billing/
│   │   └── dashboard/
│   ├── lib/
│   │   ├── auth.ts      # NextAuth 配置
│   │   ├── stripe.ts    # Stripe 客户端
│   │   └── email.ts     # Resend 客户端
│   └── config/
│       └── subscriptions.ts
└── package.json
```

---

## SaaS 功能

| 功能 | 实现 |
|---------|---------------|
| 认证 | NextAuth + OAuth |
| 订阅 | Stripe Checkout |
| 账单门户 | Stripe Portal |
| Webhooks | Stripe 事件 |
| 邮件 | 通过 Resend 发送事务性邮件 |

---

## 数据库模式

| 模型 | 字段 |
|-------|--------|
| User | id, email, stripeCustomerId, subscriptionId |
| Account | OAuth 提供商数据 |
| Session | 用户会话 |

---

## 环境变量

| 变量 | 用途 |
|----------|---------|
| DATABASE_URL | Prisma |
| NEXTAUTH_SECRET | 认证 |
| STRIPE_SECRET_KEY | 支付 |
| STRIPE_WEBHOOK_SECRET | Webhooks |
| RESEND_API_KEY | 邮件 |

---

## 设置步骤

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. 安装: `npm install next-auth @auth/prisma-adapter stripe resend`
3. 设置 Stripe 产品/价格
4. 配置环境变量
5. `npm run db:push`
6. `npm run stripe:listen` (webhooks)
7. `npm run dev`

---

## 最佳实践

- 使用路由组分离布局
- Stripe webhooks 同步订阅状态
- NextAuth 配合 Prisma adapter
- 使用 React Email 制作邮件模板
