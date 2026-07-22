---
name: unreal-engine-cpp-pro
description: "虚幻引擎 5.x C++ 开发专家指南，涵盖 UObject 管理、性能优化和最佳实践。"
risk: safe
source: self
date_added: "2026-02-27"
---

# 虚幻引擎 C++ 专家指南

本技能提供使用 C++ 开发虚幻引擎 5 的专家级指导，专注于编写健壮、高性能且符合标准的代码。

## 使用场景

适用情况：
- 为虚幻引擎 5.x 项目开发 C++ 代码
- 编写 Actor、Component 或 UObject 派生类
- 优化虚幻引擎中的性能关键代码
- 调试内存泄漏或垃圾回收问题
- 实现蓝图可调用的功能
- 遵循 Epic Games 编码标准和规范
- 使用虚幻反射系统（UCLASS、USTRUCT、UFUNCTION）
- 管理资源加载和软引用

不适用情况：
- 纯蓝图项目（无 C++ 代码）
- 开发虚幻引擎 5.x 之前的版本
- 非虚幻引擎的游戏引擎开发
- 与虚幻引擎开发无关的任务

## 核心原则

1. **UObject 与垃圾回收**：
    * 对 `UObject*` 成员变量始终使用 `UPROPERTY()`，确保垃圾回收器（GC）能追踪到它们。
    * 若需在 UObject 图外部保持根引用，可使用 `TStrongObjectPtr<>`，但通常优先使用 `addToRoot()`。
    * 理解 `IsValid()` 与 `nullptr` 的区别：`IsValid()` 能安全处理 pending kill 状态。

2. **虚幻反射系统**：
    * 使用 `UCLASS()`、`USTRUCT()`、`UENUM()`、`UFUNCTION()` 将类型暴露给反射系统和蓝图。
    * 尽量减少 `BlueprintReadWrite` 的使用；对于不应被 UI/关卡蓝图篡改的状态，优先使用 `BlueprintReadOnly`。

3. **性能优先**：
    * **Tick**：默认禁用 Tick（`bCanEverTick = false`），仅在绝对必要时启用。优先使用定时器（`GetWorldTimerManager()`）或事件驱动逻辑。
    * **类型转换**：避免在热循环中使用 `Cast<T>()`，在 `BeginPlay` 中缓存引用。
    * **结构体 vs 类**：对数据密集型的非 UObject 类型使用 `F` 前缀结构体，减少开销。

## 命名规范（严格）

遵循 Epic Games 编码标准：

* **模板**：`T` 前缀（如 `TArray`、`TMap`）
* **UObject**：`U` 前缀（如 `UCharacterMovementComponent`）
* **AActor**：`A` 前缀（如 `AMyGameMode`）
* **SWidget**：`S` 前缀（Slate 控件）
* **结构体**：`F` 前缀（如 `FVector`）
* **枚举**：`E` 前缀（如 `EWeaponState`）
* **接口**：`I` 前缀（如 `IInteractable`）
* **布尔值**：`b` 前缀（如 `bIsDead`）

## 常用模式

### 1. 稳健的组件查找
避免在 `Tick` 中使用 `GetComponentByClass`，应在 `PostInitializeComponents` 或 `BeginPlay` 中完成。

```cpp
void AMyCharacter::PostInitializeComponents() {
    Super::PostInitializeComponents();
    HealthComp = FindComponentByClass<UHealthComponent>();
    check(HealthComp); // Fail hard in dev if missing
}
```

### 2. 接口实现
使用接口解耦系统（如交互系统）。

```cpp
// Interface call check
if (TargetActor->Implements<UInteractable>()) {
    IInteractable::Execute_OnInteract(TargetActor, this);
}
```

### 3. 异步加载（软引用）
对大型资源避免使用硬引用（`UPROPERTY(EditDefaultsOnly) TSubclassOf<AActor>`），它会强制加载顺序。改用 `TSoftClassPtr` 或 `TSoftObjectPtr`。

```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite)
TSoftClassPtr<AWeapon> WeaponClassToLoad;

void AMyCharacter::Equip() {
    if (WeaponClassToLoad.IsPending()) {
        WeaponClassToLoad.LoadSynchronous(); // Or use StreamableManager for async
    }
}
```

## 调试

* **日志**：使用带自定义分类的 `UE_LOG`。
    ```cpp
    DEFINE_LOG_CATEGORY_STATIC(LogMyGame, Log, All);
    UE_LOG(LogMyGame, Warning, TEXT("Health is low: %f"), CurrentHealth);
    ```
* **屏幕消息**：
    ```cpp
    if (GEngine) GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, TEXT("Died!"));
    ```
* **可视化日志**：对 AI 调试极为有用，实现 `IVisualLoggerDebugSnapshotInterface` 接口。

## 提交 PR 前检查清单

- [ ] 这个 Actor 是否需要 Tick？能否用定时器替代？
- [ ] 所有 `UObject*` 成员是否都用 `UPROPERTY` 包装？
- [ ] 硬引用（TSubclassOf）是否导致加载链？能否改为软引用？
- [ ] 是否在 `EndPlay` 中清理了已验证的委托？

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清。