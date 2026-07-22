---
name: senior-architect
description: "面向高级架构师的完整工具包，集成现代工具和最佳实践。触发词：架构师、系统设计、架构图、依赖分析、项目架构、架构模式、技术选型"
risk: critical
source: community
date_added: "2026-02-27"
---

# 高级架构师

面向高级架构师的完整工具包，集成现代工具和最佳实践。

## 快速开始

### 核心能力

此技能通过自动化脚本提供三大核心能力：

```bash
# Script 1: Architecture Diagram Generator
python scripts/architecture_diagram_generator.py [options]

# Script 2: Project Architect
python scripts/project_architect.py [options]

# Script 3: Dependency Analyzer
python scripts/dependency_analyzer.py [options]
```

## 核心能力

### 1. 架构图生成器

用于架构图生成任务的自动化工具。

**功能特性：**
- 自动化脚手架搭建
- 内置最佳实践
- 可配置模板
- 质量检查

**用法：**
```bash
python scripts/architecture_diagram_generator.py <project-path> [options]
```

### 2. 项目架构师

综合分析与优化工具。

**功能特性：**
- 深度分析
- 性能指标
- 优化建议
- 自动修复

**用法：**
```bash
python scripts/project_architect.py <target-path> [--verbose]
```

### 3. 依赖分析器

用于专项任务的高级工具。

**功能特性：**
- 专家级自动化
- 自定义配置
- 即用型集成
- 生产级输出

**用法：**
```bash
python scripts/dependency_analyzer.py [arguments] [options]
```

## 参考文档

### 架构模式

完整指南见 `references/architecture_patterns.md`：

- 详细模式与实践
- 代码示例
- 最佳实践
- 应避免的反模式
- 真实场景

### 系统设计工作流

完整工作流文档见 `references/system_design_workflows.md`：

- 分步流程
- 优化策略
- 工具集成
- 性能调优
- 故障排查指南

### 技术决策指南

技术参考指南见 `references/tech_decision_guide.md`：

- 技术栈详情
- 配置示例
- 集成模式
- 安全考量
- 可扩展性指南

## 技术栈

**语言：** TypeScript、JavaScript、Python、Go、Swift、Kotlin
**前端：** React、Next.js、React Native、Flutter
**后端：** Node.js、Express、GraphQL、REST APIs
**数据库：** PostgreSQL、Prisma、NeonDB、Supabase
**DevOps：** Docker、Kubernetes、Terraform、GitHub Actions、CircleCI
**云平台：** AWS、GCP、Azure

## 开发工作流

### 1. 设置与配置

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. 运行质量检查

```bash
# Use the analyzer script
python scripts/project_architect.py .

# Review recommendations
# Apply fixes
```

### 3. 落地最佳实践

遵循以下文档中记录的模式和实践：
- `references/architecture_patterns.md`
- `references/system_design_workflows.md`
- `references/tech_decision_guide.md`

## 最佳实践总结

### 代码质量
- 遵循既定模式
- 编写全面的测试
- 记录决策
- 定期审查

### 性能
- 优化前先度量
- 合理使用缓存
- 优化关键路径
- 生产环境监控

### 安全
- 验证所有输入
- 使用参数化查询
- 实施正确的认证
- 保持依赖更新

### 可维护性
- 编写清晰的代码
- 使用一致的命名
- 添加有用的注释
- 保持简洁

## 常用命令

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/project_architect.py .
python scripts/dependency_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## 故障排查

### 常见问题

请查阅 `references/tech_decision_guide.md` 中的完整故障排查章节。

### 获取帮助

- 查阅参考文档
- 检查脚本输出信息
- 参考技术栈文档
- 查看错误日志

## 资源

- 模式参考：`references/architecture_patterns.md`
- 工作流指南：`references/system_design_workflows.md`
- 技术指南：`references/tech_decision_guide.md`
- 工具脚本：`scripts/` 目录

## 适用场景
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
