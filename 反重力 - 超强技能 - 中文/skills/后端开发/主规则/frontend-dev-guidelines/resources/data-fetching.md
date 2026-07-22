# 数据获取模式

使用 TanStack Query 结合 Suspense 边界、缓存优先策略和集中式 API 服务的现代数据获取方案。

---

## 主要模式：useSuspenseQuery

### 为什么使用 useSuspenseQuery？

对于**所有新组件**，应使用 `useSuspenseQuery` 替代普通的 `useQuery`：

**优势：**
- 无需 `isLoading` 检查
- 与 Suspense 边界集成
- 更简洁的组件代码
- 一致的加载体验
- 通过 Error Boundary 实现更好的错误处理

### 基本模式

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { myFeatureApi } from '../api/myFeatureApi';

export const MyComponent: React.FC<Props> = ({ id }) => {
    // No isLoading - Suspense handles it!
    const { data } = useSuspenseQuery({
        queryKey: ['myEntity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    // data is ALWAYS defined here (not undefined | Data)
    return <div>{data.name}</div>;
};

// Wrap in Suspense boundary
<SuspenseLoader>
    <MyComponent id={123} />
</SuspenseLoader>
```

### useSuspenseQuery 与 useQuery 对比

| 特性 | useSuspenseQuery | useQuery |
|---------|------------------|----------|
| 加载状态 | 由 Suspense 处理 | 手动 `isLoading` 检查 |
| 数据类型 | 始终有定义 | `Data \| undefined` |
| 配合使用 | Suspense 边界 | 传统组件 |
| 推荐用于 | **新组件** | 仅限遗留代码 |
| 错误处理 | Error Boundary | 手动错误状态 |

**何时使用普通 useQuery：**
- 维护遗留代码
- 不需要 Suspense 的简单场景
- 带后台更新的轮询

**对于新组件：始终优先使用 useSuspenseQuery**

---

## 缓存优先策略

### 缓存优先模式示例

**智能缓存**通过先检查 React Query 缓存来减少 API 调用：

```typescript
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';

export function useSuspensePost(postId: number) {
    const queryClient = useQueryClient();

    return useSuspenseQuery({
        queryKey: ['post', postId],
        queryFn: async () => {
            // Strategy 1: Try to get from list cache first
            const cachedListData = queryClient.getQueryData<{ posts: Post[] }>([
                'posts',
                'list'
            ]);

            if (cachedListData?.posts) {
                const cachedPost = cachedListData.posts.find(
                    (post) => post.id === postId
                );

                if (cachedPost) {
                    return cachedPost;  // Return from cache!
                }
            }

            // Strategy 2: Not in cache, fetch from API
            return postApi.getPost(postId);
        },
        staleTime: 5 * 60 * 1000,      // Consider fresh for 5 minutes
        gcTime: 10 * 60 * 1000,         // Keep in cache for 10 minutes
        refetchOnWindowFocus: false,    // Don't refetch on focus
    });
}
```

**关键要点：**
- 在 API 调用前先检查 grid/list 缓存
- 避免冗余请求
- `staleTime`：数据被视为新鲜的时长
- `gcTime`：未使用数据在缓存中保留的时长
- `refetchOnWindowFocus: false`：用户偏好设置

---

## 并行数据获取

### useSuspenseQueries

当需要获取多个独立资源时：

```typescript
import { useSuspenseQueries } from '@tanstack/react-query';

export const MyComponent: React.FC = () => {
    const [userQuery, settingsQuery, preferencesQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['user'],
                queryFn: () => userApi.getCurrentUser(),
            },
            {
                queryKey: ['settings'],
                queryFn: () => settingsApi.getSettings(),
            },
            {
                queryKey: ['preferences'],
                queryFn: () => preferencesApi.getPreferences(),
            },
        ],
    });

    // All data available, Suspense handles loading
    const user = userQuery.data;
    const settings = settingsQuery.data;
    const preferences = preferencesQuery.data;

    return <Display user={user} settings={settings} prefs={preferences} />;
};
```

**优势：**
- 所有查询并行执行
- 单个 Suspense 边界
- 类型安全的结果

---

## Query Key 组织

### 命名约定

```typescript
// Entity list
['entities', blogId]
['entities', blogId, 'summary']    // With view mode
['entities', blogId, 'flat']

// Single entity
['entity', blogId, entityId]

// Related data
['entity', entityId, 'history']
['entity', entityId, 'comments']

