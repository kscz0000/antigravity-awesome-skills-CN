# 文件组织

应用中可维护、可扩展的前端代码的文件和目录结构规范。

---

## features/ 与 components/ 的区别

### features/ 目录

**用途**：具有独立逻辑、API 和组件的领域特定功能

**何时使用：**
- 功能包含多个相关组件
- 功能有独立的 API 端点
- 功能包含领域特定逻辑
- 功能包含自定义 hooks/工具函数

**示例：**
- `features/posts/` - 项目目录/文章管理
- `features/blogs/` - 博客构建器和渲染
- `features/auth/` - 认证流程

**结构：**
```
features/
  my-feature/
    api/
      myFeatureApi.ts         # API service layer
    components/
      MyFeatureMain.tsx       # Main component
      SubComponents/          # Related components
    hooks/
      useMyFeature.ts         # Custom hooks
      useSuspenseMyFeature.ts # Suspense hooks
    helpers/
      myFeatureHelpers.ts     # Utility functions
    types/
      index.ts                # TypeScript types
    index.ts                  # Public exports
```

### components/ 目录

**用途**：跨多个功能使用的真正可复用组件

**何时使用：**
- 组件在 3 个以上的地方使用
- 组件是通用的（无功能特定逻辑）
- 组件是 UI 原语或模式

**示例：**
- `components/SuspenseLoader/` - 加载包装器
- `components/CustomAppBar/` - 应用头部
- `components/ErrorBoundary/` - 错误处理
- `components/LoadingOverlay/` - 加载覆盖层

**结构：**
```
components/
  SuspenseLoader/
    SuspenseLoader.tsx
    SuspenseLoader.test.tsx
  CustomAppBar/
    CustomAppBar.tsx
    CustomAppBar.test.tsx
```

---

## 功能目录结构（详细版）

### 完整功能示例

基于 `features/posts/` 的结构：

```
features/
  posts/
    api/
      postApi.ts              # API service layer (GET, POST, PUT, DELETE)

    components/
      PostTable.tsx           # Main container component
      grids/
        PostDataGrid/
          PostDataGrid.tsx
      drawers/
        ProjectPostDrawer/
          ProjectPostDrawer.tsx
      cells/
        editors/
          TextEditCell.tsx
        renderers/
          DateCell.tsx
      toolbar/
        CustomToolbar.tsx

    hooks/
      usePostQueries.ts       # Regular queries
      useSuspensePost.ts      # Suspense queries
      usePostMutations.ts     # Mutations
      useGridLayout.ts              # Feature-specific hooks

    helpers/
      postHelpers.ts          # Utility functions
      validation.ts                 # Validation logic

    types/
      index.ts                      # TypeScript types/interfaces

    queries/
      postQueries.ts          # Query key factories (optional)

    context/
      PostContext.tsx         # React context (if needed)

    index.ts                        # Public API exports
```

### 子目录指南

#### api/ 目录

**用途**：功能的集中式 API 调用

**文件：**
- `{feature}Api.ts` - 主 API 服务

**模式：**
```typescript
// features/my-feature/api/myFeatureApi.ts
import apiClient from '@/lib/apiClient';

export const myFeatureApi = {
    getItem: async (id: number) => {
        const { data } = await apiClient.get(`/blog/items/${id}`);
        return data;
    },
    createItem: async (payload) => {
        const { data } = await apiClient.post('/blog/items', payload);
        return data;
    },
};
```

#### components/ 目录

**用途**：功能特定的组件

**组织方式：**
- 少于 5 个组件时使用扁平结构
- 超过 5 个组件时按职责划分子目录

**示例：**
```
components/
  MyFeatureMain.tsx           # Main component
  MyFeatureHeader.tsx         # Supporting components
  MyFeatureFooter.tsx

  # OR with subdirectories:
  containers/
    MyFeatureContainer.tsx
  presentational/
    MyFeatureDisplay.tsx
  blogs/
    MyFeatureBlog.tsx
```

