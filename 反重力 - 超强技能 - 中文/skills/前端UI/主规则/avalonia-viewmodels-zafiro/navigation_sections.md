# 导航与区块

Zafiro 提供了强大的抽象，用于管理应用程序范围的导航和模块化 UI 区块。

## 使用 INavigator 导航

`INavigator` 接口用于在不同的 view 或 viewmodel 之间切换。

```csharp
public class MyViewModel(INavigator navigator)
{
    public async Task GoToDetails()
    {
        await navigator.Navigate(() => new DetailsViewModel());
    }
}
```

## UI 区块

区块是 UI 的模块化部分（如选项卡或侧边栏项），可以自动注册。

### [Section] 属性

打算作为区块的 ViewModel 应使用 `[Section]` 属性标记。

```csharp
[Section("Wallet", icon: "fa-wallet")]
public class WalletSectionViewModel : IWalletSectionViewModel
{
    // ...
}
```

### 自动注册

在 `CompositionRoot` 中，区块可以自动注册：

```csharp
services.AddAnnotatedSections(logger);
services.AddSectionsFromAttributes(logger);
```

### 切换区块

可以通过 `IShellViewModel` 切换当前活动区块：

```csharp
shellViewModel.SetSection("Browse");
```

> [!IMPORTANT]
> `[Section]` 属性中的 `icon` 参数支持 FontAwesome 图标（如 `fa-home`），需要配置 `ProjektankerIconControlProvider`。
