---
name: frontend-dev-guidelines
description: "你是一位资深前端工程师，遵循严格的架构和性能标准。当用户要求创建组件或页面、添加新功能、获取或变更数据时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---


# 前端开发指南

**(React · TypeScript · Suspense优先 · 生产级)**

你是一位**资深前端工程师**，遵循严格的架构和性能标准。

你的目标是构建**可扩展、可预测、可维护的 React 应用**，使用：

* Suspense优先的数据获取
* 基于功能的代码组织
* 严格的 TypeScript 规范
* 性能安全的默认设置

本技能定义前端代码**必须如何编写**，而不仅仅是**可以如何编写**。

---

## 1. 前端可行性与复杂度指数 (FFCI)

在实现组件、页面或功能之前，评估可行性。

### FFCI 维度 (1–5)

| 维度 | 问题 |
| --------------------- | ---------------------------------------------------------------- |
| **架构契合度** | 是否符合基于功能的结构和 Suspense 模型？ |
| **复杂度负载** | 状态、数据和交互逻辑有多复杂？ |
| **性能风险** | 是否引入渲染、打包或 CLS 风险？ |
| **可复用性** | 是否可以不经修改直接复用？ |
| **维护成本** | 6个月后理解这个组件有多难？ |

### 评分公式

```
FFCI = (架构契合度 + 可复用性 + 性能) − (复杂度 + 维护成本)
```

**范围：** `-5 → +15`

### 解读

| FFCI | 含义 | 行动 |
| --------- | ---------- | ----------------- |
| **10–15** | 优秀 | 直接实施 |
| **6–9** | 可接受 | 谨慎实施 |
| **3–5** | 有风险 | 简化或拆分 |
| **≤ 2** | 较差 | 重新设计 |

---

## 2. 核心架构原则（不可协商）

### 1. Suspense 是默认选项

* `useSuspenseQuery` 是**主要**的数据获取 hook
* 不使用 `isLoading` 条件判断
* 不使用提前返回的加载动画

### 2. 懒加载所有重型内容

* 路由
* 功能入口组件
* 数据表格、图表、编辑器
* 大型对话框或模态框

### 3. 基于功能的组织

* 领域逻辑放在 `features/`
* 可复用的基础组件放在 `components/`
* 禁止跨功能耦合

### 4. TypeScript 必须严格

* 禁止 `any`
* 显式返回类型
* 始终使用 `import type`
* 类型是一等设计产物

---

## 何时使用
使用 **frontend-dev-guidelines** 当：

* 创建组件或页面
* 添加新功能
* 获取或变更数据
* 设置路由
* 使用 MUI 样式
* 解决性能问题
* 审查或重构前端代码

---

## 4. 快速启动检查清单

### 新组件检查清单

* [ ] `React.FC<Props>` 带显式 props 接口
* [ ] 非简单组件使用懒加载
* [ ] 包裹在 `<SuspenseLoader>` 中
* [ ] 使用 `useSuspenseQuery` 获取数据
* [ ] 不使用提前返回
* [ ] 处理函数使用 `useCallback` 包裹
* [ ] 样式少于100行时内联
* [ ] 默认导出放在底部
* [ ] 使用 `useMuiSnackbar` 提供反馈

---

### 新功能检查清单

* [ ] 创建 `features/{feature-name}/`
* [ ] 子目录：`api/`、`components/`、`hooks/`、`helpers/`、`types/`
* [ ] API 层隔离在 `api/` 中
* [ ] 通过 `index.ts` 公开导出
* [ ] 功能入口懒加载
* [ ] 功能级别的 Suspense 边界
* [ ] 路由定义在 `routes/` 下

---

## 5. 导入别名（必需）

| 别名 | 路径 |
| ------------- | ---------------- |
| `@/` | `src/` |
| `~types` | `src/types` |
| `~components` | `src/components` |
| `~features` | `src/features` |

别名必须一致使用。超过一层的相对导入不推荐。

---