// User-specific
['user', userId, 'profile']
['user', userId, 'permissions']
```

**规则：**
- 以实体名称开头（列表用复数，单个用单数）
- 包含 ID 以提高精确性
- 在末尾添加视图模式/关联关系
- 在整个应用中保持一致

### Query Key 示例

```typescript
// From useSuspensePost.ts
queryKey: ['post', blogId, postId]
queryKey: ['posts-v2', blogId, 'summary']

// Invalidation patterns
queryClient.invalidateQueries({ queryKey: ['post', blogId] });  // All posts for form
queryClient.invalidateQueries({ queryKey: ['post'] });          // All posts
```

---

## API 服务层模式

### 文件结构

为每个功能模块创建集中式 API 服务：

```
features/
  my-feature/
    api/
      myFeatureApi.ts    # Service layer
```

### 服务模式（来自 postApi.ts）

```typescript
/**
 * Centralized API service for my-feature operations
 * Uses apiClient for consistent error handling
 */
import apiClient from '@/lib/apiClient';
import type { MyEntity, UpdatePayload } from '../types';

export const myFeatureApi = {
    /**
     * Fetch a single entity
     */
    getEntity: async (blogId: number, entityId: number): Promise<MyEntity> => {
        const { data } = await apiClient.get(
            `/blog/entities/${blogId}/${entityId}`
        );
        return data;
    },

    /**
     * Fetch all entities for a form
     */
    getEntities: async (blogId: number, view: 'summary' | 'flat'): Promise<MyEntity[]> => {
        const { data } = await apiClient.get(
            `/blog/entities/${blogId}`,
            { params: { view } }
        );
        return data.rows;
    },

    /**
     * Update entity
     */
    updateEntity: async (
        blogId: number,
        entityId: number,
        payload: UpdatePayload
    ): Promise<MyEntity> => {
        const { data } = await apiClient.put(
            `/blog/entities/${blogId}/${entityId}`,
            payload
        );
        return data;
    },

    /**
     * Delete entity
     */
    deleteEntity: async (blogId: number, entityId: number): Promise<void> => {
        await apiClient.delete(`/blog/entities/${blogId}/${entityId}`);
    },
};
```

**关键要点：**
- 导出包含方法的单一对象
- 使用 `apiClient`（来自 `@/lib/apiClient` 的 axios 实例）
- 类型安全的参数和返回值
- 每个方法添加 JSDoc 注释
- 集中式错误处理（由 apiClient 处理）

---

## 路由格式规则（重要）

### 正确格式

```typescript
// ✅ CORRECT - Direct service path
await apiClient.get('/blog/posts/123');
await apiClient.post('/projects/create', data);
await apiClient.put('/users/update/456', updates);
await apiClient.get('/email/templates');

