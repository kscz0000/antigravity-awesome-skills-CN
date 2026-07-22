---
name: react-flow-architect
description: "构建生产级 ReactFlow 应用，支持层级导航、性能优化和高级状态管理。触发词：ReactFlow、流程图、图编辑器、节点导航、图布局、流程编排、Dagre、图状态管理、交互式图、React 图组件、graph editor、flow chart、node navigation、hierarchical tree、auto-layout"
risk: unknown
source: community
date_added: "2026-02-27"
---

# ReactFlow Architect

构建生产级 ReactFlow 应用，支持层级导航、性能优化和高级状态管理。

## 快速开始

创建一个基础的交互式图：

```tsx
import ReactFlow, { Node, Edge } from "reactflow";

const nodes: Node[] = [
  { id: "1", position: { x: 0, y: 0 }, data: { label: "Node 1" } },
  { id: "2", position: { x: 100, y: 100 }, data: { label: "Node 2" } },
];

const edges: Edge[] = [{ id: "e1-2", source: "1", target: "2" }];

export default function Graph() {
  return <ReactFlow nodes={nodes} edges={edges} />;
}
```

## 核心模式

### 层级树导航

构建支持展开/折叠的树形结构，管理父子关系。

#### Node Schema

```typescript
interface TreeNode extends Node {
  data: {
    label: string;
    level: number;
    hasChildren: boolean;
    isExpanded: boolean;
    childCount: number;
    category: "root" | "category" | "process" | "detail";
  };
}
```

#### 增量节点构建

```typescript
const buildVisibleNodes = useCallback(
  (allNodes: TreeNode[], expandedIds: Set<string>, otherDeps: any[]) => {
    const visibleNodes = new Map<string, TreeNode>();
    const visibleEdges = new Map<string, TreeEdge>();

    // Start with root nodes
    const rootNodes = allNodes.filter((n) => n.data.level === 0);

    // Recursively add visible nodes
    const addVisibleChildren = (node: TreeNode) => {
      visibleNodes.set(node.id, node);

      if (expandedIds.has(node.id)) {
        const children = allNodes.filter((n) => n.parentNode === node.id);
        children.forEach((child) => addVisibleChildren(child));
      }
    };

    rootNodes.forEach((root) => addVisibleChildren(root));

    return {
      nodes: Array.from(visibleNodes.values()),
      edges: Array.from(visibleEdges.values()),
    };
  },
  [],
);
```

### 性能优化

通过增量渲染和 memoization 处理大规模数据集。

#### 增量渲染

```typescript
const useIncrementalGraph = (
  allNodes: Node[],
  allEdges: Edge[],
  expandedList: string[],
) => {
  const prevExpandedListRef = useRef<Set<string>>(new Set());
  const prevOtherDepsRef = useRef<any[]>([]);

  const { visibleNodes, visibleEdges } = useMemo(() => {
    const currentExpandedSet = new Set(expandedList);
    const prevExpandedSet = prevExpandedListRef.current;

    // Check if expanded list changed
    const expandedChanged = !areSetsEqual(currentExpandedSet, prevExpandedSet);

    // Check if other dependencies changed
    const otherDepsChanged = !arraysEqual(otherDeps, prevOtherDepsRef.current);

    if (expandedChanged && !otherDepsChanged) {
      // Only expanded list changed - incremental update
      return buildIncrementalUpdate(
        cachedVisibleNodesRef.current,
        cachedVisibleEdgesRef.current,
        allNodes,
        allEdges,
        currentExpandedSet,
        prevExpandedSet,
      );
    } else {
      // Full rebuild needed
      return buildFullGraph(allNodes, allEdges, currentExpandedSet);
    }
  }, [allNodes, allEdges, expandedList, ...otherDeps]);

  return { visibleNodes, visibleEdges };
};
```

#### Memoization 模式

