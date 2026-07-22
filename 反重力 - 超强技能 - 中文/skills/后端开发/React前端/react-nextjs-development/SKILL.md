---
name: react-nextjs-development
description: "React 和 Next.js 14+ 应用开发，使用 App Router、Server Components、TypeScript、Tailwind CSS 和现代前端模式。触发词：React开发、Next.js开发、前端开发"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# React/Next.js 开发工作流

## 概述

构建 React 和 Next.js 14+ 应用程序的专业工作流，涵盖 App Router、Server Components、TypeScript 和 Tailwind CSS 等现代开发模式。

## 何时使用此工作流

在以下场景中使用此工作流：
- 构建新的 React 应用程序
- 使用 App Router 创建 Next.js 14+ 项目
- 实现 Server Components
- 设置 TypeScript 与 React 集成
- 使用 Tailwind CSS 进行样式设计
- 构建全栈 Next.js 应用程序

## 工作流阶段

### 阶段 1：项目设置

#### 调用技能
- `app-builder` - 应用程序脚手架
- `senior-fullstack` - 全栈开发指导
- `nextjs-app-router-patterns` - Next.js 14+ 开发模式
- `typescript-pro` - TypeScript 配置

#### 操作步骤
1. 选择项目类型（React SPA、Next.js 应用）
2. 选择构建工具（Vite、Next.js、Create React App）
3. 搭建项目结构
4. 配置 TypeScript
5. 设置 ESLint 和 Prettier

#### 复制粘贴提示词
```
Use @app-builder to scaffold a new Next.js 14 project with App Router
```

```
Use @nextjs-app-router-patterns to set up Server Components
```

### 阶段 2：组件架构

#### 调用技能
- `frontend-developer` - 组件开发
- `react-patterns` - React 开发模式
- `react-state-management` - 状态管理
- `react-ui-patterns` - UI 模式

#### 操作步骤
1. 设计组件层次结构
2. 创建基础组件
3. 实现布局组件
4. 设置状态管理
5. 创建自定义 hooks

#### 复制粘贴提示词
```
Use @frontend-developer to create reusable React components
```

```
Use @react-patterns to implement proper component composition
```

```
Use @react-state-management to set up Zustand store
```

### 阶段 3：样式与设计

#### 调用技能
- `frontend-design` - UI 设计
- `tailwind-patterns` - Tailwind CSS
- `tailwind-design-system` - 设计系统
- `core-components` - 组件库

#### 操作步骤
1. 设置 Tailwind CSS
2. 配置设计令牌
3. 创建工具类
4. 构建组件样式
5. 实现响应式设计

#### 复制粘贴提示词
```
Use @tailwind-patterns to style components with Tailwind CSS v4
```

```
Use @frontend-design to create a modern dashboard UI
```

### 阶段 4：数据获取

#### 调用技能
- `nextjs-app-router-patterns` - Server Components
- `react-state-management` - React Query
- `api-patterns` - API 集成

#### 操作步骤
1. 实现 Server Components
2. 设置 React Query/SWR
3. 创建 API 客户端
4. 处理加载状态
5. 实现错误边界

#### 复制粘贴提示词
```
Use @nextjs-app-router-patterns to implement Server Components data fetching
```

### 阶段 5：路由与导航

#### 调用技能
- `nextjs-app-router-patterns` - App Router
- `nextjs-best-practices` - Next.js 开发模式

#### 操作步骤
1. 设置基于文件的路由
2. 创建动态路由
3. 实现嵌套路由
4. 添加路由守卫
5. 配置重定向

#### 复制粘贴提示词
```
Use @nextjs-app-router-patterns to set up parallel routes and intercepting routes
```

### 阶段 6：表单与验证

#### 调用技能
- `frontend-developer` - 表单开发
- `typescript-advanced-types` - 类型验证
- `react-ui-patterns` - 表单模式

#### 操作步骤
1. 选择表单库（React Hook Form、Formik）
2. 设置验证（Zod、Yup）
3. 创建表单组件
4. 处理提交
5. 实现错误处理

#### 复制粘贴提示词
```
Use @frontend-developer to create forms with React Hook Form and Zod
```

### 阶段 7：测试

#### 调用技能
- `javascript-testing-patterns` - Jest/Vitest
- `playwright-skill` - E2E 测试
- `e2e-testing-patterns` - E2E 模式

#### 操作步骤
1. 设置测试框架
2. 编写单元测试
3. 创建组件测试
4. 实现 E2E 测试
5. 配置 CI 集成

#### 复制粘贴提示词
```
Use @javascript-testing-patterns to write Vitest tests
```

```
Use @playwright-skill to create E2E tests for critical flows
```

### 阶段 8：构建与部署

#### 调用技能
- `vercel-deployment` - Vercel 部署
- `vercel-deploy-claimable` - Vercel 部署
- `web-performance-optimization` - 性能优化

#### 操作步骤
1. 配置构建设置
2. 优化打包体积
3. 设置环境变量
4. 部署到 Vercel
5. 配置预览部署

#### 复制粘贴提示词
```
Use @vercel-deployment to deploy Next.js app to production
```

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 14+、React 18+ |
| 语言 | TypeScript 5+ |
| 样式 | Tailwind CSS v4 |
| 状态管理 | Zustand、React Query |
| 表单 | React Hook Form、Zod |
| 测试 | Vitest、Playwright |
| 部署 | Vercel |

## 质量门

- [ ] TypeScript 编译无错误
- [ ] 所有测试通过
- [ ] 代码规范检查通过
- [ ] 性能指标达标（LCP、CLS、FID）
- [ ] 无障碍检查通过（WCAG 2.1）
- [ ] 响应式设计验证

## 相关工作流包

- `development` - 通用开发
- `testing-qa` - 测试工作流
- `documentation` - 文档
- `typescript-development` - TypeScript 模式

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为替代环境特定验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。