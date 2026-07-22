---
name: nextjs-best-practices
description: "Next.js App Router 开发原则。服务端组件、数据获取、路由模式。触发词：Next.js最佳实践、App Router、Server Components、服务端组件、Next.js开发模式"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Next.js 最佳实践

> Next.js App Router 开发原则。

---

## 1. 服务端组件 vs 客户端组件

### 决策树

```
Does it need...?
│
├── useState, useEffect, event handlers
│   └── Client Component ('use client')
│
├── Direct data fetching, no interactivity
│   └── Server Component (default)
│
└── Both? 
    └── Split: Server parent + Client child
```

### 默认选择

| 类型 | 用途 |
|------|------|
| **服务端组件** | 数据获取、布局、静态内容 |
| **客户端组件** | 表单、按钮、交互式 UI |

---

## 2. 数据获取模式

### 获取策略

| 模式 | 用途 |
|------|------|
| **默认** | 静态（构建时缓存） |
| **Revalidate** | ISR（基于时间的刷新） |
| **No-store** | 动态（每次请求） |

### 数据流

| 来源 | 模式 |
|------|------|
| 数据库 | Server Component 直接获取 |
| API | fetch 带缓存 |
| 用户输入 | 客户端状态 + Server Action |

---

## 3. 路由原则

### 文件约定

| 文件 | 用途 |
|------|------|
| `page.tsx` | 路由 UI |
| `layout.tsx` | 共享布局 |
| `loading.tsx` | 加载状态 |
| `error.tsx` | 错误边界 |
| `not-found.tsx` | 404 页面 |

### 路由组织

| 模式 | 用途 |
|------|------|
| 路由组 `(name)` | 组织路由但不影响 URL |
| 并行路由 `@slot` | 同级多页面 |
| 拦截路由 `(.)` | 模态框覆盖层 |

---

## 4. API 路由

### 路由处理器

| 方法 | 用途 |
|------|------|
| GET | 读取数据 |
| POST | 创建数据 |
| PUT/PATCH | 更新数据 |
| DELETE | 删除数据 |

### 最佳实践

- 使用 Zod 验证输入
- 返回正确的状态码
- 优雅地处理错误
- 尽可能使用 Edge 运行时

---

## 5. 性能原则

### 图片优化

- 使用 next/image 组件
- 为首屏图片设置 priority
- 提供模糊占位符
- 使用响应式尺寸

### 包体积优化

- 对重型组件使用动态导入
- 基于路由的代码分割（自动）
- 使用 bundle analyzer 分析

---

## 6. 元数据

### 静态 vs 动态

| 类型 | 用途 |
|------|------|
| 静态导出 | 固定元数据 |
| generateMetadata | 按路由动态生成 |

### 必要标签

- title（50-60 字符）
- description（150-160 字符）
- Open Graph 图片
- Canonical URL

---

## 7. 缓存策略

### 缓存层级

| 层级 | 控制方式 |
|------|----------|
| 请求 | fetch 选项 |
| 数据 | revalidate/tags |
| 完整路由 | 路由配置 |

### 重新验证

| 方法 | 用途 |
|------|------|
| 基于时间 | `revalidate: 60` |
| 按需 | `revalidatePath/Tag` |
| 不缓存 | `no-store` |

---

## 8. Server Actions

### 使用场景

- 表单提交
- 数据变更
- 触发重新验证

### 最佳实践

- 使用 'use server' 标记
- 验证所有输入
- 返回类型化的响应
- 处理错误

---

## 9. 反模式

| ❌ 不要 | ✅ 应该 |
|---------|---------|
| 到处使用 'use client' | 默认使用服务端组件 |
| 在客户端组件中获取数据 | 在服务端获取数据 |
| 跳过加载状态 | 使用 loading.tsx |
| 忽略错误边界 | 使用 error.tsx |
| 客户端包体积过大 | 使用动态导入 |

---

## 10. 项目结构

```
app/
├── (marketing)/     # Route group
│   └── page.tsx
├── (dashboard)/
│   ├── layout.tsx   # Dashboard layout
│   └── page.tsx
├── api/
│   └── [resource]/
│       └── route.ts
└── components/
    └── ui/
```

---

> **记住：** 服务端组件作为默认选择是有原因的。从服务端组件开始，仅在需要时添加客户端组件。

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