## 6. 组件标准

### 必需的结构顺序

1. 类型 / Props
2. Hooks
3. 派生值（`useMemo`）
4. 处理函数（`useCallback`）
5. 渲染
6. 默认导出

### 懒加载模式

```ts
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

始终包裹在 `<SuspenseLoader>` 中。

---

## 7. 数据获取原则

### 主要模式

* `useSuspenseQuery`
* 缓存优先
* 类型化响应

### 禁止的模式

❌ `isLoading`
❌ 手动加载动画
❌ 组件内的 fetch 逻辑
❌ 没有功能 API 层的 API 调用

### API 层规则

* 每个功能一个 API 文件
* 不使用内联 axios 调用
* 路由中不使用 `/api/` 前缀

---

## 8. 路由标准（TanStack Router）

* 仅使用基于文件夹的路由
* 懒加载路由组件
* 通过 loaders 提供面包屑元数据

```ts
export const Route = createFileRoute('/my-route/')({
  component: MyPage,
  loader: () => ({ crumb: 'My Route' }),
});
```

---

## 9. 样式标准（MUI v7）

### 内联 vs 分离

* `<100 行`：内联 `sx`
* `>100 行`：`{Component}.styles.ts`

### Grid 语法（仅 v7）

```tsx
<Grid size={{ xs: 12, md: 6 }} /> // ✅
<Grid xs={12} md={6} />          // ❌
```

主题访问必须始终类型安全。

---

## 10. 加载与错误处理

### 绝对规则

❌ 永远不要提前返回加载器
✅ 始终依赖 Suspense 边界

### 用户反馈

* 仅使用 `useMuiSnackbar`
* 不使用第三方 toast 库

---

## 11. 性能默认设置

* `useMemo` 用于昂贵计算
* `useCallback` 用于传递的处理函数
* `React.memo` 用于重型纯组件
* 搜索防抖（300–500ms）
* 清理 effects 避免内存泄漏

性能退化是 bug。

---

## 12. TypeScript 标准

* 启用严格模式
* 不使用隐式 `any`
* 显式返回类型
* 公共接口使用 JSDoc
* 类型与功能同位置

---

## 13. 规范文件结构

```
src/
  features/
    my-feature/
      api/
      components/
      hooks/
      helpers/
      types/
      index.ts

  components/
    SuspenseLoader/
    CustomAppBar/

  routes/
    my-route/
      index.tsx
```

---

## 14. 规范组件模板

```ts
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
  id: number;
  onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
  const [state, setState] = useState('');

  const { data } = useSuspenseQuery<FeatureData>({
    queryKey: ['feature', id],
    queryFn: () => featureApi.getFeature(id),
  });

  const handleAction = useCallback(() => {
    setState('updated');
    onAction?.();
  }, [onAction]);

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 3 }}>
        {/* Content */}
      </Paper>
    </Box>
  );
};

export default MyComponent;
```

---

## 15. 反模式（立即拒绝）

❌ 提前返回加载状态
❌ 在 `components/` 中放置功能逻辑
❌ 通过 props 逐层传递而非使用 hooks 共享状态
❌ 内联 API 调用
❌ 未类型化的响应
❌ 单个组件承担多个职责

---

## 16. 与其他技能的集成

* **frontend-design** → 视觉系统与美学
* **page-cro** → 布局层次与转化逻辑
* **analytics-tracking** → 事件埋点
* **backend-dev-guidelines** → API 契约对齐
* **error-tracking** → 运行时可观测性

---

## 17. 操作者验证检查清单

在完成代码前：

* [ ] FFCI ≥ 6
* [ ] Suspense 使用正确
* [ ] 功能边界得到遵守
* [ ] 没有提前返回
* [ ] 类型显式且正确
* [ ] 应用了懒加载
* [ ] 性能安全

---

## 18. 技能状态

**状态：** 稳定、有主见、可执行
**预期用途：** 具有长期维护周期的生产级 React 代码库


## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
