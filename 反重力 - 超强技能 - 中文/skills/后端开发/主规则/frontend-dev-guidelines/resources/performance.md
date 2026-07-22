# 性能优化

优化 React 组件性能、防止不必要的重新渲染以及避免内存泄漏的模式。

---

## 记忆化模式

### 使用 useMemo 进行昂贵计算

```typescript
import { useMemo } from 'react';

export const DataDisplay: React.FC<{ items: Item[], searchTerm: string }> = ({
    items,
    searchTerm,
}) => {
    // ❌ AVOID - Runs on every render
    const filteredItems = items
        .filter(item => item.name.includes(searchTerm))
        .sort((a, b) => a.name.localeCompare(b.name));

    // ✅ CORRECT - Memoized, only recalculates when dependencies change
    const filteredItems = useMemo(() => {
        return items
            .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
            .sort((a, b) => a.name.localeCompare(b.name));
    }, [items, searchTerm]);

    return <List items={filteredItems} />;
};
```

**何时使用 useMemo：**
- 过滤/排序大型数组
- 复杂计算
- 转换数据结构
- 昂贵的计算（循环、递归）

**何时不使用 useMemo：**
- 简单的字符串拼接
- 基本算术运算
- 过早优化（先做性能分析！）

---

## 使用 useCallback 处理事件处理函数

### 问题所在

```typescript
// ❌ AVOID - Creates new function on every render
export const Parent: React.FC = () => {
    const handleClick = (id: string) => {
        console.log('Clicked:', id);
    };

    // Child re-renders every time Parent renders
    // because handleClick is a new function reference each time
    return <Child onClick={handleClick} />;
};
```

### 解决方案

```typescript
import { useCallback } from 'react';

export const Parent: React.FC = () => {
    // ✅ CORRECT - Stable function reference
    const handleClick = useCallback((id: string) => {
        console.log('Clicked:', id);
    }, []); // Empty deps = function never changes

    // Child only re-renders when props actually change
    return <Child onClick={handleClick} />;
};
```

**何时使用 useCallback：**
- 作为 props 传递给子组件的函数
- 在 useEffect 中作为依赖项的函数
- 传递给记忆化组件的函数
- 列表中的事件处理函数

**何时不使用 useCallback：**
- 不传递给子组件的事件处理函数
- 简单的内联处理函数：`onClick={() => doSomething()}`

---

## 使用 React.memo 进行组件记忆化

### 基本用法

```typescript
import React from 'react';

interface ExpensiveComponentProps {
    data: ComplexData;
    onAction: () => void;
}

// ✅ Wrap expensive components in React.memo
export const ExpensiveComponent = React.memo<ExpensiveComponentProps>(
    function ExpensiveComponent({ data, onAction }) {
        // Complex rendering logic
        return <ComplexVisualization data={data} />;
    }
);
```

**何时使用 React.memo：**
- 组件频繁渲染
- 组件渲染开销大
- props 不经常变化
- 组件是列表项
- DataGrid 单元格/渲染器

**何时不使用 React.memo：**
- props 本身经常变化
- 渲染速度已经很快
- 过早优化

---

## 防抖搜索

### 使用 use-debounce Hook

```typescript
import { useState } from 'react';
import { useDebounce } from 'use-debounce';
import { useSuspenseQuery } from '@tanstack/react-query';

export const SearchComponent: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');

    // Debounce for 300ms
    const [debouncedSearchTerm] = useDebounce(searchTerm, 300);

    // Query uses debounced value
    const { data } = useSuspenseQuery({
        queryKey: ['search', debouncedSearchTerm],
        queryFn: () => api.search(debouncedSearchTerm),
        enabled: debouncedSearchTerm.length > 0,
    });

    return (
        <input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder='Search...'
        />
    );
};
```

**最佳防抖时间：**
- **300-500ms**：搜索/过滤
- **1000ms**：自动保存
- **100-200ms**：实时验证

---

## 内存泄漏防护

### 清理定时器/间隔器

```typescript
import { useEffect, useState } from 'react';

export const MyComponent: React.FC = () => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        // ✅ CORRECT - Cleanup interval
        const intervalId = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);

        return () => {
            clearInterval(intervalId);  // Cleanup!
        };
    }, []);

    useEffect(() => {
        // ✅ CORRECT - Cleanup timeout
        const timeoutId = setTimeout(() => {
            console.log('Delayed action');
        }, 5000);

        return () => {
            clearTimeout(timeoutId);  // Cleanup!
        };
    }, []);

    return <div>{count}</div>;
};
```

### 清理事件监听器

