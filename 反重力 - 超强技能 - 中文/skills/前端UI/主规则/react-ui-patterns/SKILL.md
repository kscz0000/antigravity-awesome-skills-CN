---
name: react-ui-patterns
description: "React 现代 UI 模式，涵盖加载状态、错误处理和数据获取。适用于构建 UI 组件、处理异步数据或管理 UI 状态。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# React UI 模式

## 核心原则

1. **永远不要展示过时的 UI** - 只在实际加载时才显示加载动画
2. **始终暴露错误** - 用户必须知道何时发生了错误
3. **乐观更新** - 让 UI 感觉即时响应
4. **渐进式展示** - 内容就绪时立即展示
5. **优雅降级** - 部分数据总比没有数据好

## 加载状态模式

### 黄金法则

**只在没有数据可展示时才显示加载指示器。**

```typescript
// 正确 - 只在没有数据时才显示加载
const { data, loading, error } = useGetItemsQuery();

if (error) return <ErrorState error={error} onRetry={refetch} />;
if (loading && !data) return <LoadingState />;
if (!data?.items.length) return <EmptyState />;

return <ItemList items={data.items} />;
```

```typescript
// 错误 - 即使有缓存数据也显示加载动画
if (loading) return <LoadingState />; // 重新获取时会闪烁！
```

### 加载状态决策树

```
是否有错误？
  → 是：显示带重试选项的错误状态
  → 否：继续

是否正在加载且没有数据？
  → 是：显示加载指示器（spinner/skeleton）
  → 否：继续

是否有数据？
  → 是，有数据项：显示数据
  → 是，但为空：显示空状态
  → 否：显示加载（兜底）
```

### Skeleton 与 Spinner 选择指南

| 使用 Skeleton 的场景 | 使用 Spinner 的场景 |
|---------------------|---------------------|
| 内容结构已知 | 内容结构未知 |
| 列表/卡片布局 | 模态框操作 |
| 页面首次加载 | 按钮提交 |
| 内容占位符 | 内联操作 |

## 错误处理模式

### 错误处理层级

```
1. 内联错误（字段级） → 表单验证错误
2. Toast 通知 → 可恢复错误，用户可重试
3. 错误横幅 → 页面级错误，数据仍部分可用
4. 完整错误页面 → 不可恢复，需要用户操作
```

### 始终显示错误

**关键：永远不要静默吞掉错误。**

```typescript
// 正确 - 错误始终暴露给用户
const [createItem, { loading }] = useCreateItemMutation({
  onCompleted: () => {
    toast.success({ title: 'Item created' });
  },
  onError: (error) => {
    console.error('createItem failed:', error);
    toast.error({ title: 'Failed to create item' });
  },
});

// 错误 - 错误被静默捕获，用户毫无察觉
const [createItem] = useCreateItemMutation({
  onError: (error) => {
    console.error(error); // 用户什么都看不到！
  },
});
```

### 错误状态组件模式

```typescript
interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
  title?: string;
}

const ErrorState = ({ error, onRetry, title }: ErrorStateProps) => (
  <div className="error-state">
    <Icon name="exclamation-circle" />
    <h3>{title ?? 'Something went wrong'}</h3>
    <p>{error.message}</p>
    {onRetry && (
      <Button onClick={onRetry}>Try Again</Button>
    )}
  </div>
);
```

## 按钮状态模式

### 按钮加载状态

```tsx
<Button
  onClick={handleSubmit}
  isLoading={isSubmitting}
  disabled={!isValid || isSubmitting}
>
  Submit
</Button>
```

### 操作期间禁用

**关键：异步操作期间始终禁用触发器。**

```tsx
// 正确 - 加载时按钮禁用
<Button
  disabled={isSubmitting}
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Submit
</Button>

// 错误 - 用户可以多次点击
<Button onClick={handleSubmit}>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</Button>
```

## 空状态

### 空状态要求

每个列表/集合都必须有空状态：

```tsx
// 错误 - 没有空状态
return <FlatList data={items} />;

// 正确 - 显式空状态
return (
  <FlatList
    data={items}
    ListEmptyComponent={<EmptyState />}
  />
);
```

### 上下文空状态

```tsx
// 搜索无结果
<EmptyState
  icon="search"
  title="No results found"
  description="Try different search terms"
/>

// 列表暂无数据
<EmptyState
  icon="plus-circle"
  title="No items yet"
  description="Create your first item"
  action={{ label: 'Create Item', onClick: handleCreate }}
/>
```

## 表单提交模式

```tsx
const MyForm = () => {
  const [submit, { loading }] = useSubmitMutation({
    onCompleted: handleSuccess,
    onError: handleError,
  });

  const handleSubmit = async () => {
    if (!isValid) {
      toast.error({ title: 'Please fix errors' });
      return;
    }
    await submit({ variables: { input: values } });
  };

  return (
    <form>
      <Input
        value={values.name}
        onChange={handleChange('name')}
        error={touched.name ? errors.name : undefined}
      />
      <Button
        type="submit"
        onClick={handleSubmit}
        disabled={!isValid || loading}
        isLoading={loading}
      >
        Submit
      </Button>
    </form>
  );
};
```

## 反模式

### 加载状态

```typescript
// 错误 - 有数据时显示加载动画（导致闪烁）
if (loading) return <Spinner />;

// 正确 - 只在没有数据时才显示加载
if (loading && !data) return <Spinner />;
```

### 错误处理

```typescript
// 错误 - 错误被吞掉
try {
  await mutation();
} catch (e) {
  console.log(e); // 用户毫不知情！
}

// 正确 - 错误暴露
onError: (error) => {
  console.error('operation failed:', error);
  toast.error({ title: 'Operation failed' });
}
```

### 按钮状态

```typescript
// 错误 - 提交时按钮未禁用
<Button onClick={submit}>Submit</Button>

// 正确 - 禁用并显示加载
<Button onClick={submit} disabled={loading} isLoading={loading}>
  Submit
</Button>
```

## 检查清单

完成任何 UI 组件前：

**UI 状态：**
- [ ] 错误状态已处理并展示给用户
- [ ] 加载状态仅在无数据时显示
- [ ] 集合提供了空状态
- [ ] 异步操作期间按钮已禁用
- [ ] 按钮在适当时显示加载指示器

**数据与变更：**
- [ ] 变更操作有 onError 处理
- [ ] 所有用户操作都有反馈（toast/视觉）

## 与其他技能的集成

- **graphql-schema**: 使用变更模式配合正确的错误处理
- **testing-patterns**: 测试所有 UI 状态（加载、错误、空、成功）
- **formik-patterns**: 应用表单提交模式

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
