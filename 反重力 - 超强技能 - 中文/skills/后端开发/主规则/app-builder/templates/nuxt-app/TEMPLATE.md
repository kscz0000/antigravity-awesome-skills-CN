---
name: nuxt-app
description: Nuxt 3 全栈模板。Vue 3、Pinia、Tailwind、Prisma。触发词：Nuxt应用、Vue全栈、Nuxt 3项目
---
# Nuxt 3 全栈模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Nuxt 3 |
| 语言 | TypeScript |
| UI | Vue 3 (Composition API) |
| 状态 | Pinia |
| 数据库 | PostgreSQL + Prisma |
| 样式 | Tailwind CSS |
| 验证 | Zod |

---

## 目录结构

```
project-name/
├── prisma/
│   └── schema.prisma
├── server/
│   ├── api/
│   │   └── [resource]/
│   │       └── index.ts
│   └── utils/
│       └── db.ts         # Prisma 客户端
├── composables/
│   └── useAuth.ts
├── stores/
│   └── user.ts           # Pinia store
├── components/
│   └── ui/
├── pages/
│   ├── index.vue
│   └── [...slug].vue
├── layouts/
│   └── default.vue
├── assets/
│   └── css/
│       └── main.css
├── .env.example
├── nuxt.config.ts
└── package.json
```

---

## 核心概念

| 概念 | 描述 |
|---------|-------------|
| 自动导入 | 组件、composables、工具函数 |
| 基于文件的路由 | pages/ → 路由 |
| 服务端路由 | server/api/ → API 端点 |
| Composables | 可复用的响应式逻辑 |
| Pinia | 状态管理 |

---

## 环境变量

| 变量 | 用途 |
|----------|---------|
| DATABASE_URL | Prisma 连接 |
| NUXT_PUBLIC_APP_URL | 公开 URL |

---

## 设置步骤

1. `npx nuxi@latest init {{name}}`
2. `cd {{name}}`
3. `npm install @pinia/nuxt @prisma/client prisma zod`
4. `npm install -D @nuxtjs/tailwindcss`
5. 在 `nuxt.config.ts` 中添加模块:
   ```ts
   modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss']
   ```
6. `npx prisma init`
7. 配置模式
8. `npx prisma db push`
9. `npm run dev`

---

## 最佳实践

- 组件使用 `<script setup>`
- Composables 用于可复用逻辑
- Pinia stores 放在 `stores/` 文件夹
- 服务端路由用于 API 逻辑
- 自动导入保持代码简洁
- TypeScript 确保类型安全
- 参见 `@[skills/vue-expert]` 了解 Vue 模式
