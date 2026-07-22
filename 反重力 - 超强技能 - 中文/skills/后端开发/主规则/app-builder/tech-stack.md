# 技术栈选择 (2025)

> Web 应用的默认和替代技术选择。

## 默认技术栈 (Web 应用 - 2025)

```yaml
Frontend:
  framework: Next.js 16 (Stable)
  language: TypeScript 5.7+
  styling: Tailwind CSS v4
  state: React 19 Actions / Server Components
  bundler: Turbopack (Stable for Dev)

Backend:
  runtime: Node.js 23
  framework: Next.js API Routes / Hono (for Edge)
  validation: Zod / TypeBox

Database:
  primary: PostgreSQL
  orm: Prisma / Drizzle
  hosting: Supabase / Neon

Auth:
  provider: Auth.js (v5) / Clerk

Monorepo:
  tool: Turborepo 2.0
```

## 替代方案

| 需求 | 默认 | 替代方案 |
|------|---------|-------------|
| 实时功能 | - | Supabase Realtime, Socket.io |
| 文件存储 | - | Cloudinary, S3 |
| 支付 | Stripe | LemonSqueezy, Paddle |
| 邮件 | - | Resend, SendGrid |
| 搜索 | - | Algolia, Typesense |
