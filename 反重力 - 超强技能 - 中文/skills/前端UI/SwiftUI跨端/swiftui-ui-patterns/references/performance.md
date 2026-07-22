# 性能防护

## 意图

当 SwiftUI 页面内容多、滚动密集、频繁更新或存在不必要的重计算风险时，使用这些规则。

## 核心规则

- 为 `ForEach` 和列表内容提供稳定的标识。当集合可能重排或变更时，不要使用不稳定的索引作为标识。
- 将耗时的过滤、排序和格式化移出 `body`；当不是简单操作时，预计算或将其移入模型/助手。
- 缩小观察范围，让只有读取变化状态的视图才需要更新。
- 对大型滚动内容优先使用惰性容器，当页面只有部分频繁变化时提取子视图。
- 避免为小的状态变更替换整个顶层视图树，保持稳定的根视图并只变化局部区域或修饰符。

## 示例：稳定标识

```swift
ForEach(items) { item in
  Row(item: item)
}
```

当集合可能改变顺序时，优先使用这种方式而非基于索引的标识：

```swift
ForEach(Array(items.enumerated()), id: \.offset) { _, item in
  Row(item: item)
}
```

## 示例：将耗时工作移出 body

```swift
struct FeedView: View {
  let items: [FeedItem]

  private var sortedItems: [FeedItem] {
    items.sorted(using: KeyPathComparator(\.createdAt, order: .reverse))
  }

  var body: some View {
    List(sortedItems) { item in
      FeedRow(item: item)
    }
  }
}
```

如果工作比简单的派生属性更耗时，将其移入更新频率更低的模型、store 或助手。

## 何时需要进一步调查

- 长列表或网格中的滚动卡顿
- 搜索或表单验证导致的输入延迟
- 一个小的状态变化触发了过于宽泛的视图更新
- 大量条件判断或重复格式化工作的大型页面

## 陷阱

- 每次渲染都重新计算重量级转换
- 从大量后代视图观察一个大对象，但只有其中一个字段是重要的
- 在 `List`、`LazyVStack` 或 `LazyHGrid` 已经能解决问题时构建自定义滚动容器
