# Avalonia、Zafiro 与响应式规则

## Avalonia UI 规则

- **严格 Avalonia**：永远不要使用 `System.Drawing`；始终使用 Avalonia 类型。
- **纯 ViewModel**：ViewModel **绝不能**引用 Avalonia 类型。
- **绑定优于代码后置**：逻辑应由绑定驱动。
- **DataTemplates**：优先使用显式 `DataTemplate` 和类型化的 `DataContext`。
- **VisualStates**：除非绝对必要，否则避免使用 `VisualStates`。

## Zafiro 指南

- **优先抽象**：在重新实现逻辑之前，始终查找现有的 Zafiro 辅助工具、扩展方法和抽象。
- **验证**：使用 Zafiro 的 `ValidationRule` 和验证扩展，而不是临时性的响应式逻辑。

## DynamicData 与响应式规则

### 强制方法

- **操作符偏好**：在处理集合时，始终优先使用 **DynamicData** 操作符（`Connect`、`Filter`、`Transform`、`Sort`、`Bind`、`DisposeMany`）而非普通 Rx 操作符。
- **可读管道**：将管道构建和维护为单一、可读的链式调用。
- **生命周期**：使用 `DisposeWith` 进行生命周期管理。
- **最小订阅**：订阅应最小化、集中化，且仅用于副作用。

### 禁止的反模式

- **临时数据源**：不要为局部问题临时创建新的 `SourceList` / `SourceCache`。
- **Subscribe 中的逻辑**：不要在 `Subscribe` 中放置业务逻辑。
- **操作符不匹配**：如果存在 DynamicData 等效操作符，不要使用 `System.Reactive` 操作符。

### 规范模式

**动态集合验证：**
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

**过滤空值：**
在响应式管道中使用 `WhereNotNull()`。
```csharp
this.WhenAnyValue(x => x.DurationPreset).WhereNotNull()
```
