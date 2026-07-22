# 加载与错误状态

**关键**：正确处理加载和错误状态可防止布局偏移，并提供更好的用户体验。

---

## ⚠️ 关键规则：永远不要使用提前返回

### 问题所在

```typescript
// ❌ NEVER DO THIS - Early return with loading spinner
const Component = () => {
    const { data, isLoading } = useQuery();

    // WRONG: This causes layout shift and poor UX
    if (isLoading) {
        return <LoadingSpinner />;
    }

    return <Content data={data} />;
};
```

**为什么这样做不好：**
1. **布局偏移**：加载完成时内容位置会跳动
2. **CLS（累积布局偏移）**：Core Web Vitals 评分差
3. **糟糕的用户体验**：页面结构突然变化
4. **丢失滚动位置**：用户在页面上的位置丢失

### 解决方案

**方案一：SuspenseLoader（新组件推荐使用）**

```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

export const MyComponent: React.FC = () => {
    return (
        <SuspenseLoader>
            <HeavyComponent />
        </SuspenseLoader>
    );
};
```

**方案二：LoadingOverlay（适用于遗留的 useQuery 模式）**

```typescript
import { LoadingOverlay } from '~components/LoadingOverlay';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <LoadingOverlay loading={isLoading}>
            <Content data={data} />
        </LoadingOverlay>
    );
};
```

---

## SuspenseLoader 组件

### 功能说明

- 在懒加载组件加载时显示加载指示器
- 平滑的淡入动画
- 防止布局偏移
- 应用中统一的加载体验

### 导入

```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';
// Or
import { SuspenseLoader } from '@/components/SuspenseLoader';
```

### 基本用法

```typescript
<SuspenseLoader>
    <LazyLoadedComponent />
</SuspenseLoader>
```

### 配合 useSuspenseQuery 使用

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { SuspenseLoader } from '~components/SuspenseLoader';

const Inner: React.FC = () => {
    // No isLoading needed!
    const { data } = useSuspenseQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),
    });

    return <Display data={data} />;
};

// Outer component wraps in Suspense
export const Outer: React.FC = () => {
    return (
        <SuspenseLoader>
            <Inner />
        </SuspenseLoader>
    );
};
```

### 多个 Suspense 边界

**模式**：为独立区域分别设置加载状态

```typescript
export const Dashboard: React.FC = () => {
    return (
        <Box>
            <SuspenseLoader>
                <Header />
            </SuspenseLoader>

            <SuspenseLoader>
                <MainContent />
            </SuspenseLoader>

            <SuspenseLoader>
                <Sidebar />
            </SuspenseLoader>
        </Box>
    );
};
```

**优势：**
- 每个区域独立加载
- 用户能更快看到部分内容
- 更好的感知性能

### 嵌套 Suspense

```typescript
export const ParentComponent: React.FC = () => {
    return (
        <SuspenseLoader>
            {/* Parent suspends while loading */}
            <ParentContent>
                <SuspenseLoader>
                    {/* Nested suspense for child */}
                    <ChildComponent />
                </SuspenseLoader>
            </ParentContent>
        </SuspenseLoader>
    );
};
```

---

## LoadingOverlay 组件

### 使用场景

- 使用 `useQuery` 的遗留组件（尚未重构为 Suspense）
- 需要遮罩层加载状态
- 无法使用 Suspense 边界

### 用法

```typescript
import { LoadingOverlay } from '~components/LoadingOverlay';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),
    });

    return (
        <LoadingOverlay loading={isLoading}>
            <Box sx={{ p: 2 }}>
                {data && <Content data={data} />}
            </Box>
        </LoadingOverlay>
    );
};
```

**功能说明：**
- 显示带旋转加载器的半透明遮罩层
- 内容区域保留（无布局偏移）
- 加载期间阻止交互

---

## 错误处理

### useMuiSnackbar Hook（必需）

**永远不要使用 react-toastify** — 项目标准为 MUI Snackbar

```typescript
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const MyComponent: React.FC = () => {
    const { showSuccess, showError, showInfo, showWarning } = useMuiSnackbar();

    const handleAction = async () => {
        try {
            await api.doSomething();
            showSuccess('Operation completed successfully');
        } catch (error) {
            showError('Operation failed');
        }
    };

    return <Button onClick={handleAction}>Do Action</Button>;
};
```

**可用方法：**
- `showSuccess(message)` - 绿色成功消息
- `showError(message)` - 红色错误消息
- `showWarning(message)` - 橙色警告消息
- `showInfo(message)` - 蓝色信息消息

### TanStack Query 错误回调

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const MyComponent: React.FC = () => {
    const { showError } = useMuiSnackbar();

    const { data } = useSuspenseQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),

        // Handle errors
        onError: (error) => {
            showError('Failed to load data');
            console.error('Query error:', error);
        },
    });

    return <Content data={data} />;
};
```

### 错误边界

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
    return (
        <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant='h5' color='error'>
                Something went wrong
            </Typography>
            <Typography>{error.message}</Typography>
            <Button onClick={resetErrorBoundary}>Try Again</Button>
        </Box>
    );
}

