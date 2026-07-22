---
title: 策略性 Suspense 边界
impact: HIGH
impactDescription: 更快的首次渲染
tags: async, suspense, streaming, layout-shift
---

## 策略性 Suspense 边界

不要在 async 组件中 await 数据后再返回 JSX，而是使用 Suspense 边界在数据加载时更快地展示外壳 UI。

**错误写法（外壳被数据获取阻塞）：**

```tsx
async function Page() {
  const data = await fetchData() // 阻塞整个页面
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

整个布局都在等待数据，即使只有中间部分需要它。

**正确写法（外壳立即显示，数据流入）：**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // 仅阻塞此组件
  return <div>{data.content}</div>
}
```

Sidebar、Header 和 Footer 会立即渲染。只有 DataDisplay 等待数据。

**替代方案（跨组件共享 promise）：**

```tsx
function Page() {
  // 立即启动获取，但不 await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 解包 promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 复用同一个 promise
  return <div>{data.summary}</div>
}
```

两个组件共享同一个 promise，因此只会发起一次请求。布局立即渲染，同时两个组件一起等待。

**不适用此模式的场景：**

- 影响布局定位的关键数据
- 首屏以上的 SEO 关键内容
- 小型快速查询，suspense 开销不值得
- 需要避免布局偏移（加载 → 内容跳动）

**权衡：** 更快的首次渲染 vs 潜在的布局偏移。根据你的 UX 优先级做出选择。
