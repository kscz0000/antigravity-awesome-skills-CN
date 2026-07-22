# 在 SwiftUI 中实现 Liquid Glass 设计

## 概述

Liquid Glass 是 iOS 中引入的一种动态材质，结合了玻璃的光学特性和流动感。它会模糊后方内容、反射周围内容的颜色和光线，并实时响应触摸和指针交互。本指南介绍如何在 SwiftUI 应用中实现和自定义 Liquid Glass 效果。当用户请求帮助采用新的 Apple 设计时，应始终查阅 Liquid Glass 相关指南。

Liquid Glass 的核心特性：
- 模糊后方内容
- 反射周围内容的颜色和光线
- 响应触摸和指针交互
- 过渡期间可在形状间形变
- 适用于标准和自定义组件

## 基础实现

### 为视图添加 Liquid Glass

为视图添加 Liquid Glass 最简单的方式是使用 `glassEffect()` 修饰符：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()
```

默认情况下，这会在视图内容后方以 Capsule 形状应用标准 Glass 效果。

### 自定义形状

你可以为 Liquid Glass 效果指定不同的形状：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(in: .rect(cornerRadius: 16.0))
```

常用形状选项：
- `.capsule`（默认）
- `.rect(cornerRadius: CGFloat)`
- `.circle`

## 自定义 Liquid Glass 效果

### Glass 变体和属性

你可以通过配置 `Glass` 结构来自定义 Liquid Glass 效果：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.tint(.orange).interactive())
```

关键自定义选项：
- `.regular` - 标准玻璃效果
- `.tint(Color)` - 添加颜色着色以表示突出程度
- `.interactive(Bool)` - 使玻璃响应触摸和指针交互

### 创建交互式玻璃

使 Liquid Glass 响应触摸和指针交互：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.interactive(true))
```

更简洁的写法：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.interactive())
```

## 处理多个玻璃效果

### 使用 GlassEffectContainer

当对多个视图应用 Liquid Glass 效果时，使用 `GlassEffectContainer` 以获得更好的渲染性能，并启用混合和形变效果：

```swift
GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()

        Image(systemName: "eraser.fill")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()
    }
}
```

`spacing` 参数控制 Liquid Glass 效果之间的交互方式：
- 间距越小：视图需要更靠近才能合并效果
- 间距越大：效果在更远距离即可合并

### 合并多个玻璃效果

要将多个视图合并为单个 Liquid Glass 效果，使用 `glassEffectUnion` 修饰符：

```swift
@Namespace private var namespace

// 在视图中使用：
GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        ForEach(symbolSet.indices, id: \.self) { item in
            Image(systemName: symbolSet[item])
                .frame(width: 80.0, height: 80.0)
                .font(.system(size: 36))
                .glassEffect()
                .glassEffectUnion(id: item < 2 ? "1" : "2", namespace: namespace)
        }
    }
}
```

这在动态创建视图或视图位于 HStack/VStack 之外时非常有用。

## 形变效果和过渡

### 创建形变过渡

要在使用 Liquid Glass 的视图之间创建形变过渡效果：

1. 使用 `@Namespace` 属性包装器创建命名空间
2. 使用 `glassEffectID` 将每个 Liquid Glass 效果与唯一标识符关联
3. 在更改视图层级时使用动画

```swift
@State private var isExpanded: Bool = false
@Namespace private var namespace

var body: some View {
    GlassEffectContainer(spacing: 40.0) {
        HStack(spacing: 40.0) {
            Image(systemName: "scribble.variable")
                .frame(width: 80.0, height: 80.0)
                .font(.system(size: 36))
                .glassEffect()
                .glassEffectID("pencil", in: namespace)

            if isExpanded {
                Image(systemName: "eraser.fill")
                    .frame(width: 80.0, height: 80.0)
                    .font(.system(size: 36))
                    .glassEffect()
                    .glassEffectID("eraser", in: namespace)
            }
        }
    }

    Button("Toggle") {
        withAnimation {
            isExpanded.toggle()
        }
    }
    .buttonStyle(.glass)
}
```

形变效果会在带有 Liquid Glass 的视图因视图层级变化而出现或消失时触发。

## 使用 Liquid Glass 的按钮样式

### 玻璃按钮样式

SwiftUI 提供了内置的 Liquid Glass 按钮样式：

```swift
Button("Click Me") {
    // Action
}
.buttonStyle(.glass)
```

### 突出玻璃按钮样式

要获得更突出的玻璃按钮：

```swift
Button("Important Action") {
    // Action
}
.buttonStyle(.glassProminent)
```

## 高级技巧

### 背景扩展效果

使用背景扩展效果将内容延伸到侧边栏或检查器下方：

```swift
NavigationSplitView {
    // 侧边栏内容
} detail: {
    // 详情内容
        .background {
            // 延伸到侧边栏下方的背景内容
        }
}
```

### 将水平滚动延伸到侧边栏下方

将水平滚动视图延伸到侧边栏或检查器下方：

```swift
ScrollView(.horizontal) {
    // 可滚动内容
}
.scrollExtensionMode(.underSidebar)
```

## 最佳实践

1. **容器使用**：对多个视图应用 Liquid Glass 时，始终使用 `GlassEffectContainer` 以获得更好的性能和形变效果。

2. **效果顺序**：在影响视图外观的其他修饰符之后应用 `.glassEffect()` 修饰符。

3. **间距考量**：仔细选择容器中的间距值，以控制玻璃效果的合并方式和时机。

4. **动画**：在更改视图层级时使用动画，以实现平滑的形变过渡。

5. **交互性**：为需要响应用户交互的玻璃效果添加 `.interactive()`。

6. **设计一致性**：在整个应用中保持一致的形状和样式，以获得协调的视觉效果。

## 示例：使用 Liquid Glass 的自定义徽章

```swift
struct BadgeView: View {
    let symbol: String
    let color: Color

    var body: some View {
        ZStack {
            Image(systemName: "hexagon.fill")
                .foregroundColor(color)
                .font(.system(size: 50))

            Image(systemName: symbol)
                .foregroundColor(.white)
                .font(.system(size: 30))
        }
        .glassEffect(.regular, in: .rect(cornerRadius: 16))
    }
}

// 使用方式：
GlassEffectContainer(spacing: 20) {
    HStack(spacing: 20) {
        BadgeView(symbol: "star.fill", color: .blue)
        BadgeView(symbol: "heart.fill", color: .red)
        BadgeView(symbol: "leaf.fill", color: .green)
    }
}
```

## 参考资料

- [为自定义视图应用 Liquid Glass](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Landmarks: 使用 Liquid Glass 构建应用](https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass)
- [SwiftUI View.glassEffect(_:in:isEnabled:)](https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:isEnabled:))
- [SwiftUI GlassEffectContainer](https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer)
- [SwiftUI GlassEffectTransition](https://developer.apple.com/documentation/SwiftUI/GlassEffectTransition)
- [SwiftUI GlassButtonStyle](https://developer.apple.com/documentation/SwiftUI/GlassButtonStyle)
