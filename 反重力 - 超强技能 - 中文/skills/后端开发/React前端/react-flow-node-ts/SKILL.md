---
name: react-flow-node-ts
description: "按照既定模式创建React Flow节点组件，包含正确的TypeScript类型和存储集成。触发词：React Flow、节点组件、TypeScript、存储集成、组件模式"
risk: unknown
source: community
date_added: "2026-02-27"
---

# React Flow 节点

按照既定模式创建React Flow节点组件，包含正确的TypeScript类型和存储集成。

## 快速开始

从assets/目录复制模板并替换占位符：
- `{{NodeName}}` → PascalCase组件名（例如：`VideoNode`）
- `{{nodeType}}` → kebab-case类型标识符（例如：`video-node`）
- `{{NodeData}}` → 数据接口名（例如：`VideoNodeData`）

## 模板

- assets/template.tsx - 节点组件
- assets/types.template.ts - TypeScript定义

## 节点组件模式

```tsx
export const MyNode = memo(function MyNode({
  id,
  data,
  selected,
  width,
  height,
}: MyNodeProps) {
  const updateNode = useAppStore((state) => state.updateNode);
  const canvasMode = useAppStore((state) => state.canvasMode);
  
  return (
    <>
      <NodeResizer isVisible={selected && canvasMode === 'editing'} />
      <div className="node-container">
        <Handle type="target" position={Position.Top} />
        {/* Node content */}
        <Handle type="source" position={Position.Bottom} />
      </div>
    </>
  );
});
```

## 类型定义模式

```typescript
export interface MyNodeData extends Record<string, unknown> {
  title: string;
  description?: string;
}

export type MyNode = Node<MyNodeData, 'my-node'>;
```

## 集成步骤

1. 将类型添加到 `src/frontend/src/types/index.ts`
2. 在 `src/frontend/src/components/nodes/` 创建组件
3. 从 `src/frontend/src/components/nodes/index.ts` 导出
4. 在 `src/frontend/src/store/app-store.ts` 添加默认值
5. 在画布 `nodeTypes` 中注册
6. 添加到 AddBlockMenu 和 ConnectMenu

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清