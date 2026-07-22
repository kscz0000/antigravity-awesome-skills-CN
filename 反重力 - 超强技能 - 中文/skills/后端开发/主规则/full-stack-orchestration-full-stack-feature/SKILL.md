---
name: full-stack-orchestration-full-stack-feature
description: "全栈功能编排技能，协调后端、前端和基础设施层的完整功能开发。适用于全栈功能开发、完整功能实现、端到端功能交付或全栈编排等场景。"
risk: unknown
source: community
date_added: "2026-02-27"
---

## 适用场景

- 执行全栈功能编排任务或工作流
- 需要全栈功能开发的指导、最佳实践或检查清单

## 不适用场景

- 任务与全栈功能编排无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和必要输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

使用现代 API 优先方法，跨后端、前端和基础设施层编排全栈功能开发：

[扩展思考：此工作流协调多个专业智能体，从架构设计到部署交付完整的全栈功能。遵循 API 优先开发原则，确保契约驱动开发——即 API 规范同时驱动后端实现和前端消费。每个阶段基于前一阶段的输出构建，形成具有合理关注点分离、全面测试和生产就绪部署的完整系统。工作流强调现代实践，如组件驱动 UI 开发、功能开关、可观测性和渐进式发布策略。]

## 第一阶段：架构与设计基础

### 1. 数据库架构设计
- 使用 Task 工具，subagent_type="database-design::database-architect"
- 提示词："为以下需求设计数据库模式和数据模型：$ARGUMENTS。考虑可扩展性、查询模式、索引策略和数据一致性要求。如修改现有模式，需包含迁移策略。提供逻辑数据模型和物理数据模型。"
- 预期输出：实体关系图、表结构、索引策略、迁移脚本、数据访问模式
- 上下文：初始需求和业务领域模型

### 2. 后端服务架构
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："为以下需求设计后端服务架构：$ARGUMENTS。基于前一步的数据库设计，创建服务边界，定义 API 契约（OpenAPI/GraphQL），设计认证/授权策略，并指定服务间通信模式。包含弹性模式（熔断器、重试）和缓存策略。"
- 预期输出：服务架构图、OpenAPI 规范、认证流程、缓存架构、消息队列设计（如适用）
- 上下文：步骤 1 的数据库模式、非功能性需求

### 3. 前端组件架构
- 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
- 提示词："为以下需求设计前端架构和组件结构：$ARGUMENTS。基于前一步的 API 契约，设计组件层次结构、状态管理方案（Redux/Zustand/Context）、路由结构和数据获取模式。包含无障碍要求和响应式设计策略。规划 Storybook 组件文档。"
- 预期输出：组件树图、状态管理设计、路由配置、设计系统集成方案、无障碍检查清单
- 上下文：步骤 2 的 API 规范、UI/UX 需求

## 第二阶段：并行实现

### 4. 后端服务实现
- 使用 Task 工具，subagent_type="python-development::python-pro"（或根据技术栈选择 "golang-pro"/"nodejs-expert"）
- 提示词："为以下需求实现后端服务：$ARGUMENTS。基于第一阶段的架构和 API 规范，构建 RESTful/GraphQL 端点，包含正确的验证、错误处理和日志记录。实现业务逻辑、数据访问层、认证中间件，以及与外部服务的集成。包含可观测性（结构化日志、指标、追踪）。"
- 预期输出：后端服务代码、API 端点、中间件、后台任务、单元测试、集成测试
- 上下文：第一阶段的架构设计、数据库模式

### 5. 前端实现
- 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
- 提示词："为以下需求实现前端应用：$ARGUMENTS。基于第一阶段的组件架构构建 React/Next.js 组件。实现状态管理、API 集成（含正确的错误处理和加载状态）、表单验证和响应式布局。为组件创建 Storybook stories。确保无障碍性（符合 WCAG 2.1 AA 标准）。"
- 预期输出：React 组件、状态管理实现、API 客户端代码、Storybook stories、响应式样式、无障碍实现
- 上下文：步骤 3 的组件架构、API 契约

### 6. 数据库实现与优化
- 使用 Task 工具，subagent_type="database-design::sql-pro"
- 提示词："为以下需求实现并优化数据库层：$ARGUMENTS。创建迁移脚本、存储过程（如需要），优化后端实现中识别的查询，设置合适的索引，并实现数据验证约束。包含数据库级安全措施和备份策略。"
- 预期输出：迁移脚本、优化后的查询、存储过程、索引定义、数据库安全配置
- 上下文：步骤 1 的数据库设计、后端实现的查询模式

## 第三阶段：集成与测试

