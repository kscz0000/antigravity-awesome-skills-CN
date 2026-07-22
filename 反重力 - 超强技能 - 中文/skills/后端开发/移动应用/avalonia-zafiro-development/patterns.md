# Angor/Zafiro 中的常见模式

## 可刷新集合

`RefreshableCollection` 模式用于管理可通过命令刷新的列表，维护内部的 `SourceCache`/`SourceList` 并暴露 `ReadOnlyObservableCollection`。

### 实现

```csharp
var refresher = RefreshableCollection.Create(
        () => GetDataTask(), 
        model => model.Id)
    .DisposeWith(disposable);

LoadData = refresher.Refresh;
Items = refresher.Items;
```

### 优势
- **自动加载**：处理命令执行和结果。
- **高效更新**：内部使用 `EditDiff` 更新项目而无需清空列表。
- **UI 友好**：将 `Items` 暴露为适合绑定的 `ReadOnlyObservableCollection`。

## 强制验证模式

验证动态集合时，始终使用 Zafiro 验证扩展：

```csharp
this.ValidationRule(
        StagesSource
            .Connect()
            .FilterOnObservable(stage => stage.IsValid)
            .IsEmpty(),
        b => !b,
        _ => "Stages are not valid")
    .DisposeWith(Disposables);
```

## 错误处理管道

不要使用手动的 `Subscribe`，而是使用 `HandleErrorsWith` 将错误直接传递给用户：

```csharp
LoadProjects.HandleErrorsWith(uiServices.NotificationService, "Could not load projects");
```
