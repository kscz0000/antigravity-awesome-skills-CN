# 常见代码异味与修复模式

## 用途

在代码优先审查中使用此参考，将可见的 SwiftUI 模式映射到可能的运行时开销，并获取更安全的修复指导。

## 高优先级异味

### `body` 中使用昂贵的格式化器

```swift
var body: some View {
    let number = NumberFormatter()
    let measure = MeasurementFormatter()
    Text(measure.string(from: .init(value: meters, unit: .meters)))
}
```

优先在模型或专用辅助类中缓存格式化器：

```swift
final class DistanceFormatter {
    static let shared = DistanceFormatter()
    let number = NumberFormatter()
    let measure = MeasurementFormatter()
}
```

### 重计算属性

```swift
var filtered: [Item] {
    items.filter { $0.isEnabled }
}
```

优先在模型/辅助类中仅在有意义的输入变更时计算一次，或仅在视图确实拥有转换生命周期时存储派生的视图自有状态。

### 在 `body` 内排序或过滤

```swift
List {
    ForEach(items.sorted(by: sortRule)) { item in
        Row(item)
    }
}
```

优先在渲染工作开始前完成排序：

```swift
let sortedItems = items.sorted(by: sortRule)
```

### `ForEach` 内联过滤

```swift
ForEach(items.filter { $0.isEnabled }) { item in
    Row(item)
}
```

优先使用预先过滤且具有稳定身份标识的集合。

### 不稳定的身份标识

```swift
ForEach(items, id: \.self) { item in
    Row(item)
}
```

对非稳定值或会重排的集合避免使用 `id: \.self`。使用稳定的领域标识符。

### 顶层条件视图切换

```swift
var content: some View {
    if isEditing {
        editingView
    } else {
        readOnlyView
    }
}
```

优先使用一个稳定的基础视图，将条件局部化到各个区段或修饰符中。这减少了根身份抖动，使 diff 计算更廉价。

### 主线程图片解码

```swift
Image(uiImage: UIImage(data: data)!)
```

优先将解码和降采样工作移出主线程，然后存储处理后的图片。

## 观察扇出

### iOS 17+ 上广泛的 `@Observable` 读取

```swift
@Observable final class Model {
    var items: [Item] = []
}

var body: some View {
    Row(isFavorite: model.items.contains(item))
}
```

如果多个视图读取同一个广泛的集合或根模型，小变更可能扇出为大范围失效。优先使用更精细的派生输入、更小的 Observable 表面积，或将逐项状态移近叶视图。

### iOS 16 及更早版本上的广泛 `ObservableObject` 读取

```swift
final class Model: ObservableObject {
    @Published var items: [Item] = []
}
```

同样的警告适用于传统观察机制。避免让大量后代观察一个大型共享对象，而它们只需要其中一个派生字段。

## 修复说明

### `@State` 不是通用缓存

`@State` 用于视图自有状态和有意属于视图生命周期的派生值。不要将任意昂贵计算移入 `@State`，除非你同时定义了何时以及为何更新。

更好的替代方案：
- 在模型或 store 中预计算
- 响应特定输入变更更新派生状态
- 在专用辅助类中记忆化
- 在渲染前通过后台任务预处理

### `equatable()` 是有条件指导

仅在以下情况使用 `equatable()`：
- 相等性判断比重计算子树更便宜，且
- 视图输入具有值语义且足够稳定，能进行有意义的相等性检查

不要将 `equatable()` 作为所有重绘的通用修复手段。

## 分诊顺序

当多个异味同时出现时，按以下优先级排列：
1. 广泛失效和观察扇出
2. 不稳定身份标识和列表抖动
3. 渲染期间的主线程工作
4. 图片解码或缩放开销
5. 布局和动画复杂度
