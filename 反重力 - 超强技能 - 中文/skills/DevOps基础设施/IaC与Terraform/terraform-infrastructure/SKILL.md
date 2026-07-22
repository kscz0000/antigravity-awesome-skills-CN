---
name: terraform-infrastructure
description: "Terraform 基础设施即代码工作流，用于调配云资源、创建可复用模块和大规模管理基础设施。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Terraform 基础设施工作流

## 概述

使用 Terraform 进行基础设施即代码的专用工作流，涵盖资源调配、模块创建、状态管理和多环境部署。

## 适用场景

适用于以下场景：
- 调配云基础设施
- 创建 Terraform 模块
- 管理多环境基础设施
- 实施 IaC 最佳实践
- 设置 Terraform 工作流

## 工作流阶段

### 阶段 1：Terraform 初始化

#### 调用技能
- `terraform-skill` - Terraform 基础
- `terraform-specialist` - 高级 Terraform

#### 操作步骤
1. 初始化 Terraform
2. 配置后端
3. 设置提供商
4. 配置变量
5. 创建输出

#### 复制粘贴提示词
```
Use @terraform-skill to set up Terraform project
```

### 阶段 2：资源调配

#### 调用技能
- `terraform-module-library` - Terraform 模块
- `cloud-architect` - 云架构

#### 操作步骤
1. 设计基础设施
2. 创建资源定义
3. 配置网络
4. 设置计算资源
5. 添加存储

#### 复制粘贴提示词
```
Use @terraform-module-library to provision cloud resources
```

### 阶段 3：模块创建

#### 调用技能
- `terraform-module-library` - 模块创建

#### 操作步骤
1. 设计模块接口
2. 创建模块结构
3. 定义变量/输出
4. 添加文档
5. 测试模块

#### 复制粘贴提示词
```
Use @terraform-module-library to create reusable Terraform module
```

### 阶段 4：状态管理

#### 调用技能
- `terraform-specialist` - 状态管理

#### 操作步骤
1. 配置远程后端
2. 设置状态锁定
3. 实现工作空间
4. 配置状态访问
5. 设置备份

#### 复制粘贴提示词
```
Use @terraform-specialist to configure Terraform state
```

### 阶段 5：多环境

#### 调用技能
- `terraform-specialist` - 多环境

#### 操作步骤
1. 设计环境结构
2. 创建环境配置
3. 设置变量文件
4. 配置隔离
5. 测试部署

#### 复制粘贴提示词
```
Use @terraform-specialist to set up multi-environment Terraform
```

### 阶段 6：CI/CD 集成

#### 调用技能
- `cicd-automation-workflow-automate` - CI/CD
- `github-actions-templates` - GitHub Actions

#### 操作步骤
1. 创建 CI 流水线
2. 配置 plan/apply
3. 设置审批
4. 添加验证
5. 测试流水线

#### 复制粘贴提示词
```
Use @cicd-automation-workflow-automate to create Terraform CI/CD
```

### 阶段 7：安全

#### 调用技能
- `secrets-management` - 密钥管理
- `terraform-specialist` - 安全

#### 操作步骤
1. 配置密钥
2. 设置加密
3. 实施策略
4. 添加合规
5. 审计访问

#### 复制粘贴提示词
```
Use @secrets-management to secure Terraform secrets
```

## 质量门禁

- [ ] 资源已调配
- [ ] 模块正常工作
- [ ] 状态已配置
- [ ] 多环境已测试
- [ ] CI/CD 正常工作
- [ ] 安全已验证

## 相关工作流包

- `cloud-devops` - Cloud/DevOps
- `kubernetes-deployment` - Kubernetes
- `aws-infrastructure` - AWS 专用

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。