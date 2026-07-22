---
name: react-component-performance
description: 诊断 React 组件性能瓶颈并提供针对性优化建议。触发词：React性能、组件优化、re-render、渲染优化、性能分析、memo、useCallback、useMemo、列表性能、虚拟化
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# React 组件性能优化

## 概述

定位渲染热点，隔离高开销更新，在不改变 UI 行为的前提下实施针对性优化。

## 使用场景
- 用户要求对某个慢组件进行性能分析或优化。
- 需要减少 React UI 中的重渲染、列表卡顿或高开销渲染操作。

## 工作流程

1. 复现或描述性能瓶颈。
2. 定位触发重渲染的原因（state 更新、props 变化、effect 副作用）。
3. 将高频变化的 state 从重量级子树中隔离出来。
4. 稳定 props 和回调函数；在收益明显处使用 memoization。
5. 减少高开销操作（计算量、DOM 规模、列表长度）。
6. **验证**：打开 React DevTools Profiler → 录制交互过程 → 在 Flamegraph 中检查渲染耗时超过 ~16 ms 的组件 → 与优化前的基线录制进行对比。

## 检查清单

- 度量：使用 React DevTools Profiler 或日志记录渲染次数；捕获基线数据。
- 定位抖动：找出被定时器、滚动、输入或动画驱动的 state 更新。
- 拆分：将高频变化的 state 移入子组件；保持重量级列表为静态。
- Memoize：仅在 props 稳定时用 `memo` 包裹叶子行组件。
- 稳定 props：用 `useCallback`/`useMemo` 处理回调函数和派生值。
- 避免在 render 中做派生计算：提前计算，或在 memoized 辅助函数中完成。
- 控制列表规模：对长列表做窗口化/虚拟化；避免渲染不可见项。
- Keys：确保 key 稳定；顺序可能变化时避免使用 index。
- Effects：检查依赖数组；避免每次渲染都重新执行的 effect。
- 样式/布局：警惕高开销的 layout thrash 或大型 Markdown/diff 渲染。

## 优化模式

### 隔离高频 state

将定时器或动画计数器移入子组件，使父级列表不会因每次 tick 而重渲染。

```tsx
// ❌ Before – entire parent (and list) re-renders every second
function Dashboard({ items }: { items: Item[] }) {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return (
    <>
      <Clock tick={tick} />
      <ExpensiveList items={items} /> {/* re-renders every second */}
    </>
  );
}

// ✅ After – only <Clock> re-renders; list is untouched
function Clock() {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return <span>{tick}s</span>;
}

function Dashboard({ items }: { items: Item[] }) {
  return (
    <>
      <Clock />
      <ExpensiveList items={items} />
    </>
  );
}
```

### 用 `useCallback` + `memo` 稳定回调

```tsx
// ❌ Before – new handler reference on every render busts Row memo
function List({ items }: { items: Item[] }) {
  const handleClick = (id: string) => console.log(id); // new ref each render
  return items.map(item => <Row key={item.id} item={item} onClick={handleClick} />);
}

// ✅ After – stable handler; Row only re-renders when its own item changes
const Row = memo(({ item, onClick }: RowProps) => (
  <li onClick={() => onClick(item.id)}>{item.name}</li>
));

function List({ items }: { items: Item[] }) {
  const handleClick = useCallback((id: string) => console.log(id), []);
  return items.map(item => <Row key={item.id} item={item} onClick={handleClick} />);
}
```

### 在 render 外部处理派生数据

```tsx
// ❌ Before – recomputes on every render
function Summary({ orders }: { orders: Order[] }) {
  const total = orders.reduce((sum, o) => sum + o.amount, 0); // runs every render
  return <p>Total: {total}</p>;
}

// ✅ After – recomputes only when orders changes
function Summary({ orders }: { orders: Order[] }) {
  const total = useMemo(() => orders.reduce((sum, o) => sum + o.amount, 0), [orders]);
  return <p>Total: {total}</p>;
}
```

### 其他模式

- **拆分行组件**：将列表行提取为独立的 memoized 组件，接收窄范围的 props。
- **延迟重量级渲染**：对高开销内容做懒渲染或折叠处理，展开时再渲染。

## 性能分析验证步骤

1. 打开 **React DevTools → Profiler** 标签页。
2. 点击 **Record**，执行慢交互操作，然后点击 **Stop**。
3. 切换到 **Flamegraph** 视图；标注了组件名且耗时 > ~16 ms 的条目即为优化候选。
4. 使用 **Ranked chart** 按自身渲染时间排序，锁定耗时最高的组件。
5. 每次只应用一项优化，重新录制，将渲染次数和耗时与基线进行对比。

## 示例参考

当用户需要具体的重构示例时，加载 `references/examples.md`。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境下的验证、测试或专家评审。
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清。