```typescript
// Memoize node components to prevent unnecessary re-renders
const ProcessNode = memo(({ data, selected }: NodeProps) => {
  return (
    <div className={`process-node ${selected ? 'selected' : ''}`}>
      {data.label}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return (
    prevProps.data.label === nextProps.data.label &&
    prevProps.selected === nextProps.selected &&
    prevProps.data.isExpanded === nextProps.data.isExpanded
  );
});

// Memoize edge calculations
const styledEdges = useMemo(() => {
  return edges.map(edge => ({
    ...edge,
    style: {
      ...edge.style,
      strokeWidth: selectedEdgeId === edge.id ? 3 : 2,
      stroke: selectedEdgeId === edge.id ? '#3b82f6' : '#94a3b8',
    },
    animated: selectedEdgeId === edge.id,
  }));
}, [edges, selectedEdgeId]);
```

### 状态管理

管理复杂的 Node/Edge 状态，支持撤销/重做和持久化。

#### Reducer 模式

```typescript
type GraphAction =
  | { type: "SELECT_NODE"; payload: string }
  | { type: "SELECT_EDGE"; payload: string }
  | { type: "TOGGLE_EXPAND"; payload: string }
  | { type: "UPDATE_NODES"; payload: Node[] }
  | { type: "UPDATE_EDGES"; payload: Edge[] }
  | { type: "UNDO" }
  | { type: "REDO" };

const graphReducer = (state: GraphState, action: GraphAction): GraphState => {
  switch (action.type) {
    case "SELECT_NODE":
      return {
        ...state,
        selectedNodeId: action.payload,
        selectedEdgeId: null,
      };

    case "TOGGLE_EXPAND":
      const newExpanded = new Set(state.expandedNodeIds);
      if (newExpanded.has(action.payload)) {
        newExpanded.delete(action.payload);
      } else {
        newExpanded.add(action.payload);
      }
      return {
        ...state,
        expandedNodeIds: newExpanded,
        isDirty: true,
      };

    default:
      return state;
  }
};
```

#### 历史记录管理

```typescript
const useHistoryManager = (
  state: GraphState,
  dispatch: Dispatch<GraphAction>,
) => {
  const canUndo = state.historyIndex > 0;
  const canRedo = state.historyIndex < state.history.length - 1;

  const undo = useCallback(() => {
    if (canUndo) {
      const newIndex = state.historyIndex - 1;
      const historyEntry = state.history[newIndex];

      dispatch({
        type: "RESTORE_FROM_HISTORY",
        payload: {
          ...historyEntry,
          historyIndex: newIndex,
        },
      });
    }
  }, [canUndo, state.historyIndex, state.history]);

  const saveToHistory = useCallback(() => {
    dispatch({ type: "SAVE_TO_HISTORY" });
  }, [dispatch]);

  return { canUndo, canRedo, undo, redo, saveToHistory };
};
```

## 高级功能

### 自动布局集成

集成 Dagre 实现自动图布局：

```typescript
import dagre from "dagre";

const layoutOptions = {
  rankdir: "TB", // Top to Bottom
  nodesep: 100, // Node separation
  ranksep: 150, // Rank separation
  marginx: 50,
  marginy: 50,
  edgesep: 10,
};

const applyLayout = (nodes: Node[], edges: Edge[]) => {
  const g = new dagre.graphlib.Graph();
  g.setGraph(layoutOptions);
  g.setDefaultEdgeLabel(() => ({}));

  // Add nodes to graph
  nodes.forEach((node) => {
    g.setNode(node.id, { width: 200, height: 100 });
  });

  // Add edges to graph
  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  // Calculate layout
  dagre.layout(g);

  // Apply positions
  return nodes.map((node) => ({
    ...node,
    position: {
      x: g.node(node.id).x - 100,
      y: g.node(node.id).y - 50,
    },
  }));
};

// Debounce layout calculations
const debouncedLayout = useMemo(() => debounce(applyLayout, 150), []);
```

### 聚焦模式

隔离选中节点及其直接关联：

```typescript
const useFocusMode = (
  selectedNodeId: string,
  allNodes: Node[],
  allEdges: Edge[],
) => {
  return useMemo(() => {
    if (!selectedNodeId) return { nodes: allNodes, edges: allEdges };

    // Get direct connections
    const connectedNodeIds = new Set([selectedNodeId]);
    const focusedEdges: Edge[] = [];

    allEdges.forEach((edge) => {
      if (edge.source === selectedNodeId || edge.target === selectedNodeId) {
        focusedEdges.push(edge);
        connectedNodeIds.add(edge.source);
        connectedNodeIds.add(edge.target);
      }
    });

    // Get connected nodes
    const focusedNodes = allNodes.filter((n) => connectedNodeIds.has(n.id));

    return { nodes: focusedNodes, edges: focusedEdges };
  }, [selectedNodeId, allNodes, allEdges]);
};

// Smooth transitions for focus mode
const focusModeStyles = {
  transition: "all 0.3s ease-in-out",
  opacity: isInFocus ? 1 : 0.3,
  filter: isInFocus ? "none" : "blur(2px)",
};
```

