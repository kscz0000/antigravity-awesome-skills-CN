---
name: api-documentation
description: "API文档工作流，用于生成OpenAPI规范、创建开发者指南和维护全面的API文档。触发词：API文档、OpenAPI、Swagger、开发者指南、API规范、接口文档、API文档生成"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# API文档工作流

## 概述

用于创建全面API文档的专项工作流，包括OpenAPI/Swagger规范、开发者指南、代码示例和交互式文档。

## 何时使用此工作流

在以下情况下使用此工作流：
- 创建API文档
- 生成OpenAPI规范
- 编写开发者指南
- 添加代码示例
- 搭建API门户

## 工作流阶段

### 阶段1：API发现

#### 调用技能
- `api-documenter` - API文档
- `api-design-principles` - API设计

#### 操作步骤
1. 盘点端点
2. 记录请求/响应
3. 识别认证方式
4. 映射错误码
5. 记录速率限制

#### 复制粘贴提示词
```
Use @api-documenter to discover and document API endpoints
```

### 阶段2：OpenAPI规范

#### 调用技能
- `openapi-spec-generation` - OpenAPI
- `api-documenter` - API规范

#### 操作步骤
1. 创建OpenAPI模式
2. 定义路径
3. 添加模式定义
4. 配置安全机制
5. 添加示例

#### 复制粘贴提示词
```
Use @openapi-spec-generation to create OpenAPI specification
```

### 阶段3：开发者指南

#### 调用技能
- `api-documentation-generator` - 文档生成
- `documentation-templates` - 文档模板

#### 操作步骤
1. 创建入门指南
2. 编写认证指南
3. 记录常用模式
4. 添加故障排查
5. 创建FAQ

#### 复制粘贴提示词
```
Use @api-documentation-generator to create developer guide
```

### 阶段4：代码示例

#### 调用技能
- `api-documenter` - 代码示例
- `tutorial-engineer` - 教程

#### 操作步骤
1. 创建示例请求
2. 编写SDK示例
3. 添加curl示例
4. 创建教程
5. 测试示例

#### 复制粘贴提示词
```
Use @api-documenter to generate code examples
```

### 阶段5：交互式文档

#### 调用技能
- `api-documenter` - 交互式文档

#### 操作步骤
1. 搭建Swagger UI
2. 配置Redoc
3. 添加试用功能
4. 测试交互性
5. 部署文档

#### 复制粘贴提示词
```
Use @api-documenter to set up interactive documentation
```

### 阶段6：文档站点

#### 调用技能
- `docs-architect` - 文档架构
- `wiki-page-writer` - 文档编写

#### 操作步骤
1. 选择平台
2. 设计结构
3. 创建页面
4. 添加导航
5. 配置搜索

#### 复制粘贴提示词
```
Use @docs-architect to design API documentation site
```

### 阶段7：维护

#### 调用技能
- `api-documenter` - 文档维护

#### 操作步骤
1. 设置自动生成
2. 配置验证
3. 添加审核流程
4. 安排更新计划
5. 监控反馈

#### 复制粘贴提示词
```
Use @api-documenter to set up automated doc generation
```

## 质量检查清单

- [ ] OpenAPI规范完整
- [ ] 开发者指南已编写
- [ ] 代码示例可运行
- [ ] 交互式文档可用
- [ ] 文档已部署

## 相关工作流包

- `documentation` - 文档
- `api-development` - API开发
- `development` - 开发

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
