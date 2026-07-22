---
name: documentation
description: "文档生成工作流，涵盖 API 文档、架构文档、README 文件、代码注释和技术写作。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 文档工作流套件

## 概述

全面的文档工作流，用于从代码库生成 API 文档、架构文档、README 文件、代码注释和技术内容。

## 何时使用此工作流

在以下情况下使用此工作流：
- 创建项目文档
- 生成 API 文档
- 编写架构文档
- 记录代码
- 创建用户指南
- 维护 Wiki

## 工作流阶段

### 阶段 1：文档规划

#### 要调用的技能
- `docs-architect` - 文档架构
- `documentation-templates` - 文档模板

#### 操作
1. 识别文档需求
2. 选择文档工具
3. 规划文档结构
4. 定义风格指南
5. 搭建文档站点

#### 可复制提示词
```
Use @docs-architect to plan documentation structure
```

```
Use @documentation-templates to set up documentation
```

### 阶段 2：API 文档

#### 要调用的技能
- `api-documenter` - API 文档
- `api-documentation-generator` - 自动生成
- `openapi-spec-generation` - OpenAPI 规范

#### 操作
1. 提取 API 端点
2. 生成 OpenAPI 规范
3. 创建 API 参考
4. 添加使用示例
5. 设置自动生成

#### 可复制提示词
```
Use @api-documenter to generate API documentation
```

```
Use @openapi-spec-generation to create OpenAPI specs
```

### 阶段 3：架构文档

#### 要调用的技能
- `c4-architecture-c4-architecture` - C4 架构
- `c4-context` - 上下文图
- `c4-container` - 容器图
- `c4-component` - 组件图
- `c4-code` - 代码图
- `mermaid-expert` - Mermaid 图表

#### 操作
1. 创建 C4 图
2. 记录架构
3. 生成时序图
4. 记录数据流
5. 创建部署文档

#### 可复制提示词
```
Use @c4-architecture-c4-architecture to create C4 diagrams
```

```
Use @mermaid-expert to create architecture diagrams
```

### 阶段 4：代码文档

#### 要调用的技能
- `code-documentation-code-explain` - 代码解释
- `code-documentation-doc-generate` - 文档生成
- `documentation-generation-doc-generate` - 自动生成

#### 操作
1. 提取代码注释
2. 生成 JSDoc/TSDoc
3. 创建类型文档
4. 记录函数
5. 添加使用示例

#### 可复制提示词
```
Use @code-documentation-code-explain to explain code
```

```
Use @code-documentation-doc-generate to generate docs
```

### 阶段 5：README 和入门指南

#### 要调用的技能
- `readme` - README 生成
- `environment-setup-guide` - 设置指南
- `tutorial-engineer` - 教程创建

#### 操作
1. 创建 README
2. 编写入门指南
3. 记录安装步骤
4. 添加使用示例
5. 创建故障排除指南

#### 可复制提示词
```
Use @readme to create project README
```

```
Use @tutorial-engineer to create tutorials
```

### 阶段 6：Wiki 和知识库

#### 要调用的技能
- `wiki-architect` - Wiki 架构
- `wiki-page-writer` - Wiki 页面
- `wiki-onboarding` - 入职文档
- `wiki-qa` - Wiki 问答
- `wiki-researcher` - Wiki 研究
- `wiki-vitepress` - VitePress Wiki

#### 操作
1. 设计 Wiki 结构
2. 创建 Wiki 页面
3. 编写入职指南
4. 记录流程
5. 搭建 Wiki 站点

#### 可复制提示词
```
Use @wiki-architect to design wiki structure
```

```
Use @wiki-page-writer to create wiki pages
```

```
Use @wiki-onboarding to create onboarding docs
```

### 阶段 7：变更日志和发布说明

#### 要调用的技能
- `changelog-automation` - 变更日志生成
- `wiki-changelog` - 从 Git 生成变更日志

#### 操作
1. 提取提交历史
2. 分类变更
3. 生成变更日志
4. 创建发布说明
5. 发布更新

#### 可复制提示词
```
Use @changelog-automation to generate changelog
```

```
Use @wiki-changelog to create release notes
```

### 阶段 8：文档维护

#### 要调用的技能
- `doc-coauthoring` - 协作写作
- `reference-builder` - 参考文档

#### 操作
1. 审查文档
2. 更新过时内容
3. 修复失效链接
4. 添加新功能说明
5. 收集反馈

#### 可复制提示词
```
Use @doc-coauthoring to collaborate on docs
```

## 文档类型

### 代码级
- JSDoc/TSDoc 注释
- 函数文档
- 类型定义
- 示例代码

### API 文档
- 端点参考
- 请求/响应模式
- 认证指南
- SDK 文档

### 架构文档
- 系统概览
- 组件图
- 数据流图
- 部署架构

### 用户文档
- 入门指南
- 用户手册
- 教程
- 常见问题

### 流程文档
- 运维手册
- 入职指南
- 标准操作程序
- 决策记录

## 质量门禁

- [ ] 所有 API 已记录
- [ ] 架构图保持最新
- [ ] README 已更新
- [ ] 代码注释有帮助
- [ ] 示例可运行
- [ ] 链接有效

## 相关工作流套件

- `development` - 开发工作流
- `testing-qa` - 文档测试
- `ai-ml` - AI 文档

## 限制
- 仅当任务明确匹配上述描述的范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
