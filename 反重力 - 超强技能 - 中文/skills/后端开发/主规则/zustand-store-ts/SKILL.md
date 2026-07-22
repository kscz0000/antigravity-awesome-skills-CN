---
name: zustand-store-ts
description: "按照既定模式创建 Zustand 存储，使用恰当的 TypeScript 类型和中间件。触发词：zustand、store、状态管理、typescript、中间件、subscribeWithSelector"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Zustand 存储

按照既定模式创建 Zustand 存储，使用恰当的 TypeScript 类型和中间件。

## 快速开始

从 assets/template.ts 复制模板并替换占位符：
- `{{StoreName}}` → PascalCase 形式的存储名称（例如 `Project`）
- `{{description}}` → 用于 JSDoc 的简要描述

## 始终使用 subscribeWithSelector

```typescript
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

export const useMyStore = create<MyStore>()(
  subscribeWithSelector((set, get) => ({
    // state and actions
  }))
);
```

## 分离状态与操作

```typescript
export interface MyState {
  items: Item[];
  isLoading: boolean;
}

export interface MyActions {
  addItem: (item: Item) => void;
  loadItems: () => Promise<void>;
}

export type MyStore = MyState & MyActions;
```

## 使用独立选择器

```typescript
// Good - only re-renders when `items` changes
const items = useMyStore((state) => state.items);

// Avoid - re-renders on any state change
const { items, isLoading } = useMyStore();
```

## 在 React 外部订阅

```typescript
useMyStore.subscribe(
  (state) => state.selectedId,
  (selectedId) => console.log('Selected:', selectedId)
);
```

## 集成步骤

1. 在 `src/frontend/src/store/` 中创建存储
2. 从 `src/frontend/src/store/index.ts` 导出
3. 在 `src/frontend/src/store/*.test.ts` 中添加测试

## 适用场景

本技能适用于执行上述概览中描述的工作流或操作。

## 限制说明
- 仅当任务明确匹配上述范围时使用本技能。
- 请勿将输出视为可替代特定环境验证、测试或专家审查的产物。
- 若缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
