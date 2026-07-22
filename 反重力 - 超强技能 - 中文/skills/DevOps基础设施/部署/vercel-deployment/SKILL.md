---
name: vercel-deployment
description: Vercel 部署专家知识，涵盖 Next.js 部署、边缘函数、Serverless、环境变量配置。触发词：vercel部署、部署到vercel、边缘函数、serverless部署、环境变量配置、vercel deploy、部署上线
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Vercel 部署

使用 Next.js 部署到 Vercel 的专家知识

## 能力

- vercel
- 部署
- 边缘函数
- serverless
- 环境变量

## 前置条件

- 所需技能：nextjs-app-router

## 模式

### 环境变量配置

为所有环境正确配置环境变量

**何时使用**：在 Vercel 上设置新项目时

// Vercel 中的三个环境：
// - Development（本地开发）
// - Preview（PR 预览部署）
// - Production（主分支生产环境）

// 在 Vercel 控制台中：
// Settings → Environment Variables

// 公开变量（暴露给浏览器）
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

// 私有变量（仅服务端）
SUPABASE_SERVICE_ROLE_KEY=eyJ...  // 绝不要加 NEXT_PUBLIC_！
DATABASE_URL=postgresql://...

// 各环境的值：
// Production：真实数据库、生产 API 密钥
// Preview：预发布数据库、测试 API 密钥
// Development：本地/开发值（也在 .env.local 中）

// 在代码中检查环境：
const isProduction = process.env.VERCEL_ENV === 'production'
const isPreview = process.env.VERCEL_ENV === 'preview'

### Edge 与 Serverless 函数

为 API 路由选择正确的运行时

**何时使用**：创建 API 路由或中间件时

// EDGE 运行时 — 冷启动快，API 有限
// 适用于：认证检查、重定向、简单转换

// app/api/hello/route.ts
export const runtime = 'edge'

export async function GET() {
  return Response.json({ message: 'Hello from Edge!' })
}

// middleware.ts（始终为 edge 运行时）
export function middleware(request: NextRequest) {
  // 在此进行快速认证检查
}

// SERVERLESS（Node.js）— 完整 Node API，冷启动较慢
// 适用于：数据库查询、文件操作、重度计算

// app/api/users/route.ts
export const runtime = 'nodejs'  // 默认值，可省略

export async function GET() {
  const users = await db.query('SELECT * FROM users')
  return Response.json(users)
}

### 构建优化

优化构建以实现更快的部署和更小的包体积

**何时使用**：准备生产部署时

// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // 最小化输出
  output: 'standalone',  // 用于 Docker/自托管

  // 图片优化
  images: {
    remotePatterns: [
      { hostname: 'your-cdn.com' },
    ],
  },

  // 包分析器（仅开发环境）
  // npm install @next/bundle-analyzer
  ...(process.env.ANALYZE === 'true' && {
    webpack: (config) => {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
      config.plugins.push(new BundleAnalyzerPlugin())
      return config
    },
  }),
}

// 减小 serverless 函数体积：
// - 对大型库使用动态导入
// - 使用以下命令检查包：npx @next/bundle-analyzer

### 预览部署工作流

使用预览部署进行 PR 审查

**何时使用**：设置团队开发工作流时

// 每个 PR 自动获得唯一的预览 URL

// 使用密码保护预览部署：
// Vercel 控制台 → Settings → Deployment Protection

// 为预览环境使用不同的环境变量：
// - PREVIEW：使用预发布数据库
// - PRODUCTION：使用生产数据库

// 在代码中检测预览环境：
if (process.env.VERCEL_ENV === 'preview') {
  // 显示"预览"横幅
  // 使用测试支付处理器
  // 禁用分析
}

// 在 PR 上评论预览 URL（Vercel GitHub 集成自动完成）

### 自定义域名配置

配置自定义域名及正确的 SSL

**何时使用**：上线生产环境时

// 在 Vercel 控制台 → Domains

// 添加域名：
// - example.com（根域名）
// - www.example.com（子域名）

// DNS 配置（在域名注册商处）：
// Type: A, Name: @, Value: 76.76.21.21
// Type: CNAME, Name: www, Value: cname.vercel-dns.com

// 将 www 重定向到根域名（或反之）：
// Vercel 会自动处理

// 在 next.config.js 中配置重定向：
module.exports = {
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,  // 308
      },
    ]
  },
}

