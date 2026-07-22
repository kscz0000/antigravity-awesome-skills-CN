---
name: python-fastapi-development
description: "Python FastAPI后端开发，包含异步模式、SQLAlchemy、Pydantic、认证和生产级API模式。触发词：FastAPI开发、异步模式、SQLAlchemy、Pydantic、API认证"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Python/FastAPI 开发工作流

## 概述

用于构建生产级Python后端的专业工作流，基于FastAPI框架，包含异步模式、SQLAlchemy ORM、Pydantic验证和完整的API模式。

## 何时使用此工作流

在以下情况下使用此工作流：
- 使用FastAPI构建新的REST API
- 创建异步Python后端
- 使用SQLAlchemy实现数据库集成
- 设置API认证
- 开发微服务

## 工作流阶段

### 阶段1：项目设置

#### 调用技能
- `app-builder` - 应用程序脚手架
- `python-development-python-scaffold` - Python脚手架
- `fastapi-templates` - FastAPI模板
- `uv-package-manager` - 包管理

#### 操作
1. 设置Python环境（uv/poetry）
2. 创建项目结构
3. 配置FastAPI应用
4. 设置日志
5. 配置环境变量

#### 复制粘贴提示
```
Use @fastapi-templates to scaffold a new FastAPI project
```

```
Use @python-development-python-scaffold to set up Python project structure
```

### 阶段2：数据库设置

#### 调用技能
- `prisma-expert` - Prisma ORM（替代方案）
- `database-design` - Schema设计
- `postgresql` - PostgreSQL设置
- `pydantic-models-py` - Pydantic模型

#### 操作
1. 设计数据库Schema
2. 设置SQLAlchemy模型
3. 创建数据库连接
4. 配置迁移（Alembic）
5. 设置会话管理

#### 复制粘贴提示
```
Use @database-design to design PostgreSQL schema
```

```
Use @pydantic-models-py to create Pydantic models for API
```

### 阶段3：API路由

#### 调用技能
- `fastapi-router-py` - FastAPI路由器
- `api-design-principles` - API设计
- `api-patterns` - API模式

#### 操作
1. 设计API端点
2. 创建API路由器
3. 实现CRUD操作
4. 添加请求验证
5. 配置响应模型

#### 复制粘贴提示
```
Use @fastapi-router-py to create API endpoints with CRUD operations
```

```
Use @api-design-principles to design RESTful API
```

### 阶段4：认证

#### 调用技能
- `auth-implementation-patterns` - 认证
- `api-security-best-practices` - API安全

#### 操作
1. 选择认证策略（JWT、OAuth2）
2. 实现用户注册
3. 设置登录端点
4. 创建认证中间件
5. 添加密码哈希

#### 复制粘贴提示
```
Use @auth-implementation-patterns to implement JWT authentication
```

### 阶段5：错误处理

#### 调用技能
- `fastapi-pro` - FastAPI模式
- `error-handling-patterns` - 错误处理

#### 操作
1. 创建自定义异常
2. 设置异常处理器
3. 实现错误响应
4. 添加请求日志
5. 配置错误跟踪

#### 复制粘贴提示
```
Use @fastapi-pro to implement comprehensive error handling
```

### 阶段6：测试

#### 调用技能
- `python-testing-patterns` - pytest测试
- `api-testing-observability-api-mock` - API测试

#### 操作
1. 设置pytest
2. 创建测试夹具
3. 编写单元测试
4. 实现集成测试
5. 配置测试数据库

#### 复制粘贴提示
```
Use @python-testing-patterns to write pytest tests for FastAPI
```

### 阶段7：文档

#### 调用技能
- `api-documenter` - API文档
- `openapi-spec-generation` - OpenAPI规范

#### 操作
1. 配置OpenAPI Schema
2. 添加端点文档
3. 创建使用示例
4. 设置API版本控制
5. 生成API文档

#### 复制粘贴提示
```
Use @api-documenter to generate comprehensive API documentation
```

### 阶段8：部署

#### 调用技能
- `deployment-engineer` - 部署
- `docker-expert` - 容器化

#### 操作
1. 创建Dockerfile
2. 设置docker-compose
3. 配置生产环境设置
4. 设置反向代理
5. 部署到云

#### 复制粘贴提示
```
Use @docker-expert to containerize FastAPI application
```

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | FastAPI |
| 语言 | Python 3.11+ |
| ORM | SQLAlchemy 2.0 |
| 验证 | Pydantic v2 |
| 数据库 | PostgreSQL |
| 迁移 | Alembic |
| 认证 | JWT、OAuth2 |
| 测试 | pytest |

## 质量门禁

- [ ] 所有测试通过（>80%覆盖率）
- [ ] 类型检查通过（mypy）
- [ ] 代码规范检查通过（ruff、black）
- [ ] API文档完整
- [ ] 安全扫描通过
- [ ] 性能基准达标

## 相关工作流包

- `development` - 通用开发
- `database` - 数据库操作
- `security-audit` - 安全测试
- `api-development` - API模式

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。