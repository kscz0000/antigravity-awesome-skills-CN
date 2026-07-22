# 语义容器

为数据类型选择合适的容器可以简化 XAML 并提高可维护性。`Zafiro.Avalonia` 为常见布局模式提供了专用控件。

## 📦 HeaderedContainer

当区块需要标题或头部时，优先使用 `HeaderedContainer` 而非 `Border` 或 `Grid`。

```xml
<HeaderedContainer Header="Security Settings" Classes="WizardSection">
    <StackPanel>
        <!-- 内容放在这里 -->
    </StackPanel>
</HeaderedContainer>
```

### 关键属性：
- `Header`：头部的内容或字符串。
- `HeaderBackground`：头部区域的画笔。
- `ContentPadding`：内容区域的内边距。

## ↔️ EdgePanel

使用 `EdgePanel` 将元素定位在容器边缘，无需复杂的 `Grid` 定义。

```xml
<EdgePanel StartContent="{Icon fa-wallet}" 
           Content="Wallet Balance" 
           EndContent="$1,234.00" />
```

### 插槽：
- `StartContent`：左对齐（或起始位置）。
- `Content`：填充中间剩余空间。
- `EndContent`：右对齐（或结束位置）。

## 📇 Card

用于分组相关信息的简单容器，通常在 `HeaderedContainer` 内部使用或作为列表中的独立元素。

```xml
<Card Header="Enter recipient address:">
    <TextBox Text="{Binding Address}" />
</Card>
```

## 📐 最佳实践

- 使用 `Classes` 应用主题变体（例如 `Classes="Section"`、`Classes="Highlight"`）。
- 必要时在样式中使用模板自定义容器的内部部件，而不是嵌套更多控件。
