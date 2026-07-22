---
name: avalonia-layout-zafiro
description: "使用 Zafiro.Avalonia 构建现代 Avalonia UI 布局的指南，强调共享样式、通用组件和避免 XAML 冗余。触发词：Avalonia布局、Zafiro布局、XAML样式、语义容器、EdgePanel、HeaderedContainer、图标扩展、行为模式、UI组件"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 使用 Zafiro.Avalonia 构建 Avalonia 布局

> 掌握现代、简洁、可维护的 Avalonia UI 布局。
> **专注于语义容器、共享样式和精简 XAML。**

## 🎯 选择性阅读规则

**只阅读与当前布局挑战相关的文件！**

---

## 📑 内容导航

| 文件 | 描述 | 阅读时机 |
|------|------|----------|
| `themes.md` | 主题组织和共享样式 | 设置或优化应用主题时 |
| `containers.md` | 语义容器（`HeaderedContainer`、`EdgePanel`、`Card`） | 构建视图和布局结构时 |
| `icons.md` | 使用 `IconExtension` 和 `IconOptions` 管理图标 | 添加和自定义图标时 |
| `behaviors.md` | `Xaml.Interaction.Behaviors` 和避免转换器 | 实现复杂交互时 |
| `components.md` | 通用组件和减少嵌套 | 创建可复用 UI 元素时 |

---

## 🔗 相关项目（示例实现）

如需实际案例，请参考 **Angor** 项目：
`/mnt/fast/Repos/angor/src/Angor/Avalonia/Angor.Avalonia.sln`

---

## ✅ 简洁布局检查清单

- [ ] **使用了语义容器？**（例如用 `HeaderedContainer` 代替手动添加标题的 `Border`）
- [ ] **避免了冗余属性？** 在 `axaml` 文件中使用共享样式。
- [ ] **最小化了嵌套？** 使用 `EdgePanel` 或通用组件扁平化布局。
- [ ] **通过扩展使用图标？** 使用 `{Icon fa-name}` 和 `IconOptions` 设置样式。
- [ ] **优先使用行为而非代码隐藏？** 使用 `Interaction.Behaviors` 处理 UI 逻辑。
- [ ] **避免了转换器？** 优先使用 ViewModel 属性或行为，除非必要。

---

## ❌ 反模式

**不要：**
- 在视图中使用硬编码的颜色或尺寸（字面量）。
- 创建深度嵌套的 `Grid` 和 `StackPanel`。
- 在多个元素上重复视觉属性（应使用样式）。
- 将简单逻辑放在 `IValueConverter` 中，这些逻辑应该属于 ViewModel。

**应该：**
- 使用 `DynamicResource` 引用颜色和画笔。
- 将重复布局提取为通用组件。
- 利用 `Zafiro.Avalonia` 特有的面板（如 `EdgePanel`）处理常见 UI 模式。

## 使用时机
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
