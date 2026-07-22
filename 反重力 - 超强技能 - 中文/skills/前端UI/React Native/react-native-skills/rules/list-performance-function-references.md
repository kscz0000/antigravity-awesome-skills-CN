---
title: Optimize List Performance with Stable Object References
impact: CRITICAL
impactDescription: 虚拟化依赖引用稳定性
tags: lists, performance, flatlist, virtualization
---

## 使用稳定对象引用优化列表性能

不要在传递给虚拟化列表之前对数据进行 map 或 filter。虚拟化依赖对象引用稳定性来判断哪些发生了变化——新引用会导致所有可见项的完整重渲染。尽量防止列表父层级的频繁渲染。

需要时，在列表项内使用 context 选择器。

**错误示例（每次击键都创建新的对象引用）：**

```tsx
function DomainSearch() {
  const { keyword, setKeyword } = useKeywordZustandState()
  const { data: tlds } = useTlds()

  // Bad: creates new objects on every render, reparenting the entire list on every keystroke
  const domains = tlds.map((tld) => ({
    domain: `${keyword}.${tld.name}`,
    tld: tld.name,
    price: tld.price,
  }))

  return (
    <>
      <TextInput value={keyword} onChangeText={setKeyword} />
      <LegendList
        data={domains}
        renderItem={({ item }) => <DomainItem item={item} keyword={keyword} />}
      />
    </>
  )
}
```

**正确示例（稳定引用，在列表项内转换）：**

```tsx
const renderItem = ({ item }) => <DomainItem tld={item} />

function DomainSearch() {
  const { data: tlds } = useTlds()

  return (
    <LegendList
      // good: as long as the data is stable, LegendList will not re-render the entire list
      data={tlds}
      renderItem={renderItem}
    />
  )
}

function DomainItem({ tld }: { tld: Tld }) {
  // good: transform within items, and don't pass the dynamic data as a prop
  // good: use a selector function from zustand to receive a stable string back
  const domain = useKeywordZustandState((s) => s.keyword + '.' + tld.name)
  return <Text>{domain}</Text>
}
```

**更新父数组引用：**

创建新的数组实例是可以的，只要其内部对象引用是稳定的。例如，对对象列表排序：

```tsx
// good: creates a new array instance without mutating the inner objects
// good: parent array reference is unaffected by typing and updating "keyword"
const sortedTlds = tlds.toSorted((a, b) => a.name.localeCompare(b.name))

return <LegendList data={sortedTlds} renderItem={renderItem} />
```

虽然这创建了新的数组实例 `sortedTlds`，但内部对象引用是稳定的。

**使用 zustand 处理动态数据（避免父级重渲染）：**

```tsx
const useSearchStore = create<{ keyword: string }>(() => ({ keyword: '' }))

function DomainSearch() {
  const { data: tlds } = useTlds()

  return (
    <>
      <SearchInput />
      <LegendList
        data={tlds}
        // if you aren't using React Compiler, wrap renderItem with useCallback
        renderItem={({ item }) => <DomainItem tld={item} />}
      />
    </>
  )
}

function DomainItem({ tld }: { tld: Tld }) {
  // Select only what you need—component only re-renders when keyword changes
  const keyword = useSearchStore((s) => s.keyword)
  const domain = `${keyword}.${tld.name}`
  return <Text>{domain}</Text>
}
```

虚拟化现在可以在输入时跳过未变化的项。击键时仅重渲染可见项（约 20 个），而非父级。

**在列表项内基于父级数据派生状态（避免父级重渲染）：**

对于数据依赖父级状态的条件组件，这种模式更为重要。例如，检查某个项是否已收藏，如果由项自身访问状态而非父级，则切换收藏只重渲染一个组件：

```tsx
function DomainItemFavoriteButton({ tld }: { tld: Tld }) {
  const isFavorited = useFavoritesStore((s) => s.favorites.has(tld.id))
  return <TldFavoriteButton isFavorited={isFavorited} />
}
```

注意：如果使用 React Compiler，可以直接在列表项内读取 React Context 值。虽然这在大多数情况下比使用 Zustand 选择器稍慢，但影响可能可以忽略。