## 陷阱

### NEXT_PUBLIC_ 将密钥暴露给浏览器

严重程度：严重

场景：对敏感 API 密钥使用 NEXT_PUBLIC_ 前缀

症状：
- 密钥在浏览器 DevTools → Sources 中可见
- 安全审计发现暴露的密钥
- 来自未知来源的异常 API 访问

原因分析：
带有 NEXT_PUBLIC_ 前缀的变量会在构建时内联到 JavaScript 包中。
任何人都可以在浏览器 DevTools 中查看它们，包括所有用户和潜在攻击者。

推荐修复：

仅对真正公开的值使用 NEXT_PUBLIC_：

// 可以安全使用 NEXT_PUBLIC_
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...  // Anon 密钥设计为公开的
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_GA_ID=G-XXXXXXX

// 绝不要使用 NEXT_PUBLIC_
SUPABASE_SERVICE_ROLE_KEY=eyJ...     // 完整数据库访问权限！
STRIPE_SECRET_KEY=sk_live_...         // 可以扣款！
DATABASE_URL=postgresql://...          // 直接数据库访问！
JWT_SECRET=...                         // 可以伪造令牌！

// 在以下位置访问仅服务端变量：
// - Server Components（app router）
// - API Routes
// - Server Actions（'use server'）
// - getServerSideProps（pages router）

### 预览部署使用生产数据库

严重程度：高

场景：未为预览环境配置独立的环境变量

症状：
- 测试数据出现在生产环境中
- PR 合并后生产数据被损坏
- 用户看到测试账号/内容

原因分析：
预览部署运行的是未经测试的代码。如果它们使用生产数据库，
PR 中的 bug 可能损坏生产数据。此外，测试人员可能创建
出现在生产环境中的测试数据。

推荐修复：

为每个环境设置独立的数据库：

// 在 Vercel 控制台 → Settings → Environment Variables

// Production（仅生产环境）：
DATABASE_URL=postgresql://prod-host/prod-db

// Preview（仅预览环境）：
DATABASE_URL=postgresql://staging-host/staging-db

// 或使用 Vercel 的分支数据库：
// - Neon、PlanetScale、Supabase 都支持分支数据库
// - 为每个 PR 自动创建预览数据库

// 对于 Supabase，创建一个预发布项目：
// Production：
NEXT_PUBLIC_SUPABASE_URL=https://prod-xxx.supabase.co

// Preview：
NEXT_PUBLIC_SUPABASE_URL=https://staging-xxx.supabase.co

### Serverless 函数过大，冷启动缓慢

严重程度：高

场景：API 路由或服务端组件初始加载缓慢

症状：
- 首次请求耗时 3-10+ 秒
- 后续请求很快
- 函数大小超限错误
- 部署因大小错误失败

原因分析：
Vercel serverless 函数有 50MB 限制（压缩后）。
大函数意味着慢冷启动（1-5+ 秒）。
puppeteer、sharp 等重度依赖可能导致此问题。

推荐修复：

减小函数体积：

// 1. 对大型库使用动态导入
export async function GET() {
  const sharp = await import('sharp')  // 仅在需要时加载
  // ...
}

// 2. 将重度处理移至 edge 或外部服务
export const runtime = 'edge'  // 更小、更快的冷启动

// 3. 检查包体积
// npx @next/bundle-analyzer
// 查找大型依赖

// 4. 对重度任务使用外部服务
// - 图片处理：Cloudinary、imgix
// - PDF 生成：API 服务
// - Puppeteer：Browserless.io

// 5. 拆分为多个函数
// /api/heavy-task/start - 排队任务
// /api/heavy-task/status - 检查进度

### Edge 运行时缺少 Node.js API

严重程度：高

场景：在 edge 运行时函数中使用 Node.js API

症状：
- 运行时报错"X is not defined"
- 找不到模块 fs
- 本地正常，部署后失败
- 中间件崩溃

原因分析：
Edge 运行时运行在 V8 上，而非 Node.js。许多 Node API 不可用：
fs、path、crypto（部分）、child_process 及大多数原生模块。
代码将在运行时以"X is not defined"报错失败。

推荐修复：

使用 edge 前检查 API 兼容性：

