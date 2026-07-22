# 路由指南

TanStack Router 实现，包含基于文件夹的路由和懒加载模式。

---

## TanStack Router 概述

**TanStack Router** 使用基于文件的路由：
- 文件夹结构定义路由
- 懒加载实现代码分割
- 类型安全的路由
- 面包屑加载器

---

## 基于文件夹的路由

### 目录结构

```
routes/
  __root.tsx                    # Root layout
  index.tsx                     # Home route (/)
  posts/
    index.tsx                   # /posts
    create/
      index.tsx                 # /posts/create
    $postId.tsx                 # /posts/:postId (dynamic)
  comments/
    index.tsx                   # /comments
```

**模式**：
- `index.tsx` = 该路径的路由
- `$param.tsx` = 动态参数
- 嵌套文件夹 = 嵌套路由

---

## 基本路由模式

### 示例：posts/index.tsx

```typescript
/**
 * Posts route component
 * Displays the main blog posts list
 */

import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

// Lazy load the page component
const PostsList = lazy(() =>
    import('@/features/posts/components/PostsList').then(
        (module) => ({ default: module.PostsList }),
    ),
);

export const Route = createFileRoute('/posts/')({
    component: PostsPage,
    // Define breadcrumb data
    loader: () => ({
        crumb: 'Posts',
    }),
});

function PostsPage() {
    return (
        <PostsList
            title='All Posts'
            showFilters={true}
        />
    );
}

export default PostsPage;
```

**关键点：**
- 懒加载重型组件
- `createFileRoute` 配合路由路径
- `loader` 用于面包屑数据
- 页面组件渲染内容
- 同时导出 Route 和组件

---

## 懒加载路由

### 命名导出模式

```typescript
import { lazy } from 'react';

// For named exports, use .then() to map to default
const MyPage = lazy(() =>
    import('@/features/my-feature/components/MyPage').then(
        (module) => ({ default: module.MyPage })
    )
);
```

### 默认导出模式

```typescript
import { lazy } from 'react';

// For default exports, simpler syntax
const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));
```

### 为什么使用懒加载路由？

- 代码分割 - 更小的初始包体积
- 更快的初始页面加载
- 仅在导航到路由时加载路由代码
- 更好的性能

---

## createFileRoute

### 基本配置

```typescript
export const Route = createFileRoute('/my-route/')({
    component: MyRoutePage,
});

function MyRoutePage() {
    return <div>My Route Content</div>;
}
```

### 带面包屑加载器

```typescript
export const Route = createFileRoute('/my-route/')({
    component: MyRoutePage,
    loader: () => ({
        crumb: 'My Route Title',
    }),
});
```

面包屑会自动显示在导航栏/应用栏中。

### 带数据加载器

```typescript
export const Route = createFileRoute('/my-route/')({
    component: MyRoutePage,
    loader: async () => {
        // Can prefetch data here
        const data = await api.getData();
        return { crumb: 'My Route', data };
    },
});
```

### 带搜索参数

```typescript
export const Route = createFileRoute('/search/')({
    component: SearchPage,
    validateSearch: (search: Record<string, unknown>) => {
        return {
            query: (search.query as string) || '',
            page: Number(search.page) || 1,
        };
    },
});

function SearchPage() {
    const { query, page } = Route.useSearch();
    // Use query and page
}
```

---

## 动态路由

### 参数路由

```typescript
// routes/users/$userId.tsx

export const Route = createFileRoute('/users/$userId')({
    component: UserPage,
});

function UserPage() {
    const { userId } = Route.useParams();

    return <UserProfile userId={userId} />;
}
```

### 多个参数

```typescript
// routes/posts/$postId/comments/$commentId.tsx

export const Route = createFileRoute('/posts/$postId/comments/$commentId')({
    component: CommentPage,
});

function CommentPage() {
    const { postId, commentId } = Route.useParams();

    return <CommentEditor postId={postId} commentId={commentId} />;
}
```

---

## 导航

### 编程式导航

```typescript
import { useNavigate } from '@tanstack/react-router';

export const MyComponent: React.FC = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate({ to: '/posts' });
    };

    return <Button onClick={handleClick}>View Posts</Button>;
};
```

### 带参数

```typescript
const handleNavigate = () => {
    navigate({
        to: '/users/$userId',
        params: { userId: '123' },
    });
};
```

### 带搜索参数

```typescript
const handleSearch = () => {
    navigate({
        to: '/search',
        search: { query: 'test', page: 1 },
    });
};
```

---

## 路由布局模式

### 根布局 (__root.tsx)

```typescript
import { createRootRoute, Outlet } from '@tanstack/react-router';
import { Box } from '@mui/material';
import { CustomAppBar } from '~components/CustomAppBar';

export const Route = createRootRoute({
    component: RootLayout,
});

function RootLayout() {
    return (
        <Box>
            <CustomAppBar />
            <Box sx={{ p: 2 }}>
                <Outlet />  {/* Child routes render here */}
            </Box>
        </Box>
    );
}
```

### 嵌套布局

```typescript
// routes/dashboard/index.tsx
export const Route = createFileRoute('/dashboard/')({
    component: DashboardLayout,
});

function DashboardLayout() {
    return (
        <Box>
            <DashboardSidebar />
            <Box sx={{ flex: 1 }}>
                <Outlet />  {/* Nested routes */}
            </Box>
        </Box>
    );
}
```

---

## 完整路由示例

```typescript
/**
 * User profile route
 * Path: /users/:userId
 */

import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';
import { SuspenseLoader } from '~components/SuspenseLoader';

// Lazy load heavy component
const UserProfile = lazy(() =>
    import('@/features/users/components/UserProfile').then(
        (module) => ({ default: module.UserProfile })
    )
);

export const Route = createFileRoute('/users/$userId')({
    component: UserPage,
    loader: () => ({
        crumb: 'User Profile',
    }),
});

function UserPage() {
    const { userId } = Route.useParams();

    return (
        <SuspenseLoader>
            <UserProfile userId={userId} />
        </SuspenseLoader>
    );
}

export default UserPage;
```

---

## 总结

**路由检查清单：**
- ✅ 基于文件夹：`routes/my-route/index.tsx`
- ✅ 懒加载组件：`React.lazy(() => import())`
- ✅ 使用 `createFileRoute` 配合路由路径
- ✅ 在 `loader` 函数中添加面包屑
- ✅ 使用 `SuspenseLoader` 处理加载状态
- ✅ 使用 `Route.useParams()` 获取动态参数
- ✅ 使用 `useNavigate()` 进行编程式导航

**另请参阅：**
- [component-patterns.md](component-patterns.md) - 懒加载模式
- [loading-and-error-states.md](loading-and-error-states.md) - SuspenseLoader 用法
- [complete-examples.md](complete-examples.md) - 完整路由示例
