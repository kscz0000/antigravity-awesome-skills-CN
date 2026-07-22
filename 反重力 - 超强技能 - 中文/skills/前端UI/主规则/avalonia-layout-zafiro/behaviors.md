# 交互与逻辑

为了保持 XAML 简洁和可维护，应尽量减少视图中的逻辑，避免过度使用转换器。

## 🎭 Xaml.Interaction.Behaviors

使用 `Interaction.Behaviors` 处理不属于 ViewModel 的 UI 相关逻辑，例如焦点管理、动画或特殊事件处理。

```xml
<TextBox Text="{Binding Address}">
    <Interaction.Behaviors>
        <UntouchedClassBehavior />
    </Interaction.Behaviors>
</TextBox>
```

### 为什么要使用行为？
- **封装**：UI 逻辑封装在可复用的行为类中。
- **简洁的 XAML**：避免代码隐藏和复杂的 XAML 触发器。
- **可测试性**：行为可以独立于视图进行测试。

## 🚫 避免使用转换器

转换器往往导致"魔法"逻辑隐藏在 XAML 中。尽可能优先选择：

1.  **ViewModel 属性**：让 ViewModel 提供最终的数据格式（例如，格式化为显示用的 `string`）。
2.  **MultiBinding**：直接在 XAML 中进行简单的逻辑组合（与/或）。
3.  **行为**：用于涉及状态或事件的更复杂交互。

### 何时使用转换器？
仅当转换纯粹是视觉性的且在不同上下文中高度可复用时才使用（例如 `BoolToOpacityConverter`）。

## 🧩 简化交互

如果你发现自己需要一个复杂的转换器或行为，请考虑是否可以简化组件，或者调整数据模型使视图绑定更加直接。