// ❌ WRONG - Do NOT add /api/ prefix
await apiClient.get('/api/blog/posts/123');  // WRONG!
await apiClient.post('/api/projects/create', data); // WRONG!
```

**微服务路由：**
- 表单服务：`/blog/*`
- 项目服务：`/projects/*`
- 邮件服务：`/email/*`
- 用户服务：`/users/*`

**原因：** API 路由由代理配置处理，不需要 `/api/` 前缀。

---

## 变更操作

### 基本变更模式

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { myFeatureApi } from '../api/myFeatureApi';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const MyComponent: React.FC = () => {
    const queryClient = useQueryClient();
    const { showSuccess, showError } = useMuiSnackbar();

    const updateMutation = useMutation({
        mutationFn: (payload: UpdatePayload) =>
            myFeatureApi.updateEntity(blogId, entityId, payload),

        onSuccess: () => {
            // Invalidate and refetch
            queryClient.invalidateQueries({
                queryKey: ['entity', blogId, entityId]
            });
            showSuccess('Entity updated successfully');
        },

        onError: (error) => {
            showError('Failed to update entity');
            console.error('Update error:', error);
        },
    });

    const handleUpdate = () => {
        updateMutation.mutate({ name: 'New Name' });
    };

    return (
        <Button
            onClick={handleUpdate}
            disabled={updateMutation.isPending}
        >
            {updateMutation.isPending ? 'Updating...' : 'Update'}
        </Button>
    );
};
```

### 乐观更新

```typescript
const updateMutation = useMutation({
    mutationFn: (payload) => myFeatureApi.update(id, payload),

    // Optimistic update
    onMutate: async (newData) => {
        // Cancel outgoing refetches
        await queryClient.cancelQueries({ queryKey: ['entity', id] });

        // Snapshot current value
        const previousData = queryClient.getQueryData(['entity', id]);

        // Optimistically update
        queryClient.setQueryData(['entity', id], (old) => ({
            ...old,
            ...newData,
        }));

        // Return rollback function
        return { previousData };
    },

    // Rollback on error
    onError: (err, newData, context) => {
        queryClient.setQueryData(['entity', id], context.previousData);
        showError('Update failed');
    },

    // Refetch after success or error
    onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ['entity', id] });
    },
});
```

---

## 高级查询模式

### 预获取

```typescript
export function usePrefetchEntity() {
    const queryClient = useQueryClient();

    return (blogId: number, entityId: number) => {
        return queryClient.prefetchQuery({
            queryKey: ['entity', blogId, entityId],
            queryFn: () => myFeatureApi.getEntity(blogId, entityId),
            staleTime: 5 * 60 * 1000,
        });
    };
}

// Usage: Prefetch on hover
<div onMouseEnter={() => prefetch(blogId, id)}>
    <Link to={`/entity/${id}`}>View</Link>
</div>
```

### 不发起请求的缓存访问

```typescript
export function useEntityFromCache(blogId: number, entityId: number) {
    const queryClient = useQueryClient();

    // Get from cache, don't fetch if missing
    const directCache = queryClient.getQueryData<MyEntity>(['entity', blogId, entityId]);

    if (directCache) return directCache;

    // Try grid cache
    const gridCache = queryClient.getQueryData<{ rows: MyEntity[] }>(['entities-v2', blogId]);

    return gridCache?.rows.find(row => row.id === entityId);
}
```

### 依赖查询

```typescript
// Fetch user first, then user's settings
const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => userApi.getUser(userId),
});

const { data: settings } = useSuspenseQuery({
    queryKey: ['user', userId, 'settings'],
    queryFn: () => settingsApi.getUserSettings(user.id),
    // Automatically waits for user to load due to Suspense
});
```

---

## API Client 配置

### 使用 apiClient

```typescript
import apiClient from '@/lib/apiClient';

// apiClient is a configured axios instance
// Automatically includes:
// - Base URL configuration
// - Cookie-based authentication
// - Error interceptors
// - Response transformers
```

**不要创建新的 axios 实例** - 使用 apiClient 以保持一致性。

---

## 查询中的错误处理

### onError 回调

```typescript
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

const { showError } = useMuiSnackbar();

const { data } = useSuspenseQuery({
    queryKey: ['entity', id],
    queryFn: () => myFeatureApi.getEntity(id),

    // Handle errors
    onError: (error) => {
        showError('Failed to load entity');
        console.error('Load error:', error);
    },
});
```

### Error Boundary

结合 Error Boundary 实现全面的错误处理：

```typescript
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary
    fallback={<ErrorDisplay />}
    onError={(error) => console.error(error)}
>
    <SuspenseLoader>
        <ComponentWithSuspenseQuery />
    </SuspenseLoader>
</ErrorBoundary>
```

---

## 完整示例

### 示例 1：简单实体获取

```typescript
import React from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Box, Typography } from '@mui/material';
import { userApi } from '../api/userApi';

interface UserProfileProps {
    userId: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
    const { data: user } = useSuspenseQuery({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
    });

    return (
        <Box>
            <Typography variant='h5'>{user.name}</Typography>
            <Typography>{user.email}</Typography>
        </Box>
    );
};

// Usage with Suspense
<SuspenseLoader>
    <UserProfile userId='123' />
</SuspenseLoader>
```

### 示例 2：缓存优先策略

```typescript
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';
import type { Post } from '../types';

/**
 * Hook with cache-first strategy
 * Checks grid cache before API call
 */
export function useSuspensePost(blogId: number, postId: number) {
    const queryClient = useQueryClient();

    return useSuspenseQuery<Post, Error>({
        queryKey: ['post', blogId, postId],
        queryFn: async () => {
            // 1. Check grid cache first
            const gridCache = queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                blogId,
                'summary'
            ]) || queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                blogId,
                'flat'
            ]);

            if (gridCache?.rows) {
                const cached = gridCache.rows.find(row => row.S_ID === postId);
                if (cached) {
                    return cached;  // Reuse grid data
                }
            }

            // 2. Not in cache, fetch directly
            return postApi.getPost(blogId, postId);
        },
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
        refetchOnWindowFocus: false,
    });
}
```

**优势：**
- 避免重复 API 调用
- 已加载的数据可即时显示
- 未缓存时回退到 API 请求

### 示例 3：并行获取

```typescript
import { useSuspenseQueries } from '@tanstack/react-query';

