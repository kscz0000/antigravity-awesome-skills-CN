# ViewModel 与命令

在基于 Zafiro 的应用程序中，ViewModel 应该是函数式的、响应式的且具有弹性。

## 响应式 ViewModel

使用 `ReactiveObject` 作为基类。属性应使用 `[Reactive]` 属性（来自 ReactiveUI.SourceGenerators）定义，以保持简洁。

```csharp
public partial class MyViewModel : ReactiveObject
{
    [Reactive] private string name;
    [Reactive] private bool isBusy;
}
```

### 观察与转换

使用 `WhenAnyValue` 响应属性变化：

```csharp
this.WhenAnyValue(x => x.Name)
    .Select(name => !string.IsNullOrEmpty(name))
    .ToPropertyEx(this, x => x.CanSubmit);
```

## 增强命令

Zafiro 使用 `IEnhancedCommand`，它扩展了 `ICommand` 和 `IReactiveCommand`，增加了 `Name` 和 `Text` 等额外元数据。

### 创建命令

使用 `ReactiveCommand.Create` 或 `ReactiveCommand.CreateFromTask`，然后调用 `Enhance()`。

```csharp
public IEnhancedCommand Submit { get; }

public MyViewModel()
{
    Submit = ReactiveCommand.CreateFromTask(OnSubmit, canSubmit)
        .Enhance(text: "Submit Data", name: "SubmitCommand");
}
```

### 错误处理

使用 `HandleErrorsWith` 自动将命令错误传递到 `NotificationService`。

```csharp
Submit.HandleErrorsWith(uiServices.NotificationService, "Submission Failed")
    .DisposeWith(disposable);
```

## 可释放对象

始终使用 `CompositeDisposable` 管理订阅和命令生命周期。

```csharp
public class MyViewModel : ReactiveObject, IDisposable
{
    private readonly CompositeDisposable disposables = new();

    public void Dispose() => disposables.Dispose();
}
```

> [!TIP]
> 在任何可观察订阅或命令上使用 `.DisposeWith(disposables)` 以确保正确清理。
