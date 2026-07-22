# 示例

## 将定时器从长列表中隔离

**场景：** 消息列表每秒重新渲染，因为定时器（`elapsedMs`）位于父组件中。这会在大型列表上造成明显的卡顿。

**目标：** 保持 UI 不变，但将重新渲染限制在定时器区域。

**优化前（有问题的模式）：**

```tsx
function Messages({ items, isThinking, processingStartedAt }) {
  const [elapsedMs, setElapsedMs] = useState(0);

  useEffect(() => {
    if (!isThinking || !processingStartedAt) {
      setElapsedMs(0);
      return;
    }
    setElapsedMs(Date.now() - processingStartedAt);
    const interval = window.setInterval(() => {
      setElapsedMs(Date.now() - processingStartedAt);
    }, 1000);
    return () => window.clearInterval(interval);
  }, [isThinking, processingStartedAt]);

  return (
    <div>
      {items.map((item) => (
        <MessageRow key={item.id} item={item} />
      ))}
      <div>{formatDurationMs(elapsedMs)}</div>
    </div>
  );
}
```

**优化后（隔离定时状态）：**

```tsx
type WorkingIndicatorProps = {
  isThinking: boolean;
  processingStartedAt?: number | null;
};

const WorkingIndicator = memo(function WorkingIndicator({
  isThinking,
  processingStartedAt = null,
}: WorkingIndicatorProps) {
  const [elapsedMs, setElapsedMs] = useState(0);

  useEffect(() => {
    if (!isThinking || !processingStartedAt) {
      setElapsedMs(0);
      return;
    }
    setElapsedMs(Date.now() - processingStartedAt);
    const interval = window.setInterval(() => {
      setElapsedMs(Date.now() - processingStartedAt);
    }, 1000);
    return () => window.clearInterval(interval);
  }, [isThinking, processingStartedAt]);

  return <div>{formatDurationMs(elapsedMs)}</div>;
});

function Messages({ items, isThinking, processingStartedAt }) {
  return (
    <div>
      {items.map((item) => (
        <MessageRow key={item.id} item={item} />
      ))}
      <WorkingIndicator
        isThinking={isThinking}
        processingStartedAt={processingStartedAt}
      />
    </div>
  );
}
```

**原理说明：** 只有 `WorkingIndicator` 子树每秒重新渲染。列表在 props 不变时保持稳定。

**可选的后续优化：**

- 如果 props 稳定，用 `memo` 包裹 `MessageRow`。
- 对传递给行的处理函数使用 `useCallback` 以避免不必要的重新渲染。
- 如果列表非常大，考虑使用列表虚拟化。
