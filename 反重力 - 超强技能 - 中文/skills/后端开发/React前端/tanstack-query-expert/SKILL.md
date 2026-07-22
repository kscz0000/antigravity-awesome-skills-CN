---
name: tanstack-query-expert
description: "TanStack Query（React Query）异步状态管理专家。涵盖数据请求、过期时间配置、变更操作、乐观更新及 Next.js App Router（SSR）集成。触发词：TanStack Query、React Query、数据请求、缓存管理、乐观更新、useQuery、useMutation、SSR水合"
risk: safe
source: community
date_added: "2026-03-07"
---

# TanStack Query 专家

你是一名生产级 TanStack Query（前身为 React Query）专家。你帮助开发者在 React 和 Next.js 应用中构建健壮、高性能的异步状态管理层。你精通声明式数据请求、缓存失效、乐观 UI 更新、后台同步、错误边界和 SSR 水合模式。

## 适用场景

- 搭建或重构数据请求逻辑时（替代 `useEffect` + `useState`）
- 设计 query key 时（基于数组的严格类型 key）
- 配置全局或查询级别的 `staleTime`、`gcTime` 和 `retry` 行为时
- 编写 `useMutation` hook 处理 POST/PUT/DELETE 请求时
- 变更操作后使缓存失效（`queryClient.invalidateQueries`）时
- 实现乐观更新以提供即时 UX 反馈时
- 将 TanStack Query 集成到 Next.js App Router（Server Components + Client Boundary 水合）时

## 核心概念

### 为什么选择 TanStack Query？

TanStack Query 不仅仅是请求数据的工具，它是一个**异步状态管理器**。它处理缓存、后台更新、相同数据的多个请求去重、分页，以及开箱即用的 loading/error 状态。

**经验法则：** 如果项目中已集成 TanStack Query，就不要再用 `useEffect` 请求数据。

## 查询定义模式

### 自定义 Hook 模式（最佳实践）

始终将 `useQuery` 调用抽象为自定义 hook，封装请求逻辑、TypeScript 类型和 query key。

```typescript
import { useQuery } from '@tanstack/react-query';

// 1. Define strict types
type User = { id: string; name: string; status: 'active' | 'inactive' };

// 2. Define the fetcher function
const fetchUser = async (userId: string): Promise<User> => {
  const res = await fetch(`/api/users/${userId}`);
  if (!res.ok) throw new Error('Failed to fetch user');
  return res.json();
};

// 3. Export a custom hook
export const useUser = (userId: string) => {
  return useQuery({
    queryKey: ['users', userId], // Array-based query key
    queryFn: () => fetchUser(userId),
    staleTime: 1000 * 60 * 5, // Data is fresh for 5 minutes (no background refetching)
    enabled: !!userId, // Dependent query: only run if userId exists
  });
};
```

### 高级 Query Key

Query key 唯一标识缓存。它必须是数组，且顺序很重要。

```typescript
// Filtering / Sorting
useQuery({
  queryKey: ['issues', { status: 'open', sort: 'desc' }],
  queryFn: () => fetchIssues({ status: 'open', sort: 'desc' })
});

// Factory pattern for query keys (Highly recommended for large apps)
export const issueKeys = {
  all: ['issues'] as const,
  lists: () => [...issueKeys.all, 'list'] as const,
  list: (filters: string) => [...issueKeys.lists(), { filters }] as const,
  details: () => [...issueKeys.all, 'detail'] as const,
  detail: (id: number) => [...issueKeys.details(), id] as const,
};
```

## 变更操作与缓存失效

### 基本变更与缓存失效

在服务端修改数据后，必须通知客户端缓存旧数据已过期。

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export const useCreatePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (newPost: { title: string }) => {
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost),
      });
      return res.json();
    },
    // On success, invalidate the 'posts' cache to trigger a background refetch
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
};
```

### 乐观更新

在服务端响应*之前*更新缓存，让用户获得即时反馈；若请求失败则回滚。

```typescript
export const useUpdateTodo = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodoFn,
    
    // 1. Triggered immediately when mutate() is called
    onMutate: async (newTodo) => {
      // Cancel any outgoing refetches so they don't overwrite our optimistic update
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot the previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update to the new value
      queryClient.setQueryData(['todos'], (old: any) => 
        old.map((todo: any) => todo.id === newTodo.id ? { ...todo, ...newTodo } : todo)
      );

      // Return a context object with the snapshotted value
      return { previousTodos };
    },
    
    // 2. If the mutation fails, use the context returned from onMutate to roll back
    onError: (err, newTodo, context) => {
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    
    // 3. Always refetch after error or success to ensure server sync
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
};
```

## Next.js App Router 集成

### 初始化 Provider

```typescript
// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            refetchOnWindowFocus: false, // Prevents aggressive refetching on tab switch
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### 服务端组件预取（水合）

在服务端预取数据并传递给客户端，无需 prop drilling 或 `initialData`。

```typescript
// app/posts/page.tsx (Server Component)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import PostsList from './PostsList'; // Client Component

export default async function PostsPage() {
  const queryClient = new QueryClient();

  // Prefetch the data on the server
  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: fetchPostsServerSide,
  });

  // Dehydrate the cache and pass it to the HydrationBoundary
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostsList />
    </HydrationBoundary>
  );
}
```

```typescript
// app/posts/PostsList.tsx (Client Component)
'use client'
import { useQuery } from '@tanstack/react-query';

export default function PostsList() {
  // This will NOT trigger a network request on mount! 
  // It reads instantly from the dehydrated server cache.
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPostsClientSide,
  });

  return <div>{data.map(post => <p key={post.id}>{post.title}</p>)}</div>;
}
```

## 最佳实践

- ✅ **推荐：** 创建 Query Key 工厂，避免在不同文件中拼错 `['users']` 和 `['user']`。
- ✅ **推荐：** 如果数据不是每秒都在变化，设置全局 `staleTime`（如 `1000 * 60`）。默认 `staleTime` 为 `0`，意味着 TanStack Query 会在每次组件重新挂载时触发后台重新请求。
- ✅ **推荐：** 谨慎使用 `queryClient.setQueryData`。通常更好的做法是直接 `invalidateQueries`，让 TanStack Query 自然地重新请求最新数据。
- ✅ **推荐：** 将所有 `useMutation` 和 `useQuery` 调用抽象为自定义 hook。视图层只需 `const { mutate } = useCreatePost()`。
- ❌ **禁止：** 在依赖闭包的情况下，将原始回调直接内联传给 `useQuery` 而不做 memoization。（应依赖 `queryKey` 依赖数组。）
- ❌ **禁止：** 将查询数据同步到本地 React state（如 `useEffect(() => setLocalState(data), [data])`）。直接使用查询数据即可。如需派生状态，在渲染期间派生。

## 故障排除

**问题：** 网络面板中出现无限请求循环。
**解决方案：** 检查你的 `queryFn`。如果 `fetch` 逻辑结构不正确，或在 return 之前抛出未处理的异常，TanStack Query 默认会自动重试最多 3 次。如果包裹在不稳定的 `useEffect` 中，会导致无限循环。调试时可设置 `retry: false`。

**问题：** `staleTime` 和 `gcTime`（原 `cacheTime`）混淆。
**解决方案：** `staleTime` 控制何时触发后台重新请求。`gcTime` 控制组件卸载后非活跃数据在内存中保留多久。如果 `gcTime` < `staleTime`，数据会在过期之前就被删除！

## 限制

- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如缺少必要的输入、权限、安全边界或成功标准，应停止并请求澄清。
