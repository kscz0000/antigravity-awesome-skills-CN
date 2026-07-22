---
title: Reanimated 共享值使用 .get() 和 .set()（而非 .value）
impact: LOW
impactDescription: React Compiler 兼容性所必需
tags: reanimated, react-compiler, shared-values
---

## React Compiler 下共享值应使用 .get() 和 .set()

启用 React Compiler 后，使用 `.get()` 和 `.set()` 代替直接读写 Reanimated 共享值的 `.value`。编译器无法追踪属性访问——显式方法能确保正确行为。直接读写 `.value` 会导致编译器退出优化，降低性能。

**核心原因**：React Compiler 通过分析函数调用来追踪数据流。`.value` 是属性访问，编译器无法感知其变化；而 `.get()` 和 `.set()` 是显式的方法调用，编译器可以正确追踪。

**错误（与 React Compiler 不兼容）：**

以下代码直接读写 `.value`，会导致 React Compiler 无法追踪共享值的变化，从而退出编译优化：

```tsx
import { useSharedValue } from 'react-native-reanimated'

function Counter() {
  const count = useSharedValue(0)

  const increment = () => {
    count.value = count.value + 1 // opts out of react compiler
  }

  return <Button onPress={increment} title={`Count: ${count.value}`} />
}
```

**正确（兼容 React Compiler）：**

使用 `.get()` 读取和 `.set()` 写入，编译器可以正确追踪调用：

```tsx
import { useSharedValue } from 'react-native-reanimated'

function Counter() {
  const count = useSharedValue(0)

  const increment = () => {
    count.set(count.get() + 1)
  }

  return <Button onPress={increment} title={`Count: ${count.get()}`} />
}
```

详见
[Reanimated 文档](https://docs.swmansion.com/react-native-reanimated/docs/core/useSharedValue/#react-compiler-support)。
此规则仅在使用 React Compiler 时需要遵守。若未启用编译器，使用 `.value` 仍然正确。

**总结**：启用 React Compiler 时，将 `count.value` 替换为 `count.get()` 读取、`count.set()` 写入，即可保持编译器优化生效。