```typescript
useEffect(() => {
    const handleResize = () => {
        console.log('Resized');
    };

    window.addEventListener('resize', handleResize);

    return () => {
        window.removeEventListener('resize', handleResize);  // Cleanup!
    };
}, []);
```

### 使用 Abort Controller 中止 Fetch 请求

```typescript
useEffect(() => {
    const abortController = new AbortController();

    fetch('/api/data', { signal: abortController.signal })
        .then(response => response.json())
        .then(data => setState(data))
        .catch(error => {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            }
        });

    return () => {
        abortController.abort();  // Cleanup!
    };
}, []);
```

**注意**：使用 TanStack Query 时，这些清理操作会自动处理。

---

## 表单性能

### 监听特定字段（而非全部）

```typescript
import { useForm } from 'react-hook-form';

export const MyForm: React.FC = () => {
    const { register, watch, handleSubmit } = useForm();

    // ❌ AVOID - Watches all fields, re-renders on any change
    const formValues = watch();

    // ✅ CORRECT - Watch only what you need
    const username = watch('username');
    const email = watch('email');

    // Or multiple specific fields
    const [username, email] = watch(['username', 'email']);

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('username')} />
            <input {...register('email')} />
            <input {...register('password')} />

            {/* Only re-renders when username/email change */}
            <p>Username: {username}, Email: {email}</p>
        </form>
    );
};
```

---

## 列表渲染优化

### Key 属性的使用

```typescript
// ✅ CORRECT - Stable unique keys
{items.map(item => (
    <ListItem key={item.id}>
        {item.name}
    </ListItem>
))}

// ❌ AVOID - Index as key (unstable if list changes)
{items.map((item, index) => (
    <ListItem key={index}>  // WRONG if list reorders
        {item.name}
    </ListItem>
))}
```

### 记忆化列表项

```typescript
const ListItem = React.memo<ListItemProps>(({ item, onAction }) => {
    return (
        <Box onClick={() => onAction(item.id)}>
            {item.name}
        </Box>
    );
});

export const List: React.FC<{ items: Item[] }> = ({ items }) => {
    const handleAction = useCallback((id: string) => {
        console.log('Action:', id);
    }, []);

    return (
        <Box>
            {items.map(item => (
                <ListItem
                    key={item.id}
                    item={item}
                    onAction={handleAction}
                />
            ))}
        </Box>
    );
};
```

---

## 防止组件重新初始化

### 问题所在

```typescript
// ❌ AVOID - Component recreated on every render
export const Parent: React.FC = () => {
    // New component definition each render!
    const ChildComponent = () => <div>Child</div>;

    return <ChildComponent />;  // Unmounts and remounts every render
};
```

### 解决方案

```typescript
// ✅ CORRECT - Define outside or use useMemo
const ChildComponent: React.FC = () => <div>Child</div>;

export const Parent: React.FC = () => {
    return <ChildComponent />;  // Stable component
};

// ✅ OR if dynamic, use useMemo
export const Parent: React.FC<{ config: Config }> = ({ config }) => {
    const DynamicComponent = useMemo(() => {
        return () => <div>{config.title}</div>;
    }, [config.title]);

    return <DynamicComponent />;
};
```

---

## 懒加载重量级依赖

### 代码分割

```typescript
// ❌ AVOID - Import heavy libraries at top level
import jsPDF from 'jspdf';  // Large library loaded immediately
import * as XLSX from 'xlsx';  // Large library loaded immediately

// ✅ CORRECT - Dynamic import when needed
const handleExportPDF = async () => {
    const { jsPDF } = await import('jspdf');
    const doc = new jsPDF();
    // Use it
};

const handleExportExcel = async () => {
    const XLSX = await import('xlsx');
    // Use it
};
```

---

## 总结

**性能检查清单：**
- ✅ 使用 `useMemo` 处理昂贵计算（filter、sort、map）
- ✅ 使用 `useCallback` 处理传递给子组件的函数
- ✅ 使用 `React.memo` 处理昂贵组件
- ✅ 搜索/过滤防抖（300-500ms）
- ✅ 在 useEffect 中清理定时器/间隔器
- ✅ 监听特定表单字段（而非全部）
- ✅ 列表中使用稳定的 key
- ✅ 懒加载重量级库
- ✅ 使用 React.lazy 进行代码分割

**另请参阅：**
- [component-patterns.md](component-patterns.md) - 懒加载
- [data-fetching.md](data-fetching.md) - TanStack Query 优化
- [complete-examples.md](complete-examples.md) - 实际场景中的性能模式
