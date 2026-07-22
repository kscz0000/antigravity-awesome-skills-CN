---
name: clerk-auth
description: Clerk 认证实现专家模式，涵盖中间件、组织、Webhook 和用户同步。触发词：Clerk认证、用户认证、登录注册、身份验证、多租户、组织管理、SSO单点登录、中间件保护、Webhook同步
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Clerk 认证

Clerk 认证实现专家模式，涵盖中间件、组织、Webhook 和用户同步。

## 模式

### Next.js App Router 配置

Next.js 14/15 App Router 的完整 Clerk 配置。

包括 ClerkProvider、环境变量和基础登录/注册组件。

核心组件：
- ClerkProvider：为应用提供认证上下文
- <SignIn />, <SignUp />：预构建的认证表单
- <UserButton />：带会话管理的用户菜单

### 代码示例

# Environment variables (.env.local)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding

// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}

// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignIn />
    </div>
  );
}

// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignUp />
    </div>
  );
}

// components/Header.tsx
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';

export function Header() {
  return (
    <header className="flex justify-between p-4">
      <h1>My App</h1>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserButton afterSignOutUrl="/" />
      </SignedIn>
    </header>
  );
}

### 反模式

- 模式：在页面组件中使用 ClerkProvider | 原因：Provider 必须在根布局中包裹整个应用 | 修复：将 ClerkProvider 移至 app/layout.tsx
- 模式：未配置中间件就使用 auth() | 原因：auth() 需要配置 clerkMiddleware | 修复：在 middleware.ts 中设置 clerkMiddleware

### 参考资料

- https://clerk.com/docs/nextjs/getting-started/quickstart

### 中间件路由保护

使用 clerkMiddleware 和 createRouteMatcher 保护路由。

最佳实践：
- 在项目根目录使用单一 middleware.ts 文件
- 使用 createRouteMatcher 定义路由组
- 使用 auth.protect() 进行显式保护
- 在中间件中集中所有认证逻辑

### 代码示例

// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

// 定义受保护的路由模式
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/settings(.*)',
  '/api/private(.*)',
]);

// 定义公开路由（可选，用于清晰说明）
const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  // 保护匹配的路由
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    // 匹配所有路由，除了静态文件
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // 始终对 API 路由运行
    '/(api|trpc)(.*)',
  ],
};

// 高级：基于角色的保护
export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }

  // 管理员路由需要管理员角色
  if (req.nextUrl.pathname.startsWith('/admin')) {
    await auth.protect({
      role: 'org:admin',
    });
  }

  // 高级路由需要高级权限
  if (req.nextUrl.pathname.startsWith('/premium')) {
    await auth.protect({
      permission: 'org:premium:access',
    });
  }
});

### 反模式

- 模式：多个 middleware.ts 文件 | 原因：导致冲突和重定向循环 | 修复：使用带路由匹配器的单一 middleware.ts
- 模式：在组件中手动重定向 | 原因：双重重定向、遗漏路由 | 修复：在中间件中处理所有重定向
- 模式：缺少 matcher 配置 | 原因：中间件不会在所有路由上运行 | 修复：添加全面的 matcher 模式

### 参考资料

- https://clerk.com/docs/reference/nextjs/clerk-middleware

### 服务端组件认证

在服务端组件中使用 auth() 和 currentUser() 访问认证状态。

核心函数：
- auth()：返回 userId、sessionId、orgId、claims
- currentUser()：返回完整 User 对象
- 两者都需要配置 clerkMiddleware

### 代码示例

// app/dashboard/page.tsx (Server Component)
import { auth, currentUser } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect('/sign-in');
  }

  // 完整用户数据（计入速率限制）
  const user = await currentUser();

  return (
    <div>
      <h1>Welcome, {user?.firstName}!</h1>
      <p>Email: {user?.emailAddresses[0]?.emailAddress}</p>
    </div>
  );
}

// 使用 auth() 进行快速检查
export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { userId, orgId, orgRole } = await auth();

  if (!userId) {
    redirect('/sign-in');
  }

  // 检查组织访问权限
  if (!orgId) {
    redirect('/select-org');
  }

  return (
    <div>
      <p>Organization Role: {orgRole}</p>
      {children}
    </div>
  );
}

// 带认证检查的服务端操作
// app/actions/posts.ts
'use server';
import { auth } from '@clerk/nextjs/server';

