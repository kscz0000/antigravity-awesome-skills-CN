---
name: react-patterns
description: "现代 React 模式与原则。Hooks、组合、性能、TypeScript 最佳实践。触发词：React模式、React最佳实践、Hooks模式、组件设计、状态管理、React性能、React组合模式、React反模式、React 19、useActionState、useOptimistic、React编译器"
risk: safe
source: community
date_added: "2026-02-27"
---

# React 模式

> 构建生产级 React 应用的原则。

---

## 1. 组件设计原则

### 组件类型

| 类型 | 用途 | 状态 |
|------|-----|------|
| **Server** | 数据获取、静态内容 | 无 |
| **Client** | 交互性 | useState、effects |
| **Presentational** | UI 展示 | 仅 Props |
| **Container** | 逻辑/状态 | 重度状态 |

### 设计规则

- 每个组件单一职责
- Props 向下传递，事件向上冒泡
- 组合优于继承
- 优先使用小型、聚焦的组件

---

## 2. Hook 模式

### 何时提取 Hook

| 模式 | 提取时机 |
|------|----------|
| **useLocalStorage** | 需要相同的存储逻辑 |
| **useDebounce** | 多个防抖值 |
| **useFetch** | 重复的请求模式 |
| **useForm** | 复杂的表单状态 |

### Hook 规则

- Hook 只能在顶层调用
- 每次渲染顺序相同
- 自定义 Hook 以 "use" 开头
- 卸载时清理 effect

---

## 3. 状态管理选择

| 复杂度 | 方案 |
|--------|------|
| 简单 | useState, useReducer |
| 局部共享 | Context |
| 服务端状态 | React Query, SWR |
| 复杂全局 | Zustand, Redux Toolkit |

### 状态放置

| 作用域 | 位置 |
|--------|------|
| 单个组件 | useState |
| 父子组件 | 状态提升 |
| 子树 | Context |
| 全应用 | 全局 Store |

---

## 4. React 19 模式

### 新 Hook

| Hook | 用途 |
|------|------|
| **useActionState** | 表单提交状态 |
| **useOptimistic** | 乐观 UI 更新 |
| **use** | 在渲染中读取资源 |

### 编译器优势

- 自动记忆化
- 减少手动 useMemo/useCallback
- 聚焦纯组件

---

## 5. 组合模式

### 复合组件

- 父组件提供 Context
- 子组件消费 Context
- 灵活的插槽式组合
- 示例：Tabs, Accordion, Dropdown

### Render Props vs Hooks

| 使用场景 | 推荐方式 |
|----------|----------|
| 可复用逻辑 | 自定义 Hook |
| 渲染灵活性 | Render Props |
| 横切关注点 | 高阶组件 |

---

## 6. 性能原则

### 何时优化

| 信号 | 行动 |
|------|------|
| 渲染缓慢 | 先 Profile |
| 大列表 | 虚拟化 |
| 昂贵计算 | useMemo |
| 稳定回调 | useCallback |

### 优化顺序

1. 检查是否真的慢
2. 用 DevTools Profile
3. 定位瓶颈
4. 针对性修复

---

## 7. 错误处理

### Error Boundary 使用

| 作用域 | 放置位置 |
|--------|----------|
| 全应用 | 根级别 |
| 功能模块 | 路由/功能级别 |
| 组件 | 包裹风险组件 |

### 错误恢复

- 显示降级 UI
- 记录错误
- 提供重试选项
- 保留用户数据

---

## 8. TypeScript 模式

### Props 类型

| 模式 | 用途 |
|------|------|
| Interface | 组件 Props |
| Type | 联合类型、复杂类型 |
| Generic | 可复用组件 |

### 常用类型

| 需求 | 类型 |
|------|------|
| Children | ReactNode |
| 事件处理 | MouseEventHandler |
| Ref | RefObject<Element> |

---

## 9. 测试原则

| 层级 | 关注点 |
|------|--------|
| 单元测试 | 纯函数、Hooks |
| 集成测试 | 组件行为 |
| E2E | 用户流程 |

### 测试优先级

- 用户可见的行为
- 边界情况
- 错误状态
- 无障碍

---

## 10. 反模式

| ❌ 不要 | ✅ 应该 |
|---------|---------|
| 深层 Props 传递 | 使用 Context |
| 巨型组件 | 拆分为小组件 |
| 万事皆 useEffect | 使用 Server Components |
| 过早优化 | 先 Profile |
| 用索引作 key | 使用稳定的唯一 ID |

---

> **记住：** React 的核心是组合。构建小组件，用心组合。

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
