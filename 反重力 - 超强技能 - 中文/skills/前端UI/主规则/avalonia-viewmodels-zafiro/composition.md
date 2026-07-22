# 组合与映射

确保 ViewModel 正确实例化并映射到对应的 View，对于可维护的应用程序至关重要。

## ViewModel 到 View 的映射

Zafiro 使用 `DataTypeViewLocator` 根据数据类型自动将 ViewModel 映射到 View。

### 在 App.axaml 中集成

在应用程序的数据模板中注册 `DataTypeViewLocator`：

```xml
<Application.DataTemplates>
    <DataTypeViewLocator />
    <DataTemplateInclude Source="avares://Zafiro.Avalonia/DataTemplates.axaml" />
</Application.DataTemplates>
```

### 注册

映射可以全局或局部注册。Zafiro 项目的常见做法是使用命名约定或源生成器进行的显式注册。

## 组合根

使用集中的 `CompositionRoot` 管理依赖注入和服务注册。

```csharp
public static class CompositionRoot
{
    public static IShellViewModel CreateMainViewModel(Control topLevelView)
    {
        var services = new ServiceCollection();
        
        services
            .AddViewModels()
            .AddUIServices(topLevelView);
            
        var serviceProvider = services.BuildServiceProvider();
        return serviceProvider.GetRequiredService<IShellViewModel>();
    }
}
```

### 注册 ViewModel

使用适当的作用域（Transient、Scoped 或 Singleton）注册 ViewModel。

```csharp
public static IServiceCollection AddViewModels(this IServiceCollection services)
{
    return services
        .AddTransient<IHomeSectionViewModel, HomeSectionSectionViewModel>()
        .AddSingleton<IShellViewModel, ShellViewModel>();
}
```

## View 注入

使用 `Connect` 辅助方法（如果可用）或在 `OnFrameworkInitializationCompleted` 中手动实例化：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    this.Connect(
        () => new ShellView(),
        view => CompositionRoot.CreateMainViewModel(view),
        () => new MainWindow());

    base.OnFrameworkInitializationCompleted();
}
```

> [!TIP]
> 当你需要手动实例化类，同时仍从 `IServiceProvider` 解析其依赖项时，使用 `ActivatorUtilities.CreateInstance`。
