# Zafiro 响应式快捷方式

使用这些 Zafiro 扩展方法来替代标准的、更冗长的 Reactive 和 DynamicData 模式。

## 通用 Observable 辅助方法

| 标准模式 | Zafiro 快捷方式 |
| :--- | :--- |
| `Replay(1).RefCount()` | `ReplayLastActive()` |
| `Select(_ => Unit.Default)` | `ToSignal()` |
| `Select(b => !b)` | `Not()` |
| `Where(b => b).ToSignal()` | `Trues()` |
| `Where(b => !b).ToSignal()` | `Falses()` |
| `Select(x => x is null)` | `Null()` |
| `Select(x => x is not null)` | `NotNull()` |
| `Select(string.IsNullOrWhiteSpace)` | `NullOrWhitespace()` |
| `Select(s => !string.IsNullOrWhiteSpace(s))` | `NotNullOrEmpty()` |

## Result 与 Maybe 扩展

| 标准模式 | Zafiro 快捷方式 |
| :--- | :--- |
| `Where(r => r.IsSuccess).Select(r => r.Value)` | `Successes()` |
| `Where(r => r.IsFailure).Select(r => r.Error)` | `Failures()` |
| `Where(m => m.HasValue).Select(m => m.Value)` | `Values()` |
| `Where(m => !m.HasValue).ToSignal()` | `Empties()` |

## 生命周期管理

| 描述 | 方法 |
| :--- | :--- |
| 在发射新项之前释放旧项 | `DisposePrevious()` |
| 在 disposable 内管理生命周期 | `DisposeWith(disposables)` |

## 命令与交互

| 描述 | 方法 |
| :--- | :--- |
| 为 ReactiveCommand 添加元数据/文本 | `Enhance(text, name)` |
| 自动在 UI 中显示错误 | `HandleErrorsWith(notificationService)` |

> [!TIP]
> 在编写自定义 Rx 逻辑之前，始终检查 `Zafiro.Reactive.ObservableMixin` 和 `Zafiro.CSharpFunctionalExtensions.ObservableExtensions`。