export const MyPage: React.FC = () => {
    return (
        <ErrorBoundary
            FallbackComponent={ErrorFallback}
            onError={(error) => console.error('Boundary caught:', error)}
        >
            <SuspenseLoader>
                <ComponentThatMightError />
            </SuspenseLoader>
        </ErrorBoundary>
    );
};
```

---

## 完整示例

### 示例一：使用 Suspense 的现代组件

```typescript
import React from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { SuspenseLoader } from '~components/SuspenseLoader';
import { myFeatureApi } from '../api/myFeatureApi';

// Inner component uses useSuspenseQuery
const InnerComponent: React.FC<{ id: number }> = ({ id }) => {
    const { data } = useSuspenseQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    // data is always defined - no isLoading needed!
    return (
        <Paper sx={{ p: 2 }}>
            <h2>{data.title}</h2>
            <p>{data.description}</p>
        </Paper>
    );
};

// Outer component provides Suspense boundary
export const OuterComponent: React.FC<{ id: number }> = ({ id }) => {
    return (
        <Box>
            <SuspenseLoader>
                <InnerComponent id={id} />
            </SuspenseLoader>
        </Box>
    );
};

export default OuterComponent;
```

### 示例二：使用 LoadingOverlay 的遗留模式

```typescript
import React from 'react';
import { Box } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { LoadingOverlay } from '~components/LoadingOverlay';
import { myFeatureApi } from '../api/myFeatureApi';

export const LegacyComponent: React.FC<{ id: number }> = ({ id }) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    return (
        <LoadingOverlay loading={isLoading}>
            <Box sx={{ p: 2 }}>
                {error && <ErrorDisplay error={error} />}
                {data && <Content data={data} />}
            </Box>
        </LoadingOverlay>
    );
};
```

### 示例三：使用 Snackbar 的错误处理

```typescript
import React from 'react';
import { useSuspenseQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@mui/material';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';
import { myFeatureApi } from '../api/myFeatureApi';

export const EntityEditor: React.FC<{ id: number }> = ({ id }) => {
    const queryClient = useQueryClient();
    const { showSuccess, showError } = useMuiSnackbar();

    const { data } = useSuspenseQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
        onError: () => {
            showError('Failed to load entity');
        },
    });

    const updateMutation = useMutation({
        mutationFn: (updates) => myFeatureApi.update(id, updates),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity', id] });
            showSuccess('Entity updated successfully');
        },

        onError: () => {
            showError('Failed to update entity');
        },
    });

    return (
        <Button onClick={() => updateMutation.mutate({ name: 'New' })}>
            Update
        </Button>
    );
};
```

---

## 加载状态反模式

### ❌ 不要这样做

```typescript
// ❌ NEVER - Early return
if (isLoading) {
    return <CircularProgress />;
}

// ❌ NEVER - Conditional rendering
{isLoading ? <Spinner /> : <Content />}

// ❌ NEVER - Layout changes
if (isLoading) {
    return (
        <Box sx={{ height: 100 }}>
            <Spinner />
        </Box>
    );
}
return (
    <Box sx={{ height: 500 }}>  // Different height!
        <Content />
    </Box>
);
```

### ✅ 应该这样做

```typescript
// ✅ BEST - useSuspenseQuery + SuspenseLoader
<SuspenseLoader>
    <ComponentWithSuspenseQuery />
</SuspenseLoader>

// ✅ ACCEPTABLE - LoadingOverlay
<LoadingOverlay loading={isLoading}>
    <Content />
</LoadingOverlay>

// ✅ OK - Inline skeleton with same layout
<Box sx={{ height: 500 }}>
    {isLoading ? <Skeleton variant='rectangular' height='100%' /> : <Content />}
</Box>
```

---

## 骨架屏加载（替代方案）

### MUI Skeleton 组件

```typescript
import { Skeleton, Box } from '@mui/material';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <Box sx={{ p: 2 }}>
            {isLoading ? (
                <>
                    <Skeleton variant='text' width={200} height={40} />
                    <Skeleton variant='rectangular' width='100%' height={200} />
                    <Skeleton variant='text' width='100%' />
                </>
            ) : (
                <>
                    <Typography variant='h5'>{data.title}</Typography>
                    <img src={data.image} />
                    <Typography>{data.description}</Typography>
                </>
            )}
        </Box>
    );
};
```

**关键**：骨架屏必须与实际内容具有**相同的布局**（避免偏移）

---

## 总结

**加载状态：**
- ✅ **首选**：SuspenseLoader + useSuspenseQuery（现代模式）
- ✅ **可接受**：LoadingOverlay（遗留模式）
- ✅ **可以**：相同布局的骨架屏
- ❌ **绝不**：提前返回或条件布局

**错误处理：**
- ✅ **始终**：使用 useMuiSnackbar 进行用户反馈
- ❌ **绝不**：react-toastify
- ✅ 在查询/变更中使用 onError 回调
- ✅ 组件级错误使用错误边界

**另请参阅：**
- [component-patterns.md](component-patterns.md) - Suspense 集成
- [data-fetching.md](data-fetching.md) - useSuspenseQuery 详情
