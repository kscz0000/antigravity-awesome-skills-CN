# 构建通用组件

通过将视图分解为通用、可复用的组件来减少嵌套和复杂度。

## 🧊 通用组件

不要构建大型、复杂的视图，而是将重复模式提取为小型 `UserControl`。

### 示例：通用的"摘要项"
不要重复使用带有标签和值的 `Grid`：

```xml
<!-- ❌ 错误：重复的 Grid -->
<Grid ColumnDefinitions="*,Auto">
   <TextBlock Text="Total:" />
   <TextBlock Grid.Column="1" Text="{Binding Total}" />
</Grid>
```

创建一个通用组件（或使用带样式的 `EdgePanel`）：

```xml
<!-- ✅ 正确：使用专用控件或样式 -->
<EdgePanel StartContent="Total:" EndContent="{Binding Total}" Classes="SummaryItem" />
```

## 📉 扁平化布局

避免深度嵌套。深度嵌套的 XAML 难以阅读且可能影响性能。

- **StackPanel vs Grid**：对于简单的线性布局使用 `StackPanel`（配合 `Spacing`）。
- **EdgePanel**：非常适合"标签 - 值"或"图标 - 文本 - 操作"行。
- **UniformGrid**：用于所有单元格大小相同的网格。

## 🔧 组件粒度

- **原子级**：小型控件，如自定义按钮或图标。
- **分子级**：原子组合，如带有特定内容的 `HeaderedContainer`。
- **有机体级**：页面的更高级别区块。

目标是创建足够通用以复用，但又足够具体以显著简化父视图的组件。
