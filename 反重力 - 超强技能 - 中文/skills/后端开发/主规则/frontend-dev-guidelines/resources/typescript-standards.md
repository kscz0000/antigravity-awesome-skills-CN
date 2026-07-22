# TypeScript 标准

React 前端代码中 TypeScript 类型安全与可维护性的最佳实践。

---

## 严格模式

### 配置

项目中 TypeScript 严格模式已**启用**：

```json
// tsconfig.json
{
    "compilerOptions": {
        "strict": true,
        "noImplicitAny": true,
        "strictNullChecks": true
    }
}
```

**这意味着：**
- 没有隐式 `any` 类型
- Null/undefined 必须显式处理
- 强制类型安全

---

## 禁止使用 `any` 类型

### 规则

```typescript
// ❌ NEVER use any
function handleData(data: any) {
    return data.something;
}

// ✅ Use specific types
interface MyData {
    something: string;
}

function handleData(data: MyData) {
    return data.something;
}

// ✅ Or use unknown for truly unknown data
function handleUnknown(data: unknown) {
    if (typeof data === 'object' && data !== null && 'something' in data) {
        return (data as MyData).something;
    }
}
```

**如果你确实不知道类型：**
- 使用 `unknown`（强制类型检查）
- 使用类型守卫进行缩窄
- 记录类型未知的原因

---

## 显式返回类型

### 函数返回类型

```typescript
// ✅ CORRECT - Explicit return type
function getUser(id: number): Promise<User> {
    return apiClient.get(`/users/${id}`);
}

function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ AVOID - Implicit return type (less clear)
function getUser(id: number) {
    return apiClient.get(`/users/${id}`);
}
```

### 组件返回类型

```typescript
// React.FC already provides return type (ReactElement)
export const MyComponent: React.FC<Props> = ({ prop }) => {
    return <div>{prop}</div>;
};

// For custom hooks
function useMyData(id: number): { data: Data; isLoading: boolean } {
    const [data, setData] = useState<Data | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    return { data: data!, isLoading };
}
```

---

## 类型导入

### 使用 'type' 关键字

```typescript
// ✅ CORRECT - Explicitly mark as type import
import type { User } from '~types/user';
import type { Post } from '~types/post';
import type { SxProps, Theme } from '@mui/material';

// ❌ AVOID - Mixed value and type imports
import { User } from '~types/user';  // Unclear if type or value
```

**优点：**
- 清晰区分类型与值
- 更好的 tree-shaking
- 防止循环依赖
- TypeScript 编译器优化

---

## 组件 Props 接口

### 接口模式

```typescript
/**
 * Props for MyComponent
 */
interface MyComponentProps {
    /** The user ID to display */
    userId: number;

    /** Optional callback when action completes */
    onComplete?: () => void;

    /** Display mode for the component */
    mode?: 'view' | 'edit';

    /** Additional CSS classes */
    className?: string;
}

export const MyComponent: React.FC<MyComponentProps> = ({
    userId,
    onComplete,
    mode = 'view',  // Default value
    className,
}) => {
    return <div>...</div>;
};
```

**关键点：**
- 为 props 单独定义接口
- 每个 prop 添加 JSDoc 注释
- 可选 prop 使用 `?`
- 在解构中提供默认值

### 带 Children 的 Props

```typescript
interface ContainerProps {
    children: React.ReactNode;
    title: string;
}

// React.FC automatically includes children type, but be explicit
export const Container: React.FC<ContainerProps> = ({ children, title }) => {
    return (
        <div>
            <h2>{title}</h2>
            {children}
        </div>
    );
};
```

---

## 工具类型

### Partial<T>

```typescript
// Make all properties optional
type UserUpdate = Partial<User>;

function updateUser(id: number, updates: Partial<User>) {
    // updates can have any subset of User properties
}
```

### Pick<T, K>

```typescript
// Select specific properties
type UserPreview = Pick<User, 'id' | 'name' | 'email'>;

const preview: UserPreview = {
    id: 1,
    name: 'John',
    email: 'john@example.com',
    // Other User properties not allowed
};
```

### Omit<T, K>

