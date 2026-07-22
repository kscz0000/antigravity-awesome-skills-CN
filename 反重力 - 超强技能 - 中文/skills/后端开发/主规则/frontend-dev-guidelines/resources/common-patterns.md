# 常用模式

表单、认证、DataGrid、对话框和其他常用 UI 元素的常用模式。

---

## 使用 useAuth 进行认证

### 获取当前用户

```typescript
import { useAuth } from '@/hooks/useAuth';

export const MyComponent: React.FC = () => {
    const { user } = useAuth();

    // 可用属性：
    // - user.id: string
    // - user.email: string
    // - user.username: string
    // - user.roles: string[]

    return (
        <div>
            <p>登录用户: {user.email}</p>
            <p>用户名: {user.username}</p>
            <p>角色: {user.roles.join(', ')}</p>
        </div>
    );
};
```

**永远不要直接进行认证 API 调用** - 始终使用 `useAuth` hook。

---

## 使用 React Hook Form 处理表单

### 基础表单

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { TextField, Button } from '@mui/material';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

// Zod schema 用于验证
const formSchema = z.object({
    username: z.string().min(3, '用户名至少3个字符'),
    email: z.string().email('无效的邮箱地址'),
    age: z.number().min(18, '必须年满18岁'),
});

type FormData = z.infer<typeof formSchema>;

export const MyForm: React.FC = () => {
    const { showSuccess, showError } = useMuiSnackbar();

    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: '',
            email: '',
            age: 18,
        },
    });

    const onSubmit = async (data: FormData) => {
        try {
            await api.submitForm(data);
            showSuccess('表单提交成功');
        } catch (error) {
            showError('表单提交失败');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <TextField
                {...register('username')}
                label='用户名'
                error={!!errors.username}
                helperText={errors.username?.message}
            />

            <TextField
                {...register('email')}
                label='邮箱'
                error={!!errors.email}
                helperText={errors.email?.message}
                type='email'
            />

            <TextField
                {...register('age', { valueAsNumber: true })}
                label='年龄'
                error={!!errors.age}
                helperText={errors.age?.message}
                type='number'
            />

            <Button type='submit' variant='contained'>
                提交
            </Button>
        </form>
    );
};
```

---

## 对话框组件模式

### 标准对话框结构

来自 BEST_PRACTICES.md - 所有对话框应包含：
- 标题中的图标
- 关闭按钮（X）
- 底部操作按钮

```typescript
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, IconButton } from '@mui/material';
import { Close, Info } from '@mui/icons-material';

interface MyDialogProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
}

export const MyDialog: React.FC<MyDialogProps> = ({ open, onClose, onConfirm }) => {
    return (
        <Dialog open={open} onClose={onClose} maxWidth='sm' fullWidth>
            <DialogTitle>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Info color='primary' />
                        对话框标题
                    </Box>
                    <IconButton onClick={onClose} size='small'>
                        <Close />
                    </IconButton>
                </Box>
            </DialogTitle>

            <DialogContent>
                {/* 内容在这里 */}
            </DialogContent>

            <DialogActions>
                <Button onClick={onClose}>取消</Button>
                <Button onClick={onConfirm} variant='contained'>
                    确认
                </Button>
            </DialogActions>
        </Dialog>
    );
};
```

---

## DataGrid 包装器模式

### 包装器组件契约

来自 BEST_PRACTICES.md - DataGrid 包装器应接受：

**必需 Props：**
- `rows`：数据数组
- `columns`：列定义
- 加载/错误状态

**可选 Props：**
- 工具栏组件
- 自定义操作
- 初始状态

```typescript
import { DataGridPro } from '@mui/x-data-grid-pro';
import type { GridColDef } from '@mui/x-data-grid-pro';

interface DataGridWrapperProps {
    rows: any[];
    columns: GridColDef[];
    loading?: boolean;
    toolbar?: React.ReactNode;
    onRowClick?: (row: any) => void;
}

export const DataGridWrapper: React.FC<DataGridWrapperProps> = ({
    rows,
    columns,
    loading = false,
    toolbar,
    onRowClick,
}) => {
    return (
        <DataGridPro
            rows={rows}
            columns={columns}
            loading={loading}
            slots={{ toolbar: toolbar ? () => toolbar : undefined }}
            onRowClick={(params) => onRowClick?.(params.row)}
            // 标准配置
            pagination
            pageSizeOptions={[25, 50, 100]}
            initialState={{
                pagination: { paginationModel: { pageSize: 25 } },
            }}
        />
    );
};
```

---

## 变更模式

### 带缓存失效的更新

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const useUpdateEntity = () => {
    const queryClient = useQueryClient();
    const { showSuccess, showError } = useMuiSnackbar();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) =>
            api.updateEntity(id, data),

        onSuccess: (result, variables) => {
            // 使受影响的查询失效
            queryClient.invalidateQueries({ queryKey: ['entity', variables.id] });
            queryClient.invalidateQueries({ queryKey: ['entities'] });

            showSuccess('实体已更新');
        },

        onError: () => {
            showError('更新实体失败');
        },
    });
};

// 使用方式
const updateEntity = useUpdateEntity();

const handleSave = () => {
    updateEntity.mutate({ id: 123, data: { name: '新名称' } });
};
```

---

## 状态管理模式

### TanStack Query 用于服务端状态（主要）

使用 TanStack Query 管理**所有服务端数据**：
- 获取：useSuspenseQuery
- 变更：useMutation
- 缓存：自动
- 同步：内置

```typescript
// ✅ 正确 - TanStack Query 用于服务端数据
const { data: users } = useSuspenseQuery({
    queryKey: ['users'],
    queryFn: () => userApi.getUsers(),
});
```

### useState 用于 UI 状态

使用 `useState` 仅用于**本地 UI 状态**：
- 表单输入（非受控）
- 模态框打开/关闭
- 选中的标签页
- 临时 UI 标志

```typescript
// ✅ 正确 - useState 用于 UI 状态
const [modalOpen, setModalOpen] = useState(false);
const [selectedTab, setSelectedTab] = useState(0);
```

### Zustand 用于全局客户端状态（最小化）

仅将 Zustand 用于**全局客户端状态**：
- 主题偏好
- 侧边栏折叠状态
- 用户偏好（非来自服务端）

```typescript
import { create } from 'zustand';

interface AppState {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
}

export const useAppState = create<AppState>((set) => ({
    sidebarOpen: true,
    toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
```

**避免 props 逐层传递** - 使用 context 或 Zustand 替代。

---

## 总结

**常用模式：**
- ✅ useAuth hook 获取当前用户（id, email, roles, username）
- ✅ React Hook Form + Zod 处理表单
- ✅ 对话框带图标 + 关闭按钮
- ✅ DataGrid 包装器契约
- ✅ 带缓存失效的变更
- ✅ TanStack Query 用于服务端状态
- ✅ useState 用于 UI 状态
- ✅ Zustand 用于全局客户端状态（最小化）

**另见：**
- [data-fetching.md](data-fetching.md) - TanStack Query 模式
- [component-patterns.md](component-patterns.md) - 组件结构
- [loading-and-error-states.md](loading-and-error-states.md) - 错误处理