#### hooks/ 目录

**用途**：功能的自定义 hooks

**命名规范：**
- 使用 `use` 前缀（camelCase）
- 描述其用途

**示例：**
```
hooks/
  useMyFeature.ts               # Main hook
  useSuspenseMyFeature.ts       # Suspense version
  useMyFeatureMutations.ts      # Mutations
  useMyFeatureFilters.ts        # Filters/search
```

#### helpers/ 目录

**用途**：功能特定的工具函数

**示例：**
```
helpers/
  myFeatureHelpers.ts           # General utilities
  validation.ts                 # Validation logic
  transblogers.ts               # Data transblogations
  constants.ts                  # Constants
```

#### types/ 目录

**用途**：TypeScript 类型和接口

**文件：**
```
types/
  index.ts                      # Main types, exported
  internal.ts                   # Internal types (not exported)
```

---

## 导入别名（Vite 配置）

### 可用别名

来自 `vite.config.ts` 第 180-185 行：

| 别名 | 解析到 | 用途 |
|-------|-------------|---------|
| `@/` | `src/` | 从 src 根目录的绝对导入 |
| `~types` | `src/types` | 共享 TypeScript 类型 |
| `~components` | `src/components` | 可复用组件 |
| `~features` | `src/features` | 功能导入 |

### 使用示例

```typescript
// ✅ PREFERRED - Use aliases for absolute imports
import { apiClient } from '@/lib/apiClient';
import { SuspenseLoader } from '~components/SuspenseLoader';
import { postApi } from '~features/posts/api/postApi';
import type { User } from '~types/user';

// ❌ AVOID - Relative paths from deep nesting
import { apiClient } from '../../../lib/apiClient';
import { SuspenseLoader } from '../../../components/SuspenseLoader';
```

### 何时使用哪个别名

**@/（通用）**：
- 工具库：`@/lib/apiClient`
- Hooks：`@/hooks/useAuth`
- 配置：`@/config/theme`
- 共享服务：`@/services/authService`

**~types（类型导入）**：
```typescript
import type { Post } from '~types/post';
import type { User, UserRole } from '~types/user';
```

**~components（可复用组件）**：
```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';
import { CustomAppBar } from '~components/CustomAppBar';
import { ErrorBoundary } from '~components/ErrorBoundary';
```

**~features（功能导入）**：
```typescript
import { postApi } from '~features/posts/api/postApi';
import { useAuth } from '~features/auth/hooks/useAuth';
```

---

## 文件命名规范

### 组件

**模式**：PascalCase，使用 `.tsx` 扩展名

```
MyComponent.tsx
PostDataGrid.tsx
CustomAppBar.tsx
```

**避免：**
- camelCase：`myComponent.tsx` ❌
- kebab-case：`my-component.tsx` ❌
- 全大写：`MYCOMPONENT.tsx` ❌

### Hooks

**模式**：camelCase，使用 `use` 前缀，`.ts` 扩展名

```
useMyFeature.ts
useSuspensePost.ts
useAuth.ts
useGridLayout.ts
```

### API 服务

**模式**：camelCase，使用 `Api` 后缀，`.ts` 扩展名

```
myFeatureApi.ts
postApi.ts
userApi.ts
```

### 工具函数

**模式**：camelCase，描述性名称，`.ts` 扩展名

```
myFeatureHelpers.ts
validation.ts
transblogers.ts
constants.ts
```

### 类型

**模式**：camelCase，`index.ts` 或描述性名称

```
types/index.ts
types/post.ts
types/user.ts
```

---

## 何时创建新功能

### 创建新功能的条件：

- 多个相关组件（>3 个）
- 拥有独立的 API 端点
- 包含领域特定逻辑
- 会随时间增长
- 跨多个路由复用

**示例：** `features/posts/`
- 20+ 个组件
- 独立的 API 服务
- 复杂的状态管理
- 在多个路由中使用

### 添加到现有功能的条件：