// Edge 中支持的 API：
// - fetch、Request、Response
// - crypto.subtle（Web Crypto）
// - TextEncoder、TextDecoder
// - URL、URLSearchParams
// - Headers、FormData
// - setTimeout、setInterval

// Edge 中不支持的 API：
// - fs、path、os
// - Buffer（使用 Uint8Array）
// - crypto.createHash（使用 crypto.subtle）
// - 大多数带有原生依赖的 npm 包

// 如果需要 Node.js API：
export const runtime = 'nodejs'  // 改用 Node 运行时

// 在 edge 中进行加密哈希：
// 错误
import { createHash } from 'crypto'  // 在 edge 中会失败

// 正确
async function hash(message: string) {
  const encoder = new TextEncoder()
  const data = encoder.encode(message)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}

### 函数超时导致操作不完整

严重程度：中

场景：长时间运行的操作超时

症状：
- 任务在 X 秒后超时
- 数据库操作不完整
- 文件上传部分完成
- 函数在执行中途被终止

原因分析：
Vercel 有超时限制：
- Hobby：10 秒
- Pro：60 秒（可增加至 300）
- Enterprise：900 秒

超过限制的操作会在执行中途被终止。

推荐修复：

正确处理长时间操作：

// 1. 尽早返回，异步处理
export async function POST(request: Request) {
  const data = await request.json()

  // 排队进行后台处理
  await queue.add('process-data', data)

  // 立即返回
  return Response.json({ status: 'queued' })
}

// 2. 对长响应使用流式传输
export async function GET() {
  const stream = new ReadableStream({
    async start(controller) {
      for (const chunk of generateChunks()) {
        controller.enqueue(chunk)
        await sleep(100)  // 防止超时
      }
      controller.close()
    }
  })
  return new Response(stream)
}

// 3. 对重度处理使用外部服务
// - 触发 serverless 函数，返回任务 ID
// - 在后台处理（Inngest、Trigger.dev）
// - 客户端轮询完成状态

// 4. 增加超时时间（Pro 计划）
// vercel.json:
{
  "functions": {
    "app/api/slow/route.ts": {
      "maxDuration": 60
    }
  }
}

### 环境变量构建时存在但运行时缺失

严重程度：中

场景：环境变量在构建时正常但运行时为 undefined

症状：
- 生产环境中环境变量为 undefined
- 在控制台更新后值不变
- 开发环境正常，生产环境值错误
- 需要重新部署才能更新值

原因分析：
某些环境变量仅在构建时可用（硬编码到包中）。
如果你期望运行时值但它被构建时固化，你会得到
构建时的值或 undefined。

推荐修复：

理解环境变量何时被读取：

// 构建时（固化到包中）：
// - NEXT_PUBLIC_* 变量
// - next.config.js
// - generateStaticParams
// - 静态页面

// 运行时（每次请求时读取）：
// - Server Components（无缓存）
// - API Routes
// - Server Actions
// - Middleware

// 强制运行时读取：
export const dynamic = 'force-dynamic'

// 对于必须是运行时的配置：
// 不要使用 NEXT_PUBLIC_，在服务端读取后传递给客户端

// 检查你需要哪些环境变量：
// 构建时：URL、公开密钥、功能开关（如果是静态的）
// 运行时：密钥、数据库 URL、用户特定配置

### 跨域调用 API 路由时 CORS 错误

严重程度：中

场景：不同域名的前端无法调用 API 路由

症状：
- 浏览器控制台出现 CORS 策略错误
- 没有 Access-Control-Allow-Origin 头
- 请求在 Postman 中正常但浏览器中失败
- 同源正常，跨域失败

原因分析：
默认情况下，浏览器阻止跨域请求。Vercel 不会
自动添加 CORS 头。如果你的前端在不同域名
（或开发环境的 localhost），请求会失败。

推荐修复：

为 API 路由添加 CORS 头：

// app/api/data/route.ts
export async function GET(request: Request) {
  const data = await fetchData()

  return Response.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',  // 或指定域名
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

// 处理预检请求
export async function OPTIONS() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

// 或使用 next.config.js 为所有路由配置：
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
        ],
      },
    ]
  },
}

### 部署后页面显示过期数据

严重程度：中

场景：新部署后更新的数据未显示

症状：
- 部署后显示旧内容
- 更改不会立即可见
- 不同用户看到不同版本
- 数据已更新但页面未更新

