---
name: react-state-management
description: "精通 React 现代状态管理，涵盖 Redux Toolkit、Zustand、Jotai 和 React Query。适用于配置全局状态、管理服务端状态或选型状态管理方案。触发词：React状态管理、Redux Toolkit、Zustand、Jotai、React Query、全局状态、服务端状态、状态管理选型、乐观更新、状态调试"
risk: unknown
source: community
date_added: "2026-02-27"
---

# React 状态管理

React 现代状态管理模式的完整指南，涵盖从组件本地状态到全局 Store 和服务端状态同步的全链路方案。

## 不适用场景

- 任务与 React 状态管理无关
- 需要本技能范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 适用场景

- 在 React 应用中配置全局状态管理
- 在 Redux Toolkit、Zustand 或 Jotai 之间做选型
- 使用 React Query 或 SWR 管理服务端状态
- 实现乐观更新
- 调试状态相关问题
- 从旧版 Redux 迁移到现代模式

## 核心概念

### 1. 状态分类

| 类型 | 说明 | 方案 |
|------|------|------|
| **本地状态** | 组件专属的 UI 状态 | useState, useReducer |
| **全局状态** | 跨组件共享 | Redux Toolkit, Zustand, Jotai |
| **服务端状态** | 远程数据、缓存 | React Query, SWR, RTK Query |
| **URL 状态** | 路由参数、搜索参数 | React Router, nuqs |
| **表单状态** | 输入值、校验 | React Hook Form, Formik |

### 2. 选型标准

```
小型应用，简单状态 → Zustand 或 Jotai
大型应用，复杂状态 → Redux Toolkit
重服务端交互 → React Query + 轻量客户端状态
原子化/细粒度更新 → Jotai
```

## 快速上手

### Zustand（最简方案）

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Usage in component
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## 模式

### 模式 1：Redux Toolkit + TypeScript

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import userReducer from './slices/userSlice'
import cartReducer from './slices/cartSlice'

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Typed hooks
export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
```

```typescript
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'

interface User {
  id: string
  email: string
  name: string
}

interface UserState {
  current: User | null
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  error: string | null
}

const initialState: UserState = {
  current: null,
  status: 'idle',
  error: null,
}

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`)
      if (!response.ok) throw new Error('Failed to fetch user')
      return await response.json()
    } catch (error) {
      return rejectWithValue((error as Error).message)
    }
  }
)

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.current = action.payload
      state.status = 'succeeded'
    },
    clearUser: (state) => {
      state.current = null
      state.status = 'idle'
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.current = action.payload
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.payload as string
      })
  },
})

export const { setUser, clearUser } = userSlice.actions
export default userSlice.reducer
```

### 模式 2：Zustand 分片模式（可扩展）

```typescript
// store/slices/createUserSlice.ts
import { StateCreator } from 'zustand'

export interface UserSlice {
  user: User | null
  isAuthenticated: boolean
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice, // Combined store type
  [],
  [],
  UserSlice
> = (set, get) => ({
  user: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const user = await authApi.login(credentials)
    set({ user, isAuthenticated: true })
  },
  logout: () => {
    set({ user: null, isAuthenticated: false })
    // Can access other slices
    // get().clearCart()
  },
})

// store/index.ts
import { create } from 'zustand'
import { createUserSlice, UserSlice } from './slices/createUserSlice'
import { createCartSlice, CartSlice } from './slices/createCartSlice'

type StoreState = UserSlice & CartSlice

export const useStore = create<StoreState>()((...args) => ({
  ...createUserSlice(...args),
  ...createCartSlice(...args),
}))

// Selective subscriptions (prevents unnecessary re-renders)
export const useUser = () => useStore((state) => state.user)
export const useCart = () => useStore((state) => state.cart)
```

### 模式 3：Jotai 原子化状态

