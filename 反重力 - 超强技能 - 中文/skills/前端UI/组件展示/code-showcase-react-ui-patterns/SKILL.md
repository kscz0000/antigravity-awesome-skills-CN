---
name: code-showcase-react-ui-patterns
description: 现代 React UI 模式，涵盖加载状态、错误处理与数据获取。用于构建 UI 组件、处理异步数据或管理 UI 状态时。触发词：React UI 模式、加载状态、错误处理、数据获取、UI 状态、loading state、error handling、data fetching、React 组件、异步数据。
risk: unknown
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/react-ui-patterns
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# React UI 模式
## 使用场景

当你需要使用现代 React UI 模式处理加载状态、错误处理和数据获取时，请使用此技能。也可在构建 UI 组件、处理异步数据或管理 UI 状态时使用。


## 核心原则

1. **绝不展示过期的 UI** — 仅在实际加载时才显示加载动画
2. **始终暴露错误** — 用户必须知道何时发生失败
3. **乐观更新** — 让 UI 感觉即时响应
4. **渐进式展示** — 随着数据就绪逐步显示内容
5. **优雅降级** — 部分数据优于无数据

## 加载状态模式

### 黄金法则

**仅在没有数据可显示时才展示加载指示器。**

```typescript
// 正确 - 仅在没有数据时显示加载状态
const { data, loading, error } = useGetItemsQuery();

if (error) return <ErrorState error={error} onRetry={refetch} />;
if (loading && !data) return <LoadingState />;
if (!data?.items.length) return <EmptyState />;

return <ItemList items={data.items} />;
```

```typescript
// 错误 - 即使有缓存数据也显示旋转动画
if (loading) return <LoadingState />; // 重新获取时会闪烁！
```

### 加载状态决策树

```
是否存在错误？
  → 是：显示错误状态并提供重试选项
  → 否：继续

是否正在加载且没有数据？
  → 是：显示加载指示器（旋转/骨架屏）
  → 否：继续

是否有数据？
  → 有，且有内容：展示数据
  → 有，但为空：显示空状态
  → 没有：显示加载状态（兜底）
```

### 骨架屏 vs 旋转动画

| 使用骨架屏的场景 | 使用旋转动画的场景 |
|-------------------|------------------|
| 内容结构已知 | 内容结构未知 |
| 列表/卡片布局 | 模态框操作 |
| 首次页面加载 | 按钮提交 |
| 内容占位符 | 内联操作 |

## 错误处理模式

### 错误处理层级

```
1. 内联错误（字段级）→ 表单验证错误
2. Toast 通知 → 可恢复错误，用户可重试
3. 错误横幅 → 页面级错误，数据仍可部分使用
4. 完整错误页 → 不可恢复，需要用户操作
```

### 始终显示错误

**关键：绝不能静默吞掉错误。**

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
    console.error(error); // 用户什么也看不到！
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

### 操作期间禁用按钮

**关键：在异步操作期间务必禁用触发按钮。**

```tsx
// 正确 - 加载期间按钮被禁用
<Button
  disabled={isSubmitting}
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Submit
</Button>

// 错误 - 用户可多次点击
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

### 上下文感知的空状态

```tsx
// 搜索无结果
<EmptyState
  icon="search"
  title="No results found"
  description="Try different search terms"
/>

// 列表尚无项目
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
// 错误 - 有数据时仍显示旋转动画（导致闪烁）
if (loading) return <Spinner />;

// 正确 - 仅在无数据时显示加载
if (loading && !data) return <Spinner />;
```

### 错误处理

```typescript
// 错误 - 错误被吞掉
try {
  await mutation();
} catch (e) {
  console.log(e); // 用户毫无察觉！
}

// 正确 - 错误被暴露
onError: (error) => {
  console.error('operation failed:', error);
  toast.error({ title: 'Operation failed' });
}
```

### 按钮状态

```typescript
// 错误 - 提交期间按钮未被禁用
<Button onClick={submit}>Submit</Button>

// 正确 - 禁用并显示加载状态
<Button onClick={submit} disabled={loading} isLoading={loading}>
  Submit
</Button>
```

## 检查清单

在完成任何 UI 组件之前：

**UI 状态：**
- [ ] 错误状态已处理并展示给用户
- [ ] 仅在没有数据时显示加载状态
- [ ] 为集合提供空状态
- [ ] 异步操作期间按钮被禁用
- [ ] 按钮在适当时显示加载指示器

**数据与变更：**
- [ ] 变更操作具有 onError 处理函数
- [ ] 所有用户操作都有反馈（toast/视觉提示）

## 与其他技能的集成

- **graphql-schema**：将变更模式与适当的错误处理结合使用
- **testing-patterns**：测试所有 UI 状态（加载、错误、空、成功）
- **formik-patterns**：应用表单提交模式

## 局限性

- 仅当任务与上游来源及本地项目上下文明确匹配时才使用此技能。
- 在应用更改前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例视为环境特定测试、安全审查或针对破坏性/高成本操作的用户批准之替代品。