原因分析：
Vercel 缓存策略激进。静态页面在边缘节点缓存。
即使是动态页面，如果未正确配置也可能被缓存。
旧缓存版本会一直提供服务，直到缓存过期或被清除。

推荐修复：

控制缓存行为：

// 强制不缓存（始终最新）
export const dynamic = 'force-dynamic'
export const revalidate = 0

// ISR — 每 60 秒重新验证
export const revalidate = 60

// 按需重新验证（数据变更后）
import { revalidatePath, revalidateTag } from 'next/cache'

// 在 Server Action 中：
async function updatePost(id: string) {
  await db.post.update({ ... })
  revalidatePath(`/posts/${id}`)  // 清除此页面缓存
  revalidateTag('posts')          // 清除带有此标签的所有缓存
}

// 通过 API 清除缓存（部署钩子）：
// POST https://your-site.vercel.app/api/revalidate?path=/posts

// 在响应头中检查缓存状态：
// x-vercel-cache: HIT = 从缓存提供服务
// x-vercel-cache: MISS = 新鲜生成

## 验证检查

### NEXT_PUBLIC 变量中的密钥

严重程度：严重

消息：密钥通过 NEXT_PUBLIC_ 前缀暴露，将在浏览器中可见。

修复操作：移除 NEXT_PUBLIC_ 前缀，仅在服务端代码中访问

### 硬编码的 Vercel URL

严重程度：警告

消息：硬编码的 Vercel URL。请改用 VERCEL_URL 环境变量。

修复操作：使用 process.env.VERCEL_URL 或 NEXT_PUBLIC_VERCEL_URL

### Edge 运行时中的 Node.js API

严重程度：错误

消息：在 Edge 运行时中使用了 Node.js 模块。fs/path 在 Edge 中不可用。

修复操作：使用 runtime = 'nodejs' 或移除 Node.js 依赖

### API 路由缺少 CORS 头

严重程度：警告

消息：没有 CORS 头的 API 路由可能在跨域请求时失败。

修复操作：如果 API 被其他域名调用，添加 Access-Control-Allow-Origin 头

### API 路由缺少错误处理

严重程度：警告

消息：API 路由没有 try/catch。未处理的错误返回 500 且无详情。

修复操作：用 try/catch 包裹并返回适当的错误响应

### 静态上下文中读取密钥

严重程度：警告

消息：在静态生成中访问了服务端密钥。值被固化到构建中。

修复操作：将密钥访问移至运行时代码，或对公开值使用 NEXT_PUBLIC_

### 大型包导入

严重程度：警告

消息：导入了大型包。可能导致冷启动缓慢。请考虑替代方案。

修复操作：使用 lodash-es 配合 tree shaking、用 date-fns 替代 moment、用 @aws-sdk/client-* 替代 aws-sdk

### 动态页面缺少重新验证配置

严重程度：警告

消息：动态页面没有重新验证配置。请考虑设置重新验证策略。

修复操作：添加 export const revalidate = 60 用于 ISR，或 0 用于不缓存

## 协作

### 委派触发器

- next.js|app router|pages|server components -> nextjs-app-router（部署需要 Next.js 模式）
- database|supabase|backend -> supabase-backend（部署需要数据库）
- auth|authentication|session -> nextjs-supabase-auth（部署需要认证配置）
- monitoring|logs|errors|analytics -> analytics-architecture（部署需要监控）

### 生产上线

技能：vercel-deployment、nextjs-app-router、supabase-backend、nextjs-supabase-auth

工作流：

```
1. 应用配置 (nextjs-app-router)
2. 数据库设置 (supabase-backend)
3. 认证配置 (nextjs-supabase-auth)
4. 部署 (vercel-deployment)
```

### CI/CD 流水线

技能：vercel-deployment、devops、qa-engineering

工作流：

```
1. 测试自动化 (qa-engineering)
2. 流水线配置 (devops)
3. 部署策略 (vercel-deployment)
```

## 相关技能

配合使用：`nextjs-app-router`、`supabase-backend`

## 何时使用
- 用户提及或暗示：vercel
- 用户提及或暗示：部署
- 用户提及或暗示：deployment
- 用户提及或暗示：托管
- 用户提及或暗示：生产环境
- 用户提及或暗示：环境变量
- 用户提及或暗示：边缘函数
- 用户提及或暗示：serverless 函数

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