export async function createPost(formData: FormData) {
  const { userId } = await auth();

  if (!userId) {
    throw new Error('Unauthorized');
  }

  const title = formData.get('title') as string;

  // 使用 userId 创建文章
  const post = await prisma.post.create({
    data: {
      title,
      authorId: userId,
    },
  });

  return post;
}

### 反模式

- 模式：不等待 auth() | 原因：auth() 在 App Router 中是异步的 | 修复：使用 await auth() 或 const { userId } = await auth()
- 模式：使用 currentUser() 进行简单检查 | 原因：计入速率限制，比 auth() 慢 | 修复：使用 auth() 检查 userId，使用 currentUser() 获取用户数据

### 参考资料

- https://clerk.com/docs/references/nextjs/auth

### 客户端组件 Hooks

在客户端组件中使用 Hooks 访问认证状态。

核心 Hooks：
- useUser()：用户对象和加载状态
- useAuth()：认证状态、signOut 等
- useSession()：会话对象
- useOrganization()：当前组织

### 代码示例

// components/UserProfile.tsx
'use client';
import { useUser, useAuth } from '@clerk/nextjs';

export function UserProfile() {
  const { user, isLoaded, isSignedIn } = useUser();
  const { signOut } = useAuth();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <div>Not signed in</div>;
  }

  return (
    <div>
      <img src={user.imageUrl} alt={user.fullName ?? ''} />
      <h2>{user.fullName}</h2>
      <p>{user.emailAddresses[0]?.emailAddress}</p>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}

// 组织上下文
'use client';
import { useOrganization, useOrganizationList } from '@clerk/nextjs';

export function OrgSwitcher() {
  const { organization, membership } = useOrganization();
  const { setActive, userMemberships } = useOrganizationList({
    userMemberships: { infinite: true },
  });

  if (!organization) {
    return <p>No organization selected</p>;
  }

  return (
    <div>
      <p>Current: {organization.name}</p>
      <p>Role: {membership?.role}</p>

      <select
        onChange={(e) => setActive?.({ organization: e.target.value })}
        value={organization.id}
      >
        {userMemberships.data?.map((mem) => (
          <option key={mem.organization.id} value={mem.organization.id}>
            {mem.organization.name}
          </option>
        ))}
      </select>
    </div>
  );
}

// 受保护的客户端组件
'use client';
import { useAuth } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function ProtectedContent() {
  const { isLoaded, userId } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && !userId) {
      router.push('/sign-in');
    }
  }, [isLoaded, userId, router]);

  if (!isLoaded || !userId) {
    return <div>Loading...</div>;
  }

  return <div>Protected content here</div>;
}

### 反模式

- 模式：不检查 isLoaded | 原因：水合期间认证状态为 undefined | 修复：访问 user/auth 状态前始终检查 isLoaded
- 模式：在服务端组件中使用 Hooks | 原因：Hooks 只在客户端组件中工作 | 修复：在服务端组件中使用 auth() 和 currentUser()

### 参考资料

- https://clerk.com/docs/references/react/use-user

### 组织与多租户

使用 Clerk 组织实现 B2B 多租户。

功能：
- 每个用户多个组织
- 角色和权限
- 组织范围的数据
- 每个组织的企业 SSO

### 代码示例

// 组织创建 UI
// app/create-org/page.tsx
import { CreateOrganization } from '@clerk/nextjs';

export default function CreateOrgPage() {
  return (
    <div className="flex justify-center">
      <CreateOrganization afterCreateOrganizationUrl="/dashboard" />
    </div>
  );
}

// 组织配置文件和管理
// app/org-settings/page.tsx
import { OrganizationProfile } from '@clerk/nextjs';

export default function OrgSettingsPage() {
  return <OrganizationProfile />;
}

// 头部组织切换器
// components/Header.tsx
import { OrganizationSwitcher, UserButton } from '@clerk/nextjs';

export function Header() {
  return (
    <header className="flex justify-between p-4">
      <OrganizationSwitcher
        hidePersonal
        afterCreateOrganizationUrl="/dashboard"
        afterSelectOrganizationUrl="/dashboard"
      />
      <UserButton />
    </header>
  );
}

// 组织范围的数据访问
// app/dashboard/page.tsx
import { auth } from '@clerk/nextjs/server';
import { prisma } from '@/lib/prisma';

export default async function DashboardPage() {
  const { orgId } = await auth();

  if (!orgId) {
    redirect('/select-org');
  }

  // 获取组织范围的数据
  const projects = await prisma.project.findMany({
    where: { organizationId: orgId },
  });

  return (
    <div>
      <h1>Projects</h1>
      {projects.map((p) => (
        <div key={p.id}>{p.name}</div>
      ))}
    </div>
  );
}

