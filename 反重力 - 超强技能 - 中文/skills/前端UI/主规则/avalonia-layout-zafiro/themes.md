# 主题组织与共享样式

高效的主题组织是避免 XAML 冗余和确保视觉一致性的关键。

## 🏗️ 结构

遵循 Angor 项目的模式：

1.  **颜色与画笔**：在专用的 `Colors.axaml` 中定义。使用 `DynamicResource` 支持主题切换。
2.  **样式**：按类别分组样式（例如 `Buttons.axaml`、`Containers.axaml`、`Typography.axaml`）。
3.  **应用级主题**：在主 `Theme.axaml` 中聚合所有样式。

## 🎨 避免冗余

不要直接在元素上设置属性：

```xml
<!-- ❌ 错误：冗余属性 -->
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />

<!-- ✅ 正确：使用 Classes 和 Styles -->
<HeaderedContainer Classes="BlueSection" />
<HeaderedContainer Classes="BlueSection" />
```

在共享的 `axaml` 文件中定义样式：

```xml
<Style Selector="HeaderedContainer.BlueSection">
    <Setter Property="CornerRadius" Value="10" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="BorderBrush" Value="{DynamicResource Accent}" />
    <Setter Property="Background" Value="{DynamicResource SurfaceSubtle}" />
</Style>
```

## 🧩 共享图标和资源

将图标定义和其他共享资源集中在 `Icons.axaml` 中，并在主题或 `App.axaml` 的 `MergedDictionaries` 中引入。

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <MergeResourceInclude Source="UI/Themes/Styles/Containers.axaml" />
            <MergeResourceInclude Source="UI/Shared/Resources/Icons.axaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```
