---
name: development
description: "综合 Web、移动端和后端开发工作流，打包前端、后端、全栈和移动开发技能，实现端到端应用交付。触发词：开发工作流、全栈开发、Web开发、移动开发、后端开发、应用构建、项目脚手架、开发流程、端到端开发。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 开发工作流打包

## 概述

整合端到端软件开发工作流，覆盖 Web、移动端和后端开发。此打包编排从脚手架搭建到部署的生产就绪应用构建技能。

## 何时使用此工作流

以下情况使用此工作流：
- 构建新的 Web 或移动应用
- 为现有应用添加功能
- 重构或现代化遗留代码
- 使用最佳实践搭建新项目
- 全栈功能开发
- 跨平台应用开发

## 工作流阶段

### 阶段 1：项目设置与脚手架

#### 调用技能
- `app-builder` - 主应用构建编排器
- `senior-fullstack` - 全栈开发指导
- `environment-setup-guide` - 开发环境设置
- `concise-planning` - 任务规划与拆解

#### 操作
1. 确定项目类型（Web、移动端、全栈）
2. 选择技术栈
3. 搭建项目结构
4. 配置开发环境
5. 设置版本控制和 CI/CD

#### 复制粘贴提示词
```
Use @app-builder to scaffold a new React + Node.js full-stack application
```

```
Use @senior-fullstack to set up a Next.js 14 project with App Router
```

```
Use @environment-setup-guide to configure my development environment
```

### 阶段 2：前端开发

#### 调用技能
- `frontend-developer` - React/Next.js 组件开发
- `frontend-design` - UI/UX 设计实现
- `react-patterns` - 现代 React 模式
- `typescript-pro` - TypeScript 最佳实践
- `tailwind-patterns` - Tailwind CSS 样式
- `nextjs-app-router-patterns` - Next.js 14+ 模式

#### 操作
1. 设计组件架构
2. 实现 UI 组件
3. 设置状态管理
4. 配置路由
5. 应用样式和主题
6. 实现响应式设计

#### 复制粘贴提示词
```
Use @frontend-developer to create a dashboard component with React and TypeScript
```

```
Use @react-patterns to implement proper state management with Zustand
```

```
Use @tailwind-patterns to style components with a consistent design system
```

### 阶段 3：后端开发

#### 调用技能
- `backend-architect` - 后端架构设计
- `backend-dev-guidelines` - 后端开发标准
- `nodejs-backend-patterns` - Node.js/Express 模式
- `fastapi-pro` - FastAPI 开发
- `api-design-principles` - REST/GraphQL API 设计
- `auth-implementation-patterns` - 认证实现

#### 操作
1. 设计 API 架构
2. 实现 REST/GraphQL 端点
3. 设置数据库连接
4. 实现认证/授权
5. 配置中间件
6. 设置错误处理

#### 复制粘贴提示词
```
Use @backend-architect to design a microservices architecture for my application
```

```
Use @nodejs-backend-patterns to create Express.js API endpoints
```

```
Use @auth-implementation-patterns to implement JWT authentication
```

### 阶段 4：数据库开发

#### 调用技能
- `database-architect` - 数据库设计
- `database-design` - 模式设计原则
- `prisma-expert` - Prisma ORM
- `postgresql` - PostgreSQL 优化
- `neon-postgres` - 无服务器 Postgres

#### 操作
1. 设计数据库模式
2. 创建迁移
3. 设置 ORM
4. 优化查询
5. 配置连接池

#### 复制粘贴提示词
```
Use @database-architect to design a normalized schema for an e-commerce platform
```

```
Use @prisma-expert to set up Prisma ORM with TypeScript
```

### 阶段 5：测试

#### 调用技能
- `test-driven-development` - TDD 工作流
- `javascript-testing-patterns` - Jest/Vitest 测试
- `python-testing-patterns` - pytest 测试
- `e2e-testing-patterns` - Playwright/Cypress E2E
- `playwright-skill` - 浏览器自动化测试

#### 操作
1. 编写单元测试
2. 创建集成测试
3. 设置 E2E 测试
4. 配置 CI 测试运行器
5. 达成覆盖率目标

#### 复制粘贴提示词
```
Use @test-driven-development to implement features with TDD
```

```
Use @playwright-skill to create E2E tests for critical user flows
```

### 阶段 6：代码质量与审查

#### 调用技能
- `code-reviewer` - AI 驱动代码审查
- `clean-code` - 整洁代码原则
- `lint-and-validate` - Lint 和验证
- `security-scanning-security-sast` - 静态安全分析

#### 操作
1. 运行 Linter 和格式化工具
2. 执行代码审查
3. 修复代码质量问题
4. 运行安全扫描
5. 处理漏洞

#### 复制粘贴提示词
```
Use @code-reviewer to review my pull request
```

```
Use @lint-and-validate to check code quality
```

### 阶段 7：构建与部署

#### 调用技能
- `deployment-engineer` - 部署编排
- `docker-expert` - 容器化
- `vercel-deployment` - Vercel 部署
- `github-actions-templates` - CI/CD 工作流
- `cicd-automation-workflow-automate` - CI/CD 自动化

#### 操作
1. 创建 Dockerfile
2. 配置构建流水线
3. 设置部署工作流
4. 配置环境变量
5. 部署到生产环境

#### 复制粘贴提示词
```
Use @docker-expert to containerize my application
```

```
Use @vercel-deployment to deploy my Next.js app to production
```

```
Use @github-actions-templates to set up CI/CD pipeline
```

## 技术栈特定工作流

### React/Next.js 开发
```
Skills: frontend-developer, react-patterns, nextjs-app-router-patterns, typescript-pro, tailwind-patterns
```

### Python/FastAPI 开发
```
Skills: fastapi-pro, python-pro, python-patterns, pydantic-models-py
```

### Node.js/Express 开发
```
Skills: nodejs-backend-patterns, javascript-pro, typescript-pro, express (via nodejs-backend-patterns)
```

### 全栈开发
```
Skills: senior-fullstack, app-builder, frontend-developer, backend-architect, database-architect
```

### 移动端开发
```
Skills: mobile-developer, react-native-architecture, flutter-expert, ios-developer
```

## 质量门控

进入下一阶段前，验证：
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 安全扫描通过
- [ ] Lint/格式化检查通过
- [ ] 文档已更新

## 相关工作流打包

- `wordpress` - WordPress 专项开发
- `security-audit` - 安全测试工作流
- `testing-qa` - 综合测试工作流
- `documentation` - 文档生成工作流

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 输出内容不替代环境特定验证、测试或专家审查。
- 若缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清。
