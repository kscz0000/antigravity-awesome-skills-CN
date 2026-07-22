---
name: graphql-schema
description: GraphQL 查询、变更与代码生成模式。用于创建 GraphQL 操作、使用 Apollo Client 或生成类型时。触发词：GraphQL、Apollo、gql、codegen、代码生成、查询、变更、mutation、schema、类型生成、useQuery、useMutation。
risk: unknown
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/graphql-schema
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# GraphQL Schema 模式
## 何时使用

当你需要 GraphQL 查询、变更和代码生成模式时使用此技能。用于创建 GraphQL 操作、使用 Apollo Client 或生成类型时。


## 核心规则

1. **永远不要内联 `gql` 字面量** —— 创建 `.gql` 文件
2. **在创建/修改 `.gql` 文件后必须运行 codegen**
3. **必须为 mutation 添加 `onError` 处理函数**
4. **使用生成的 hooks** —— 永远不要手写原始的 Apollo hooks

## 文件结构

```
src/
├── components/
│   └── ItemList/
│       ├── ItemList.tsx
│       ├── GetItems.gql           # Query definition
│       └── GetItems.generated.ts  # Auto-generated (don't edit)
└── graphql/
    └── mutations/
        └── CreateItem.gql         # Shared mutations
```

## 创建 Query

### 步骤 1：创建 .gql 文件

```graphql
# src/components/ItemList/GetItems.gql
query GetItems($limit: Int, $offset: Int) {
  items(limit: $limit, offset: $offset) {
    id
    name
    description
    createdAt
  }
}
```

### 步骤 2：运行 codegen

```bash
npm run gql:typegen
```

### 步骤 3：导入并使用生成的 hook

```typescript
import { useGetItemsQuery } from './GetItems.generated';

const ItemList = () => {
  const { data, loading, error, refetch } = useGetItemsQuery({
    variables: { limit: 20, offset: 0 },
  });

  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (loading && !data) return <LoadingSkeleton />;
  if (!data?.items.length) return <EmptyState />;

  return <List items={data.items} />;
};
```

## 创建 Mutation

### 步骤 1：创建 .gql 文件

```graphql
# src/graphql/mutations/CreateItem.gql
mutation CreateItem($input: CreateItemInput!) {
  createItem(input: $input) {
    id
    name
    description
  }
}
```

### 步骤 2：运行 codegen

```bash
npm run gql:typegen
```

### 步骤 3：搭配必需的错误处理一起使用

```typescript
import { useCreateItemMutation } from 'graphql/mutations/CreateItem.generated';

const CreateItemForm = () => {
  const [createItem, { loading }] = useCreateItemMutation({
    // Success handling
    onCompleted: (data) => {
      toast.success({ title: 'Item created' });
      navigation.goBack();
    },
    // ERROR HANDLING IS REQUIRED
    onError: (error) => {
      console.error('createItem failed:', error);
      toast.error({ title: 'Failed to create item' });
    },
    // Cache update
    update: (cache, { data }) => {
      if (data?.createItem) {
        cache.modify({
          fields: {
            items: (existing = []) => [...existing, data.createItem],
          },
        });
      }
    },
  });

  return (
    <Button
      onPress={() => createItem({ variables: { input: formValues } })}
      isDisabled={!isValid || loading}
      isLoading={loading}
    >
      Create
    </Button>
  );
};
```

## Mutation 的 UI 要求

**关键：每个 mutation 触发器都必须：**

1. **在 mutation 期间被禁用** —— 防止重复点击
2. **展示 loading 状态** —— 提供视觉反馈
3. **包含 onError 处理函数** —— 让用户知道操作失败
4. **展示成功反馈** —— 让用户知道操作成功

```typescript
// CORRECT - Complete mutation pattern
const [submit, { loading }] = useSubmitMutation({
  onError: (error) => {
    console.error('submit failed:', error);
    toast.error({ title: 'Save failed' });
  },
  onCompleted: () => {
    toast.success({ title: 'Saved' });
  },
});

<Button
  onPress={handleSubmit}
  isDisabled={!isValid || loading}
  isLoading={loading}
>
  Submit
</Button>
```

## Query 选项

### Fetch 策略

| 策略 | 使用场景 |
|--------|----------|
| `cache-first` | 数据很少变化 |
| `cache-and-network` | 既要快速又要新鲜（默认） |
| `network-only` | 始终需要最新数据 |
| `no-cache` | 从不缓存（少见） |

### 常用选项

```typescript
useGetItemsQuery({
  variables: { id: itemId },

  // Fetch strategy
  fetchPolicy: 'cache-and-network',

  // Re-render on network status changes
  notifyOnNetworkStatusChange: true,

  // Skip if condition not met
  skip: !itemId,

  // Poll for updates
  pollInterval: 30000,
});
```

## 乐观更新

用于即时 UI 反馈：

```typescript
const [toggleFavorite] = useToggleFavoriteMutation({
  optimisticResponse: {
    toggleFavorite: {
      __typename: 'Item',
      id: itemId,
      isFavorite: !currentState,
    },
  },
  onError: (error) => {
    // Rollback happens automatically
    console.error('toggleFavorite failed:', error);
    toast.error({ title: 'Failed to update' });
  },
});
```

### 何时不要使用乐观更新

- 可能校验失败的操作
- 带有服务器生成值的操作
- 破坏性操作（删除）
- 会影响其他用户的操作

## Fragments

用于可复用的字段选择：

```graphql
# src/graphql/fragments/ItemFields.gql
fragment ItemFields on Item {
  id
  name
  description
  createdAt
  updatedAt
}
```

在 query 中使用：

```graphql
query GetItems {
  items {
    ...ItemFields
  }
}
```

## 反模式

```typescript
// WRONG - Inline gql
const GET_ITEMS = gql`
  query GetItems { items { id } }
`;

// CORRECT - Use .gql file + generated hook
import { useGetItemsQuery } from './GetItems.generated';


// WRONG - No error handler
const [mutate] = useMutation(MUTATION);

// CORRECT - Always handle errors
const [mutate] = useMutation(MUTATION, {
  onError: (error) => {
    console.error('mutation failed:', error);
    toast.error({ title: 'Operation failed' });
  },
});


// WRONG - Button not disabled during mutation
<Button onPress={submit}>Submit</Button>

// CORRECT - Disabled and loading
<Button onPress={submit} isDisabled={loading} isLoading={loading}>
  Submit
</Button>
```

## Codegen 命令

```bash
# Generate types from .gql files
npm run gql:typegen

# Download schema + generate types
npm run sync-types
```

## 与其他技能的集成

- **react-ui-patterns**：Query 的 loading/error/empty 状态
- **testing-patterns**：在测试中 mock 生成的 hooks
- **formik-patterns**：Mutation 提交模式

## 使用限制

- 仅当任务明确匹配其上游来源和本地项目上下文时才使用此技能。
- 在应用更改前，请验证命令、生成的代码、依赖项、凭据以及外部服务的行为。
- 不要将示例视为针对特定环境的测试、安全审查或用户对破坏性或高成本操作的批准的替代品。