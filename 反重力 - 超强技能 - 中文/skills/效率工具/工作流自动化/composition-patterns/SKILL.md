---
name: composition-patterns
description: "Use when working with composition-patterns tasks or workflows. 触发词：组合模式、composition pattern、组件架构、React 组合、复合组件、上下文提供者、布尔属性、组件库、灵活 API。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# React 组合模式

用于构建灵活、可维护 React 组件的组合模式。通过使用复合组件、状态提升以及内部组合，避免布尔属性的泛滥。这些模式能让代码库在规模增长时对人类和 AI 智能体都更易于使用。

## 适用场景

在以下情况下参考这些指南：

- 重构具有大量布尔属性的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或上下文提供者

## 按优先级划分的规则类别

| 优先级 | 类别                | 影响   | 前缀            |
| ------ | ------------------- | ------ | --------------- |
| 1      | 组件架构            | 高     | `architecture-` |
| 2      | 状态管理            | 中     | `state-`        |
| 3      | 实现模式            | 中     | `patterns-`     |
| 4      | React 19 API        | 中     | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要添加布尔属性来定制行为；而是使用组合
- `architecture-compound-components` - 使用共享上下文来组织复杂组件

### 2. 状态管理（中）

- `state-decouple-implementation` - 提供者是唯一知晓如何管理状态的地方
- `state-context-interface` - 定义包含 state、actions、meta 的通用接口用于依赖注入
- `state-lift-state` - 将状态提升到提供者组件中以便兄弟组件访问

### 3. 实现模式（中）

- `patterns-explicit-variants` - 创建显式的变体组件，而非使用布尔模式
- `patterns-children-over-render-props` - 使用 children 进行组合，而非 renderX 属性

### 4. React 19 API（中）

> **⚠️ 仅限 React 19+。** 如果使用的是 React 18 或更早版本，请跳过本节。

- `react19-no-forwardref` - 不要使用 `forwardRef`；使用 `use()` 替代 `useContext()`

## 如何使用

阅读单个规则文件以获取详细说明和代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：

- 简要说明其重要性
- 错误代码示例及解释
- 正确代码示例及解释
- 其它上下文与参考

## 完整编译文档

如需包含所有规则展开内容的完整指南，请参阅：`AGENTS.md`

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下并请求澄清。