### 搜索集成

搜索并导航到指定节点：

```typescript
const searchNodes = useCallback((nodes: Node[], query: string) => {
  if (!query.trim()) return [];

  const lowerQuery = query.toLowerCase();
  return nodes.filter(
    (node) =>
      node.data.label.toLowerCase().includes(lowerQuery) ||
      node.data.description?.toLowerCase().includes(lowerQuery),
  );
}, []);

const navigateToSearchResult = (nodeId: string) => {
  // Expand parent nodes
  const nodePath = calculateBreadcrumbPath(nodeId, allNodes);
  const parentIds = nodePath.slice(0, -1).map((n) => n.id);

  setExpandedIds((prev) => new Set([...prev, ...parentIds]));
  setSelectedNodeId(nodeId);

  // Fit view to node
  fitView({ nodes: [{ id: nodeId }], duration: 800 });
};
```

## 性能工具

### 图性能分析器

创建性能分析脚本：

```javascript
// scripts/graph-analyzer.js
class GraphAnalyzer {
  analyzeCode(content, filePath) {
    const analysis = {
      metrics: {
        nodeCount: this.countNodes(content),
        edgeCount: this.countEdges(content),
        renderTime: this.estimateRenderTime(content),
        memoryUsage: this.estimateMemoryUsage(content),
        complexity: this.calculateComplexity(content),
      },
      issues: [],
      optimizations: [],
      patterns: this.detectPatterns(content),
    };

    // Detect performance issues
    this.detectPerformanceIssues(analysis);

    // Suggest optimizations
    this.suggestOptimizations(analysis);

    return analysis;
  }

  countNodes(content) {
    const nodePatterns = [
      /nodes:\s*\[.*?\]/gs,
      /const\s+\w+\s*=\s*\[.*?id:.*?position:/gs,
    ];

    let totalCount = 0;
    nodePatterns.forEach((pattern) => {
      const matches = content.match(pattern);
      if (matches) {
        matches.forEach((match) => {
          const nodeMatches = match.match(/id:\s*['"`][^'"`]+['"`]/g);
          if (nodeMatches) {
            totalCount += nodeMatches.length;
          }
        });
      }
    });

    return totalCount;
  }

  estimateRenderTime(content) {
    const nodeCount = this.countNodes(content);
    const edgeCount = this.countEdges(content);

    // Base render time estimation (ms)
    const baseTime = 5;
    const nodeTime = nodeCount * 0.1;
    const edgeTime = edgeCount * 0.05;

    return baseTime + nodeTime + edgeTime;
  }

  detectPerformanceIssues(analysis) {
    const { metrics } = analysis;

    if (metrics.nodeCount > 500) {
      analysis.issues.push({
        type: "HIGH_NODE_COUNT",
        severity: "high",
        message: `Too many nodes (${metrics.nodeCount}). Consider virtualization.`,
        suggestion: "Implement virtualization or reduce visible nodes",
      });
    }

    if (metrics.renderTime > 16) {
      analysis.issues.push({
        type: "SLOW_RENDER",
        severity: "high",
        message: `Render time (${metrics.renderTime.toFixed(2)}ms) exceeds 60fps.`,
        suggestion: "Optimize with memoization and incremental rendering",
      });
    }
  }
}
```

## 最佳实践

### 性能准则

1. **使用 React.memo** 包裹 Node 组件，避免不必要的重渲染
2. **实现虚拟化** 处理 1000+ 节点的图
3. **防抖布局计算** 在快速交互时避免频繁重算
4. **使用 useCallback** 处理 Edge 的创建和操作函数
5. **定义完整的 TypeScript 类型** 约束 Node 和 Edge

### 内存管理

```typescript
// Use Map for O(1) lookups instead of array.find
const nodesById = useMemo(
  () => new Map(allNodes.map((n) => [n.id, n])),
  [allNodes],
);

