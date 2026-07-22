---
name: swiftui-liquid-glass
description: 实现或审查 SwiftUI Liquid Glass API，确保正确的回退方案和修饰符顺序。触发词：Liquid Glass、SwiftUI玻璃效果、glassEffect、GlassEffectContainer、iOS 26设计
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# SwiftUI Liquid Glass 设计系统

## 概述
使用此技能构建或审查完全符合 iOS 26+ Liquid Glass API 的 SwiftUI 功能。优先使用原生 API（`glassEffect`、`GlassEffectContainer`、glass 按钮样式）和 Apple 设计指南。保持使用一致性、按需添加交互性，并关注性能。

## 使用场景
- 用户需要在 SwiftUI 界面中采用或审查 Liquid Glass。
- 需要正确的 API 用法、回退处理或 Liquid Glass 的修饰符顺序。

## 工作流决策树
根据请求选择对应路径：

### 1) 审查现有功能
- 检查哪些地方应使用 Liquid Glass，哪些地方不应使用。
- 验证正确的修饰符顺序、形状用法和容器放置。
- 检查 iOS 26+ 可用性处理和合理的回退方案。

### 2) 使用 Liquid Glass 改进功能
- 确定需要应用玻璃效果的目标组件（表面、标签、按钮、卡片）。
- 在多个玻璃元素出现时重构为使用 `GlassEffectContainer`。
- 仅对可点击或可聚焦的元素引入交互式玻璃。

### 3) 使用 Liquid Glass 实现新功能
- 先设计玻璃表面和交互（形状、突出程度、分组）。
- 在布局/外观修饰符之后添加玻璃修饰符。
- 仅在视图层级随动画变化时添加形变过渡。

## 核心指南
- 优先使用原生 Liquid Glass API，而非自定义模糊效果。
- 当多个玻璃元素共存时使用 `GlassEffectContainer`。
- 在布局和视觉修饰符之后应用 `.glassEffect(...)`。
- 对需要响应触摸/指针的元素使用 `.interactive()`。
- 在相关元素间保持形状一致，以获得协调的视觉效果。
- 使用 `#available(iOS 26, *)` 进行版本判断，并提供非玻璃回退方案。

## 审查清单
- **可用性**：存在 `#available(iOS 26, *)` 并配有回退 UI。
- **组合**：多个玻璃视图已包裹在 `GlassEffectContainer` 中。
- **修饰符顺序**：`glassEffect` 在布局/外观修饰符之后应用。
- **交互性**：`interactive()` 仅用于存在用户交互的地方。
- **过渡**：`glassEffectID` 与 `@Namespace` 配合用于形变效果。
- **一致性**：形状、着色和间距在整个功能中保持一致。

## 实现清单
- 定义目标元素和期望的玻璃突出程度。
- 将分组的玻璃元素包裹在 `GlassEffectContainer` 中并调整间距。
- 按需使用 `.glassEffect(.regular.tint(...).interactive(), in: .rect(cornerRadius: ...))`。
- 使用 `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` 处理操作按钮。
- 在层级变化时使用 `glassEffectID` 添加形变过渡。
- 为早期 iOS 版本提供回退材质和视觉效果。

## 快速代码片段
直接使用以下模式，并根据需要调整形状/着色/间距。

```swift
if #available(iOS 26, *) {
    Text("Hello")
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    Text("Hello")
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}
```

```swift
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        Image(systemName: "scribble.variable")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
        Image(systemName: "eraser.fill")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
    }
}
```

```swift
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

## 资源
- 参考指南：`references/liquid-glass.md`
- 优先查阅 Apple 文档获取最新的 API 细节。

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
