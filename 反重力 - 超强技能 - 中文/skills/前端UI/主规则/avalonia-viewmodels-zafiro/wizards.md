# 向导与流程

复杂的多步骤流程使用 `SlimWizard` 模式处理。这提供了一种声明式的方式来定义步骤、导航逻辑和最终结果。

## 定义向导

使用 `WizardBuilder` 定义步骤。每个步骤对应一个 ViewModel。

```csharp
SlimWizard<string> wizard = WizardBuilder
    .StartWith(() => new Step1ViewModel(data))
        .NextUnit()
        .WhenValid()
    .Then(prevResult => new Step2ViewModel(prevResult))
        .NextCommand(vm => vm.CustomNextCommand)
    .Then(result => new SuccessViewModel("Done!"))
        .Next((_, s) => s, "Finish")
    .WithCompletionFinalStep();
```

### 导航规则

- **NextUnit()**：当发出简单信号时前进。
- **NextCommand()**：当 ViewModel 中的特定命令成功执行时前进。
- **WhenValid()**：等待当前 ViewModel 验证通过后才允许导航。
- **Always()**：始终允许导航。

## 导航集成

向导使用 `INavigator` 进行导航：

```csharp
public async Task CreateSomething()
{
    var wizard = BuildWizard();
    var result = await wizard.Navigate(navigator);
    // 处理结果
}
```

## 步骤配置

- **WithCompletionFinalStep()**：当最后一步完成时标记向导为已完成。
- **WithCommitFinalStep()**：通常用于执行最终"保存"或"部署"操作的向导。

> [!NOTE]
> `SlimWizard` 自动处理"返回"命令，为不同流程提供一致的用户体验。