// Cache layout results
const layoutCacheRef = useRef<Map<string, Node[]>>(new Map());

// Proper cleanup in useEffect
useEffect(() => {
  return () => {
    // Clean up any lingering references
    nodesMapRef.current.clear();
    edgesMapRef.current.clear();
  };
}, []);
```

### 状态优化

```typescript
// Use useRef for objects that shouldn't trigger re-renders
const autoSaveDataRef = useRef({
  nodes: [],
  edges: [],
  lastSaved: Date.now(),
});

// Update properties without breaking reference
const updateAutoSaveData = (newNodes: Node[], newEdges: Edge[]) => {
  autoSaveDataRef.current.nodes = newNodes;
  autoSaveDataRef.current.edges = newEdges;
  autoSaveDataRef.current.lastSaved = Date.now();
};
```

## 常见问题与解决方案

### 性能问题

- **问题**：展开节点时卡顿
- **方案**：实现增量渲染，配合变更检测

- **问题**：内存占用随时间增长
- **方案**：在 useEffect 中正确清理，临时数据使用 WeakMap

### 布局冲突

- **问题**：手动定位与自动布局冲突
- **方案**：使用受控的定位状态，分离布局模式

### 渲染问题

- **问题**：过度重渲染
- **方案**：配合稳定的依赖项使用 memo、useMemo 和 useCallback

- **问题**：布局计算缓慢
- **方案**：对布局计算做防抖处理并缓存结果

## 完整示例

```typescript
import React, { useState, useCallback, useMemo, useRef } from 'react';
import ReactFlow, { Node, Edge, useReactFlow } from 'reactflow';
import dagre from 'dagre';
import { debounce } from 'lodash';

interface GraphState {
  nodes: Node[];
  edges: Edge[];
  selectedNodeId: string | null;
  expandedNodeIds: Set<string>;
  history: GraphState[];
  historyIndex: number;
}

export default function InteractiveGraph() {
  const [state, setState] = useState<GraphState>({
    nodes: [],
    edges: [],
    selectedNodeId: null,
    expandedNodeIds: new Set(),
    history: [],
    historyIndex: 0,
  });

  const { fitView } = useReactFlow();
  const layoutCacheRef = useRef<Map<string, Node[]>>(new Map());

  // Memoized styled edges
  const styledEdges = useMemo(() => {
    return state.edges.map(edge => ({
      ...edge,
      style: {
        ...edge.style,
        strokeWidth: state.selectedNodeId === edge.source || state.selectedNodeId === edge.target ? 3 : 2,
        stroke: state.selectedNodeId === edge.source || state.selectedNodeId === edge.target ? '#3b82f6' : '#94a3b8',
      },
      animated: state.selectedNodeId === edge.source || state.selectedNodeId === edge.target,
    }));
  }, [state.edges, state.selectedNodeId]);

  // Debounced layout calculation
  const debouncedLayout = useMemo(
    () => debounce((nodes: Node[], edges: Edge[]) => {
      const cacheKey = generateLayoutCacheKey(nodes, edges);

      if (layoutCacheRef.current.has(cacheKey)) {
        return layoutCacheRef.current.get(cacheKey)!;
      }

      const layouted = applyDagreLayout(nodes, edges);
      layoutCacheRef.current.set(cacheKey, layouted);

      return layouted;
    }, 150),
    []
  );

  const handleNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setState(prev => ({
      ...prev,
      selectedNodeId: node.id,
    }));
  }, []);

  const handleToggleExpand = useCallback((nodeId: string) => {
    setState(prev => {
      const newExpanded = new Set(prev.expandedNodeIds);
      if (newExpanded.has(nodeId)) {
        newExpanded.delete(nodeId);
      } else {
        newExpanded.add(nodeId);
      }

      return {
        ...prev,
        expandedNodeIds: newExpanded,
      };
    });
  }, []);

  return (
    <ReactFlow
      nodes={state.nodes}
      edges={styledEdges}
      onNodeClick={handleNodeClick}
      fitView
    />
  );
}
```

本技能提供构建生产级 ReactFlow 应用所需的全部内容，涵盖层级导航、性能优化和高级状态管理模式。

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出结果不能替代针对特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