- 与现有功能相关
- 共享相同的 API
- 逻辑上可归为一组
- 扩展现有功能

**示例：** 为 posts 功能添加导出对话框

### 创建可复用组件的条件：

- 跨 3 个以上功能使用
- 通用，无领域逻辑
- 纯展示组件
- 共享模式

**示例：** `components/SuspenseLoader/`

---

## 导入组织

### 导入顺序（推荐）

```typescript
// 1. React and React-related
import React, { useState, useCallback, useMemo } from 'react';
import { lazy } from 'react';

// 2. Third-party libraries (alphabetical)
import { Box, Paper, Button, Grid } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { createFileRoute } from '@tanstack/react-router';

// 3. Alias imports (@ first, then ~)
import { apiClient } from '@/lib/apiClient';
import { useAuth } from '@/hooks/useAuth';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';
import { SuspenseLoader } from '~components/SuspenseLoader';
import { postApi } from '~features/posts/api/postApi';

// 4. Type imports (grouped)
import type { Post } from '~types/post';
import type { User } from '~types/user';

// 5. Relative imports (same feature)
import { MySubComponent } from './MySubComponent';
import { useMyFeature } from '../hooks/useMyFeature';
import { myFeatureHelpers } from '../helpers/myFeatureHelpers';
```

**所有导入使用单引号**（项目标准）

---

## 公共 API 模式

### feature/index.ts

从功能导出公共 API 以实现干净的导入：

```typescript
// features/my-feature/index.ts

// Export main components
export { MyFeatureMain } from './components/MyFeatureMain';
export { MyFeatureHeader } from './components/MyFeatureHeader';

// Export hooks
export { useMyFeature } from './hooks/useMyFeature';
export { useSuspenseMyFeature } from './hooks/useSuspenseMyFeature';

// Export API
export { myFeatureApi } from './api/myFeatureApi';

// Export types
export type { MyFeatureData, MyFeatureConfig } from './types';
```

**用法：**
```typescript
// ✅ Clean import from feature index
import { MyFeatureMain, useMyFeature } from '~features/my-feature';

// ❌ Avoid deep imports (but OK if needed)
import { MyFeatureMain } from '~features/my-feature/components/MyFeatureMain';
```

---

## 目录结构可视化

```
src/
├── features/                    # Domain-specific features
│   ├── posts/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── helpers/
│   │   ├── types/
│   │   └── index.ts
│   ├── blogs/
│   └── auth/
│
├── components/                  # Reusable components
│   ├── SuspenseLoader/
│   ├── CustomAppBar/
│   ├── ErrorBoundary/
│   └── LoadingOverlay/
│
├── routes/                      # TanStack Router routes
│   ├── __root.tsx
│   ├── index.tsx
│   ├── project-catalog/
│   │   ├── index.tsx
│   │   └── create/
│   └── blogs/
│
├── hooks/                       # Shared hooks
│   ├── useAuth.ts
│   ├── useMuiSnackbar.ts
│   └── useDebounce.ts
│
├── lib/                         # Shared utilities
│   ├── apiClient.ts
│   └── utils.ts
│
├── types/                       # Shared TypeScript types
│   ├── user.ts
│   ├── post.ts
│   └── common.ts
│
├── config/                      # Configuration
│   └── theme.ts
│
└── App.tsx                      # Root component
```

---

## 总结

**核心原则：**
1. **features/** 用于领域特定代码
2. **components/** 用于真正可复用的 UI
3. 使用子目录：api/、components/、hooks/、helpers/、types/
4. 使用导入别名实现干净导入（@/、~types、~components、~features）
5. 统一命名：PascalCase 用于组件，camelCase 用于工具函数
6. 从功能的 index.ts 导出公共 API

**另请参阅：**
- [component-patterns.md](component-patterns.md) - 组件结构
- [data-fetching.md](data-fetching.md) - API 服务模式
- [complete-examples.md](complete-examples.md) - 完整功能示例
