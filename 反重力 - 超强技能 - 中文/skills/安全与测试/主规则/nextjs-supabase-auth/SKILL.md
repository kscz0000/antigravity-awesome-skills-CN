---
name: nextjs-supabase-auth
description: 将 Supabase Auth 与 Next.js App Router 专业集成。当用户要求"supabase auth next"、"authentication next.js"、"login supabase"、"auth middleware"、"protected route"、"auth callback"、"session management"时使用。
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Next.js + Supabase Auth

将 Supabase Auth 与 Next.js App Router 专业集成

## 能力

- nextjs-auth
- supabase-auth-nextjs
- auth-middleware
- auth-callback

## 前置条件

- 必需技能：nextjs-app-router, supabase-backend

## 模式

### Supabase 客户端设置

为不同上下文创建正确配置的 Supabase 客户端

**使用场景**：在 Next.js 项目中设置认证

// lib/supabase/client.ts (Browser client)
'use client'
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts (Server client)
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options)
          })
        },
      },
    }
  )
}

### 认证中间件

在中间件中保护路由并刷新会话

**使用场景**：需要路由保护或会话刷新时

// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options)
          })
        },
      },
    }
  )

  // Refresh session if expired
  const { data: { user } } = await supabase.auth.getUser()

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}

### 认证回调路由

处理 OAuth 回调并用 code 换取 session

**使用场景**：使用 OAuth 提供商（Google、GitHub 等）时

// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const next = searchParams.get('next') ?? '/'

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`)
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`)
}

### Server Action 认证

在 Server Actions 中处理认证操作

**使用场景**：从 Server Components 进行登录、注销或注册

// app/actions/auth.ts
'use server'
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'

export async function signIn(formData: FormData) {
  const supabase = await createClient()
  const { error } = await supabase.auth.signInWithPassword({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  })

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/', 'layout')
  redirect('/dashboard')
}

export async function signOut() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  revalidatePath('/', 'layout')
  redirect('/')
}

### 在 Server Component 中获取用户

在 Server Components 中访问已认证的用户

**使用场景**：在服务端渲染用户特定内容时

// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
    </div>
  )
}

## 验证检查

### 使用 getSession() 进行认证检查

严重级别：ERROR

消息：getSession() 不会验证 JWT。请使用 getUser() 进行安全的认证检查。

修复操作：将 getSession() 替换为 getUser() 以进行安全关键检查

### OAuth 缺少回调路由

严重级别：ERROR

消息：使用了 OAuth 但缺少 app/auth/callback/route.ts 处的回调路由

修复操作：创建 app/auth/callback/route.ts 以处理 OAuth 重定向

### 在服务端上下文中使用浏览器客户端

严重级别：ERROR

消息：在服务端上下文中使用了浏览器客户端。请改用 createServerClient。

修复操作：从 @supabase/ssr 导入并使用 createServerClient

### 受保护路由缺少中间件

严重级别：WARNING

消息：未找到 middleware.ts。建议添加中间件以保护路由。

修复操作：创建 middleware.ts 以保护路由并刷新会话

### 硬编码的认证重定向 URL

严重级别：WARNING

消息：硬编码了 localhost 重定向。请使用 origin 以兼容不同环境。

修复操作：使用 window.location.origin 或 process.env.NEXT_PUBLIC_SITE_URL

### 认证调用缺少错误处理

严重级别：WARNING

消息：认证操作缺少错误处理。请始终检查错误。

修复操作：解构 { data, error } 并处理错误情况

### 认证操作缺少重新验证

严重级别：WARNING

消息：认证操作缺少 revalidatePath。缓存可能显示过期的认证状态。

修复操作：在认证操作后添加 revalidatePath('/', 'layout')

### 仅客户端路由保护

严重级别：WARNING

消息：客户端路由保护会出现内容闪烁。请使用中间件。

修复操作：将保护逻辑移至 middleware.ts 以获得更好的用户体验

## 协作

### 委派触发器

- database|rls|queries|tables -> supabase-backend（认证需要数据库层）
- route|page|component|layout -> nextjs-app-router（认证需要 Next.js 模式）
- deploy|production|vercel -> vercel-deployment（认证需要部署配置）
- ui|form|button|design -> frontend（认证需要 UI 组件）

### 完整认证栈

技能：nextjs-supabase-auth, supabase-backend, nextjs-app-router, vercel-deployment

工作流程：

```
1. Database setup (supabase-backend)
2. Auth implementation (nextjs-supabase-auth)
3. Route protection (nextjs-app-router)
4. Deployment config (vercel-deployment)
```

### 受保护的 SaaS

技能：nextjs-supabase-auth, stripe-integration, supabase-backend

工作流程：

```
1. User authentication (nextjs-supabase-auth)
2. Customer sync (stripe-integration)
3. Subscription gating (supabase-backend)
```

## 相关技能

适用搭配：`nextjs-app-router`, `supabase-backend`

## 使用场景
- 用户提及或暗示：supabase auth next
- 用户提及或暗示：authentication next.js
- 用户提及或暗示：login supabase
- 用户提及或暗示：auth middleware
- 用户提及或暗示：protected route
- 用户提及或暗示：auth callback
- 用户提及或暗示：session management

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