// 基于角色的 UI
'use client';
import { useOrganization, Protect } from '@clerk/nextjs';

export function AdminPanel() {
  const { membership } = useOrganization();

  // 使用 Protect 组件
  return (
    <Protect role="org:admin" fallback={<p>Admin access required</p>}>
      <div>Admin content here</div>
    </Protect>
  );

  // 或手动检查
  if (membership?.role !== 'org:admin') {
    return <p>Admin access required</p>;
  }

  return <div>Admin content here</div>;
}

### 反模式

- 模式：不按 orgId 限定数据范围 | 原因：数据在组织间泄漏 | 修复：始终使用 auth() 返回的 orgId 过滤查询
- 模式：硬编码角色字符串 | 原因：拼写错误导致访问问题 | 修复：定义角色常量或使用 TypeScript 枚举

### 参考资料

- https://clerk.com/docs/guides/organizations
- https://clerk.com/articles/multi-tenancy-in-react-applications-guide

### Webhook 用户同步

使用 Webhook 将 Clerk 用户同步到数据库。

核心 Webhook：
- user.created：新用户注册
- user.updated：用户配置文件更改
- user.deleted：用户删除账户

使用 svix 进行签名验证。

### 代码示例

// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';
import { WebhookEvent } from '@clerk/nextjs/server';
import { prisma } from '@/lib/prisma';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    throw new Error('Missing CLERK_WEBHOOK_SECRET');
  }

  // 获取请求头
  const headerPayload = await headers();
  const svix_id = headerPayload.get('svix-id');
  const svix_timestamp = headerPayload.get('svix-timestamp');
  const svix_signature = headerPayload.get('svix-signature');

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing svix headers', { status: 400 });
  }

  // 获取请求体
  const payload = await req.json();
  const body = JSON.stringify(payload);

  // 验证 Webhook
  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    console.error('Webhook verification failed:', err);
    return new Response('Verification failed', { status: 400 });
  }

  // 处理事件
  const eventType = evt.type;

  if (eventType === 'user.created') {
    const { id, email_addresses, first_name, last_name, image_url } = evt.data;

    await prisma.user.create({
      data: {
        clerkId: id,
        email: email_addresses[0]?.email_address,
        firstName: first_name,
        lastName: last_name,
        imageUrl: image_url,
      },
    });
  }

  if (eventType === 'user.updated') {
    const { id, email_addresses, first_name, last_name, image_url } = evt.data;

    await prisma.user.update({
      where: { clerkId: id },
      data: {
        email: email_addresses[0]?.email_address,
        firstName: first_name,
        lastName: last_name,
        imageUrl: image_url,
      },
    });
  }

  if (eventType === 'user.deleted') {
    const { id } = evt.data;

    await prisma.user.delete({
      where: { clerkId: id! },
    });
  }

  return new Response('Webhook processed', { status: 200 });
}

// Prisma schema
// prisma/schema.prisma
model User {
  id        String   @id @default(cuid())
  clerkId   String   @unique
  email     String   @unique
  firstName String?
  lastName  String?
  imageUrl  String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts     Post[]
  @@index([clerkId])
}

### 反模式

- 模式：不验证 Webhook 签名 | 原因：任何人都可以用假数据访问你的端点 | 修复：始终使用 svix 验证
- 模式：中间件阻止 Webhook 路由 | 原因：Webhook 来自 Clerk，而非已认证用户 | 修复：将 `/api/webhooks(.*)` 添加到公开路由
- 模式：不处理竞态条件 | 原因：user.created 可能在 user.updated 之后到达 | 修复：使用 upsert 而非 create，处理缺失记录

### 参考资料

- https://clerk.com/docs/webhooks/sync-data
- https://clerk.com/articles/how-to-sync-clerk-user-data-to-your-database

### API 路由保护

使用 Clerk 的 auth() 保护 API 路由。

App Router 中的路由处理器使用 auth() 进行认证。中间件提供初始保护，auth() 提供处理器内验证。

### 代码示例

// app/api/projects/route.ts
import { auth } from '@clerk/nextjs/server';
import { prisma } from '@/lib/prisma';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId, orgId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 用户的个人项目或组织项目
  const projects = await prisma.project.findMany({
    where: orgId
      ? { organizationId: orgId }
      : { userId, organizationId: null },
  });

  return NextResponse.json(projects);
}

