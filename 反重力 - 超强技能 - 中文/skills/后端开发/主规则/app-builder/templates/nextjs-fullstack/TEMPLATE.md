---
name: nextjs-fullstack
description: Next.js 全栈模板原则。App Router、Prisma、Tailwind。触发词：Next.js全栈、全栈应用、Next.js项目
---
# Next.js 全栈模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Next.js 14 (App Router) |
| 语言 | TypeScript |
| 数据库 | PostgreSQL + Prisma |
| 样式 | Tailwind CSS |
| 认证 | Clerk (可选) |
| 验证 | Zod |

---

## 目录结构

```
project-name/
├── prisma/
│   └── schema.prisma
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── api/
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   ├── db.ts        # Prisma 客户端
│   │   └── utils.ts
│   └── types/
├── .env.example
└── package.json
```

---

## 核心概念

| 概念 | 描述 |
|---------|-------------|
| 服务端组件 | 默认，用于获取数据 |
| 服务端操作 | 表单变更 |
| 路由处理器 | API 端点 |
| Prisma | 类型安全的 ORM |

---

## 环境变量

| 变量 | 用途 |
|----------|---------|
| DATABASE_URL | Prisma 连接 |
| NEXT_PUBLIC_APP_URL | 公开 URL |

---

## 设置步骤

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. `npm install prisma @prisma/client zod`
3. `npx prisma init`
4. 配置模式
5. `npm run db:push`
6. `npm run dev`

---

## 最佳实践

- 默认使用服务端组件
- 变更操作使用服务端操作
- Prisma 用于类型安全的数据库访问
- Zod 用于验证
- 尽可能使用 Edge 运行时
