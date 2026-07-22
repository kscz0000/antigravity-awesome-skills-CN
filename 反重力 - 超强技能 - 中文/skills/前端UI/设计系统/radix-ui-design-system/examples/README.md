# Radix UI 设计系统 - 技能示例

本目录包含实用示例，演示如何使用 Radix UI 原语构建可访问、可自定义的组件。

## 示例

### `dialog-example.tsx`

演示 Dialog（模态框）组件模式：
- **BasicDialog**：带表单的标准模态框
- **ControlledDialog**：外部受控的模态框状态

**关键概念**：
- 在 DOM 层级之外进行 Portal 渲染
- 遮罩层（背景）处理
- 无障碍要求（Title、Description）
- 使用 CSS 进行自定义样式

### `dropdown-example.tsx`

完整的下拉菜单实现：
- **CompleteDropdown**：包含所有 Radix 原语的功能完备菜单
  - 普通项
  - 分隔符与标签
  - 复选框项
  - 单选组
  - 子菜单
- **ActionsMenu**：用于数据表格/卡片的简单操作菜单

**关键概念**：
- 复合组件架构
- 键盘导航
- 项指示器（复选框、单选按钮）
- 嵌套子菜单

## 使用方法

```tsx
import { BasicDialog } from './examples/dialog-example';
import { CompleteDropdown } from './examples/dropdown-example';

function App() {
  return (
    <>
      <BasicDialog />
      <CompleteDropdown />
    </>
  );
}
```

## 样式

这些示例使用 CSS 类。你可以选择：
1. 复制每个文件中的 CSS
2. 替换为 Tailwind 类
3. 使用 CSS-in-JS（Stitches、Emotion 等）

## 了解更多

- [主 SKILL.md](../SKILL.md) - 完整指南
- [组件模板](../templates/component-template.tsx.template) - 样板代码
- [Radix UI 文档](https://www.radix-ui.com/primitives)