export const Dashboard: React.FC = () => {
    const [statsQuery, projectsQuery, notificationsQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['stats'],
                queryFn: () => statsApi.getStats(),
            },
            {
                queryKey: ['projects', 'active'],
                queryFn: () => projectsApi.getActiveProjects(),
            },
            {
                queryKey: ['notifications', 'unread'],
                queryFn: () => notificationsApi.getUnread(),
            },
        ],
    });

    return (
        <Box>
            <StatsCard data={statsQuery.data} />
            <ProjectsList projects={projectsQuery.data} />
            <Notifications items={notificationsQuery.data} />
        </Box>
    );
};
```

---

## 带缓存失效的变更操作

### 更新变更

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const useUpdatePost = () => {
    const queryClient = useQueryClient();
    const { showSuccess, showError } = useMuiSnackbar();

    return useMutation({
        mutationFn: ({ blogId, postId, data }: UpdateParams) =>
            postApi.updatePost(blogId, postId, data),

        onSuccess: (data, variables) => {
            // Invalidate specific post
            queryClient.invalidateQueries({
                queryKey: ['post', variables.blogId, variables.postId]
            });

            // Invalidate list to refresh grid
            queryClient.invalidateQueries({
                queryKey: ['posts-v2', variables.blogId]
            });

            showSuccess('Post updated');
        },

        onError: (error) => {
            showError('Failed to update post');
            console.error('Update error:', error);
        },
    });
};

// Usage
const updatePost = useUpdatePost();

const handleSave = () => {
    updatePost.mutate({
        blogId: 123,
        postId: 456,
        data: { responses: { '101': 'value' } }
    });
};
```

### 删除变更

```typescript
export const useDeletePost = () => {
    const queryClient = useQueryClient();
    const { showSuccess, showError } = useMuiSnackbar();

    return useMutation({
        mutationFn: ({ blogId, postId }: DeleteParams) =>
            postApi.deletePost(blogId, postId),

        onSuccess: (data, variables) => {
            // Remove from cache manually (optimistic)
            queryClient.setQueryData<{ rows: Post[] }>(
                ['posts-v2', variables.blogId],
                (old) => ({
                    ...old,
                    rows: old?.rows.filter(row => row.S_ID !== variables.postId) || []
                })
            );

            showSuccess('Post deleted');
        },

        onError: (error, variables) => {
            // Rollback - refetch to get accurate state
            queryClient.invalidateQueries({
                queryKey: ['posts-v2', variables.blogId]
            });
            showError('Failed to delete post');
        },
    });
};
```

---

## 查询配置最佳实践

### 默认配置

```typescript
// In QueryClientProvider setup
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 1000 * 60 * 5,        // 5 minutes
            gcTime: 1000 * 60 * 10,           // 10 minutes (was cacheTime)
            refetchOnWindowFocus: false,       // Don't refetch on focus
            refetchOnMount: false,             // Don't refetch on mount if fresh
            retry: 1,                          // Retry failed queries once
        },
    },
});
```

### 单查询覆盖

```typescript
// Frequently changing data - shorter staleTime
useSuspenseQuery({
    queryKey: ['notifications', 'unread'],
    queryFn: () => notificationApi.getUnread(),
    staleTime: 30 * 1000,  // 30 seconds
});

// Rarely changing data - longer staleTime
useSuspenseQuery({
    queryKey: ['form', blogId, 'structure'],
    queryFn: () => formApi.getStructure(blogId),
    staleTime: 30 * 60 * 1000,  // 30 minutes
});
```

---

## 总结

**现代数据获取方案：**

1. **创建 API 服务**：`features/X/api/XApi.ts`，使用 apiClient
2. **使用 useSuspenseQuery**：在 SuspenseLoader 包裹的组件中使用
3. **缓存优先**：在 API 调用前先检查 grid 缓存
4. **Query Key**：一致的命名规则 ['entity', id]
5. **路由格式**：`/blog/route` 而非 `/api/blog/route`
6. **变更操作**：成功后调用 invalidateQueries
7. **错误处理**：onError + useMuiSnackbar
8. **类型安全**：为所有参数和返回值添加类型

**另请参阅：**
- [component-patterns.md](component-patterns.md) - Suspense 集成
- [loading-and-error-states.md](loading-and-error-states.md) - SuspenseLoader 用法
- [complete-examples.md](complete-examples.md) - 完整工作示例