### 7. API 契约测试
- 使用 Task 工具，subagent_type="test-automator"
- 提示词："为以下需求创建契约测试：$ARGUMENTS。实现 Pact/Dredd 测试以验证前后端之间的 API 契约。为所有 API 端点创建集成测试，测试认证流程，验证错误响应，并确保正确的 CORS 配置。包含负载测试场景。"
- 预期输出：契约测试套件、集成测试、负载测试场景、API 文档验证
- 上下文：第二阶段的 API 实现

### 8. 端到端测试
- 使用 Task 工具，subagent_type="test-automator"
- 提示词："为以下需求实现 E2E 测试：$ARGUMENTS。创建 Playwright/Cypress 测试，覆盖关键用户旅程、跨浏览器兼容性、移动端响应式和错误场景。测试功能开关集成、分析追踪和性能指标。包含视觉回归测试。"
- 预期输出：E2E 测试套件、视觉回归基线、性能基准、测试报告
- 上下文：第二阶段的前后端实现

### 9. 安全审计与加固
- 使用 Task 工具，subagent_type="security-auditor"
- 提示词："为以下需求执行安全审计：$ARGUMENTS。审查 API 安全（认证、授权、限流），检查 OWASP Top 10 漏洞，审计前端的 XSS/CSRF 风险，验证输入清理，并审查密钥管理。提供渗透测试结果和修复步骤。"
- 预期输出：安全审计报告、漏洞评估、修复建议、安全头配置
- 上下文：第二阶段的所有实现

## 第四阶段：部署与运维

### 10. 基础设施与 CI/CD 配置
- 使用 Task 工具，subagent_type="deployment-engineer"
- 提示词："为以下需求设置部署基础设施：$ARGUMENTS。创建 Docker 容器、Kubernetes manifests（或云平台特定配置），实现带自动化测试门禁的 CI/CD 流水线，设置功能开关（LaunchDarkly/Unleash），并配置监控/告警。包含蓝绿部署策略和回滚流程。"
- 预期输出：Dockerfile、K8s manifests、CI/CD 流水线配置、功能开关设置、IaC 模板（Terraform/CloudFormation）
- 上下文：前序阶段的所有实现和测试

### 11. 可观测性与监控
- 使用 Task 工具，subagent_type="deployment-engineer"
- 提示词："为以下需求实现可观测性栈：$ARGUMENTS。设置分布式追踪（OpenTelemetry），配置应用指标（Prometheus/DataDog），实现集中式日志（ELK/Splunk），创建关键指标仪表盘，并定义 SLI/SLO。包含告警规则和值班流程。"
- 预期输出：可观测性配置、仪表盘定义、告警规则、运维手册、SLI/SLO 定义
- 上下文：步骤 10 的基础设施配置

### 12. 性能优化
- 使用 Task 工具，subagent_type="performance-engineer"
- 提示词："为以下需求优化全栈性能：$ARGUMENTS。分析并优化数据库查询，实现缓存策略（Redis/CDN），优化前端包体积和加载性能，设置懒加载和代码分割，并调优后端服务性能。包含优化前后的指标对比。"
- 预期输出：性能改进、缓存配置、CDN 设置、优化后的构建产物、性能指标报告
- 上下文：步骤 11 的监控数据、负载测试结果

## 配置选项
- `stack`：指定技术栈（如 "React/FastAPI/PostgreSQL"、"Next.js/Django/MongoDB"）
- `deployment_target`：云平台（AWS/GCP/Azure）或本地部署
- `feature_flags`：启用/禁用功能开关集成
- `api_style`：REST 或 GraphQL
- `testing_depth`：全面或基础
- `compliance`：特定合规要求（GDPR、HIPAA、SOC2）

## 成功标准
- 所有 API 契约通过契约测试验证
- 前后端集成测试通过
- E2E 测试覆盖关键用户旅程
- 安全审计通过，无严重漏洞
- 性能指标达到定义的 SLO
- 可观测性栈捕获所有关键指标
- 功能开关配置完成，支持渐进式发布
- 所有组件文档完整
- CI/CD 流水线具备自动化质量门禁
- 验证零停机部署能力

## 协调说明
- 每个阶段基于前序阶段的输出构建
- 第二阶段的并行任务可同时运行，但必须在第三阶段前汇合
- 保持需求与实现之间的可追溯性
- 跨所有服务使用关联 ID 进行分布式追踪
- 将所有架构决策记录在 ADR 中
- 确保跨服务的错误处理和 API 响应一致

待实现功能：$ARGUMENTS

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家评审。
- 若缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