export async function POST(req: Request) {
  const { userId, orgId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await req.json();

  const project = await prisma.project.create({
    data: {
      name: body.name,
      userId,
      organizationId: orgId ?? null,
    },
  });

  return NextResponse.json(project, { status: 201 });
}

// 带角色检查的保护
// app/api/admin/users/route.ts
export async function GET() {
  const { userId, orgRole } = await auth();

  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (orgRole !== 'org:admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  // 仅管理员逻辑
  const users = await prisma.user.findMany();
  return NextResponse.json(users);
}

// 在旧模式中使用 getAuth（不推荐）
// 仅用于向后兼容
import { getAuth } from '@clerk/nextjs/server';

export async function GET(req: Request) {
  const { userId } = getAuth(req);
  // ...
}

### 反模式

- 模式：仅信任中间件 | 原因：中间件可能被绕过（CVE-2025-29927）| 修复：始终在路由处理器中也验证认证
- 模式：不检查多租户的 orgId | 原因：用户可能访问其他组织的数据 | 修复：始终使用 auth() 返回的 orgId 过滤

### 参考资料

- https://clerk.com/docs/guides/protecting-pages

## 关键风险

### CVE-2025-29927 中间件绕过漏洞

严重程度：严重

### 多个中间件文件导致冲突

严重程度：高

### 4KB 会话令牌 Cookie 限制

严重程度：高

### auth() 需要 clerkMiddleware 配置

严重程度：高

### Webhook 竞态条件

严重程度：中

### auth() 在 App Router 中是异步的

严重程度：中

### 中间件阻止 Webhook 端点

严重程度：中

### 在 isLoaded 之前访问认证状态

严重程度：中

### 手动重定向导致双重重定向

严重程度：中

### 组织数据未按 orgId 限定范围

严重程度：高

## 验证检查

### 客户端代码中的 Clerk 密钥

严重程度：错误

CLERK_SECRET_KEY 必须仅在服务端使用

消息：Clerk 密钥暴露给客户端。使用不带 NEXT_PUBLIC 前缀的 CLERK_SECRET_KEY。

### 无中间件保护的受保护路由

严重程度：错误

API 路由应有中间件保护

消息：API 路由无认证检查。添加中间件保护或 auth() 检查。

### 硬编码的 Clerk API 密钥

严重程度：错误

Clerk 密钥应使用环境变量

消息：硬编码的 Clerk 密钥。使用环境变量。

### auth() 缺少 await

严重程度：错误

auth() 在 App Router 中是异步的，必须被等待

消息：auth() 未被等待。在 App Router 中使用 'await auth()'。

### 多个中间件文件

严重程度：警告

只应存在一个 middleware.ts 文件

消息：检测到多个中间件文件。使用单一 middleware.ts。

### Webhook 路由未排除保护

严重程度：警告

Webhook 路由应为公开

消息：Webhook 路由可能被中间件阻止。添加到公开路由。

### 无 isLoaded 检查访问认证状态

严重程度：警告

在客户端组件中访问用户状态前检查 isLoaded

消息：无 isLoaded 检查访问用户。先检查 isLoaded。

### 服务端组件中的 Clerk Hooks

严重程度：错误

Clerk Hooks 仅在客户端组件中工作

消息：服务端组件中的 Clerk Hooks。添加 'use client' 或使用 auth()。

### 无 orgId 的多租户查询

严重程度：警告

组织数据应按 orgId 限定范围

消息：无组织范围的查询。按 orgId 过滤以实现多租户。

### 无签名验证的 Webhook

严重程度：错误

Clerk Webhook 必须验证 svix 签名

消息：无签名验证的 Webhook。使用 svix 验证。

## 协作

### 委托触发器

- 用户需要数据库 -> postgres-wizard（带 clerkId 的 User 表）
- 用户需要支付 -> stripe-integration（关联到 Clerk 用户的客户）
- 用户需要搜索 -> algolia-search（每用户安全 API 密钥）
- 用户需要分析 -> segment-cdp（用户识别）
- 用户需要邮件 -> resend-email（事务性邮件）

## 使用时机
- 用户提到或暗示：添加认证
- 用户提到或暗示：clerk auth
- 用户提到或暗示：用户认证
- 用户提到或暗示：登录
- 用户提到或暗示：注册
- 用户提到或暗示：用户管理
- 用户提到或暗示：多租户
- 用户提到或暗示：组织
- 用户提到或暗示：sso
- 用户提到或暗示：单点登录

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
