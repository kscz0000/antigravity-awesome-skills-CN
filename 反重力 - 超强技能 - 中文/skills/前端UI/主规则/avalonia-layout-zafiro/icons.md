# 图标使用

`Zafiro.Avalonia` 通过专用的标记扩展和样式选项简化了图标管理。

## 🛠️ IconExtension

使用 `{Icon}` 标记扩展轻松包含来自 FontAwesome 等库的图标。

```xml
<!-- 位置参数 -->
<Button Content="{Icon fa-wallet}" />

<!-- 命名参数 -->
<ContentControl Content="{Icon Source=fa-gear}" />
```

## 🎨 IconOptions

`IconOptions` 允许你自定义图标，而无需手动将其包装在其他控件中。它通常在样式中使用以提供一致的外观。

```xml
<Style Selector="HeaderedContainer /template/ ContentPresenter#Header EdgePanel /template/ ContentControl#StartContent">
    <Setter Property="IconOptions.Size" Value="20" />
    <Setter Property="IconOptions.Fill" Value="{DynamicResource Accent}" />
    <Setter Property="IconOptions.Padding" Value="10" />
    <Setter Property="IconOptions.CornerRadius" Value="10" />
</Style>
```

### 常用属性：
- `IconOptions.Size`：设置图标的宽度和高度。
- `IconOptions.Fill`：图标的颜色/画笔。
- `IconOptions.Background`：图标容器的背景画笔。
- `IconOptions.Padding`：图标容器内的内边距。
- `IconOptions.CornerRadius`：使用背景时的圆角半径。

## 📁 共享图标资源

将图标定义为资源以便在应用程序中复用。

```xml
<ResourceDictionary xmlns="https://github.com/avaloniaui">
    <Icon x:Key="fa-wallet" Source="fa-wallet" />
</ResourceDictionary>
```

然后使用 `StaticResource` 引用已定义的图标：

```xml
<Button Content="{StaticResource fa-wallet}" />
```

不过，`{Icon ...}` 扩展通常更受欢迎，因为它简洁且能够即时创建新的图标实例。
