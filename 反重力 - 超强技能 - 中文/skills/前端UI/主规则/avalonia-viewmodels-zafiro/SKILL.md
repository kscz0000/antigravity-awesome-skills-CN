---
name: avalonia-viewmodels-zafiro
description: "使用 Zafiro 和 ReactiveUI 创建 Avalonia ViewModel 和向导的最佳模式。触发词：Avalonia ViewModel、Zafiro、ReactiveUI、向导模式、SlimWizard、WizardBuilder、IEnhancedCommand、Section属性、DataTypeViewLocator、组合根、导航区块"
risk: none
source: community
date_added: "2026-02-27"
---

# Avalonia ViewModels with Zafiro

本技能提供了一套最佳实践和模式，用于在 Avalonia 应用程序中创建 ViewModel、向导以及管理导航，充分利用 **ReactiveUI** 和 **Zafiro** 工具包的强大功能。

## 核心原则

1.  **函数式响应式方法**：使用 ReactiveUI（`ReactiveObject`、`WhenAnyValue` 等）处理状态和逻辑。
2.  **增强命令**：使用 `IEnhancedCommand` 实现更好的命令管理，包括进度报告和名称/文本属性。
3.  **向导模式**：使用 `SlimWizard` 和 `WizardBuilder` 实现复杂流程，采用声明式且易于维护的方式。
4.  **自动区块发现**：使用 `[Section]` 属性自动注册和发现 UI 区块。
5.  **清晰的组合**：使用 `DataTypeViewLocator` 将 ViewModel 映射到 View，并在 `CompositionRoot` 中管理依赖项。

## 指南

- [ViewModel 与命令](viewmodels.md)：创建健壮的 ViewModel 和处理命令。
- [向导与流程](wizards.md)：使用 `SlimWizard` 构建多步骤向导。
- [导航与区块](navigation_sections.md)：管理导航和基于区块的 UI。
- [组合与映射](composition.md)：View-ViewModel 绑定和依赖注入的最佳实践。

## 示例参考

关于实际实现，请参考 **Angor** 项目：
- `CreateProjectFlowV2.cs`：复杂向导构建的优秀示例。
- `HomeViewModel.cs`：使用函数式响应式命令的简单区块 ViewModel。

## 适用场景
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确符合上述描述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
