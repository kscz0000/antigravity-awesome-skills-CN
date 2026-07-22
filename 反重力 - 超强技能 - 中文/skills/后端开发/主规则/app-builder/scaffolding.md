# 项目脚手架

> 新项目的目录结构和核心文件。

---

## Next.js 全栈结构 (2025 优化版)

```
project-name/
├── src/
│   ├── app/                        # 仅路由（薄层）
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── (auth)/                 # 路由组 - 认证页面
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/            # 路由组 - 仪表盘布局
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── api/
│   │       └── [resource]/route.ts
│   │
│   ├── features/                   # 基于功能的模块
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── actions.ts          # 服务端操作
│   │   │   ├── queries.ts          # 数据获取
│   │   │   └── types.ts
│   │   ├── products/
│   │   │   ├── components/
│   │   │   ├── actions.ts
│   │   │   └── queries.ts
│   │   └── cart/
│   │       └── ...
│   │
│   ├── shared/                     # 共享工具
│   │   ├── components/ui/          # 可复用 UI 组件
│   │   ├── lib/                    # 工具函数、辅助方法
│   │   └── hooks/                  # 全局 hooks
│   │
│   └── server/                     # 仅服务端代码
│       ├── db/                     # 数据库客户端 (Prisma)
│       ├── auth/                   # 认证配置
│       └── services/               # 外部 API 集成
│
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
│
├── public/
├── .env.example
├── .env.local
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

---

## 结构原则

| 原则 | 实现方式 |
|-----------|----------------|
| **功能隔离** | 每个功能在 `features/` 中有自己的组件、hooks、actions |
| **服务端/客户端分离** | 仅服务端代码放在 `server/`，防止意外导入客户端 |
| **薄路由** | `app/` 仅用于路由，逻辑放在 `features/` |
| **路由组** | `(groupName)/` 用于共享布局而不影响 URL |
| **共享代码** | `shared/` 用于真正可复用的 UI 和工具 |

---

## 核心文件

| 文件 | 用途 |
|------|---------|
| `package.json` | 依赖 |
| `tsconfig.json` | TypeScript + 路径别名 (`@/features/*`) |
| `tailwind.config.ts` | Tailwind 配置 |
| `.env.example` | 环境变量模板 |
| `README.md` | 项目文档 |
| `.gitignore` | Git 忽略规则 |
| `prisma/schema.prisma` | 数据库模式 |

---

## 路径别名 (tsconfig.json)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/features/*": ["./src/features/*"],
      "@/shared/*": ["./src/shared/*"],
      "@/server/*": ["./src/server/*"]
    }
  }
}
```

---

## 何时使用什么

| 需求 | 位置 |
|------|----------|
| 新页面/路由 | `app/(group)/page.tsx` |
| 功能组件 | `features/[name]/components/` |
| 服务端操作 | `features/[name]/actions.ts` |
| 数据获取 | `features/[name]/queries.ts` |
| 可复用按钮/输入框 | `shared/components/ui/` |
| 数据库查询 | `server/db/` |
| 外部 API 调用 | `server/services/` |