```typescript
// Exclude specific properties
type UserWithoutPassword = Omit<User, 'password' | 'passwordHash'>;

const publicUser: UserWithoutPassword = {
    id: 1,
    name: 'John',
    email: 'john@example.com',
    // password and passwordHash not allowed
};
```

### Required<T>

```typescript
// Make all properties required
type RequiredConfig = Required<Config>;  // All optional props become required
```

### Record<K, V>

```typescript
// Type-safe object/map
const userMap: Record<string, User> = {
    'user1': { id: 1, name: 'John' },
    'user2': { id: 2, name: 'Jane' },
};

// For styles
import type { SxProps, Theme } from '@mui/material';

const styles: Record<string, SxProps<Theme>> = {
    container: { p: 2 },
    header: { mb: 1 },
};
```

---

## 类型守卫

### 基本类型守卫

```typescript
function isUser(data: unknown): data is User {
    return (
        typeof data === 'object' &&
        data !== null &&
        'id' in data &&
        'name' in data
    );
}

// Usage
if (isUser(response)) {
    console.log(response.name);  // TypeScript knows it's User
}
```

### 可辨识联合类型

```typescript
type LoadingState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: Data }
    | { status: 'error'; error: Error };

function Component({ state }: { state: LoadingState }) {
    // TypeScript narrows type based on status
    if (state.status === 'success') {
        return <Display data={state.data} />;  // data available here
    }

    if (state.status === 'error') {
        return <Error error={state.error} />;  // error available here
    }

    return <Loading />;
}
```

---

## 泛型类型

### 泛型函数

```typescript
function getById<T>(items: T[], id: number): T | undefined {
    return items.find(item => (item as any).id === id);
}

// Usage with type inference
const users: User[] = [...];
const user = getById(users, 123);  // Type: User | undefined
```

### 泛型组件

```typescript
interface ListProps<T> {
    items: T[];
    renderItem: (item: T) => React.ReactNode;
}

export function List<T>({ items, renderItem }: ListProps<T>): React.ReactElement {
    return (
        <div>
            {items.map((item, index) => (
                <div key={index}>{renderItem(item)}</div>
            ))}
        </div>
    );
}

// Usage
<List<User>
    items={users}
    renderItem={(user) => <UserCard user={user} />}
/>
```

---

## 类型断言（谨慎使用）

### 何时使用

```typescript
// ✅ OK - When you know more than TypeScript
const element = document.getElementById('my-element') as HTMLInputElement;
const value = element.value;

// ✅ OK - API response that you've validated
const response = await api.getData();
const user = response.data as User;  // You know the shape
```

### 何时不使用

```typescript
// ❌ AVOID - Circumventing type safety
const data = getData() as any;  // WRONG - defeats TypeScript

// ❌ AVOID - Unsafe assertion
const value = unknownValue as string;  // Might not actually be string
```

---

## Null/Undefined 处理

### 可选链

```typescript
// ✅ CORRECT
const name = user?.profile?.name;

// Equivalent to:
const name = user && user.profile && user.profile.name;
```

### 空值合并

```typescript
// ✅ CORRECT
const displayName = user?.name ?? 'Anonymous';

// Only uses default if null or undefined
// (Different from || which triggers on '', 0, false)
```

### 非空断言（谨慎使用）

```typescript
// ✅ OK - When you're certain value exists
const data = queryClient.getQueryData<Data>(['data'])!;

// ⚠️ CAREFUL - Only use when you KNOW it's not null
// Better to check explicitly:
const data = queryClient.getQueryData<Data>(['data']);
if (data) {
    // Use data
}
```

---

## 总结

**TypeScript 检查清单：**
- ✅ 启用严格模式
- ✅ 禁止使用 `any` 类型（需要时使用 `unknown`）
- ✅ 函数显式返回类型
- ✅ 使用 `import type` 进行类型导入
- ✅ Props 接口添加 JSDoc 注释
- ✅ 工具类型（Partial、Pick、Omit、Required、Record）
- ✅ 使用类型守卫进行缩窄
- ✅ 可选链与空值合并
- ❌ 避免使用类型断言，除非必要

**另见：**
- [component-patterns.md](component-patterns.md) - 组件类型
- [data-fetching.md](data-fetching.md) - API 类型