```typescript
// atoms/userAtoms.ts
import { atom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'

// Basic atom
export const userAtom = atom<User | null>(null)

// Derived atom (computed)
export const isAuthenticatedAtom = atom((get) => get(userAtom) !== null)

// Atom with localStorage persistence
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light')

// Async atom
export const userProfileAtom = atom(async (get) => {
  const user = get(userAtom)
  if (!user) return null
  const response = await fetch(`/api/users/${user.id}/profile`)
  return response.json()
})

// Write-only atom (action)
export const logoutAtom = atom(null, (get, set) => {
  set(userAtom, null)
  set(cartAtom, [])
  localStorage.removeItem('token')
})

// Usage
function Profile() {
  const [user] = useAtom(userAtom)
  const [, logout] = useAtom(logoutAtom)
  const [profile] = useAtom(userProfileAtom) // Suspense-enabled

  return (
    <Suspense fallback={<Skeleton />}>
      <ProfileContent profile={profile} onLogout={logout} />
    </Suspense>
  )
}
```

### 模式 4：React Query 管理服务端状态

```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Query keys factory
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}

// Fetch hook
export function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes (formerly cacheTime)
  })
}

// Single user hook
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    enabled: !!id, // Don't fetch if no id
  })
}

// Mutation with optimistic update
export function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) })

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(userKeys.detail(newUser.id))

      // Optimistically update
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser)

      return { previousUser }
    },
    onError: (err, newUser, context) => {
      // Rollback on error
      queryClient.setQueryData(
        userKeys.detail(newUser.id),
        context?.previousUser
      )
    },
    onSettled: (data, error, variables) => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) })
    },
  })
}
```

### 模式 5：客户端状态 + 服务端状态组合

```typescript
// Zustand for client state
const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  modal: null,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  openModal: (modal) => set({ modal }),
  closeModal: () => set({ modal: null }),
}))

// React Query for server state
function Dashboard() {
  const { sidebarOpen, toggleSidebar } = useUIStore()
  const { data: users, isLoading } = useUsers({ active: true })
  const { data: stats } = useStats()

  if (isLoading) return <DashboardSkeleton />

  return (
    <div className={sidebarOpen ? 'with-sidebar' : ''}>
      <Sidebar open={sidebarOpen} onToggle={toggleSidebar} />
      <main>
        <StatsCards stats={stats} />
        <UserTable users={users} />
      </main>
    </div>
  )
}
```

## 最佳实践

### 推荐做法
- **就近放置状态** — 状态尽量靠近使用它的位置
- **善用选择器** — 通过选择性订阅避免不必要的重渲染
- **数据扁平化** — 展平嵌套结构便于更新操作
- **全面类型覆盖** — 完整的 TypeScript 类型防止运行时错误
- **关注点分离** — 服务端状态用 React Query，客户端状态用 Zustand

### 避免做法
- **不要过度全局化** — 并非所有状态都需要放入全局
- **不要重复存储服务端状态** — 交给 React Query 管理
- **不要直接修改** — 始终使用不可变更新
- **不要存储派生数据** — 应该计算得出
- **不要混用范式** — 每个分类选定一个主方案

## 迁移指南

### 从旧版 Redux 迁移到 RTK

```typescript
// Before (legacy Redux)
const ADD_TODO = 'ADD_TODO'
const addTodo = (text) => ({ type: ADD_TODO, payload: text })
function todosReducer(state = [], action) {
  switch (action.type) {
    case ADD_TODO:
      return [...state, { text: action.payload, completed: false }]
    default:
      return state
  }
}

// After (Redux Toolkit)
const todosSlice = createSlice({
  name: 'todos',
  initialState: [],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      // Immer allows "mutations"
      state.push({ text: action.payload, completed: false })
    },
  },
})
```

## 参考资源

- [Redux Toolkit 文档](https://redux-toolkit.js.org/)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [Jotai 文档](https://jotai.org/)
- [TanStack Query](https://tanstack.com/query)

## 局限性
- 仅在任务明确匹配上述范围时使用本技能
- 不可将输出视为环境特定验证、测试或专家评审的替代品
- 所需输入、权限、安全边界或成功标准缺失时，请停止并请求澄清
