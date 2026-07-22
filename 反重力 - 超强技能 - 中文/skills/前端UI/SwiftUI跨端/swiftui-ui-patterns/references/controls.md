# 控件（Toggle、Slider、Picker）

## 意图

在设置和配置页面使用原生控件，保持标签可访问、状态绑定清晰。

## 核心模式

- 控件直接绑定到 `@State`、`@Binding` 或 `@AppStorage`。
- 布尔偏好优先使用 `Toggle`。
- 数值范围使用 `Slider`，并在标签中显示当前值。
- 离散选择使用 `Picker`；仅 2–4 个选项时使用 `.pickerStyle(.segmented)`。
- 标签保持可见且有描述性，避免在控件内嵌入按钮。

## 示例：带分区的开关

```swift
Form {
  Section("Notifications") {
    Toggle("Mentions", isOn: $preferences.notificationsMentionsEnabled)
    Toggle("Follows", isOn: $preferences.notificationsFollowsEnabled)
    Toggle("Boosts", isOn: $preferences.notificationsBoostsEnabled)
  }
}
```

## 示例：带数值文本的滑块

```swift
Section("Font Size") {
  Slider(value: $fontSizeScale, in: 0.5...1.5, step: 0.1)
  Text("Scale: \(String(format: "%.1f", fontSizeScale))")
    .font(.scaledBody)
}
```

## 示例：枚举选择器

```swift
Picker("Default Visibility", selection: $visibility) {
  ForEach(Visibility.allCases, id: \.self) { option in
    Text(option.title).tag(option)
  }
}
```

## 设计要点

- 在 `Form` 分区中对相关控件分组。
- 使用 `.disabled(...)` 反映锁定或继承的设置。
- 需要增加清晰度时，在开关内使用 `Label` 组合图标 + 文本。

## 陷阱

- 大量选项避免使用 `.pickerStyle(.segmented)`，改用菜单或内联样式。
- 不要隐藏滑块的标签，始终显示上下文。
- 避免硬编码控件颜色，谨慎使用主题 tint。
